# Batch 12CV — 奎章閣通軌實物閉合：太陰《晨昏分立成鈐》× 南京大統 C-II-N；GK12437 全卷作用域控制

## Status

```text
GK12436_PRE1578_PHYSICAL_WITNESS=CLOSED
GK12436_DIRECT_HEADING=冬夏二至日晨昏分立成鈐
GK12436_DAY0_MORNING_DUSK=2681.70/7318.30
GK12436_DAY0_HALF_DAY=2068.30
GK12436_DAY178_MORNING_DUSK=1819.66/8180.34
GK12436_DAY178_HALF_DAY=2930.34
NCL_CII_N_EXACT_TWO_POINT_FINGERPRINT=HIGH_CONFIDENCE_SAME_NUMERICAL_TABLE_FAMILY
GK12437_COMPLETE_PHYSICAL_SCOPE=78_PAGES_REVIEWED
GK12437_INDEPENDENT_CHENHUN_DAYNIGHT_TABLE=NOT_ATTESTED_ON_REVIEWED_OBJECT
DIRECT_SANMING_PARENT=UNRESOLVED
EXACT_SANMING_QUANTIZATION_CHANGE_DAY_RULE=UNRESOLVED
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
```

## 1. Trigger

Batch 12CU moved the Sanming ancestry gate from annual almanacs to the original Tonggui computational carrier. The live branch then acquired three independent Kyujanggak physical routes:

- `GK12436_00 / 奎貴12436 / 太陰通軌`;
- `GK12437_00 / 奎貴12437 / 大統曆日通軌`;
- a neighboring `GK12435_00 / 太陽通軌` control.

This batch closes the two evidence questions that matter most: whether a pre-1578 Tonggui witness physically preserves the Nanjing-type `晨昏分` daily table, and whether the corrected `GK12437` record itself contains that table.

## 2. Date and object firewall

Kyujanggak directly identifies `GK12436` and `GK12437` as `甲寅字` witnesses corrected by 李純之/金淡 and catalogued within the fifteenth-century Sejong-era scope. The list surface emits a broad `1418` display field, but this batch does not turn that into an exact impression year.

Safe scope:

```text
physical witnesses = catalogued 15th-century / Sejong-era / pre-1578
exact impression year = unresolved
Chinese source exemplar = unresolved
same title/system != same physical object
```

## 3. GK12436《太陰通軌》directly preserves the target daily table

Source-bound `039a` SHA-256:

```text
eeacba803100e6391e2cda54f9d3f499eb89a7cae1ab32773fd82c294bcb3dc5
```

Direct no-OCR visual review reads:

```text
冬夏二至日晨昏分立成鈐
```

and the winter-solstice initial day:

```text
晨分 2681.70
昏分 7318.30
sum 10000.00
```

Source-bound `047a` SHA-256:

```text
57dad7c13b24f6a1a265a3b6794205102f95808bd73424d89519b0fd9c00250c
```

At accumulated day 178 the physical page reads:

```text
晨分 1819.66
昏分 8180.34
sum 10000.00
```

The table is organized by accumulated daily arguments from the solstice, not merely by 24 solar-term rows.

## 4. Exact mechanical bridge to NCL《大統日出分》C-II-N

The already-registered Ming-history Tonggui relation gives:

```text
日出分 = 晨分 + 250
半晝分 = 5000 - 日出分
```

Thus:

```text
day 0:
2681.70 + 250 = 2931.70
5000 - 2931.70 = 2068.30

day 178:
1819.66 + 250 = 2069.66
5000 - 2069.66 = 2930.34
```

Batch 12CG independently fixed the NCL/Li-Liang C-II-N fingerprints as:

```text
day 0   half-day = 2068.30
day 178 half-day = 2930.34
```

Two exact fen-level matches separated by 178 daily steps, plus the same daily post-solstice structure, identify the GK12436 passage as transmission of the same Nanjing Datong C-II-N numerical family at high confidence.

This is materially stronger than matching a single `59/41` pair.

## 5. GK12437《大統曆日通軌》complete physical control

Workflow `35317924654` / artifact `10536220506` acquired all 78 viewer pages of `GK12437_00`.

Direct contact-sheet and page review shows the object is dominated by the solar `盈縮 / 限` computational tables expected from the corrected Batch 12CO description. Page `006a` visibly opens:

```text
大陽冬至前後二象盈初縮末限
```

Across the complete reviewed physical object, no independent `晨昏分 / 日出入 / 晝夜刻` table was identified.

This conclusion is deliberately object-scoped:

```text
GK12437 reviewed object: target day/night table not attested
wider 大統曆法通軌/Tonggui system: absence NOT claimed
```

Therefore Batch 12CO remains correct: the target day/night table must not be attributed to `DIC_A3_000150 / GK12437` merely from generic title or catalog identity.

## 6. Historical consequence

The numerical-substrate chain is now stronger:

```text
1380s Nanjing Datong C-II-N daily table family
        ↓
15th-century Joseon Gabinja physical transmission in GK12436
        ↓ (structural/numerical ancestry component; exact path unresolved)
1578 Sanming displayed day/night-ke ladder
```

What is now closed:

- a directly readable pre-1578 Tonggui physical witness for the C-II-N daily table family;
- exact fen-level identity at day 0 and day 178;
- cross-object correction that GK12437 itself is not the target day/night table carrier on the reviewed complete surface.

What remains open:

- the Chinese physical exemplar between early-Ming Nanjing table production and the Joseon witness;
- the exact integer reduction / quantization / change-day rule;
- a direct-copy parent for Wan Minying's 1578 display.

## 7. Transmission impact

Nodes added/strengthened:

- `PHYSICAL-COPY-KYUDB-TAIYIN-GK12436-15C-GABINJA`
- `PASSAGE-KYUDB-TAIYIN-039A-CHENHUN-LICHENG`
- `PHYSICAL-COPY-KYUDB-RITONGGUI-GK12437-15C-GABINJA`
- existing `TABLE-NANJING-DATONG-DAILY-CII-N-1380S`

Supported:

- GK12436 physical copy directly attests the `晨昏分立成鈐` passage;
- that passage transmits the C-II-N numerical family at high confidence.

Explicitly unproved:

- GK12436 as direct physical/textual parent of 1578 Sanming;
- GK12437 as carrier of the target day/night table.

## 8. Product adjudication

No chart runtime rule changes.

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
HPA_ZDATE_006=MISSING_FROM_PRODUCT
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 9. Next gate

The bottleneck has moved from “find a pre-1578 daily table” to “find the reduction rule”:

1. locate a securely pre-1578 Chinese/Tonggui rule that states how daily `晨昏/半晝` fen are reduced to integer day/night ke or defines the change day;
2. test it against the exact 1578 Sanming transitions, not only extrema;
3. continue Chinese physical-witness search for the same C-II-N table to distinguish origin from Joseon transmission;
4. keep the Fullbook upper-five-ke → previous-night Hai lineage independent.

Research record: `docs/research/ZIWEI-KYUDB-TONGGUI-DAILY-TABLE-PHYSICAL-CLOSURE-R1.json`
