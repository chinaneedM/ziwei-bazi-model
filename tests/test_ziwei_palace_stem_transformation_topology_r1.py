from __future__ import annotations

import unittest
from collections import defaultdict
from pathlib import Path

from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
)
from fortune_training.ziwei_application.palace_stem_topology import (
    PALACE_STEM_TOPOLOGY_CLASSIFICATION_POLICY,
    PALACE_STEM_TOPOLOGY_SCHEMA,
    PALACE_STEM_TOPOLOGY_SELECTION_SEMANTICS,
    PALACE_STEM_TOPOLOGY_SEMANTIC_SCOPE,
    TRANSFORMATION_TYPES,
)


ROOT = Path(__file__).resolve().parents[1]


def _payload() -> dict[str, object]:
    return {
        "birth_datetime": "1994-05-17T14:30:00",
        "birth_place": "Beijing",
        "latitude": 39.9042,
        "longitude": 116.4074,
        "timezone_id": "Asia/Shanghai",
        "sex": "MALE",
        "precision": "EXACT_SECOND",
        "uncertainty_seconds": 0,
        "ziwei_daxian_count": 12,
        "ziwei_daxian_frame_id": None,
        "ziwei_annual_year": 2025,
        "ziwei_lunar_month": 4,
        "ziwei_minor_limit_age": None,
        "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
        "bazi_dayun_count": 12,
        "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
    }


class ZiweiPalaceStemTransformationTopologyR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = CombinedChartWorkbenchApplication(ROOT)
        cls.payload = _payload()
        cls.base = cls.app.resolve_payload(dict(cls.payload))
        cls.response = cls.app.resolve_ziwei_palace_stem_topology_payload(
            dict(cls.payload)
        )
        cls.topology = cls.response[
            "ziwei_palace_stem_transformation_topology"
        ]

    def test_sidecar_is_bound_to_exact_released_application_bundle(self) -> None:
        combined = self.base["combined_resolution"]
        expected = combined["ziwei_bundle"]["bundle_hash"]
        self.assertEqual(self.response["source_ziwei_bundle_hash"], expected)
        self.assertEqual(self.topology["source_application_bundle_hash"], expected)
        self.assertEqual(
            self.response["source_combined_manifest_hash"],
            combined["manifest_hash"],
        )

    def test_sidecar_releases_exact_12_by_4_topology_domain(self) -> None:
        self.assertEqual(self.topology["schema"], PALACE_STEM_TOPOLOGY_SCHEMA)
        self.assertEqual(self.topology["status"], "COMPLETE")
        self.assertEqual(self.topology["integrity"]["status"], "PASS")
        self.assertEqual(
            self.topology["classification_policy"],
            PALACE_STEM_TOPOLOGY_CLASSIFICATION_POLICY,
        )
        self.assertEqual(
            self.topology["selection_semantics"],
            PALACE_STEM_TOPOLOGY_SELECTION_SEMANTICS,
        )
        self.assertEqual(
            self.topology["semantic_scope"],
            PALACE_STEM_TOPOLOGY_SEMANTIC_SCOPE,
        )

        rows = self.topology["rows"]
        self.assertEqual(len(rows), 48)
        by_source: dict[int, list[dict[str, object]]] = defaultdict(list)
        for row in rows:
            by_source[row["source_address_index"]].append(row)
            self.assertEqual(row["source_layer"], "PALACE_STEM")
            self.assertIn(
                row["topology_relation"],
                {"SAME_PALACE", "OPPOSITE_PALACE", "OTHER_PALACE"},
            )
            self.assertTrue(row["source_refs"])
            self.assertEqual(len(row["fact_hash"]), 64)
            self.assertEqual(len(row["computation_hash"]), 64)
            self.assertTrue(row["row_id"].startswith("ZIWEI-PALACE-STEM-TOPOLOGY:"))

        self.assertEqual(set(by_source), set(range(12)))
        for source_index, source_rows in by_source.items():
            with self.subTest(source_index=source_index):
                self.assertEqual(len(source_rows), 4)
                self.assertEqual(
                    {row["transformation_type"] for row in source_rows},
                    set(TRANSFORMATION_TYPES),
                )
                self.assertEqual(len({row["source_stem"] for row in source_rows}), 1)
                self.assertEqual(len({row["source_branch"] for row in source_rows}), 1)
                self.assertEqual(len({row["context_id"] for row in source_rows}), 1)

    def test_sidecar_does_not_release_self_transformation_direction(self) -> None:
        for row in self.topology["rows"]:
            self.assertNotIn("direction", row)
            self.assertNotIn("self_transformation_kind", row)
        self.assertNotIn("OUTWARD_DISSIPATION", str(self.topology))
        self.assertNotIn("INWARD_RECEPTION", str(self.topology))

    def test_full_replay_is_stable(self) -> None:
        replay = self.app.resolve_ziwei_palace_stem_topology_payload(
            dict(self.payload)
        )
        self.assertEqual(replay, self.response)
        for name in ("fact_hash", "computation_hash", "bundle_hash"):
            self.assertEqual(len(self.topology[name]), 64)


if __name__ == "__main__":
    unittest.main()
