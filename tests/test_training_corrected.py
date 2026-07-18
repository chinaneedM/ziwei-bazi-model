import json
from pathlib import Path

from fortune_v1.training_corrected import advance_cycle, create_cycle, evaluate_question_training
from fortune_v1.util import canonical_bytes, sha256_bytes


def dump(path: Path, value):
    path.write_text(json.dumps(value), encoding="utf-8")


def with_hash(value):
    value = dict(value)
    value["object_hash"] = sha256_bytes(canonical_bytes(value))
    return value


def reasoning_object():
    return with_hash({
        "schema": "REASONING-CORRECTION-OBJECT-V2.1",
        "unit_id": "Q1",
        "error_mechanisms": [{"id": "E1", "mechanism": "scope error"}],
        "source_parent_chains": [{
            "library_id": "S02",
            "active_file_sha256": "a" * 64,
            "excerpt_sha256": "b" * 64,
            "line_ranges": ["1-2"],
            "knowledge_point": "family scope",
            "applicability_conditions": ["family-origin question"],
            "capability_ceiling": "SEMANTIC_DEFINITION_ONLY",
            "downstream_effect": "adult finance zeroed",
        }],
        "corrected_reasoning_order": ["scope", "entity", "evidence", "endpoint", "pairwise"],
        "capability_ceiling_and_no_overreach": ["resource channel is not wealth"],
        "applicability_conditions": ["family-origin question"],
        "counterexamples_and_failure_boundaries": ["adult wealth does not imply wealthy origin"],
        "option_semantics": [
            {"option_id": "A", "concept": "A"},
            {"option_id": "B", "concept": "B"},
            {"option_id": "C", "concept": "C"},
            {"option_id": "D", "concept": "D"},
        ],
        "pairwise_rows": [
            {"row_id": "AB", "left": "A", "right": "B", "direction": "RIGHT_AHEAD", "decisive_rule": "R", "reason": "r", "left_vector": {}, "right_vector": {}},
            {"row_id": "AC", "left": "A", "right": "C", "direction": "RIGHT_AHEAD", "decisive_rule": "R", "reason": "r", "left_vector": {}, "right_vector": {}},
            {"row_id": "AD", "left": "A", "right": "D", "direction": "LEFT_AHEAD", "decisive_rule": "R", "reason": "r", "left_vector": {}, "right_vector": {}},
            {"row_id": "BC", "left": "B", "right": "C", "direction": "LEFT_AHEAD", "decisive_rule": "R", "reason": "r", "left_vector": {}, "right_vector": {}},
            {"row_id": "BD", "left": "B", "right": "D", "direction": "LEFT_AHEAD", "decisive_rule": "R", "reason": "r", "left_vector": {}, "right_vector": {}},
            {"row_id": "CD", "left": "C", "right": "D", "direction": "LEFT_AHEAD", "decisive_rule": "R", "reason": "r", "left_vector": {}, "right_vector": {}},
        ],
        "strongest_competitor": {"relative_first": "B", "relative_second": "C", "pairwise_row_id": "BC"},
        "contamination_and_answer_memory_audit": {
            "original_first_blind_preserved": True,
            "post_reveal_replays_excluded_from_accuracy": True,
            "generic_rule_has_no_case_or_option_fixed_selection": True,
            "bazi_variant_not_selected_by_revealed_result": True,
            "base_knowledge_not_promoted_from_single_unit": True,
            "case_specific_rule_detected": False,
            "answer_memorization_rule_detected": False,
            "status": "PASS",
        },
        "training_unit_conclusion": {"status": "TRAINING_UNIT_COMPLETE_CANDIDATE"},
    })


