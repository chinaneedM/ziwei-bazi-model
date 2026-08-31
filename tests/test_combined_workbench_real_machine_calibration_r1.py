from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SMOKE_PATH = ROOT / "scripts" / "combined-workbench-smoke.py"
RUNBOOK_PATH = ROOT / "docs" / "COMBINED-WORKBENCH-REAL-MACHINE-CALIBRATION-R1.md"
README_PATH = ROOT / "README.md"
SHARED_APPLY_ASSETS_PATH = (
    ROOT / "src" / "fortune_training" / "combined_chart_application" / "shared_apply_assets.py"
)


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("combined_workbench_smoke_r1", SMOKE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load combined workbench smoke module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CombinedWorkbenchRealMachineCalibrationR1Tests(unittest.TestCase):
    def test_smoke_receipt_exercises_all_released_workbench_surfaces(self) -> None:
        smoke = _load_smoke_module()
        receipt = smoke.run_smoke(ROOT)
        self.assertEqual("COMBINED-WORKBENCH-SMOKE-RECEIPT-R2", receipt["schema"])
        self.assertEqual("PASS", receipt["status"])
        self.assertEqual("LOOPBACK_ONLY", receipt["bind_policy"])
        for key in (
            "combined_manifest_hash",
            "ziwei_bundle_hash",
            "bazi_bundle_hash",
            "ziwei_interaction_bundle_hash",
            "bazi_target_flow_bundle_hash",
            "target_coordinate_fact_hash",
            "shared_projection_fact_hash",
            "fusion_r2_bundle_hash",
        ):
            with self.subTest(key=key):
                self.assertEqual(64, len(receipt[key]))
        self.assertGreaterEqual(receipt["bazi_target_flow_candidate_count"], 1)
        self.assertGreaterEqual(receipt["shared_projection_candidate_count"], 1)
        self.assertGreaterEqual(receipt["fusion_r2_ziwei_selector_candidate_count"], 1)

    def test_smoke_harness_uses_workbench_boundary_not_temporal_algorithms(self) -> None:
        source = SMOKE_PATH.read_text(encoding="utf-8")
        self.assertIn("CombinedChartWorkbenchApplication", source)
        self.assertIn("app.health()", source)
        self.assertIn("app.resolve_payload(base_payload)", source)
        self.assertIn("app.resolve_ziwei_interaction_payload(interaction_payload)", source)
        self.assertIn("app.resolve_flow_payload(target_payload)", source)
        self.assertIn("app.resolve_shared_ziwei_projection_payload(target_payload)", source)
        self.assertIn("app.resolve_flow_fusion_r2_payload(target_payload)", source)
        for forbidden in (
            "BaziTimeResolver",
            "TargetTemporalCoordinateFoundation",
            "SharedZiweiSelectorProjectionService",
            "ZiweiTemporal",
            "sexagenary_index",
            "nominal_age =",
            "DaxianFrame(",
            "AnnualFrame(",
            "MinorLimitFrame(",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)

    def test_runbook_names_actual_entrypoint_loopback_and_health(self) -> None:
        text = RUNBOOK_PATH.read_text(encoding="utf-8")
        self.assertIn("fortune-chart-app", text)
        self.assertIn("fortune_training.combined_chart_application.workbench_local_app:main", text)
        self.assertIn("http://127.0.0.1:8767/", text)
        self.assertIn("GET http://127.0.0.1:8767/health", text)
        self.assertIn("fortune-chart-app --no-browser", text)
        self.assertIn("fortune-chart-app --port 8877", text)
        self.assertIn("Ctrl+C", text)

    def test_runbook_preserves_explicit_apply_and_candidate_semantics(self) -> None:
        text = RUNBOOK_PATH.read_text(encoding="utf-8")
        self.assertIn("Calculation alone does not change Ziwei Daxian / Annual / Minor selectors", text)
        self.assertIn("candidate-preserving", text)
        self.assertIn("candidate 0 is not auto-applied", text)
        self.assertIn("应用目标时间到紫微", text)
        self.assertIn("does not rewrite target fields", text)
        self.assertIn("Manual Ziwei navigation after Apply does not rewrite target fields", text)

    def test_shared_projection_ui_exposes_layer_facts_read_only(self) -> None:
        source = SHARED_APPLY_ASSETS_PATH.read_text(encoding="utf-8")
        self.assertIn("daxian_layer_projection", source)
        self.assertIn("annual_layer_projection", source)
        self.assertIn("monthly_layer_projection", source)
        self.assertIn("来源干=", source)
        self.assertIn("四化=", source)
        self.assertIn("禄羊陀=", source)
        self.assertIn("layer.fact_hash", source)
        self.assertIn("按来源层只读显示", source)

    def test_calibration_workflow_contains_no_training_write_commands(self) -> None:
        text = RUNBOOK_PATH.read_text(encoding="utf-8")
        self.assertIn("fortune-train verify", text)
        for forbidden in (
            "fortune-train start",
            "fortune-train learn",
            "fortune-train score",
            "fortune-train maintenance-run",
            "fortune-train maintenance-auto",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)

    def test_readme_links_to_current_combined_workbench_calibration_runbook(self) -> None:
        text = README_PATH.read_text(encoding="utf-8")
        self.assertIn("fortune-chart-app", text)
        self.assertIn("docs/COMBINED-WORKBENCH-REAL-MACHINE-CALIBRATION-R1.md", text)
        self.assertIn("scripts/combined-workbench-smoke.py", text)


if __name__ == "__main__":
    unittest.main()
