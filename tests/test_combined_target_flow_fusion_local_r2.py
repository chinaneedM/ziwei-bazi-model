from __future__ import annotations

import json
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from fortune_training.combined_chart_application.flow_fusion_local_app import (
    FLOW_FUSION_R2_ENDPOINT,
    FLOW_FUSION_R2_LOCAL_RESOLVE_SCHEMA,
)
from fortune_training.combined_chart_application.flow_local_app import (
    FLOW_LOCAL_APP_RESOLVE_SCHEMA,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedTargetFlowFusionLocalR2Tests(unittest.TestCase):
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
    def target_payload(
        cls,
        *,
        target_datetime: str = "2026-06-01T12:00:00",
        target_place: str = "Greenwich",
        target_latitude: float = 51.4769,
        target_longitude: float = 0.0,
        target_timezone_id: str = "Etc/UTC",
        target_uncertainty_seconds: int = 0,
    ) -> dict[str, object]:
        return {
            **cls.base_payload(),
            "target_datetime": target_datetime,
            "target_place": target_place,
            "target_latitude": target_latitude,
            "target_longitude": target_longitude,
            "target_timezone_id": target_timezone_id,
            "target_precision": "EXACT_SECOND",
            "target_uncertainty_seconds": target_uncertainty_seconds,
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

    def test_application_payload_binds_released_r1_bazi_and_ziwei_outputs(self) -> None:
        app = CombinedChartWorkbenchApplication(ROOT)
        payload = self.target_payload()

        r1 = app.resolve_flow_payload(payload)
        shared = app.resolve_shared_ziwei_projection_payload(payload)
        fusion = app.resolve_flow_fusion_r2_payload(payload)

        self.assertEqual(FLOW_FUSION_R2_LOCAL_RESOLVE_SCHEMA, fusion["schema"])
        result = fusion["combined_target_flow_fusion_r2"]
        self.assertEqual("RESOLVED", result["status"])
        self.assertEqual("PASS", result["integrity"]["status"])

        self.assertEqual(
            r1["combined_target_flow_resolution"]["bundle_hash"],
            result["r1_target_flow_bundle_hash"],
        )
        self.assertEqual(
            r1["combined_target_flow_resolution"]["target_coordinate_fact_hash"],
            result["target_coordinate_fact_hash"],
        )
        self.assertEqual(
            shared["target_coordinate_fact_hash"],
            result["target_coordinate_fact_hash"],
        )
        self.assertEqual(
            r1["bazi_target_flow_bundle"]["bundle_hash"],
            result["bazi_target_flow_bundle_hash"],
        )
        self.assertEqual(
            shared["projection"]["hashes"]["fact_hash"],
            result["ziwei_selector_fact_hash"],
        )
        self.assertEqual(
            shared["projection"]["hashes"]["computation_hash"],
            result["ziwei_selector_computation_hash"],
        )
        self.assertEqual(
            "PASS",
            fusion["target_coordinate_resolution"]["integrity"]["status"],
        )
        self.assertEqual(
            "PASS",
            fusion["ziwei_selector_projection"]["integrity"]["status"],
        )

    def test_real_workbench_exposes_additive_r2_endpoint_and_preserves_r1(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        self.assertEqual("127.0.0.1", server.server_address[0])
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            with self._post(
                f"http://{host}:{port}{FLOW_FUSION_R2_ENDPOINT}",
                self.target_payload(),
            ) as response:
                self.assertEqual(200, response.status)
                self.assertEqual(
                    "nosniff",
                    response.headers["X-Content-Type-Options"],
                )
                fusion = json.loads(response.read().decode("utf-8"))

            self.assertEqual(FLOW_FUSION_R2_LOCAL_RESOLVE_SCHEMA, fusion["schema"])
            self.assertEqual(
                "PASS",
                fusion["combined_target_flow_fusion_r2"]["integrity"]["status"],
            )

            with self._post(
                f"http://{host}:{port}/api/resolve-flow",
                self.target_payload(),
            ) as response:
                self.assertEqual(200, response.status)
                r1 = json.loads(response.read().decode("utf-8"))
            self.assertEqual(FLOW_LOCAL_APP_RESOLVE_SCHEMA, r1["schema"])
            self.assertEqual(
                "PASS",
                r1["combined_target_flow_resolution"]["integrity"]["status"],
            )
            self.assertEqual(
                r1["combined_target_flow_resolution"]["bundle_hash"],
                fusion["combined_target_flow_fusion_r2"][
                    "r1_target_flow_bundle_hash"
                ],
            )
        finally:
            server.shutdown()
            thread.join(timeout=10)
            server.server_close()

    def test_dst_fold_remains_explicit_uncertainty_at_r2_http_boundary(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            payload = self.target_payload(
                target_datetime="2026-11-01T01:30:00",
                target_place="New York",
                target_latitude=40.7128,
                target_longitude=-74.0060,
                target_timezone_id="America/New_York",
            )
            with self._post(
                f"http://{host}:{port}{FLOW_FUSION_R2_ENDPOINT}",
                payload,
            ) as response:
                self.assertEqual(200, response.status)
                fusion = json.loads(response.read().decode("utf-8"))

            result = fusion["combined_target_flow_fusion_r2"]
            self.assertEqual("UNCERTAINTY_PRESENT", result["status"])
            self.assertEqual(
                "MULTI_CANDIDATE_OR_BOUNDARY_UNCERTAINTY",
                result["target_coordinate_status"],
            )
            self.assertEqual("PASS", result["integrity"]["status"])
            self.assertGreaterEqual(result["ziwei_selector_candidate_count"], 2)
        finally:
            server.shutdown()
            thread.join(timeout=10)
            server.server_close()

    def test_out_of_materialized_flow_range_fails_closed_before_fusion(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            with self.assertRaises(HTTPError) as caught:
                self._post(
                    f"http://{host}:{port}{FLOW_FUSION_R2_ENDPOINT}",
                    self.target_payload(target_datetime="2500-06-01T12:00:00"),
                )
            self.assertEqual(422, caught.exception.code)
            error = json.loads(caught.exception.read().decode("utf-8"))["error"]
            self.assertEqual(
                "BAZI_APP_FLOW_CONTEXT_RESOLUTION_FAILED",
                error["code"],
            )
        finally:
            server.shutdown()
            thread.join(timeout=10)
            server.server_close()


if __name__ == "__main__":
    unittest.main()
