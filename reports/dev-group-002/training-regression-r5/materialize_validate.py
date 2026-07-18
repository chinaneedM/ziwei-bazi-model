#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

ROUND_DIR = Path("reports/dev-group-002/training-regression-r5")
HISTORY = {
    "R1": "reports/dev-group-002/training-regression-r1/manifest.json",
    "R2": "reports/dev-group-002/training-regression-r2/active-whitelist-receipt.json",
    "R3": "reports/dev-group-002/training-regression-r3/progress.json",
    "R4": "reports/dev-group-002/training-regression-r4/compact-manifest.json",
}
GENERATED = (
    "prediction-freeze.json",
    "pairwise-replay.json",
    "postreveal-review.json",
    "generic-fix.json",
    "manifest.json",
    "summary.md",
    "validation.json",
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_payload(obj: dict[str, Any]) -> bytes:
    clone = dict(obj)
    clone.pop("canonical_sha256", None)
    return (json.dumps(clone, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def canonical_hash(obj: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_payload(obj)).hexdigest()


def with_hash(obj: dict[str, Any]) -> dict[str, Any]:
    obj = dict(obj)
    obj["canonical_sha256"] = canonical_hash(obj)
    return obj


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def build_objects(repo_root: Path) -> dict[str, Any]:
    r4 = read_json(repo_root / HISTORY["R4"])
    cases = r4["cases"]
    expected_case_ids = [f"DEV-EXAMPLE-{i:03d}" for i in range(1, 6)]
    if [case["case_id"] for case in cases] != expected_case_ids:
        raise ValueError("R4 fixed-case order changed")

    prediction_cases: list[dict[str, Any]] = []
    pairwise_rows: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []
    answer_vectors: dict[str, str] = {}
    top1_hits = 0
    top2_coverage = 0
    answer_rank_position_counts = {1: 0, 2: 0, 3: 0, 4: 0}

    for case in cases:
        case_id = case["case_id"]
        ranks = case["ranks"]
        answer = case["answer_vector"]
        answer_vectors[case_id] = answer
        if len(ranks) != 5 or len(answer) != 5:
            raise ValueError(f"{case_id}: expected five questions")
        for rank in ranks:
            if sorted(rank) != list("ABCD"):
                raise ValueError(f"{case_id}: invalid total order {rank}")

        prediction_cases.append(
            {
                "case_id": case_id,
                "question_count": 5,
                "ranks": ranks,
                "top1_vector": "".join(rank[0] for rank in ranks),
                "top2_vector": "".join(rank[1] for rank in ranks),
                "prediction_origin": "R4_SOURCE_CONSTRAINED_TOTAL_ORDER_REPLAY",
                "answer_visible_during_prediction_materialization": False,
            }
        )

        for qindex, (rank, literal_answer) in enumerate(zip(ranks, answer), 1):
            question_id = f"Q{qindex}"
            answer_position = rank.index(literal_answer) + 1
            answer_rank_position_counts[answer_position] += 1
            top1_hits += int(answer_position == 1)
            top2_coverage += int(answer_position <= 2)
            outcome = "TOP1_HIT" if answer_position == 1 else ("TOP2_ONLY" if answer_position == 2 else "OUTSIDE_TOP2")
            review_rows.append(
                {
                    "case_id": case_id,
                    "question_id": question_id,
                    "frozen_rank": rank,
                    "frozen_top1": rank[0],
                    "frozen_top2": rank[1],
                    "literal_answer": literal_answer,
                    "answer_rank_position": answer_position,
                    "outcome": outcome,
                    "diagnostic_scope": "EXECUTION_AUDIT_ONLY",
                    "reproducible_defect": "R4_DID_NOT_PERSIST_ACTUAL_PAIRWISE_ROWS_OR_RECOMPUTE_DECLARED_CANONICAL_HASH",
                    "astrological_direction_change_authorized": False,
                }
            )
            for left, right in itertools.combinations("ABCD", 2):
                winner = left if rank.index(left) < rank.index(right) else right
                loser = right if winner == left else left
                pairwise_rows.append(
                    {
                        "case_id": case_id,
                        "question_id": question_id,
                        "left": left,
                        "right": right,
                        "winner": winner,
                        "loser": loser,
                        "winner_rank_index": rank.index(winner),
                        "loser_rank_index": rank.index(loser),
                        "decision_basis": "FROZEN_R4_TOTAL_ORDER_REPLAY",
                        "evidence_direction_claim": "NOT_RECONSTRUCTED_IN_R5",
                        "astrological_contribution_added": False,
                    }
                )

    prediction = with_hash(
        {
            "schema": "DEV-GROUP-002-R5-PREDICTION-FREEZE-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R5",
            "run_class": "ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD_WITH_PREDICTION_OBJECT_ISOLATION",
            "source_round": "R4",
            "source_r4_full_object_canonical_sha256": r4["full_object_canonical_sha256"],
            "case_ids": expected_case_ids,
            "cases": prediction_cases,
            "question_count": 25,
            "formal_exact_assertion_permission": "NULL_ONLY",
            "machine_valid_local_seals": 0,
            "s03_fusions": 0,
            "new_case_admission": "BLOCKED",
            "contains_answers": False,
            "changes_astrological_knowledge": False,
            "changes_relative_choices": False,
        }
    )

    pairwise = with_hash(
        {
            "schema": "DEV-GROUP-002-R5-PAIRWISE-REPLAY-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R5",
            "parent_prediction_sha256": prediction["canonical_sha256"],
            "row_count": len(pairwise_rows),
            "rows": pairwise_rows,
            "purpose": "Materialize the 150 pairwise rows that R4 claimed but did not persist.",
            "decision_limit": "This replay proves total-order consistency only and does not reconstruct missing evidence-direction reasons.",
            "changes_astrological_knowledge": False,
        }
    )

    review = with_hash(
        {
            "schema": "DEV-GROUP-002-R5-POSTREVEAL-QUESTION-REVIEW-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R5",
            "parent_prediction_sha256": prediction["canonical_sha256"],
            "answer_vectors": answer_vectors,
            "question_rows": review_rows,
            "statistics": {
                "question_count": 25,
                "top1_hits": top1_hits,
                "top2_coverage": top2_coverage,
                "answer_rank_position_counts": {str(key): value for key, value in answer_rank_position_counts.items()},
                "top1_rate": top1_hits / 25,
                "top2_rate": top2_coverage / 25,
            },
            "diagnosis": {
                "primary_defect": "R4 validator generated a pair count in memory but did not persist pairwise row bodies, direction matrices, parent evidence identifiers, or recompute the declared full-object canonical hash.",
                "impact": "R4 score and rank shape were reproducible, but the claimed pairwise object and its provenance were not independently replayable.",
                "classification": "EXECUTION_AND_AUDIT_DEFECT",
                "knowledge_defect_proven": False,
                "base_knowledge_change_authorized": False,
            },
        }
    )

    generic_fix = with_hash(
        {
            "schema": "DEV-GROUP-002-R5-GENERIC-FIX-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R5",
            "fix_id": "TR-R5-PAIRWISE-BODY-HASH-AND-ANSWER-SEPARATION",
            "defect_class": "CLAIMED_PAIRWISE_AND_CANONICAL_OBJECT_NOT_MATERIALIZED",
            "reproduction": {
                "r4_validator_path": HISTORY["R4"].replace("compact-manifest.json", "validate.py"),
                "r4_manifest_path": HISTORY["R4"],
                "observed_behavior": [
                    "R4 validator increments a local pair counter from rank permutations but stores no pairwise row bodies.",
                    "R4 manifest declares a full_object_canonical_sha256 but R4 validator does not recompute it.",
                    "R4 manifest co-locates answer vectors with frozen ranks, so prediction freezing and answer scoring are not separate artifacts.",
                ],
            },
            "general_rules": [
                "A round claiming pairwise replay must persist exactly N(N-1)/2 pairwise row bodies per question and validate every row against the frozen rank.",
                "A declared canonical hash must be recomputed from a deterministic canonical serialization during validation.",
                "Prediction ranks must be stored in an answer-free immutable object before answer replay and scoring.",
                "Postreveal review must contain one row per question and must not rewrite the frozen prediction.",
                "An execution-audit repair may preserve all relative choices and scores; it must not be presented as an accuracy gain.",
            ],
            "case_specific_direction_rule_added": False,
            "answer_token_in_general_rule_scan": "PASS",
            "base_astrological_knowledge_changed": False,
            "s00_s19_modified": False,
            "impact_scope": "TRAINING_RUNTIME_ARTIFACTS_AND_VALIDATOR_ONLY",
        }
    )

    history_rows: dict[str, dict[str, Any]] = {}
    for round_id, relative_path in HISTORY.items():
        history_path = repo_root / relative_path
        row: dict[str, Any] = {
            "path": relative_path,
            "git_blob_sha": git_blob_sha(history_path),
            "preserved": True,
        }
        if round_id == "R4":
            row["full_object_canonical_sha256"] = r4["full_object_canonical_sha256"]
        history_rows[round_id] = row

    manifest = with_hash(
        {
            "schema": "DEV-GROUP-002-R5-FROZEN-MANIFEST-V1",
            "group_id": "DEV-GROUP-002",
            "round_id": "R5",
            "status": "FROZEN",
            "run_class": "ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD",
            "historical_rounds": history_rows,
            "artifacts": {
                "prediction_freeze": {"path": str(ROUND_DIR / "prediction-freeze.json"), "canonical_sha256": prediction["canonical_sha256"]},
                "pairwise_replay": {"path": str(ROUND_DIR / "pairwise-replay.json"), "canonical_sha256": pairwise["canonical_sha256"], "row_count": 150},
                "postreveal_review": {"path": str(ROUND_DIR / "postreveal-review.json"), "canonical_sha256": review["canonical_sha256"], "row_count": 25},
                "generic_fix": {"path": str(ROUND_DIR / "generic-fix.json"), "canonical_sha256": generic_fix["canonical_sha256"]},
            },
            "statistics": {
                "original_blind_baseline": {"top1_hits": 11, "top2_coverage": 16, "status": "PRESERVED_NOT_OVERWRITTEN"},
                "r4": {"top1_hits": 14, "top2_coverage": 16, "status": "TRAINING_REGRESSION_SCORE"},
                "r5": {"top1_hits": top1_hits, "top2_coverage": top2_coverage, "status": "TRAINING_REGRESSION_SCORE_NO_SELECTION_CHANGE"},
                "question_count": 25,
                "pairwise_row_count": 150,
                "formal_valid_questions": 0,
                "machine_valid_local_seals": 0,
                "s03_fusions": 0,
            },
            "training_conclusion": "R5 closes an execution-audit gap without changing any choice. It does not prove a knowledge improvement, formal validity, blind accuracy, or generalization.",
            "new_case_admission": "BLOCKED",
            "s00_s19_modified": False,
            "base_astrological_knowledge_changed": False,
            "case_specific_direction_rule_added": False,
        }
    )

    return {
        "prediction-freeze.json": prediction,
        "pairwise-replay.json": pairwise,
        "postreveal-review.json": review,
        "generic-fix.json": generic_fix,
        "manifest.json": manifest,
    }


def materialize(repo_root: Path) -> None:
    output_dir = repo_root / ROUND_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    objects = build_objects(repo_root)
    for filename, obj in objects.items():
        write_json(output_dir / filename, obj)

    stats = objects["manifest.json"]["statistics"]
    review_stats = objects["postreveal-review.json"]["statistics"]
    summary = f"""# DEV-GROUP-002 R5：成对对象与冻结边界闭合

R5只使用固定五案 `DEV-EXAMPLE-001` 至 `005`，完整保留R1—R4，不新增案例，不修改S00—S19，也不改变任何R4相对选择。

本轮先重放R4的25个冻结全排序，再把此前只在验证器内计数、但未落盘的150条成对比较逐行物化。预测对象与答案复盘对象已拆分；每个JSON对象的规范化SHA256由R5验证器现场重算；25题均生成逐题复盘行。

统计保持不变：`TRAINING_REGRESSION_SCORE` TOP1为{stats['r5']['top1_hits']}/25，TOP2为{stats['r5']['top2_coverage']}/25。答案位次分布为：第1位{review_stats['answer_rank_position_counts']['1']}题、第2位{review_stats['answer_rank_position_counts']['2']}题、第3位{review_stats['answer_rank_position_counts']['3']}题、第4位{review_stats['answer_rank_position_counts']['4']}题。

本轮确认的是可复现执行缺陷：R4声称150条成对比较与完整对象哈希，但没有保存成对正文，也没有现场重算声明的完整对象哈希。R5修复训练运行对象与验证接口，不证明命理知识改进、正式有效性、盲测提升或泛化。

正式有效题仍为0，紫微与八字机器有效本地密封仍为0，S03融合仍为0，新案例准入继续关闭。
"""
    (output_dir / "summary.md").write_text(summary, encoding="utf-8")


def validate(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    output_dir = repo_root / ROUND_DIR
    required = GENERATED[:-1]
    for filename in required:
        if not (output_dir / filename).exists():
            errors.append(f"missing generated artifact: {filename}")
    if errors:
        return {"status": "FAIL", "errors": errors, "error_count": len(errors)}

    prediction = read_json(output_dir / "prediction-freeze.json")
    pairwise = read_json(output_dir / "pairwise-replay.json")
    review = read_json(output_dir / "postreveal-review.json")
    generic_fix = read_json(output_dir / "generic-fix.json")
    manifest = read_json(output_dir / "manifest.json")
    r4 = read_json(repo_root / HISTORY["R4"])

    for label, obj in (
        ("prediction", prediction),
        ("pairwise", pairwise),
        ("review", review),
        ("generic_fix", generic_fix),
        ("manifest", manifest),
    ):
        if canonical_hash(obj) != obj.get("canonical_sha256"):
            errors.append(f"{label}: canonical hash mismatch")

    forbidden_prediction_keys = {"answer_vector", "answer_vectors", "literal_answer"}

    def contains_forbidden_key(value: Any) -> bool:
        if isinstance(value, dict):
            return any(key in forbidden_prediction_keys or contains_forbidden_key(item) for key, item in value.items())
        if isinstance(value, list):
            return any(contains_forbidden_key(item) for item in value)
        return False

    if contains_forbidden_key(prediction):
        errors.append("prediction freeze contains answer payload key")
    if prediction.get("contains_answers") is not False:
        errors.append("prediction answer-isolation declaration")
    if prediction.get("changes_relative_choices") is not False:
        errors.append("R5 rewrote an R4 choice")

    r4_cases = {case["case_id"]: case for case in r4["cases"]}
    ranks: dict[tuple[str, str], str] = {}
    for case in prediction.get("cases", []):
        case_id = case["case_id"]
        if case_id not in r4_cases or case["ranks"] != r4_cases[case_id]["ranks"]:
            errors.append(f"{case_id}: prediction is not exact R4 replay")
        if "".join(rank[0] for rank in case["ranks"]) != case["top1_vector"]:
            errors.append(f"{case_id}: top1 derivation")
        if "".join(rank[1] for rank in case["ranks"]) != case["top2_vector"]:
            errors.append(f"{case_id}: top2 derivation")
        for index, rank in enumerate(case["ranks"], 1):
            if sorted(rank) != list("ABCD"):
                errors.append(f"{case_id} Q{index}: invalid rank")
            ranks[(case_id, f"Q{index}")] = rank

    pairwise_rows = pairwise.get("rows", [])
    if pairwise.get("row_count") != 150 or len(pairwise_rows) != 150:
        errors.append("pairwise row count")
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in pairwise_rows:
        key = (row["case_id"], row["question_id"])
        grouped.setdefault(key, []).append(row)
        rank = ranks.get(key)
        if rank is None:
            errors.append(f"unknown pairwise question: {key}")
            continue
        expected_winner = row["left"] if rank.index(row["left"]) < rank.index(row["right"]) else row["right"]
        if row["winner"] != expected_winner:
            errors.append(f"pairwise winner mismatch: {key} {row['left']}/{row['right']}")
        if row.get("decision_basis") != "FROZEN_R4_TOTAL_ORDER_REPLAY":
            errors.append(f"pairwise basis mismatch: {key}")
        if row.get("astrological_contribution_added") is not False:
            errors.append(f"unauthorized pairwise contribution: {key}")
    expected_pairs = set(itertools.combinations("ABCD", 2))
    if len(grouped) != 25:
        errors.append("pairwise question coverage")
    for key, rows in grouped.items():
        if len(rows) != 6 or {(row["left"], row["right"]) for row in rows} != expected_pairs:
            errors.append(f"pairwise option coverage: {key}")

    answer_vectors = review.get("answer_vectors", {})
    review_rows = review.get("question_rows", [])
    top1_hits = 0
    top2_coverage = 0
    rank_positions = {1: 0, 2: 0, 3: 0, 4: 0}
    if len(review_rows) != 25:
        errors.append("postreveal review row count")
    for row in review_rows:
        key = (row["case_id"], row["question_id"])
        rank = ranks.get(key)
        question_index = int(row["question_id"][1:]) - 1
        literal_answer = answer_vectors.get(row["case_id"], "")[question_index:question_index + 1]
        if rank is None or row.get("literal_answer") != literal_answer:
            errors.append(f"review mapping mismatch: {key}")
            continue
        answer_position = rank.index(literal_answer) + 1
        if row.get("answer_rank_position") != answer_position:
            errors.append(f"review answer position: {key}")
        rank_positions[answer_position] += 1
        top1_hits += int(answer_position == 1)
        top2_coverage += int(answer_position <= 2)
        if row.get("astrological_direction_change_authorized") is not False:
            errors.append(f"review authorized direction rewrite: {key}")

    review_stats = review.get("statistics", {})
    if (top1_hits, top2_coverage) != (14, 16):
        errors.append("R5 score recomputation")
    if (review_stats.get("top1_hits"), review_stats.get("top2_coverage")) != (14, 16):
        errors.append("R5 declared score")
    if review_stats.get("answer_rank_position_counts") != {str(key): value for key, value in rank_positions.items()}:
        errors.append("answer rank-position distribution")

    general_rule_text = "\n".join(generic_fix.get("general_rules", []))
    forbidden_tokens = [
        "DEV-EXAMPLE-001", "DEV-EXAMPLE-002", "DEV-EXAMPLE-003", "DEV-EXAMPLE-004", "DEV-EXAMPLE-005",
        "BDBAB", "DBDDB", "BBDCA", "CDBAB", "DADAB",
    ]
    if any(token in general_rule_text for token in forbidden_tokens):
        errors.append("case-specific token leaked into general rules")
    if generic_fix.get("base_astrological_knowledge_changed") is not False or generic_fix.get("s00_s19_modified") is not False:
        errors.append("unauthorized knowledge-library change")

    for round_id, row in manifest.get("historical_rounds", {}).items():
        expected_path = HISTORY.get(round_id)
        if row.get("path") != expected_path:
            errors.append(f"{round_id}: historical path")
            continue
        path = repo_root / expected_path
        if git_blob_sha(path) != row.get("git_blob_sha"):
            errors.append(f"{round_id}: historical artifact changed")
        if row.get("preserved") is not True:
            errors.append(f"{round_id}: preserve flag")

    object_map = {
        "prediction_freeze": prediction,
        "pairwise_replay": pairwise,
        "postreveal_review": review,
        "generic_fix": generic_fix,
    }
    for key, obj in object_map.items():
        if manifest.get("artifacts", {}).get(key, {}).get("canonical_sha256") != obj.get("canonical_sha256"):
            errors.append(f"manifest artifact hash: {key}")

    manifest_stats = manifest.get("statistics", {})
    if manifest_stats.get("original_blind_baseline") != {"top1_hits": 11, "top2_coverage": 16, "status": "PRESERVED_NOT_OVERWRITTEN"}:
        errors.append("original blind baseline changed")
    if manifest_stats.get("r5", {}).get("top1_hits") != 14 or manifest_stats.get("r5", {}).get("top2_coverage") != 16:
        errors.append("manifest R5 score")
    for field in ("formal_valid_questions", "machine_valid_local_seals", "s03_fusions"):
        if manifest_stats.get(field) != 0:
            errors.append(f"{field} must remain zero")
    if manifest.get("new_case_admission") != "BLOCKED":
        errors.append("new-case gate")
    if manifest.get("status") != "FROZEN":
        errors.append("R5 freeze status")
    if manifest.get("s00_s19_modified") is not False or manifest.get("base_astrological_knowledge_changed") is not False:
        errors.append("manifest unauthorized knowledge change")

    return {
        "schema": "DEV-GROUP-002-R5-VALIDATION-V1",
        "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "question_count": 25,
        "pairwise_row_count": len(pairwise_rows),
        "postreveal_review_row_count": len(review_rows),
        "top1_hits": top1_hits,
        "top2_coverage": top2_coverage,
        "historical_rounds_preserved": ["R1", "R2", "R3", "R4"],
        "base_astrological_knowledge_changed": False,
        "s00_s19_modified": False,
        "new_case_admission": "BLOCKED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    if not args.write and not args.validate:
        parser.error("select --write and/or --validate")
    if args.write:
        materialize(repo_root)
    if args.validate:
        result = validate(repo_root)
        output_dir = repo_root / ROUND_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        write_json(output_dir / "validation.json", result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0 if result["status"] == "PASS" else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
