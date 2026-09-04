# Fusion Chart Historical Provenance Audit R1 — Batch 08A

## Ziwei dynamic auxiliaries: authority scope and source-layer decomposition

Status: **AUDITED / DYNAMIC AUXILIARY DECOMPOSITION / PROVENANCE LABEL REPAIR / NO ALGORITHM REOPEN**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
PROVENANCE_DEFECT_COUNT=7
```

## 1. Audit question

A natal placement table does not by itself authorize regenerating the same star at Daxian, annual, monthly, daily or hourly layers. Batch 08A separates placement geometry, temporal-layer authorization, school scope and compatibility behavior.

## 2. Evidence

The received 《紫微斗数全书》 explicitly contains `安流禄流羊流陀诀论流年太岁` and gives a 己丑 flow-year example: 流禄午、流羊未、流陀巳. This closes the annual LuCun/QingYang/TuoLuo mechanism.

`EXT-WANGTINGZHI-ANXING-2013`, independently identified by the UIBE library catalog as 王亭之《安星法及推断实例》, 复旦大学出版社 2013.06, ISBN 978-7-309-09665-1, is used only as a modern Zhongzhou-school witness. It documents flowing Kui/Yue/LuCun/Yang/Tuo, the separate 流昌/流曲 table, and 运马/流马 temporal bases.

## 3. Verdicts

- Annual 流禄/流羊/流陀: `HISTORICALLY_SUPPORTED`.
- Daxian and fine-layer 禄羊陀: `SUPPORTED_BUT_SCHOOL_SPECIFIC`.
- 流文昌/流文曲: `SUPPORTED_BUT_SCHOOL_SPECIFIC`.
- Strict dynamic Kui/Yue reuse: school-supported project method; parent remains disputed because alternative tables exist.
- Wenmo dynamic Kui/Yue: `MODERN_COMPATIBILITY_ONLY`.
- Daxian 运马 and annual 流马: `SUPPORTED_BUT_SCHOOL_SPECIFIC`.

The runtime correctly does not extend Tianma to Month/Day/Hour.

## 4. Provenance defect 007

The strict dynamic Kui/Yue candidate previously exposed `authority_status=CANONICAL_SOURCE_TABLE`. That contradicts the active authority policy because S01 is project research corpus, not infallible historical authority.

Forward-only repair:

`S01_STRICT_PROJECT_CORPUS_METHOD`

Since authority status participates in hashes:

- `TEMPORAL_KUI_YUE_ALGORITHM_VERSION`: 1.0.0 → 1.0.1
- `TEMPORAL_AUXILIARY_CANDIDATE_SET_HASH_VERSION`: 1.1.0 → 1.2.0

No coordinate, method ID, candidate membership, ranking or winner changed.

## 5. Matrix decomposition

Batch 08A adds HPA-ZAUX-001..008 and audits parents HPA-ZT-009..012.

```text
NEW_GRANULAR_RULE_ROWS=8
NEWLY_AUDITED_EXISTING_PARENT_ROWS=4
TARGET_TOTAL_MATRIX_ROWS=153
TARGET_TOTAL_AUDITED_ROWS=107
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=7
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
PRODUCTION_COORDINATE_CHANGE_COUNT=0
```

Next: annual frame semantics, Five-Tigers month Ganzhi, flow-day palace sequence, flow-hour candidates, and leap-month temporal policy.
