from __future__ import annotations

import threading
import unittest
import urllib.request
from pathlib import Path

from fortune_training.combined_chart_application.bazi_pillar_metadata_assets import (
    BAZI_PILLAR_METADATA_CSS,
    BAZI_PILLAR_METADATA_JS,
    bazi_pillar_metadata_index_html,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedBrowserBaziPillarMetadataR1Tests(unittest.TestCase):
    def test_html_injection_is_additive_and_idempotence_guarded(self) -> None:
        base = "<html><head></head><body><script src=\"/app.js\"></script></body></html>"
        rendered = bazi_pillar_metadata_index_html(base)
        self.assertIn('/bazi-pillar-metadata.css', rendered)
        self.assertIn('/bazi-pillar-metadata.js', rendered)
        self.assertIn('/app.js', rendered)
        with self.assertRaises(ValueError):
            bazi_pillar_metadata_index_html(rendered)

    def test_sidecar_consumes_only_released_pillar_metadata(self) -> None:
        for key in (
            "source.stem_element",
            "source.stem_polarity",
            "source.branch_element_affiliation",
        ):
            with self.subTest(key=key):
                self.assertIn(key, BAZI_PILLAR_METADATA_JS)
        self.assertIn("干五行：${source.stem_element}", BAZI_PILLAR_METADATA_JS)
        self.assertIn("阴阳：${source.stem_polarity}", BAZI_PILLAR_METADATA_JS)
        self.assertIn("支五行：${source.branch_element_affiliation}", BAZI_PILLAR_METADATA_JS)
        self.assertNotIn("五行强弱", BAZI_PILLAR_METADATA_JS)
        self.assertNotIn("旺衰", BAZI_PILLAR_METADATA_JS)
        self.assertNotIn("喜用", BAZI_PILLAR_METADATA_JS)

    def test_sidecar_validates_candidate_pillars_before_rendering(self) -> None:
        self.assertIn("selectedApplicationCandidateIndex", BAZI_PILLAR_METADATA_JS)
        self.assertIn("source.position !== expectedPositions[index]", BAZI_PILLAR_METADATA_JS)
        self.assertIn("renderedPosition !== source.position", BAZI_PILLAR_METADATA_JS)
        self.assertIn("renderedGanzhi !== source.ganzhi", BAZI_PILLAR_METADATA_JS)
        self.assertNotIn("bundle.candidates[0]", BAZI_PILLAR_METADATA_JS)
        self.assertIn("bundle.candidates[selectedIndex]", BAZI_PILLAR_METADATA_JS)
        self.assertIn("data-application-candidate-index", BAZI_PILLAR_METADATA_JS.replace("dataset.applicationCandidateIndex", "data-application-candidate-index"))

    def test_sidecar_is_read_only_and_uses_same_resolve_response(self) -> None:
        self.assertIn("const copy = response.clone();", BAZI_PILLAR_METADATA_JS)
        self.assertIn("pathname !== '/api/resolve'", BAZI_PILLAR_METADATA_JS)
        self.assertIn("response?.combined_resolution?.bazi_bundle", BAZI_PILLAR_METADATA_JS)
        for forbidden in (
            "fetch('/api/bazi",
            ".innerHTML =",
            "selector.value =",
            "candidate.view.pillars =",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, BAZI_PILLAR_METADATA_JS)

    def test_candidate_selector_change_rerenders_metadata(self) -> None:
        self.assertIn("baziRoot.addEventListener('change'", BAZI_PILLAR_METADATA_JS)
        self.assertIn("bazi-candidate-select", BAZI_PILLAR_METADATA_JS)
        self.assertIn("scheduleRender();", BAZI_PILLAR_METADATA_JS)
        self.assertIn("MutationObserver", BAZI_PILLAR_METADATA_JS)

    def test_visual_contract_is_narrow(self) -> None:
        self.assertIn(".pillar .bazi-pillar-metadata", BAZI_PILLAR_METADATA_CSS)
        self.assertNotIn("position:absolute", BAZI_PILLAR_METADATA_CSS.replace(" ", ""))

    def test_real_workbench_serves_metadata_assets(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            with urllib.request.urlopen(f"http://{host}:{port}/", timeout=10) as response:
                html = response.read().decode("utf-8")
            with urllib.request.urlopen(
                f"http://{host}:{port}/bazi-pillar-metadata.js", timeout=10
            ) as response:
                javascript = response.read().decode("utf-8")
            with urllib.request.urlopen(
                f"http://{host}:{port}/bazi-pillar-metadata.css", timeout=10
            ) as response:
                stylesheet = response.read().decode("utf-8")
            self.assertIn('/bazi-pillar-metadata.js', html)
            self.assertIn('/bazi-pillar-metadata.css', html)
            self.assertIn("stem_element", javascript)
            self.assertIn("stem_polarity", javascript)
            self.assertIn("branch_element_affiliation", javascript)
            self.assertIn(".bazi-pillar-metadata", stylesheet)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
