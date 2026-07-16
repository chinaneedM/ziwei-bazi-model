# External prediction runner

## Installed repository-side components

The runtime repository now contains a fail-closed HTTP adapter at `fortune_v1.external_runner`, exposed as:

```bash
fortune-v1 external-run \
  --snapshot data/snapshots/<snapshot-id>/manifest.json \
  --contract data/contracts/<run-id>.json \
  --endpoint "$PREDICTION_RUNNER_ENDPOINT" \
  --runner-id FORTUNE-EXTERNAL-DUAL-TRACK-V1 \
  --output data/runner-probes/<run-id>/prediction-run.json \
  --receipt data/runner-probes/<run-id>/external-runner-receipt.json
```

The adapter sends only the frozen no-answer snapshot, immutable run contract, question set and repository bindings. It rejects a contract that does not declare `answer_data_available=false`, rejects a snapshot without a passing answer scan, scans the outbound request for forbidden answer material, never persists the bearer token, and writes no prediction object unless the returned `PREDICTION-RUN-V1` passes the complete local validator.

The manual workflow `.github/workflows/external-runner-smoke.yml` performs the live activation probe, validates a fresh non-overwriting `RUN_ID`, invokes the remote executor, freezes the validated prediction and emits machine receipts.

## Deliberately unresolved external dependency

`config/external-runner.json` remains:

```text
EXTERNAL_PREDICTION_RUNNER_STATUS=NOT_INSTALLED
```

This is intentional. The repository adapter is installed, but a real separate model/executor endpoint has not yet been bound and tested on a fresh unrevealed DEV case. ChatGPT conversation state, schemas, fixtures and locally manufactured JSON do not satisfy this gate.

Activation requires all of the following in one live run:

1. A separately hosted dual-track prediction executor is bound through `PREDICTION_RUNNER_ENDPOINT`.
2. The executor has no answer-vault credential or answer path.
3. Its response passes `PREDICTION-RUN-V1` validation, complete pairwise coverage and independent Ziwei/Bazi local seals.
4. The resulting prediction is frozen under a new `RUN_ID` before any reveal.
5. The live receipt is written back to `config/external-runner.json` and the final `make install-check` returns `INSTALL_VALIDATION_CANDIDATE`.

Until those facts exist, the formal installation status must remain `SCHEMA_DEFINED_NOT_INSTALLED`.
