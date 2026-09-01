from __future__ import annotations

from dataclasses import dataclass

from fortune_training.util import object_sha256
from fortune_training.ziwei_chart.transformations import (
    S08_TRANSFORMATION_RULE_SET_ID,
    S08_TRANSFORMATION_RULE_SET_VERSION,
    TRANSFORMATION_ALGORITHM_ID,
    TRANSFORMATION_ALGORITHM_VERSION,
    TransformationGenerationError,
    TransformationGenerator,
)

from .models import ApplicationChartBundle
from .service import ApplicationResolutionError, validate_application_bundle


PALACE_STEM_TOPOLOGY_SCHEMA = "ZIWEI-PALACE-STEM-TRANSFORMATION-TOPOLOGY-SIDECAR-R1"
PALACE_STEM_TOPOLOGY_PROFILE_ID = "ZIWEI-PALACE-STEM-TRANSFORMATION-TOPOLOGY-R1"
PALACE_STEM_TOPOLOGY_PROFILE_VERSION = "1.0.0"
PALACE_STEM_TOPOLOGY_ALGORITHM_ID = "ZIWEI-PALACE-STEM-TRANSFORMATION-TOPOLOGY-COMPOSER-R1"
PALACE_STEM_TOPOLOGY_ALGORITHM_VERSION = "1.0.0"
PALACE_STEM_TOPOLOGY_INTEGRITY_ID = "ZIWEI-PALACE-STEM-TRANSFORMATION-TOPOLOGY-INTEGRITY-R1"
PALACE_STEM_TOPOLOGY_INTEGRITY_VERSION = "1.0.0"

PALACE_STEM_TOPOLOGY_CLASSIFICATION_POLICY = "GEOMETRIC_SAME_OPPOSITE_OTHER_ONLY"
PALACE_STEM_TOPOLOGY_SEMANTIC_SCOPE = (
    "PALACE_STEM_TARGET_TOPOLOGY_ONLY_NO_SELF_TRANSFORMATION_DIRECTION_OR_INTERPRETATION"
)
PALACE_STEM_TOPOLOGY_SELECTION_SEMANTICS = (
    "NO_SELF_OR_INWARD_DIRECTION_CLASSIFICATION_NO_WINNER"
)
PALACE_STEM_TOPOLOGY_SOURCE_LAYER = "PALACE_STEM"
TOPOLOGY_RELATIONS = ("SAME_PALACE", "OPPOSITE_PALACE", "OTHER_PALACE")
TRANSFORMATION_TYPES = ("化禄", "化权", "化科", "化忌")


class ZiweiPalaceStemTopologyResolutionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code
        self.detail = detail


@dataclass(frozen=True)
class ZiweiPalaceStemTopologyIntegrityReport:
    status: str
    diagnostics: tuple[str, ...]
    algorithm_id: str = PALACE_STEM_TOPOLOGY_INTEGRITY_ID
    algorithm_version: str = PALACE_STEM_TOPOLOGY_INTEGRITY_VERSION


@dataclass(frozen=True)
class ZiweiPalaceStemTopologyRow:
    row_id: str
    source_address_index: int
    source_branch: str
    source_stem: str
    source_layer: str
    context_id: str
    transformation_type: str
    target_entity_id: str
    target_display_name: str
    target_address_index: int
    target_branch: str
    topology_relation: str
    assignment_id: str
    mechanism_id: str
    source_refs: tuple[str, ...]
    fact_hash: str
    computation_hash: str


@dataclass(frozen=True)
class ZiweiPalaceStemTopologyResolution:
    schema: str
    status: str
    source_application_bundle_hash: str
    source_natal_fact_hash: str
    source_natal_computation_hash: str
    source_transformation_rule_set_id: str
    source_transformation_rule_set_version: str
    profile_id: str
    profile_version: str
    classification_policy: str
    selection_semantics: str
    semantic_scope: str
    rows: tuple[ZiweiPalaceStemTopologyRow, ...]
    fact_hash: str
    computation_hash: str
    bundle_hash: str
    integrity: ZiweiPalaceStemTopologyIntegrityReport


