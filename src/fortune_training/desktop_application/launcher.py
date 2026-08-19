from __future__ import annotations

import argparse
import webbrowser
from collections.abc import Callable
from typing import Protocol

from fortune_training.combined_chart_application.workbench_local_app import (
    build_workbench_server,
)

from .runtime import resolve_runtime_repository_root


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the portable Windows Ziwei + Bazi chart workbench"
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Start the loopback workbench without opening the default browser",
    )
    args = parser.parse_args(argv)
    return serve_desktop(build_desktop_server(), open_browser=not args.no_browser)


if __name__ == "__main__":
    raise SystemExit(main())
