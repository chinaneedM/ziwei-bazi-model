from __future__ import annotations

import unittest

from fortune_training.combined_chart_application.shared_apply_assets import SHARED_APPLY_JS
from fortune_training.combined_chart_application.target_flow_assets import TARGET_FLOW_JS
from fortune_training.combined_chart_application.target_flow_guard_assets import (
    TARGET_FLOW_GUARD_JS,
)


ZIWEI_ONLY_TEMPORAL_IDS = (
    "ziwei-daxian-count",
    "ziwei-daxian-frame-id",
    "ziwei-annual-year",
    "ziwei-minor-limit-age",
)


class CombinedBrowserBaziTargetFlowZiweiNavIndependenceR1Tests(unittest.TestCase):
    def test_bazi_flow_fingerprint_excludes_ziwei_only_temporal_controls(self) -> None:
        source_block = TARGET_FLOW_JS.split("const sourceFieldIds = [", 1)[1].split(
            "];", 1
        )[0]
        guard_block = TARGET_FLOW_GUARD_JS.split("const sourceFieldIds = [", 1)[1].split(
            "];", 1
        )[0]
        for field_id in ZIWEI_ONLY_TEMPORAL_IDS:
            with self.subTest(field_id=field_id):
                self.assertNotIn(f"'{field_id}'", source_block)
                self.assertNotIn(f"'{field_id}'", guard_block)

    def test_combined_flow_request_payload_still_carries_ziwei_contract_fields(self) -> None:
        payload_block = TARGET_FLOW_JS.split("function payload()", 1)[1].split(
            "function frameCard", 1
        )[0]
        for field_name in (
            "ziwei_daxian_count",
            "ziwei_daxian_frame_id",
            "ziwei_annual_year",
            "ziwei_minor_limit_age",
        ):
            with self.subTest(field_name=field_name):
                self.assertIn(f"{field_name}:", payload_block)

    def test_real_bazi_and_target_dependencies_still_drive_stale_identity(self) -> None:
        source_block = TARGET_FLOW_JS.split("const sourceFieldIds = [", 1)[1].split(
            "];", 1
        )[0]
        target_block = TARGET_FLOW_JS.split("const targetFieldIds = [", 1)[1].split(
            "];", 1
        )[0]
        for field_id in (
            "birth-datetime",
            "birth-place",
            "latitude",
            "longitude",
            "timezone-id",
            "location-manual",
            "sex",
            "precision",
            "uncertainty-seconds",
            "bazi-natal-profile",
            "bazi-temporal-profile",
            "bazi-dayun-count",
        ):
            with self.subTest(source_field_id=field_id):
                self.assertIn(f"'{field_id}'", source_block)
        for field_id in (
            "target-datetime",
            "target-place",
            "target-latitude",
            "target-longitude",
            "target-timezone-id",
            "target-precision",
            "target-uncertainty-seconds",
        ):
            with self.subTest(target_field_id=field_id):
                self.assertIn(f"'{field_id}'", target_block)

    def test_shared_projection_stale_guard_remains_strict(self) -> None:
        shared_source_block = SHARED_APPLY_JS.split("const sourceFieldIds = [", 1)[1].split(
            "];", 1
        )[0]
        for field_id in ZIWEI_ONLY_TEMPORAL_IDS:
            with self.subTest(field_id=field_id):
                self.assertIn(f"'{field_id}'", shared_source_block)
        self.assertIn("observer.observe(ziweiRoot", SHARED_APPLY_JS)
        self.assertIn("紫微显示源已刷新；旧 Projection 已失效。", SHARED_APPLY_JS)


if __name__ == "__main__":
    unittest.main()
