# Fusion Chart Historical Provenance Audit — Batch 12CM

## Scope

This batch tests a high-value pre-1578 route opened after Batch 12CL: Zhou Xiang's Longqing-3 `《大明大統曆法》` book 6. The question is whether this surviving technical witness directly preserves the missing Nanjing/day-night-ke bridge to the 1578 `《三命通會》` display.

The result is a useful scope correction: the witness is genuine and chronologically close, but the reviewed public fascicle does **not** expose the target day/night-ke table. The batch therefore records a positive transmission/date control plus a strictly fascicle-scoped nonattestation. Deterministic charting remains closed.

## 1. Direct acquisition and no-OCR review

GitHub Actions run `35009608549` downloaded `https://www.kotenmon.com/cal/arabe/vol6.pdf`, SHA-256 `4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c`, rendered all 45 pages, and emitted artifact `10412298745` (`sha256:7ba11d497bd40e7683d0429662316e91ac900b60ab5f9f492a10d9d076c3356e`). The visual collation uses the rendered page images; OCR is not admitted for glyph claims.

## 2. Four-layer date firewall

Direct review separates the historical layers rather than collapsing them:

```text
p7   隆慶三年七月 ... 周相              -> 1569 reprint/prefatory layer
p9   步氣朔卷第一
     大元至元十八年辛巳為元至
     大明成化十三年丁酉所距積年...      -> 1477 calculation epoch
copy National Archives holding lineage       -> exact current call number/copy date unresolved here
PDF  modern public surrogate, metadata 2019 -> digital-surrogate layer only
```

The direct p9 wording is especially important: `1477` is not back-calculated from a modern scholar; the public facsimile itself states `大明成化十三年丁酉` as the calculation epoch. Conversely, that does **not** prove every textual layer was first composed in 1477.

Peer-reviewed control: Kobayashi (2014), note 38, identifies the National Archives Zhou Xiang reprint, states that books 1–5 contain `回回暦法` while book 6 appends `《大明大統曆法》`, notes the Longqing-3/1569 preface and Chenghua-13/1477 calculation content, and proposes that Zhou Xiang probably reprinted the paired material associated with Bei Lin. The final Bei-Lin→Zhou-Xiang dependency remains a scholarly hypothesis, not a confirmed graph edge.

## 3. What the 45-page fascicle actually contains

Direct visual review finds a dense technical calendrical compilation:

```text
p14  太陽冬至前後立成卷第二
p19  太陽夏至前後立成卷第四
p24+ 曆成 / 遲疾 procedures
p25+ 太陰立成 and lunar tables
p33+ further calculation rules/tables
p42  定朔 / 月大小 / 合朔時刻
p43  盈日 and related procedures
p44  交泛 / 直宿 procedures
p45  closing numerical material
```

Across the complete reviewed 45-page public reproduction, no independent table headed or mechanically identifiable as `晨昏分`, `日出入`, or `晝夜刻` was observed.

The negative is deliberately narrow:

```text
NO_EXPLICIT_DAYNIGHT_KE_TABLE_OBSERVED_IN_REVIEWED_PUBLIC_ZHOUXIANG_VOL6 = TRUE
WHOLE_DATONG_TRADITION_ABSENCE = NOT_AUTHORIZED
OTHER_FASCICLES / TONGGUI / ANNUAL_ALMANACS = UNRESOLVED
```

## 4. Consequence for the Sanming 1578 bridge

Zhou Xiang vol6 remains important because it physically demonstrates Datong technical material in circulation immediately before 1578 and directly preserves a 1477 calculation epoch inside a 1569 reprint layer. But the inspected fascicle cannot currently supply the missing `59/41 + daily ladder + change-day` bridge because the target day/night table itself is not present on the reviewed surface.

Therefore the search priority changes from another Datong-titled book to the mechanically relevant carriers: `大統曆通軌 / 大統曆日通軌` 晨昏分立成, actual pre-1578 annual Datong almanacs, and 楊瓚《閑中錄》.

## 5. Tianwen transmission impact

New graph nodes record the 2019 digital surrogate, the Longqing-3/1569 edition layer, and the directly visible 1569/1477 passages. New confirmed edges attach the surrogate to the two direct passages and the 1569 passage to the edition layer.

An explicit non-edge is recorded against `TABLE-SANMING-1578-DAYNIGHT-KE`: the reviewed Zhou Xiang vol6 is **not established** as a direct day/night-table parent. A separate Bei Lin 1477 -> Zhou Xiang 1569 dependency is also withheld as confirmed because the current support is secondary/probabilistic.

## 6. Product adjudication

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_RUNTIME_CANDIDATE=false
RUNTIME_WINNER=false
CANDIDATE_COLLAPSE=false
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 7. Next gate

1. directly acquire/collate `大統曆通軌/大統曆日通軌` surfaces that actually contain `晨昏分`, sunrise/sunset, or day/night standing tables;
2. inspect pre-1578 annual Datong almanacs and `楊瓚《閑中錄》` for the Nanjing `59` cap and Sanming-like change-day fingerprint;
3. continue searching for an explicit historical selection/rounding rule capable of explaining the Batch 12CI `(78,81]/147` threshold.

Research record: `docs/research/ZIWEI-ZHOUXIANG-DAMING-DATONG-1569-1477-PHYSICAL-COLLATION-R1.json`.
