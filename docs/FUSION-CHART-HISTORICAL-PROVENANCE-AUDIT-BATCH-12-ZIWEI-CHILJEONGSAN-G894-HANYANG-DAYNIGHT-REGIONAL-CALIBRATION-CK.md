# Fusion Chart Historical Provenance Audit — Batch 12CK

## Scope

This batch closes a regional-calibration control that emerged after Batch 12CJ. It asks whether the directly dated 1444 Joseon `《七政算內篇》` witness preserves a Hanyang-localized sunrise/sunset and day/night-ke table, and whether that localization changes how we should read the 1447 Nanjing/Beijing standards and the later 1578 `《三命通會》` 59/41 display.

This is historical provenance / transmission-genealogy work only. It does **not** reopen deterministic charting and does not select any runtime candidate.

## 1. Bibliographic firewall: G894 is a dated 1444 witness

The Seoul National University Kyujanggak provider catalog identifies:

```text
title: 七政算內篇
call number: 奎貴894-v.1-3
compilers: 李純之、金淡（朝鮮）受命編
edition: 甲寅字
publication year: 1444
provider book_cd: GK00894_00
```

The 1444 attribution comes from the provider bibliography. It is not inferred from image filenames or from a modern surrogate.

## 2. Direct physical table collation: no OCR for glyph claims

GitHub Actions run `34937262190` fetched provider pages `039b..044b` from volume `0003`. Every image path was parsed from the Kyujanggak renderer response for the requested page ID; filename-sequence inference is forbidden. Artifact `10383449874` has digest `sha256:a3941a77566bb2ac2a963ed376c5ba5023e290e7e4a319c8c2dc4d0a67742f1c`.

Key direct readings:

```text
040a  二至後日出入晝夜辰刻 / 冬至後
      初日 日出辰初一刻 日入申正二刻
      晝三十九刻 / 夜六十一刻

042a  一百五十九日
      晝六十刻 / 夜四十刻

042a  夏至後
      初日 日出寅正二刻 日入戌初一刻
      晝六十一刻 / 夜三十九刻
```

Therefore the directly reviewed Hanyang table is a 100-ke regional table with solstitial extremes:

```text
winter: 39 / 61
summer: 61 / 39
```

## 3. Official Sillok article binding and locator repair

The earlier research locator scanned a guessed `wda_50018...` prefix. That guess was wrong. It was never admissible evidence and must not be reinterpreted as a negative historical result.

The corrected provider route is `wda_50034...`. Run `34939861102` proves:

```text
wda_50034001
  世宗實錄 158卷 / 內篇 下卷 / 二至後日出入晝夜辰刻 / 冬至後
  太白山事故本 62책 158권 28장 A면

wda_50034002
  世宗實錄 158卷 / 內篇 下卷 / 二至後日出入晝夜辰刻 / 夏至後
  太白山事故本 62책 158권 29장 B면
```

The official institutional transcription on `wda_50034002` states:

> 日出入隨處各異，諸曆不同。內篇據漢陽日至之晷，推求至差，得每日日出入，晝夜刻分，定爲本國所用。

This wording is used as an official transcriptional witness. The table numerals above are independently adjudicated from the G894 physical-page images.

## 4. Historical adjudication: locality is explicit, not retrospective

The combined evidence allows a stronger claim than mere numerical comparison:

1. the 1444 physical G894 witness supplies the Hanyang table and its 39↔61 extrema;
2. the official Sillok text explicitly says sunrise/sunset differ by place and that the Inner Chapter derives its daily values from the **Hanyang solstitial gnomon** for domestic use;
3. the already audited 1447 Ming memorial directly distinguishes Nanjing `59` ke from Beijing `62` ke.

Hence `region/locality` is an explicitly attested historical variable in 15th-century East-Asian day/night-ke practice. A single universal solstitial-ke value is rejected.

## 5. Consequence for the Sanming 59/41 ancestry problem

The result does **not** make Hanyang a parent of the 1578 `《三命通會》` table. Quite the opposite:

```text
1444 Hanyang: summer 61/39
1447 Nanjing: 59/(41 complement)
1447 Beijing: 62/(38 complement)
1578 Sanming: summer 59/41
```

Hanyang is therefore a high-value parallel regional negative control. It proves that generic phrases such as “traditional day/night-ke table” or mere proximity to 60 cannot establish a direct lineage. The Sanming search should now privilege securely localized Nanjing/Jiangnan or other `59`-cap intermediaries that also reproduce its step-ladder/change-day fingerprint.

This does not erase the Huqianjing structural ancestry candidate from Batch 12CJ. It sharpens the missing bridge: a viable intermediary must explain **both** the inherited one-ke operational family **and** the regional/quantization move to a 59-ke cap.

## 6. Tianwen transmission impact

New graph nodes:

```text
PHYSICAL-COPY-CHILJEONGSAN-NAEPYEON-G894-1444
PASSAGE-SEJONG158-HANYANG-LOCAL-CALIBRATION
STANDARD-HANYANG-61KE-1444
```

New edges:

```text
G894 physical copy
  --ATTESTS--> Hanyang 61-ke regional standard

Sejong 158 locality passage
  --ATTESTS--> Hanyang 61-ke regional standard

Hanyang 61-ke regional standard
  --PARALLEL_COEXISTS_WITH--> Nanjing 59-ke 1447 standard
```

No transmission direction between Hanyang and Nanjing is inferred. No Hanyang -> Sanming direct-copy edge is asserted.

## 7. Product adjudication

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
UPPER_ZI_TO_HAI_VOTE_INCREMENT=0
NEW_RUNTIME_CANDIDATE=false
RUNTIME_WINNER=false
CANDIDATE_COLLAPSE=false
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

The failed `wda_50018` locator is a research-tool defect only. It is not a product/provenance-metadata defect-counter increment.

## 8. Next gate

1. search pre-1578 Nanjing/Jiangnan or another securely localized intermediary that combines a Huqian-style intra-term one-ke ladder with a `59`-ke cap or Sanming-like change-day fingerprint;
2. search for an explicit historical selection/rounding instruction capable of explaining the Batch 12CI `(78,81]/147` precision-to-coarse threshold;
3. continue the independent Fullbook upper-five-ke -> previous-night Hai lineage without conflating it with seasonal-table ancestry.

Research record: `docs/research/ZIWEI-CHILJEONGSAN-G894-HANYANG-DAYNIGHT-REGIONAL-CALIBRATION-R1.json`.
