# Fusion Chart Historical Provenance Audit R1 — Batch 12G

## Qing Lianyuange 《紫微斗數全集》 late-Zi parallel lineage

Status: **LIANYUANGE COLLATION ROUTE CLOSED / RECEIVED QUANJI PARALLEL BOUND / PHYSICAL TARGET PAGE NOT OBSERVED / NO NEW CANDIDATE / NO ALGORITHM REOPEN**

Batch 12G asks whether the late-Zi ten-ke rule is confined to the received 《紫微斗數全書》 lineage or whether a distinct 《紫微斗數全集》 lineage preserves a parallel upper/lower-half distinction.

## 1. Qing Lianyuange Quanji route

Heart-One's official Jielan publication page directly states that the point-collated edition used a 虛白廬藏【清】連元閣刊本《紫微斗數全集》 together with the Qing Wenchengtang Fullbook. The same page states that missing tail material in the Jielan base was supplemented from the Lianyuange Quanji.

Research workflow run `34133129317` / artifact `10022892119` independently captures the public Google Books index of volume `rZRcCwAAQBAJ`:

- `連元閣` → PT176/PT177;
- `紫微斗數全集` → PT175/PT176/PT177/PT205;
- PT176 explicitly labels the Lianyuange witness `《連本斗數全集》`;
- PT177 says missing Jielan tail material is supplied from the Lianyuange Quanji;
- PT205 shows that the editorial layer can quote a specific `《斗數全集》作……` variant elsewhere.

Therefore the Qing Lianyuange Quanji collation route is directly bound at publisher/editorial-index level.

## 2. Received Quanji late-Zi transcription

A public DestinyNet transcription titled 《紫微斗數全集》 contains under `五凶神`:

```text
凡論人命有稱兩時者可詳之，子有十刻，
上五刻屬昨夜，下五刻屬今夜子。如今夜子即上五刻。
```

This is retained only as a **secondary received-text control**. It is not a facsimile and cannot establish original punctuation, glyph form, or exact edition identity.

## 3. Jielan index target search

Exact searches for the received Quanji late-Zi phrases returned zero across all three public SearchWithinVolume2 request forms. These zero results are not negative textual proof.

The shorter query `子有十刻` returned PT88 in all three forms, but the returned snippet does not contain the query phrase and is unrelated to the target. It is therefore treated as an index mismatch, not positive evidence.

Thus:

```text
LIANYUANGE_PHYSICAL_TARGET_PAGE=NOT_OBSERVED
LIANYUANGE_TARGET_LATE_ZI_TEXT=NOT_DIRECTLY_BOUND
ZERO_RESULT_NEGATIVE_PROOF=FORBIDDEN
```

## 4. Philological adjudication

The Quanji received wording is relevant, but it is **not mechanically identical** to the Nanyangtang Fullbook rule.

Nanyangtang directly reads:

```text
上五刻屬昨夜亥時，下五刻屬今日子時
```

The Quanji received transcription instead says:

```text
上五刻屬昨夜，下五刻屬今夜子
```

The shared semantic core is an upper/lower-half distinction tied to different night/day relations. The critical difference is that the Quanji transcription does **not** directly say the upper half is reclassified as `亥時`.

Therefore Batch 12G does not create a new candidate row and does not backfill HPA-ZDATE-006 authority.

```text
QUANJI_PARALLEL_LINEAGE=RECEIVED_TRANSCRIPTION_BOUND_PHYSICAL_TARGET_PENDING
NEW_CANDIDATE_ROW=NO
HPA-ZDATE-006_HAI_RECLASSIFICATION_FROM_QUANJI=NOT_AUTHORIZED
```

## 5. Effect on product and accounting

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
HAI_GLYPH_STABILITY_ACROSS_PHYSICAL_EDITIONS=UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES
RUNTIME_TIME_STANDARD_BINDING=UNRESOLVED
CANDIDATE_SELECTION_AUTHORIZED=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0

MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
```

Machine evidence: `docs/research/ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-R1.json`.

The deterministic fusion-chart product remains CLOSED.
