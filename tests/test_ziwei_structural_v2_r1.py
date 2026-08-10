from __future__ import annotations

import json
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator

import fortune_training.ziwei_chart as ziwei_chart
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.calendar_foundation.models import json_value
from fortune_training.ziwei_chart import (
    Sex,
    ZiweiChartFoundation,
    ZiweiChartRequest,
    ziwei_chart_engine_v1_profile,
)
from fortune_training.ziwei_structural import (
    NeutralZ12Topology,
    ZiweiStructuralRuntime,
    canonical_addresses,
    clockwise_offset,
    shift,
    structural_fact_projection,
    structural_hash_bundle,
    validate_structural_state,
    ziwei_structural_v2_r1_profile,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiStructuralV2R1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
        cls.natal_profile = ziwei_chart_engine_v1_profile(registry)
        cls.structural_profile = ziwei_structural_v2_r1_profile()
        cls.natal_runtime = ZiweiChartFoundation(TimeCalendarFoundation(registry))
        cls.structural_runtime = ZiweiStructuralRuntime()
        request = ZiweiChartRequest(
            birth=BirthInput(
                reported_local_datetime=datetime(1994, 5, 17, 14, 30),
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            sex=Sex.MALE,
            profile=cls.natal_profile,
        )
        typed = cls.natal_runtime.resolve_typed(request)
        if typed.status != "RESOLVED" or len(typed.candidates) != 1:
            raise AssertionError(f"unexpected V1 typed resolution: {typed.status}")
        cls.candidate = typed.candidates[0]
        cls.state = cls.structural_runtime.generate_from_candidate(
            cls.candidate,
            cls.structural_profile,
        )

    @staticmethod
    def _schema() -> dict:
        return json.loads(
            (ROOT / "schemas" / "ziwei-structural-state-v2-r1.schema.json").read_text(
                encoding="utf-8"
            )
        )

    def test_v1_release_contract_remains_frozen(self) -> None:
        self.assertEqual("1.0.0", ziwei_chart.__version__)
        self.assertEqual("ZIWEI-CHART-ENGINE-V1", self.natal_profile.profile_id)
        self.assertEqual("1.0.0", self.natal_profile.profile_version)
        self.assertEqual("ZIWEI-CHART-ENGINE-V1", self.structural_profile.natal_profile_id)
        self.assertEqual("1.0.0", self.structural_profile.natal_profile_version)

    def test_neutral_z12_topology_is_complete_and_exhaustive(self) -> None:
        addresses = canonical_addresses()
        self.assertEqual(12, len(addresses))
        self.assertEqual(set(range(12)), {row.index for row in addresses})

        facts = NeutralZ12Topology().generate()
        self.assertEqual(144, len(facts))
        self.assertEqual(144, len({(row.source.index, row.target.index) for row in facts}))
        self.assertEqual(
            [(source, target) for source in range(12) for target in range(12)],
            [(row.source.index, row.target.index) for row in facts],
        )

        by_pair = {(row.source.index, row.target.index): row for row in facts}
        for source in addresses:
            source_rows = [row for row in facts if row.source == source]
            self.assertEqual(set(range(12)), {row.target.index for row in source_rows})
            self.assertEqual(source, shift(source, 12))
            self.assertEqual(source, shift(shift(source, 6), 6))
            for target in addresses:
                fact = by_pair[(source.index, target.index)]
                expected_offset = (target.index - source.index) % 12
                self.assertEqual(expected_offset, fact.clockwise_offset)
                self.assertEqual(expected_offset, clockwise_offset(source, target))
                self.assertEqual(target, shift(source, expected_offset))
            for offset in range(12):
                self.assertEqual(source, shift(shift(source, offset), -offset))

    def test_canonical_serialization_is_input_order_independent(self) -> None:
        facts = self.state.topology_facts
        forward = structural_fact_projection(self.candidate.hashes.fact_hash, facts)
        reverse = structural_fact_projection(self.candidate.hashes.fact_hash, tuple(reversed(facts)))
        self.assertEqual(forward, reverse)

        forward_hashes = structural_hash_bundle(
            self.candidate.hashes.fact_hash,
            self.candidate.hashes.computation_hash,
            self.structural_profile,
            facts,
        )
        reverse_hashes = structural_hash_bundle(
            self.candidate.hashes.fact_hash,
            self.candidate.hashes.computation_hash,
            self.structural_profile,
            tuple(reversed(facts)),
        )
        self.assertEqual(forward_hashes, reverse_hashes)

    def test_birth_input_to_natal_to_structural_typed_handoff_and_schema(self) -> None:
        state = self.state
        self.assertEqual("ZIWEI-STRUCTURAL-STATE-V2-R1", state.schema)
        self.assertEqual("ZIWEI-STRUCTURAL-RUNTIME-V2-R1", state.profile.profile_id)
        self.assertEqual("1.0.0", state.profile.profile_version)
        self.assertEqual(144, len(state.topology_facts))
        self.assertEqual("PASS", state.integrity.status)
        self.assertFalse(state.integrity.diagnostics)
        self.assertEqual(self.candidate.hashes.fact_hash, state.upstream_natal_fact_hash)
        self.assertEqual(
            self.candidate.hashes.computation_hash,
            state.upstream_natal_computation_hash,
        )
        self.assertRegex(state.hashes.fact_hash, r"^[0-9a-f]{64}$")
        self.assertRegex(state.hashes.computation_hash, r"^[0-9a-f]{64}$")
        self.assertEqual("PASS", validate_structural_state(state).status)

        schema = self._schema()
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        errors = sorted(
            validator.iter_errors(json_value(state)),
            key=lambda row: list(row.absolute_path),
        )
        if errors:
            rendered = "\n".join(
                f"{'.'.join(str(part) for part in row.absolute_path) or '<root>'}: {row.message}"
                for row in errors
            )
            self.fail(f"structural schema validation failed:\n{rendered}")

    def test_structural_generation_is_deterministic(self) -> None:
        replay = self.structural_runtime.generate(
            self.candidate.chart,
            self.candidate.hashes,
            self.structural_profile,
        )
        self.assertEqual(self.state.topology_facts, replay.topology_facts)
        self.assertEqual(self.state.hashes, replay.hashes)
        self.assertEqual(self.state.integrity, replay.integrity)

    def test_hash_layers_bind_upstream_fact_computation_and_profile_lineage(self) -> None:
        facts = self.state.topology_facts
        changed_fact = structural_hash_bundle(
            "0" * 64,
            self.candidate.hashes.computation_hash,
            self.structural_profile,
            facts,
        )
        self.assertNotEqual(self.state.hashes.fact_hash, changed_fact.fact_hash)
        self.assertNotEqual(self.state.hashes.computation_hash, changed_fact.computation_hash)

        changed_computation = structural_hash_bundle(
            self.candidate.hashes.fact_hash,
            "f" * 64,
            self.structural_profile,
            facts,
        )
        self.assertEqual(self.state.hashes.fact_hash, changed_computation.fact_hash)
        self.assertNotEqual(
            self.state.hashes.computation_hash,
            changed_computation.computation_hash,
        )

        unsupported_profile = replace(self.structural_profile, profile_version="1.0.1")
        changed_profile = structural_hash_bundle(
            self.candidate.hashes.fact_hash,
            self.candidate.hashes.computation_hash,
            unsupported_profile,
            facts,
        )
        self.assertEqual(self.state.hashes.fact_hash, changed_profile.fact_hash)
        self.assertNotEqual(self.state.hashes.computation_hash, changed_profile.computation_hash)
        with self.assertRaises(ValueError):
            unsupported_profile.validate()

        unsupported_topology = replace(
            self.structural_profile,
            topology_algorithm_version="1.0.1",
        )
        changed_topology = structural_hash_bundle(
            self.candidate.hashes.fact_hash,
            self.candidate.hashes.computation_hash,
            unsupported_topology,
            facts,
        )
        self.assertEqual(self.state.hashes.fact_hash, changed_topology.fact_hash)
        self.assertNotEqual(self.state.hashes.computation_hash, changed_topology.computation_hash)
        with self.assertRaises(ValueError):
            unsupported_topology.validate()

    def test_named_structural_semantics_remain_fail_closed_in_r1(self) -> None:
        named = replace(
            self.structural_profile,
            semantic_rule_set_id="UNFROZEN-TRADITIONAL-SEMANTICS",
            semantic_rule_set_version="0.0.0",
        )
        with self.assertRaises(ValueError):
            named.validate()

    def test_tampered_topology_fails_integrity_and_hash_validation(self) -> None:
        first = self.state.topology_facts[0]
        tampered_first = replace(first, clockwise_offset=1)
        tampered = replace(
            self.state,
            topology_facts=(tampered_first,) + self.state.topology_facts[1:],
        )
        report = validate_structural_state(tampered)
        self.assertEqual("FAIL", report.status)
        codes = {row.code for row in report.diagnostics}
        self.assertIn("TOPOLOGY_OFFSET_MISMATCH", codes)
        self.assertIn("STRUCTURAL_FACT_HASH_MISMATCH", codes)
        self.assertIn("STRUCTURAL_COMPUTATION_HASH_MISMATCH", codes)


if __name__ == "__main__":
    unittest.main()
