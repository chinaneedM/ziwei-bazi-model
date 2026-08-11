from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .bazi_classical_relation_interaction_assertion import (
    MATRIX_PATH,
    MANDATORY_SOURCE_OCCURRENCE_IDS,
    validate_classical_relation_interaction_assertion_matrix,
)
from .util import (
    TrainingError,
    atomic_write_bytes,
    atomic_write_json,
    load_json,
    object_sha256,
    sha256_file,
)


AUDIT_ID = "BAZI-STRUCTURED-SOURCE-INTERACTION-PATTERN-GRAPH-R1"
GRAPH_PROFILE_ID = AUDIT_ID
GRAPH_PROFILE_VERSION = "1.0.0"
AUDIT_ROOT = Path("audits/bazi-structured-source-interaction-pattern-graph-r1")
GRAPH_PATH = AUDIT_ROOT / "graph.json"
REPORT_PATH = AUDIT_ROOT / "coverage-report.md"
SCHEMA_PATH = Path("schemas/bazi-structured-source-interaction-pattern-graph-r1.schema.json")

EXPECTED_MATRIX_FILE_SHA256 = "50da1ae51b8838ba29520cf114ccb963f34a1ef8b8011a6593be25a48a95eacd"
EXPECTED_MATRIX_ARTIFACT_SEMANTICS_SHA256 = "6d9f4cdc4b44b1b6a78f892690ededea9be1e40f436638d8f5f54b6d3e9cb906"
EXPECTED_MATRIX_RECORD_HASH_CHAIN_SHA256 = "f32c55a88e8699268ba04fadc0e6f07e26ef79caafe9c75a51f87fd1460d4672"

UPSTREAM_CONTRACT_HASHES = {
    "schemas/bazi-classical-relation-interaction-assertion-matrix-r1.schema.json": "b79c9037b323bcccc03304e7634d707c3ec55b8f60b14192a53e476111dac9e4",
    "schemas/bazi-branch-relation-positional-context-foundation-r1.schema.json": "6aaf67e07b58da15eabf266842345f7433b0166bd1d441f2bd94f254f9923220",
    "schemas/bazi-stem-relation-positional-context-foundation-r1.schema.json": "4ee1b9d4a5e287acaf05b790ed01c3344eef6c1deeab4d0ad41358180264c3a5",
    "schemas/bazi-relation-incidence-foundation-r1.schema.json": "89af6132dcaafae4d337ce913e12c7a8e031c402ebfdc1206e40f11607cca8c6",
    "schemas/bazi-relation-transition-foundation-r1.schema.json": "6578d5aa918cfe832c90211e3cc3e63bfc12d044caebd5b1b640366dbe74b747",
    "src/fortune_training/bazi_chart/relations.py": "304b1a726c3c29a2bc67b3be62341ec02e45b56883149a853538250e64e9761f",
}

GRAPH_STATUSES = (
    "CONCRETE_SOURCE_PATTERN_GRAPH",
    "ABSTRACT_SOURCE_PATTERN_GRAPH",
    "CONTEXTUAL_UNRESOLVED_GRAPH",
    "PARTICIPANT_MEDIATED_SOURCE_GRAPH",
)
PARTICIPANT_KINDS = (
    "BRANCH_LITERAL_PATTERN",
    "STEM_LITERAL_PATTERN",
    "DAY_MASTER_STEM_PATTERN",
    "SOURCE_CONTEXT_PARTICIPANT_PATTERN",
    "UNRESOLVED_PARTICIPANT_PATTERN",
)
POSITION_EVIDENCE_MODES = (
    "DIRECT_SOURCE_TEXT",
    "SOURCE_CONTEXT_INHERITED",
    "SOURCE_POSITION_CONTEXT_UNRESOLVED",
)
POSITION_STATUSES = (
    "EXACT_SYMBOLIC_PARTICIPANT_PILLAR_CONSTRAINT",
    "SOURCE_PILLAR_CONTEXT_ONLY",
    "UNRESOLVED_SOURCE_TIME_CONTEXT",
)
RELATION_RESOLUTION_STATUSES = (
    "EXACT_RELEASED_RELATION_PATTERN",
    "SOURCE_RELATION_FAMILY_PATTERN_ONLY",
    "SOURCE_LEXEME_RELATION_TARGET_ONLY",
    "UNRESOLVED_RELATION_PATTERN",
)
RELEASED_RELATION_FAMILIES = (
    "STEM_COMBINATION",
    "BRANCH_SIX_HARMONY",
    "BRANCH_CLASH",
    "BRANCH_CHUAN",
    "BRANCH_PUNISHMENT",
    "BRANCH_TRINE",
)
CLAIM_EDGE_CLASSES = (
    "SOURCE_ASSERTED_RESOLUTION",
    "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE",
    "SOURCE_ASSERTED_RESOLUTION_FAILURE",
    "SOURCE_ASSERTED_ATTENUATION",
    "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION",
    "SOURCE_ASSERTED_PARTICIPANT_MEDIATED_RELEASE",
)
CLAIM_EVIDENCE_MODES = (
    "DIRECT_SOURCE_TEXT",
    "DIRECT_CLAIM_WITH_INHERITED_CONTEXT",
)
ASSERTION_TO_EDGE_CLASS = {
    "RESOLUTION_ASSERTION": "SOURCE_ASSERTED_RESOLUTION",
    "REVERSAL_OR_REAPPEARANCE_ASSERTION": "SOURCE_ASSERTED_REVERSAL_OR_REAPPEARANCE",
    "RESOLUTION_FAILURE_ASSERTION": "SOURCE_ASSERTED_RESOLUTION_FAILURE",
    "ATTENUATION_ASSERTION": "SOURCE_ASSERTED_ATTENUATION",
    "PARTICIPANT_ALLOCATION_ASSERTION": "SOURCE_ASSERTED_PARTICIPANT_ALLOCATION",
    "PARTICIPANT_MEDIATED_RELEASE_ASSERTION": "SOURCE_ASSERTED_PARTICIPANT_MEDIATED_RELEASE",
}

BRANCH_SEMANTICS = {
    ("BRANCH_SIX_HARMONY", frozenset(("子", "丑"))): "BRANCH.HARMONY.SIX.ZI_CHOU",
    ("BRANCH_SIX_HARMONY", frozenset(("卯", "戌"))): "BRANCH.HARMONY.SIX.MAO_XU",
    ("BRANCH_SIX_HARMONY", frozenset(("辰", "酉"))): "BRANCH.HARMONY.SIX.CHEN_YOU",
    ("BRANCH_CLASH", frozenset(("子", "午"))): "BRANCH.CLASH.ZI_WU",
    ("BRANCH_CLASH", frozenset(("卯", "酉"))): "BRANCH.CLASH.MAO_YOU",
    ("BRANCH_PUNISHMENT", frozenset(("子", "卯"))): "BRANCH.PUNISHMENT.ZI_MAO",
    ("BRANCH_TRINE", frozenset(("申", "子", "辰"))): "BRANCH.TRINE.WATER",
    ("BRANCH_TRINE", frozenset(("亥", "卯", "未"))): "BRANCH.TRINE.WOOD",
    ("BRANCH_TRINE", frozenset(("寅", "午", "戌"))): "BRANCH.TRINE.FIRE",
    ("BRANCH_TRINE", frozenset(("巳", "酉", "丑"))): "BRANCH.TRINE.METAL",
}

INHERITANCE_REGISTRY = {
    "ZPZQ-CL-09-003-003": "ZPZQ-CL-09-003-002",
    "ZPZQ-CL-09-003-004": "ZPZQ-CL-09-003-002",
    "ZPZQ-CL-09-003-005": "ZPZQ-CL-09-003-002",
    "ZPZQ-CL-09-003-008": "ZPZQ-CL-09-003-007",
    "ZPZQ-CL-09-003-009": "ZPZQ-CL-09-003-007",
    "ZPZQ-CL-09-003-010": "ZPZQ-CL-09-003-007",
}


def _p(
    key: str,
    lexeme: str,
    kind: str,
    role: str = "SOURCE_NAMED_PARTICIPANT",
    *,
    evidence: str = "DIRECT_SOURCE_TEXT",
    group: str | None = None,
    slot: int | None = None,
) -> dict[str, Any]:
    return {
        "key": key,
        "source_lexeme": lexeme,
        "participant_kind": kind,
        "literal_value": lexeme if kind != "UNRESOLVED_PARTICIPANT_PATTERN" else None,
        "source_role": role,
        "source_evidence_mode": evidence,
        "multiplicity_group_key": group,
        "symbolic_slot_index": slot,
    }


