from __future__ import annotations

import json
import threading
import unittest
from pathlib import Path
from urllib.request import Request, urlopen

from fortune_training.combined_chart_application.flow_local_app import (
    build_flow_server,
)
from fortune_training.combined_chart_application.local_app import (
    LOCAL_APP_RESOLVE_SCHEMA,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedTargetFlowHttpR1Tests(unittest.TestCase):
    @staticmethod
    def base_payload() -> dict[str, object]:
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
        }

    @classmethod
    def flow_payload(cls) -> dict[str, object]:
        return {
            **cls.base_payload(),
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
        return urlopen(request, timeout=45)

    def test_real_loopback_server_exposes_flow_and_preserves_legacy_route(self) -> None:
        server = build_flow_server(ROOT, port=0)
        self.assertEqual("127.0.0.1", server.server_address[0])
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            with self._post(
                f"http://{host}:{port}/api/resolve-flow",
                self.flow_payload(),
            ) as response:
                self.assertEqual(200, response.status)
                self.assertEqual(
                    "nosniff", response.headers["X-Content-Type-Options"]
                )
                self.assertIn(
                    "default-src 'self'",
                    response.headers["Content-Security-Policy"],
                )
                flow_payload = json.loads(response.read().decode("utf-8"))
            self.assertEqual(
                "ZIWEI-BAZI-COMBINED-LOCAL-FLOW-RESOLVE-R1",
                flow_payload["schema"],
            )
            self.assertEqual(
                "PASS",
                flow_payload["combined_target_flow_resolution"]["integrity"][
                    "status"
                ],
            )

            with self._post(
                f"http://{host}:{port}/api/resolve",
                self.base_payload(),
            ) as response:
                self.assertEqual(200, response.status)
                legacy_payload = json.loads(response.read().decode("utf-8"))
            self.assertEqual(LOCAL_APP_RESOLVE_SCHEMA, legacy_payload["schema"])
            self.assertEqual(
                "PASS",
                legacy_payload["combined_resolution"]["integrity"]["status"],
            )
        finally:
            server.shutdown()
            thread.join(timeout=10)
            server.server_close()


if __name__ == "__main__":
    unittest.main()
