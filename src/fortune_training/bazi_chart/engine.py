from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from fortune_training.calendar_foundation import BirthInput, TimeCalendarFoundation
from fortune_training.util import object_sha256

from .hidden_stems import (
    AFFINITY_ALGORITHM_ID,
    AFFINITY_ALGORITHM_VERSION,
    HIDDEN_STEM_ALGORITHM_ID,
    HIDDEN_STEM_ALGORITHM_VERSION,
    generate_affinities,
    generate_exposures,
    generate_hidden_stems,
)
from .integrity import natal_hash_bundle, validate_natal_state
from .models import (
    BaziNatalState,
    BaziTemporalSeed,
    BranchInstance,
    GenerationTrace,
    HashBundle,
    IntegrityReport,
    PillarState,
    StemInstance,
    TenGodBinding,
)
from .profile import NATAL_ALGORITHM_ID, NATAL_ALGORITHM_VERSION, ResolvedBaziCalculationProfile
from .registries import (
    BRANCH_ELEMENTS,
    PILLAR_POSITIONS,
    STEM_ELEMENTS,
    STEM_POLARITY,
    TEN_GOD_RULE_SET_ID,
    TEN_GOD_RULE_SET_VERSION,
    sexagenary_index,
)
from .relations import RAW_RELATION_ALGORITHM_ID, RAW_RELATION_ALGORITHM_VERSION, generate_raw_relations
from .ten_gods import TEN_GOD_ALGORITHM_ID, TEN_GOD_ALGORITHM_VERSION, ten_god


@dataclass(frozen=True)
class BaziChartRequest:
    birth: BirthInput
    profile: ResolvedBaziCalculationProfile


@dataclass(frozen=True)
class BaziChartCandidate:
    branch_indices: tuple[int, ...]
    chart: BaziNatalState
    temporal_seeds: tuple[BaziTemporalSeed, ...]
    integrity: IntegrityReport
    hashes: HashBundle


