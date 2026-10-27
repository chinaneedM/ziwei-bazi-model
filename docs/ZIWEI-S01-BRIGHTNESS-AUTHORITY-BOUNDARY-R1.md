# Ziwei S01 Brightness Authority Boundary R1

## Scope

This document locks the S01 authority boundary for Ziwei brightness labels. It does not replace or remove the existing operational `DignityAnnotation` registry; it prevents that operational annotation from being mislabeled as S01 canonical frozen-chart brightness.

Canonical source: `sources/canonical/S01_统一输入排盘与坐标冻结库.txt`, section `十二、亮度、夹拱与结构标记` (runtime materialized in `sources/canonical-runtime/S01/segment-0001.txt`).

## Canonical permission state

S01 freezes only brightness already supplied by the source chart and explicitly denies recalculation:

```text
BRIGHTNESS_PRIMARY_INPUT=FROZEN_CHART
S01_RECALCULATE_BRIGHTNESS_PERMISSION=NO
SOURCE_BRIGHTNESS_REFERENCE_CAN_OVERWRITE=NO
```

Consequences:

- source-chart brightness may be preserved as a frozen input fact;
- S01 does not authorize deriving brightness when the source chart did not provide it;
- a reference table must not overwrite frozen source-chart brightness;
- a conflict between a reference and the frozen chart remains a conflict fact rather than an automatic winner.

## Relationship to current runtime dignity

`src/fortune_training/ziwei_chart/dignity.py` releases a project-owned operational seven-grade `DignityAnnotation` rule set. That annotation is useful deterministic product data, but its operational rule set and calibration provenance are not the same authority class as S01 frozen-chart brightness.

Therefore the product MUST NOT:

- relabel an operational dignity grade as `S01 canonical brightness`;
- claim that S01 authorizes recalculating a missing source-chart brightness value;
- allow an external product/reference table to silently overwrite frozen-chart brightness;
- collapse a source/reference conflict into an automatic winner.

A future S01 brightness-input ingestion layer may preserve raw/frozen labels and conflicts, but must remain distinct from the operational dignity annotation unless source governance explicitly establishes a deterministic authority bridge.
