# Batch 12CW — 奎章閣 G893《授時曆立成》實物閉合：Type II 北京表 × 南京大統 × 1578《三命通會》

## Status

```text
G893_COMPLETE_PUBLIC_PHYSICAL_SEQUENCE=204/204_CLOSED
G893_DIRECT_TABLE=授時曆日出入晨昏半晝分
G893_WINTER_SOLSTICE_DAYLIGHT=38.1592_KE
G893_SUMMER_SOLSTICE_DAYLIGHT=61.8408_KE
G893_NUMERIC_BRANCH=SHOUSHI_TYPE_II_BEIJING_CII_B
RAW_YANDU_SHOUSHI_EQUALS_SANMING_1578=DISPROVED
NANJING_DATONG_REGIONAL_LAYER=STRENGTHENED
EXACT_SANMING_QUANTIZATION_CHANGE_DAY_RULE=UNRESOLVED
DIRECT_SANMING_PARENT=UNRESOLVED
HPA_ZDATE_006=MISSING_FROM_PRODUCT
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
```

## 1. Trigger

Batch 12CV directly closed a fifteenth-century Kyujanggak Tonggui witness for the Nanjing Datong C-II-N daily `晨昏分` family. The remaining high-value question was whether the primary `授時曆立成` table named by the 1578 `三命通會` birth-time discussion could itself be the 59/41 numerical source.

A new source-bound Kyujanggak acquisition has now made the complete G893 object directly readable, so the question can be answered from physical numerals rather than title similarity.

## 2. Object/date firewall

Kyujanggak identifies:

```text
title = 授時曆立成
call number = 奎貴893
book_cd = GK00893_00
extent = 1冊(102張)
edition = 甲寅字
provider date = 15世紀前半(世宗年間:1418-1450)
```

The exact surviving-copy year remains unresolved. Modern sources disagree between 1434 and 1444; neither is promoted above the institution's broader copy-level date range.

Complete acquisition:

```text
workflow run = 35324088110
artifact = 10538746764
artifact name = kyudb-g893-shoushi-licheng-complete-physical-r2
viewer range = 000a-101b
physical pages = 204/204
OCR final authority = false
```

## 3. Winter-solstice physical table: page 052a

SHA-256:

```text
12a9fcd04d87d00a401776fec63bb4fcc55db776b28eb37e8599dc672a1ac2c7
```

Direct visual review reads the heading and section:

```text
授時曆日出入晨昏半晝分
冬至後
初日
```

The five directly printed values are:

| field | physical value |
|---|---:|
| 晨分 | 2842.04 |
| 日出分 | 3092.04 |
| 半晝分 | 1907.96 |
| 日入分 | 6907.96 |
| 昏分 | 7157.96 |

They internally satisfy the traditional 250-fen dawn/dusk offset:

```text
2842.04 + 250 = 3092.04
5000 - 3092.04 = 1907.96
5000 + 1907.96 = 6907.96
6907.96 + 250 = 7157.96
```

Under `日周10000 = 100刻`:

```text
winter daylight = 2 × 1907.96 / 100 = 38.1592 ke
winter night = 61.8408 ke
```

This directly closes the precise `~62/38` Yandu/Beijing Shoushi branch at physical-page level.

## 4. Summer-solstice mirror: page 077a

SHA-256:

```text
629334d68177b84e551f9bdb0700d238800233832bbba417ba7cf29b247b7bbe
```

The same physical table transitions to the summer-solstice half and directly prints the initial row:

| field | physical value |
|---|---:|
| 晨分 | 1657.96 |
| 日出分 | 1907.96 |
| 半晝分 | 3092.04 |
| 日入分 | 8092.04 |
| 昏分 | 8342.04 |

Thus:

```text
summer daylight = 2 × 3092.04 / 100 = 61.8408 ke
summer night = 38.1592 ke
```

The winter/summer symmetry is therefore directly physical, not inferred from a later received transcription.

## 5. Table-family identity and geographic calibration

Li Liang's numerical-table study classifies:

