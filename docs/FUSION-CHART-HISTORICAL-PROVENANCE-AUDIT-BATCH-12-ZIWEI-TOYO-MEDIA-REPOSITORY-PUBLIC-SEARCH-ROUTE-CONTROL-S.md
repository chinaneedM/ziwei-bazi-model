# Fusion Chart Historical Provenance Audit R1 — Batch 12S

## Toyo Bunko Media Repository public search-route control

Status: **FIRST-PARTY MEDIA REPOSITORY SEARCH ROUTES BOUND / GENERAL + TOYO COLLECTION SEARCHES EXPLICITLY SHOW 0 件 / NO CONCRETE ITEM OR DOCUMENT OBJECT RETURNED / NO DIGITIZATION-ABSENCE CLAIM / NO TARGET PAGE / ZERO TEXTUAL-GLYPH VOTES / NO ALGORITHM REOPEN**

Batch 12S closes the post-12R Toyo Media Repository probes as a **current public digital-access search boundary**, not as a negative claim about Toyo Bunko's physical holdings, internal digitization, or the existence of the target passage.

### 1. First-party public repository and source-emitted routes

The controlling capture is workflow run `34221594363`, artifact `10053963935`, ZIP SHA-256 `533efe6a70dbc7f1488adf13199e47a02b908ac3c184bb54be26b2075adedf0a`.

The provider pages themselves expose:

- `/s/main/item` → advanced search `/s/main/item/search?sort_by=created&sort_order=desc&page=1`;
- `/s/main/collection/top` → collection-restricted advanced search with `item_set_id=42942`;
- the actual Omeka text field `property[0][text]` with joiner `and` and relation type `in`.

No item ID, document ID, API route, IIIF identifier, or media identifier was guessed or enumerated.

### 2. Ten valid target searches

Five target terms were submitted in both scopes:

1. `新刊希夷陳先生紫微斗數全集`
2. `紫微斗數`
3. `VII-3-157`
4. `Ⅶ-3-157`
5. `TOYO_1646`

This yields ten valid source-emitted queries. Every result page returned HTTP 200, visibly displayed `0 件` (twice in the rendered page structure), exposed zero concrete `/item/{id}` or `/document/{id}` resource links, and contained zero parsed resource nodes.

Therefore the narrow, reproducible adjudication is:

```text
CURRENT_PUBLIC_TOYO_MEDIA_REPOSITORY_TARGET_SEARCH_RESULT = ZERO_ITEMS_RETURNED
CONCRETE_TARGET_RESOURCE_OBJECT_RETURNED = NO
TARGET_PAGE_OBSERVED = NO
```

### 3. Parser-hardening boundary

Runs 2 and 3 are retained only as probe history. They exposed two parser defects:

- a pagination `page` control was initially treated as a query field;
- the `詳細検索` self-link under `/item/search` was initially misclassified as an item resource.

Both false positives were removed before the controlling run. Batch 12S relies only on run 4's reserved-route exclusion plus resource-node checks.

### 4. What this does **not** prove

The public-repository non-hit does **not** establish any of the following:

- that `VII-3-157` has never been digitized;
- that Toyo Bunko has no internal or non-indexed image;
- that the target `五凶神` page is absent from the physical object;
- that a different public catalogue or future repository ingest cannot expose it.

It is an access-surface result only and contributes no textual or glyph vote.

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

The next gate remains a directly readable `五凶神` target page from an actual first-party Toyo image resource, an explicitly authorized reading/reproduction route, or another independently bound witness with page-level provenance.

Machine evidence: `docs/research/ZIWEI-TOYO-MEDIA-REPOSITORY-PUBLIC-SEARCH-ROUTE-CONTROL-R1.json`.
