from __future__ import annotations

from typing import TYPE_CHECKING

from fortune_training.ziwei_chart.integrity import HashBundle, validate_natal_chart
from fortune_training.ziwei_chart.models import NatalChartState

from .integrity import (
    structural_hash_bundle,
    validate_structural_components,
    validate_structural_state,
)
from .models import StructuralIntegrityReport, StructuralState
from .profile import ResolvedZiweiStructuralProfile
from .topology import NeutralZ12Topology

if TYPE_CHECKING:
    from fortune_training.ziwei_chart.engine import ZiweiChartCandidate


class StructuralGenerationError(ValueError):
    def __init__(
        self,
        diagnostic_code: str,
        detail: str,
        *,
        report: StructuralIntegrityReport | None = None,
    ) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code
        self.report = report


class ZiweiStructuralRuntime:
    """Derived Structural Runtime V2-R1 over a validated frozen V1 natal state."""

    def __init__(self) -> None:
        self.topology = NeutralZ12Topology()

    @staticmethod
    def _raise_report(report: StructuralIntegrityReport) -> None:
        first = report.diagnostics[0]
        raise StructuralGenerationError(first.code, first.detail, report=report)

    def generate(
        self,
        natal_chart: NatalChartState,
        natal_hashes: HashBundle,
        profile: ResolvedZiweiStructuralProfile,
    ) -> StructuralState:
        try:
            profile.validate()
        except ValueError as exc:
            raise StructuralGenerationError("INVALID_STRUCTURAL_PROFILE", str(exc)) from exc

        if (
            natal_chart.profile_id != profile.natal_profile_id
            or natal_chart.profile_version != profile.natal_profile_version
        ):
            raise StructuralGenerationError(
                "UPSTREAM_NATAL_PROFILE_MISMATCH",
                (
                    "natal chart profile does not match the structural profile binding: "
                    f"chart={natal_chart.profile_id}@{natal_chart.profile_version} "
                    f"structural={profile.natal_profile_id}@{profile.natal_profile_version}"
                ),
            )

        natal_integrity = validate_natal_chart(natal_chart)
        if natal_integrity.status != "PASS":
            first = natal_integrity.diagnostics[0]
            raise StructuralGenerationError(
                "UPSTREAM_NATAL_INTEGRITY_FAILED",
                f"{first.code}:{first.path}:{first.detail}",
            )

        facts = self.topology.generate()
        report = validate_structural_components(
            natal_hashes.fact_hash,
            natal_hashes.computation_hash,
            profile,
            facts,
        )
        if report.status != "PASS":
            self._raise_report(report)

        hashes = structural_hash_bundle(
            natal_hashes.fact_hash,
            natal_hashes.computation_hash,
            profile,
            facts,
        )
        state = StructuralState(
            upstream_natal_fact_hash=natal_hashes.fact_hash,
            upstream_natal_computation_hash=natal_hashes.computation_hash,
            profile=profile,
            topology_facts=facts,
            integrity=report,
            hashes=hashes,
        )
        final_report = validate_structural_state(state)
        if final_report.status != "PASS":
            self._raise_report(final_report)
        return state

    def generate_from_candidate(
        self,
        candidate: "ZiweiChartCandidate",
        profile: ResolvedZiweiStructuralProfile,
    ) -> StructuralState:
        if candidate.integrity.status != "PASS":
            raise StructuralGenerationError(
                "UPSTREAM_NATAL_INTEGRITY_FAILED",
                "ZiweiChartCandidate must carry a PASS natal integrity report",
            )
        return self.generate(candidate.chart, candidate.hashes, profile)