def base(tmp_path):
    cycle_path = tmp_path / "cycle.json"
    create_cycle(
        "CYCLE",
        "GROUP",
        [
            {"unit_id": "CASE-1-Q1", "case_ids": ["CASE-1"], "question_ids": ["Q1"]},
            {"unit_id": "CASE-1-Q2", "case_ids": ["CASE-1"], "question_ids": ["Q2"]},
        ],
        cycle_path,
    )
    evidence = {
        "schema": "QUESTION-TRAINING-EVIDENCE-V2.1",
        "cycle_id": "CYCLE",
        "unit_id": "CASE-1-Q1",
        "evidence_id": "E1",
        "first_blind_prediction": {
            "evaluation_role": "FIRST_BLIND_PREDICTION",
            "case_id": "CASE-1",
            "question_id": "Q1",
            "frozen_before_reveal": True,
            "answer_visible_during_prediction": False,
            "prediction_input_answer_free": True,
            "case_specific_rule_detected": False,
            "source_provenance_status": "PASS",
            "pairwise_replay_status": "PASS",
            "top1_correct": False,
            "top2_hit": False,
            "prediction_freeze_hash": "abc",
        },
        "correction": {
            "error_diagnosis_complete": True,
            "reasoning_update_complete": True,
            "generic_method_candidate_recorded": True,
            "counterexample_tests_complete": True,
            "patch_validation_status": "PASS",
            "case_specific_rule_detected": False,
            "answer_memorization_rule_detected": False,
            "reasoning_correction_object": reasoning_object(),
        },
        "post_reveal_training_replays": [
            {
                "evaluation_role": "POST_REVEAL_TRAINING_REPLAY",
                "attempt_id": f"R{i}",
                "answer_visible_during_prediction": False,
                "prediction_input_answer_free": True,
                "case_specific_rule_detected": False,
                "source_provenance_status": "PASS",
                "pairwise_replay_status": "PASS",
                "matches_revealed_result": True,
            }
            for i in range(5)
        ],
        "prior_method_retention": {
            "prior_completed_unit_count": 0,
            "retention_rate": None,
        },
    }
    evidence_path = tmp_path / "evidence.json"
    dump(evidence_path, evidence)
    return cycle_path, evidence_path


def test_post_reveal_replays_do_not_create_blind_accuracy(tmp_path):
    cycle, evidence = base(tmp_path)
    result = evaluate_question_training(cycle, evidence, tmp_path / "evaluation.json")
    assert result["post_reveal_training_replay"]["post_reveal_fit_rate"] == 1.0
    assert result["post_reveal_training_replay"]["eligible_for_blind_accuracy"] is False
    assert result["rolling_first_blind_accuracy"]["distinct_question_count"] == 1
    assert result["rolling_first_blind_accuracy"]["top1_rate"] == 0.0
    assert result["rolling_first_blind_accuracy"]["top2_rate"] == 0.0


def test_wrong_first_blind_can_complete_training_after_reasoning_correction(tmp_path):
    cycle, evidence = base(tmp_path)
    result = evaluate_question_training(cycle, evidence, tmp_path / "evaluation.json")
    assert result["first_blind_prediction"]["top1_correct"] is False
    assert result["first_blind_prediction"]["top2_hit"] is False
    assert result["status"] == "TRAINING_UNIT_COMPLETE"
    assert result["unit_complete"] is True
    assert result["advance_allowed"] is True
    assert result["advance_executed"] is False


def test_rate_gate_not_evaluable_on_one_question(tmp_path):
    cycle, evidence = base(tmp_path)
    result = evaluate_question_training(cycle, evidence, tmp_path / "evaluation.json")
    assert result["rolling_first_blind_accuracy"]["status"] == "NOT_YET_EVALUABLE"
    assert result["rolling_first_blind_accuracy"]["rate_gate_evaluable"] is False


def test_advance_marks_training_complete_not_mastered(tmp_path):
    cycle, evidence = base(tmp_path)
    evaluation = tmp_path / "evaluation.json"
    evaluate_question_training(cycle, evidence, evaluation)
    result = advance_cycle(cycle, evaluation, tmp_path / "next.json")
    assert result["units"][0]["status"] == "TRAINING_UNIT_COMPLETE"
    assert "MASTERED" not in result["units"][0]["status"]
    assert result["current_unit_index"] == 1


