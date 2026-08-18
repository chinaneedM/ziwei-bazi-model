from __future__ import annotations

import json
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from fortune_training.bazi_target_temporal import TargetTemporalCoordinateFoundation
from fortune_training.calendar_foundation.models import json_value
from fortune_training.combined_chart_application.shared_time_service import (
    SharedZiweiSelectorProjectionService,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
    build_workbench_server,
)


ROOT = Path(__file__).resolve().parents[1]
SHARED_SCHEMA = "ZIWEI-BAZI-COMBINED-LOCAL-SHARED-ZIWEI-PROJECTION-R1"


class CombinedBrowserSharedTargetApplyHttpR1Tests(unittest.TestCase):
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

    def test_real_workbench_exposes_all_existing_routes_plus_shared_projection(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        self.assertEqual("127.0.0.1", server.server_address[0])
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            with self._post(
                f"http://{host}:{port}/api/shared-ziwei-projection",
                self.target_payload(),
            ) as response:
                self.assertEqual(200, response.status)
                self.assertEqual("nosniff", response.headers["X-Content-Type-Options"])
                data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(SHARED_SCHEMA, data["schema"])
            self.assertEqual("PASS", data["projection"]["integrity"]["status"])

            with self._post(
                f"http://{host}:{port}/api/resolve",
                self.base_payload(),
            ) as response:
                self.assertEqual(200, response.status)

            interaction_payload = {
                **self.base_payload(),
                "ziwei_origin_designation_id": "LIFE",
            }
            with self._post(
                f"http://{host}:{port}/api/ziwei-interaction",
                interaction_payload,
            ) as response:
                self.assertEqual(200, response.status)

            with self._post(
                f"http://{host}:{port}/api/resolve-flow",
                self.target_payload(),
            ) as response:
                self.assertEqual(200, response.status)
        finally:
            server.shutdown()
            thread.join(timeout=10)
            server.server_close()

    def test_endpoint_exactly_serializes_released_projection_service(self) -> None:
        app = CombinedChartWorkbenchApplication(ROOT)
        payload = self.target_payload()
        actual = app.resolve_shared_ziwei_projection_payload(payload)

        combined_request, _ = app._combined_request_from_payload(payload)
        target_input, target_profile = app._shared_target_input_from_payload(payload)
        base = app.service.resolve(combined_request)
        self.assertIsNotNone(base.ziwei_bundle)
        target = TargetTemporalCoordinateFoundation().resolve(target_input, target_profile)
        expected = SharedZiweiSelectorProjectionService().project(
            base.ziwei_bundle,
            target,
            target_profile,
        )
        self.assertEqual(json_value(expected), actual["projection"])
        self.assertEqual(base.ziwei_bundle.bundle_hash, actual["source_ziwei_bundle_hash"])
        self.assertEqual(
            target.hashes.fact_hash,
            actual["target_coordinate_fact_hash"],
        )
        self.assertEqual(
            target.hashes.computation_hash,
            actual["target_coordinate_computation_hash"],
        )

    def test_pre_daxian_projection_preserves_nullable_parent(self) -> None:
        app = CombinedChartWorkbenchApplication(ROOT)
        payload = self.target_payload(
            target_datetime="1994-06-01T12:00:00",
            target_place="Beijing",
            target_latitude=39.9042,
            target_longitude=116.4074,
            target_timezone_id="Asia/Shanghai",
        )
        result = app.resolve_shared_ziwei_projection_payload(payload)["projection"]
        self.assertEqual(1, len(result["candidates"]))
        row = result["candidates"][0]
        self.assertEqual(1994, row["annual_year"])
        self.assertEqual(1, row["minor_limit_age"])
        self.assertIsNone(row["daxian_frame_id"])

    def test_candidate_local_civil_year_wins_over_utc_year(self) -> None:
        app = CombinedChartWorkbenchApplication(ROOT)
        payload = self.target_payload(
            target_datetime="2026-01-01T00:30:00",
            target_place="Kiritimati",
            target_latitude=1.8721,
            target_longitude=-157.4278,
            target_timezone_id="Pacific/Kiritimati",
        )
        result = app.resolve_shared_ziwei_projection_payload(payload)["projection"]
        row = result["candidates"][0]
        self.assertEqual(2026, row["civil_year"])
        self.assertEqual(2026, row["annual_year"])
        self.assertTrue(row["target_utc"].startswith("2025-"))

    def test_dst_fold_preserves_two_distinct_lineages_with_same_selectors(self) -> None:
        app = CombinedChartWorkbenchApplication(ROOT)
        payload = self.target_payload(
            target_datetime="2026-11-01T01:30:00",
            target_place="New York",
            target_latitude=40.7128,
            target_longitude=-74.0060,
            target_timezone_id="America/New_York",
        )
        result = app.resolve_shared_ziwei_projection_payload(payload)["projection"]
        rows = result["candidates"]
        self.assertEqual(2, len(rows))
        self.assertEqual({0, 1}, {row["fold"] for row in rows})
        self.assertEqual(2, len({row["source_target_candidate_id"] for row in rows}))
        self.assertEqual(1, len({row["annual_year"] for row in rows}))
        self.assertEqual(1, len({row["minor_limit_age"] for row in rows}))
        self.assertEqual(1, len({row["daxian_frame_id"] for row in rows}))

    def test_new_year_uncertainty_preserves_both_annual_selector_years(self) -> None:
        app = CombinedChartWorkbenchApplication(ROOT)
        payload = self.target_payload(
            target_datetime="2026-12-31T23:59:30",
            target_place="Greenwich",
            target_latitude=51.4769,
            target_longitude=0.0,
            target_timezone_id="Etc/UTC",
            target_uncertainty_seconds=120,
        )
        result = app.resolve_shared_ziwei_projection_payload(payload)["projection"]
        rows = result["candidates"]
        self.assertGreater(len(rows), 1)
        self.assertEqual({2026, 2027}, {row["annual_year"] for row in rows})
        self.assertEqual({2026, 2027}, {row["civil_year"] for row in rows})
        self.assertEqual(list(range(len(rows))), [row["source_target_candidate_index"] for row in rows])

    def test_out_of_materialized_annual_range_fails_closed(self) -> None:
        server = build_workbench_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            with self.assertRaises(HTTPError) as caught:
                self._post(
                    f"http://{host}:{port}/api/shared-ziwei-projection",
                    self.target_payload(target_datetime="2500-06-01T12:00:00"),
                )
            self.assertEqual(422, caught.exception.code)
            error = json.loads(caught.exception.read().decode("utf-8"))["error"]
            self.assertEqual(
                "SHARED_ZIWEI_ANNUAL_FRAME_NOT_EXACTLY_ONE",
                error["code"],
            )
        finally:
            server.shutdown()
            thread.join(timeout=10)
            server.server_close()


if __name__ == "__main__":
    unittest.main()
