from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fortune_training.combined_chart_application.product_shell_assets import (
    DESKTOP_PRODUCT_SHELL_SCHEMA,
)
from fortune_training.desktop_application.distribution import (
    DESKTOP_APPLICATION_ID,
    DESKTOP_APPLICATION_VERSION,
    FORBIDDEN_REPOSITORY_DATA_PREFIXES,
    REQUIRED_RUNTIME_REPOSITORY_FILES,
    build_metadata,
    repository_data_manifest,
)
from fortune_training.desktop_application.launcher import (
    build_desktop_server,
    serve_desktop,
)
from fortune_training.desktop_application.platform_acceptance import (
    WINDOWS_BINARY_SMOKE_SCHEMA,
    run_windows_binary_smoke,
)
from fortune_training.desktop_application.runtime import resolve_runtime_repository_root


REPO_ROOT = Path(__file__).resolve().parents[1]


class _FakeServer:
    def __init__(self) -> None:
        self.server_address = ("127.0.0.1", 43123)
        self.served = False
        self.closed = False

    def serve_forever(self) -> None:
        self.served = True

    def server_close(self) -> None:
        self.closed = True


class WindowsPortableDesktopLauncherR1Test(unittest.TestCase):
    def test_packaged_runtime_root_ignores_current_working_directory(self) -> None:
        with tempfile.TemporaryDirectory() as payload_dir, tempfile.TemporaryDirectory() as cwd_dir:
            payload_root = Path(payload_dir)
            config = payload_root / "runtime" / "config" / "time-calendar-policies.json"
            config.parent.mkdir(parents=True)
            config.write_text("{}\n", encoding="utf-8")
            original = Path.cwd()
            try:
                os.chdir(cwd_dir)
                resolved = resolve_runtime_repository_root(
                    resource_root=payload_root,
                    packaged=True,
                )
            finally:
                os.chdir(original)
            self.assertEqual(resolved, (payload_root / "runtime").resolve())

    def test_repository_data_inventory_is_explicit_and_excludes_forbidden_domains(self) -> None:
        self.assertEqual(
            REQUIRED_RUNTIME_REPOSITORY_FILES,
            ("config/time-calendar-policies.json",),
        )
        manifest = repository_data_manifest()
        self.assertEqual(
            manifest["runtime_repository_files"],
            ["config/time-calendar-policies.json"],
        )
        for relative in manifest["runtime_repository_files"]:
            normalized = str(relative).replace("\\", "/")
            self.assertFalse(
                any(normalized.startswith(prefix) for prefix in FORBIDDEN_REPOSITORY_DATA_PREFIXES),
                normalized,
            )
        self.assertFalse(manifest["automatic_git_pull"])
        self.assertFalse(manifest["prediction_training_runtime"])

    def test_build_metadata_carries_version_and_exact_source_commit(self) -> None:
        source_commit = "A" * 40
        payload = build_metadata(source_commit)
        self.assertEqual(payload["application_id"], DESKTOP_APPLICATION_ID)
        self.assertEqual(payload["application_version"], DESKTOP_APPLICATION_VERSION)
        self.assertEqual(payload["source_commit"], "a" * 40)
        with self.assertRaises(ValueError):
            build_metadata("abc123")

    def test_desktop_server_requests_ephemeral_loopback_binding(self) -> None:
        from fortune_training.desktop_application import launcher

        server = _FakeServer()
        calls: list[tuple[Path, int]] = []

        def fake_builder(repository_root: Path, *, port: int):
            calls.append((repository_root, port))
            return server

        with patch.object(launcher, "resolve_runtime_repository_root", return_value=REPO_ROOT), patch.object(
            launcher,
            "build_workbench_server",
            side_effect=fake_builder,
        ):
            built = build_desktop_server()

        self.assertIs(built, server)
        self.assertEqual(calls, [(REPO_ROOT, 0)])
        self.assertEqual(server.server_address[0], "127.0.0.1")
        self.assertGreater(server.server_address[1], 0)

    def test_browser_launch_can_be_suppressed_and_server_closes(self) -> None:
        server = _FakeServer()
        opened: list[str] = []
        result = serve_desktop(
            server,
            open_browser=False,
            browser_opener=lambda url: opened.append(url),
        )
        self.assertEqual(result, 0)
        self.assertTrue(server.served)
        self.assertTrue(server.closed)
        self.assertEqual(opened, [])

    def test_windows_build_contract_is_onedir_windowed_and_exact_commit_bound(self) -> None:
        script = (REPO_ROOT / "scripts" / "build-windows-portable.ps1").read_text(encoding="utf-8")
        workflow = (REPO_ROOT / ".github" / "workflows" / "windows-portable.yml").read_text(encoding="utf-8")
        self.assertIn("--onedir", script)
        self.assertIn("--windowed", script)
        self.assertIn("--contents-directory _internal", script)
        self.assertIn("--collect-data geonamescache", script)
        self.assertIn("--collect-data tzdata", script)
        self.assertIn("--source-commit $SourceCommit", script)
        self.assertIn("github.event.pull_request.head.sha || github.sha", workflow)
        self.assertIn("ref: ${{ env.SOURCE_COMMIT }}", workflow)
        self.assertIn("FortuneChart-windows-x64.zip", workflow)

    def test_current_runtime_config_is_valid_json_and_matches_inventory(self) -> None:
        for relative in REQUIRED_RUNTIME_REPOSITORY_FILES:
            path = REPO_ROOT / relative
            self.assertTrue(path.is_file(), relative)
            if path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))

    def test_binary_smoke_runs_loopback_health_and_combined_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            metadata_root = Path(temp_dir)
            (metadata_root / "desktop-build-metadata.json").write_text(
                json.dumps(build_metadata("a" * 40)),
                encoding="utf-8",
            )
            server = build_desktop_server()
            receipt = run_windows_binary_smoke(server, runtime_root=metadata_root)
        self.assertEqual(receipt["schema"], WINDOWS_BINARY_SMOKE_SCHEMA)
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["source_commit"], "a" * 40)
        self.assertEqual(receipt["bind_policy"], "LOOPBACK_ONLY")
        self.assertEqual(len(receipt["combined_manifest_hash"]), 64)
        self.assertEqual(receipt["desktop_product_shell_schema"], DESKTOP_PRODUCT_SHELL_SCHEMA)
        self.assertEqual(receipt["desktop_product_shell_asset_count"], 3)

    def test_windows_workflow_smokes_executables_from_emitted_zip(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "windows-portable.yml").read_text(
            encoding="utf-8"
        )
        for expected in (
            "Run emitted Windows binary platform smoke",
            "Expand-Archive -LiteralPath $zip",
            "FortuneChart.exe",
            "FortuneChartUpdater.exe",
            "--platform-smoke-receipt",
            "FORTUNE-CHART-WINDOWS-BINARY-SMOKE-R1",
            "FORTUNE-CHART-WINDOWS-UPDATER-BINARY-SMOKE-R1",
            "binary smoke ZIP SHA-256 mismatch",
            "binary smoke source commit mismatch",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, workflow)


if __name__ == "__main__":
    unittest.main()
