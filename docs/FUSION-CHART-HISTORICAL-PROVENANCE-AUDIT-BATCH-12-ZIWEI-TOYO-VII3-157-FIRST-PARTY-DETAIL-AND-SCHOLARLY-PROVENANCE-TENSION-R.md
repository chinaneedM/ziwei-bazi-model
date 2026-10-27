# Fusion Chart Historical Provenance Audit R1 — Batch 12R

## Toyo Bunko VII-3-157 first-party detail + scholarly provenance tension

Status: **TWO FIRST-PARTY BIBLIOGRAPHIC DETAIL RECORDS BOUND / PHYSICAL MULTIPLICITY UNRESOLVED / CURRENT ACCESS POLICY SCOPED / NCKU GENEALOGY TENSION PRESERVED / NO TARGET PAGE / ZERO TEXTUAL-GLYPH VOTES / NO ALGORITHM REOPEN**

Batch 12R closes the post-12Q Toyo Bunko detail-route probes without changing chart-rule accounting.

### 1. Toyo Bunko first-party detail records

The public search result itself emits POST forms to `show_detail_open_kanseki.php`; no target ID was guessed or enumerated.

| targetid | 請求記号 | 書名 | 出版事項 | 冊数 | detail SHA-256 |
|---|---|---|---|---:|---|
| `502596` | `VII-3-157` | 新刊希夷陳先生紫微斗數全集 | 寫本 | 1册 | `f459ab7e651eec283d8c3b00be633ba36037ba13dc0f7d94c30ad5d17198d960` |
| `471894` | `VII-3-157` | 新刊希夷陳先生紫微斗數全集不分卷 | 鈔本 | 1册 | `b6a3e768d779fd0a5895b8936da9326ca8c4475513c5b78301ab1776193ae655` |

The two bibliographic target IDs do **not** establish two independent physical witnesses. Their physical-object relationship remains unresolved, and they receive zero witness-count increment.

Neither detail page exposes `五凶神`, the target late-Zi sentence, `亥`, `金陵益軒`, or a 1942 acquisition statement.

The detail template includes a generic notice that records whose request-number field displays `貴重書` require advance booking. The actual request-number field for both records displays only `VII-3-157`; therefore the generic notice must not be promoted into an item-specific rare-book classification.

### 2. Current access-policy scope

The current Toyo Bunko first-party notice dated 2025-11-28 says that, during facility renovation, reading is currently reservation-only. This dated notice is treated as the current access override over the general reading guidance.

The controlling GitHub runner could not obtain HTTP responses from the `.or.jp` policy pages. Batch 12R therefore records the policy as **first-party web verified in the research session, runner snapshot unavailable**, rather than fabricating a machine capture.

No reading, reservation, or reproduction request has been submitted. Any such external action remains an explicit user-authorization boundary and may require personal/contact information.

### 3. NCKU 2021 edition-genealogy tension

The official NCKU PDF was fetched successfully in run `34220050125`:

- PDF SHA-256: `17d0089c3328253230cb2f110ac40527abe41fbb97183483215a5e633e5b2e2e`
- size: 2,105,566 bytes
- 42 PDF pages
- OCR used: **false**

Direct visual review of printed p.60 / PDF p.28 preserves a table row for `新刊希夷陳先生紫微斗數全集` with `金陵益軒唐謙梓` and the note `昭和17年（民國31年，1942）6月收入東洋文庫`.

This is modern scholarly genealogy/provenance. It does not prove that the current Toyo object is an original Jinling Yixuan print. The relation remains:

`SCHOLARLY_ATTRIBUTION_UNRESOLVED_AS_PHYSICAL_PRINT_VS_MANUSCRIPT_EXEMPLAR_OR_COPIED_IMPRINT_STATEMENT`.

### 4. KOSTMA cross-catalog bridge

KOSTMA `TOYO_1646` and Toyo target `502596` share the exact title and call number, so the relation is strongly suggested. Because neither current record exposes an explicit cross-system ID bridge, physical-object identity is not declared resolved.

### 5. Adjudication

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

The next gate is a directly readable `五凶神` page through a first-party Toyo Media Repository/new Hanseki image route, an explicitly authorized reading/reproduction route, or another independently bound witness with page-level provenance.

Machine evidence: `docs/research/ZIWEI-TOYO-VII3-157-FIRST-PARTY-DETAIL-AND-SCHOLARLY-PROVENANCE-TENSION-R1.json`.