def palace_stem_topology_relation(source_index: int, target_index: int) -> str:
    if source_index not in range(12) or target_index not in range(12):
        raise ValueError("palace address index must be in [0, 11]")
    if source_index == target_index:
        return "SAME_PALACE"
    if target_index == (source_index + 6) % 12:
        return "OPPOSITE_PALACE"
    return "OTHER_PALACE"


def _row_fact_payload(
    *,
    source_address_index: int,
    source_branch: str,
    source_stem: str,
    context_id: str,
    transformation_type: str,
    target_entity_id: str,
    target_display_name: str,
    target_address_index: int,
    target_branch: str,
    topology_relation: str,
    assignment_id: str,
    mechanism_id: str,
    source_refs: tuple[str, ...],
) -> dict[str, object]:
    return {
        "source_address_index": source_address_index,
        "source_branch": source_branch,
        "source_stem": source_stem,
        "source_layer": PALACE_STEM_TOPOLOGY_SOURCE_LAYER,
        "context_id": context_id,
        "transformation_type": transformation_type,
        "target_entity_id": target_entity_id,
        "target_display_name": target_display_name,
        "target_address_index": target_address_index,
        "target_branch": target_branch,
        "topology_relation": topology_relation,
        "assignment_id": assignment_id,
        "mechanism_id": mechanism_id,
        "source_refs": list(source_refs),
    }


def _compose_row(source_attribute, activation) -> ZiweiPalaceStemTopologyRow:
    relation = palace_stem_topology_relation(
        source_attribute.address.index,
        activation.target_address.index,
    )
    fact_payload = _row_fact_payload(
        source_address_index=source_attribute.address.index,
        source_branch=source_attribute.address.branch,
        source_stem=source_attribute.stem,
        context_id=activation.context_id,
        transformation_type=activation.transformation_type,
        target_entity_id=activation.target_entity_id,
        target_display_name=activation.target_display_name,
        target_address_index=activation.target_address.index,
        target_branch=activation.target_address.branch,
        topology_relation=relation,
        assignment_id=activation.assignment_id,
        mechanism_id=activation.mechanism_id,
        source_refs=activation.source_refs,
    )
    fact_hash = object_sha256(fact_payload)
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "transformation_generator": (
                f"{TRANSFORMATION_ALGORITHM_ID}@{TRANSFORMATION_ALGORITHM_VERSION}"
            ),
            "topology_composer": (
                f"{PALACE_STEM_TOPOLOGY_ALGORITHM_ID}@"
                f"{PALACE_STEM_TOPOLOGY_ALGORITHM_VERSION}"
            ),
        }
    )
    row_id = f"ZIWEI-PALACE-STEM-TOPOLOGY:{object_sha256({'fact_hash': fact_hash})}"
    return ZiweiPalaceStemTopologyRow(
        row_id=row_id,
        source_address_index=source_attribute.address.index,
        source_branch=source_attribute.address.branch,
        source_stem=source_attribute.stem,
        source_layer=PALACE_STEM_TOPOLOGY_SOURCE_LAYER,
        context_id=activation.context_id,
        transformation_type=activation.transformation_type,
        target_entity_id=activation.target_entity_id,
        target_display_name=activation.target_display_name,
        target_address_index=activation.target_address.index,
        target_branch=activation.target_address.branch,
        topology_relation=relation,
        assignment_id=activation.assignment_id,
        mechanism_id=activation.mechanism_id,
        source_refs=tuple(activation.source_refs),
        fact_hash=fact_hash,
        computation_hash=computation_hash,
    )