def _pos(
    key: str,
    participants: tuple[str, ...],
    pillar: str | None,
    fragment: str,
    evidence: str = "DIRECT_SOURCE_TEXT",
    status: str = "EXACT_SYMBOLIC_PARTICIPANT_PILLAR_CONSTRAINT",
    unresolved: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "key": key,
        "participant_keys": participants,
        "natal_pillar": pillar,
        "source_fragment": fragment,
        "evidence_mode": evidence,
        "constraint_status": status,
        "unresolved_requirements": unresolved,
    }


def _rel(
    key: str,
    fragment: str,
    participants: tuple[str, ...] = (),
    *,
    family: str | None = None,
    arity: int | None = None,
    orientation: str = "UNRESOLVED",
    status: str = "UNRESOLVED_RELATION_PATTERN",
    unresolved: str | None = None,
    evidence: str = "DIRECT_SOURCE_TEXT",
    paths: tuple[tuple[str, ...], ...] = (),
) -> dict[str, Any]:
    return {
        "key": key,
        "source_fragment": fragment,
        "participant_keys": participants,
        "compatible_paths": paths,
        "source_arity": arity,
        "source_orientation": orientation,
        "pattern_resolution_status": status,
        "released_neutral_relation_family": family,
        "unresolved_relation_marker": unresolved,
        "source_evidence_mode": evidence,
    }


def _claim(
    key: str,
    assertion_class: str,
    fragments: tuple[str, ...],
    *,
    actor_kind: str,
    actor_relations: tuple[str, ...] = (),
    actor_participants: tuple[str, ...] = (),
    context_participants: tuple[str, ...] = (),
    target_kind: str,
    target_relations: tuple[str, ...] = (),
    target_participants: tuple[str, ...] = (),
    unresolved: tuple[str, ...] = (),
    evidence: str = "DIRECT_SOURCE_TEXT",
) -> dict[str, Any]:
    return {
        "key": key,
        "source_assertion_class": assertion_class,
        "source_fragments": fragments,
        "actor_reference_kind": actor_kind,
        "actor_relation_keys": actor_relations,
        "actor_participant_keys": actor_participants,
        "context_participant_keys": context_participants,
        "target_reference_kind": target_kind,
        "target_relation_keys": target_relations,
        "target_participant_keys": target_participants,
        "unresolved_requirements": unresolved,
        "source_evidence_mode": evidence,
    }


def _exact_rel(
    key: str,
    fragment: str,
    participants: tuple[str, ...],
    family: str,
    *,
    evidence: str = "DIRECT_SOURCE_TEXT",
    paths: tuple[tuple[str, ...], ...] = (),
) -> dict[str, Any]:
    return _rel(
        key,
        fragment,
        participants,
        family=family,
        arity=3 if family == "BRANCH_TRINE" else 2,
        orientation="GROUP" if family == "BRANCH_TRINE" else "SYMMETRIC",
        status="EXACT_RELEASED_RELATION_PATTERN",
        evidence=evidence,
        paths=paths,
    )


def _abstract_spec(
    status: str,
    actor_fragment: str,
    target_fragment: str,
    assertion_class: str,
) -> dict[str, Any]:
    return {
        "status": status,
        "participants": (),
        "positions": (),
        "relations": (
            _rel("actor", actor_fragment, status="SOURCE_RELATION_FAMILY_PATTERN_ONLY", unresolved="GENERIC_SOURCE_RELATION_FAMILY"),
            _rel("target", target_fragment, status="SOURCE_LEXEME_RELATION_TARGET_ONLY", unresolved="GENERIC_SOURCE_RELATION_TARGET"),
        ),
        "claims": (
            _claim(
                "claim",
                assertion_class,
                (actor_fragment, target_fragment) if actor_fragment != target_fragment else (actor_fragment,),
                actor_kind="RELATION_PATTERN_ACTOR",
                actor_relations=("actor",),
                target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET",
                target_relations=("target",),
                unresolved=("SOURCE_PATTERN_TO_EXACT_INSTANCE_BINDING",),
            ),
        ),
    }


def _contextual_unresolved_spec(
    source_fragment: str,
    assertion_class: str,
) -> dict[str, Any]:
    return {
        "status": "CONTEXTUAL_UNRESOLVED_GRAPH",
        "participants": (),
        "positions": (),
        "relations": (),
        "claims": (
            _claim(
                "claim",
                assertion_class,
                (source_fragment,),
                actor_kind="UNRESOLVED_ACTOR",
                target_kind="UNRESOLVED_TARGET",
                unresolved=("CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS",),
            ),
        ),
    }


