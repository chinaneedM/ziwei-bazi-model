import json
from pathlib import Path

from fortune_v1.training_corrected import advance_cycle, create_cycle, evaluate_question_training


def dump(path: Path, value):
    path.write_text(json.dumps(value), encoding="utf-8")


def base(tmp_path):
    cycle_path = tmp_path / "cycle.json"
    create_cycle(
        "CYCLE",
        "GROUP",
        [
            {"unit_id": "Q1", "question_ids": ["Q1"]},
            {"unit_id": "Q2", "question_ids": ["Q2"]},
        ],
        cycle_path,
    )
    evidence = {
        "schema": "QUESTION-TRAINING-EVIDENCE-V2.1",
        "cycle_id": "CYCLE",
        "unit_id": "Q1",
        "evidence_id": "E1",
        "first_blind_prediction": {
            "evaluation_role": "FIRST_BLIND_PREDICTION",
            "question_id": "Q1",
            "frozen_before_reveal": True,
            "answer_visible_during_prediction": False,
            "prediction_input_answer_free": True,
            "case_specific_rule_detected": False,
            "source_provenance_status": "PASS",
            "pairwise_replay_status": "PASS",
            "top1_correct": False,
            "top2_hit": True,
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


def test_wrong_first_blind_can_complete_training_after_reasoning_correction(tmp_path):
    cycle, evidence = base(tmp_path)
    result = evaluate_question_training(cycle, evidence, tmp_path / "evaluation.json")
    assert result["first_blind_prediction"]["top1_correct"] is False
    assert result["status"] == "TRAINING_UNIT_COMPLETE"
    assert result["unit_complete"] is True


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
