# FORTUNE-V1-SEMI-AUTOMATED-R1

This layer separates professional reasoning from mechanical runtime work without requiring a paid model API.

## Responsibility split

- **WORK** builds and repairs code, schemas, validators, and releases.
- **CHAT** performs only bounded professional Ziwei/Bazi reasoning.
- **Python/GitHub** performs path validation, answer isolation checks, hashing, pairwise materialization, validation, freezing prerequisites, and later scoring.

CHAT must not search the repository during a prediction run. It receives one generated `CHAT-PROFESSIONAL-PACKET-V1` per case and returns `CHAT-PROFESSIONAL-OUTPUT-V1`.

## Commands

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

R1 implements packet preparation, simplified professional output validation, pairwise materialization, and visibility classification. Prediction freeze and reveal/score remain separate so answer-bearing data cannot enter the prediction-side package.
