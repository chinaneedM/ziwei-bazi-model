# FORTUNE-V1-SEMI-AUTOMATED-R1

This layer separates professional reasoning from mechanical runtime work without requiring a paid model API.

## Responsibility split

- **WORK** builds and repairs code, schemas, validators, and releases.
- **CHAT** performs only bounded professional Ziwei/Bazi reasoning.
- **Python/GitHub** performs path validation, answer isolation checks, hashing, pairwise materialization, validation, repair scoping, and prediction freezing.

CHAT must not search the repository during a prediction run. It receives one generated `CHAT-PROFESSIONAL-PACKET-V1` per case and returns `CHAT-PROFESSIONAL-OUTPUT-V1`.

## Prediction-side commands

Prepare packets from an already generated clean start:

```bash
python scripts/semi-automated-r1.py prepare \
  --clean-start data/group-clean-starts/<group-run-id>/clean-start.json \
  --output-root data/chat-professional-packets
```

Validate one CHAT result and mechanically generate all pairwise rows:

```bash
python scripts/semi-automated-r1.py validate \
  --packet data/chat-professional-packets/<group-run-id>/<case>.chat-packet.json \
  --chat-output data/chat-professional-outputs/<group-run-id>/<case>.json \
  --validated-output data/validated-professional-outputs/<group-run-id>/<case>.json
```

Classify a visibility event:

```bash
python scripts/semi-automated-r1.py classify-visibility --operation-attempted
```

An attempted operation with no returned content is recorded but is not contamination. Actual forbidden-content visibility is fail-closed. Answer-bearing visibility is always fail-closed.

Create a local repair receipt from a case validation report:

```bash
python scripts/prediction-freeze-r1.py repair-receipt \
  --validation-report data/chat-validation/<case>.json \
  --output data/chat-repairs/<case>.json
```

A normal schema or reasoning omission is `LOCAL_NODE_REPAIR_ALLOWED`. It does not discard already valid upstream nodes. Only confirmed contamination requires a fresh run.

Freeze one case after validation passes:

```bash
python scripts/prediction-freeze-r1.py freeze-case \
  --validated-output data/validated-professional-outputs/<group-run-id>/<case>.json \
  --output data/case-prediction-freezes/<group-run-id>/<case>.json
```

Validate the complete group by supplying every case report and validated output:

```bash
python scripts/prediction-freeze-r1.py validate-group \
  --packet-manifest data/chat-professional-packets/<group-run-id>/manifest.json \
  --validation-report data/chat-validation/<case-1>.json \
  --validation-report data/chat-validation/<case-2>.json \
  --validated-output data/validated-professional-outputs/<group-run-id>/<case-1>.json \
  --validated-output data/validated-professional-outputs/<group-run-id>/<case-2>.json \
  --output data/group-validation/<group-run-id>.json
```

Freeze the group only after all expected cases pass and the case set matches exactly:

```bash
python scripts/prediction-freeze-r1.py freeze-group \
  --group-validation data/group-validation/<group-run-id>.json \
  --case-freeze data/case-prediction-freezes/<group-run-id>/<case-1>.json \
  --case-freeze data/case-prediction-freezes/<group-run-id>/<case-2>.json \
  --output-root data/group-prediction-freezes
```

The resulting `GROUP-PREDICTION-FREEZE-V1` is the first artifact that may authorize a separate reveal-side process. It does not itself reveal, score, diagnose, or rebuild anything. Prediction-side code never opens an answer vault.

## Artifact binding guarantees

Before group freeze, the runtime verifies all of the following:

- packet manifest schema, ready status, case count, and unique case IDs
- each validated output belongs to the manifest `group_run_id`
- each validation report points to the exact validated-output path and SHA-256
- report and validated-output statuses agree
- duplicate validation reports or duplicate validated outputs are rejected
- each case freeze belongs to the same `group_run_id`
- each case freeze preserves the validated-output SHA-256 approved by group validation
- the complete case-freeze set exactly matches the validated group case set
- case and group freeze files are created non-overwriting and marked read-only after creation

Read-only mode is an operational safeguard, not a substitute for hashes. The authoritative integrity proof remains the stored source and freeze SHA-256 chain.

## Nine-node execution model

1. `01_INPUT_FREEZE`
2. `02_QUESTION_SEMANTICS`
3. `03_ZIWEI_BLIND_MODEL`
4. `04_BAZI_BLIND_MODEL`
5. `05_SOURCE_CALL_LEDGER`
6. `06_REALITY_CHAIN`
7. `07_DIRECTION_MATRIX`
8. `08_PAIRWISE_SELECTION`
9. `09_LOCAL_SEAL_AND_FUSION`

## Current R1 boundary

Implemented:

- clean CHAT packet preparation
- simplified professional reasoning output validation
- complete pairwise materialization
- visibility-event classification
- local repair receipts
- immutable case freeze
- complete-group validation
- immutable group freeze
- cross-group rejection
- report/output hash binding
- duplicate artifact rejection

Not implemented in this prediction-side branch:

- answer-vault access
- reveal
- scoring
- diagnosis
- `SHADOW_REBUILD`
- automatic prompt or knowledge-base modification

Those functions must remain in a separate reveal-side implementation so prediction context cannot inherit answer-bearing data.

## Release condition

The repository test suite, group fail-closed checks, command registration checks, and synthetic end-to-end dry run must all pass on the final code head. The fixed five development cases should run only after those checks pass and this prediction-side pull request is merged or explicitly selected as the frozen run commit.
