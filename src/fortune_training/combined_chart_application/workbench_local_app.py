from __future__ import annotations

import argparse
import webbrowser
from http.server import HTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .bazi_branch_relation_assets import (
    BAZI_BRANCH_RELATION_CSS,
    BAZI_BRANCH_RELATION_JS,
    bazi_branch_relation_index_html,
)
from .bazi_branch_relation_local_app import (
    BaziBranchRelationPresentationLocalMixin,
    _BaziBranchRelationPresentationHandlerMixin,
)
from .bazi_hidden_exposure_assets import (
    BAZI_HIDDEN_EXPOSURE_CSS,
    BAZI_HIDDEN_EXPOSURE_JS,
    bazi_hidden_exposure_index_html,
)
from .bazi_hidden_exposure_local_app import (
    BaziHiddenExposurePresentationLocalMixin,
    _BaziHiddenExposurePresentationHandlerMixin,
)
from .bazi_pillar_metadata_assets import (
    BAZI_PILLAR_METADATA_CSS,
    BAZI_PILLAR_METADATA_JS,
    bazi_pillar_metadata_index_html,
)
from .bazi_stem_relation_assets import (
    BAZI_STEM_RELATION_CSS,
    BAZI_STEM_RELATION_JS,
    bazi_stem_relation_index_html,
)
from .bazi_stem_relation_local_app import (
    BaziStemRelationPresentationLocalMixin,
    _BaziStemRelationPresentationHandlerMixin,
)
from .flow_fusion_assets import (
    FLOW_FUSION_CSS,
    FLOW_FUSION_JS,
    flow_fusion_index_html,
)
from .flow_fusion_local_app import (
    FlowFusionR2LocalMixin,
    _FlowFusionR2HandlerMixin,
)
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
from .nayin_assets import NAYIN_CSS, NAYIN_JS, nayin_index_html
from .nayin_local_app import (
    BaziNayinPresentationLocalMixin,
    _NayinPresentationHandlerMixin,
)
from .palace_stem_topology_assets import (
    PALACE_STEM_TOPOLOGY_CSS,
    PALACE_STEM_TOPOLOGY_JS,
    palace_stem_topology_index_html,
)
from .palace_stem_topology_local_app import (
    ZiweiPalaceStemTopologyLocalMixin,
    _ZiweiPalaceStemTopologyHandlerMixin,
)
from .shared_apply_assets import (
    SHARED_APPLY_CSS,
    SHARED_APPLY_JS,
    shared_apply_index_html,
)
from .shared_apply_local_app import (
    SharedZiweiProjectionLocalMixin,
    _SharedZiweiProjectionHandlerMixin,
)
from .target_flow_assets import (
    TARGET_FLOW_CSS,
    TARGET_FLOW_JS,
    target_flow_index_html,
)
from .target_flow_guard_assets import TARGET_FLOW_GUARD_JS
from .target_flow_ziwei_projection_assets import (
    TARGET_FLOW_ZIWEI_PROJECTION_CSS,
    TARGET_FLOW_ZIWEI_PROJECTION_JS,
)
from .ziwei_basic_info_assets import (
    ZIWEI_BASIC_INFO_CSS,
    ZIWEI_BASIC_INFO_JS,
    ziwei_basic_info_index_html,
)
from .ziwei_dignity_provenance_assets import (
    ZIWEI_DIGNITY_PROVENANCE_CSS,
    ZIWEI_DIGNITY_PROVENANCE_JS,
    ziwei_dignity_provenance_index_html,
)
from .ziwei_dignity_provenance_local_app import (
    ZiweiDignityProvenanceLocalMixin,
    _ZiweiDignityProvenanceHandlerMixin,
)


