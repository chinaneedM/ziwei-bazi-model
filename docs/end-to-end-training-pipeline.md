# End-to-end clean-blind training pipeline

This document defines the connected repository workflow from a fresh clean start through first-blind freeze, controlled reveal, and learning-cycle activation.

## State sequence

```text
GROUP-CLEAN-START-REQUEST-V2
  -> READY_FOR_PREBLIND_MODELING
  -> GROUP-RUNTIME-PACKET-REQUEST-V1
  -> staged PREBLIND packets and stage plans
  -> PREBLIND-TRACK-MODEL-V1 for Ziwei and Bazi
  -> GROUP-PREBLIND-SEAL-AND-RELEASE-REQUEST-V1
  -> machine-built PREBLIND-SEAL-BUNDLE-V1
  -> POSTBLIND_OPTION_CHALLENGE_RELEASED
  -> POSTBLIND-PREDICTION-BUNDLE-V1
  -> GROUP-PREDICTION-FREEZE-REQUEST-V1
  -> GROUP_PREDICTION_FREEZE_PASS
  -> GROUP-REVEAL-TRAINING-REQUEST-V1
  -> ANSWER-VECTOR-LITERAL-REPLAY-V1
  -> LEARNING-CYCLE-V2.1 / LEARNING_ACTIVE
```

No reveal workflow may check out the answer vault before `GROUP_PREDICTION_FREEZE_PASS` is verified.

## 1. Staged runtime-packet request

Path:

```text
runtime/runtime-packet-requests/<GROUP_RUN_ID>.json
```

The existing `GROUP-RUNTIME-PACKET-REQUEST-V1` fields remain authoritative. The workflow now invokes `create-staged-group-runtime-packets.py`, requires `READY_FOR_PREBLIND_MODELING`, removes option-aware source packets from the PREBLIND transport allowlist, and creates one `stage-access-plan.json` per case.

## 2. Preblind model objects

Each question has two independent model files:

```text
data/group-clean-starts/<GROUP_RUN_ID>/preblind-models/<CASE_ID>/<QUESTION_ID>-ziwei.json
data/group-clean-starts/<GROUP_RUN_ID>/preblind-models/<CASE_ID>/<QUESTION_ID>-bazi.json
```

Required shape:

```json
{
  "schema": "PREBLIND-TRACK-MODEL-V1",
  "status": "READY_FOR_SEAL",
  "case_id": "DEV-EXAMPLE-001",
  "run_id": "<CASE_RUN_ID>",
  "group_run_id": "<GROUP_RUN_ID>",
  "question_id": "Q1",
  "track": "ziwei",
  "answer_data_available": false,
  "option_visibility": "WITHHELD",
  "option_accessed": false,
  "blind_axis_model": {},
  "complete_knowledge_coverage_plan": {"status": "PASS"},
  "source_route_plan": []
}
```

The Bazi file uses `track=bazi` and must be independently produced. Identical Ziwei/Bazi file hashes fail the independence gate.

## 3. Machine seal and option release request

Path:

```text
runtime/preblind-seal-requests/<GROUP_RUN_ID>.json
```

Schema:

```json
{
  "schema": "GROUP-PREBLIND-SEAL-AND-RELEASE-REQUEST-V1",
  "status": "REQUESTED",
  "group_run_id": "<GROUP_RUN_ID>",
  "clean_start_path": "data/group-clean-starts/<GROUP_RUN_ID>/clean-start.json",
  "output_root": "data/group-clean-starts/<GROUP_RUN_ID>",
  "case_model_submissions": [
    {
      "case_id": "DEV-EXAMPLE-001",
      "stage_plan_path": "data/group-clean-starts/<GROUP_RUN_ID>/runtime-packets/DEV-EXAMPLE-001/stage-access-plan.json",
      "questions": [
        {
          "question_id": "Q1",
          "ziwei_model_path": "data/group-clean-starts/<GROUP_RUN_ID>/preblind-models/DEV-EXAMPLE-001/Q1-ziwei.json",
          "bazi_model_path": "data/group-clean-starts/<GROUP_RUN_ID>/preblind-models/DEV-EXAMPLE-001/Q1-bazi.json"
        }
      ]
    }
  ]
}
```

