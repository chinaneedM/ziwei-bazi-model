# Fusion Chart Historical Provenance Audit R1 — Batch 12BK

## 《筮篋理數日抄》卷三：Japan Search → 國立公文書館 IIIF → 識典頁序對齊與存取邊界

Status: **EXACT JAPAN SEARCH FASCICLE-3 RECORD RESOLVED / EXACT NATIONAL ARCHIVES IIIF MANIFEST HTTP 200 / OFFICIAL FASCICLE-3 HAS 69 CANVASES / SHIDIAN PUBLIC VOLUME-3 TRANSCRIPTION IS A COMPLETE 56-PAGE SPAN (353–408) / TARGET TRANSCRIPTION PAGE LOCATED BUT NOT PHYSICALLY MAPPED / 56 != 69, SO ORDINAL MAPPING IS FORBIDDEN / MANIFEST IMAGE RESOURCE + SERVICE + ORDINARY CHROMIUM ITEM ROUTE ALL BLOCKED FROM GITHUB RUNNER / NO TARGET GLYPH OBSERVED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BJ established that the public YFShuhua route really reproduces the already tracked National Archives / Naikaku Bunko Shiqie set, but exposes only cover, preface and volume-one samples. Batch 12BK therefore asks a narrower question: can public machine-readable records align the volume-three transcription locus to an exact official physical canvas without guessing?

The answer is **not yet**. The route is materially stronger, but the physical target glyph remains unresolved.

## 2. Exact first-party fascicle-three object

A documented Japan Search public item query returned the exact volume-three record ID `najda-XlZliJwgFlrJCdDQsawqSkOJUKP9hAZXTdEQ_0003`. Following that returned record—not an inferred adjacent identifier—resolved the National Archives object whose public item URL is:

`https://www.digital.archives.go.jp/item/4756821`

The exact first-party IIIF manifest is:

`https://www.digital.archives.go.jp/api/iiif/4756821/manifest.json`

It returned HTTP 200 and identifies `筮篋理数日抄３`, reference code `子０６０－０００２-0003`, with **69 canvases**. The manifest SHA-256 is `e9b2af8117d8f45922cd8e8656ef0ab7165e727db5c81c59b3d805ab135ba48e`.

This closes the digital-object identity and official canvas order. It does **not** by itself identify the target canvas.

## 3. Public Shidian volume-three page order

The public Shidian SSR page for volume three returned HTTP 200. Its structured chapter record states:

- chapter: `卷三`
- `startPageNum = 353`
- `endPageNumWithoutSubchapter = 408`

That interval is exactly **56 pages inclusive**, and the independent `pagePass` sequence also contains 56 unique page IDs. This is important: the difference from the official 69-canvas manifest is not merely a parser dropping thirteen pages.

The target paragraph is publicly locatable as:

- paragraph ID `7649191097545588762`
- page ID `7640563520069697576`
- fourth visible transcription page in the derived chapter order
- transcription: `巳上是上四亥。`

Nearby explanatory text still states `上四刻屬本日管，下四刻屬第二日管`.

Shidian remains a **transcription/locator witness only** for this question. The isolated `亥` cannot be promoted to physical-glyph authority.

## 4. Why page 4 cannot be called official canvas 4

The two complete representations do not have the same cardinality:

```text
Shidian volume-three transcription pages   56
National Archives official IIIF canvases   69
difference                                 13
```

Therefore no fixed ordinal mapping is authorized. In particular, the target being the fourth Shidian page does **not** authorize treating official canvas 4 as the target. Nor is a fixed +13/-13 offset justified.

Any such mapping would be object-ID/page-order inference rather than evidence.

## 5. First-party image access boundary

The exact official manifest exposes literal resource/service IDs. A controlled probe of the first manifest-listed page produced:

- literal resource: HTTP 403
- service `info.json`: HTTP 403
- standard IIIF image transformation from the declared service ID: HTTP 403

A separate ordinary Chromium test then navigated to the exact public item URL. In the GitHub runner it also returned HTTP 403 with `ERROR: The request could not be satisfied`, emitted no usable viewer href, and produced zero successful image responses.

This closes a material ambiguity: the runner restriction is not merely an `urllib` header quirk. It persists under normal browser navigation in that environment.

No login, cookie/token injection, hidden endpoint discovery, adjacent-ID enumeration or access-bypass method was attempted.

## 6. Japan Search text-search control

Documented public Japan Search queries for `論子時隔界`, `上四亥`, `選時寶鏡局`, and `日百刻配十二時` returned no exact page-level target-text hits. This is only a public-search-surface control; it is **not** evidence that the physical page or wording is absent.

## 7. Effect on HPA-ZDATE-006

No rule vote changes:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- exact Shiqie target glyph observed: `false`
- Hai-branch glyph/witness increment: `0`
- upper/night Zi → Hai directly attested by this batch: `false`
- runtime winner: `false`
- candidate collapse: `false`
- algorithm reopen: `false`

The current safest reading remains: `上四亥` is a quarantined transcription anomaly candidate until its physical leaf is directly read. Batch 12BI's independent CADAL physical parallel (`係上四刻 / 係下四刻`) continues to strengthen that anomaly diagnosis, but cannot substitute for the exact Shiqie glyph.

## 8. Durable evidence

Machine-readable record:

`docs/research/ZIWEI-SHIQIE-JNA-FASCICLE3-PAGE-ORDER-AND-ACCESS-BOUNDARY-R1.json`

Hosted evidence chain:

- Japan Search exact item reference: run `34762934050`, artifact `10319273767`
- exact official fascicle-three manifest: run `34763008839`, artifact `10319722109`
- official page-1 image-contract probe: run `34763132512`, artifact `10319198130`
- Japan Search target-text control: run `34763331089`, artifact `10319842374`
- Shidian chapter page-order probe: run `34763494286`, artifact `10319518306`
- ordinary Chromium first-party item-route probe: run `34765354700`, artifact `10320310873`

## 9. Next gate

The next admissible promotion requires either:

1. a directly readable physical volume-three target leaf of the National Archives copy obtained through an ordinary public route outside the blocked GitHub-runner surface; or
2. an independent early physical witness explicitly assigning upper/night Zi to the Hai earthly branch.

Until then, do not infer a canvas from ordinal position and do not convert `上四亥` into a runtime rule.
