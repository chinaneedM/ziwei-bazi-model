# Fusion Chart Historical Provenance Audit R1 — Batch 12BM

## 《筮篋理數日抄》卷三：Japan Search 原樣 viewer URI × 國立公文書館第一方內容面存取邊界

Status: **EXACT JAPAN SEARCH FASCICLE-3 RECORD LITERALLY EMITS FIRST-PARTY VIEWER URI / VIEWER URI IS NOT GUESSED / ORDINARY CHROMIUM VIEWER HTTP 403 CLOUDFRONT / LITERAL THUMBNAIL HTTP 403 / NO VIEWER CONTROLS / NO DOWNLOAD UI / NO SUCCESSFUL IMAGE RESPONSE / WRONG-ROUTE HYPOTHESIS CLOSED / NO TARGET GLYPH OBSERVED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BK established the exact National Archives fascicle-three object and its 69-canvas IIIF manifest, but ordinary navigation to the catalog item and manifest-declared image resources was blocked from the GitHub runner. That left one residual ambiguity: perhaps the content viewer had a different first-party URI that had simply not yet been resolved.

Batch 12BM closes that ambiguity without URL construction.

## 2. Exact viewer URI from Japan Search

The exact public Japan Search fascicle-three record `najda-XlZliJwgFlrJCdDQsawqSkOJUKP9hAZXTdEQ_0003` literally emits the National Archives viewer URI in its `owl:sameAs` field:

`https://www.digital.archives.go.jp/img/4756821`

The same record also literally emits a first-party thumbnail URI:

`https://www.digital.archives.go.jp/thumb/4756821/C103347219500.jpg`

These values were returned by the record itself. Neither path was reconstructed from the numeric item ID.

## 3. Ordinary-browser result

A normal anonymous Chromium session navigated directly to the literal viewer URI. The response was HTTP 403 and the rendered title was `ERROR: The request could not be satisfied`, with a CloudFront error surface.

No usable anchors, viewer controls, download UI, image elements or successful image responses were exposed.

The literal thumbnail URI was tested independently and also returned HTTP 403 with the same first-party/CloudFront access boundary.

No login, cookie/token injection, alternate endpoint discovery, sequential object enumeration or bypass technique was used.

## 4. What this closes

The evidence now separates object identity from execution-environment accessibility:

```text
exact fascicle-three record identity       closed
exact National Archives item identity      closed
exact official IIIF manifest identity      closed
exact first-party viewer URI               closed
exact source-emitted thumbnail URI         closed
viewer/content reachability from runner    blocked (403)
target physical glyph                      not observed
```

Therefore the earlier first-party 403 cannot reasonably be attributed to our having guessed the wrong viewer route. The route is exact; the content surface remains blocked in this execution environment.

## 5. Effect on HPA-ZDATE-006

No textual or mechanical evidence increment occurs:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- exact Shiqie target glyph observed: `false`
- Hai glyph/witness increment: `0`
- runtime winner: `false`
- candidate collapse: `false`
- algorithm reopen: `false`

This batch is an access/provenance closure only.

## 6. Durable evidence

Machine-readable record:

`docs/research/ZIWEI-SHIQIE-JNA-LITERAL-VIEWER-ACCESS-BOUNDARY-R1.json`

Hosted evidence:

- Japan Search exact record resolution: run `34762934050`, artifact `10319273767`
- literal first-party viewer/thumbnail Chromium probe: run `34766246768`, artifact `10320761950`, digest `sha256:0093749d86190c8701e815f3158fefc4da6b9568cb9f77f2e2650e28c8b814dc`

## 7. Next gate

Do not spend further research cycles inventing National Archives viewer/download URLs from item `4756821`. The next admissible advance is a directly readable target leaf through another ordinary public first-party or independently bound facsimile route, or an independent early physical homolog that can be collated at the glyph level.
