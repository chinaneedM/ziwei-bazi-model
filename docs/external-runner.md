# CHAT/WORK prediction runner

## Execution model

The prediction engine is the active ChatGPT project session operating in either `CHAT_ONLY` or `WORK` mode. No OpenAI API key, third-party model endpoint, paid server, or background process is required.

The division of responsibility is:

- ChatGPT `CHAT_ONLY` / `WORK`: performs the Ziwei and Bazi reasoning and emits the complete `PREDICTION-RUN-V1` object.
- GitHub runtime: freezes inputs, validates bindings and object bodies, rejects answer contamination, enforces independent local seals and pairwise completeness, freezes the prediction, and manages reveal/regression receipts.
- Answer vault: remains physically separate and is read only by the reverse-grading workflow after a valid freeze receipt exists.

GitHub does not autonomously start a ChatGPT conversation. Each case is user-initiated in CHAT or WORK, consistent with the project's `CHAT_STATELESS_COLD_START` and `CHAT_ONLY` operating model.

## Repository handoff

The deterministic handoff adapter is exposed as:

```bash
fortune-v1 chat-work-import \
  --run data/chat-work-submissions/<run-id>.json \
  --contract data/contracts/<run-id>.json \
  --mode CHAT_ONLY \
  --session-id <non-secret-session-label> \
  --output data/chat-work-imports/<run-id>/prediction-run.json \
  --receipt data/chat-work-imports/<run-id>/handoff-receipt.json
```

The adapter requires `answer_data_available=false`, scans the submitted prediction for forbidden answer material, validates the entire `PREDICTION-RUN-V1` body, verifies the Ziwei/Bazi independent local seals, and writes nothing when validation fails.

The workflow `.github/workflows/external-runner-smoke.yml` is named `chat-work-handoff` in GitHub Actions. It validates the committed CHAT/WORK prediction object, freezes it under a new non-overwriting `RUN_ID`, and persists the handoff and freeze receipts before reveal.

## Installation meaning

`EXTERNAL_PREDICTION_RUNNER=INSTALLED` means the CHAT/WORK project-session handoff contract and deterministic validator are installed. It does not mean GitHub can run ChatGPT in the background, and it does not claim an API service exists.

Every real case still requires a new user-initiated CHAT or WORK conversation. Once the model emits the prediction, the remaining validation, freeze, reveal, scoring, diagnosis, and regression operations can be handled through the repository workflow.
