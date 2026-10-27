from __future__ import annotations

import json
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from fortune_training.combined_chart_application.shared_time_models import (
    SharedZiweiSelectorProjectionIntegrityReport,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]


class SharedZiweiProjectionEndpointReplayGateR1Tests(unittest.TestCase):
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

    @staticmethod
    def _post(url: str, payload: dict[str, object]):
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        return urlopen(request, timeout=90)

    def test_standalone_endpoint_fails_closed_when_full_replay_fails(self) -> None:
        failed = SharedZiweiSelectorProjectionIntegrityReport(
            status="FAIL",
            diagnostics=("FORCED_STANDALONE_FULL_REPLAY_FAILURE",),
        )
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            with patch(
                "fortune_training.combined_chart_application.shared_apply_local_app."
                "validate_shared_ziwei_selector_full_replay",
                return_value=failed,
            ):
                with self.assertRaises(HTTPError) as caught:
                    self._post(
                        f"http://{host}:{port}/api/shared-ziwei-projection",
                        self.payload(),
                    )
            self.assertEqual(422, caught.exception.code)
            error = json.loads(caught.exception.read().decode("utf-8"))["error"]
            self.assertEqual(
                "LOCAL_APP_SHARED_ZIWEI_FULL_REPLAY_FAILED",
                error["code"],
            )
            self.assertIn(
                "FORCED_STANDALONE_FULL_REPLAY_FAILURE",
                error["detail"],
            )
        finally:
            server.shutdown()
            thread.join(timeout=10)
            server.server_close()


if __name__ == "__main__":
    unittest.main()
