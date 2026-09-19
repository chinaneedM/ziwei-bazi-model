# Fusion Chart Historical Provenance Audit R1 — Batch 12DT

## 奎章閣《大統曆法通軌》六部件目录交叉映射：12434–12439 聚合关系与总题名检索边界

Status: **FIRST-PARTY SIX-COMPONENT CATALOG CROSSWALK CLOSED / GK12434_00–GK12439_00 DIRECTLY BOUND AS SIX CURRENT COMPONENT HOLDINGS / LI LIANG 2022 SUPPORTS AGGREGATE DATONG LIFA TONGGUI = COLLECTION NOS 12434–39 / CURRENT AGGREGATE-TITLE NONRETURN IS NOT NO-HOLDING EVIDENCE / 1418 VS 1444 DATE FIELDS NOT NORMALIZED / ZERO WHOLE-KE OR SANMING-PARENT VOTE / NO RUNTIME CHANGE / NO ALGORITHM REOPEN**

## 1. Why this batch

Batch 12DS localized the missing whole-ke layer outside the reviewed NLC 《太陰通軌》 p12–p24 consumer interface and left four active gates, including continued Datong/Tonggui source work.

The live branch then added workflow run `35434045642` to search the current Kyujanggak catalog for the aggregate title `《大統曆法通軌》`.

That probe cannot support a no-holding conclusion:

- the exact traditional-title request `大統曆法通軌` ended in a connection reset;
- four alternate title queries returned zero `book_cd` values;
- an earlier successful first-party route had already exposed six exact component records spanning `GK12434_00` through `GK12439_00`.

The correct question is therefore catalog modeling, not simple title presence/absence.

## 2. First-party current catalog crosswalk

Workflow `35308888364` / artifact `10532910411` directly returned these current Kyujanggak records:

| Component title | book_cd | Call number | Edition field | Catalog year field |
|---|---|---|---|---|
| 四餘纏度通軌 | GK12434_00 | 奎貴12434 | 甲寅字 | 1444 |
| 太陽通軌 | GK12435_00 | 奎貴12435 | 甲寅字 | 1418 |
| 太陰通軌 | GK12436_00 | 奎貴12436 | 甲寅字 | 1418 |
| 大統曆日通軌 | GK12437_00 | 奎貴12437 | 甲寅字 | 1418 |
| 交食通軌 | GK12438_00 | 奎貴12438 | 甲寅字 | 1418 |
| 五星通軌 | GK12439_00 | 奎貴12439 | 甲寅字 | 1418 |

The same route emitted source-bound image/thumbnail paths for all six records.

This closes current **component-record identity**. It does not by itself prove that the six records are one physical volume, one exact impression event, or textually identical in every shared layer.

## 3. Scholarly aggregate control

The already-registered peer-reviewed source `EXT-LI-LIANG-SUNRISE-TABLES-2022` bibliographically identifies:

`Datong lifa tonggui = Yuan Tong ... kept in the Gyujanggak Library of Seoul National University, collection nos 12434–39.`

It also reports a 1444 print date.

For Tianwen this source performs two separate jobs:

1. **aggregate-set control** — it directly supplies the scholarly bridge from the work title `大統曆法通軌` to collection nos `12434–39`;
2. **secondary date witness** — its 1444 statement remains secondary and must not silently override the mixed first-party current catalog fields.

The aggregate-set bridge is high-confidence. Exact copy/impression dating remains separately scoped.

## 4. Why the current HEAD aggregate-title probe is not negative evidence

Run `35434045642` / artifact `10581242234` queried:

- `大統曆法通軌`;
- `대통력법통궤`;
- `大統曆法通軌四卷`;
- `大統通軌`;
- `대통통궤`.

The decisive exact traditional-title request failed with a connection reset. The remaining variants returned no `book_cd`.

After the six-record crosswalk, those results are retained only as a **current aggregate-title search-surface control**.

They do not prove:

`Kyujanggak has no 大統曆法通軌 witness.`

Instead the current public catalog is demonstrably capable of exposing the relevant surviving material under six component titles/identifiers.

## 5. Date firewall

The first-party route exposes mixed year fields:

`GK12434 -> 1444`

`GK12435..GK12439 -> 1418`

Prior Tianwen batches already prohibited reading the broad `1418` display as a precise impression year for every surviving object. Batch 12DT extends that firewall to the aggregate set.

Therefore:

`SECONDARY_1444 != AUTOMATIC_COPY_SPECIFIC_DATE_FOR_ALL_SIX`

`MIXED_FIRST_PARTY_YEAR_FIELDS != LICENSE_TO_NORMALIZE_ALL_TO_1444`

The aggregate edition-set identity and the exact surviving-copy date are separate propositions.

## 6. Content firewall

Direct physical content review remains asymmetric:

- `GK12436《太陰通軌》` has been directly collated and preserves the C-II-N morning/evening table;
- `GK12437《大統曆日通軌》` has been completely reviewed and does not carry an independent target day/night table on that object;
- `GK12434/GK12435/GK12438/GK12439` are catalog-bound here, but their contents are not directly collated in this batch.

Therefore no content from GK12436 is imputed across the other five components.

No whole-ke reduction rule, no `改箭` instruction, no 59-ke endpoint-binding rule and no exact `大寒十三後 / 雨水後四日` fingerprint is added by this batch.

## 7. Transmission-genealogy consequence

The graph now separates three levels:

`元統《大統曆法通軌》 work`

`-> Kyujanggak 12434–39 Gabinja component-set edition identity`

`-> six component physical holdings`

This is a bibliographic/provenance crosswalk, not a direct-copy chain into `1578《三命通會》`.

It adds zero numerical ancestry vote.

## 8. Product adjudication

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
HPA-ZDATE-006=MISSING_FROM_PRODUCT
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=12
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=12
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

No runtime candidate, no winner and no algorithm reopen.

## 9. Next gate

After closing the Kyujanggak catalog-model ambiguity, the substantive mechanism gate is unchanged:

1. locate a Chinese pre-1578 whole-ke reduction / table-selection / `改箭` / endpoint-binding instruction outside the reviewed Taiyin p12–p24 interface;
2. continue the exact `大寒十三後 / 雨水後四日` fingerprint search;
3. locate and physically collate the separately reported NLC three-juan `《大統曆法通軌》`;
4. inspect GK12434/GK12435/GK12438/GK12439 physically only when a concrete mechanism locator justifies it.

Research record: `docs/research/ZIWEI-KYUDB-DATONG-LIFA-TONGGUI-COMPONENT-SET-CROSSWALK-R1.json`.
