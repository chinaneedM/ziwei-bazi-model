# Fusion Chart Historical Provenance Audit R1 — Batch 12AR

## 1581《紫微斗數捷覽》PT49 公共預覽取頁邊界

Status: **PT49 INDEX POSITIVE / PUBLIC PLAY READER SOURCE-EMITS A SIGNED PT49 IMAGE URL / PT49 IMAGE RESPONSE IS A VISIBLE “IMAGE NOT AVAILABLE” PLACEHOLDER / PT48 POSITIVE FACSIMILE CONTROL SUCCEEDS / NO PT49 PHYSICAL GLYPH AUTHORITY / GOOGLE PUBLIC PREVIEW ROUTES REVIEWED HERE CLOSED / NO ALGORITHM EFFECT**

## 1. Question

Batch 12AP established that Google Books volume `rZRcCwAAQBAJ` source-emits page id `PT49` for the inclement-weather query and associates that page with 《論十二生時難定訣》. It did **not** obtain the physical PT49 page.

Batch 12AR asks a narrower access question:

> Can the current public Google Books / Google Play preview surfaces supply the actual PT49 page image without login, DRM bypass, hidden-endpoint guessing, or forged/reused image signatures?

This is an access/provenance question, not a runtime-rule question.

## 2. Scope firewall

All probes remained within public, source-emitted routes.

```text
AUTHENTICATION_ATTEMPTED=false
DRM_BYPASS_ATTEMPTED=false
HIDDEN_ENDPOINT_GUESSING_ATTEMPTED=false
SIGNATURE_CONSTRUCTED_FORGED_OR_REUSED=false
WHOLE_BOOK_PHYSICAL_NEGATIVE_AUTHORIZED=false
PT49_TEXTUAL_ABSENCE_CLAIM_AUTHORIZED=false
```

## 3. AR-R1 — standard public PT49 page

```text
RUN=34351724023
ARTIFACT=10104042912
ZIP_SHA256=b19d1de4bee940b5c589b1023db45fb939e580e50e00b95eebb4023f0f1fb007
RECEIPT_SHA256=ce3ac8dc5c8e3db758c56ca0b589cd2bf12a302e043043f7d1424d87123c4d9d
```

The ordinary public route:

```text
books.google.com/books?id=rZRcCwAAQBAJ&pg=PT49
```

returned HTTP 200 and contained the PT49 page token, but its classic Books HTML emitted a signed physical page-image URL only for **PT48**, not PT49.

That result alone did not prove PT49 unavailable everywhere, so the source-emitted reader routes were followed next.

## 4. AR-R2 — iRead public preview route

```text
RUN=34352023215
ARTIFACT=10104169134
ZIP_SHA256=8df2d8a17cec2ece796a86eb1e07b685d9d10f0d1e00c76fb75fa15ed241439c
RECEIPT_SHA256=453eeb2e1b18b14ec48df09df7b69e4300bed0711cabf0ffdb4d369d5fc3b40b
```

The GitHub runner timed out retrieving the iRead product page.

This is classified only as:

```text
EXECUTION_ENVIRONMENT_ACCESS_BOUNDARY
```

It is **not** a content negative and does not prove the iRead preview lacks PT49.

## 5. AR-R3 — source-emitted reader routes

```text
RUN=34353366786
ARTIFACT=10104661512
ZIP_SHA256=ae10f3184ffab3bbf14ee48f6015000aa2d99308cb6ba34bb65f3f9252580bd7
RECEIPT_SHA256=25aa7a638aa04d60511274344f385d385a2ef0f9614edf6953b409c6f49215d3
```

The public PT49 Books page itself emitted a Google Play reader link.

The Play reader returned HTTP 200 and its public bootstrap HTML directly emitted signed page-image URLs across the preview page map, including:

```text
PT48
PT49
PT50
```

The PT49 image URL was therefore **not guessed or constructed**. Its page id and signature both came directly from the public Play reader response.

This was a materially stronger access result than Batch 12AP.

## 6. AR-R4 — direct source-emitted PT48 / PT49 / PT50 image responses

```text
RUN=34353510199
ARTIFACT=10104715354
ZIP_SHA256=52c968a601a56732f293d2f25318d8d70ae6dc4f2e588baeee077e51ada6b1ed
RECEIPT_SHA256=d4b7553e5e0d55f25931d2cc6e8ead590589c3ed93a200f1702ad2542408f9f4
```

