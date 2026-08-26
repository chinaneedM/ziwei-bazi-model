from __future__ import annotations

import copy
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_application import (
    BaziApplicationRequest,
    BaziApplicationResolutionError,
    BaziChartService,
    bazi_local_application_v1_profile,
    validate_application_resolution,
)
from fortune_training.bazi_application.local_app import (
    LocalAppRequestError,
    LocalBaziApplication,
)
from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    bazi_foundation_v1_profile,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    BaziTemporalEngine,
    BaziTemporalRequest,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry
from fortune_training.calendar_foundation.models import json_value


ROOT = Path(__file__).resolve().parents[1]


class BaziApplicationV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = PolicyRegistry.from_file(
            ROOT / "config" / "time-calendar-policies.json"
        )
        cls.natal_profile = bazi_foundation_v1_profile(cls.registry)
        cls.temporal_profile = bazi_temporal_v1_continuous_profile()
        cls.application_profile = bazi_local_application_v1_profile()
        cls.birth = BirthInput(
            reported_local_datetime=datetime(1984, 2, 10, 10, 30),
            birth_place="Beijing",
            latitude=39.9042,
            longitude=116.4074,
            timezone_id="Asia/Shanghai",
        )
        cls.request = BaziApplicationRequest(
            birth=cls.birth,
            sex=BaziSex.MALE,
            natal_profile=cls.natal_profile,
            temporal_profile=cls.temporal_profile,
            application_profile=cls.application_profile,
            dayun_count=12,
        )
        cls.foundation = BaziChartFoundation.from_repository(ROOT)
        cls.service = BaziChartService.from_repository(ROOT)
        cls.natal_resolution = cls.foundation.resolve_typed(
            BaziChartRequest(cls.birth, cls.natal_profile)
        )
        if len(cls.natal_resolution.candidates) != 1:
            raise AssertionError(cls.natal_resolution)
        cls.natal = cls.natal_resolution.candidates[0]
        cls.temporal_resolution = BaziTemporalEngine().resolve_typed(
            BaziTemporalRequest(
                cls.natal,
                BaziSex.MALE,
                cls.temporal_profile,
                12,
            )
        )
        if len(cls.temporal_resolution.candidates) != 1:
            raise AssertionError(cls.temporal_resolution)
        cls.temporal = cls.temporal_resolution.candidates[0]
        cls.bundle = cls.service.resolve(cls.request)

    def test_valid_birth_resolves_usable_application_bundle(self):
        self.assertEqual("RESOLVED", self.bundle.status)
        self.assertEqual("PASS", self.bundle.integrity.status)
        self.assertEqual(1, len(self.bundle.candidates))
        self.assertTrue(self.bundle.source_fact_hash)
        self.assertTrue(self.bundle.view_hash)
        self.assertTrue(self.bundle.bundle_hash)

    def test_displayed_pillars_exactly_match_natal_candidate(self):
        view = self.bundle.candidates[0].view
        self.assertEqual(
            [(row.position, row.ganzhi) for row in self.natal.chart.pillars],
            [(row["position"], row["ganzhi"]) for row in view["pillars"]],
        )
        self.assertEqual(self.natal.chart.day_master_stem, view["day_master_stem"])

    def test_hidden_stems_and_ten_gods_replay_exactly(self):
        view = self.bundle.candidates[0].view
        ten_god_by_target = {
            row.target_instance_id: row for row in self.natal.chart.ten_gods
        }
        hidden_by_branch: dict[str, list] = {}
        for row in self.natal.chart.hidden_stems:
            hidden_by_branch.setdefault(row.branch_instance_id, []).append(row)
        for rows in hidden_by_branch.values():
            rows.sort(key=lambda item: item.registry_ordinal)
        branch_by_position = {
            row.position: row for row in self.natal.chart.branches
        }
        stem_by_position = {row.position: row for row in self.natal.chart.stems}
        for pillar in view["pillars"]:
            position = pillar["position"]
            stem = stem_by_position[position]
            branch = branch_by_position[position]
            self.assertEqual(
                ten_god_by_target[stem.instance_id].display_name,
                pillar["visible_ten_god"],
            )
            expected_hidden = hidden_by_branch.get(branch.instance_id, [])
            self.assertEqual(
                [row.stem for row in expected_hidden],
                [row["stem"] for row in pillar["hidden_stems"]],
            )
            self.assertEqual(
                [ten_god_by_target[row.instance_id].display_name for row in expected_hidden],
                [row["ten_god"] for row in pillar["hidden_stems"]],
            )

    def test_xunkong_and_twelve_growth_are_identity_only_annotations(self):
        for candidate in self.bundle.candidates:
            for pillar in candidate.view["pillars"]:
                xunkong = pillar["xunkong"]
                growth = pillar["day_master_twelve_growth"]
                self.assertEqual(2, len(xunkong["void_branches"]))
                self.assertEqual(
                    "IDENTITY_ONLY_NO_AUSPICIOUSNESS",
                    xunkong["semantic_scope"],
                )
                self.assertEqual(
                    self.natal.chart.day_master_stem,
                    growth["source_stem"],
                )
                self.assertEqual(pillar["branch"], growth["target_branch"])
                self.assertEqual(
                    "PHASE_IDENTITY_ONLY_NO_STRENGTH_CONCLUSION",
                    growth["semantic_scope"],
                )
                self.assertEqual(
                    pillar["stem"],
                    pillar["self_twelve_growth"]["source_stem"],
                )

    def test_derived_coordinates_are_profiled_and_identity_only(self):
        for candidate in self.bundle.candidates:
            coordinates = candidate.view["derived_coordinates"]
            self.assertEqual(
                "BAZI-DERIVED-COORDINATES-YHZP-R1",
                coordinates["profile_id"],
            )
            for key in ("taiyuan", "minggong", "shengong"):
                self.assertEqual(2, len(coordinates[key]["ganzhi"]))
                self.assertEqual(
                    "DERIVED_COORDINATE_IDENTITY_ONLY_NO_INTERPRETATION",
                    coordinates[key]["semantic_scope"],
                )

    def test_xiaoyun_alternatives_are_preserved_in_candidate_view_hash(self):
        for candidate in self.bundle.candidates:
            xiaoyun = candidate.view["xiaoyun"]
            self.assertEqual(
                "UNRESOLVED_CLASSICAL_ALTERNATIVES",
                xiaoyun["selection_status"],
            )
            self.assertEqual(2, len(xiaoyun["candidates"]))
            self.assertTrue(
                all(
                    row["status"] == "CANDIDATE_NOT_ARBITRATED"
                    for row in xiaoyun["candidates"]
                )
            )
            self.assertTrue(
                all(
                    frame["semantic_scope"]
                    == "ANNUAL_COORDINATE_ONLY_NO_INTERPRETATION"
                    for row in xiaoyun["candidates"]
                    for frame in row["frames"]
                )
            )

    def test_shensha_anchor_alternatives_are_source_bound_and_unmerged(self):
        for candidate in self.bundle.candidates:
            shensha = candidate.view["shensha"]
            self.assertEqual(
                "UNRESOLVED_CLASSICAL_ANCHOR_ALTERNATIVES",
                shensha["resolution_status"],
            )
            self.assertEqual("NO_WINNER_NO_IMPLICIT_MERGE", shensha["selection_semantics"])
            self.assertEqual(30, len(shensha["candidates"]))
            candidate_keys = {
                (row["shensha_id"], row["anchor_basis"])
                for row in shensha["candidates"]
            }
            self.assertIn(("TIANGUAN", "YEAR_STEM"), candidate_keys)
            self.assertIn(("GONGLU", "YEAR_GANZHI"), candidate_keys)
            self.assertIn(("GONGLU", "DAY_GANZHI"), candidate_keys)
            gonglu = [
                row for row in shensha["candidates"]
                if row["shensha_id"] == "GONGLU"
            ]
            self.assertEqual(2, len(gonglu))
            self.assertTrue(
                all(
                    row["selection_status"] == "CANDIDATE_NOT_ARBITRATED"
                    for row in gonglu
                )
            )
            self.assertTrue(
                all(row["source_refs"] for row in shensha["candidates"])
            )

    def test_shensha_tamper_fails_semantic_replay(self):
        candidate = self.bundle.candidates[0]
        changed_view = copy.deepcopy(candidate.view)
        changed_view["shensha"]["candidates"][0]["target_branches"] = ["子"]
        changed_candidate = replace(candidate, view=changed_view)
        changed_bundle = replace(self.bundle, candidates=(changed_candidate,))
        report = validate_application_resolution(changed_bundle)
        self.assertEqual("FAIL", report.status)
        self.assertIn("SHENSHA_REPLAY_MISMATCH:0", report.diagnostics)

    def test_dayun_direction_jiaoyun_and_frames_replay_exactly(self):
        view = self.bundle.candidates[0].view["dayun"]
        state = self.temporal.state
        self.assertEqual(state.direction.direction, view["direction"])
        self.assertEqual(
            json_value(state.jiaoyun.first_transition_utc),
            view["jiaoyun"]["first_transition_utc"],
        )
        self.assertEqual(
            [(row.index, row.ganzhi) for row in state.dayun_frames],
            [(row["index"], row["ganzhi"]) for row in view["frames"]],
        )

    def test_local_apparent_solar_provenance_is_preserved(self):
        view = self.bundle.candidates[0].view
        provenance = view["time_provenance"]
        self.assertEqual(1, len(provenance))
        seed = self.natal.temporal_seeds[0]
        self.assertEqual(
            json_value(seed.local_apparent_solar_datetime),
            provenance[0]["local_apparent_solar_datetime"],
        )
        self.assertEqual(json_value(seed.birth_utc), provenance[0]["birth_utc"])

    def test_bundle_and_json_export_are_deterministic(self):
        second = self.service.resolve(self.request)
        exported = self.service.export(self.request)
        self.assertEqual(self.bundle.bundle_hash, second.bundle_hash)
        self.assertEqual(self.bundle.view_hash, second.view_hash)
        self.assertEqual(self.bundle.bundle_hash, exported["bundle_hash"])
        self.assertEqual("PASS", exported["integrity"]["status"])

    def test_application_view_tamper_fails_without_mutating_source_fact_hashes(self):
        candidate = self.bundle.candidates[0]
        changed_view = copy.deepcopy(candidate.view)
        changed_view["day_master_stem"] = "TAMPERED"
        changed_candidate = replace(candidate, view=changed_view)
        changed_bundle = replace(self.bundle, candidates=(changed_candidate,))
        report = validate_application_resolution(changed_bundle)
        self.assertEqual("FAIL", report.status)
        self.assertIn("CANDIDATE_VIEW_HASH_MISMATCH:0", report.diagnostics)
        self.assertEqual(self.natal.hashes.fact_hash, candidate.natal_fact_hash)
        self.assertEqual(self.temporal.hashes.fact_hash, candidate.temporal_fact_hash)

    def test_tampered_natal_and_temporal_hash_lineage_fail_closed(self):
        bad_natal = replace(
            self.natal,
            hashes=replace(self.natal.hashes, fact_hash="TAMPERED-NATAL-FACT"),
        )
        with self.assertRaises(BaziApplicationResolutionError) as natal_error:
            self.service._validate_natal_candidate(bad_natal, self.natal_profile)
        self.assertEqual("BAZI_APP_NATAL_HASH_REPLAY_MISMATCH", natal_error.exception.code)

        bad_temporal = replace(
            self.temporal,
            hashes=replace(self.temporal.hashes, fact_hash="TAMPERED-TEMPORAL-FACT"),
        )
        with self.assertRaises(BaziApplicationResolutionError) as temporal_error:
            self.service._validate_temporal_candidate(
                bad_temporal,
                self.natal,
                self.temporal_profile,
            )
        self.assertEqual(
            "BAZI_APP_TEMPORAL_HASH_REPLAY_MISMATCH",
            temporal_error.exception.code,
        )

    def test_time_uncertainty_is_not_silently_collapsed(self):
        uncertain_birth = replace(self.birth, uncertainty_seconds=7200)
        result = self.service.resolve(replace(self.request, birth=uncertain_birth))
        self.assertNotEqual("RESOLVED", result.status)
        self.assertTrue(result.events)
        self.assertTrue(
            len(result.candidates) > 1
            or result.status == "RESOLVED_WITH_TIME_UNCERTAINTY"
        )

    def test_male_and_female_direction_sensitive_fixture(self):
        female = self.service.resolve(replace(self.request, sex=BaziSex.FEMALE))
        male_direction = self.bundle.candidates[0].view["dayun"]["direction"]
        female_direction = female.candidates[0].view["dayun"]["direction"]
        self.assertNotEqual(male_direction, female_direction)
        self.assertEqual({male_direction, female_direction}, {"FORWARD", "REVERSE"})

    def test_local_request_validation_and_explicit_profiles(self):
        app = LocalBaziApplication(ROOT)
        payload = {
            "birth_datetime": "1984-02-10T10:30",
            "birth_place": "Beijing",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone_id": "Asia/Shanghai",
            "sex": "MALE",
            "precision": "EXACT_SECOND",
            "uncertainty_seconds": 0,
            "natal_profile_id": "BAZI-FOUNDATION-V1-R1",
            "temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
            "application_profile_id": "BAZI-LOCAL-APPLICATION-V1-R1",
            "dayun_count": 12,
        }
        response = app.resolve_payload(payload)
        self.assertEqual("BAZI-LOCAL-APP-RESOLVE-V1", response["schema"])
        self.assertEqual(self.bundle.bundle_hash, response["application_bundle"]["bundle_hash"])

        for key, value in (
            ("timezone_id", "Mars/Olympus"),
            ("sex", "UNKNOWN"),
            ("natal_profile_id", "IMPLICIT-DEFAULT"),
            ("temporal_profile_id", "IMPLICIT-DEFAULT"),
            ("application_profile_id", "IMPLICIT-DEFAULT"),
        ):
            with self.subTest(key=key):
                changed = dict(payload)
                changed[key] = value
                with self.assertRaises(LocalAppRequestError):
                    app.resolve_payload(changed)


if __name__ == "__main__":
    unittest.main()