GRAPH_SPECS: dict[str, dict[str, Any]] = {
    "ZPZQ-CL-09-003-001": _abstract_spec("ABSTRACT_SOURCE_PATTERN_GRAPH", "三合六合", "刑冲", "RESOLUTION_ASSERTION"),
    "ZPZQ-CL-09-003-002": {
        "status": "CONCRETE_SOURCE_PATTERN_GRAPH",
        "participants": (
            _p("jia", "甲", "DAY_MASTER_STEM_PATTERN", "DAY_MASTER"),
            _p("you", "酉", "BRANCH_LITERAL_PATTERN"),
            _p("mao", "卯", "BRANCH_LITERAL_PATTERN"),
            _p("xu", "戌", "BRANCH_LITERAL_PATTERN"),
        ),
        "positions": (_pos("day_master", ("jia",), "DAY", "甲生"), _pos("month", ("you",), "MONTH", "酉月")),
        "relations": (
            _exact_rel("target", "卯则冲", ("mao", "you"), "BRANCH_CLASH"),
            _exact_rel("actor", "卯与戌合", ("mao", "xu"), "BRANCH_SIX_HARMONY"),
        ),
        "claims": (_claim("resolution", "RESOLUTION_ASSERTION", ("卯与戌合而不冲",), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target",), unresolved=("CLASSICAL_RESOLUTION_SEMANTICS",)),),
    },
    "ZPZQ-CL-09-003-003": {
        "status": "CONCRETE_SOURCE_PATTERN_GRAPH",
        "participants": (
            _p("chen", "辰", "BRANCH_LITERAL_PATTERN"),
            _p("you", "酉", "BRANCH_LITERAL_PATTERN"),
            _p("mao_inherited", "卯", "BRANCH_LITERAL_PATTERN", evidence="SOURCE_CONTEXT_INHERITED"),
        ),
        "positions": (_pos("month_inherited", ("you",), "MONTH", "酉月", "SOURCE_CONTEXT_INHERITED"),),
        "relations": (
            _exact_rel("actor", "酉与辰合", ("you", "chen"), "BRANCH_SIX_HARMONY"),
            _exact_rel("target_inherited", "卯酉冲 target context", ("mao_inherited", "you"), "BRANCH_CLASH", evidence="SOURCE_CONTEXT_INHERITED"),
        ),
        "claims": (_claim("resolution", "RESOLUTION_ASSERTION", ("酉与辰合而不冲",), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target_inherited",), unresolved=("CLASSICAL_RESOLUTION_SEMANTICS",), evidence="DIRECT_CLAIM_WITH_INHERITED_CONTEXT"),),
        "inheritance": {"antecedent": "ZPZQ-CL-09-003-002", "participant_keys": ("mao_inherited",), "relation_keys": ("target_inherited",), "position_keys": ("month_inherited",), "reason": "The clause continues the immediately preceding 卯酉 clash example and supplies a new harmony actor."},
    },
    "ZPZQ-CL-09-003-004": {
        "status": "CONCRETE_SOURCE_PATTERN_GRAPH",
        "participants": (_p("hai", "亥", "BRANCH_LITERAL_PATTERN"), _p("wei", "未", "BRANCH_LITERAL_PATTERN"), _p("mao", "卯", "BRANCH_LITERAL_PATTERN"), _p("you_inherited", "酉", "BRANCH_LITERAL_PATTERN", evidence="SOURCE_CONTEXT_INHERITED")),
        "positions": (_pos("month_inherited", ("you_inherited",), "MONTH", "酉月", "SOURCE_CONTEXT_INHERITED"),),
        "relations": (_exact_rel("actor", "卯与亥未会", ("mao", "hai", "wei"), "BRANCH_TRINE"), _exact_rel("target_inherited", "卯酉冲 target context", ("mao", "you_inherited"), "BRANCH_CLASH", evidence="SOURCE_CONTEXT_INHERITED")),
        "claims": (_claim("resolution", "RESOLUTION_ASSERTION", ("卯与亥未会而不冲",), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target_inherited",), unresolved=("CLASSICAL_RESOLUTION_SEMANTICS",), evidence="DIRECT_CLAIM_WITH_INHERITED_CONTEXT"),),
        "inheritance": {"antecedent": "ZPZQ-CL-09-003-002", "participant_keys": ("you_inherited",), "relation_keys": ("target_inherited",), "position_keys": ("month_inherited",), "reason": "The clause remains in the regression-locked 卯酉 clash example chain."},
    },
    "ZPZQ-CL-09-003-005": {
        "status": "CONCRETE_SOURCE_PATTERN_GRAPH",
        "participants": (_p("si", "巳", "BRANCH_LITERAL_PATTERN"), _p("chou", "丑", "BRANCH_LITERAL_PATTERN"), _p("you", "酉", "BRANCH_LITERAL_PATTERN"), _p("mao_inherited", "卯", "BRANCH_LITERAL_PATTERN", evidence="SOURCE_CONTEXT_INHERITED")),
        "positions": (_pos("month", ("you",), "MONTH", "酉月", "SOURCE_CONTEXT_INHERITED"),),
        "relations": (_exact_rel("actor", "酉与巳丑会", ("you", "si", "chou"), "BRANCH_TRINE"), _exact_rel("target_inherited", "卯酉冲 target context", ("mao_inherited", "you"), "BRANCH_CLASH", evidence="SOURCE_CONTEXT_INHERITED")),
        "claims": (_claim("resolution", "RESOLUTION_ASSERTION", ("酉与巳丑会而不冲",), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target_inherited",), unresolved=("CLASSICAL_RESOLUTION_SEMANTICS",), evidence="DIRECT_CLAIM_WITH_INHERITED_CONTEXT"),),
        "inheritance": {"antecedent": "ZPZQ-CL-09-003-002", "participant_keys": ("mao_inherited",), "relation_keys": ("target_inherited",), "position_keys": ("month",), "reason": "The clause remains in the regression-locked 卯酉 clash example chain."},
    },
    "ZPZQ-CL-09-003-006": _abstract_spec("ABSTRACT_SOURCE_PATTERN_GRAPH", "会合", "冲", "RESOLUTION_ASSERTION"),
    "ZPZQ-CL-09-003-007": {
        "status": "CONCRETE_SOURCE_PATTERN_GRAPH",
        "participants": (_p("bing", "丙", "DAY_MASTER_STEM_PATTERN", "DAY_MASTER"), _p("zi", "子", "BRANCH_LITERAL_PATTERN"), _p("mao", "卯", "BRANCH_LITERAL_PATTERN"), _p("xu", "戌", "BRANCH_LITERAL_PATTERN")),
        "positions": (_pos("day_master", ("bing",), "DAY", "丙生"), _pos("month", ("zi",), "MONTH", "子月")),
        "relations": (_exact_rel("target", "逢卯则刑", ("mao", "zi"), "BRANCH_PUNISHMENT"), _exact_rel("actor", "与戌合", ("mao", "xu"), "BRANCH_SIX_HARMONY")),
        "claims": (_claim("resolution", "RESOLUTION_ASSERTION", ("与戌合而不刑",), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target",), unresolved=("CLASSICAL_RESOLUTION_SEMANTICS",)),),
    },
    "ZPZQ-CL-09-003-008": {
        "status": "CONCRETE_SOURCE_PATTERN_GRAPH",
        "participants": (_p("chou", "丑", "BRANCH_LITERAL_PATTERN"), _p("zi", "子", "BRANCH_LITERAL_PATTERN"), _p("mao_inherited", "卯", "BRANCH_LITERAL_PATTERN", evidence="SOURCE_CONTEXT_INHERITED")),
        "positions": (_pos("month", ("zi",), "MONTH", "子月", "SOURCE_CONTEXT_INHERITED"),),
        "relations": (_exact_rel("actor", "子与丑合", ("zi", "chou"), "BRANCH_SIX_HARMONY"), _exact_rel("target_inherited", "子卯刑 target context", ("zi", "mao_inherited"), "BRANCH_PUNISHMENT", evidence="SOURCE_CONTEXT_INHERITED")),
        "claims": (_claim("resolution", "RESOLUTION_ASSERTION", ("子与丑合而不刑",), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target_inherited",), unresolved=("CLASSICAL_RESOLUTION_SEMANTICS",), evidence="DIRECT_CLAIM_WITH_INHERITED_CONTEXT"),),
        "inheritance": {"antecedent": "ZPZQ-CL-09-003-007", "participant_keys": ("mao_inherited",), "relation_keys": ("target_inherited",), "position_keys": ("month",), "reason": "The clause continues the immediately preceding 子卯 punishment example."},
    },
    "ZPZQ-CL-09-003-009": {
        "status": "CONCRETE_SOURCE_PATTERN_GRAPH",
        "participants": (_p("hai", "亥", "BRANCH_LITERAL_PATTERN"), _p("wei", "未", "BRANCH_LITERAL_PATTERN"), _p("mao", "卯", "BRANCH_LITERAL_PATTERN"), _p("zi_inherited", "子", "BRANCH_LITERAL_PATTERN", evidence="SOURCE_CONTEXT_INHERITED")),
        "positions": (_pos("month", ("zi_inherited",), "MONTH", "子月", "SOURCE_CONTEXT_INHERITED"),),
        "relations": (_exact_rel("actor", "卯与亥未会", ("mao", "hai", "wei"), "BRANCH_TRINE"), _exact_rel("target_inherited", "子卯刑 target context", ("mao", "zi_inherited"), "BRANCH_PUNISHMENT", evidence="SOURCE_CONTEXT_INHERITED")),
        "claims": (_claim("resolution", "RESOLUTION_ASSERTION", ("卯与亥未会而不刑",), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target_inherited",), unresolved=("CLASSICAL_RESOLUTION_SEMANTICS",), evidence="DIRECT_CLAIM_WITH_INHERITED_CONTEXT"),),
        "inheritance": {"antecedent": "ZPZQ-CL-09-003-007", "participant_keys": ("zi_inherited",), "relation_keys": ("target_inherited",), "position_keys": ("month",), "reason": "The clause remains in the regression-locked 子卯 punishment example chain."},
    },
    "ZPZQ-CL-09-003-010": {
        "status": "CONCRETE_SOURCE_PATTERN_GRAPH",
        "participants": (_p("shen", "申", "BRANCH_LITERAL_PATTERN"), _p("chen", "辰", "BRANCH_LITERAL_PATTERN"), _p("zi", "子", "BRANCH_LITERAL_PATTERN"), _p("mao_inherited", "卯", "BRANCH_LITERAL_PATTERN", evidence="SOURCE_CONTEXT_INHERITED")),
        "positions": (_pos("month", ("zi",), "MONTH", "子月", "SOURCE_CONTEXT_INHERITED"),),
        "relations": (_exact_rel("actor", "子与申辰会", ("zi", "shen", "chen"), "BRANCH_TRINE"), _exact_rel("target_inherited", "子卯刑 target context", ("zi", "mao_inherited"), "BRANCH_PUNISHMENT", evidence="SOURCE_CONTEXT_INHERITED")),
        "claims": (_claim("resolution", "RESOLUTION_ASSERTION", ("子与申辰会而不刑",), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target_inherited",), unresolved=("CLASSICAL_RESOLUTION_SEMANTICS",), evidence="DIRECT_CLAIM_WITH_INHERITED_CONTEXT"),),
        "inheritance": {"antecedent": "ZPZQ-CL-09-003-007", "participant_keys": ("mao_inherited",), "relation_keys": ("target_inherited",), "position_keys": ("month",), "reason": "The clause remains in the regression-locked 子卯 punishment example chain."},
    },
    "ZPZQ-CL-09-003-011": _abstract_spec("ABSTRACT_SOURCE_PATTERN_GRAPH", "会合", "刑", "RESOLUTION_ASSERTION"),
    "ZPZQ-CL-09-005-001": _contextual_unresolved_spec("因解而反得刑冲", "REVERSAL_OR_REAPPEARANCE_ASSERTION"),
    "ZPZQ-CL-09-007-001": _abstract_spec("CONTEXTUAL_UNRESOLVED_GRAPH", "会合", "刑冲", "RESOLUTION_FAILURE_ASSERTION"),
    "ZPZQ-CL-09-007-004": _abstract_spec("ABSTRACT_SOURCE_PATTERN_GRAPH", "会合", "刑冲", "RESOLUTION_FAILURE_ASSERTION"),
    "ZPZQ-CL-09-009-001": _abstract_spec("CONTEXTUAL_UNRESOLVED_GRAPH", "刑冲", "刑", "RESOLUTION_ASSERTION"),
    "ZPZQ-CL-09-009-005": _abstract_spec("ABSTRACT_SOURCE_PATTERN_GRAPH", "刑冲", "刑冲", "RESOLUTION_ASSERTION"),
}


def _install_complex_specs() -> None:
    GRAPH_SPECS["ZPZQ-CL-09-005-002"] = {
        "status": "CONCRETE_SOURCE_PATTERN_GRAPH",
        "participants": (
            _p("jia", "甲", "DAY_MASTER_STEM_PATTERN", "DAY_MASTER"), _p("zi", "子", "BRANCH_LITERAL_PATTERN"),
            _p("mao1", "卯", "BRANCH_LITERAL_PATTERN", group="mao_pair", slot=1), _p("mao2", "卯", "BRANCH_LITERAL_PATTERN", group="mao_pair", slot=2),
            _p("xu", "戌", "BRANCH_LITERAL_PATTERN"),
        ),
        "positions": (_pos("day_master", ("jia",), "DAY", "甲生"), _pos("month", ("zi",), "MONTH", "子月")),
        "relations": (
            _exact_rel("target", "二卯不刑一子", (), "BRANCH_PUNISHMENT", paths=(("mao1", "zi"), ("mao2", "zi"))),
            _exact_rel("actor", "戌与卯合", (), "BRANCH_SIX_HARMONY", paths=(("xu", "mao1"), ("xu", "mao2"))),
        ),
        "claims": (
            _claim("resolution", "RESOLUTION_ASSERTION", ("本为解刑",), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target",), unresolved=("CLASSICAL_RESOLUTION_SEMANTICS",)),
            _claim("allocation", "PARTICIPANT_ALLOCATION_ASSERTION", ("合去其一", "一合而一刑"), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target",), unresolved=("CLASSICAL_PARTICIPANT_ALLOCATION", "COMPATIBLE_EXACT_INSTANCE_PATH_ENUMERATION")),
            _claim("reappearance", "REVERSAL_OR_REAPPEARANCE_ASSERTION", ("因解而反得刑冲",), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target",), unresolved=("CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS",)),
        ),
        "multiplicity": {"key": "mao_pair", "lexeme": "二卯", "participant_keys": ("mao1", "mao2")},
        "chain": {"key": "narrative", "claim_keys": ("resolution", "allocation", "reappearance"), "fragments": ("本为解刑", "合去其一", "一合而一刑")},
    }

    for oid, values in {
        "ZPZQ-CL-09-007-002": ("子", "午", "丑", "巳", "酉", "YEAR", "MONTH", "DAY", "丑与子合", "丑与巳酉会", "子复冲午"),
        "ZPZQ-CL-09-007-003": ("子", "卯", "戌", "寅", "午", "YEAR", "MONTH", "DAY", "戌与卯合", "戌与寅午会", "卯复刑子"),
    }.items():
        first, second, third, fourth, fifth, _, _, _, harmony_fragment, trine_fragment, reappear_fragment = values
        target_family = "BRANCH_CLASH" if oid.endswith("002") else "BRANCH_PUNISHMENT"
        keys = ("first", "second", "third", "fourth", "fifth")
        GRAPH_SPECS[oid] = {
            "status": "CONCRETE_SOURCE_PATTERN_GRAPH",
            "participants": tuple(_p(key, lexeme, "BRANCH_LITERAL_PATTERN") for key, lexeme in zip(keys, values[:5])),
            "positions": (
                _pos("year", ("first",), "YEAR", f"{first}年"), _pos("month", ("second",), "MONTH", f"{second}月"), _pos("day", ("third",), "DAY", f"日坐{third}位"),
                _pos("hour_unresolved", ("fourth", "fifth"), None, f"时逢{fourth}{fifth}", "SOURCE_POSITION_CONTEXT_UNRESOLVED", "UNRESOLVED_SOURCE_TIME_CONTEXT", ("SOURCE_TIME_CONSTRUCTION_MECHANICAL_INTERPRETATION",)),
            ),
            "relations": (
                _exact_rel("target", reappear_fragment, ("first", "second"), target_family),
                _exact_rel("actor", harmony_fragment, ("third", "first" if oid.endswith("002") else "second"), "BRANCH_SIX_HARMONY"),
                _exact_rel("second_relation", trine_fragment, ("third", "fourth", "fifth"), "BRANCH_TRINE"),
            ),
            "claims": (
                _claim("resolution", "RESOLUTION_ASSERTION", ("可以解冲" if oid.endswith("002") else "可以解刑",), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target",), unresolved=("CLASSICAL_RESOLUTION_SEMANTICS",)),
                _claim("failure", "RESOLUTION_FAILURE_ASSERTION", (trine_fragment, reappear_fragment), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("second_relation",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target",), unresolved=("CLASSICAL_RESOLUTION_FAILURE_SEMANTICS", "CLASSICAL_INTERACTION_CHAIN_RESOLUTION")),
                _claim("reappearance", "REVERSAL_OR_REAPPEARANCE_ASSERTION", (reappear_fragment,), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("second_relation",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target",), unresolved=("CLASSICAL_REVERSAL_OR_REAPPEARANCE_SEMANTICS",)),
            ),
            "chain": {"key": "narrative", "claim_keys": ("resolution", "failure", "reappearance"), "fragments": (harmony_fragment, trine_fragment, reappear_fragment)},
        }

    GRAPH_SPECS["ZPZQ-CL-09-009-002"] = {
        **_abstract_spec("ABSTRACT_SOURCE_PATTERN_GRAPH", "另位之刑冲", "月令之刑冲", "RESOLUTION_ASSERTION"),
        "positions": (_pos("month_context", (), "MONTH", "月令", "DIRECT_SOURCE_TEXT", "SOURCE_PILLAR_CONTEXT_ONLY"),),
    }
    GRAPH_SPECS["ZPZQ-CL-09-009-003"] = {
        "status": "CONCRETE_SOURCE_PATTERN_GRAPH",
        "participants": (_p("bing", "丙", "DAY_MASTER_STEM_PATTERN", "DAY_MASTER"), _p("zi", "子", "BRANCH_LITERAL_PATTERN"), _p("mao", "卯", "BRANCH_LITERAL_PATTERN"), _p("you", "酉", "BRANCH_LITERAL_PATTERN")),
        "positions": (_pos("day_master", ("bing",), "DAY", "丙生"), _pos("month", ("zi",), "MONTH", "子月")),
        "relations": (_exact_rel("target", "卯以刑子", ("mao", "zi"), "BRANCH_PUNISHMENT"), _exact_rel("actor", "与酉冲", ("mao", "you"), "BRANCH_CLASH")),
        "claims": (_claim("resolution", "RESOLUTION_ASSERTION", ("与酉冲不刑月令之官",), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target",), unresolved=("CLASSICAL_RESOLUTION_SEMANTICS",)),),
    }
    GRAPH_SPECS["ZPZQ-CL-09-009-004"] = {
        "status": "CONCRETE_SOURCE_PATTERN_GRAPH",
        "participants": (_p("jia", "甲", "DAY_MASTER_STEM_PATTERN", "DAY_MASTER"), _p("you", "酉", "BRANCH_LITERAL_PATTERN"), _p("mao", "卯", "BRANCH_LITERAL_PATTERN"), _p("zi", "子", "BRANCH_LITERAL_PATTERN")),
        "positions": (_pos("day_master", ("jia",), "DAY", "甲生"), _pos("month", ("you",), "MONTH", "酉月"), _pos("day", ("mao",), "DAY", "卯日"), _pos("hour", ("zi",), "HOUR", "时逢子立")),
        "relations": (_exact_rel("target", "卯日冲之", ("mao", "you"), "BRANCH_CLASH"), _exact_rel("actor", "卯与子刑", ("mao", "zi"), "BRANCH_PUNISHMENT")),
        "claims": (_claim("attenuation", "ATTENUATION_ASSERTION", ("冲之无力", "月官犹在"), actor_kind="RELATION_PATTERN_ACTOR", actor_relations=("actor",), target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("target",), unresolved=("CLASSICAL_ATTENUATION_GRADE",)),),
    }

    for oid, layer_participants in {
        "QTBJ-CL-05347": (("hai", "亥", "BRANCH_LITERAL_PATTERN", "SOURCE_CONTEXT_CONDITION"), ("zi", "子", "BRANCH_LITERAL_PATTERN", "SOURCE_CONTEXT_CONDITION"), ("shen", "申", "BRANCH_LITERAL_PATTERN", "SOURCE_CONTEXT_CONDITION"), ("gui", "癸", "SOURCE_CONTEXT_PARTICIPANT_PATTERN", "PARTICIPANT_OR_CONTEXT_ACTOR"), ("bing", "丙", "STEM_LITERAL_PATTERN", "AFFECTED_SOURCE_PARTICIPANT")),
        "QTBJ-CL-05370": (("bing", "丙", "STEM_LITERAL_PATTERN", "AFFECTED_SOURCE_PARTICIPANT"), ("gui", "癸", "SOURCE_CONTEXT_PARTICIPANT_PATTERN", "PARTICIPANT_OR_CONTEXT_ACTOR"), ("hai", "亥", "BRANCH_LITERAL_PATTERN", "SOURCE_CONTEXT_CONDITION"), ("zi", "子", "BRANCH_LITERAL_PATTERN", "SOURCE_CONTEXT_CONDITION"), ("chou", "丑", "BRANCH_LITERAL_PATTERN", "SOURCE_CONTEXT_CONDITION"), ("jia", "甲", "STEM_LITERAL_PATTERN", "SOURCE_CONTEXT_CONDITION"), ("wu", "戊", "STEM_LITERAL_PATTERN", "SOURCE_CONTEXT_CONDITION")),
    }.items():
        participant_specs = tuple(_p(key, lexeme, kind, role) for key, lexeme, kind, role in layer_participants)
        context_keys = tuple(key for key, _, _, role in layer_participants if role == "SOURCE_CONTEXT_CONDITION")
        context_fragment = "癸水通源" if oid.endswith("05347") else "癸水有力"
        release_fragment = "破丙解合" if oid.endswith("05347") else "癸水破丙解合"
        GRAPH_SPECS[oid] = {
            "status": "PARTICIPANT_MEDIATED_SOURCE_GRAPH",
            "participants": participant_specs,
            "positions": (),
            "relations": (_rel("unresolved_target", "解合", status="UNRESOLVED_RELATION_PATTERN", unresolved="QTBJ_EXACT_JIEHE_TARGET_IDENTITY_UNRESOLVED"),),
            "claims": (_claim("mediated_release", "PARTICIPANT_MEDIATED_RELEASE_ASSERTION", (context_fragment, release_fragment), actor_kind="PARTICIPANT_OR_CONTEXT_ACTOR", actor_participants=("gui",), context_participants=context_keys, target_kind="SOURCE_NAMED_RELATION_OR_EFFECT_TARGET", target_relations=("unresolved_target",), target_participants=("bing",), unresolved=("CLASSICAL_PARTICIPANT_MEDIATED_RELEASE_SEMANTICS", "QTBJ_EXACT_JIEHE_TARGET_IDENTITY_UNRESOLVED", "QTBJ_SOURCE_CONTEXT_FORCE_OR_ROOT_SEMANTICS_UNRESOLVED")),),
        }


_install_complex_specs()


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _with_hash(value: dict[str, Any]) -> dict[str, Any]:
    value["semantic_sha256"] = object_sha256(value)
    return value


def _id(prefix: str, source_occurrence_id: str, index: int) -> str:
    return f"BSSIPG-R1-{prefix}-{source_occurrence_id}-{index:02d}"


def _provenance(matrix_record: dict[str, Any], evidence_mode: str) -> dict[str, Any]:
    return {
        "interaction_assertion_id": matrix_record["interaction_assertion_id"],
        "source_occurrence_id": matrix_record["source_occurrence_id"],
        "matrix_record_sha256": matrix_record["record_sha256"],
        "source_text_sha256": matrix_record["source_text_sha256"],
        "parent_source_block_id": matrix_record["parent_source_block_id"],
        "source_evidence_mode": evidence_mode,
    }


def _build_graph_bundle(matrix_record: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    oid = matrix_record["source_occurrence_id"]
    participant_ids = {row["key"]: _id("P", oid, index) for index, row in enumerate(spec.get("participants", ()), 1)}
    relation_ids = {row["key"]: _id("R", oid, index) for index, row in enumerate(spec.get("relations", ()), 1)}
    position_ids = {row["key"]: _id("POS", oid, index) for index, row in enumerate(spec.get("positions", ()), 1)}
    claim_ids = {row["key"]: _id("E", oid, index) for index, row in enumerate(spec.get("claims", ()), 1)}

    participants = []
    for row in spec.get("participants", ()):
        if row["source_evidence_mode"] == "DIRECT_SOURCE_TEXT" and row["source_lexeme"] not in matrix_record["exact_source_text"]:
            raise TrainingError(f"direct participant lexeme does not replay: {oid}:{row['source_lexeme']}")
        participants.append(_with_hash({
            "participant_pattern_node_id": participant_ids[row["key"]],
            "graph_record_id": f"BSSIPG-R1-G-{oid}",
            "source_occurrence_id": oid,
            "source_lexeme": row["source_lexeme"],
            "participant_kind": row["participant_kind"],
            "literal_value": row["literal_value"],
            "source_role": row["source_role"],
            "multiplicity_group_id": (f"BSSIPG-R1-M-{oid}-01" if row["multiplicity_group_key"] else None),
            "symbolic_slot_index": row["symbolic_slot_index"],
            "exchangeability_status": "EXCHANGEABLE_SOURCE_EQUIVALENT" if row["multiplicity_group_key"] else "NOT_APPLICABLE",
            "source_evidence_mode": row["source_evidence_mode"],
            "provenance": _provenance(matrix_record, row["source_evidence_mode"]),
        }))

    positions = []
    for row in spec.get("positions", ()):
        if row["evidence_mode"] != "SOURCE_CONTEXT_INHERITED" and row["source_fragment"] not in matrix_record["exact_source_text"]:
            raise TrainingError(f"direct position fragment does not replay: {oid}:{row['source_fragment']}")
        positions.append(_with_hash({
            "position_constraint_id": position_ids[row["key"]],
            "graph_record_id": f"BSSIPG-R1-G-{oid}",
            "source_occurrence_id": oid,
            "participant_pattern_node_ids": [participant_ids[key] for key in row["participant_keys"]],
            "natal_pillar": row["natal_pillar"],
            "source_fragment": row["source_fragment"],
            "evidence_mode": row["evidence_mode"],
            "constraint_status": row["constraint_status"],
            "unresolved_requirements": list(row["unresolved_requirements"]),
            "provenance": _provenance(matrix_record, row["evidence_mode"]),
        }))

    relations = []
    for row in spec.get("relations", ()):
        if row["source_evidence_mode"] == "DIRECT_SOURCE_TEXT" and row["source_fragment"] not in matrix_record["exact_source_text"]:
            raise TrainingError(f"direct relation fragment does not replay: {oid}:{row['source_fragment']}")
        direct_keys = row["participant_keys"]
        paths = row["compatible_paths"]
        literal_paths = [[next(item["literal_value"] for item in spec["participants"] if item["key"] == key) for key in path] for path in paths]
        literal_values = [next(item["literal_value"] for item in spec["participants"] if item["key"] == key) for key in direct_keys]
        lookup_values = literal_values or (literal_paths[0] if literal_paths else [])
        semantic_id = None
        if row["pattern_resolution_status"] == "EXACT_RELEASED_RELATION_PATTERN":
            semantic_id = BRANCH_SEMANTICS.get((row["released_neutral_relation_family"], frozenset(lookup_values)))
            if semantic_id is None:
                raise TrainingError(f"exact source relation is not in released registry: {oid}:{row['key']}")
            if any(frozenset(path) != frozenset(lookup_values) for path in literal_paths):
                raise TrainingError(f"compatible paths do not preserve the exact relation identity: {oid}:{row['key']}")
        relations.append(_with_hash({
            "relation_pattern_node_id": relation_ids[row["key"]],
            "graph_record_id": f"BSSIPG-R1-G-{oid}",
            "source_occurrence_id": oid,
            "source_fragment": row["source_fragment"],
            "symbolic_ordered_participant_node_ids": [participant_ids[key] for key in direct_keys],
            "compatible_symbolic_participant_paths": [[participant_ids[key] for key in path] for path in paths],
            "source_arity": row["source_arity"],
            "source_orientation": row["source_orientation"],
            "pattern_resolution_status": row["pattern_resolution_status"],
            "released_neutral_relation_family": row["released_neutral_relation_family"],
            "released_neutral_semantic_relation_id": semantic_id,
            "unresolved_relation_marker": row["unresolved_relation_marker"],
            "source_evidence_mode": row["source_evidence_mode"],
            "provenance": _provenance(matrix_record, row["source_evidence_mode"]),
        }))

    claims = []
    for row in spec.get("claims", ()):
        for fragment in row["source_fragments"]:
            if fragment not in matrix_record["exact_source_text"]:
                raise TrainingError(f"claim fragment does not replay: {oid}:{fragment}")
        claims.append(_with_hash({
            "interaction_claim_edge_id": claim_ids[row["key"]],
            "graph_record_id": f"BSSIPG-R1-G-{oid}",
            "source_occurrence_id": oid,
            "edge_class": ASSERTION_TO_EDGE_CLASS[row["source_assertion_class"]],
            "source_assertion_class": row["source_assertion_class"],
            "actor_reference_kind": row["actor_reference_kind"],
            "actor_relation_pattern_node_ids": [relation_ids[key] for key in row["actor_relation_keys"]],
            "actor_participant_pattern_node_ids": [participant_ids[key] for key in row["actor_participant_keys"]],
            "context_participant_pattern_node_ids": [participant_ids[key] for key in row["context_participant_keys"]],
            "target_reference_kind": row["target_reference_kind"],
            "target_relation_pattern_node_ids": [relation_ids[key] for key in row["target_relation_keys"]],
            "target_participant_pattern_node_ids": [participant_ids[key] for key in row["target_participant_keys"]],
            "exact_source_fragments": list(row["source_fragments"]),
            "source_evidence_mode": row["source_evidence_mode"],
            "unresolved_requirements": list(row["unresolved_requirements"]),
            "raw_relation_mutation_emitted": False,
            "provenance": _provenance(matrix_record, row["source_evidence_mode"]),
        }))

    inheritance_edges: list[dict[str, Any]] = []
    inheritance = spec.get("inheritance")
    if inheritance:
        antecedent = inheritance["antecedent"]
        inheritance_edges.append(_with_hash({
            "context_inheritance_edge_id": _id("CTX", oid, 1),
            "inheriting_graph_record_id": f"BSSIPG-R1-G-{oid}",
            "antecedent_graph_record_id": f"BSSIPG-R1-G-{antecedent}",
            "inheriting_source_occurrence_id": oid,
            "antecedent_source_occurrence_id": antecedent,
            "inherited_participant_pattern_node_ids": [participant_ids[key] for key in inheritance["participant_keys"]],
            "inherited_relation_pattern_node_ids": [relation_ids[key] for key in inheritance["relation_keys"]],
            "inherited_position_constraint_ids": [position_ids[key] for key in inheritance["position_keys"]],
            "inheritance_scope": "REGRESSION_LOCKED_SAME_SOURCE_BLOCK_EXAMPLE_CHAIN",
            "inheritance_status": "EXPLICIT_SOURCE_CONTEXT_INHERITANCE",
            "reason": inheritance["reason"],
            "direct_source_lexeme_claimed": False,
            "provenance": _provenance(matrix_record, "SOURCE_CONTEXT_INHERITED"),
        }))

    multiplicities: list[dict[str, Any]] = []
    multiplicity = spec.get("multiplicity")
    if multiplicity:
        multiplicities.append(_with_hash({
            "multiplicity_constraint_id": _id("M", oid, 1),
            "graph_record_id": f"BSSIPG-R1-G-{oid}",
            "source_occurrence_id": oid,
            "source_lexeme": multiplicity["lexeme"],
            "participant_literal_value": "卯",
            "required_symbolic_cardinality": 2,
            "exchangeable_symbolic_slot_node_ids": [participant_ids[key] for key in multiplicity["participant_keys"]],
            "slot_equivalence": "EXCHANGEABLE_SOURCE_EQUIVALENT",
            "exact_slot_selection": "NOT_SELECTED",
            "alternative_path_requirement": "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS",
            "winner_emitted": False,
            "provenance": _provenance(matrix_record, "DIRECT_SOURCE_TEXT"),
        }))

    chains: list[dict[str, Any]] = []
    chain = spec.get("chain")
    if chain:
        chains.append(_with_hash({
            "chain_pattern_id": _id("CHAIN", oid, 1),
            "graph_record_id": f"BSSIPG-R1-G-{oid}",
            "source_occurrence_id": oid,
            "ordered_interaction_claim_edge_ids": [claim_ids[key] for key in chain["claim_keys"]],
            "exact_source_sequence_fragments": list(chain["fragments"]),
            "sequence_semantics": "SOURCE_NARRATIVE_ORDER_ONLY",
            "runtime_state_transition_emitted": False,
            "suppression_or_activation_emitted": False,
            "provenance": _provenance(matrix_record, "DIRECT_SOURCE_TEXT"),
        }))

    unresolved = sorted(
        set(matrix_record["unresolved_semantic_requirements"])
        | {value for relation in relations for value in [relation["unresolved_relation_marker"]] if value}
        | {value for position in positions for value in position["unresolved_requirements"]}
        | {value for claim in claims for value in claim["unresolved_requirements"]}
    )
    base_record = {
        "graph_record_id": f"BSSIPG-R1-G-{oid}",
        "interaction_assertion_id": matrix_record["interaction_assertion_id"],
        "source_occurrence_id": oid,
        "matrix_record_sha256": matrix_record["record_sha256"],
        "source_text_sha256": matrix_record["source_text_sha256"],
        "source_record_sha256": matrix_record["source_record_sha256"],
        "parent_source_block_id": matrix_record["parent_source_block_id"],
        "parent_source_segment_id": matrix_record["parent_source_segment_id"],
        "source_chapter_id": matrix_record["source_chapter_id"],
        "source_layer": matrix_record["source_layer"],
        "source_assertion_role": matrix_record["source_assertion_role"],
        "primary_assertion_class": matrix_record["primary_assertion_class"],
        "secondary_assertion_classes": matrix_record["secondary_assertion_classes"],
        "exact_source_text": matrix_record["exact_source_text"],
        "exact_source_fragments": matrix_record["source_assertion_fragments"],
        "graph_status": spec["status"],
        "participant_pattern_node_ids": [row["participant_pattern_node_id"] for row in participants],
        "relation_pattern_node_ids": [row["relation_pattern_node_id"] for row in relations],
        "position_constraint_ids": [row["position_constraint_id"] for row in positions],
        "interaction_claim_edge_ids": [row["interaction_claim_edge_id"] for row in claims],
        "context_inheritance_edge_ids": [row["context_inheritance_edge_id"] for row in inheritance_edges],
        "chain_pattern_ids": [row["chain_pattern_id"] for row in chains],
        "multiplicity_constraint_ids": [row["multiplicity_constraint_id"] for row in multiplicities],
        "unresolved_graph_requirements": unresolved,
    }
    bundle_hashes = [row["semantic_sha256"] for rows in (participants, positions, relations, claims, inheritance_edges, chains, multiplicities) for row in rows]
    base_record["graph_bundle_semantics_sha256"] = object_sha256({"record": base_record, "object_semantic_hashes": bundle_hashes})
    base_record["graph_record_sha256"] = object_sha256(base_record)
    return {
        "graph_record": base_record,
        "participants": participants,
        "positions": positions,
        "relations": relations,
        "claims": claims,
        "inheritance": inheritance_edges,
        "chains": chains,
        "multiplicities": multiplicities,
    }


def _summary(artifact: dict[str, Any]) -> dict[str, Any]:
    def counts(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
        return dict(sorted(Counter(row[field] for row in rows).items()))
    unresolved_records = [row["source_occurrence_id"] for row in artifact["graph_records"] if row["unresolved_graph_requirements"]]
    unresolved_targets = [row["source_occurrence_id"] for row in artifact["relation_pattern_nodes"] if row["pattern_resolution_status"] != "EXACT_RELEASED_RELATION_PATTERN"]
    return {
        "matrix_record_count": len(artifact["graph_records"]),
        "graph_record_count": len(artifact["graph_records"]),
        "graph_status_counts": counts(artifact["graph_records"], "graph_status"),
        "participant_kind_counts": counts(artifact["participant_pattern_nodes"], "participant_kind"),
        "relation_resolution_status_counts": counts(artifact["relation_pattern_nodes"], "pattern_resolution_status"),
        "released_relation_family_counts": dict(sorted(Counter(row["released_neutral_relation_family"] for row in artifact["relation_pattern_nodes"] if row["released_neutral_relation_family"]).items())),
        "position_evidence_mode_counts": counts(artifact["position_pattern_constraints"], "evidence_mode"),
        "interaction_edge_class_counts": counts(artifact["interaction_claim_edges"], "edge_class"),
        "context_inheritance_count": len(artifact["context_inheritance_edges"]),
        "context_inheritance_source_occurrence_ids": [row["inheriting_source_occurrence_id"] for row in artifact["context_inheritance_edges"]],
        "multiplicity_constraint_count": len(artifact["multiplicity_constraints"]),
        "multiplicity_source_occurrence_ids": [row["source_occurrence_id"] for row in artifact["multiplicity_constraints"]],
        "chain_pattern_count": len(artifact["interaction_chain_patterns"]),
        "unresolved_graph_source_occurrence_ids": unresolved_records,
        "unresolved_relation_target_source_occurrence_ids": sorted(set(unresolved_targets)),
    }


def _validate_claim_edge_matrix_replay(artifact: dict[str, Any], matrix: dict[str, Any]) -> None:
    matrix_by_oid = {row["source_occurrence_id"]: row for row in matrix["records"]}
    for edge in artifact["interaction_claim_edges"]:
        oid = edge["source_occurrence_id"]
        upstream = matrix_by_oid.get(oid)
        if upstream is None:
            raise TrainingError(f"interaction claim edge has no upstream matrix record: {oid}")
        if edge["actor_reference_kind"] != upstream["actor_reference_kind"]:
            raise TrainingError(f"interaction claim actor reference kind does not replay upstream matrix: {oid}")
        if edge["target_reference_kind"] != upstream["target_reference_kind"]:
            raise TrainingError(f"interaction claim target reference kind does not replay upstream matrix: {oid}")
        if upstream["actor_reference_kind"] == "UNRESOLVED_ACTOR" and (
            edge["actor_relation_pattern_node_ids"] or edge["actor_participant_pattern_node_ids"]
        ):
            raise TrainingError(f"unresolved upstream actor was upgraded to a graph node binding: {oid}")
        if upstream["target_reference_kind"] == "UNRESOLVED_TARGET" and (
            edge["target_relation_pattern_node_ids"] or edge["target_participant_pattern_node_ids"]
        ):
            raise TrainingError(f"unresolved upstream target was upgraded to a graph node binding: {oid}")


def build_structured_source_interaction_pattern_graph(root: Path) -> tuple[dict[str, Any], str]:
    root = root.resolve()
    upstream = validate_classical_relation_interaction_assertion_matrix(root)
    if upstream["status"] != "PASS":
        raise TrainingError("upstream interaction assertion matrix validation failed")
    if sha256_file(root / MATRIX_PATH) != EXPECTED_MATRIX_FILE_SHA256:
        raise TrainingError("upstream interaction assertion matrix file identity changed")
    matrix = load_json(root / MATRIX_PATH)
    if matrix["determinism"]["artifact_semantics_sha256"] != EXPECTED_MATRIX_ARTIFACT_SEMANTICS_SHA256 or matrix["determinism"]["record_hash_chain_sha256"] != EXPECTED_MATRIX_RECORD_HASH_CHAIN_SHA256:
        raise TrainingError("upstream interaction assertion matrix semantic identity changed")
    for path, expected in UPSTREAM_CONTRACT_HASHES.items():
        if sha256_file(root / path) != expected:
            raise TrainingError(f"released upstream contract hash changed: {path}")
    if tuple(row["source_occurrence_id"] for row in matrix["records"]) != MANDATORY_SOURCE_OCCURRENCE_IDS:
        raise TrainingError("upstream matrix source universe changed")
    if set(GRAPH_SPECS) != set(MANDATORY_SOURCE_OCCURRENCE_IDS):
        raise TrainingError("structured pattern graph specification inventory is incomplete")

    bundles = [_build_graph_bundle(record, GRAPH_SPECS[record["source_occurrence_id"]]) for record in matrix["records"]]
    artifact: dict[str, Any] = {
        "schema": AUDIT_ID,
        "audit_id": AUDIT_ID,
        "graph_profile": {"profile_id": GRAPH_PROFILE_ID, "profile_version": GRAPH_PROFILE_VERSION, "contract_role": "STATIC_SOURCE_LEVEL_INTERACTION_PATTERN_GRAPH_ONLY"},
        "authority": {
            "matrix_path": MATRIX_PATH.as_posix(),
            "matrix_file_sha256": EXPECTED_MATRIX_FILE_SHA256,
            "matrix_artifact_semantics_sha256": EXPECTED_MATRIX_ARTIFACT_SEMANTICS_SHA256,
            "matrix_record_hash_chain_sha256": EXPECTED_MATRIX_RECORD_HASH_CHAIN_SHA256,
            "matrix_source_record_count": len(matrix["records"]),
            "canonical_source_path": matrix["authority"]["canonical_source_path"],
            "canonical_source_sha256": matrix["authority"]["canonical_source_sha256"],
            "upstream_contract_file_sha256": dict(UPSTREAM_CONTRACT_HASHES),
        },
        "scope": {
            "chart_specific_exact_binding_candidates_released": False,
            "chart_matching_released": False,
            "condition_observation_verdicts_released": False,
            "classical_operability_evaluator_released": False,
            "graph_or_fixpoint_resolver_released": False,
            "global_relation_precedence_released": False,
            "winner_or_loser_selection_released": False,
            "participant_auto_allocation_released": False,
            "activation_suppression_or_release_runtime_released": False,
            "raw_relation_mutation_released": False,
            "five_combination_final_outcome_released": False,
        },
        "method": {
            "algorithm_id": "BSSIPG_EXACT_MATRIX_TO_STATIC_SOURCE_GRAPH_R1",
            "algorithm_version": "1.0.0",
            "matrix_coverage": "EXACTLY_ONCE_CLOSED_UPSTREAM_RECORD_UNIVERSE",
            "source_context_inheritance": "REGRESSION_LOCKED_SAME_BLOCK_EXAMPLE_CHAIN_ONLY",
            "source_position_compilation": "DIRECT_OR_EXPLICITLY_INHERITED_ONLY",
            "generic_keyword_runtime_mapping": "PROHIBITED",
            "chart_instance_binding": "NOT_PERFORMED",
            "record_order": "UPSTREAM_MATRIX_RECORD_ORDER",
        },
        "closed_vocabularies": {
            "graph_statuses": list(GRAPH_STATUSES),
            "participant_kinds": list(PARTICIPANT_KINDS),
            "position_evidence_modes": list(POSITION_EVIDENCE_MODES),
            "position_statuses": list(POSITION_STATUSES),
            "relation_resolution_statuses": list(RELATION_RESOLUTION_STATUSES),
            "released_relation_families": list(RELEASED_RELATION_FAMILIES),
            "claim_edge_classes": list(CLAIM_EDGE_CLASSES),
            "claim_evidence_modes": list(CLAIM_EVIDENCE_MODES),
            "natal_pillars": ["YEAR", "MONTH", "DAY", "HOUR"],
        },
        "graph_records": [bundle["graph_record"] for bundle in bundles],
        "participant_pattern_nodes": [row for bundle in bundles for row in bundle["participants"]],
        "position_pattern_constraints": [row for bundle in bundles for row in bundle["positions"]],
        "relation_pattern_nodes": [row for bundle in bundles for row in bundle["relations"]],
        "interaction_claim_edges": [row for bundle in bundles for row in bundle["claims"]],
        "context_inheritance_edges": [row for bundle in bundles for row in bundle["inheritance"]],
        "interaction_chain_patterns": [row for bundle in bundles for row in bundle["chains"]],
        "multiplicity_constraints": [row for bundle in bundles for row in bundle["multiplicities"]],
    }
    _validate_claim_edge_matrix_replay(artifact, matrix)
    artifact["summary"] = _summary(artifact)
    artifact["determinism"] = {
        "source_inventory_sha256": object_sha256([row["source_occurrence_id"] for row in artifact["graph_records"]]),
        "graph_record_hash_chain_sha256": object_sha256([row["graph_record_sha256"] for row in artifact["graph_records"]]),
        "node_edge_constraint_semantics_sha256": object_sha256([row["semantic_sha256"] for key in ("participant_pattern_nodes", "position_pattern_constraints", "relation_pattern_nodes", "interaction_claim_edges", "context_inheritance_edges", "interaction_chain_patterns", "multiplicity_constraints") for row in artifact[key]]),
        "closed_registry_sha256": object_sha256({"closed_vocabularies": artifact["closed_vocabularies"], "released_relation_semantics": sorted((family, sorted(values), semantic) for (family, values), semantic in BRANCH_SEMANTICS.items())}),
        "artifact_semantics_sha256": object_sha256(artifact),
    }
    return artifact, _build_report(artifact)


def _build_report(artifact: dict[str, Any]) -> str:
    summary = artifact["summary"]
    lines = [
        "# Bazi Structured Source Interaction Pattern Graph R1 — Coverage Report", "",
        "Status: static, source-level interaction pattern graph only.", "",
        "## Exact upstream coverage", "",
        f"- Assertion Matrix records: `{summary['matrix_record_count']}`.",
        f"- Graph records: `{summary['graph_record_count']}` (exactly once).", "",
        "| Source occurrence | Graph status | Participants | Relations | Positions | Claims | Inheritance | Chains | Multiplicity |", "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in artifact["graph_records"]:
        lines.append(f"| `{row['source_occurrence_id']}` | `{row['graph_status']}` | {len(row['participant_pattern_node_ids'])} | {len(row['relation_pattern_node_ids'])} | {len(row['position_constraint_ids'])} | {len(row['interaction_claim_edge_ids'])} | {len(row['context_inheritance_edge_ids'])} | {len(row['chain_pattern_ids'])} | {len(row['multiplicity_constraint_ids'])} |")
    def table(title: str, values: dict[str, int]) -> None:
        lines.extend(["", f"## {title}", "", "| Value | Count |", "|---|---:|"])
        lines.extend(f"| `{key}` | {count} |" for key, count in values.items())
    table("Graph status counts", summary["graph_status_counts"])
    table("Participant-pattern kinds", summary["participant_kind_counts"])
    table("Relation-pattern resolution status", summary["relation_resolution_status_counts"])
    table("Released neutral relation family mappings", summary["released_relation_family_counts"])
    table("Position-constraint evidence modes", summary["position_evidence_mode_counts"])
    table("Interaction claim edge classes", summary["interaction_edge_class_counts"])
    lines.extend(["", "## Context inheritance and multiplicity", "", f"- Context inheritance edges (`SOURCE_CONTEXT_INHERITED`): `{summary['context_inheritance_count']}` — " + ", ".join(f"`{value}`" for value in summary["context_inheritance_source_occurrence_ids"]) + ".", f"- Multiplicity constraints: `{summary['multiplicity_constraint_count']}` — " + ", ".join(f"`{value}`" for value in summary["multiplicity_source_occurrence_ids"]) + ".", f"- Source narrative chains: `{summary['chain_pattern_count']}`.", "", "## Unresolved identities", "", "Records retaining unresolved graph requirements: " + ", ".join(f"`{value}`" for value in summary["unresolved_graph_source_occurrence_ids"]) + ".", "", "Records containing relation family/target nodes that are intentionally not exact released mappings: " + ", ".join(f"`{value}`" for value in summary["unresolved_relation_target_source_occurrence_ids"]) + ".", "", "## Release boundary", "", "This release does **not** publish chart-specific binding, Classical operability, condition verdicts, precedence, winner selection, activation, suppression, release, raw-relation mutation, or final relation outcomes.", "", "`SHARED_PARTICIPANT` remains topology only; `EXITED` remains transition-set change only. Neither is compiled into Classical interaction semantics.", ""])
    return "\n".join(lines)


def write_structured_source_interaction_pattern_graph(root: Path) -> dict[str, Any]:
    root = root.resolve()
    artifact, report = build_structured_source_interaction_pattern_graph(root)
    atomic_write_json(root / GRAPH_PATH, artifact)
    atomic_write_bytes(root / REPORT_PATH, report.encode("utf-8"))
    return validate_structured_source_interaction_pattern_graph(root)


def _validate_semantic_hash(row: dict[str, Any], identity: str) -> None:
    expected = object_sha256({key: value for key, value in row.items() if key != "semantic_sha256"})
    if row["semantic_sha256"] != expected:
        raise TrainingError(f"structured pattern graph semantic hash mismatch: {identity}")


def validate_structured_source_interaction_pattern_graph_value(root: Path, artifact: dict[str, Any]) -> dict[str, Any]:
    root = root.resolve()
    schema = load_json(root / SCHEMA_PATH)
    errors = sorted(Draft202012Validator(schema).iter_errors(artifact), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        raise TrainingError(f"structured pattern graph schema failure at {list(first.path)}: {first.message}")
    matrix = load_json(root / MATRIX_PATH)
    _validate_claim_edge_matrix_replay(artifact, matrix)
    expected, expected_report = build_structured_source_interaction_pattern_graph(root)
    if artifact != expected:
        raise TrainingError("structured pattern graph deterministic replay mismatch")
    records = artifact["graph_records"]
    if [row["source_occurrence_id"] for row in records] != list(MANDATORY_SOURCE_OCCURRENCE_IDS) or len(records) != len(set(row["source_occurrence_id"] for row in records)):
        raise TrainingError("structured pattern graph matrix coverage is not exactly once")
    for key, id_key in (("participant_pattern_nodes", "participant_pattern_node_id"), ("position_pattern_constraints", "position_constraint_id"), ("relation_pattern_nodes", "relation_pattern_node_id"), ("interaction_claim_edges", "interaction_claim_edge_id"), ("context_inheritance_edges", "context_inheritance_edge_id"), ("interaction_chain_patterns", "chain_pattern_id"), ("multiplicity_constraints", "multiplicity_constraint_id")):
        for row in artifact[key]:
            _validate_semantic_hash(row, row[id_key])
    for row in artifact["relation_pattern_nodes"]:
        if row["pattern_resolution_status"] == "EXACT_RELEASED_RELATION_PATTERN":
            if row["released_neutral_relation_family"] not in RELEASED_RELATION_FAMILIES or row["released_neutral_semantic_relation_id"] is None:
                raise TrainingError("exact relation pattern is not bound to a released neutral identity")
            if row["released_neutral_relation_family"] == "BRANCH_TRINE" and row["source_arity"] != 3:
                raise TrainingError("complete Sanhe source pattern lost arity 3")
        elif row["released_neutral_relation_family"] is not None or row["released_neutral_semantic_relation_id"] is not None:
            raise TrainingError("unresolved/generic source relation was broad-inferred")
        if row["released_neutral_relation_family"] == "BRANCH_CHUAN" and "HARM" in (row["released_neutral_semantic_relation_id"] or ""):
            raise TrainingError("BRANCH_CHUAN was converted to HARM")
    by_oid = {row["source_occurrence_id"]: row for row in records}
    if set(INHERITANCE_REGISTRY) != set(artifact["summary"]["context_inheritance_source_occurrence_ids"]):
        raise TrainingError("source context inheritance inventory changed")
    matrix_by_oid = {row["source_occurrence_id"]: row for row in matrix["records"]}
    for edge in artifact["context_inheritance_edges"]:
        oid = edge["inheriting_source_occurrence_id"]
        antecedent = edge["antecedent_source_occurrence_id"]
        if INHERITANCE_REGISTRY.get(oid) != antecedent or matrix_by_oid[oid]["parent_source_block_id"] != matrix_by_oid[antecedent]["parent_source_block_id"] or edge["direct_source_lexeme_claimed"]:
            raise TrainingError("source context inheritance crossed its regression-locked scope")
    multiplicity = artifact["multiplicity_constraints"]
    if len(multiplicity) != 1 or multiplicity[0]["source_occurrence_id"] != "ZPZQ-CL-09-005-002" or multiplicity[0]["required_symbolic_cardinality"] != 2 or multiplicity[0]["exact_slot_selection"] != "NOT_SELECTED" or multiplicity[0]["alternative_path_requirement"] != "PRESERVE_ALL_COMPATIBLE_EXACT_INSTANCE_PATHS" or multiplicity[0]["winner_emitted"]:
        raise TrainingError("二卯 exchangeable path preservation failed")
    for oid in ("ZPZQ-CL-09-007-002", "ZPZQ-CL-09-007-003"):
        positions = [row for row in artifact["position_pattern_constraints"] if row["source_occurrence_id"] == oid]
        exact_hour = [row for row in positions if row["natal_pillar"] == "HOUR" and row["constraint_status"] == "EXACT_SYMBOLIC_PARTICIPANT_PILLAR_CONSTRAINT"]
        unresolved_hour = [row for row in positions if row["evidence_mode"] == "SOURCE_POSITION_CONTEXT_UNRESOLVED"]
        if exact_hour or len(unresolved_hour) != 1 or len(unresolved_hour[0]["participant_pattern_node_ids"]) != 2:
            raise TrainingError("时逢 grouped source context was fabricated as simultaneous exact HOUR values")
    attenuation = [row for row in artifact["interaction_claim_edges"] if row["source_occurrence_id"] == "ZPZQ-CL-09-009-004"]
    if len(attenuation) != 1 or attenuation[0]["edge_class"] != "SOURCE_ASSERTED_ATTENUATION" or attenuation[0]["raw_relation_mutation_emitted"]:
        raise TrainingError("冲之无力 was converted to relation absence or mutation")
    for oid in ("QTBJ-CL-05347", "QTBJ-CL-05370"):
        relations = [row for row in artifact["relation_pattern_nodes"] if row["source_occurrence_id"] == oid]
        if len(relations) != 1 or relations[0]["pattern_resolution_status"] != "UNRESOLVED_RELATION_PATTERN" or relations[0]["released_neutral_relation_family"] is not None:
            raise TrainingError("QTBJ 解合 target was broad-inferred")
    forbidden_keys = {"instance_id", "candidate_index", "binding_verdict", "operability", "precedence", "winner", "loser", "activation", "suppression", "release_verdict", "final_outcome"}
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if forbidden_keys & set(value):
                raise TrainingError(f"structured pattern graph emitted forbidden runtime fields: {sorted(forbidden_keys & set(value))}")
            for child in value.values(): walk(child)
        elif isinstance(value, list):
            for child in value: walk(child)
    walk(artifact)
    if any(value for key, value in artifact["scope"].items() if key.endswith("_released")):
        raise TrainingError("structured pattern graph released forbidden downstream semantics")
    return {"status": "PASS", "audit_id": AUDIT_ID, **artifact["summary"], **artifact["determinism"], "matrix_exact_replay": True, "schema_validation": True, "deterministic_rebuild": True, "upstream_hash_regression": True, "forbidden_scope_unchanged": True, "report_sha256": _sha256(expected_report.encode("utf-8"))}


def validate_structured_source_interaction_pattern_graph(root: Path) -> dict[str, Any]:
    root = root.resolve()
    artifact = load_json(root / GRAPH_PATH)
    report = (root / REPORT_PATH).read_text(encoding="utf-8")
    result = validate_structured_source_interaction_pattern_graph_value(root, artifact)
    _, expected_report = build_structured_source_interaction_pattern_graph(root)
    if report != expected_report:
        raise TrainingError("structured pattern graph coverage report is stale or tampered")
    return result