def test_case_specific_rule_holds(tmp_path):
    cycle, evidence = base(tmp_path)
    data = json.loads(evidence.read_text())
    data["correction"]["case_specific_rule_detected"] = True
    evidence.unlink()
    dump(evidence, data)
    result = evaluate_question_training(cycle, evidence, tmp_path / "evaluation.json")
    assert result["status"] == "HOLD_ANSWER_OR_CASE_RULE_CONTAMINATION"


def test_reasoning_object_is_required(tmp_path):
    cycle, evidence = base(tmp_path)
    data = json.loads(evidence.read_text())
    del data["correction"]["reasoning_correction_object"]
    evidence.unlink()
    dump(evidence, data)
    result = evaluate_question_training(cycle, evidence, tmp_path / "evaluation.json")
    assert result["status"] == "CONTINUE_CURRENT_UNIT_TRAINING"
    assert "REASONING_CORRECTION_OBJECT_MISSING" in result["correction"]["reasons"]


def test_complete_pairwise_matrix_is_required(tmp_path):
    cycle, evidence = base(tmp_path)
    data = json.loads(evidence.read_text())
    obj = data["correction"]["reasoning_correction_object"]
    obj["pairwise_rows"].pop()
    obj.pop("object_hash")
    obj["object_hash"] = sha256_bytes(canonical_bytes(obj))
    evidence.unlink()
    dump(evidence, data)
    result = evaluate_question_training(cycle, evidence, tmp_path / "evaluation.json")
    assert result["status"] == "CONTINUE_CURRENT_UNIT_TRAINING"
    assert "PAIRWISE_ROW_COUNT_INCOMPLETE" in result["correction"]["reasons"]


def test_same_question_label_in_different_units_counts_as_distinct(tmp_path):
    cycle, evidence = base(tmp_path)
    first_eval = tmp_path / "first-eval.json"
    evaluate_question_training(cycle, evidence, first_eval)
    first_advanced = tmp_path / "first-advanced.json"
    advance_cycle(cycle, first_eval, first_advanced)

    cycle_data = json.loads(first_advanced.read_text())
    cycle_data["units"][1]["question_ids"] = ["Q1"]
    cycle_data.pop("object_hash")
    cycle_data["object_hash"] = sha256_bytes(canonical_bytes(cycle_data))
    dump(tmp_path / "second-cycle.json", cycle_data)

    evidence_data = json.loads(evidence.read_text())
    evidence_data["unit_id"] = "CASE-1-Q2"
    evidence_data["evidence_id"] = "E2"
    evidence_data["first_blind_prediction"]["question_id"] = "Q1"
    evidence_data["first_blind_prediction"]["case_id"] = "CASE-2"
    evidence_data["first_blind_prediction"]["prediction_freeze_hash"] = "def"
    dump(tmp_path / "second-evidence.json", evidence_data)

    result = evaluate_question_training(tmp_path / "second-cycle.json", tmp_path / "second-evidence.json", tmp_path / "second-eval.json")
    assert result["rolling_first_blind_accuracy"]["distinct_question_count"] == 2


def test_answer_memorization_audit_fails_closed(tmp_path):
    cycle, evidence = base(tmp_path)
    data = json.loads(evidence.read_text())
    obj = data["correction"]["reasoning_correction_object"]
    obj["contamination_and_answer_memory_audit"]["answer_memorization_rule_detected"] = True
    obj["contamination_and_answer_memory_audit"]["status"] = "FAIL"
    obj.pop("object_hash")
    obj["object_hash"] = sha256_bytes(canonical_bytes(obj))
    evidence.unlink()
    dump(evidence, data)
    result = evaluate_question_training(cycle, evidence, tmp_path / "evaluation.json")
    assert result["status"] == "HOLD_ANSWER_OR_CASE_RULE_CONTAMINATION"
