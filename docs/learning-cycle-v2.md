# Learning Cycle V2.1 — first-blind-only scoring correction

## Objective

The revealed development examples are training material. Their purpose is to expose why a prediction was wrong, correct the reasoning mechanism, and test whether that correction improves later first-time predictions. The system must learn from an error without pretending that a post-reveal replay is a new blind prediction.

Core sequence:

> 汲取 → 拆解 → 填充 → 重塑 → 化用 → 生发

Machine names:

> ABSORB → DECOMPOSE → FILL → RESHAPE → APPLY → GENERATE

## Four separate claims

- **First-blind accuracy:** one immutable pre-reveal prediction for each distinct question.
- **Post-reveal training fit:** whether the corrected method can reproduce the revealed result on the training question.
- **Replay stability:** whether the corrected method is reproducible under clean input and order perturbations.
- **Unseen generalization:** performance on a later frozen block never used to create or revise the method.

These claims must never be substituted for one another. Five replays of one revealed question are five stability observations but only zero additional blind-accuracy observations.

A distinct question is identified by an explicit `distinct_question_key`, normally the question-unit ID or the case ID plus question ID. A bare label such as `Q1` is not globally unique because multiple cases may each contain a question named `Q1`.

## Why an incorrect answer is useful

A wrong first prediction is not erased. It is the training signal. Post-reveal work must identify the faulty reasoning path, such as semantic scope, entity confusion, endpoint overreach, timing misuse, incomplete compound coverage, unfair proof burden, or defective pairwise adjudication. The correction must be expressed as a reusable conditional mechanism with counterexamples, never as a rule that maps a case, question, option letter, exact chart fingerprint, or remembered answer to a selection.

## Question-unit lifecycle

1. **FIRST BLIND FREEZE:** make one answer-free prediction and freeze it before reveal.
2. **REVEAL AND SCORE:** score that frozen prediction once. This is the question's only blind-accuracy contribution.
3. **ABSORB:** reopen relevant source parents, conditions, exceptions, and competing methods.
4. **DECOMPOSE:** identify exactly why the reasoning failed or succeeded for the wrong reason.
5. **FILL:** add missing retrieval, semantic, entity, temporal, endpoint, pairwise, fusion, method, or source capability.
6. **RESHAPE:** convert the local defect into a general mechanism with explicit applicability conditions and counterexamples.
7. **APPLY:** run clean post-reveal replays for fit and stability only; these replays never count as blind accuracy.
8. **ADVANCE:** after the correction object, provenance, pairwise replay, contamination scan, and stability gate pass, move to the next question so the revised reasoning can be tested prospectively.
9. **GENERATE:** after the full training set, freeze the candidate and test it on an unseen blind block.

A question may be training-complete even when its original first-blind prediction was wrong. That is expected: the purpose of the unit is to correct the reasoning. The correctness of that correction is tested prospectively on later distinct questions.

Evaluation and advancement are separate operations. `evaluate-question` may return `advance_allowed=true`, but the active state does not enter the next question until the separate `advance` operation is executed.

## Case-batch execution with question-independent settlement

A five-question case should be executed as one shared case batch when the same frozen chart, Bazi foundation, source whitelist, answer isolation, and entity topology apply to all five questions. Shared preparation is materialized once, then each question keeps an independent reasoning-correction object, first-blind score, direction matrix, pairwise rows, strongest competitor, formal endpoint status, and completion receipt.

Batch execution does not merge five questions into one accuracy observation or one reasoning object. It changes execution efficiency, not the scoring or audit unit:

- **execution unit:** one case batch;
- **training and audit unit:** one question;
- **accuracy unit:** one immutable first-blind prediction per distinct question;
- **generalization unit:** later frozen unseen cases, not repeated questions from the same case.

A batch may therefore activate Q2–Q5 together while retaining `TRAINING_UNIT_COMPLETE` only for questions whose individual correction gates actually pass. Candidate post-reveal ranks inside the batch remain training hypotheses until their question-level correction objects and validators are complete.

## Required reasoning-correction object

`TRAINING_UNIT_COMPLETE` requires a content-addressed `REASONING-CORRECTION-OBJECT-V2.1`, not only boolean completion flags. The object must contain:

1. the concrete error mechanisms;
2. source-parent chains, hashes, conditions, limits, and downstream effects;
3. the corrected reasoning order;
4. capability ceilings and forbidden inference jumps;
5. applicability conditions;
6. counterexamples and failure boundaries;
7. all `N×(N-1)/2` pairwise rows and a mechanically derived strongest competitor;
8. contamination, answer-memory, case-rule, Bazi-variant, and base-knowledge-promotion checks;
9. a candidate unit conclusion that keeps retrospective training fit separate from first-blind accuracy.

A four-option question therefore requires six unique pairwise rows. Missing rows, duplicate pairs, invalid directions, incomplete parent payloads, or an invalid correction hash prevent training completion.

## Accuracy policy

Only rows with `evaluation_role=FIRST_BLIND_PREDICTION`, an immutable pre-reveal freeze, answer-free prediction input, and complete provenance are accuracy eligible.

- Exactly one eligible accuracy observation is allowed per distinct question.
- `POST_REVEAL_TRAINING_REPLAY` rows measure fit and stability only.
- Re-running one question five times cannot produce an 80% or 100% blind-accuracy claim.
- Rolling TOP1/TOP2 rates are computed across distinct questions' first frozen predictions.
- The default rolling rate gate is not evaluated before five distinct questions exist.
- QUESTION progression is driven by completion of reasoning correction, not by forcing the old question to become retrospectively correct.
- Final training-set closure still requires the configured rolling TOP1/TOP2 targets and a later frozen unseen test for generalization.

Default targets:

- at least five clean post-reveal stability replays per trained question;
- at least five distinct first-blind questions before evaluating rolling rates;
- rolling TOP1 at least 80%;
- rolling TOP2 at least 90%;
- prior-method retention at least 80% when applicable.

## State model

```text
LEARNING_ACTIVE
  ├─ contamination/case or answer rule → HOLD_ANSWER_OR_CASE_RULE_CONTAMINATION
  ├─ invalid provenance/freeze          → HOLD_INVALID_PROVENANCE_OR_FREEZE
  ├─ correction incomplete              → CONTINUE_CURRENT_UNIT_TRAINING
  ├─ correction complete                → TRAINING_UNIT_COMPLETE → next question
  ├─ all training units complete,
  │    rolling target below threshold   → RESHAPE_AND_RETEST_ON_LATER_DISTINCT_UNITS
  └─ all training units complete,
       rolling target satisfied         → AWAIT_FROZEN_UNSEEN_BLIND_TEST
```

`MASTERED` is not granted from repeated post-reveal runs of one question. The repository uses `TRAINING_UNIT_COMPLETE` for a question whose error analysis and reasoning correction are complete.

## Base-knowledge boundary

A single question may produce a method candidate. Base-knowledge promotion requires at least two independent source-parent chains and reproduction in at least two distinct training units. Even then, unseen prediction ability remains unproven until a frozen blind block is evaluated.

## CLI

```bash
fortune-learning-cycle create --cycle-id <id> --group-id <group> --unit-plan <plan.json> --output <cycle.json>
fortune-learning-cycle evaluate-question --cycle <cycle.json> --evidence <question-evidence.json> --output <evaluation.json>
fortune-learning-cycle advance --cycle <cycle.json> --evaluation <evaluation.json> --output <next-cycle.json>
```

Formal release remains separate. Training completion does not by itself establish exact endpoints, machine-valid local seals, S03 fusion, remote GitHub Actions success, or unseen-case performance.
