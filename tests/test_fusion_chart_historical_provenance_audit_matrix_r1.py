from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
README = ROOT / "README.md"
CI = ROOT / ".github" / "workflows" / "ci.yml"


class HistoricalProvenanceAuditMatrixR1Test(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(MATRIX.read_text(encoding="utf-8"))
        self.rows = self.payload["rows"]

    def test_inventory_is_broad_and_unique(self) -> None:
        self.assertGreaterEqual(len(self.rows), 100)
        ids = [row["rule_id"] for row in self.rows]
        self.assertEqual(len(ids), len(set(ids)))
        for module in (
            "Time / Calendar", "四柱本命", "八字派生字段", "大运", "小运", "神煞",
            "八字动态时限", "紫微本命", "十二宫", "主星", "辅星", "杂曜", "四化",
            "庙旺落陷", "大限", "流年", "流月", "流日", "流时", "动态辅助星",
            "Structural R1–R8", "Combined Fusion", "candidate/profile rules",
            "provenance / hashes / lineage",
        ):
            self.assertIn(module, {row["module"] for row in self.rows})

    def test_closed_product_and_unformalized_direction_are_preserved(self) -> None:
        self.assertEqual(self.payload["deterministic_product_state"], "CLOSED")
        self.assertEqual(self.payload["self_inward_transformation_state"], "NOT_YET_FORMALIZED")
        self.assertTrue(all(row["algorithm_reopen_authorized"] is False for row in self.rows))
        row = next(row for row in self.rows if row["rule_id"] == "HPA-ZT-016")
        self.assertEqual(row["audit_status"], "NOT_YET_FORMALIZED")

    def test_modern_compatibility_is_not_historical_authority(self) -> None:
        self.assertEqual(
            self.payload["external_reference_policy"],
            "WENMO_WENZHEN_COMPATIBILITY_ONLY_NOT_HISTORICAL_AUTHORITY",
        )
        modern = [row for row in self.rows if row["audit_status"] == "MODERN_COMPATIBILITY_ONLY"]
        self.assertTrue(modern)

    def test_machine_gate_runs(self) -> None:
        completed = subprocess.run(
            [sys.executable, "scripts/verify-fusion-chart-historical-provenance-audit-r1.py"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        receipt = json.loads(completed.stdout)
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["row_count"], len(self.rows))
        self.assertEqual(receipt["algorithm_reopen_authorized_count"], 0)
        self.assertGreaterEqual(receipt["historical_research_batch_count"], 1)
        self.assertGreaterEqual(receipt["audited_row_count"], 64)
        self.assertEqual(receipt["confirmed_chart_algorithm_defect_count"], 0)
        self.assertGreaterEqual(receipt["confirmed_provenance_metadata_defect_count"], 4)
        self.assertGreaterEqual(receipt["repaired_provenance_metadata_defect_count"], 4)
        self.assertGreaterEqual(receipt["historical_candidate_registry_count"], 1)
        self.assertGreaterEqual(receipt["historical_candidate_runtime_resolver_count"], 1)
        self.assertGreaterEqual(receipt["identified_missing_candidate_family_count"], 6)

    def test_readme_and_ci_bind_the_audit_stage(self) -> None:
        readme = README.read_text(encoding="utf-8")
        ci = CI.read_text(encoding="utf-8")
        self.assertIn("FUSION_CHART_HISTORICAL_PROVENANCE_AUDIT_R1=IN_PROGRESS", readme)
        self.assertIn("HISTORICAL_PROVENANCE_INVENTORY=COMPLETE", readme)
        self.assertIn("DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED", readme)
        self.assertIn("ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED", readme)
        self.assertIn("verify-fusion-chart-historical-provenance-audit-r1.py", ci)
        self.assertIn("test_fusion_chart_historical_provenance_audit_matrix_r1.py", ci)


if __name__ == "__main__":
    unittest.main()
