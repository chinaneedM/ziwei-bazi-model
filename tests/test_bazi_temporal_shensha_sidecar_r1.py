from __future__ import annotations

import copy
import json
import unittest
from dataclasses import replace
from pathlib import Path

import jsonschema

from fortune_training.bazi_target_temporal import (
    TargetTemporalInput,
    bazi_target_temporal_coordinate_r1_profile,
)
from fortune_training.calendar_foundation.models import json_value
from fortune_training.combined_chart_application.flow_models import CombinedTargetFlowRequest
from fortune_training.combined_chart_application.flow_local_app import FlowLocalCombinedChartApplication
from fortune_training.bazi_temporal_shensha_sidecar import (
    BaziTemporalShenshaSidecarService,
    TemporalShenshaSidecarResolutionError,
    coherent_source_shensha_for_candidates,
    validate_temporal_shensha_sidecar_full_replay,
    validate_temporal_shensha_sidecar_resolution,
)


ROOT = Path(__file__).resolve().parents[1]


class BaziTemporalShenshaSidecarR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = FlowLocalCombinedChartApplication(ROOT)
        cls.service = BaziTemporalShenshaSidecarService()
        cls.schema = json.loads(
            (
                ROOT
                / "schemas"
                / "bazi-temporal-shensha-projection-sidecar-r1.schema.json"
            ).read_text(encoding="utf-8")
        )

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
            "ziwei_daxian_frame_id": "DAXIAN:index=1",
            "ziwei_annual_year": 2025,
            "ziwei_minor_limit_age": 8,
            "bazi_natal_profile_id": "BAZI-FOUNDATION-V1-R1",
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
            "target_temporal_profile_id": "BAZI-TARGET-TEMPORAL-COORDINATE-FOUNDATION-R1",
        }

    @classmethod
    def upstream(cls):
        payload = cls.payload()
        combined_request, _ = cls.app._combined_request_from_payload(payload)
        target_input = TargetTemporalInput(
            reported_local_datetime=cls.app._target_datetime(payload),
            target_place=str(payload["target_place"]),
            latitude=float(payload["target_latitude"]),
            longitude=float(payload["target_longitude"]),
            timezone_id=str(payload["target_timezone_id"]),
            uncertainty_seconds=int(payload["target_uncertainty_seconds"]),
        )
        request = CombinedTargetFlowRequest(
            combined_request=combined_request,
            target_input=target_input,
            target_coordinate_profile=bazi_target_temporal_coordinate_r1_profile(),
        )
        base, flow, _ = cls.app.flow_service.resolve_with_bundles(request)
        if base.bazi_bundle is None:
            raise RuntimeError("fixture requires Bazi application bundle")
        return base.bazi_bundle, flow

    def test_sidecar_is_independent_schema_bound_and_deterministic(self) -> None:
        base, flow = self.upstream()
        flow_before = copy.deepcopy(flow)
        first = self.service.resolve(base, flow)
        second = self.service.resolve(base, flow)
        self.assertEqual(first, second)
        self.assertEqual(flow_before, flow)
        self.assertEqual("PASS", first.integrity.status)
        self.assertEqual(
            "PASS", validate_temporal_shensha_sidecar_resolution(first).status
        )
        self.assertEqual(base.bundle_hash, first.base_application_bundle_hash)
        self.assertEqual(flow.bundle_hash, first.bazi_target_flow_bundle_hash)
        self.assertEqual(len(flow.candidates), len(first.candidates))
        jsonschema.Draft202012Validator(self.schema).validate(json_value(first))

        for index, candidate in enumerate(first.candidates):
            source = flow.candidates[index]
            self.assertEqual(source.candidate_id, candidate.source_bazi_target_flow_candidate_id)
            self.assertEqual(index, candidate.source_bazi_target_flow_candidate_index)
            self.assertEqual(
                source.source_application_candidate_ids,
                candidate.source_application_candidate_ids,
            )
            projection = candidate.projection
            self.assertEqual(
                "ENGINEERING_TARGET_MATCH_NOT_CLASSICAL_TEMPORAL_APPLICABILITY",
                projection["projection_policy"],
            )
            self.assertEqual(
                "SOURCE_CANDIDATES_PRESERVED_NO_WINNER",
                projection["selection_semantics"],
            )
            self.assertEqual(29, len(projection["eligible_source_candidates"]))
            self.assertEqual(26, projection["annual"]["evaluated_candidate_count"])
            self.assertEqual(29, projection["daily"]["evaluated_candidate_count"])
            self.assertEqual(2, len(projection["xiaoyun_candidates"]))

    def test_full_replay_passes_and_projection_tamper_fails(self) -> None:
        base, flow = self.upstream()
        sidecar = self.service.resolve(base, flow)
        self.assertEqual(
            "PASS",
            validate_temporal_shensha_sidecar_full_replay(
                self.service, base, flow, sidecar
            ).status,
        )
        tampered = copy.deepcopy(sidecar)
        tampered.candidates[0].projection["projection_policy"] = "TAMPERED"
        report = validate_temporal_shensha_sidecar_full_replay(
            self.service, base, flow, tampered
        )
        self.assertEqual("FAIL", report.status)
        self.assertTrue(
            any("PROJECTION_POLICY_MISMATCH" in row for row in report.diagnostics)
        )
        self.assertTrue(any("FULL_REPLAY_MISMATCH" in row for row in report.diagnostics))

    def test_source_shensha_lineage_mismatch_fails_closed(self) -> None:
        base, _ = self.upstream()
        original = base.candidates[0]
        altered_view = copy.deepcopy(original.view)
        altered_view["shensha"] = copy.deepcopy(altered_view["shensha"])
        altered_view["shensha"]["candidate_set_id"] = "TAMPERED-CANDIDATE-SET"
        altered = replace(
            original,
            candidate_id=original.candidate_id + ":ALTERED",
            view=altered_view,
        )
        with self.assertRaises(TemporalShenshaSidecarResolutionError) as caught:
            coherent_source_shensha_for_candidates((original, altered))
        self.assertEqual(
            "BAZI_TEMPORAL_SHENSHA_SOURCE_LINEAGE_MISMATCH",
            caught.exception.code,
        )

    def test_resolve_flow_exposes_sidecar_without_mutating_old_flow_bundle(self) -> None:
        base, flow = self.upstream()
        response = self.app.resolve_flow_payload(self.payload())
        self.assertIn("bazi_temporal_shensha_projection_bundle", response)
        sidecar = response["bazi_temporal_shensha_projection_bundle"]
        self.assertEqual("PASS", sidecar["integrity"]["status"])
        self.assertEqual(base.bundle_hash, sidecar["base_application_bundle_hash"])
        self.assertEqual(flow.bundle_hash, response["bazi_target_flow_bundle"]["bundle_hash"])
        self.assertEqual(flow.bundle_hash, sidecar["bazi_target_flow_bundle_hash"])
        jsonschema.Draft202012Validator(self.schema).validate(sidecar)


if __name__ == "__main__":
    unittest.main()
