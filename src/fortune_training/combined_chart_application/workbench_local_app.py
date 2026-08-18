from __future__ import annotations

import argparse
import webbrowser
from http.server import HTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .flow_local_app import FlowLocalCombinedChartApplication, _FlowHandler
from .interaction_assets import interaction_index_html
from .interaction_local_app import (
    InteractionLocalCombinedChartApplication,
    _InteractionHandler,
)
from .local_app import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    INDEX_HTML,
    LocalCombinedChartApplication,
)
from .target_flow_assets import (
    TARGET_FLOW_CSS,
    TARGET_FLOW_JS,
    target_flow_index_html,
)


class CombinedChartWorkbenchApplication(
    InteractionLocalCombinedChartApplication,
    FlowLocalCombinedChartApplication,
):
    """One loopback workspace over released independent Ziwei/Bazi sidecars."""

    def __init__(self, repository_root: Path) -> None:
        # Cooperative MRO is intentional:
        # Interaction -> Flow -> Local initializes both released sidecar services
        # over the same CombinedChartService instance.
        super().__init__(repository_root)

    def health(self):
        # `fortune-chart-app` keeps the browser-app health contract released before
        # target-flow browser composition. The Flow app keeps its own health on its
        # separate `fortune-chart-flow-app` entry point.
        return LocalCombinedChartApplication.health(self)


class _WorkbenchHandler(_InteractionHandler, _FlowHandler):
    application: CombinedChartWorkbenchApplication
    server_version = "CombinedChartWorkbenchLocalApp/1.0"

    def do_GET(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        if path == "/":
            html = target_flow_index_html(interaction_index_html(INDEX_HTML))
            self._send_bytes(200, "text/html; charset=utf-8", html.encode())
            return
        if path == "/target-flow.css":
            self._send_bytes(
                200,
                "text/css; charset=utf-8",
                TARGET_FLOW_CSS.encode(),
            )
            return
        if path == "/target-flow.js":
            self._send_bytes(
                200,
                "application/javascript; charset=utf-8",
                TARGET_FLOW_JS.encode(),
            )
            return
        super().do_GET()


def workbench_handler_for(application: CombinedChartWorkbenchApplication):
    class Handler(_WorkbenchHandler):
        pass

    Handler.application = application
    return Handler


def build_workbench_server(
    repository_root: Path,
    *,
    port: int = DEFAULT_PORT,
) -> HTTPServer:
    if not 0 <= port <= 65535:
        raise ValueError("port must be in [0, 65535]")
    return HTTPServer(
        (DEFAULT_HOST, port),
        workbench_handler_for(CombinedChartWorkbenchApplication(repository_root)),
    )


def _default_repository_root() -> Path:
    root = Path(__file__).resolve().parents[3]
    return (
        root
        if (root / "config" / "time-calendar-policies.json").is_file()
        else Path.cwd()
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the local-only Ziwei + Bazi chart workbench with independent "
            "Ziwei Sanhe and Bazi target-flow sidecars"
        )
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=_default_repository_root(),
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args(argv)
    server = build_workbench_server(args.repository_root, port=args.port)
    host, port = server.server_address[:2]
    url = f"http://{host}:{port}/"
    print(f"Combined chart local workbench: {url}")
    print("Ziwei interaction: SANHE sidecar. Bazi interaction: explicit target-flow sidecar.")
    print("No cross-system temporal synchronization. Bind policy: 127.0.0.1 only.")
    print("Press Ctrl+C to stop.")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