class CombinedChartWorkbenchApplication(
    ZiweiDignityProvenanceLocalMixin,
    ZiweiPalaceStemTopologyLocalMixin,
    BaziHiddenExposurePresentationLocalMixin,
    BaziStemRelationPresentationLocalMixin,
    BaziBranchRelationPresentationLocalMixin,
    BaziNayinPresentationLocalMixin,
    FlowFusionR2LocalMixin,
    SharedZiweiProjectionLocalMixin,
    InteractionLocalCombinedChartApplication,
    FlowLocalCombinedChartApplication,
):
    """One loopback workspace over released independent Ziwei/Bazi sidecars."""

    def __init__(self, repository_root: Path) -> None:
        # Cooperative MRO is intentional: provenance/topology/presentation/shared/
        # fusion mixins compose over Interaction -> Flow -> Local, sharing the same
        # CombinedChartService instance. Read-only Ziwei sidecars bind to the exact
        # released application bundle and never mutate NatalChartState.
        super().__init__(repository_root)

    def health(self):
        # `fortune-chart-app` keeps the browser-app health contract released before
        # additive browser composition. Sidecars expose separate endpoints without
        # rewriting legacy health identity.
        return LocalCombinedChartApplication.health(self)


class _WorkbenchHandler(
    _ZiweiDignityProvenanceHandlerMixin,
    _ZiweiPalaceStemTopologyHandlerMixin,
    _BaziHiddenExposurePresentationHandlerMixin,
    _BaziStemRelationPresentationHandlerMixin,
    _BaziBranchRelationPresentationHandlerMixin,
    _NayinPresentationHandlerMixin,
    _FlowFusionR2HandlerMixin,
    _SharedZiweiProjectionHandlerMixin,
    _InteractionHandler,
    _FlowHandler,
):
    application: CombinedChartWorkbenchApplication
    server_version = "CombinedChartWorkbenchLocalApp/1.11"

    def do_GET(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        if path == "/":
            html = bazi_hidden_exposure_index_html(
                bazi_stem_relation_index_html(
                    bazi_branch_relation_index_html(
                        bazi_pillar_metadata_index_html(
                            ziwei_basic_info_index_html(
                                flow_fusion_index_html(
                                    nayin_index_html(
                                        shared_apply_index_html(
                                            target_flow_index_html(
                                                ziwei_dignity_provenance_index_html(
                                                    palace_stem_topology_index_html(
                                                        interaction_index_html(INDEX_HTML)
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
            self._send_bytes(200, "text/html; charset=utf-8", html.encode())
            return
        if path == "/bazi-hidden-exposure.css":
            self._send_bytes(
                200,
                "text/css; charset=utf-8",
                BAZI_HIDDEN_EXPOSURE_CSS.encode(),
            )
            return
        if path == "/bazi-hidden-exposure.js":
            self._send_bytes(
                200,
                "application/javascript; charset=utf-8",
                BAZI_HIDDEN_EXPOSURE_JS.encode(),
            )
            return
        if path == "/bazi-stem-relations.css":
            self._send_bytes(
                200,
                "text/css; charset=utf-8",
                BAZI_STEM_RELATION_CSS.encode(),
            )
            return
        if path == "/bazi-stem-relations.js":
            self._send_bytes(
                200,
                "application/javascript; charset=utf-8",
                BAZI_STEM_RELATION_JS.encode(),
            )
            return
        if path == "/bazi-branch-relations.css":
            self._send_bytes(
                200,
                "text/css; charset=utf-8",
                BAZI_BRANCH_RELATION_CSS.encode(),
            )
            return
        if path == "/bazi-branch-relations.js":
            self._send_bytes(
                200,
                "application/javascript; charset=utf-8",
                BAZI_BRANCH_RELATION_JS.encode(),
            )
            return
        if path == "/bazi-pillar-metadata.css":
            self._send_bytes(
                200,
                "text/css; charset=utf-8",
                BAZI_PILLAR_METADATA_CSS.encode(),
            )
            return
        if path == "/bazi-pillar-metadata.js":
            self._send_bytes(
                200,
                "application/javascript; charset=utf-8",
                BAZI_PILLAR_METADATA_JS.encode(),
            )
            return
        if path == "/nayin.css":
            self._send_bytes(
                200,
                "text/css; charset=utf-8",
                NAYIN_CSS.encode(),
            )
            return
        if path == "/nayin.js":
            self._send_bytes(
                200,
                "application/javascript; charset=utf-8",
                NAYIN_JS.encode(),
            )
            return
        if path == "/target-flow.css":
            combined_css = f"{TARGET_FLOW_CSS}\n{TARGET_FLOW_ZIWEI_PROJECTION_CSS}"
            self._send_bytes(
                200,
                "text/css; charset=utf-8",
                combined_css.encode(),
            )
            return
        if path == "/target-flow.js":
            combined_js = (
                f"{TARGET_FLOW_JS}\n{TARGET_FLOW_GUARD_JS}\n"
                f"{TARGET_FLOW_ZIWEI_PROJECTION_JS}"
            )
            self._send_bytes(
                200,
                "application/javascript; charset=utf-8",
                combined_js.encode(),
            )
            return
        if path == "/shared-apply.css":
            self._send_bytes(
                200,
                "text/css; charset=utf-8",
                SHARED_APPLY_CSS.encode(),
            )
            return
        if path == "/shared-apply.js":
            self._send_bytes(
                200,
                "application/javascript; charset=utf-8",
                SHARED_APPLY_JS.encode(),
            )
            return
        if path == "/flow-fusion.css":
            self._send_bytes(
                200,
                "text/css; charset=utf-8",
                FLOW_FUSION_CSS.encode(),
            )
            return
        if path == "/flow-fusion.js":
            self._send_bytes(
                200,
                "application/javascript; charset=utf-8",
                FLOW_FUSION_JS.encode(),
            )
            return
        if path == "/ziwei-basic-info.css":
            self._send_bytes(
                200,
                "text/css; charset=utf-8",
                ZIWEI_BASIC_INFO_CSS.encode(),
            )
            return
        if path == "/ziwei-basic-info.js":
            self._send_bytes(
                200,
                "application/javascript; charset=utf-8",
                ZIWEI_BASIC_INFO_JS.encode(),
            )
            return
        if path == "/ziwei-palace-stem-topology.css":
            self._send_bytes(
                200,
                "text/css; charset=utf-8",
                PALACE_STEM_TOPOLOGY_CSS.encode(),
            )
            return
        if path == "/ziwei-palace-stem-topology.js":
            self._send_bytes(
                200,
                "application/javascript; charset=utf-8",
                PALACE_STEM_TOPOLOGY_JS.encode(),
            )
            return
        if path == "/ziwei-dignity-provenance.css":
            self._send_bytes(
                200,
                "text/css; charset=utf-8",
                ZIWEI_DIGNITY_PROVENANCE_CSS.encode(),
            )
            return
        if path == "/ziwei-dignity-provenance.js":
            self._send_bytes(
                200,
                "application/javascript; charset=utf-8",
                ZIWEI_DIGNITY_PROVENANCE_JS.encode(),
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
            "Ziwei Sanhe, palace-stem topology, star provenance and Dignity-provenance "
            "sidecars, Bazi target-flow, R2 cross-system target-flow fusion, Ziwei natal "
            "basic-info presentation, Bazi Nayin/pillar-metadata/hidden-exposure/"
            "stem-relation/branch-relation presentation, and explicit shared-time apply "
            "sidecars"
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
    print(
        "Ziwei interaction: SANHE plus read-only palace-stem, star-placement and Dignity "
        "annotation provenance. Bazi interaction: explicit target-flow sidecar. Fusion: "
        "additive R2 target-flow endpoint + read-only browser panel. Ziwei natal basics "
        "plus Bazi Nayin, pillar metadata, exact hidden-stem exposure and natal stem/"
        "branch relation facts are read-only presentation projections."
    )
    print(
        "Palace-stem SAME/OPPOSITE/OTHER topology is not promoted to outward/inward "
        "self-transformation direction. Operational Dignity provenance is not S01 frozen "
        "brightness authority. Shared target synchronization is explicit opt-in only; no "
        "automatic cross-system sync."
    )
    print("Bind policy: 127.0.0.1 only. Press Ctrl+C to stop.")
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
