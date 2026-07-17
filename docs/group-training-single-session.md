# Group training in one CHAT/WORK session

## Authority and scope

This document defines the runtime correction for fixed development groups such as `DEV-GROUP-002`.
It changes orchestration granularity only. It does not change S00–S19 astrological knowledge, question semantics, evidence direction, pairwise adjudication, or case-specific outcome rules.

## Correct cold-start boundary

`CHAT_STATELESS_COLD_START` applies between training groups, not between cases inside one group.

One user instruction starts one `GROUP_SESSION_ID`. The active CHAT/WORK session may then retrieve and process every answer-free case in the group without asking the user to open a new conversation or send a per-case continue instruction.

## Runtime object

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

Each `CASE_RUN_ROW` must bind:

```text
CASE_ID
CASE_RUN_ID
PREDICTION_INPUT_SNAPSHOT_ID
CASE_WHITELIST_ID
ZIWEI_LOCAL_SEAL_ID
BAZI_LOCAL_SEAL_ID
S18_LOCAL_ADJUDICATION_OBJECT_IDS
PREDICTION_RUN_ID
CASE_FREEZE_STATUS
CASE_OBJECT_HASH
```

## Execution sequence

```text
GROUP_INPUT_FREEZE
→ CASE_1_BLIND_PREDICTION_AND_LOCAL_SEALS
→ CASE_2_BLIND_PREDICTION_AND_LOCAL_SEALS
→ CASE_3_BLIND_PREDICTION_AND_LOCAL_SEALS
→ CASE_4_BLIND_PREDICTION_AND_LOCAL_SEALS
→ CASE_5_BLIND_PREDICTION_AND_LOCAL_SEALS
→ GROUP_PREDICTION_FREEZE
→ GROUP_REVEAL
→ ANSWER_VECTOR_LITERAL_REPLAY_PER_CASE
→ GROUP_DIAGNOSIS
→ PATCH_CANDIDATE
→ CLEAN_GROUP_RERUN_WITH_NEW_IDS
→ REGRESSION_COMPARE
→ ACCEPT_OR_ROLLBACK
```

The case count is read from the frozen group manifest. Five is the current fixed development-group size, not a universal schema constant.

## Case isolation inside one session

The session may retain only group-level administrative state between cases:

- frozen S00–S19 bindings;
- main-prompt runtime ID;
- runtime code commit;
- group and case ordering;
- completion status and immutable object identifiers.

The following are forbidden inputs to a later case prediction:

- prior case TOP1 or TOP2 selections;
- prior case blind-model text or mechanism synthesis;
- prior case evidence direction or strongest competitor;
- prior case reveal, answer, score, error explanation, or shadow rebuild;
- case-specific patch rules.

Before each case, the executor must create a fresh case whitelist and verify that only the current answer-free `PREDICTION_INPUT_SNAPSHOT` is present.

## Group freeze and reveal

No answer for any group member may become visible until all expected cases have:

1. a complete `PREDICTION-RUN-V1` body;
2. two machine-valid independent local seals where applicable;
3. complete direction matrices and pairwise rows;
4. a non-overwriting case freeze receipt.

`GROUP_PREDICTION_FREEZE` passes only when every expected case row passes. Partial group freeze, missing case rows, duplicate case IDs, reused run IDs, or changed prediction bodies fail closed.

The answer vault performs one group-authorized reveal after the group freeze. Literal answer replay and grading remain per case and per question; the group layer only authorizes timing and aggregates results.

## Iterative training

A patch candidate may be produced only after the original group prediction is immutable and the group answer replay has passed. A candidate may repair reproducible execution, retrieval, semantic, entity, time, endpoint, independence, fusion, mapping, or release-interface defects.

It may not:

- overwrite the original prediction;
- add answer-direction rules for the five development cases;
- modify base astrological knowledge from a single group result;
- select a Bazi variant by outcome;
- inject answers, prior predictions, reveal explanations, or `SHADOW_REBUILD` into a clean rerun.

Every rerun uses a new `GROUP_RUN_ID` and new `CASE_RUN_ID` values. Acceptance requires the configured group policy to pass and no prohibited regression damage. Otherwise the candidate is rejected and the prior runtime commit remains authoritative.

## User interaction contract

A single user instruction such as:

> Continue the repository fixed five-case blind group training cycle.

is sufficient to start the whole group in the current session. The executor must not require five new conversations or five separate continue messages.

GitHub still does not autonomously wake ChatGPT after the response ends. “Autonomous group training” means that, once started by the user, the active session continuously performs the full group workflow without per-case intervention.

## Required validation tests

- later-case prediction cannot read earlier-case predictions;
- any answer visibility before group freeze fails the group;
- partial group freeze cannot authorize reveal;
- duplicate or reused group/case run IDs fail;
- changed frozen prediction body fails;
- patch files containing answer vectors, old selections, case-specific direction rules, or reveal text fail leak scanning;
- clean rerun uses new IDs and answer-free snapshots;
- rejection restores the previously authoritative runtime commit.
