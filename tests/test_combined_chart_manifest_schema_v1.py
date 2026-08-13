from __future__ import annotations

import copy
import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator

from fortune_training.bazi_application import bazi_local_application_v1_profile
from fortune_training.bazi_chart import bazi_foundation_v1_profile
from fortune_training.bazi_temporal import bazi_temporal_v1_continuous_profile
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.combined_chart_application import (
    CombinedChartApplicationRequest,
    CombinedChartService,
    combined_chart_application_v1_profile,
    combined_manifest_payload,
)
from fortune_training.ziwei_application import (
    ziwei_application_default_presentation_profile,
    ziwei_application_v1_profile,
)
from fortune_training.ziwei_chart import ziwei_chart_engine_v1_profile


ROOT = Path(__file__).resolve().parents[1]


class CombinedChartManifestSchemaV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        cls.request = CombinedChartApplicationRequest(
            birth=BirthInput(
                reported_local_datetime=datetime(1994, 5, 17, 14, 30),
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            sex="MALE",
            ziwei_calculation_profile=ziwei_chart_engine_v1_profile(registry),
            ziwei_application_profile=ziwei_application_v1_profile(),
            ziwei_presentation_profile=ziwei_application_default_presentation_profile(),
            bazi_natal_profile=bazi_foundation_v1_profile(registry),
            bazi_temporal_profile=bazi_temporal_v1_continuous_profile(),
            bazi_application_profile=bazi_local_application_v1_profile(),
            combined_profile=combined_chart_application_v1_profile(),
        )
        cls.service = CombinedChartService.from_repository(ROOT)
        cls.resolution = cls.service.resolve(cls.request)
        cls.schema = json.loads(
            (ROOT / "schemas/ziwei-bazi-combined-manifest-v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        cls.validator = Draft202012Validator(cls.schema)

    def test_resolved_and_partial_manifests_validate(self):
        self.validator.validate(combined_manifest_payload(self.resolution))
        partial = self.service.resolve(replace(self.request, ziwei_annual_year=1900))
        self.assertEqual("PARTIAL", partial.status)
        self.validator.validate(combined_manifest_payload(partial))

    def test_schema_rejects_cross_system_semantic_or_prediction_fields(self):
        base = combined_manifest_payload(self.resolution)
        injections = (
            ((), "prediction", "A"),
            ((), "synthesis", "CONFIRMED"),
            (("subsystems", "ziwei"), "score", 0.9),
            (("subsystems", "bazi"), "winner", True),
            (("profiles",), "cross_system_weight", 0.5),
        )
        for path, field, value in injections:
            with self.subTest(path=path, field=field):
                changed = copy.deepcopy(base)
                target = changed
                for key in path:
                    target = target[key]
                target[field] = value
                self.assertTrue(list(self.validator.iter_errors(changed)))

    def test_schema_rejects_full_profile_payload_leakage(self):
        changed = copy.deepcopy(combined_manifest_payload(self.resolution))
        changed["profiles"]["bazi_application"]["prediction_semantics"] = "NOT_INCLUDED"
        changed["combined_profile"]["prediction_semantics"] = "NOT_INCLUDED"
        self.assertTrue(list(self.validator.iter_errors(changed)))


if __name__ == "__main__":
    unittest.main()