All three URLs were copied from their literal public reader bootstrap records and fetched unchanged.

### PT48 positive control

```text
HTTP=200
CONTENT_TYPE=image/jpeg
SHA256=4d95bcc7a8c14d842d1d735faa83cfbb33cc16773cc35ddb4ef18d3c679d95d0
MANUAL_VISUAL_REVIEW=GENUINE_JIELAN_FACSIMILE_PAGE_IMAGE
```

Direct visual review confirms PT48 is a genuine facsimile page.

This positive control is important: the signed-image route is operational and can return real page pixels.

### PT49 target

```text
HTTP=200
CONTENT_TYPE=image/png
SHA256=3efa8c43e5b4348f303a528c81adf435f0111ea752fe9f0f6241478b60987fa6
MANUAL_VISUAL_REVIEW=VISIBLE_IMAGE_NOT_AVAILABLE_PLACEHOLDER
```

PT49 is **not** a book page. It is a visible `image not available` placeholder.

### PT50 adjacency control

```text
HTTP=200
CONTENT_TYPE=image/png
SHA256=3efa8c43e5b4348f303a528c81adf435f0111ea752fe9f0f6241478b60987fa6
MANUAL_VISUAL_REVIEW=VISIBLE_IMAGE_NOT_AVAILABLE_PLACEHOLDER
```

PT50 returns the identical placeholder hash.

Therefore:

```text
PT49_SIGNED_IMAGE_URL_SOURCE_EMITTED=true
PT49_IMAGE_HTTP_200=true
PT49_REAL_PAGE_IMAGE=false
PT49_PHYSICAL_GLYPH_AUTHORITY=false
```

A public signed image URL is not equivalent to page-image availability.

## 7. AR-R5 — English accessible mode and “new Google Books”

```text
RUN=34353757432
ARTIFACT=10104818160
ZIP_SHA256=2cb09e99dd917ee5a1b5c2fe00a9f1d1c35c027f82810758f8793517c369ddad
RECEIPT_SHA256=9c73da62633b4a8365ca013b9b6b6c70386f4b83ae914f6e79a5dd3de1f3a4bb
```

Both URLs had been literally emitted by the earlier English PT49 public page.

Results:

- accessible English mode: HTTP 403;
- “new Google Books”: redirects back to classic Books;
- PT49 token remains present;
- no PT49 page-image object is source-emitted by that returned surface.

No hidden API or synthesized image route was attempted.

## 8. What Batch 12AR proves

Batch 12AR **does prove**:

1. PT49 remains a positive public index/page-id witness.
2. Google Play reader publicly emits a signed PT49 page-image URL.
3. The same public signed route successfully returns a genuine PT48 facsimile page.
4. PT49's signed route instead returns an `image not available` placeholder.
5. PT50 returns the same placeholder.
6. The reviewed Google public preview routes therefore do not yield PT49 physical glyphs.

Batch 12AR **does not prove**:

- that PT49 is absent from the physical book;
- that PT49 has no image in any private/licensed/purchased reader state;
- that iRead lacks the page;
- that no library/facsimile copy can expose the page;
- that the Google index OCR is exact glyph authority;
- that any Fullbook/Jielan runtime candidate should be selected.

## 9. Product / Matrix effect

No chart-affecting state changes.

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
MATRIX=198/166
CURRENT_MISSING_FROM_PRODUCT=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
PROVENANCE_DEFECTS=11_CONFIRMED/11_REPAIRED
CHART_ALGORITHM_DEFECT=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
RUNTIME_STANDARD_SELECTED=false
FULLBOOK_INCLEMENT_TIME_ACQUISITION_CHAIN_CLOSED=false
```

## 10. Next gate

Do not repeat the Google Books / Play public preview paths closed above unless the provider surface materially changes.

The next chart-affecting gates are:

1. acquire a directly readable Jielan PT49 physical leaf from an independent holding/facsimile route; and
2. prioritize a source that explicitly states the **Fullbook-line cloudy/rainy current-time acquisition procedure**, because that is the unresolved step that can actually bind `HPA-ZDATE-006` to a runtime time coordinate.

Machine evidence:

`docs/research/ZIWEI-JIELAN-PT49-PUBLIC-PREVIEW-ACCESS-BOUNDARY-R1.json`
