# Fusion Chart Historical Provenance Audit R1 — Batch 12HU

## FID070 同一实物“十行十七字 vs 10行16字”行款著录权威三角校验

Status: **HISTORICAL 17/23 DOUBLE ATTESTATION / CURRENT NLC 16/23 DIRECT METADATA / PHYSICAL LINE-COUNT CLOSURE STILL PENDING / NO DEFECT INCREMENT / ZERO PRODUCT OR MATRIX CHANGE**

## 1. Why this batch exists

Batch 12HS left one exact-copy metadata tension deliberately unresolved:

```text
1987 北京图书馆：十行十七字 / 小字双行二十三字
current NLC：10行16字 / 小字双行23字
```

Batch 12HP had already closed FID `412004000070` to the Tieqin old-collection witness at a high-confidence multilayer catalog/donor-provenance/bibliographic-fingerprint level. Therefore this is not an object-identity problem. It is a **format-description authority problem**.

## 2. Historical Tieqin catalog control: 17 / 23

The public transcription of the Qing `《铁琴铜剑楼藏书目录》` entry for the same 60-juan work records:

> 每半叶十行，行十七字。注疏皆双行，行廿三字。

It also binds the entry to the old Huang-family `百宋一廛` provenance and reasons that the surviving impression is Yuan-period.

This layer is historical object-description evidence. In this batch it is **not** promoted to direct physical-glyph authority because the exact manuscript/catalog leaf was not newly re-collated here.

## 3. 1987 Beijing Library direct catalog control: 17 / 23

The hash-bound 1987 catalog target on PDF p.104, already directly reviewed without OCR, describes book number `3288` as:

```text
元刻明修本
三十二冊
十行十七字
小字雙行二十三字
```

Thus `17/23` is not a single later transcription artifact. It is independently present in the 1987 institutional catalog layer.

## 4. Current NLC detail control: 16 / 23

Batch 12HS directly recovered the current NLC detail payload for:

```text
UID  = UCS01003868188
SYS  = 002838237
905s = 03288
FID  = 412004000070
```

The current format note is:

```text
10行16字，小字雙行23字，白口，左右雙邊。
```

The current `16` is therefore a real current metadata value, not a project transcription guess.

## 5. Zhang Lijuan physical-research control

The official NOPSS project report states that Zhang Lijuan physically investigated the NLC Tieqin-old-collection ten-line witness previously cataloged as `元刻明修本`, and re-adjudicated it as `元刻元印十行本`, reporting no Ming repair traces.

This matters negatively: the project currently has no basis to explain the `17 → 16` discrepancy by asserting that Ming repair physically changed the line format.

The 2018 article itself has **not** yet been recovered in full, so this batch does not claim that Zhang printed either 16 or 17.

## 6. Authority adjudication

The current evidence stack is:

```text
Tieqin historical catalog : 10 / 17 / 23
1987 Beijing Library      : 10 / 17 / 23
current NLC               : 10 / 16 / 23
```

Two dimensions are stable across all three layers:

- ten lines per half leaf;
- 23 characters per double-line commentary line.

Only the main-text character count differs.

The evidence therefore moves the tension from a neutral `17 vs 16` note to:

```text
UNRESOLVED_HIGH_PRIORITY_METADATA_TENSION
evidence direction = LEAN 17
physical closure   = NOT YET
```

This is **not** PROV-DEFECT-016. A direct, reproducible count on multiple clean representative lines, or an equivalent object-specific scholarly/source record, is still required before calling the current NLC `16` a confirmed metadata defect.

## 7. Candidate explanations kept open

The following remain admissible until direct physical counting or Zhang's full article closes them:

- current NLC `16` is a catalog/transcription error;
- the sources use different conventions for what is counted as a main-text character position;
- the physical copy has irregular/mixed 16–17-character lines and different catalogers summarized it differently;
- an historical description was inherited from the edition family rather than recounted leaf by leaf;
- another catalog-normalization step remains unrecovered.

No winner is selected.

## 8. Product and accounting consequence

No deterministic chart rule, runtime candidate, Matrix row, transmission-genealogy topology, algorithm reopen or candidate collapse changes.

```text
Matrix rows = 198
audited rows = 166
MISSING_FROM_PRODUCT = 10
provenance defects = 15 / 15 repaired
confirmed chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```

## 9. Next gate

1. directly count multiple clean representative main-text lines on FID070 with a reproducible page/leaf locator;
2. recover Zhang Lijuan 2018 full text and inspect its exact format/shelfmark/book-number statements;
3. continue the independent target-specific `3368 → 3288` catalog-card/correction/preparation-record search;
4. continue the exact Qu donation/accession batch/date search without collapsing aggregate chronology into the target object.
