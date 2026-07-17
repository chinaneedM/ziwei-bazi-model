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

R1 now implements packet preparation, simplified professional output validation, pairwise materialization, visibility classification, local repair scoping, case freeze, complete-group validation, and immutable group freeze. Reveal, scoring, diagnosis, and `SHADOW_REBUILD` remain outside the prediction-side package and require a separate future implementation.
