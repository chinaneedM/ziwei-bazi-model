# End-to-end clean-blind training pipeline

This document defines the connected public-repository workflow from a fresh clean start through first-blind freeze, controlled reveal, and learning-cycle activation.

## Public-only repository policy

The runtime uses one public GitHub repository only. It must not clone, fetch, call, or depend on any private repository.

Answer isolation is provided by encrypted answer envelopes stored in the same public repository:

```text
public-answer-vault/encrypted/<GROUP_RUN_ID>.json.fernet
```

The ciphertext is public. The symmetric decryption key is held only in the repository Actions secret `FORTUNE_PUBLIC_ANSWER_KEY`. A GitHub Actions secret is not a repository and does not require a private repository. Decrypted answer plaintext exists only in a transient runner path under `/tmp`, after group-freeze validation, and is destroyed before the job finishes.

The reveal workflow is intentionally limited to `push` and `workflow_dispatch`. It does not run for pull requests, so public fork PRs cannot access the answer key.

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
  -> decrypt PUBLIC-ENCRYPTED-ANSWER-VECTOR-V1 in runner /tmp
  -> GROUP-REVEAL-TRAINING-REQUEST-V1
  -> ANSWER-VECTOR-LITERAL-REPLAY-V1
  -> LEARNING-CYCLE-V2.1 / LEARNING_ACTIVE
```

No reveal workflow may decrypt an answer envelope before `GROUP_PREDICTION_FREEZE_PASS` is verified.

## 1. Staged runtime-packet request

Path:

```text
runtime/runtime-packet-requests/<GROUP_RUN_ID>.json
```

The existing `GROUP-RUNTIME-PACKET-REQUEST-V1` fields remain authoritative. The workflow invokes `create-staged-group-runtime-packets.py`, requires `READY_FOR_PREBLIND_MODELING`, removes option-aware source packets from the PREBLIND transport allowlist, and creates one `stage-access-plan.json` per case.

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

## 5. Prepare a public encrypted answer envelope

Generate a Fernet key once and save it as the repository Actions secret `FORTUNE_PUBLIC_ANSWER_KEY`:

```bash
fortune-public-answer-vault generate-key
```

Do not commit the generated key. Keep the plaintext answer vector outside the repository, then encrypt it into the public repository:

```bash
export FORTUNE_PUBLIC_ANSWER_KEY='<secret value>'
fortune-public-answer-vault encrypt \
  --answer /secure-local-path/<GROUP_RUN_ID>.json \
  --envelope public-answer-vault/encrypted/<GROUP_RUN_ID>.json.fernet
```

The plaintext input must use `GROUP-ANSWER-VECTOR-V1`, include `group_run_id`, the original raw answer string, Unicode codepoints, character offsets, ordered case/question rows, and exact answer option IDs. Only the encrypted envelope is committed.

## 6. Controlled reveal and training activation

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
  "encrypted_answer_envelope_path": "public-answer-vault/encrypted/<GROUP_RUN_ID>.json.fernet",
  "output_root": "data/group-clean-starts/<GROUP_RUN_ID>/training",
  "cycle_id": "CYCLE-<GROUP_RUN_ID>",
  "main_prompt_runtime_id": "MP-PROFESSIONAL-REASONING-20260718-R17",
  "knowledge_release_id": "KNOWLEDGE-R17",
  "method_release_id": "METHOD-R17",
  "model_release_id": "MODEL-R17-REPOSITORY-ACTIVE-V1"
}
```

The workflow first validates the immutable group freeze and the encrypted envelope identity. It then decrypts the answer vector into `/tmp/fortune-public-answer-vault`, performs two independent literal parsers, creates the training objects, and destroys the transient plaintext.

The output creates:

- `answer-vector-literal-replay.json`;
- `learning-unit-plan.json`;
- `learning-cycle.json`;
- one answer-memory-safe training evidence seed per question;
- `group-training-intake.json` with `status=LEARNING_ACTIVE`.

Reasoning correction, stability replays, evaluation, and advancement continue through the existing `fortune-learning-cycle` commands. Post-reveal replays never count as additional blind-accuracy observations.

## Public-repository security boundaries

- No private repository or cross-repository token is used.
- The encrypted answer envelope may be public; the decryption key must never be committed.
- Pull-request workflows never receive `FORTUNE_PUBLIC_ANSWER_KEY`.
- Decryption is blocked before group freeze.
- Decrypted plaintext is forbidden inside the repository tree.
- Runtime retrieval remains exact-path-only and must not search historical revealed runs.
- A public repository makes source files, code, encrypted envelopes, and post-reveal training objects visible to everyone. Only material legally and operationally suitable for public release may be committed.

## Operational boundary

Component installation is not equivalent to end-to-end readiness. `INSTALLED_VALIDATED` may be restored only after:

1. the unit tests pass, including public answer-vault tests;
2. all workflow files parse and are bound to the staged scripts;
3. a synthetic answer-free run reaches group freeze;
4. a separate synthetic public-envelope reveal reaches `LEARNING_ACTIVE`;
5. no private-repository or private-token reference remains in the active runtime;
6. the immutable installation receipt records those results;
7. repository metadata confirms `visibility=public`.