The repository computes the raw-file SHA-256 for each model and a canonical seal hash. The model does not self-certify its hash. Only after all cases and questions pass does the workflow create `POSTBLIND-ACCESS-RECEIPT-V1` objects.

## 4. Postblind prediction and group freeze

One prediction bundle is written per case:

```text
data/group-clean-starts/<GROUP_RUN_ID>/postblind-predictions/<CASE_ID>.json
```

It must use `POSTBLIND-PREDICTION-BUNDLE-V1`, preserve answer invisibility, contain TOP1/TOP2, track conclusions, coverage and provenance statuses, evidence-usage ledger rows, all `N*(N-1)/2` pairwise rows, and a mechanically derived strongest competitor.

Freeze request path:

```text
runtime/group-freeze-requests/<GROUP_RUN_ID>.json
```

The request must bind exactly:

```json
{
  "schema": "GROUP-PREDICTION-FREEZE-REQUEST-V1",
  "status": "REQUESTED",
  "group_run_id": "<GROUP_RUN_ID>",
  "group_postblind_access_path": "data/group-clean-starts/<GROUP_RUN_ID>/group-postblind-access.json",
  "output_root": "data/group-clean-starts/<GROUP_RUN_ID>",
  "case_prediction_bundles": [
    {
      "case_id": "DEV-EXAMPLE-001",
      "prediction_bundle_path": "data/group-clean-starts/<GROUP_RUN_ID>/postblind-predictions/DEV-EXAMPLE-001.json"
    }
  ]
}
```

The workflow rejects missing or duplicate pairs, invalid direction vectors, TOP1/TOP2 not derived from the pairwise matrix, incomplete coverage/provenance, or any answer visibility.

## 5. Controlled reveal and training activation

The repository secret `FORTUNE_ANSWER_VAULT_TOKEN` must grant read-only access to `chinaneedM/fortune-answer-vault`.

Reveal request path:

```text
runtime/group-reveal-requests/<GROUP_RUN_ID>.json
```

Schema:

```json
{
  "schema": "GROUP-REVEAL-TRAINING-REQUEST-V1",
  "status": "REQUESTED",
  "group_run_id": "<GROUP_RUN_ID>",
  "group_prediction_freeze_path": "data/group-clean-starts/<GROUP_RUN_ID>/group-prediction-freeze.json",
  "answer_vector_path": "<ANSWER-VAULT-RELATIVE-PATH>.json",
  "output_root": "data/group-clean-starts/<GROUP_RUN_ID>/training",
  "cycle_id": "CYCLE-<GROUP_RUN_ID>",
  "main_prompt_runtime_id": "MP-PROFESSIONAL-REASONING-20260718-R17",
  "knowledge_release_id": "KNOWLEDGE-R17",
  "method_release_id": "METHOD-R17",
  "model_release_id": "MODEL-R17-REPOSITORY-ACTIVE-V1"
}
```

The answer vector must use `GROUP-ANSWER-VECTOR-V1`, include the original raw answer string, Unicode codepoints, character offsets, ordered case/question rows, and exact answer option IDs. Two independent literal parsers must agree before scoring.

The output creates:

- `answer-vector-literal-replay.json`;
- `learning-unit-plan.json`;
- `learning-cycle.json`;
- one answer-memory-safe training evidence seed per question;
- `group-training-intake.json` with `status=LEARNING_ACTIVE`.

Reasoning correction, stability replays, evaluation, and advancement continue through the existing `fortune-learning-cycle` commands. Post-reveal replays never count as additional blind-accuracy observations.

## Operational boundary

Component installation is not equivalent to end-to-end readiness. `INSTALLED_VALIDATED` may be restored only after:

1. the new unit tests pass;
2. all workflow files parse and are bound to the staged scripts;
3. a synthetic answer-free run reaches group freeze;
4. a separate synthetic reveal reaches `LEARNING_ACTIVE`;
5. the immutable installation receipt records those results.
