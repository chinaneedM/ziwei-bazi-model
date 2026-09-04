from __future__ import annotations

import hashlib
import io
import json
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from fortune_training.desktop_application.distribution import (
    DESKTOP_APPLICATION_ID,
    DESKTOP_APPLICATION_VERSION,
)
from fortune_training.desktop_application.launcher import run_startup_update_check
from fortune_training.desktop_application.updater import (
    WINDOWS_UPDATER_BINARY_SMOKE_SCHEMA,
    apply_update_transaction,
    close_stale_same_install_processes,
    main as updater_main,
)
from fortune_training.desktop_application.updates import (
    UPDATE_ARCHIVE_ROOT,
    UPDATE_ASSET_NAME,
    UPDATE_CHANNEL,
    UPDATE_MANIFEST_SCHEMA,
    UPDATE_MANIFEST_URL,
    UPDATE_PROTOCOL_VERSION,
    PreparedUpdate,
    UpdateSecurityError,
    _stream_download_asset,
    extract_verified_archive,
    is_newer_version,
    maybe_launch_verified_update,
    release_update_manifest,
    spawn_standalone_updater,
    validate_update_manifest,
    verify_staged_bundle,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "a" * 40


def _manifest_payload(*, version: str = "0.2.1", sha256: str = "b" * 64, size: int = 123) -> dict[str, object]:
    return {
        "schema": UPDATE_MANIFEST_SCHEMA,
        "application_id": DESKTOP_APPLICATION_ID,
        "channel": UPDATE_CHANNEL,
        "version": version,
        "source_commit": SOURCE_COMMIT,
        "asset_url": (
            "https://github.com/chinaneedM/ziwei-bazi-model/releases/download/"
            f"fortune-chart-v{version}/{UPDATE_ASSET_NAME}"
        ),
        "asset_sha256": sha256,
        "asset_size": size,
        "archive_root": UPDATE_ARCHIVE_ROOT,
        "updater_protocol": UPDATE_PROTOCOL_VERSION,
    }


def _write_bundle(root: Path, *, version: str = "0.2.1", source_commit: str = SOURCE_COMMIT) -> None:
    metadata_root = root / "_internal" / "runtime"
    metadata_root.mkdir(parents=True, exist_ok=True)
    (root / "FortuneChart.exe").write_bytes(b"app")
    (root / "FortuneChartUpdater.exe").write_bytes(b"updater")
    (metadata_root / "desktop-build-metadata.json").write_text(
        json.dumps(
            {
                "application_id": DESKTOP_APPLICATION_ID,
                "application_version": version,
                "source_commit": source_commit,
            }
        ),
        encoding="utf-8",
    )


class _BytesResponse:
    def __init__(self, data: bytes) -> None:
        self._stream = io.BytesIO(data)

    def read(self, amount: int = -1) -> bytes:
        return self._stream.read(amount)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


class _AliveProcess:
    def poll(self):
        return None


class WindowsVerifiedAutoUpdateR1Tests(unittest.TestCase):
    def test_updater_binary_smoke_receipt_is_non_mutating(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            receipt_path = Path(temp_dir) / "updater-smoke.json"
            self.assertEqual(
                updater_main(["--platform-smoke-receipt", str(receipt_path)]),
                0,
            )
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        self.assertEqual(receipt["schema"], WINDOWS_UPDATER_BINARY_SMOKE_SCHEMA)
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["application_version"], DESKTOP_APPLICATION_VERSION)
        self.assertFalse(receipt["mutation_performed"])

    def test_manifest_is_closed_stable_and_fixed_to_repository_release_route(self) -> None:
        manifest = validate_update_manifest(_manifest_payload())
        self.assertEqual(manifest.version, "0.2.1")
        self.assertEqual(
            UPDATE_MANIFEST_URL,
            "https://github.com/chinaneedM/ziwei-bazi-model/releases/download/fortune-chart-stable/fortune-chart-update.json",
        )

        extra = _manifest_payload()
        extra["unexpected"] = True
        with self.assertRaises(UpdateSecurityError):
            validate_update_manifest(extra)

        wrong_route = _manifest_payload()
        wrong_route["asset_url"] = "https://example.com/FortuneChart-windows-x64.zip"
        with self.assertRaises(UpdateSecurityError):
            validate_update_manifest(wrong_route)

    def test_semver_is_monotonic_and_rejects_prerelease_or_downgrade(self) -> None:
        self.assertTrue(is_newer_version("0.2.1", "0.2.0"))
        self.assertFalse(is_newer_version("0.2.0", "0.2.0"))
        self.assertFalse(is_newer_version("0.1.9", "0.2.0"))
        with self.assertRaises(UpdateSecurityError):
            is_newer_version("0.2.1-beta", "0.2.0")

    def test_release_manifest_binds_tag_commit_hash_size_and_asset_url(self) -> None:
        payload = release_update_manifest(
            version="0.2.1",
            source_commit=SOURCE_COMMIT.upper(),
            asset_sha256=("B" * 64),
            asset_size=100,
            release_tag="fortune-chart-v0.2.1",
        )
        self.assertEqual(payload["source_commit"], SOURCE_COMMIT)
        self.assertEqual(payload["asset_sha256"], "b" * 64)
        self.assertEqual(
            payload["asset_url"],
            "https://github.com/chinaneedM/ziwei-bazi-model/releases/download/fortune-chart-v0.2.1/FortuneChart-windows-x64.zip",
        )
        with self.assertRaises(ValueError):
            release_update_manifest(
                version="0.2.1",
                source_commit=SOURCE_COMMIT,
                asset_sha256="b" * 64,
                asset_size=100,
                release_tag="fortune-chart-v0.2.2",
            )

    def test_download_rejects_declared_size_and_sha_mismatch(self) -> None:
        data = b"verified update bytes"
        correct = hashlib.sha256(data).hexdigest()
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "update.zip"
            manifest = validate_update_manifest(_manifest_payload(sha256=correct, size=len(data)))
            with patch(
                "fortune_training.desktop_application.updates.urllib.request.urlopen",
                return_value=_BytesResponse(data),
            ):
                _stream_download_asset(manifest, destination)
            self.assertEqual(destination.read_bytes(), data)

            wrong_hash = validate_update_manifest(_manifest_payload(sha256="0" * 64, size=len(data)))
            with patch(
                "fortune_training.desktop_application.updates.urllib.request.urlopen",
                return_value=_BytesResponse(data),
            ):
                with self.assertRaises(UpdateSecurityError):
                    _stream_download_asset(wrong_hash, destination)

            wrong_size = validate_update_manifest(_manifest_payload(sha256=correct, size=len(data) + 1))
            with patch(
                "fortune_training.desktop_application.updates.urllib.request.urlopen",
                return_value=_BytesResponse(data),
            ):
                with self.assertRaises(UpdateSecurityError):
                    _stream_download_asset(wrong_size, destination)

    def test_archive_rejects_traversal_case_collision_and_symlink(self) -> None:
        cases: list[zipfile.ZipInfo | str] = [
            "FortuneChart/../escape.txt",
        ]
        symlink = zipfile.ZipInfo("FortuneChart/link")
        symlink.create_system = 3
        symlink.external_attr = (stat.S_IFLNK | 0o777) << 16
        cases.append(symlink)

        for bad_member in cases:
            with self.subTest(member=str(bad_member)), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                archive_path = root / "bad.zip"
                stage = root / "stage"
                stage.mkdir()
                with zipfile.ZipFile(archive_path, "w") as archive:
                    archive.writestr(bad_member, b"x")
                with self.assertRaises(UpdateSecurityError):
                    extract_verified_archive(archive_path, stage)

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            archive_path = root / "collision.zip"
            stage = root / "stage"
            stage.mkdir()
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("FortuneChart/A.txt", b"a")
                archive.writestr("FortuneChart/a.txt", b"b")
            with self.assertRaises(UpdateSecurityError):
                extract_verified_archive(archive_path, stage)

    def test_staged_bundle_metadata_must_match_manifest(self) -> None:
        manifest = validate_update_manifest(_manifest_payload())
        with tempfile.TemporaryDirectory() as temp_dir:
            bundle = Path(temp_dir) / "FortuneChart"
            bundle.mkdir()
            _write_bundle(bundle, version="0.2.0")
            with self.assertRaises(UpdateSecurityError):
                verify_staged_bundle(bundle, manifest)

    def test_transaction_rolls_back_complete_old_tree_if_activation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            parent = Path(temp_dir)
            install = parent / "RenamedPortableFolder"
            install.mkdir()
            (install / "old-marker.txt").write_text("known-good", encoding="utf-8")
            staging = parent / ".RenamedPortableFolder.update-test"
            staged = staging / "FortuneChart"
            staged.mkdir(parents=True)
            _write_bundle(staged)

            def fail_relaunch(_exe: Path):
                raise RuntimeError("simulated activation failure")

            with self.assertRaises(RuntimeError):
                apply_update_transaction(
                    install_root=install,
                    staged_bundle=staged,
                    expected_version="0.2.1",
                    expected_source_commit=SOURCE_COMMIT,
                    relauncher=fail_relaunch,
                    health_wait_seconds=0,
                )
            self.assertEqual(
                (install / "old-marker.txt").read_text(encoding="utf-8"),
                "known-good",
            )
            self.assertFalse((install / "FortuneChart.exe").exists())

    def test_transaction_activates_staged_tree_and_supports_renamed_install_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            parent = Path(temp_dir)
            install = parent / "D-drive-user-name"
            install.mkdir()
            (install / "old-marker.txt").write_text("old", encoding="utf-8")
            staging = parent / ".D-drive-user-name.update-test"
            staged = staging / "FortuneChart"
            staged.mkdir(parents=True)
            _write_bundle(staged)

            activated = apply_update_transaction(
                install_root=install,
                staged_bundle=staged,
                expected_version="0.2.1",
                expected_source_commit=SOURCE_COMMIT,
                relauncher=lambda _exe: _AliveProcess(),
                health_wait_seconds=0,
            )
            self.assertEqual(activated, install.resolve())
            self.assertTrue((install / "FortuneChart.exe").is_file())
            self.assertFalse((install / "old-marker.txt").exists())

    def test_stale_process_scan_is_safe_noop_without_same_install_process(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            self.assertEqual(close_stale_same_install_processes(Path(temp_dir)), 0)

    def test_standalone_updater_launch_cwd_is_outside_install_root(self) -> None:
        manifest = validate_update_manifest(_manifest_payload(version="0.2.2"))
        with tempfile.TemporaryDirectory() as temp_dir:
            parent = Path(temp_dir)
            install = parent / "FortuneChart"
            install.mkdir()
            updater_source = install / "FortuneChartUpdater.exe"
            updater_source.write_bytes(b"updater")
            staging = parent / ".FortuneChart.update-test"
            staged = staging / "FortuneChart"
            staged.mkdir(parents=True)
            prepared = PreparedUpdate(
                manifest=manifest,
                staging_root=staging,
                staged_bundle=staged,
            )
            temp_updater_root = parent / "standalone-updater"
            temp_updater_root.mkdir()
            calls: list[tuple[list[str], dict[str, object]]] = []

            def fake_popen(args, **kwargs):
                calls.append((args, kwargs))
                return object()

            with patch(
                "fortune_training.desktop_application.updates.tempfile.mkdtemp",
                return_value=str(temp_updater_root),
            ):
                spawn_standalone_updater(
                    prepared,
                    install_root=install,
                    updater_source=updater_source,
                    parent_pid=12345,
                    popen=fake_popen,
                )

            self.assertEqual(len(calls), 1)
            args, kwargs = calls[0]
            self.assertEqual(Path(args[0]).parent.resolve(), temp_updater_root.resolve())
            self.assertEqual(Path(str(kwargs["cwd"])).resolve(), install.parent.resolve())
            self.assertNotEqual(Path(str(kwargs["cwd"])).resolve(), install.resolve())

    def test_source_execution_and_explicit_recovery_switch_never_touch_network(self) -> None:
        self.assertFalse(maybe_launch_verified_update(packaged=False))
        with patch("fortune_training.desktop_application.launcher.maybe_launch_verified_update") as updater:
            self.assertFalse(run_startup_update_check(disabled=True))
            updater.assert_not_called()

    def test_post_update_version_notice_is_gated_to_post_update_relaunch(self) -> None:
        from fortune_training.desktop_application import launcher

        fake_server = object()
        with patch.object(launcher, "_notify_post_update_version") as notice, patch.object(
            launcher,
            "run_startup_update_check",
            return_value=False,
        ) as update_check, patch.object(
            launcher,
            "build_desktop_server",
            return_value=fake_server,
        ), patch.object(
            launcher,
            "serve_desktop",
            return_value=0,
        ):
            self.assertEqual(launcher.main(["--post-update", "--no-browser"]), 0)
            notice.assert_called_once_with()
            update_check.assert_called_once_with(disabled=True)

        with patch.object(launcher, "_notify_post_update_version") as notice, patch.object(
            launcher,
            "run_startup_update_check",
            return_value=False,
        ) as update_check, patch.object(
            launcher,
            "build_desktop_server",
            return_value=fake_server,
        ), patch.object(
            launcher,
            "serve_desktop",
            return_value=0,
        ):
            self.assertEqual(launcher.main(["--no-browser"]), 0)
            notice.assert_not_called()
            update_check.assert_called_once_with(disabled=False)

    def test_build_and_release_contract_produces_standalone_updater_and_verified_manifest(self) -> None:
        script = (REPO_ROOT / "scripts" / "build-windows-portable.ps1").read_text(encoding="utf-8")
        workflow = (REPO_ROOT / ".github" / "workflows" / "windows-portable.yml").read_text(encoding="utf-8")
        self.assertIn("--onefile", script)
        self.assertIn("--name FortuneChartUpdater", script)
        self.assertIn("FortuneChartUpdater.exe", script)
        self.assertIn("fortune-chart-update.json", script)
        self.assertIn("fortune_training.desktop_application.updates", script)
        self.assertIn("tags:", workflow)
        self.assertIn('"fortune-chart-v*"', workflow)
        self.assertIn("gh release create", workflow)
        self.assertIn("fortune-chart-stable", workflow)
        self.assertIn("gh release upload", workflow)
        self.assertIn("--clobber", workflow)
        self.assertIn("test_windows_verified_auto_update_r1.py", workflow)
        self.assertIn("asset_sha256", workflow)
        self.assertEqual(DESKTOP_APPLICATION_VERSION, "0.2.4")


if __name__ == "__main__":
    unittest.main()
