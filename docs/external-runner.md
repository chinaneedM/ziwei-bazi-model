# CHAT/WORK prediction runner

## Execution model

The prediction engine is the active ChatGPT project session operating in either `CHAT_ONLY` or `WORK` mode. No OpenAI API key, third-party model endpoint, paid server, or background process is required.

The division of responsibility is:

- ChatGPT `CHAT_ONLY` / `WORK`: performs the Ziwei and Bazi reasoning and emits complete `PREDICTION-RUN-V1` child objects.
- GitHub runtime: freezes inputs, validates bindings and object bodies, rejects answer contamination, enforces independent local seals and pairwise completeness, freezes predictions, and manages group reveal/regression receipts.
- Answer vault: remains physically separate and is read only by the reverse-grading workflow after a valid group freeze exists.

GitHub does not autonomously start a ChatGPT conversation. The user starts one training-group session in CHAT or WORK. `CHAT_STATELESS_COLD_START` applies between groups, not between cases inside one frozen group. After that single start, the active session may process every answer-free case in the group without requiring a new conversation or a per-case continue message.

## Single-case repository handoff

The legacy deterministic adapter remains available:

```bash
fortune-v1 chat-work-import \
  --run data/chat-work-submissions/<run-id>.json \
  --contract data/contracts/<run-id>.json \
  --mode CHAT_ONLY \
  --session-id <non-secret-session-label> \
  --output data/chat-work-imports/<run-id>/prediction-run.json \
  --receipt data/chat-work-imports/<run-id>/handoff-receipt.json
```

It requires `answer_data_available=false`, scans the submitted prediction for forbidden answer material, validates the entire `PREDICTION-RUN-V1` body, verifies the Ziwei/Bazi independent local seals, and writes nothing when validation fails.

## Group-level single-session handoff

The preferred development-training adapter is:

```bash
fortune-v1 group-chat-work-run \
  --manifest data/group-submissions/<group-run-id>.json \
  --group-root data/dev-groups/<group-id> \
  --output-root data/group-runs \
  --mode CHAT_ONLY \
  --session-id <non-secret-session-label> \
  --group-run-id <new-group-run-id>
```

The manifest uses `GROUP-TRAINING-RUN-V1` and contains an ordered child row for every frozen group member. The adapter requires:

- the exact group case order and complete case count;
- one unique, non-overwriting `CASE_RUN_ID` per case;
- a common `GROUP_SESSION_ID` and session mode;
- an answer-free run contract and prediction object for every case;
- the frozen group binding on every child;
- no prior-case prediction, reveal, diagnosis, or shadow-rebuild references.

It imports and freezes every child, then writes one immutable `GROUP-PREDICTION-FREEZE-V1` object. Partial group submissions, duplicate IDs, changed child objects, cross-case references, answer contamination, or a reused group-run path fail closed.

Validation is exposed as:

```bash
fortune-v1 group-verify-freeze \
  --group-freeze data/group-runs/<group-run-id>/group-freeze.json \
  --group-run-id <group-run-id> \
  --output reports/group-freeze-validation.json
```

No answer reveal may be authorized until this validation passes for the complete group.

## Workflows

The workflow `.github/workflows/external-runner-smoke.yml` is named `chat-work-handoff` in GitHub Actions. It validates committed CHAT/WORK prediction objects and persists handoff and freeze receipts before reveal.

The group-level command adds deterministic batch orchestration around those same child validators. A later workflow may automate command dispatch, but workflow automation is not allowed to weaken group freeze, answer isolation, or run non-overwrite gates.

## Installation meaning

`EXTERNAL_PREDICTION_RUNNER=INSTALLED` means the CHAT/WORK project-session handoff contract and deterministic validator are installed. It does not mean GitHub can run ChatGPT in the background, and it does not claim an API service exists.

For group training, one real frozen group requires one user-initiated CHAT or WORK session. The group may contain five cases and 25 questions, all processed continuously inside that session. A separate conversation for every case is neither required nor the intended operating model.
