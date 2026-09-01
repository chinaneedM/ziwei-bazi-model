# Ziwei Laiyin Runtime Denial R1

## Scope

This document records a canonical runtime denial for 来因宫. It is not a runtime feature specification and does not authorize a Laiyin palace field in the deterministic chart.

Canonical source: `sources/canonical/S01_统一输入排盘与坐标冻结库.txt`, section `20.1 来因宫` (runtime materialized in `sources/canonical-runtime/S01/segment-0001.txt`).

## Canonical permission state

S01 freezes the following permission triple:

```text
LAIYIN_RAW_INPUT_PRESERVE=YES
LAIYIN_RUNTIME_PERMISSION=NO
LAIYIN_EVIDENCE_PERMISSION=NO
```

The consequences are explicit:

- a source/chart label may be preserved as raw text;
- no runtime palace is created from it;
- no evidence node is created from it;
- it does not participate in themes, transformations, temporal layers, special topics, scoring, or conflict resolution.

## Product boundary

The deterministic Ziwei + Bazi charting product MUST NOT add a computed Laiyin palace field merely for compatibility parity with external software. A future change requires the canonical runtime permission itself to be revised through source governance; product screenshots or compatibility fixtures alone are insufficient.

This denial is independent from already released standard twelve-palace geometry and must not alter Life Palace, Body Palace, palace Ganzhi, transformation topology, temporal frames, or application hashes.