@dataclass(frozen=True)
class BaziTypedResolution:
    schema: str
    status: str
    calculation_profile: ResolvedBaziCalculationProfile
    time_calendar: dict[str, Any]
    candidates: tuple[BaziChartCandidate, ...]
    integrity_reports: tuple[IntegrityReport, ...]
    events: tuple[str, ...]
    diagnostics: tuple[str, ...]


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class BaziChartFoundation:
    schema = "BAZI-CHART-FOUNDATION-RESULT-V1"
    typed_schema = "BAZI-CHART-TYPED-RESOLUTION-V1"

    def __init__(self, time_calendar: TimeCalendarFoundation) -> None:
        self.time_calendar = time_calendar

    @classmethod
    def from_repository(cls, repository_root: Path) -> "BaziChartFoundation":
        return cls(TimeCalendarFoundation.from_repository(repository_root))

    @staticmethod
    def _generate_chart(
        branch: dict[str, Any],
        profile: ResolvedBaziCalculationProfile,
    ) -> BaziNatalState:
        bazi = branch["bazi_time"]
        pillar_values = {
            "YEAR": bazi["year_pillar"],
            "MONTH": bazi["month_pillar"],
            "DAY": bazi["day_pillar"],
            "HOUR": bazi["hour_pillar"],
        }

        pillars: list[PillarState] = []
        stems: list[StemInstance] = []
        branches: list[BranchInstance] = []
        for position in PILLAR_POSITIONS:
            ganzhi = pillar_values[position]
            index = sexagenary_index(ganzhi)
            stem, branch_char = ganzhi[0], ganzhi[1]
            stem_id = f"{position}.STEM"
            branch_id = f"{position}.BRANCH"
            pillars.append(
                PillarState(
                    position=position,
                    ganzhi=ganzhi,
                    sexagenary_index=index,
                    stem_instance_id=stem_id,
                    branch_instance_id=branch_id,
                )
            )
            stems.append(
                StemInstance(
                    instance_id=stem_id,
                    position=position,
                    stem=stem,
                    element=STEM_ELEMENTS[stem],
                    polarity=STEM_POLARITY[stem],
                )
            )
            branches.append(
                BranchInstance(
                    instance_id=branch_id,
                    position=position,
                    branch=branch_char,
                    element_affiliation=BRANCH_ELEMENTS[branch_char],
                )
            )

        stem_rows = tuple(stems)
        branch_rows = tuple(branches)
        hidden = generate_hidden_stems(branch_rows)
        day_master = next(row.stem for row in stem_rows if row.position == "DAY")

        ten_gods: list[TenGodBinding] = []
        targets = tuple((row.instance_id, row.stem) for row in stem_rows) + tuple(
            (row.instance_id, row.stem) for row in hidden
        )
        for target_id, target_stem in targets:
            semantic_id, display = ten_god(day_master, target_stem)
            ten_gods.append(
                TenGodBinding(
                    binding_id=f"TEN_GOD:{target_id}",
                    target_instance_id=target_id,
                    target_stem=target_stem,
                    day_master_stem=day_master,
                    semantic_role_id=semantic_id,
                    display_name=display,
                    rule_set_id=TEN_GOD_RULE_SET_ID,
                    rule_set_version=TEN_GOD_RULE_SET_VERSION,
                    source_refs=("S11",),
                )
            )

        exposures = generate_exposures(stem_rows, hidden)
        affinities = generate_affinities(stem_rows, branch_rows, hidden)
        relations = generate_raw_relations(stem_rows, branch_rows)
        trace = (
            GenerationTrace(
                operation="bind_time_calendar_four_pillars",
                algorithm_id=bazi.get("algorithm_id", "BAZI-TIME-RESOLVER-V1"),
                algorithm_version="PHASE-01-R1",
                source_refs=("TIME-CALENDAR-FOUNDATION-R1",),
            ),
            GenerationTrace(
                operation="bind_sexagenary_identity",
                algorithm_id=NATAL_ALGORITHM_ID,
                algorithm_version=NATAL_ALGORITHM_VERSION,
                source_refs=("S11",),
            ),
            GenerationTrace(
                operation="generate_hidden_stem_membership",
                algorithm_id=HIDDEN_STEM_ALGORITHM_ID,
                algorithm_version=HIDDEN_STEM_ALGORITHM_VERSION,
                source_refs=("S11",),
            ),
            GenerationTrace(
                operation="generate_ten_god_bindings",
                algorithm_id=TEN_GOD_ALGORITHM_ID,
                algorithm_version=TEN_GOD_ALGORITHM_VERSION,
                source_refs=("S11",),
            ),
            GenerationTrace(
                operation="generate_stem_branch_affinity",
                algorithm_id=AFFINITY_ALGORITHM_ID,
                algorithm_version=AFFINITY_ALGORITHM_VERSION,
                source_refs=("S11",),
            ),
            GenerationTrace(
                operation="generate_raw_relation_hypergraph",
                algorithm_id=RAW_RELATION_ALGORITHM_ID,
                algorithm_version=RAW_RELATION_ALGORITHM_VERSION,
                source_refs=("S14",),
            ),
        )
        return BaziNatalState(
            pillars=tuple(pillars),
            stems=stem_rows,
            branches=branch_rows,
            hidden_stems=hidden,
            ten_gods=tuple(ten_gods),
            exposures=exposures,
            affinities=affinities,
            raw_relations=relations,
            day_master_stem=day_master,
            profile_id=profile.profile_id,
            profile_version=profile.profile_version,
            algorithm_versions={
                "natal": NATAL_ALGORITHM_VERSION,
                "hidden_stems": HIDDEN_STEM_ALGORITHM_VERSION,
                "ten_gods": TEN_GOD_ALGORITHM_VERSION,
                "affinity": AFFINITY_ALGORITHM_VERSION,
                "raw_relations": RAW_RELATION_ALGORITHM_VERSION,
            },
            trace=trace,
        )

    @staticmethod
    def _temporal_seed(
        branch_index: int,
        branch: dict[str, Any],
        time_result: dict[str, Any],
    ) -> BaziTemporalSeed:
        selected_civil = branch["selected_civil_candidate"]
        solar = branch["solar_time"]
        jie = branch["jie_boundaries"]
        previous = jie["previous_jie"]
        following = jie["next_jie"]
        seed_payload = {
            "branch_index": branch_index,
            "sample_reported_local_datetime": branch["sample_reported_local_datetime"],
            "birth_utc": selected_civil["utc_instant"],
            "local_apparent_solar_datetime": solar["local_apparent_solar_datetime"],
            "previous_jie": previous["utc_instant"],
            "next_jie": following["utc_instant"],
            "policy_registry_version": time_result["policy_registry_version"],
        }
        return BaziTemporalSeed(
            seed_id=f"BAZI-TEMPORAL-SEED:{object_sha256(seed_payload)}",
            source_time_branch_index=branch_index,
            sample_reported_local_datetime=_parse_datetime(branch["sample_reported_local_datetime"]),
            birth_utc=_parse_datetime(selected_civil["utc_instant"]),
            local_apparent_solar_datetime=_parse_datetime(solar["local_apparent_solar_datetime"]),
            previous_jie_name=previous["name"],
            previous_jie_utc=_parse_datetime(previous["utc_instant"]),
            next_jie_name=following["name"],
            next_jie_utc=_parse_datetime(following["utc_instant"]),
            input_uncertainty_seconds_each_side=int(
                time_result["input_interval"]["uncertainty_seconds_each_side"]
            ),
            time_calendar_policy_registry_version=time_result["policy_registry_version"],
        )

    @classmethod
    def _failed_result(
        cls,
        profile: ResolvedBaziCalculationProfile,
        time_result: dict[str, Any],
        diagnostics: list[str],
        *,
        integrity_reports: tuple[IntegrityReport, ...] = (),
    ) -> BaziTypedResolution:
        return BaziTypedResolution(
            schema=cls.typed_schema,
            status="FAILED",
            calculation_profile=profile,
            time_calendar=time_result,
            candidates=(),
            integrity_reports=integrity_reports,
            events=(),
            diagnostics=tuple(diagnostics),
        )

    def resolve_typed(self, request: BaziChartRequest) -> BaziTypedResolution:
        profile = request.profile.validate(self.time_calendar.policy_registry)
        time_result = self.time_calendar.resolve_bazi(
            request.birth,
            profile.time_calendar_policies,
        )
        if not time_result["branches"]:
            return self._failed_result(profile, time_result, ["TIME_CALENDAR_UNRESOLVED"])

        unique: dict[str, dict[str, Any]] = {}
        integrity_reports: list[IntegrityReport] = []
        try:
            for branch_index, branch in enumerate(time_result["branches"]):
                chart = self._generate_chart(branch, profile)
                integrity = validate_natal_state(chart)
                integrity_reports.append(integrity)
                if integrity.status != "PASS":
                    return self._failed_result(
                        profile,
                        time_result,
                        [f"INTEGRITY:{row.code}:{row.path}" for row in integrity.diagnostics],
                        integrity_reports=(integrity,),
                    )
                hashes = natal_hash_bundle(chart, profile)
                seed = self._temporal_seed(branch_index, branch, time_result)
                if hashes.fact_hash not in unique:
                    unique[hashes.fact_hash] = {
                        "chart": chart,
                        "integrity": integrity,
                        "hashes": hashes,
                        "branch_indices": [branch_index],
                        "seeds": [seed],
                    }
                else:
                    row = unique[hashes.fact_hash]
                    if row["hashes"].computation_hash != hashes.computation_hash:
                        return self._failed_result(
                            profile,
                            time_result,
                            ["INTEGRITY:SAME_NATAL_FACT_DIFFERENT_COMPUTATION_LINEAGE"],
                        )
                    row["branch_indices"].append(branch_index)
                    if seed.seed_id not in {item.seed_id for item in row["seeds"]}:
                        row["seeds"].append(seed)
        except ValueError as exc:
            return self._failed_result(profile, time_result, [f"BAZI_NATAL_GENERATION_FAILED:{exc}"])

        candidates = tuple(
            BaziChartCandidate(
                branch_indices=tuple(row["branch_indices"]),
                chart=row["chart"],
                temporal_seeds=tuple(row["seeds"]),
                integrity=row["integrity"],
                hashes=row["hashes"],
            )
            for row in unique.values()
        )

        if len(candidates) > 1:
            status = "MULTI_CANDIDATE"
            events = ("TIME_UNCERTAINTY_CHANGED_BAZI_NATAL",)
        elif time_result["status"] == "RESOLVED":
            status = "RESOLVED"
            events = ()
        else:
            status = "RESOLVED_SINGLE_NATAL_WITH_TIME_UNCERTAINTY"
            events = ("TIME_UNCERTAINTY_PRESERVED_AS_TEMPORAL_SEEDS",)

        return BaziTypedResolution(
            schema=self.typed_schema,
            status=status,
            calculation_profile=profile,
            time_calendar=time_result,
            candidates=candidates,
            integrity_reports=tuple(integrity_reports),
            events=events,
            diagnostics=(),
        )
