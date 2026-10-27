from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable, Protocol

from .distribution import (
    DESKTOP_APPLICATION_ID,
    DESKTOP_APPLICATION_VERSION,
)

UPDATE_MANIFEST_SCHEMA = "FORTUNE-CHART-WINDOWS-UPDATE-MANIFEST-R1"
UPDATE_CHANNEL = "stable"
UPDATE_PROTOCOL_VERSION = 1
UPDATE_ARCHIVE_ROOT = "FortuneChart"
UPDATE_ASSET_NAME = "FortuneChart-windows-x64.zip"
UPDATE_MANIFEST_ASSET_NAME = "fortune-chart-update.json"
UPDATE_REPOSITORY = "chinaneedM/ziwei-bazi-model"
UPDATE_CHANNEL_RELEASE_TAG = "fortune-chart-stable"
UPDATE_MANIFEST_URL = (
    "https://github.com/chinaneedM/ziwei-bazi-model/"
    "releases/download/fortune-chart-stable/fortune-chart-update.json"
)

MAX_MANIFEST_BYTES = 64 * 1024
MAX_ASSET_BYTES = 512 * 1024 * 1024
MAX_ARCHIVE_ENTRIES = 20_000
MAX_ARCHIVE_UNCOMPRESSED_BYTES = 2 * 1024 * 1024 * 1024
MANIFEST_TIMEOUT_SECONDS = 3.0
ASSET_TIMEOUT_SECONDS = 60.0

