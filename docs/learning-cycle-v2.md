# Learning Cycle V2

## Objective

The fixed development examples are a revealed training set. They must be studied repeatedly until the model reaches stable mastery from clean prediction inputs. Audit controls remain guardrails; they are not a substitute for learning.

Core sequence:

> 汲取 → 拆解 → 填充 → 重塑 → 化用 → 生发

Machine names:

> ABSORB → DECOMPOSE → FILL → RESHAPE → APPLY → GENERATE

## Three separate claims

- **Training mastery:** performance on examples already used for learning.
- **Cold-start stability:** reproducibility with new run IDs and clean inputs.
- **Unseen generalization:** performance on a later frozen block never used for learning.

Training mastery must never be reported as unseen accuracy.

## Learning phases

1. **ABSORB:** reopen relevant source parents, conditions, exceptions and competing methods.
2. **DECOMPOSE:** locate the exact defect in source coverage, literal atoms, structure, timing, endpoint, pairwise decision, fusion or execution.
3. **FILL:** add missing retrieval, semantic, entity, temporal, endpoint, pairwise, fusion, method or knowledge capability.
4. **RESHAPE:** turn the local defect into a conditional general mechanism with counterexamples.
5. **APPLY:** perform fresh cold-start replays and retention tests for mastered units.
6. **GENERATE:** freeze the mastered candidate and test it on unseen cases.

A single question may justify a method candidate. A base-knowledge promotion requires two independent source parents and reproduction in two distinct training units.

## Unit modes

### QUESTION

Train one question at a time. Default gate:

- at least five clean cold-start attempts;
- TOP1 at least 80%;
- TOP2 at least 90%;
- complete provenance and pairwise replay;
- no case-specific direction rule;
- previously mastered questions remain at or above 80%.

Four correct TOP1 results out of five clean attempts is the minimum default mastery.

### CASE

Train one case at a time. Default gate is TOP1 at least 80% across its questions, TOP2 at least 90%, two clean replays and retention of earlier units.

### GROUP

Train the complete development group. Default gate is TOP1 at least 80%, TOP2 at least 90%, two clean replays and no unacceptable regression damage.

`DEV-GROUP-002` should begin in QUESTION mode and advance in frozen question order.

## Legal changes

The learning cycle may change retrieval, semantics, mappings, timing, endpoint logic, pairwise adjudication, fusion, general methods and source knowledge. Changes must have explicit parent chains, conditions, counterexamples and downstream effects.

Forbidden changes include rules keyed to a case ID, question ID, option letter, exact fingerprint or prior output. A Bazi version cannot be selected because it matches a known result.

## State model

```text
LEARNING_ACTIVE
  ├─ contamination/case rule → HOLD_ANSWER_OR_CASE_RULE_CONTAMINATION
  ├─ invalid provenance      → HOLD_INVALID_PROVENANCE
  ├─ below mastery           → continue DECOMPOSE/FILL/RESHAPE/APPLY
  ├─ current unit mastered   → next unit
  └─ all units mastered      → TRAINING_SET_MASTERED_AWAITING_UNSEEN_BLIND_TEST
```

There is no fixed five-round stop, no fixed defect retry limit and no stop after two zero-improvement rounds. Lack of improvement triggers deeper decomposition or method reshaping.

## CLI

```bash
fortune-learning-cycle create --cycle-id <id> --group-id <group> --unit-mode QUESTION --unit-plan <plan.json> --output <cycle.json>
fortune-learning-cycle evaluate --cycle <cycle.json> --replay <replay.json> --output <evaluation.json>
fortune-learning-cycle advance --cycle <cycle.json> --evaluation <evaluation.json> --output <next-cycle.json>
fortune-learning-cycle validate-patch --patch <patch.json> --output <validation.json>
```

Formal release remains separate. Mastery does not by itself establish exact endpoints, machine-valid local seals, S03 fusion or unseen-case performance.
