from __future__ import annotations

import unittest
from pathlib import Path

from fortune_training.combined_chart_application.flow_local_app import (
    FlowLocalCombinedChartApplication,
)
from fortune_training.combined_chart_application.local_app import (
    LocalCombinedAppRequestError,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedTargetFlowCoordinateValidationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = FlowLocalCombinedChartApplication(ROOT)

    @staticmethod
    def payload() -> dict[str, object]:
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
            "ziwei_minor_limit_age": None,
            "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
            "bazi_dayun_count": 12,
            "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
            "target_datetime": "2026-06-01T12:00:00",
            "target_place": "Greenwich",
            "target_latitude": 51.4769,
            "target_longitude": 0.0,
            "target_timezone_id": "Etc/UTC",
            "target_precision": "EXACT_SECOND",
            "target_uncertainty_seconds": 0,
            "target_temporal_profile_id": (
                "BAZI-TARGET-TEMPORAL-COORDINATE-FOUNDATION-R1"
            ),
        }

    def test_birth_coordinate_out_of_range_is_structured_local_error(self) -> None:
        payload = self.payload()
        payload["latitude"] = 91.0
        with self.assertRaises(LocalCombinedAppRequestError) as error:
            self.app.resolve_flow_payload(payload)
        self.assertEqual("LOCAL_APP_INVALID_INPUT", error.exception.code)
        self.assertIn("latitude", error.exception.detail)

    def test_target_coordinate_out_of_range_is_structured_local_error(self) -> None:
        payload = self.payload()
        payload["target_longitude"] = 181.0
        with self.assertRaises(LocalCombinedAppRequestError) as error:
            self.app.resolve_flow_payload(payload)
        self.assertEqual("LOCAL_APP_INVALID_INPUT", error.exception.code)
        self.assertIn("target_longitude", error.exception.detail)


if __name__ == "__main__":
    unittest.main()
