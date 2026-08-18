from __future__ import annotations

import unittest

from fortune_training.combined_chart_application.interaction_assets import INTERACTION_JS


class CombinedBrowserZiweiInteractionStaleGuardR1Tests(unittest.TestCase):
    def test_displayed_source_fingerprint_covers_all_user_inputs_that_can_stale_the_svg(self) -> None:
        self.assertIn("displayedInputFingerprint", INTERACTION_JS)
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
            "ziwei-daxian-count",
            "ziwei-daxian-frame-id",
            "ziwei-annual-year",
            "ziwei-minor-limit-age",
            "bazi-natal-profile",
            "bazi-temporal-profile",
            "bazi-dayun-count",
        ):
            with self.subTest(field_id=field_id):
                self.assertIn(f"'{field_id}'", INTERACTION_JS)

    def test_palace_and_temporal_interactions_fail_closed_when_displayed_source_is_stale(self) -> None:
        self.assertIn("function displayedInputIsCurrent()", INTERACTION_JS)
        self.assertIn("function staleSourceMessage()", INTERACTION_JS)
        self.assertGreaterEqual(
            INTERACTION_JS.count("if (!displayedInputIsCurrent())"),
            2,
        )
        self.assertIn(
            "请先点击“联合排盘”，再进行三合交互。",
            INTERACTION_JS,
        )
        self.assertIn(
            "state.displayedInputFingerprint = inputFingerprint();",
            INTERACTION_JS,
        )


if __name__ == "__main__":
    unittest.main()
