# Fusion Chart Historical Provenance Audit R1 — Batch 12EK

## GK02538《大統曆註》× 1580《庚辰年大統曆》：源图锁定共享字形裁切与字形判定防火墙

Status: **SOURCE-HASH-BOUND FIXED 正/月 CROPS CLOSED / OCR = NONE / TYPE CLASSIFICATION = NONE / 1580 SIZE CLASS UNRESOLVED / CASTING GENERATION UNRESOLVED / EXACT IMPRESSION YEAR UNRESOLVED / NO RUNTIME CHANGE**

## 1. Why this batch

12EH acquired dated whole-page comparators. 12EI added physical-scale metadata. 12EJ removed the title-name subtype shortcut. The remaining evidence problem was reproducibility: a shared-glyph comparison had to be bound to exact source bytes and exact pixel coordinates before any typographic inference could be audited.

12EK closes that evidence layer only.

## 2. Probe artifact

GitHub Actions run `35671323140`, artifact `10671595229`:

```text
gk02538-gyeongjin1580-shared-glyphs-r1
sha256:4bdc7d69457fe7b988286c63028dd2e6afbb0897d99728b1273dae59cb9111b8
```

The probe re-acquired both images and failed hard unless the exact 12EH source SHA-256 values matched.

## 3. Source-bound objects

```text
1580 Gyeongjin tail
1748×2048
SHA256 306b8f03949850c0cedd9575263208ccbd9dc8e6465165b13406ef1918788590

GK02538 0001/002a
1186×2000
SHA256 8458f8a0fd58f23f91139d7d489077472fd7fddb449d9635f6f29df5e2a9b461
```

## 4. Fixed manual glyph locators

The probe uses no OCR. Direct visual review identifies `正` and `月` and records fixed source-pixel boxes.

```text
1580 正  [698,565,754,625]  crop SHA256 435701fe0d243b869d700471106774a62f6b11cc63f7b2b8a5ed13efcf48cf05
1580 月  [698,620,754,680]  crop SHA256 41fab7d68a3d1565a3d74042522cd428ad7b2278a8b88350923264f78a55dc1d

GK 正    [900,315,961,375]  crop SHA256 1f5833438ca3fefe5b8a12301c46a19a5fec563268d2849bcdd70d86a43442d1
GK 月    [900,370,961,431]  crop SHA256 5790ac69eecef028763001e24dc3d604c5890b90ccb6bcf8a0e540f3fac2da8b
```

Context windows are separately hash-bound so the glyphs cannot be detached from their source columns.

## 5. What the direct comparison closes

```text
same glyph identities available for comparison    YES: 正 / 月
source bytes fixed                                YES
source coordinates fixed                          YES
crop outputs hash-bound                           YES
shared-glyph evidence reproducible                YES
```

This is a material improvement over whole-page visual resemblance.

## 6. What it does not close

The artifact intentionally does not infer type family or casting generation. Equal display magnification is only a viewing aid, not physical-scale normalization.

Apparent differences between the 1580 and GK02538 forms can arise from source photography, perspective, inking, wear, paper deformation, different individual sorts of the same type family, or scan processing.

Therefore:

```text
pixel resemblance -> same casting generation      FALSE
pixel difference  -> different casting generation FALSE
fixed crop dimensions -> same physical size class FALSE
```

12EI's GK02538 nominal medium-scale compatibility remains valid, but the 1580 `正/月` occurrences are not yet independently bound to the official 1.2×0.8 cm medium 印曆字 size class.

## 7. Chronology / product consequence

GK02538 subtype, casting generation and exact impression year remain unresolved. Secure pre-1578 surviving physical impression remains false. Exact Sanming-parent vote increment remains 0.

Matrix 198 / audited 166 / MISSING_FROM_PRODUCT 10 / provenance defects 12/12 repaired / chart algorithm defect 0 / reopen 0 / candidate collapse 0. Deterministic product remains CLOSED.

## 8. Next gate

1. bind the 1580 shared-glyph occurrences to a reliable physical type-size class;
2. then add more same-size shared glyphs and normalize by physical scale before type-form adjudication;
3. continue recovery of Kim Sang-Ho 1987 or equivalent object-level subtype diagnostics;
4. keep the pre-1578 Rainwater+Dahan fingerprint search separate.

Research record: `docs/research/ZIWEI-KYUDB-GK02538-GYEONGJIN1580-SOURCE-BOUND-SHARED-GLYPH-CROPS-R1.json`.
