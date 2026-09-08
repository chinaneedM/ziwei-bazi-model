# Fusion Chart Historical Provenance Audit R1 — Batch 12X

## Jiwen 1982/1999 old-print reproduction route + Dayuan 2012 manuscript copy-text route

Status: **TWO NEW COLLATION ROUTES BOUND / JIWEN ZHOU-ZUYONG PRIVATE OLD-PRINT REPRODUCTION PROVENANCE EXPOSED / DAYUAN 434-PAGE HANDWRITTEN COPY-TEXT SAMPLES DIRECTLY REVIEWED / `五神` DIRECTORY SURFACE QUARANTINED FROM `五凶神` / TARGET PAGE NOT OBSERVED / ZERO TEXTUAL VOTE / NO ALGORITHM EFFECT**

### 1. 集文 1982 → 1999 route

The public 1999 集文 product page (`ISBN 9579789800 / 9789579789806`) reproduces 周祖勇's preface and directly states that he supplied a privately held six-volume old edition for reproduction. The wording identifies it as a `古本明版` and parenthetically as a `清同治九年木刻再版`. The preface itself is dated `中華民國七十一年歲次壬戍孟春`, tying the reproduction project back to 1982.

Google Books separately exposes public HTML for volume `YOwLlQEACAAJ`, the 1982 集文 record. The API metadata endpoint was rate-limited with HTTP 429 in this run, so no API-only field is promoted beyond the public record already located.

This materially adds a **private-copy reproduction route** for the 1870 received edition family. It does not prove whether 周祖勇's physical copy is the same exemplar as, or independent from, the SNU Ilsa copy. Therefore it is not counted as an independent textual witness until a target page and copy-level provenance are collated.

### 2. 大元 2012 精鈔本 route

Two public retailer surfaces consistently bind:

- `十八飛星策天紫微斗數全集精鈔本`;
- 大元書局;
- ISBN `9789866171680`;
- main text `六卷`;
- main-text extent `434頁 / 鈔本四三四頁`.

A public National Central Library acquisition-list PDF independently binds the same ISBN/title/publisher as a 2012 acquisition record.

More importantly, the Xinyi public product page directly emits large internal sample images. These were reviewed visually without OCR. The samples establish that this route contains a genuine handwritten/copy-text layer rather than merely a modern prose summary. One title/imprint sample directly shows:

```text
十八飛星策天紫微斗數全集
大宋扶搖子白雲先生陳摶著
南州草坪徐良弼校正
金陵益軒唐謙繡梓
```

Other samples show handwritten vertical body-text pages and printed contents pages. None of the reviewed public samples is the `五凶神` target page and none exposes the late-Zi target sentence.

### 3. Philological firewall: `五神` ≠ automatically `五凶神`

The NCC/Xinyi public directory text for the end of volume four contains the surface:

```text
五神 百字千金訣
```

Other received-text routes locate a heading `五凶神`. This batch does **not** silently normalize `五神` into `五凶神`.

Until the underlying volume-four page is directly observed, the possibilities include at least:

- a directory-level omission or transcription defect;
- a genuine title variant;
- a formatting boundary in which `五神` belongs to another heading construction;
- modern retailer transcription noise.

Accordingly:

```text
五神_TO_五凶神_MECHANICAL_EQUIVALENCE=NOT_AUTHORIZED
DIRECT_TARGET_PAGE_REQUIRED=YES
```

This is exactly the kind of case where philology must precede rule identity.

### 4. Evidence boundary

Research run `34240652003` / artifact `10061841718` / ZIP SHA-256 `022d32ef5cb09043ea8b662a13b8a45d09c596e02cd612d673da1c7adde8d7ca` captured the reviewed public routes and source-emitted images. No login, purchase, paid content, copy request, or access-control bypass was attempted.

The evidence supports two new acquisition/collation paths, but neither supplies the decisive physical target page:

```text
JIWEN_COPY_ROUTE=BOUND_TARGET_PAGE_PENDING
DAYUAN_434_PAGE_COPY_TEXT_ROUTE=BOUND_TARGET_PAGE_AND_STEMMA_PENDING
DIRECT_FIVE_XIONG_SHEN_PAGE=NOT_OBSERVED
INDEPENDENT_TEXTUAL_WITNESS_INCREMENT=0
```

### 5. Rule effect

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
DIRECT_INDEPENDENT_HAI_GLYPH_WITNESS_ADDED=0
NEW_CHART_RULE_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
```

The deterministic product remains CLOSED. The next high-value gate is a directly readable volume-four `五凶神` page from the 集文 reproduction, the 大元 434-page copy-text, SNU v4, Hanyang v4, or another copy with sufficiently bound physical/stemmatic provenance.

Machine evidence: `docs/research/ZIWEI-JIWEN-1982-1999-AND-DAYUAN-2012-COPY-TEXT-ROUTES-R1.json`.
