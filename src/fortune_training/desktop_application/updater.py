from __future__ import annotations

import argparse
import ctypes
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Callable

from .distribution import DESKTOP_APPLICATION_ID
from .updates import UpdateSecurityError, parse_semver


class UpdateApplyError(RuntimeError):
    pass


def _creationflags_no_window() -> int:
    return int(getattr(subprocess, "CREATE_NO_WINDOW", 0))


def wait_for_process_exit(pid: int, timeout_seconds: float = 30.0) -> bool:
    if pid <= 0:
        return True
    if os.name == "nt":
        SYNCHRONIZE = 0x00100000
        WAIT_OBJECT_0 = 0x00000000
        WAIT_TIMEOUT = 0x00000102
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(SYNCHRONIZE, False, pid)
        if not handle:
            return True
        try:
            result = kernel32.WaitForSingleObject(handle, int(timeout_seconds * 1000))
            if result == WAIT_OBJECT_0:
                return True
            if result == WAIT_TIMEOUT:
                return False
            return False
        finally:
            kernel32.CloseHandle(handle)
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return True
        except PermissionError:
            pass
        time.sleep(0.1)
    return False


def _read_metadata(install_root: Path) -> dict[str, object]:
    path = install_root / "_internal" / "runtime" / "desktop-build-metadata.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise UpdateApplyError("activated build metadata is unreadable") from exc
    if not isinstance(payload, dict):
        raise UpdateApplyError("activated build metadata must be an object")
    return payload


def validate_activated_install(
    install_root: Path,
    *,
    expected_version: str,
    expected_source_commit: str,
) -> Path:
    root = Path(install_root).resolve()
    exe = root / "FortuneChart.exe"
    updater = root / "FortuneChartUpdater.exe"
    if not exe.is_file() or not updater.is_file():
        raise UpdateApplyError("activated installation is missing required executables")
    parse_semver(expected_version)
    metadata = _read_metadata(root)
    if metadata.get("application_id") != DESKTOP_APPLICATION_ID:
        raise UpdateApplyError("activated application identity mismatch")
    if metadata.get("application_version") != expected_version:
        raise UpdateApplyError("activated version mismatch")
    if str(metadata.get("source_commit", "")).lower() != expected_source_commit.lower():
        raise UpdateApplyError("activated source commit mismatch")
    return exe


def _default_relauncher(executable: Path) -> subprocess.Popen[bytes]:
    return subprocess.Popen(
        [str(executable), "--post-update"],
        close_fds=True,
        creationflags=_creationflags_no_window(),
    )


def apply_update_transaction(
    *,
    install_root: Path,
    staged_bundle: Path,
    expected_version: str,
    expected_source_commit: str,
    relauncher: Callable[[Path], object] = _default_relauncher,
    health_wait_seconds: float = 2.0,
) -> Path:
    install = Path(install_root).resolve()
    staged = Path(staged_bundle).resolve()
    if not install.is_dir():
        raise UpdateApplyError("current installation root is missing")
    if staged.name != "FortuneChart" or not staged.is_dir():
        raise UpdateApplyError("staged bundle root is invalid")
    if staged.parent.parent != install.parent:
        raise UpdateApplyError("staged bundle must be on the same adjacent volume")
    backup = install.parent / f".{install.name}.backup-{uuid.uuid4().hex}"
    activated = False
    try:
        install.rename(backup)
        staged.rename(install)
        activated = True
        executable = validate_activated_install(
            install,
            expected_version=expected_version,
            expected_source_commit=expected_source_commit,
        )
        process = relauncher(executable)
        if health_wait_seconds > 0:
            time.sleep(health_wait_seconds)
        poll = getattr(process, "poll", None)
        if callable(poll) and poll() is not None:
            raise UpdateApplyError("new FortuneChart process exited during activation health window")
    except Exception:
        if activated and install.exists():
            shutil.rmtree(install, ignore_errors=True)
        if backup.exists() and not install.exists():
            backup.rename(install)
        raise
    try:
        shutil.rmtree(backup)
    except OSError:
        # A complete old-version backup is safe to leave behind if antivirus or
        # indexing holds a transient handle; never mix it into the active tree.
        pass
    return install


def _validate_transaction_paths(
    *,
    install_root: Path,
    staging_root: Path,
    staged_bundle: Path,
) -> tuple[Path, Path, Path]:
    install = install_root.resolve()
    staging = staging_root.resolve()
    staged = staged_bundle.resolve()
    if staging.parent != install.parent:
        raise UpdateSecurityError("staging root is not adjacent to the portable install")
    if staged.parent != staging or staged.name != "FortuneChart":
        raise UpdateSecurityError("staged bundle is not the expected archive root")
    return install, staging, staged


def _relaunch_old_after_failure(install_root: Path) -> None:
    executable = install_root / "FortuneChart.exe"
    if executable.is_file():
        try:
            subprocess.Popen(
                [str(executable), "--post-update"],
                close_fds=True,
                creationflags=_creationflags_no_window(),
            )
        except OSError:
            pass


def _show_error(message: str) -> None:
    if os.name != "nt":
        return
    try:
        ctypes.windll.user32.MessageBoxW(
            None,
            f"自动更新失败，已保留/恢复当前版本。\n\n{message}",
            "FortuneChart 更新",
            0x10,
        )
    except Exception:
        pass


def _schedule_self_cleanup() -> None:
    if os.name != "nt" or not getattr(sys, "frozen", False):
        return
    executable = Path(sys.executable).resolve()
    parent = executable.parent
    command = (
        f'timeout /t 2 /nobreak >nul & del /f /q "{executable}" '
        f'& rmdir /q "{parent}"'
    )
    try:
        subprocess.Popen(
            ["cmd.exe", "/d", "/c", command],
            close_fds=True,
            creationflags=_creationflags_no_window(),
        )
    except OSError:
        pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply a verified FortuneChart portable update")
    parser.add_argument("--parent-pid", type=int, required=True)
    parser.add_argument("--install-root", type=Path, required=True)
    parser.add_argument("--staging-root", type=Path, required=True)
    parser.add_argument("--staged-bundle", type=Path, required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--expected-source-commit", required=True)
    args = parser.parse_args(argv)
    install = args.install_root.resolve()
    staging = args.staging_root.resolve()
    try:
        install, staging, staged = _validate_transaction_paths(
            install_root=args.install_root,
            staging_root=args.staging_root,
            staged_bundle=args.staged_bundle,
        )
        if not wait_for_process_exit(args.parent_pid):
            raise UpdateApplyError("running FortuneChart did not exit before update timeout")
        apply_update_transaction(
            install_root=install,
            staged_bundle=staged,
            expected_version=args.expected_version,
            expected_source_commit=args.expected_source_commit,
        )
        shutil.rmtree(staging, ignore_errors=True)
        _schedule_self_cleanup()
        return 0
    except Exception as exc:
        shutil.rmtree(staging, ignore_errors=True)
        _relaunch_old_after_failure(install)
        _show_error(str(exc))
        _schedule_self_cleanup()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