_SEMVER_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SOURCE_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
_RELEASE_TAG_RE = re.compile(r"^fortune-chart-v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


class UpdateError(RuntimeError):
    pass


class UpdateUnavailable(UpdateError):
    """The remote update service could not be reached; current app may continue."""


class UpdateSecurityError(UpdateError):
    """Remote or staged update data violated the closed update contract."""


@dataclass(frozen=True)
class UpdateManifest:
    version: str
    source_commit: str
    asset_url: str
    asset_sha256: str
    asset_size: int
    archive_root: str = UPDATE_ARCHIVE_ROOT
    updater_protocol: int = UPDATE_PROTOCOL_VERSION


@dataclass(frozen=True)
class PreparedUpdate:
    manifest: UpdateManifest
    staging_root: Path
    staged_bundle: Path


class _Response(Protocol):
    def read(self, amount: int = -1) -> bytes: ...
    def __enter__(self): ...
    def __exit__(self, exc_type, exc, tb): ...


Fetcher = Callable[[str, int, float], bytes]


def parse_semver(value: str) -> tuple[int, int, int]:
    match = _SEMVER_RE.fullmatch(value.strip())
    if not match:
        raise UpdateSecurityError(f"invalid stable semantic version: {value!r}")
    return tuple(int(part) for part in match.groups())


def is_newer_version(candidate: str, current: str) -> bool:
    return parse_semver(candidate) > parse_semver(current)


def _validate_release_asset_url(url: str, *, version: str) -> str:
    expected = (
        f"https://github.com/{UPDATE_REPOSITORY}/releases/download/"
        f"fortune-chart-v{version}/{UPDATE_ASSET_NAME}"
    )
    if url != expected:
        raise UpdateSecurityError("update asset URL is outside the fixed GitHub release route")
    return url


def validate_update_manifest(payload: object) -> UpdateManifest:
    if not isinstance(payload, dict):
        raise UpdateSecurityError("update manifest must be a JSON object")
    required = {
        "schema",
        "application_id",
        "channel",
        "version",
        "source_commit",
        "asset_url",
        "asset_sha256",
        "asset_size",
        "archive_root",
        "updater_protocol",
    }
    if set(payload) != required:
        raise UpdateSecurityError("update manifest keys do not match the closed R1 schema")
    if payload["schema"] != UPDATE_MANIFEST_SCHEMA:
        raise UpdateSecurityError("unexpected update manifest schema")
    if payload["application_id"] != DESKTOP_APPLICATION_ID:
        raise UpdateSecurityError("update manifest application identity mismatch")
    if payload["channel"] != UPDATE_CHANNEL:
        raise UpdateSecurityError("only the stable update channel is accepted")
    version = str(payload["version"])
    parse_semver(version)
    source_commit = str(payload["source_commit"]).lower()
    if not _SOURCE_COMMIT_RE.fullmatch(source_commit):
        raise UpdateSecurityError("update source_commit must be a full Git SHA")
    asset_sha256 = str(payload["asset_sha256"]).lower()
    if not _SHA256_RE.fullmatch(asset_sha256):
        raise UpdateSecurityError("update asset SHA-256 must be 64 lowercase hex characters")
    asset_size = payload["asset_size"]
    if not isinstance(asset_size, int) or isinstance(asset_size, bool) or not (0 < asset_size <= MAX_ASSET_BYTES):
        raise UpdateSecurityError("update asset size is invalid or exceeds the R1 bound")
    if payload["archive_root"] != UPDATE_ARCHIVE_ROOT:
        raise UpdateSecurityError("unexpected update archive root")
    if payload["updater_protocol"] != UPDATE_PROTOCOL_VERSION:
        raise UpdateSecurityError("unsupported updater protocol")
    asset_url = _validate_release_asset_url(str(payload["asset_url"]), version=version)
    return UpdateManifest(
        version=version,
        source_commit=source_commit,
        asset_url=asset_url,
        asset_sha256=asset_sha256,
        asset_size=asset_size,
    )


def release_update_manifest(
    *,
    version: str,
    source_commit: str,
    asset_sha256: str,
    asset_size: int,
    release_tag: str,
) -> dict[str, object]:
    parse_semver(version)
    normalized_commit = source_commit.strip().lower()
    normalized_hash = asset_sha256.strip().lower()
    if not _SOURCE_COMMIT_RE.fullmatch(normalized_commit):
        raise ValueError("source_commit must be a full 40-character lowercase/uppercase Git SHA")
    if not _SHA256_RE.fullmatch(normalized_hash):
        raise ValueError("asset_sha256 must be 64 lowercase/uppercase hex characters")
    if not isinstance(asset_size, int) or isinstance(asset_size, bool) or not (0 < asset_size <= MAX_ASSET_BYTES):
        raise ValueError("asset_size must be within the R1 asset bound")
    match = _RELEASE_TAG_RE.fullmatch(release_tag)
    if not match or release_tag != f"fortune-chart-v{version}":
        raise ValueError("release_tag must exactly match fortune-chart-v<application version>")
    asset_url = (
        f"https://github.com/{UPDATE_REPOSITORY}/releases/download/"
        f"{release_tag}/{UPDATE_ASSET_NAME}"
    )
    payload = {
        "schema": UPDATE_MANIFEST_SCHEMA,
        "application_id": DESKTOP_APPLICATION_ID,
        "channel": UPDATE_CHANNEL,
        "version": version,
        "source_commit": normalized_commit,
        "asset_url": asset_url,
        "asset_sha256": normalized_hash,
        "asset_size": asset_size,
        "archive_root": UPDATE_ARCHIVE_ROOT,
        "updater_protocol": UPDATE_PROTOCOL_VERSION,
    }
    validate_update_manifest(payload)
    return payload


def _fetch_small_https(url: str, max_bytes: int, timeout: float) -> bytes:
    if not url.startswith("https://"):
        raise UpdateSecurityError("update transport must use HTTPS")
    request = urllib.request.Request(
        url,
        headers={"User-Agent": f"FortuneChart/{DESKTOP_APPLICATION_VERSION}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read(max_bytes + 1)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise UpdateUnavailable(str(exc)) from exc
    if len(data) > max_bytes:
        raise UpdateSecurityError("update manifest exceeds size bound")
    return data


def fetch_update_manifest(*, fetcher: Fetcher = _fetch_small_https) -> UpdateManifest:
    try:
        raw = fetcher(UPDATE_MANIFEST_URL, MAX_MANIFEST_BYTES, MANIFEST_TIMEOUT_SECONDS)
    except UpdateError:
        raise
    except Exception as exc:
        raise UpdateUnavailable(str(exc)) from exc
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UpdateSecurityError("update manifest is not valid UTF-8 JSON") from exc
    return validate_update_manifest(payload)


def read_packaged_build_metadata(resource_root: Path) -> dict[str, object]:
    path = Path(resource_root) / "runtime" / "desktop-build-metadata.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise UpdateSecurityError("packaged desktop build metadata is unavailable") from exc
    if not isinstance(payload, dict):
        raise UpdateSecurityError("packaged desktop build metadata must be an object")
    if payload.get("application_id") != DESKTOP_APPLICATION_ID:
        raise UpdateSecurityError("packaged desktop application identity mismatch")
    version = payload.get("application_version")
    source_commit = str(payload.get("source_commit", "")).lower()
    if not isinstance(version, str):
        raise UpdateSecurityError("packaged desktop version is missing")
    parse_semver(version)
    if not _SOURCE_COMMIT_RE.fullmatch(source_commit):
        raise UpdateSecurityError("packaged source commit is invalid")
    return payload


def _stream_download_asset(manifest: UpdateManifest, destination: Path) -> None:
    request = urllib.request.Request(
        manifest.asset_url,
        headers={"User-Agent": f"FortuneChart/{DESKTOP_APPLICATION_VERSION}"},
        method="GET",
    )
    digest = hashlib.sha256()
    total = 0
    try:
        with urllib.request.urlopen(request, timeout=ASSET_TIMEOUT_SECONDS) as response, destination.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > manifest.asset_size or total > MAX_ASSET_BYTES:
                    raise UpdateSecurityError("downloaded update exceeds declared size")
                digest.update(chunk)
                output.write(chunk)
    except UpdateSecurityError:
        raise
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise UpdateUnavailable(str(exc)) from exc
    if total != manifest.asset_size:
        raise UpdateSecurityError("downloaded update size does not match manifest")
    if digest.hexdigest() != manifest.asset_sha256:
        raise UpdateSecurityError("downloaded update SHA-256 does not match manifest")


def _zip_entry_is_symlink(info: zipfile.ZipInfo) -> bool:
    unix_mode = (info.external_attr >> 16) & 0xFFFF
    return stat.S_IFMT(unix_mode) == stat.S_IFLNK


def _validated_member_parts(info: zipfile.ZipInfo) -> tuple[str, ...]:
    name = info.filename
    if not name or "\\" in name or "\x00" in name:
        raise UpdateSecurityError("update archive contains an invalid member path")
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise UpdateSecurityError("update archive contains path traversal")
    if any(":" in part for part in path.parts):
        raise UpdateSecurityError("update archive contains a drive/stream-qualified path")
    if path.parts[0] != UPDATE_ARCHIVE_ROOT:
        raise UpdateSecurityError("update archive contains an unexpected top-level root")
    if _zip_entry_is_symlink(info):
        raise UpdateSecurityError("update archive symlinks are not permitted")
    return path.parts


def extract_verified_archive(archive_path: Path, staging_root: Path) -> Path:
    staging_root = Path(staging_root).resolve()
    try:
        with zipfile.ZipFile(archive_path, "r") as archive:
            infos = archive.infolist()
            if not infos or len(infos) > MAX_ARCHIVE_ENTRIES:
                raise UpdateSecurityError("update archive entry count is invalid")
            total_uncompressed = sum(info.file_size for info in infos)
            if total_uncompressed > MAX_ARCHIVE_UNCOMPRESSED_BYTES:
                raise UpdateSecurityError("update archive expanded size exceeds R1 bound")
            seen_paths: set[str] = set()
            for info in infos:
                parts = _validated_member_parts(info)
                collision_key = "/".join(parts).casefold().rstrip("/")
                if collision_key in seen_paths:
                    raise UpdateSecurityError("update archive contains duplicate/case-colliding paths")
                seen_paths.add(collision_key)
                target = staging_root.joinpath(*parts)
                target_resolved = target.resolve()
                try:
                    target_resolved.relative_to(staging_root)
                except ValueError as exc:
                    raise UpdateSecurityError("update archive escaped staging root") from exc
                if info.is_dir():
                    target_resolved.mkdir(parents=True, exist_ok=True)
                    continue
                target_resolved.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(info, "r") as source, target_resolved.open("wb") as output:
                    shutil.copyfileobj(source, output, length=1024 * 1024)
    except zipfile.BadZipFile as exc:
        raise UpdateSecurityError("update asset is not a valid ZIP archive") from exc
    return staging_root / UPDATE_ARCHIVE_ROOT


def verify_staged_bundle(staged_bundle: Path, manifest: UpdateManifest) -> None:
    root = Path(staged_bundle)
    required = (
        root / "FortuneChart.exe",
        root / "FortuneChartUpdater.exe",
        root / "_internal" / "runtime" / "desktop-build-metadata.json",
    )
    if any(not path.is_file() for path in required):
        raise UpdateSecurityError("staged update is missing required desktop files")
    metadata_path = required[2]
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise UpdateSecurityError("staged update build metadata is invalid") from exc
    if not isinstance(metadata, dict):
        raise UpdateSecurityError("staged update metadata must be an object")
    if metadata.get("application_id") != DESKTOP_APPLICATION_ID:
        raise UpdateSecurityError("staged application identity mismatch")
    if metadata.get("application_version") != manifest.version:
        raise UpdateSecurityError("staged application version does not match manifest")
    if str(metadata.get("source_commit", "")).lower() != manifest.source_commit:
        raise UpdateSecurityError("staged source commit does not match manifest")


def prepare_update(
    manifest: UpdateManifest,
    *,
    install_root: Path,
    downloader: Callable[[UpdateManifest, Path], None] = _stream_download_asset,
) -> PreparedUpdate:
    install_root = Path(install_root).resolve()
    parent = install_root.parent
    try:
        staging_root = Path(tempfile.mkdtemp(prefix=f".{install_root.name}.update-", dir=parent))
    except OSError as exc:
        raise UpdateError("portable application parent directory is not writable for update staging") from exc
    archive_path = staging_root / UPDATE_ASSET_NAME
    try:
        downloader(manifest, archive_path)
        staged_bundle = extract_verified_archive(archive_path, staging_root)
        verify_staged_bundle(staged_bundle, manifest)
        return PreparedUpdate(manifest=manifest, staging_root=staging_root, staged_bundle=staged_bundle)
    except Exception:
        shutil.rmtree(staging_root, ignore_errors=True)
        raise


def _creationflags_no_window() -> int:
    return int(getattr(subprocess, "CREATE_NO_WINDOW", 0))


def spawn_standalone_updater(
    prepared: PreparedUpdate,
    *,
    install_root: Path,
    updater_source: Path,
    parent_pid: int,
    popen: Callable[..., object] = subprocess.Popen,
) -> None:
    updater_source = Path(updater_source).resolve()
    install_root = Path(install_root).resolve()
    if updater_source.parent != install_root or updater_source.name != "FortuneChartUpdater.exe":
        raise UpdateSecurityError("updater executable is not bound to the current installation root")
    if not updater_source.is_file():
        raise UpdateSecurityError("current installation is missing FortuneChartUpdater.exe")
    temp_root = Path(tempfile.mkdtemp(prefix="fortunechart-updater-"))
    temp_updater = temp_root / "FortuneChartUpdater.exe"
    try:
        shutil.copy2(updater_source, temp_updater)
        args = [
            str(temp_updater),
            "--parent-pid",
            str(parent_pid),
            "--install-root",
            str(install_root),
            "--staging-root",
            str(prepared.staging_root),
            "--staged-bundle",
            str(prepared.staged_bundle),
            "--expected-version",
            prepared.manifest.version,
            "--expected-source-commit",
            prepared.manifest.source_commit,
        ]
        popen(
            args,
            close_fds=True,
            creationflags=_creationflags_no_window(),
            cwd=str(install_root.parent),
        )
    except Exception:
        shutil.rmtree(temp_root, ignore_errors=True)
        raise


def maybe_launch_verified_update(
    *,
    packaged: bool | None = None,
    executable: Path | None = None,
    resource_root: Path | None = None,
    fetcher: Fetcher = _fetch_small_https,
    downloader: Callable[[UpdateManifest, Path], None] = _stream_download_asset,
    popen: Callable[..., object] = subprocess.Popen,
) -> bool:
    is_packaged = bool(getattr(sys, "frozen", False)) if packaged is None else packaged
    if not is_packaged:
        return False
    executable_path = Path(sys.executable if executable is None else executable).resolve()
    install_root = executable_path.parent
    if executable_path.name.lower() != "fortunechart.exe":
        raise UpdateSecurityError("packaged updater is bound to FortuneChart.exe")
    if resource_root is None:
        raw = getattr(sys, "_MEIPASS", None)
        if raw is None:
            raise UpdateSecurityError("packaged update check is missing sys._MEIPASS")
        resource_root = Path(raw)
    metadata = read_packaged_build_metadata(Path(resource_root))
    current_version = str(metadata["application_version"])
    manifest = fetch_update_manifest(fetcher=fetcher)
    if not is_newer_version(manifest.version, current_version):
        return False
    prepared = prepare_update(manifest, install_root=install_root, downloader=downloader)
    try:
        spawn_standalone_updater(
            prepared,
            install_root=install_root,
            updater_source=install_root / "FortuneChartUpdater.exe",
            parent_pid=os.getpid(),
            popen=popen,
        )
    except Exception:
        shutil.rmtree(prepared.staging_root, ignore_errors=True)
        raise
    return True


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def manifest_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Emit verified FortuneChart release update manifest")
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--asset-path", type=Path, required=True)
    parser.add_argument("--release-tag", required=True)
    parser.add_argument("--manifest-out", type=Path, required=True)
    args = parser.parse_args(argv)
    asset = args.asset_path.resolve()
    if not asset.is_file():
        raise SystemExit(f"asset not found: {asset}")
    size = asset.stat().st_size
    digest = hashlib.sha256()
    with asset.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    payload = release_update_manifest(
        version=DESKTOP_APPLICATION_VERSION,
        source_commit=args.source_commit,
        asset_sha256=digest.hexdigest(),
        asset_size=size,
        release_tag=args.release_tag,
    )
    _write_json(args.manifest_out, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(manifest_cli())