def _aggregate_resolution_hashes(
    *,
    schema: str,
    status: str,
    source_application_bundle_hash: str,
    source_natal_fact_hash: str,
    source_natal_computation_hash: str,
    source_transformation_rule_set_id: str,
    source_transformation_rule_set_version: str,
    profile_id: str,
    profile_version: str,
    classification_policy: str,
    selection_semantics: str,
    semantic_scope: str,
    row_fact_hashes: tuple[str, ...],
    row_computation_hashes: tuple[str, ...],
    row_ids: tuple[str, ...],
) -> tuple[str, str, str]:
    fact_hash = object_sha256(
        {
            "schema": schema,
            "source_natal_fact_hash": source_natal_fact_hash,
            "source_transformation_rule_set_id": source_transformation_rule_set_id,
            "source_transformation_rule_set_version": source_transformation_rule_set_version,
            "profile_id": profile_id,
            "profile_version": profile_version,
            "classification_policy": classification_policy,
            "selection_semantics": selection_semantics,
            "semantic_scope": semantic_scope,
            "row_fact_hashes": list(row_fact_hashes),
        }
    )
    computation_hash = object_sha256(
        {
            "fact_hash": fact_hash,
            "source_application_bundle_hash": source_application_bundle_hash,
            "source_natal_computation_hash": source_natal_computation_hash,
            "row_computation_hashes": list(row_computation_hashes),
            "algorithm": (
                f"{PALACE_STEM_TOPOLOGY_ALGORITHM_ID}@"
                f"{PALACE_STEM_TOPOLOGY_ALGORITHM_VERSION}"
            ),
        }
    )
    bundle_hash = object_sha256(
        {
            "schema": schema,
            "status": status,
            "profile_id": profile_id,
            "profile_version": profile_version,
            "fact_hash": fact_hash,
            "computation_hash": computation_hash,
            "row_ids": list(row_ids),
        }
    )
    return fact_hash, computation_hash, bundle_hash


def _resolution_hashes(
    base_application: ApplicationChartBundle,
    rows: tuple[ZiweiPalaceStemTopologyRow, ...],
) -> tuple[str, str, str]:
    return _aggregate_resolution_hashes(
        schema=PALACE_STEM_TOPOLOGY_SCHEMA,
        status="COMPLETE",
        source_application_bundle_hash=base_application.bundle_hash,
        source_natal_fact_hash=base_application.candidate.hashes.fact_hash,
        source_natal_computation_hash=(
            base_application.candidate.hashes.computation_hash
        ),
        source_transformation_rule_set_id=S08_TRANSFORMATION_RULE_SET_ID,
        source_transformation_rule_set_version=S08_TRANSFORMATION_RULE_SET_VERSION,
        profile_id=PALACE_STEM_TOPOLOGY_PROFILE_ID,
        profile_version=PALACE_STEM_TOPOLOGY_PROFILE_VERSION,
        classification_policy=PALACE_STEM_TOPOLOGY_CLASSIFICATION_POLICY,
        selection_semantics=PALACE_STEM_TOPOLOGY_SELECTION_SEMANTICS,
        semantic_scope=PALACE_STEM_TOPOLOGY_SEMANTIC_SCOPE,
        row_fact_hashes=tuple(row.fact_hash for row in rows),
        row_computation_hashes=tuple(row.computation_hash for row in rows),
        row_ids=tuple(row.row_id for row in rows),
    )


