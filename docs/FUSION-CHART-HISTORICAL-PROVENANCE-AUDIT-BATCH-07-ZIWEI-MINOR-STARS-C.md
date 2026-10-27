# Fusion Chart Historical Provenance Audit R1 — Batch 07C

## Ziwei minor-star source gaps, identity collisions, and YueDe school split

Status: **AUDITED / R4 RULE-FAMILY DECOMPOSITION COMPLETE / NO ALGORITHM REOPEN**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
```

## 1. Purpose

Batch 07A and 07B closed the rule families that could be tied to direct
received-text or 1581 early-print mechanics. Batch 07C deliberately handles the
opposite class: rules whose current coordinates are deterministic but whose
historical genealogy is mixed, source-insufficient, or name-colliding.

The goal is not to force every current rule into a classical pedigree. A rule
can remain operationally stable while its historical authority is downgraded.

## 2. Findings

### 2.1 Standalone 蜚廉 is not the 博士十二神 飞/蜚廉 rule

The current standalone `STAR.FEILIAN` uses a four-sector birth-year table from
S01 PR-033. The early Ziwei witnesses currently registered instead expose
飞/蜚廉 as a member of 博士十二神, anchored from 禄存 and traversed by
year-polarity/sex direction.

The product already represents that ring member separately as
`RING.BOSHI12.FEILIAN`.

Verdict: **SOURCE_INSUFFICIENT for the standalone table; no runtime identity
conflation and no coordinate reopen**.

### 2.2 龙德 has an early-print coordinate witness

In the 1581 《捷览》 生年太岁十二神 sequence, 龙德 is ordinal 7 from the
birth-year 太岁 palace. Current `STAR.LONGDE` is `year_branch + 7`, and
`RING.TAISUI12.LONGDE` is independently generated at the same ordinal.

Verdict: **HISTORICALLY_SUPPORTED for placement geometry**.

The standalone/ring duplication is now treated as an identity/provenance
relationship rather than two unrelated coordinate rules.

### 2.3 月德 is a genuine historical split

Two historical families are materially different:

- the family preserved in 《神峰通考》 says 月德 follows from 巳;
- received 《紫微斗数全书》 says 月德 starts from 子 and advances to the
  current 流年太岁.

Current production uses the 巳-start family.

This is not sufficient evidence to switch defaults. The received Fullbook
wording also carries a temporal-scope question (flow-year vs natal projection),
so its alternative is not yet promoted into a replayable runtime candidate.

Verdict: **DISPUTED_MULTIPLE_CANDIDATES; no winner selected**.

### 2.4 月解 / month 解神 lacks an early Ziwei placement witness

Current `STAR.JIESHEN` uses the two-month table
申、戌、子、寅、辰、午. The received Fullbook witness found in this audit is
instead year-based 解神, already separated in the product as modern 年解.

Verdict: **SOURCE_INSUFFICIENT for the month table**.

The product's distinction between month 月解 and year 年解 is retained because
it prevents a real name collision, but historical provenance for the month
table remains open.

### 2.5 天巫: same-name evidence from another system is not proof

The current four-palace monthly table is common in modern Ziwei material.
External classical hits for 天巫 are calendrical/Qizheng material with different
logic, not a Ziwei-specific witness for the current coordinates.

Verdict: **SOURCE_INSUFFICIENT**.

### 2.6 天月: modern table is stable, historical identity is noisy

The current twelve-month table is widely repeated in modern implementations.
Historical searches under 天月 predominantly retrieve other concepts such as
天月德/天月德合 from different systems.

Verdict: **SOURCE_INSUFFICIENT**.

### 2.7 阴煞: cross-system homonyms are not candidates by default

The current six-palace monthly cycle is deterministic. Classical same-name hits
found externally use incompatible Bazi/astrological definitions.

Verdict: **SOURCE_INSUFFICIENT**.

## 3. Parent R4 closure

After HPA-ZMINOR-001..026, plus the separately audited TianShang/TianShi row
HPA-ZIWEI-017, every placement family in the current Operational minor-star R4
generator has a granular audit disposition.

Therefore HPA-ZIWEI-008 no longer needs
`IMPLEMENTATION_REVIEW_REQUIRED`. It is now a fully decomposed
`SOURCE_INSUFFICIENT` parent summary because some child rules still lack
qualifying historical provenance.

This is a research-status closure, not an algorithm closure change.

## 4. Accounting

```text
BATCH_07C_ZIWEI_MINOR_STARS=AUDITED
NEW_GRANULAR_RULE_ROWS=7
NEW_AUDITED_ROWS=7
TOTAL_MATRIX_ROWS=145
TOTAL_AUDITED_ROWS=95
MINOR_STAR_CHILD_ROWS=26
HPA_ZIWEI_008=FULLY_DECOMPOSED_SOURCE_INSUFFICIENT_PARENT
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
PRODUCTION_DEFAULT_CHANGE_COUNT=0
```

## 5. Next research direction

Do not keep expanding the broad R4 parent. Future work should target only the
remaining child evidence problems:

1. establish or reject a Ziwei-specific historical witness for standalone 蜚廉;
2. resolve 月德 natal-vs-flow scope before candidate promotion;
3. seek edition-bound provenance for 月解、天巫、天月、阴煞;
4. audit standalone/ring alias relationships so identical display names never
   imply identical historical identities;
5. then move to Ziwei temporal/dynamic auxiliary rules.
