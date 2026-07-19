# Group training in one CHAT/WORK session

## Authority and scope

This document defines orchestration for fixed development groups such as `DEV-GROUP-002`.

It preserves S00–S19 provenance, blind prediction isolation, literal answer replay and immutable prediction objects. It also defines the corrected learning objective: revealed development cases are repeatedly studied until they reach configured mastery. General methods and source knowledge may be revised through controlled candidates; case-specific outcome rules remain forbidden.

## Correct cold-start boundary

`CHAT_STATELESS_COLD_START` applies between training groups, not between cases inside one group.

One user instruction starts one `GROUP_SESSION_ID`. The active CHAT/WORK session may process every answer-free case in the group without requiring a new conversation or per-case continue instruction.

Within a revealed training cycle, each replay attempt still receives a fresh run ID and an answer-free prediction input. Old selections, old error explanations and reveal payloads are not prediction inputs.

## Runtime objects

The original group object remains:

```text
SCHEMA=GROUP-TRAINING-RUN-V1
GROUP_SESSION_ID
GROUP_RUN_ID
GROUP_ID
EXPECTED_CASE_COUNT
EXPECTED_QUESTION_COUNT
SOURCE_BASELINE_COMMIT
RUNTIME_CODE_COMMIT
MAIN_PROMPT_RUNTIME_ID
CASE_RUN_ROWS
GROUP_FREEZE_STATUS
ANSWER_VISIBILITY_STATUS
REVEAL_STATUS
DIAGNOSIS_STATUS
PATCH_CANDIDATE_STATUS
REGRESSION_STATUS
FINAL_DECISION
OBJECT_HASH
```

Mastery training adds:

```text
SCHEMA=LEARNING-CYCLE-V2
CYCLE_ID
GROUP_ID
UNIT_MODE
UNITS
CURRENT_UNIT_INDEX
THRESHOLDS
MASTERED_UNITS
HISTORY
STATUS
GENERALIZATION_STATUS
OBJECT_HASH
```

Each `CASE_RUN_ROW` continues to bind the case snapshot, whitelists, local seals, S18 adjudication objects, prediction run and immutable hashes.

## Baseline freeze and first reveal

The first group execution remains:

```text
GROUP_INPUT_FREEZE
→ CASE_1_BLIND_PREDICTION_AND_LOCAL_SEALS
→ ...
→ CASE_N_BLIND_PREDICTION_AND_LOCAL_SEALS
→ GROUP_PREDICTION_FREEZE
→ GROUP_REVEAL
→ ANSWER_VECTOR_LITERAL_REPLAY_PER_CASE
```

No group answer may become visible until all expected baseline case runs are frozen and validated.

## Corrected iterative learning

After reveal, the active sequence is:

```text
ABSORB
→ DECOMPOSE
→ FILL
→ RESHAPE
→ APPLY_WITH_CLEAN_COLD_START
→ MASTERY_AND_RETENTION_EVALUATION
→ either repeat learning or advance unit
→ GENERATE_UNSEEN_BLIND_TEST after all units are mastered
```

The answer is allowed in diagnosis after immutable freeze. It is forbidden in prediction, clean replay, patch direction logic and variant selection.

## Training unit granularity

The cycle can run in three modes:

- `QUESTION`: one question at a time;
- `CASE`: one case at a time;
- `GROUP`: the complete group.

`DEV-GROUP-002` defaults to `QUESTION` mode when full-group work is too large. The frozen order is preserved. A later question cannot begin until the active question passes its mastery and retention gates.

Default question gate:

- five clean cold-start attempts;
- TOP1 at least 80%;
- TOP2 at least 90%;
- source provenance and pairwise replay PASS;
- no case-specific direction rule;
- previously mastered units remain at least 80%.

## What learning may change

A general candidate may revise:

- retrieval and source routing;
- literal semantics and atom decomposition;
- entity and person-Taiji mapping;
- neutral time, occurrence and duration logic;
- real-world endpoint chains;
- pairwise adjudication;
- two-track independence and fusion;
- method rules;
- source knowledge under stronger review.

A method candidate may originate from one wrong question if it is expressed as a general mechanism with explicit conditions and counterexamples.

A base-knowledge promotion requires at least two independent source parents and reproduction in two distinct training units. Before that it remains a research candidate.

## Forbidden learning shortcuts

The following remain illegal:

- overwrite a frozen prediction;
- encode a case ID, question ID, answer letter or exact fingerprint as a decision rule;
- choose a Bazi variant because it matches the known result;
- pass old selections, reveal explanations or shadow rebuild text to a clean replay;
- call training mastery blind accuracy;
- claim unseen generalization before a frozen unseen block.

## Retention and regression

A candidate is evaluated on the active unit and all previously mastered units.

- Active unit below target: continue learning.
- Prior unit below retention target: reshape or repair the candidate.
- No improvement in repeated rounds: return to decomposition; do not stop automatically.
- Base knowledge needed: enter knowledge review; do not stop automatically.
- Case-specific rule or prediction contamination: HOLD.
- Invalid source or pairwise provenance: HOLD.

There is no arbitrary maximum of five rounds, no maximum same-defect retry count and no stop after two zero-improvement rounds.

## State transitions

```text
LEARNING_ACTIVE
  ├─ active unit below target     → LEARNING_ACTIVE
  ├─ prior-unit regression        → REGRESSION_REPAIR_REQUIRED
  ├─ method stagnation            → METHOD_RETHINK_REQUIRED
  ├─ knowledge candidate needed   → KNOWLEDGE_REVIEW_REQUIRED
  ├─ contamination                → GROUP_HOLD
  ├─ current unit mastered        → next unit
  ├─ all units complete, rate pass → TRAINING_SET_COMPLETE_AWAITING_UNSEEN_BLIND_TEST
  └─ all units complete, rate low  → TRAINING_SET_COMPLETE_BELOW_ROLLING_TARGET_REQUIRES_RESHAPING
```

## User interaction contract

One user instruction is enough to start or continue the current cycle. GitHub does not wake ChatGPT autonomously after a response, but the active response should perform the complete available learning step without asking for per-case confirmation.

## Required validation tests

- reveal is impossible before the baseline group freeze;
- clean replay cannot read answer payloads, old predictions or old error explanations;
- case-specific direction rules are rejected;
- a question reaches mastery only after the required clean attempts and rate threshold;
- previously mastered questions are replayed and retained;
- arbitrary round counts do not force HOLD;
- base-knowledge candidates require independent sources and multi-unit reproduction;
- training mastery remains explicitly separate from unseen generalization;
- frozen prediction objects remain immutable throughout learning.