def validate_palace_stem_topology(
    resolution: ZiweiPalaceStemTopologyResolution,
) -> ZiweiPalaceStemTopologyIntegrityReport:
    diagnostics: list[str] = []
    if resolution.schema != PALACE_STEM_TOPOLOGY_SCHEMA:
        diagnostics.append("SCHEMA_MISMATCH")
    if resolution.status != "COMPLETE":
        diagnostics.append("STATUS_NOT_COMPLETE")
    if (
        resolution.profile_id != PALACE_STEM_TOPOLOGY_PROFILE_ID
        or resolution.profile_version != PALACE_STEM_TOPOLOGY_PROFILE_VERSION
    ):
        diagnostics.append("PROFILE_MISMATCH")
    if resolution.classification_policy != PALACE_STEM_TOPOLOGY_CLASSIFICATION_POLICY:
        diagnostics.append("CLASSIFICATION_POLICY_MISMATCH")
    if resolution.selection_semantics != PALACE_STEM_TOPOLOGY_SELECTION_SEMANTICS:
        diagnostics.append("SELECTION_SEMANTICS_MISMATCH")
    if resolution.semantic_scope != PALACE_STEM_TOPOLOGY_SEMANTIC_SCOPE:
        diagnostics.append("SEMANTIC_SCOPE_MISMATCH")
    if resolution.source_transformation_rule_set_id != S08_TRANSFORMATION_RULE_SET_ID:
        diagnostics.append("TRANSFORMATION_RULE_SET_MISMATCH")
    if resolution.source_transformation_rule_set_version != S08_TRANSFORMATION_RULE_SET_VERSION:
        diagnostics.append("TRANSFORMATION_RULE_SET_VERSION_MISMATCH")
    if len(resolution.rows) != 48:
        diagnostics.append("ROW_COUNT_NOT_48")

    ids: set[str] = set()
    by_source: dict[int, list[ZiweiPalaceStemTopologyRow]] = {}
    expected_row_fact_hashes: list[str] = []
    expected_row_computation_hashes: list[str] = []
    expected_row_ids: list[str] = []
    for row in resolution.rows:
        if row.row_id in ids:
            diagnostics.append(f"DUPLICATE_ROW_ID:{row.row_id}")
        ids.add(row.row_id)
        by_source.setdefault(row.source_address_index, []).append(row)
        if row.source_address_index not in range(12) or row.target_address_index not in range(12):
            diagnostics.append(f"ADDRESS_OUT_OF_RANGE:{row.row_id}")
            continue
        if row.source_layer != PALACE_STEM_TOPOLOGY_SOURCE_LAYER:
            diagnostics.append(f"SOURCE_LAYER_MISMATCH:{row.row_id}")
        if row.topology_relation not in TOPOLOGY_RELATIONS:
            diagnostics.append(f"TOPOLOGY_RELATION_INVALID:{row.row_id}")
        elif row.topology_relation != palace_stem_topology_relation(
            row.source_address_index,
            row.target_address_index,
        ):
            diagnostics.append(f"TOPOLOGY_RELATION_MISMATCH:{row.row_id}")
        if not row.source_refs:
            diagnostics.append(f"SOURCE_REFS_EMPTY:{row.row_id}")
        expected_fact_hash = object_sha256(
            _row_fact_payload(
                source_address_index=row.source_address_index,
                source_branch=row.source_branch,
                source_stem=row.source_stem,
                context_id=row.context_id,
                transformation_type=row.transformation_type,
                target_entity_id=row.target_entity_id,
                target_display_name=row.target_display_name,
                target_address_index=row.target_address_index,
                target_branch=row.target_branch,
                topology_relation=row.topology_relation,
                assignment_id=row.assignment_id,
                mechanism_id=row.mechanism_id,
                source_refs=row.source_refs,
            )
        )
        expected_row_fact_hashes.append(expected_fact_hash)
        if row.fact_hash != expected_fact_hash:
            diagnostics.append(f"ROW_FACT_HASH_MISMATCH:{row.row_id}")
        expected_computation_hash = object_sha256(
            {
                "fact_hash": expected_fact_hash,
                "transformation_generator": (
                    f"{TRANSFORMATION_ALGORITHM_ID}@{TRANSFORMATION_ALGORITHM_VERSION}"
                ),
                "topology_composer": (
                    f"{PALACE_STEM_TOPOLOGY_ALGORITHM_ID}@"
                    f"{PALACE_STEM_TOPOLOGY_ALGORITHM_VERSION}"
                ),
            }
        )
        expected_row_computation_hashes.append(expected_computation_hash)
        if row.computation_hash != expected_computation_hash:
            diagnostics.append(f"ROW_COMPUTATION_HASH_MISMATCH:{row.row_id}")
        expected_row_id = (
            f"ZIWEI-PALACE-STEM-TOPOLOGY:"
            f"{object_sha256({'fact_hash': expected_fact_hash})}"
        )
        expected_row_ids.append(expected_row_id)
        if row.row_id != expected_row_id:
            diagnostics.append(f"ROW_ID_MISMATCH:{row.row_id}")

    if set(by_source) != set(range(12)):
        diagnostics.append("SOURCE_ADDRESS_DOMAIN_INCOMPLETE")
    for source_index, rows in by_source.items():
        if len(rows) != 4:
            diagnostics.append(f"SOURCE_ROW_COUNT_NOT_4:{source_index}")
            continue
        if {row.transformation_type for row in rows} != set(TRANSFORMATION_TYPES):
            diagnostics.append(f"SOURCE_TRANSFORMATION_TYPES_INCOMPLETE:{source_index}")
        if len({row.source_stem for row in rows}) != 1:
            diagnostics.append(f"SOURCE_STEM_NOT_STABLE:{source_index}")
        if len({row.source_branch for row in rows}) != 1:
            diagnostics.append(f"SOURCE_BRANCH_NOT_STABLE:{source_index}")
        if len({row.context_id for row in rows}) != 1:
            diagnostics.append(f"SOURCE_CONTEXT_NOT_STABLE:{source_index}")

    expected_fact_hash, expected_computation_hash, expected_bundle_hash = (
        _aggregate_resolution_hashes(
            schema=resolution.schema,
            status=resolution.status,
            source_application_bundle_hash=resolution.source_application_bundle_hash,
            source_natal_fact_hash=resolution.source_natal_fact_hash,
            source_natal_computation_hash=resolution.source_natal_computation_hash,
            source_transformation_rule_set_id=(
                resolution.source_transformation_rule_set_id
            ),
            source_transformation_rule_set_version=(
                resolution.source_transformation_rule_set_version
            ),
            profile_id=resolution.profile_id,
            profile_version=resolution.profile_version,
            classification_policy=resolution.classification_policy,
            selection_semantics=resolution.selection_semantics,
            semantic_scope=resolution.semantic_scope,
            row_fact_hashes=tuple(expected_row_fact_hashes),
            row_computation_hashes=tuple(expected_row_computation_hashes),
            row_ids=tuple(expected_row_ids),
        )
    )
    if resolution.fact_hash != expected_fact_hash:
        diagnostics.append("FACT_HASH_MISMATCH")
    if resolution.computation_hash != expected_computation_hash:
        diagnostics.append("COMPUTATION_HASH_MISMATCH")
    if resolution.bundle_hash != expected_bundle_hash:
        diagnostics.append("BUNDLE_HASH_MISMATCH")

    return ZiweiPalaceStemTopologyIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
    )


