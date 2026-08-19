from __future__ import annotations

import argparse
import ctypes
import os
import webbrowser
from collections.abc import Callable
from typing import Protocol

from fortune_training.combined_chart_application.workbench_local_app import (
    build_workbench_server,
)

from .distribution import DESKTOP_APPLICATION_VERSION
from .runtime import resolve_runtime_repository_root
from .updates import (
    UpdateSecurityError,
    UpdateUnavailable,
    maybe_launch_verified_update,
)


class _DesktopServer(Protocol):
    server_address: tuple[object, ...]

    def serve_forever(self) -> None: ...

    def server_close(self) -> None: ...


def desktop_url(server: _DesktopServer) -> str:
    host, port = server.server_address[:2]
    return f"http://{host}:{port}/"


def build_desktop_server():
    repository_root = resolve_runtime_repository_root()
    # Port 0 asks the OS for an available ephemeral loopback port. This avoids
    # fixed-port collisions while preserving the existing HTTP workbench.
    server = build_workbench_server(repository_root, port=0)
    host, port = server.server_address[:2]
    if host != "127.0.0.1" or not isinstance(port, int) or port <= 0:
        server.server_close()
        raise RuntimeError(f"desktop launcher bind policy violation: {host}:{port}")
    return server


def serve_desktop(
    server: _DesktopServer,
    *,
    open_browser: bool = True,
    browser_opener: Callable[[str], object] = webbrowser.open,
) -> int:
    url = desktop_url(server)
    if open_browser:
        browser_opener(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def _notify_update_integrity_failure(message: str) -> None:
    if os.name != "nt":
        return
    try:
        ctypes.windll.user32.MessageBoxW(
            None,
            f"自动更新校验失败，当前版本不会被替换，将继续启动。\n\n{message}",
            "FortuneChart 更新",
            0x30,
        )
    except Exception:
        pass


def _notify_post_update_version() -> None:
    """Show the activated build version only on an updater-owned relaunch.

    The wording is deliberately neutral rather than claiming the preceding
    transaction succeeded: the same hidden recovery switch may also be used to
    relaunch a known-good build after a failed future activation.  For the
    real-machine calibration it still gives visible proof of the activated
    package version without touching chart semantics or update authority.
    """

    if os.name != "nt":
        return
    try:
        ctypes.windll.user32.MessageBoxW(
            None,
            f"FortuneChart 已启动。\n\n当前版本：{DESKTOP_APPLICATION_VERSION}",
            "FortuneChart 版本",
            0x40,
        )
    except Exception:
        pass


def run_startup_update_check(*, disabled: bool = False) -> bool:
    """Return True only when a verified updater process was launched.

    Development/source execution is a no-op inside ``maybe_launch_verified_update``.
    Network unavailability deliberately continues the current known-good build.
    Integrity failures never apply remote bytes and leave the installation intact.
    """

    if disabled:
        return False
    try:
        return maybe_launch_verified_update()
    except UpdateUnavailable:
        return False
    except UpdateSecurityError as exc:
        _notify_update_integrity_failure(str(exc))
        return False
    except Exception as exc:
        _notify_update_integrity_failure(str(exc))
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the portable Windows Ziwei + Bazi chart workbench"
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Start the loopback workbench without opening the default browser",
    )
    parser.add_argument("--no-update", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--post-update", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.post_update:
        _notify_post_update_version()
    if run_startup_update_check(disabled=args.no_update or args.post_update):
        # The temporary standalone updater now owns activation. Exit so Windows
        # can rotate the complete portable directory without locked app files.
        return 0
    return serve_desktop(build_desktop_server(), open_browser=not args.no_browser)


if __name__ == "__main__":
    raise SystemExit(main())
