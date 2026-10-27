# Fusion Chart Historical Provenance Audit R1 — Batch 06

## Ziwei natal foundations: day boundary, Life/Body, palaces, stems and bureau

Status: **AUDITED / NO CHART ALGORITHM REOPEN**

Invariant states:

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

## 1. Scope

Batch 06 audits the five upstream Ziwei natal-foundation rows that control most
downstream geometry:

- `HPA-ZIWEI-001` Ziwei day-boundary policy;
- `HPA-ZIWEI-002` Life/Body palace placement;
- `HPA-ZIWEI-003` Twelve palace designations;
- `HPA-ZIWEI-004` Palace stem assignment;
- `HPA-ZIWEI-005` Five-element bureau.

The key methodological change in this batch is to bind the audit directly to the
frozen `ZZQS` received-text atoms inside S01 instead of treating modern
normalized/projected summaries as the primary historical authority.

## 2. Direct received-text anchors

S01 freezes the following received-Fullbook text atoms in its primary-source
layer.

### 2.1 Life / Body palace

`S01:ZZQS-A-1744`:

> 大抵人命，俱从寅上起正月，顺数至本生月止。又自人生月上起子时，逆至本生时安命，顺至本生时安身。

`S01:ZZQS-A-1745` gives worked examples for 正月子、丑、寅时.

This mechanically matches the released non-leap geometry:

```text
month_anchor = 寅 + (lunar_month - 1)
Life = month_anchor - hour_ordinal
Body = month_anchor + hour_ordinal
```

The released tests already exhaust all 12 × 12 ordinary month/hour pairs.

Leap-month handling remains a separate policy question and is not collapsed into
this base formula.

### 2.2 Twelve palaces

`S01:ZZQS-A-1749` states that the twelve palaces are placed in reverse
sequence from Life.

`S01:ZZQS-A-1751` preserves the sequence:

```text
命 兄弟 妻妾 子女 财帛 疾厄 迁移 奴仆 官禄 田宅 福德 父母
```

The current runtime sequence is geometrically identical. The product's
`夫妻` display label is a terminology normalization of the received
`妻妾`; it is not a geometric rule change. `奴仆` is retained in the
current low-level registry, while higher presentation layers may expose modern
friend/servant terminology.

### 2.3 Palace stems / Five Tigers

`S01:ZZQS-A-1755` and `S01:ZZQS-A-1756` preserve the five start pairs:

```text
甲己 -> 丙寅
乙庚 -> 戊寅
丙辛 -> 庚寅
丁壬 -> 壬寅
戊癸 -> 甲寅
```

This matches `YEAR_STEM_TO_YIN_START_STEM` exactly. The runtime then advances
the Heavenly Stem cyclically with the twelve branch addresses. No mismatch was
found.

### 2.4 Five-element bureau

`S01:ZZQS-A-1747` directly demonstrates the historical dependency chain:

```text
birth-year stem -> Five-Tigers palace stem
-> Life-palace Ganzhi -> NaYin element -> bureau
```

Its worked example is:

```text
甲年 + 命寅 -> 丙寅 -> 炉中火 -> 火局
```

The immediately following received `六十花甲子纳音歌`
(`S01:ZZQS-A-1760..1767`) supplies the NaYin table used by that derivation.
The current runtime reproduces this example as `丙寅 / 炉中火 / 火六局`.
The 1581 Jielan family and received Fullbook star tables also independently
preserve named bureau families, so this is not a modern-only construction.

No chart algorithm defect was found in the current bureau derivation.

## 3. Ziwei day boundary: source attribution is not closed

S01's modern normalized/projected layer contains two candidate traditions:

- `ZZZA-PR-005`: Zi hour begins the new chart date at 23:00;
- `ZZZA-PR-006`: late Zi stays on the old date and early Zi uses the next date.

The normalized layer additionally carries the sentence:

`《紫微斗数全书》载：“子时乃一日之始，当从新日计。”`

However, Batch 06 could not locate that exact sentence in the repository's
frozen `ZZQS` received-Fullbook raw-text layer. A checked external received
transcription likewise did not expose the exact string.

This is **not sufficient to call the sentence fabricated**: another edition,
commentary or recensional line may still establish it. It is sufficient to say
that the present attribution is not primary-source-closed.

Therefore the audit records:

```text
PROV-DEFECT-005=UNVERIFIED_FULLBOOK_ATTRIBUTION_FOR_ZIWEI_DAY_BOUNDARY
REPAIR=QUARANTINE_AS_UNVERIFIED_ATTRIBUTION
HPA-ZIWEI-001=DISPUTED_MULTIPLE_CANDIDATES
ALGORITHM_REOPEN_AUTHORIZED=false
```

The released production profile continues to use `ZI_START_23` because Product
R1 is closed. Historical provenance does not elevate that production choice into
a unique classical winner.

A later Zhongzhou-school witness explicitly acknowledges the dispute and prefers
midnight division. That is useful as a school witness, but it cannot retroactively
prove the received-Fullbook attribution.

## 4. Findings by Matrix row

| Row | Verdict | Reason |
|---|---|---|
| `HPA-ZIWEI-001` | `DISPUTED_MULTIPLE_CANDIDATES` | The dispute is real; the current direct-Fullbook attribution for the 23:00 rule is not closed. |
| `HPA-ZIWEI-002` | `HISTORICALLY_SUPPORTED` | Direct received-text formula and worked examples match the runtime base geometry. |
| `HPA-ZIWEI-003` | `HISTORICALLY_SUPPORTED` | Direct received-text palace order and reverse placement match runtime geometry. |
| `HPA-ZIWEI-004` | `HISTORICALLY_SUPPORTED` | Direct Five-Tigers start table matches runtime exactly. |
| `HPA-ZIWEI-005` | `HISTORICALLY_SUPPORTED` | Direct Life-palace Ganzhi -> NaYin -> bureau example and NaYin table match runtime. |

## 5. No silent source rewriting

The immutable S01 canonical corpus is not rewritten merely because one
normalized attribution is not yet verified. The audit layer performs the repair
by quarantining that attribution from primary-authority use and recording the
defect explicitly.

This distinction matters:

- source preservation remains intact;
- provenance authority is corrected;
- chart calculations remain unchanged;
- future edition/facsimile evidence can resolve the attribution forward-only.

## 6. Batch verdict

```text
BATCH_06_ZIWEI_NATAL_FOUNDATIONS=AUDITED
AUDITED_ROW_DELTA=5
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT_DELTA=1
ALGORITHM_REOPEN_COUNT=0
PRODUCTION_DEFAULT_CHANGE_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

Next work should audit the still-broad Ziwei minor-star and ring bundles by
splitting independent historical rule families, then proceed to temporal/dynamic
rules. The day-boundary attribution remains an explicit research target rather
than an excuse to force a winner.
