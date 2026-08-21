from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator

from fortune_training.bazi_chart import BaziChartFoundation, BaziChartRequest
from fortune_training.bazi_chart.integrity import natal_hash_bundle
from fortune_training.bazi_chart.profile import bazi_foundation_v1_profile
from fortune_training.bazi_chart.registries import PILLAR_POSITIONS, SEXAGENARY_CYCLE
from fortune_training.bazi_nayin_annotation import (
    BaziNayinAnnotationService,
    NAYIN_REGISTRY,
    NAYIN_REGISTRY_ID,
    NAYIN_REGISTRY_VERSION,
    RELEASED_ZIWEI_NAYIN_PAIRS_SHA256,
    compute_nayin_hashes,
    entry_for_sexagenary_index,
    released_registry_hash,
    validate_nayin_full_replay,
    validate_nayin_resolution,
    validate_released_registry,
)
from fortune_training.calendar_foundation import BirthInput, TimePrecision
from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_chart.registries import NAYIN_PAIRS as RELEASED_ZIWEI_NAYIN_PAIRS


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "bazi-nayin-annotation-r1.schema.json"


class BaziNayinAnnotationR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.foundation = BaziChartFoundation.from_repository(ROOT)
        cls.profile = bazi_foundation_v1_profile(cls.foundation.time_calendar.policy_registry)
        cls.birth = BirthInput(
            reported_local_datetime=datetime(1994, 5, 17, 14, 30),
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
            precision=TimePrecision.EXACT_SECOND,
            uncertainty_seconds=0,
        )
        typed = cls.foundation.resolve_typed(BaziChartRequest(birth=cls.birth, profile=cls.profile))
        if not typed.candidates:
            raise AssertionError(f"fixture Bazi foundation failed: {typed.diagnostics}")
        cls.candidate = typed.candidates[0]
        cls.natal = cls.candidate.chart
        cls.service = BaziNayinAnnotationService()
        cls.resolution = cls.service.resolve(cls.natal, cls.profile)

        with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
            cls.schema = json.load(handle)
        cls.validator = Draft202012Validator(cls.schema)

    def test_released_registry_is_pinned_and_complete(self) -> None:
        validate_released_registry()
        self.assertEqual(released_registry_hash(), RELEASED_ZIWEI_NAYIN_PAIRS_SHA256)
        self.assertEqual(len(RELEASED_ZIWEI_NAYIN_PAIRS), 30)
        self.assertEqual(len(NAYIN_REGISTRY), 30)
        self.assertEqual(len(SEXAGENARY_CYCLE), 60)

    def test_all_60_bazi_identities_exactly_match_released_ziwei_nayin_registry(self) -> None:
        for index, ganzhi in enumerate(SEXAGENARY_CYCLE):
            with self.subTest(index=index, ganzhi=ganzhi):
                entry = entry_for_sexagenary_index(index)
                released_name, released_element = RELEASED_ZIWEI_NAYIN_PAIRS[index // 2]
                self.assertEqual(entry.display_name, released_name)
                self.assertEqual(entry.element, released_element)
                self.assertIn(ganzhi, entry.ganzhi)
                self.assertIn(index, entry.sexagenary_indexes)

    def test_30_semantic_ids_each_cover_exactly_two_consecutive_indices(self) -> None:
        semantic_ids = {entry.semantic_id for entry in NAYIN_REGISTRY}
        self.assertEqual(len(semantic_ids), 30)
        covered: list[int] = []
        for pair_index, entry in enumerate(NAYIN_REGISTRY):
            self.assertEqual(entry.semantic_id, f"NAYIN:PAIR:{pair_index:02d}")
            self.assertEqual(entry.sexagenary_indexes, (pair_index * 2, pair_index * 2 + 1))
            self.assertEqual(
                entry.ganzhi,
                (SEXAGENARY_CYCLE[pair_index * 2], SEXAGENARY_CYCLE[pair_index * 2 + 1]),
            )
            covered.extend(entry.sexagenary_indexes)
        self.assertEqual(covered, list(range(60)))

    def test_ordinary_natal_emits_exactly_four_pillar_annotations(self) -> None:
        result = self.resolution
        self.assertEqual(result.integrity.status, "PASS")
        self.assertEqual(tuple(row.source_pillar_position for row in result.annotations), PILLAR_POSITIONS)
        self.assertEqual(len(result.annotations), 4)
        for pillar, annotation in zip(self.natal.pillars, result.annotations, strict=True):
            entry = entry_for_sexagenary_index(pillar.sexagenary_index)
            self.assertEqual(annotation.source_pillar_ganzhi, pillar.ganzhi)
            self.assertEqual(annotation.source_pillar_sexagenary_index, pillar.sexagenary_index)
            self.assertEqual(annotation.source_stem_instance_id, pillar.stem_instance_id)
            self.assertEqual(annotation.source_branch_instance_id, pillar.branch_instance_id)
            self.assertEqual(annotation.nayin_semantic_id, entry.semantic_id)
            self.assertEqual(annotation.display_name, entry.display_name)
            self.assertEqual(annotation.element, entry.element)
            self.assertEqual(annotation.registry_id, NAYIN_REGISTRY_ID)
            self.assertEqual(annotation.registry_version, NAYIN_REGISTRY_VERSION)

    def test_resolution_is_deterministic_and_full_replay_passes(self) -> None:
        second = self.service.resolve(self.natal, self.profile)
        self.assertEqual(json_value(second), json_value(self.resolution))
        replay = validate_nayin_full_replay(self.natal, self.profile, self.resolution)
        self.assertEqual(replay.status, "PASS", replay.diagnostics)

    def test_annotation_does_not_mutate_upstream_natal_state_or_hashes(self) -> None:
        before_state = json_value(self.natal)
        before_hashes = natal_hash_bundle(self.natal, self.profile)
        result = self.service.resolve(self.natal, self.profile)
        after_hashes = natal_hash_bundle(self.natal, self.profile)
        self.assertEqual(json_value(self.natal), before_state)
        self.assertEqual(after_hashes, before_hashes)
        self.assertEqual(result.source_natal_fact_hash, before_hashes.fact_hash)
        self.assertEqual(result.source_natal_computation_hash, before_hashes.computation_hash)

    def test_invalid_upstream_sexagenary_index_fails_closed(self) -> None:
        first = self.natal.pillars[0]
        bad_first = replace(first, sexagenary_index=(first.sexagenary_index + 1) % 60)
        bad_natal = replace(self.natal, pillars=(bad_first,) + self.natal.pillars[1:])
        with self.assertRaisesRegex(ValueError, "invalid upstream Bazi Natal state"):
            self.service.resolve(bad_natal, self.profile)

    def test_source_profile_identity_mismatch_fails_closed(self) -> None:
        wrong_profile = replace(self.profile, profile_version="999.0.0")
        with self.assertRaisesRegex(ValueError, "Natal/profile identity mismatch"):
            self.service.resolve(self.natal, wrong_profile)
        report = validate_nayin_resolution(self.natal, wrong_profile, self.resolution)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SOURCE_NATAL_PROFILE_MISMATCH", {row.code for row in report.diagnostics})

    def test_wrong_annotation_with_recomputed_local_hashes_still_fails_replay(self) -> None:
        original = self.resolution.annotations[0]
        replacement_name = "炉中火" if original.display_name != "炉中火" else "海中金"
        wrong = replace(original, display_name=replacement_name)
        annotations = (wrong,) + self.resolution.annotations[1:]
        fact_hash, computation_hash = compute_nayin_hashes(
            source_natal_fact_hash=self.resolution.source_natal_fact_hash,
            source_natal_computation_hash=self.resolution.source_natal_computation_hash,
            annotations=annotations,
        )
        rewritten = replace(
            self.resolution,
            annotations=annotations,
            fact_hash=fact_hash,
            computation_hash=computation_hash,
        )
        report = validate_nayin_resolution(self.natal, self.profile, rewritten)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("ANNOTATION_REPLAY_MISMATCH", {row.code for row in report.diagnostics})
        replay = validate_nayin_full_replay(self.natal, self.profile, rewritten)
        self.assertEqual(replay.status, "FAIL")
        self.assertIn("FULL_REPLAY_MISMATCH", {row.code for row in replay.diagnostics})

    def test_source_hash_tamper_fails_integrity(self) -> None:
        tampered = replace(self.resolution, source_natal_fact_hash="0" * 64)
        report = validate_nayin_resolution(self.natal, self.profile, tampered)
        self.assertEqual(report.status, "FAIL")
        codes = {row.code for row in report.diagnostics}
        self.assertIn("SOURCE_NATAL_FACT_HASH_MISMATCH", codes)
        self.assertIn("ANNOTATION_FACT_HASH_MISMATCH", codes)

    def test_closed_schema_accepts_release_and_rejects_interpretation_fields(self) -> None:
        payload = json_value(self.resolution)
        self.validator.validate(payload)

        top_level = dict(payload)
        top_level["strength"] = "STRONG"
        self.assertTrue(list(self.validator.iter_errors(top_level)))

        inner = json.loads(json.dumps(payload, ensure_ascii=False))
        inner["annotations"][0]["auspiciousness"] = "AUSPICIOUS"
        self.assertTrue(list(self.validator.iter_errors(inner)))

        prediction = dict(payload)
        prediction["prediction"] = "EVENT"
        self.assertTrue(list(self.validator.iter_errors(prediction)))

    def test_r1_contains_no_temporal_nayin_rows_or_interpretive_fields(self) -> None:
        payload = json_value(self.resolution)
        serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        self.assertNotIn("DAYUN", serialized)
        self.assertNotIn("ANNUAL", serialized)
        self.assertNotIn("MONTHLY", serialized)
        self.assertNotIn("DAILY", serialized)
        self.assertNotIn("HOURLY", serialized)
        for forbidden in ("旺衰", "格局", "用神", "喜忌", "prediction", "winner", "score"):
            self.assertNotIn(forbidden, serialized)


if __name__ == "__main__":
    unittest.main()