```text
Shoushi Type II = C-II-B = Beijing/Dadu
Datong Type II = C-II-N = Nanjing
```

Independent modern astronomy-history work likewise identifies Shoushi-Licheng sunrise/sunset data with Beijing and Ming Datong data with Nanjing.

Those modern studies are classification/control layers only. The decisive numerical claims in this batch rest on G893 and the already physically controlled C-II-N witnesses.

Direct comparison:

| table branch | winter daylight | summer daylight |
|---|---:|---:|
| G893 Shoushi C-II-B Beijing | 38.1592 | 61.8408 |
| Datong C-II-N Nanjing | 41.3660 | 58.6332 |

The local calibration difference is therefore about 3.21 ke at the solstitial extremes.

## 6. Consequence for 1578《三命通會》

The exact 1578 physical Sanming target prints:

```text
夏至 -> 晝59 / 夜41
```

Therefore the shortcut

```text
Sanming says 授時曆分之
=> directly use the raw Yandu/Beijing 授時曆立成 table
```

is now rejected by direct pre-1578 physical numerals.

```text
G893 raw Shoushi summer daylight = 61.8408
Sanming displayed summer daylight = 59
```

At the same time, the Nanjing C-II-N day-182 half-day `2931.66` yields daylight `58.6332`, which sits in the numerical neighborhood of Sanming's displayed 59. This strengthens the Nanjing/Datong regional-numerical component already established in Batches 12CF/12CG/12CV.

Firewall:

```text
58.6332 -> 59 does NOT prove nearest-integer was Wan Minying's historical rule.
The exact Sanming intermediate/change-day fingerprint remains unresolved.
```

## 7. Historical synthesis

The evidence now supports a more precise composite model:

```text
Shoushi:
  daily Type-II table architecture
  + explicit locality-capable computational framework

        ↓ regional recalibration / Datong lineage

Nanjing Datong C-II-N:
  41.3660 ↔ 58.6332 precise daily substrate
  + official pre-1578 Nanjing 59-ke regime

        ↓ unresolved integer reduction / editorial binning

1578 Sanming:
  displayed seasonal integer ladder
  + summer 59/41
  + distinctive intra-term change instructions
```

This model does not require the false equation `授時曆 = raw Beijing numerical table`.

## 8. Transmission impact

Added/strengthened:

- `PHYSICAL-COPY-KYUDB-G893-SHOUSHI-LICHENG-15C-GABINJA`
- `TABLE-SHOUSHI-DAILY-CII-B-BEIJING`
- existing `TABLE-NANJING-DATONG-DAILY-CII-N-1380S`
- existing `TABLE-SANMING-1578-DAYNIGHT-KE`

New graph results:

- G893 directly **ATTESTS** the Beijing Type-II table;
- Beijing C-II-B and Nanjing C-II-N **PARALLEL_COEXIST** as structurally homologous but regionally different numerical branches;
- raw Beijing C-II-B **DISPROVES_LINEAGE_SHORTCUT** to the 1578 Sanming numeric table.

No direct-copy direction between C-II-B and C-II-N is asserted.

## 9. Product adjudication

This is a provenance/genealogy closure only.

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

The six legacy G893 numerical/textual controls from Batch 11 are **not** silently adjudicated by whole-volume acquisition; they remain page-specific collation work.

## 10. Next gate

The Sanming ancestry bottleneck is now almost entirely the reduction layer:

1. find a securely pre-1578 Chinese source that states how precise daily `半晝/晨昏` values are converted into integer `晝夜刻` bins or specifies the exact change day;
2. mechanically test that rule against the 1578 Sanming intra-term transitions, especially `大寒十三後日` and `雨水後四日`;
3. continue a Chinese physical C-II-N witness search so origin and Joseon transmission remain distinguished;
4. later, separately use the newly complete G893 image sequence to close the six old Batch-11 G893 controls without contaminating the Sanming genealogy question.

Research record: `docs/research/ZIWEI-KYUDB-G893-SHOUSHI-TYPE-II-BEIJING-PHYSICAL-COLLATION-R1.json`
