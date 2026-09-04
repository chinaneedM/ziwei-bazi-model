# Project Continuity Protocol R1

## Purpose

This protocol makes the repository, rather than chat memory, the durable handoff
mechanism for long-running Ziwei Dou Shu + Four Pillars development and research.

It exists because the project can span many conversations and a previous chat
may end because of context limits before a manual summary is written.

## Fixed new-chat entry point

A new conversation should begin with this instruction:

```text
继续项目。按仓库 docs/PROJECT-CONTINUITY-PROTOCOL-R1.md 启动，
以 GitHub 远端最新状态为唯一事实源。
```

No old SHA needs to be pasted.

## Mandatory startup sequence

Every new work session must perform these steps in order:

1. Read the live remote branch:
   `agent/fusion-chart-core-r1-20260822`.
2. Record the live HEAD and tree SHA.
3. Read recent commits and determine whether the branch moved after the last chat.
4. Read GitHub Actions for the exact live HEAD.
5. Read `docs/PROJECT-CURRENT-STATE-R1.json`.
6. Read `docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md`.
7. Read the historical provenance Matrix JSON/MD and external source registry.
8. Read the latest batch document named by the current-state JSON.
9. Check recent commits for any batch/state changes newer than that document.
10. Only then open the source/tests/docs needed for the next rule family.

If live GitHub state and any chat summary disagree, **live GitHub wins**.

## No self-referential HEAD in the handoff

The current-state file intentionally does not claim that an embedded commit SHA
is authoritative. A state file committed at SHA X would immediately make X
obsolete if it tried to update itself with the new commit.

Therefore:

```text
live HEAD = discovered at session start
project semantic state = read from PROJECT-CURRENT-STATE-R1.json
```

This avoids stale-SHA handoffs.

## What PROJECT-CURRENT-STATE-R1.json must contain

It must track at minimum:

- repository and development branch;
- current project stage;
- source-authority policy;
- non-negotiable invariants;
- current Historical Audit Matrix counts;
- completed research batches;
- latest batch document;
- current next-work focus;
- forward-only repository rules;
- fixed new-chat bootstrap order.

Whenever a research batch changes any of those fields, the current-state JSON
must be updated in the same work unit.

## CI synchronization gate

`scripts/verify-project-continuity-state-r1.py` compares the handoff state with
the live repository artifacts available in CI.

It fails when, for example:

- Matrix row/audited counts move but the handoff file does not;
- completed batch lists differ;
- provenance defect counts differ;
- the product CLOSED invariant changes unexpectedly;
- S00–S19 are again labeled infallible/canonical historical authority;
- the self/inward transformation rule is silently formalized;
- the continuity protocol or authority-policy files disappear.

This makes “forgot to update the handoff” a machine-detectable repository defect.

## Source-authority rule carried across chats

Every session must apply:

```text
S00-S19 = project research corpus, not infallible historical authority
sources/canonical/ = legacy storage/freeze path, not epistemic truth
modern software = compatibility witness, not classical authority
historical rules = edition/source/school scoped
disputed methods = preserve candidates unless explicitly governed
```

A future chat must not infer “S01 says X, therefore X is historically correct.”
It must inspect the underlying source identity and, when material, seek outside
bibliographic/textual corroboration.


## Philological continuity rule

Every new research session must preserve the project's 训诂 layer:

```text
surface wording != mechanical identity
different wording may encode the same rule
same wording may encode different concepts
philological ambiguity => preserve candidates, do not force a winner
```

When comparing historical passages, the session must normalize terminology only
after checking edition context, syntax, temporal layer and school usage. Any
normalization bridge that affects rule identity should be recorded in the
Matrix or batch document so a future chat can reproduce the interpretation.

## Historical audit continuation rule

For each batch:

1. identify the next over-broad or unresolved Matrix family;
2. decompose independent rules before judging them;
3. retrieve the strongest underlying historical witness available;
4. verify edition/date/title identity separately from rule text where possible;
5. compare exact mechanical rule with current implementation;
6. classify the result:
   - historically supported;
   - school-specific;
   - disputed candidates;
   - modern compatibility only;
   - source insufficient;
   - missing from product;
   - true implementation defect;
7. only a true scoped implementation defect may authorize local algorithm reopen;
8. write source/tests/docs/Matrix changes forward-only;
9. update `PROJECT-CURRENT-STATE-R1.json`;
10. run focused gates and inspect exact-HEAD CI.

## Interrupted-chat rule

If a conversation ends mid-batch, the next chat must not assume the last
assistant message reflects the repository. It should inspect recent commits and:

- continue from committed work if the batch advanced;
- repair a failing exact-HEAD CI if present;
- otherwise resume the first unfinished Matrix action named by the current state.

Partial chat reasoning that was never committed is not repository state.

## Handoff output at intentional session end

When a user asks for a manual handoff, generate it from:

1. live remote HEAD/tree/actions;
2. `PROJECT-CURRENT-STATE-R1.json`;
3. current Matrix;
4. recent commits.

The generated handoff is explanatory only. The fixed protocol remains the
authoritative startup mechanism.

## Current stage invariants

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
FUSION_CHART_HISTORICAL_PROVENANCE_AUDIT_R1=IN_PROGRESS
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
PREDICTION_AI_INTERPRETATION=CURRENTLY_OUT_OF_SCOPE
```
