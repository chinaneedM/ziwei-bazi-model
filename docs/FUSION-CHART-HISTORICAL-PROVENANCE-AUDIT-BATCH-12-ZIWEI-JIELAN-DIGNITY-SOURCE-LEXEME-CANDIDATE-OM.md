# Historical Provenance Audit — Batch 12OM

## Scope

Target: `HPA-ZIWEI-018` — 1581 Jielan historical dignity table.

12OM converts the star-oriented CH70 material into a deterministic **source-lexeme candidate**, not a modern Dignity grade table.

## Representation

New registry:

`ZIWEI-JIELAN-1581-DIGNITY-LEXEME-CANDIDATES-R1@1.0.0`

Runtime resolver:

`ZIWEI-JIELAN-1581-DIGNITY-LEXEME-RUNTIME-R1@1.0.0`

The candidate contains 25 named star entities/groups × 12 branches = **300 cells**.

Each cell carries:

- exact source lexeme set;
- attested/un-stated status;
- source-conflict flag;
- source-explicit lexical gloss relations only.

No production R4 grade/status is assigned.

## Source anomalies preserved

The CH70 candidate deliberately retains:

- 紫微午宫: both `庙` and `平`;
- 巨门丑宫: both `局` and `陷`;
- 天机巳宫: `UNSTATED_IN_CH70_STAR_VERSE`.

Those cells are evidence, not errors to auto-correct.

The chapter's own gloss relations are stored as lexical links, e.g. 旺→庙, 平→闲, 得地→旺, 嗔→陷, 庭→庙. The resolver does not transitively collapse those relations into a production scale.

## CH69 boundary

CH69 is a palace-oriented parallel dignity text and remains registered for **cell-level cross-collation**.

12OM does not use CH69 to fill CH70 holes or decide CH70 conflicts. That work is reserved for 12ON.

## Matrix status

`HPA-ZIWEI-018` remains `MISSING_FROM_PRODUCT`.

The gap is now narrower: raw source-lexeme candidate readiness exists internally, but CH69/CH70 reconciliation and an explicit read-only product surface remain outstanding.

No production Dignity rule or algorithm changes.

## Next

**12ON — cross-collate CH69 against CH70 at cell level.**
