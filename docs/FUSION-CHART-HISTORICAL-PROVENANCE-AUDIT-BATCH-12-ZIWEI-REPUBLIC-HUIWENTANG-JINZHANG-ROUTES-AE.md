# Fusion Chart Historical Provenance Audit R1 — Batch 12AE

## Republic-era Huiwentang physical imprint and Jinzhang catalog/facsimile routes

Status: **HUIWENTANG PHYSICAL IMPRINT DIRECTLY OBSERVED / JINZHANG CATALOG IDENTITY BOUND / JINZHANG IMPRINT NOT DIRECTLY OBSERVED IN REVIEWED PHOTOS / TARGET LATE-ZI LEAF NOT OBSERVED / ZERO TEXTUAL OR HAI-GLYPH VOTES / NO ALGORITHM EFFECT**

## 1. Scope

Batch 12AE continues `HPA-ZDATE-006` after Batch 12AD. It does not reopen deterministic chart algorithms. The batch separates three evidentiary layers that are easy to conflate:

1. a directly photographed Republic-era-looking Huiwentang physical Fullbook set;
2. catalog/facsimile routes that identify a Republic Jinzhang Fullbook edition;
3. modern reformat/reprint surfaces that can locate the target section but are not historical glyph authority.

The purpose is edition-route closure, not source-count voting.

## 2. Huiwentang physical copy

Kongfz public item `520108/4153377684` records `紫薇斗数全书（1-4卷）`, Chen Xiyi, stone printing, thread binding, four volumes and `上海会文堂书局印行`.

A source-emitted large physical photograph was directly reviewed without OCR. Its title surface visibly reads:

```text
陳希夷先生著
紫微斗數全書
上海會文堂書局印行
```

The image SHA-256 is `767f5d01986c8f4a2b655699fce7af50917afd76a34e321ecf8254e6e09a0e9a`.

This upgrades Huiwentang from a generic bibliographic mention to a directly observed physical-imprint route. The public photos do **not** show `《論人生時要審的確》`, so they add no target-text or Hai-glyph vote.

## 3. Jinzhang routes

### 3.1 `術藏` catalog binding

The public `《重刊術藏》` catalog directly places:

```text
術藏 第五十九卷
紫微斗數全書 [宋]陳希夷撰
民國錦章書局石印本 四卷一冊全
三三三
```

Thus the Jinzhang edition is reproducibly bound at modern reprint-catalog level to volume 59 starting at page 333. This is bibliographic identity, not direct target-glyph authority.

### 3.2 Artron physical set

Artron object `1689675` publicly describes a four-volume set as a reproduction based on the Republic Jinzhang lithographic edition. Six source-emitted physical photographs were directly reviewed without OCR. They visibly establish a physical four-volume Fullbook set and expose title/open-text surfaces, but none of the reviewed photographs directly shows a `錦章書局` imprint and none shows the target late-Zi leaf.

Therefore the seller description and photographs must remain two separate evidence layers:

```text
SELLER_JINZHANG_DESCRIPTION=OBSERVED
DIRECT_JINZHANG_IMPRINT_IN_REVIEWED_PHOTOS=NOT_OBSERVED
```

No direct Jinzhang physical-text vote is added.

## 4. Jinyuan modern reformat control

Xinyi's public product page for the Jinyuan edition (`ISBN 9789868759374`) identifies it as a modern reformat. Its public table of contents directly places `論人生時要審的確` at modern printed page 175. The public image set exposes cover and contents pages only; the target body page is not shown.

This is useful as a modern locator but cannot establish the historical Jinzhang wording or glyphs.

## 5. HPA-ZDATE-006 adjudication

Nothing in Batch 12AE changes the direct textual conflict already established by Nanyangtang and the Korea Springgang manuscript.

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
WITHIN_FULLBOOK_HAI_GLYPH_STABILITY=UNRESOLVED
HUIWENTANG_PHYSICAL_IMPRINT=OBSERVED
HUIWENTANG_TARGET_LEAF=NOT_OBSERVED
JINZHANG_CATALOG_IDENTITY=BOUND
JINZHANG_DIRECT_TARGET_LEAF=NOT_OBSERVED
BATCH_12AE_TARGET_TEXT_WITNESS_INCREMENT=0
BATCH_12AE_HAI_GLYPH_WITNESS_INCREMENT=0
NEW_CANDIDATE_FAMILY=NO
CANDIDATE_SELECTION=NO
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
```

The deterministic fusion-chart product remains CLOSED.

## 6. Next evidence gate

The next high-value gate is no longer another generic Republic-edition catalog entry. It is a directly readable target leaf from one of these imprint-bound routes:

- Shanghai Huiwentang physical copy;
- Republic Jinzhang copy/facsimile whose internal imprint is directly visible;
- another independently bound Fullbook edition.

Modern contents pages, seller prose and reprint catalogs may locate that leaf but must not substitute for it.

## 7. Machine evidence

`docs/research/ZIWEI-REPUBLIC-HUIWENTANG-JINZHANG-ROUTES-R1.json`


## 8. Closure execution binding

Batch 12AE state synchronization was executed by fail-closed workflow run `34313376760`. Before committing, that workflow passed the Fusion Chart Historical Provenance Audit R1 machine gate, the Project Continuity State R1 machine gate, and the focused `test_fusion_chart_historical_provenance_audit_matrix_r1.py` suite. It then produced closure commit `a9be70d9635c655c02d4381bc9b4d76435716a63` (tree `6f2a8568f77ca6b044d40bffae04e5909be1270a`). The staging commit's full CI run `34313376716` also completed successfully. This binding records execution provenance only; it adds no textual evidence, no witness vote, and no algorithm effect.
