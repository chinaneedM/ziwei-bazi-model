from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .learning import load_taxonomy
from .util import TrainingError, load_json, object_sha256, sha256_file


MANIFEST_PATH = Path("case-bank/manifest.json")
CASE_ID = re.compile(r"CASE-(\d{3})")
FORBIDDEN_KEYS = {
    "answer",
    "answers",
    "answer_key",
    "correct_answer",
    "correct_option",
    "score",
    "review",
    "top1",
    "top2",
}


def _answer_free(value: Any, location: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in FORBIDDEN_KEYS:
                raise TrainingError(f"answer/review-bearing key in case bank: {location}.{key}")
            _answer_free(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _answer_free(child, f"{location}[{index}]")


def _validate_profile(profile: Any, taxonomy: dict[str, Any], case_id: str, question_id: str) -> None:
    fields = {
        "topic_tags",
        "subject_tags",
        "time_scope_tags",
        "endpoint_tags",
        "reasoning_skill_tags",
        "source_routes",
        "governance_tags",
        "atomization_required",
        "option_atom_hints",
    }
    if not isinstance(profile, dict) or set(profile) != fields:
        raise TrainingError(f"invalid preblind profile fields for {case_id}/{question_id}")
    for field in (
        "topic_tags",
        "subject_tags",
        "time_scope_tags",
        "endpoint_tags",
        "reasoning_skill_tags",
        "source_routes",
        "governance_tags",
    ):
        values = profile[field]
        if not isinstance(values, list) or len(values) != len(set(values)):
            raise TrainingError(f"invalid {field} for {case_id}/{question_id}")
        allowed = set(taxonomy[field])
        if any(value not in allowed for value in values):
            raise TrainingError(f"unknown {field} value for {case_id}/{question_id}")
    if not isinstance(profile["atomization_required"], bool):
        raise TrainingError(f"invalid atomization flag for {case_id}/{question_id}")
    hints = profile["option_atom_hints"]
    if not isinstance(hints, dict):
        raise TrainingError(f"invalid option atom hints for {case_id}/{question_id}")


def validate_case_bank(root: Path) -> dict[str, Any]:
    root = root.resolve()
    manifest = load_json(root / MANIFEST_PATH)
    if manifest.get("schema") != "FORTUNE-CASE-BANK-MANIFEST-V1":
        raise TrainingError("wrong case-bank manifest schema")
    if manifest.get("corpus_id") != "FORTUNE-CASE-BANK-107-V1":
        raise TrainingError("unexpected case-bank corpus id")
    if manifest.get("answer_payload_present") is not False:
        raise TrainingError("case-bank manifest does not declare answer isolation")
    expected_ids = [f"CASE-{number:03d}" for number in range(1, 108)]
    if set(manifest.get("case_hashes", {})) != set(expected_ids):
        raise TrainingError("case-bank hash set is not exactly CASE-001 through CASE-107")
    taxonomy = load_taxonomy(root)
    accepted: set[str] = set()
    blocked: set[str] = set()
    question_count = 0
    identity_to_cases: dict[str, list[str]] = {}
    for case_id in expected_ids:
        case_path = root / "case-bank" / "cases" / f"{case_id}.json"
        case = load_json(case_path)
        if case.get("schema") != "FORTUNE-CASE-BANK-CASE-V1" or case.get("case_id") != case_id:
            raise TrainingError(f"invalid case-bank record: {case_id}")
        if manifest["case_hashes"][case_id] != object_sha256(case):
            raise TrainingError(f"case-bank record hash mismatch: {case_id}")
        if case.get("answer_isolation", {}).get("answer_payload_present") is not False:
            raise TrainingError(f"case-bank record does not declare answer isolation: {case_id}")
        _answer_free(case)
        status = case.get("quality", {}).get("status")
        if status == "BLOCKED_INPUT":
            blocked.add(case_id)
        elif status in {"ACCEPTED", "ACCEPTED_REVEALED_HISTORY"}:
            accepted.add(case_id)
        else:
            raise TrainingError(f"unknown case-bank quality status: {case_id}")
        identity = case.get("identity_group_id")
        if not isinstance(identity, str) or not identity.startswith("PERSON-"):
            raise TrainingError(f"invalid identity group: {case_id}")
        identity_to_cases.setdefault(identity, []).append(case_id)
        questions = case.get("questions", {}).get("parsed")
        if not isinstance(questions, list) or len(questions) != case.get("questions", {}).get("question_count"):
            raise TrainingError(f"case-bank question count mismatch: {case_id}")
        question_count += len(questions)
        for question in questions:
            question_id = question.get("question_id")
            if not isinstance(question_id, str):
                raise TrainingError(f"invalid question id: {case_id}")
            option_ids = [option.get("option_id") for option in question.get("options", [])]
            if case_id in accepted and option_ids not in (
                list("ABCD"),
                list("ABCDE"),
            ):
                raise TrainingError(f"accepted case has an invalid option set: {case_id}/{question_id}")
            _validate_profile(question.get("preblind_profile"), taxonomy, case_id, question_id)
            atom_keys = set(question["preblind_profile"]["option_atom_hints"])
            if atom_keys != set(option_ids):
                raise TrainingError(f"option-atom keys do not match option ids: {case_id}/{question_id}")
        source_image = case.get("bazi", {}).get("source_image", {})
        image_path = source_image.get("path")
        if image_path:
            absolute = root / image_path
            if not absolute.is_file() or sha256_file(absolute) != source_image.get("sha256"):
                raise TrainingError(f"bazi source-image binding mismatch: {case_id}")
        for section_name in ("ziwei", "questions"):
            section = case.get(section_name, {})
            source_path = section.get("source_path")
            if isinstance(source_path, str) and source_path.startswith("case-bank/raw/"):
                absolute = root / source_path
                if not absolute.is_file() or sha256_file(absolute) != section.get("source_sha256", section.get("sha256")):
                    raise TrainingError(f"{section_name} raw-source binding mismatch: {case_id}")

    if len(expected_ids) != manifest.get("case_count") or question_count != manifest.get("question_count"):
        raise TrainingError("case-bank manifest totals do not balance")
    if len(accepted) != manifest.get("accepted_case_count") or len(blocked) != manifest.get("blocked_case_count"):
        raise TrainingError("case-bank accepted/blocked totals do not balance")
    manifest_blocked = {row.get("case_id") for row in manifest.get("blocked_cases", [])}
    if manifest_blocked != blocked:
        raise TrainingError("case-bank blocked-case list mismatch")

    partition_members: dict[str, str] = {}
    expected_partition_paths = {
        "DEVELOPMENT": "case-bank/partitions/development.json",
        "STAGE_VALIDATION": "case-bank/partitions/stage-validation.json",
        "FINAL_HOLDOUT": "case-bank/partitions/final-holdout.json",
    }
    for partition_id, relative_path in expected_partition_paths.items():
        partition = load_json(root / relative_path)
        if partition.get("schema") != "FORTUNE-CASE-BANK-PARTITION-V1" or partition.get("partition_id") != partition_id:
            raise TrainingError(f"invalid case-bank partition: {partition_id}")
        case_order = partition.get("case_order")
        if not isinstance(case_order, list) or len(case_order) != len(set(case_order)):
            raise TrainingError(f"invalid case order in partition: {partition_id}")
        if set(partition.get("cases", {})) != set(case_order):
            raise TrainingError(f"partition case mapping mismatch: {partition_id}")
        for case_id in case_order:
            if case_id in blocked or case_id not in accepted:
                raise TrainingError(f"blocked or unknown case entered partition: {case_id}")
            if case_id in partition_members:
                raise TrainingError(f"case appears in multiple partitions: {case_id}")
            partition_members[case_id] = partition_id
    if set(partition_members) != accepted:
        raise TrainingError("accepted cases are not partitioned exactly once")
    for identity, case_ids in identity_to_cases.items():
        partitions = {partition_members[case_id] for case_id in case_ids if case_id in partition_members}
        if len(partitions) > 1:
            raise TrainingError(f"same-person leakage across partitions: {identity}")
    if manifest.get("duplicate_identity_groups") != {
        identity: case_ids for identity, case_ids in identity_to_cases.items() if len(case_ids) > 1
    }:
        raise TrainingError("duplicate-identity manifest is stale")
    overlap = load_json(root / "case-bank" / "source-overlap-audit.json")
    if overlap.get("schema") != "CASE-SOURCE-OVERLAP-AUDIT-V1":
        raise TrainingError("wrong case/source overlap audit schema")
    if overlap.get("case_bank_manifest_sha256") != object_sha256(manifest):
        raise TrainingError("case/source overlap audit is stale for the case bank")
    canonical_manifest = load_json(root / "sources" / "canonical-manifest.json")
    if overlap.get("canonical_source_manifest_sha256") != object_sha256(canonical_manifest):
        raise TrainingError("case/source overlap audit is stale for canonical sources")
    if overlap.get("uncontained_high_risk_case_ids"):
        raise TrainingError("high-risk case/source overlap escaped the development partition")
    source_exposed = set(overlap.get("source_exposed_case_ids", []))
    if any(partition_members.get(case_id) != "DEVELOPMENT" for case_id in source_exposed):
        raise TrainingError("source-exposed cases must remain development-only")
    development = load_json(root / "case-bank" / "partitions" / "development.json")
    if set(development.get("source_exposed_case_ids", [])) != source_exposed:
        raise TrainingError("development source-exposure list is stale")
    if source_exposed & set(development.get("first_blind_schedule", [])):
        raise TrainingError("source-exposed cases entered the first-blind schedule")
    return {
        "status": "PASS",
        "corpus_id": manifest["corpus_id"],
        "cases": manifest["case_count"],
        "questions": manifest["question_count"],
        "accepted_cases": manifest["accepted_case_count"],
        "blocked_cases": sorted(blocked),
        "partition_counts": {
            partition_id: sum(value == partition_id for value in partition_members.values())
            for partition_id in expected_partition_paths
        },
        "answer_payload_present": False,
        "same_person_cross_partition_leakage": False,
        "exact_source_stem_overlap_questions": overlap.get("exact_stem_question_count"),
        "high_risk_source_overlap_questions": overlap.get("high_risk_question_count"),
        "source_exposed_development_cases": sorted(source_exposed),
    }


def case_bank_report(root: Path) -> dict[str, Any]:
    validation = validate_case_bank(root)
    manifest = load_json(root.resolve() / MANIFEST_PATH)
    return {**validation, "coverage": manifest["coverage"]}
