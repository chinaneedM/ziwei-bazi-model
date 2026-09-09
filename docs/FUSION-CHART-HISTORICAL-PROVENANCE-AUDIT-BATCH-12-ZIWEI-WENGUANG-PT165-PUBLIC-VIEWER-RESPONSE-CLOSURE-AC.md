# Fusion Chart Historical Provenance Audit R1 — Batch 12AC

## 文光堂合刊本 PT165 公开 Viewer 响应闭包

Status: **PUBLIC PAGE OBJECT CONFIRMED / SEARCH INDEX TEXT PRESERVED / VIEWER RUN+CLICK3 RETURN NO SOURCE-EMITTED TARGET IMAGE / NO PHYSICAL GLYPH AUTHORITY / ZERO NEW TEXTUAL OR HAI VOTES / NO ALGORITHM EFFECT**

## 1. Scope

Batch 12AC continues `HPA-ZDATE-006` after Batch 12AB. It does **not** reopen any deterministic chart algorithm.

This batch closes a specific ambiguity left by the 2017 Heart-One combined Wenguangtang facsimile route:

1. distinguish SearchWithinVolume index text from physical page glyph authority;
2. distinguish an existing Google Books page object from actual public image access;
3. inspect the exact public `jscmd=run` and `jscmd=click3` responses without guessing signatures, tokens or hidden identifiers;
4. prevent future sessions from treating HTTP 200 or `PT165` existence as proof that the target physical page has been seen.

## 2. Existing index-level evidence remains valid but scoped

The already-controlled public SearchWithinVolume evidence for volume:

```text
aIRbDgAAQBAJ
ISBN 9789888266944
```

maps `《論人生時要審的確》` to body page object `PT165` and preserves index text corresponding to:

```text
如子時有十刻上五刻属昨夜亥時下五刻属今日子時
```

That remains:

```text
SEARCH_INDEX_TEXT_ONLY
NOT_PHYSICAL_GLYPH_AUTHORITY
PT165_BASE_COPY_IDENTITY=UNRESOLVED_DUNHUATANG_VS_JISHUTANG
```

No zero-result or unstable SearchWithinVolume query is upgraded into negative textual proof.

## 3. Exact public Viewer response probes

### 3.1 First click3 probe

```text
head=bae844ac8aaf9ce8eb626af27a54b2b908474ff4
run=34310578924
artifact=10088199538
artifact ZIP SHA-256=84f0e9a76c160e0eb577bfc39e09a2274b76138d2c726461e68a1e68214576a3
```

Exact public `click3` requests for `PT164`, `PT165`, and `PT166` returned HTTP 200 JSON, but no image URL.

### 3.2 Controlling Viewer-response probe

```text
head=c97ce1179033f65e7e5c9ad7a7a4ffd48ecbe7b8
run=34310657883
artifact=10088226638
artifact ZIP SHA-256=cdbfaf35561588e6001f7eb6af5b61a4aed83261beba749ee0e6ccc45e5378d2
```

The exact public Viewer initialization route:

```text
https://books.google.com/books?id=aIRbDgAAQBAJ&jscmd=run
```

returned:

```text
HTTP 200
Content-Type: application/json; charset=UTF-8
body bytes: 0
source-emitted image URLs: 0
```

The exact public page route for `PT165`:

```text
https://books.google.com/books?id=aIRbDgAAQBAJ&pg=PT165&jscmd=click3
```

returned:

```json
{"pid":"PT165","flags":8,"order":165}
```

inside a 209-page metadata array. The response was 3288 bytes and exposed zero source-emitted image URLs.

Adjacent controls behave the same way:

```text
PT164 -> flags=8 / order=164
PT165 -> flags=8 / order=165
PT166 -> flags=8 / order=166
```

Therefore:

```text
PAGE_OBJECT_EXISTS=YES
PUBLIC_METADATA_RESPONSE=YES
PUBLIC_TARGET_IMAGE_RETURNED=NO
DIRECT_TARGET_GLYPH_OBSERVED=NO
```

## 4. Interpretation firewall

Batch 12AC explicitly fixes the following non-equivalences:

```text
HTTP_200 != PAGE_IMAGE_ACCESS
PAGE_ID_EXISTS != PHYSICAL_PAGE_SEEN
SEARCH_INDEX_SNIPPET != PHYSICAL_GLYPH_AUTHORITY
VIEWER_GOTO_OR_CLICK3_SUCCESS != EDITION_IDENTITY
```

No authentication, purchase, token reuse, identifier guessing, hidden-page enumeration or access-control bypass was attempted.

## 5. HPA-ZDATE-006 adjudication

The textual state remains unchanged:

- Nanyangtang Fullbook directly preserves explicit `昨夜亥時 / 今日子時`.
- Korea Springgang manuscript directly preserves `昨夜 / 今夜` without explicit `亥` in the exact target span.
- the 2017 Wenguangtang combined facsimile public search index corroborates the Hai wording at index-text level, but its target physical page still has not been displayed and the `PT165` base copy remains unresolved between Dunhuatang and Jishutang.
- Batch 12AC adds no physical target-text witness.

Therefore:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
WITHIN_FULLBOOK_HAI_GLYPH_STABILITY=UNRESOLVED
NEW_TEXTUAL_WITNESS_BATCH_12AC=0
NEW_HAI_GLYPH_WITNESS_BATCH_12AC=0
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

## 6. Next evidence gate

The next high-value gate remains a directly readable `《論人生時要審的確》` leaf from a physically bound Fullbook copy whose edition/imprint identity is known.

Priority remains:

```text
經述堂
敦化堂
繼述堂
經綸堂
文誠堂
輝縣市博物館藏清刻本
or another independently bound Fullbook physical witness
```

Viewer metadata routes should not be re-probed unless Google changes the public response surface or a source-emitted image object becomes available.

## 7. Evidence artifact

`docs/research/ZIWEI-WENGUANG-PT165-PUBLIC-VIEWER-RESPONSE-CLOSURE-R1.json`