class ZiweiPalaceStemTransformationTopologyService:
    schema = PALACE_STEM_TOPOLOGY_SCHEMA

    def __init__(self) -> None:
        self.transformations = TransformationGenerator()

    def _resolve_once(
        self,
        base_application: ApplicationChartBundle,
    ) -> ZiweiPalaceStemTopologyResolution:
        try:
            validate_application_bundle(base_application)
        except ApplicationResolutionError as exc:
            raise ZiweiPalaceStemTopologyResolutionError(
                "ZIWEI_PALACE_STEM_TOPOLOGY_SOURCE_APPLICATION_INVALID",
                str(exc),
            ) from exc

        profile = base_application.calculation_profile
        if profile.transformation_rule_set_id != S08_TRANSFORMATION_RULE_SET_ID:
            raise ZiweiPalaceStemTopologyResolutionError(
                "ZIWEI_PALACE_STEM_TOPOLOGY_RULE_SET_UNSUPPORTED",
                str(profile.transformation_rule_set_id),
            )

        attributes = tuple(
            sorted(
                base_application.candidate.chart.structure.address_attributes,
                key=lambda row: row.address.index,
            )
        )
        if len(attributes) != 12:
            raise ZiweiPalaceStemTopologyResolutionError(
                "ZIWEI_PALACE_STEM_TOPOLOGY_SOURCE_ADDRESS_COUNT_INVALID",
                f"expected 12 address attributes, found {len(attributes)}",
            )
        if {row.address.index for row in attributes} != set(range(12)):
            raise ZiweiPalaceStemTopologyResolutionError(
                "ZIWEI_PALACE_STEM_TOPOLOGY_SOURCE_ADDRESS_DOMAIN_INVALID",
                "address indices must cover [0, 11] exactly once",
            )
        if len({row.address.branch for row in attributes}) != 12:
            raise ZiweiPalaceStemTopologyResolutionError(
                "ZIWEI_PALACE_STEM_TOPOLOGY_SOURCE_BRANCH_DOMAIN_INVALID",
                "palace branches must be one-to-one across the 12 addresses",
            )

        composed: list[ZiweiPalaceStemTopologyRow] = []
        for attribute in attributes:
            context_id = (
                f"PALACE_STEM:{attribute.address.index}:{attribute.address.branch}"
            )
            try:
                activations = self.transformations.activate(
                    attribute.stem,
                    base_application.candidate.chart.placements,
                    source_layer=PALACE_STEM_TOPOLOGY_SOURCE_LAYER,
                    context_id=context_id,
                )
            except (TransformationGenerationError, ValueError) as exc:
                raise ZiweiPalaceStemTopologyResolutionError(
                    "ZIWEI_PALACE_STEM_TOPOLOGY_TRANSFORMATION_GENERATION_FAILED",
                    str(exc),
                ) from exc
            if len(activations) != 4:
                raise ZiweiPalaceStemTopologyResolutionError(
                    "ZIWEI_PALACE_STEM_TOPOLOGY_TRANSFORMATION_COUNT_INVALID",
                    f"{context_id} produced {len(activations)} rows",
                )
            composed.extend(_compose_row(attribute, activation) for activation in activations)

        rows = tuple(
            sorted(
                composed,
                key=lambda row: (
                    row.source_address_index,
                    TRANSFORMATION_TYPES.index(row.transformation_type),
                ),
            )
        )
        fact_hash, computation_hash, bundle_hash = _resolution_hashes(
            base_application,
            rows,
        )
        provisional = ZiweiPalaceStemTopologyResolution(
            schema=PALACE_STEM_TOPOLOGY_SCHEMA,
            status="COMPLETE",
            source_application_bundle_hash=base_application.bundle_hash,
            source_natal_fact_hash=base_application.candidate.hashes.fact_hash,
            source_natal_computation_hash=(
                base_application.candidate.hashes.computation_hash
            ),
            source_transformation_rule_set_id=S08_TRANSFORMATION_RULE_SET_ID,
            source_transformation_rule_set_version=S08_TRANSFORMATION_RULE_SET_VERSION,
            profile_id=PALACE_STEM_TOPOLOGY_PROFILE_ID,
            profile_version=PALACE_STEM_TOPOLOGY_PROFILE_VERSION,
            classification_policy=PALACE_STEM_TOPOLOGY_CLASSIFICATION_POLICY,
            selection_semantics=PALACE_STEM_TOPOLOGY_SELECTION_SEMANTICS,
            semantic_scope=PALACE_STEM_TOPOLOGY_SEMANTIC_SCOPE,
            rows=rows,
            fact_hash=fact_hash,
            computation_hash=computation_hash,
            bundle_hash=bundle_hash,
            integrity=ZiweiPalaceStemTopologyIntegrityReport(
                status="PENDING",
                diagnostics=(),
            ),
        )
        integrity = validate_palace_stem_topology(provisional)
        if integrity.status != "PASS":
            raise ZiweiPalaceStemTopologyResolutionError(
                "ZIWEI_PALACE_STEM_TOPOLOGY_INTEGRITY_FAILED",
                ";".join(integrity.diagnostics),
            )
        return ZiweiPalaceStemTopologyResolution(
            **{
                **provisional.__dict__,
                "integrity": integrity,
            }
        )

    def resolve(
        self,
        base_application: ApplicationChartBundle,
    ) -> ZiweiPalaceStemTopologyResolution:
        first = self._resolve_once(base_application)
        replay = self._resolve_once(base_application)
        if replay != first:
            raise ZiweiPalaceStemTopologyResolutionError(
                "ZIWEI_PALACE_STEM_TOPOLOGY_FULL_REPLAY_FAILED",
                "identical application bundle produced a different topology sidecar",
            )
        return first
