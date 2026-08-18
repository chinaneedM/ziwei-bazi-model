from __future__ import annotations

import re
import unittest

from fortune_training.combined_chart_application.shared_apply_assets import SHARED_APPLY_JS
from fortune_training.combined_chart_application.target_flow_assets import TARGET_FLOW_JS


TARGET_TEMPORAL_PROFILE_ID = "BAZI-TARGET-TEMPORAL-COORDINATE-FOUNDATION-R1"


class CombinedSharedTargetProfileDomContractR1Tests(unittest.TestCase):
    def test_shared_apply_direct_target_value_reads_exist_in_target_flow_dom(self) -> None:
        target_dom_ids = set(re.findall(r'id=\\"(target-[^\\"]+)\\"', TARGET_FLOW_JS))
        direct_target_reads = {
            field_id
            for field_id in re.findall(r"\$\('([^']+)'\)\.value", SHARED_APPLY_JS)
            if field_id.startswith("target-")
        }
        self.assertTrue(target_dom_ids)
        self.assertTrue(direct_target_reads)
        self.assertEqual(set(), direct_target_reads - target_dom_ids)

    def test_target_temporal_profile_is_released_constant_not_dom_input(self) -> None:
        expected = f"target_temporal_profile_id: '{TARGET_TEMPORAL_PROFILE_ID}'"
        self.assertIn(expected, TARGET_FLOW_JS)
        self.assertIn(expected, SHARED_APPLY_JS)
        self.assertNotIn("$('target-temporal-profile').value", SHARED_APPLY_JS)
        self.assertNotIn("'target-temporal-profile'", SHARED_APPLY_JS)
        self.assertNotIn('id=\\"target-temporal-profile\\"', TARGET_FLOW_JS)

    def test_actual_editable_target_fields_remain_stale_guard_inputs(self) -> None:
        target_field_block = SHARED_APPLY_JS.split("const targetFieldIds = [", 1)[1].split("];", 1)[0]
        for field_id in (
            "target-datetime",
            "target-place",
            "target-latitude",
            "target-longitude",
            "target-timezone-id",
            "target-precision",
            "target-uncertainty-seconds",
        ):
            with self.subTest(field_id=field_id):
                self.assertIn(f"'{field_id}'", target_field_block)
        self.assertNotIn("target-temporal-profile", target_field_block)
        self.assertIn("projectionTargetFingerprint !== targetFingerprint()", SHARED_APPLY_JS)


if __name__ == "__main__":
    unittest.main()
