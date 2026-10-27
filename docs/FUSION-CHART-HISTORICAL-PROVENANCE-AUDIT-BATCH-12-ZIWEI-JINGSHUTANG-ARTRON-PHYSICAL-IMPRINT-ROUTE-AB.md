# Fusion Chart Historical Provenance Audit R1 — Batch 12AB

## 經述堂《紫微斗數全書》实体题页路线与堂号训诂隔离

Status: **NEW PHYSICAL IMPRINT ROUTE DIRECTLY OBSERVED / 經述堂 GLYPHS CLOSED AT TITLE-PAGE LEVEL / TARGET LATE-ZI PAGE NOT OBSERVED / ZERO NEW HAI-GLYPH VOTES / NO ALGORITHM EFFECT**

## 1. Scope

Batch 12AB continues `HPA-ZDATE-006` from Batch 12AA. It does **not** reopen deterministic chart algorithms.

The narrow goals are:

1. resolve the imprint reading on Artron/Taihe Jiacheng 2017 Lot *2036 from the exact source-emitted physical photograph;
2. prevent visual or textual normalization of `經述堂` into the already-known `繼述堂` or `經綸堂`;
3. register the newly observed physical Fullbook imprint route while keeping textual witness weight at zero until `《論人生時要審的確》` is directly collated;
4. record current Kongfz public-picture access boundaries without bypassing login.

## 2. Artron / Taihe Jiacheng Lot *2036

The public lot page identifies:

```text
紫微斗数全书
清刊本
线装1函4册
23.5×15cm
```

The page's own `window.__INITIAL_STATE__` emits a `bigPic` URL whose nested `src` points to the exact auction image object. Research run `34257871010` fetched that exact source-emitted image without identifier guessing.

Binding:

```text
page SHA-256:
94abfdd0310f233c97f9e5481be56b4d396029297af5e592ae6d163867769277

source image:
https://image.artron.net/wd/auction//300/art/35274/2a788545f5a9bd4c0982130a5a41c83b.jpg

image:
1018 × 903 JPEG
162457 bytes
SHA-256:
44c0369f078d27894579b10208f8906ed3592a814a2bc8d58a8f2760090a9685
```

Direct visual review, with **no OCR**, reads the title-page surface:

```text
陳希夷先生著
紫微斗數全書
經述堂藏板
```

The imprint reading is therefore closed at the photographed title-page level as:

```text
經述堂藏板
```

## 3. Philological firewall: 經述堂 ≠ 繼述堂 ≠ 經綸堂

The repository already contains independently evidenced `繼述堂` and `經綸堂` Fullbook routes. Batch 12AB directly observes a third glyph sequence, `經述堂`.

Accordingly:

```text
SILENT_NORMALIZATION_經述堂_TO_繼述堂=FORBIDDEN
SILENT_NORMALIZATION_經述堂_TO_經綸堂=FORBIDDEN
STEMMATIC_EQUIVALENCE=UNRESOLVED
```

This is a version/imprint identity finding only. It does not imply that the three routes have independent text for the target late-Zi passage.

A broader web check also finds `经述堂` used as an edition/imprint label for an unrelated late-Qing work. That secondary control is useful only against treating the observed name as an impossible typo; it is **not** a provenance bridge to this Ziwei copy.

## 4. Target-page boundary

The available Lot *2036 photograph shows a title page and adjacent text leaf. It does **not** show:

```text
《論人生時要審的確》
子時有十刻
上五刻屬昨夜...
```

Therefore:

```text
JINGSHUTANG_PHYSICAL_IMPRINT_ROUTE=REGISTERED
DIRECT_TARGET_LATE_ZI_PAGE=NOT_OBSERVED
INDEPENDENT_TEXTUAL_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
```

No reading of `亥` may be assigned to 經述堂 from this batch.

## 5. Kongfz public-route controls

The exact public picture URLs for object ids `78170971`, `70370885`, and `54804686` were requested normally. All three resolved to Kongfz login surfaces.

No login, authentication bypass, token reuse, identifier guessing, or private-page enumeration was attempted.

Thus the current GitHub-runner boundary is:

```text
KONGFZ_PUBLIC_PICTURE_SURFACE=LOGIN_REDIRECT
CONTENT_ABSENCE_CLAIM=FORBIDDEN
TARGET_PAGE_ABSENCE_CLAIM=FORBIDDEN
WITNESS_INCREMENT=0
```

Search-engine image surfaces may remain useful as secondary locators, but they are not promoted to direct target-text authority.

## 6. HPA-ZDATE-006 adjudication after Batch 12AB

The controlling textual state remains:

- Nanyangtang Fullbook directly preserves explicit `昨夜亥時 / 今日子時`.
- Korea Springgang manuscript directly preserves `昨夜 / 今夜` without explicit `亥` in the exact target span.
- 經述堂 is now a directly observed additional Fullbook physical imprint route, but its target late-Zi page is still unseen.

Therefore:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
WITHIN_FULLBOOK_HAI_GLYPH_STABILITY=UNRESOLVED
NEW_PHYSICAL_IMPRINT_ROUTE_BATCH_12AB=1
NEW_TEXTUAL_WITNESS_BATCH_12AB=0
NEW_HAI_GLYPH_WITNESS_BATCH_12AB=0
NEW_CANDIDATE_FAMILY=NO
CANDIDATE_SELECTION=NO
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
```

The deterministic fusion-chart product remains **CLOSED**.

## 7. Next evidence gate

The highest-value next step is no longer merely to find another catalog name. It is to obtain the target leaf from a physically bound Fullbook copy whose edition identity is known.

Priority now includes:

```text
經述堂
敦化堂
繼述堂
經綸堂
文誠堂
輝縣市博物館藏清刻本
or another independently bound Fullbook physical witness
```

For the new 經述堂 route specifically, search should prioritize another sale/library/facsimile instance that exposes later leaves or the exact `《論人生時要審的確》` section.

Only after the target wording is sufficiently bounded across Fullbook physical editions should runtime time-standard binding be adjudicated.

## 8. Execution binding

Probe execution:

```text
head=a3936aa698a4137c83c4e777682f1e6767856901
run=34257871010
job=102168131300
artifact=10068625939
artifact ZIP SHA-256=85f5fbe89ec450979646556bcb0ceeffc714441c0374a591b2b1fc4f9afb875e
```

Evidence artifact:

`docs/research/ZIWEI-JINGSHUTANG-ARTRON-PHYSICAL-IMPRINT-ROUTE-R1.json`

This execution binding adds provenance reproducibility only and authorizes no algorithm change.
