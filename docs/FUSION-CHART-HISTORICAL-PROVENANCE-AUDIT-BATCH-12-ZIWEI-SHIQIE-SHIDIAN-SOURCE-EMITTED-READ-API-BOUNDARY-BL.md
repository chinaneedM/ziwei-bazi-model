# Fusion Chart Historical Provenance Audit R1 — Batch 12BL

## 《筮篋理數日抄》卷三：識典普通瀏覽器自行發出的 read API 與影像請求之存取邊界

Status: **PUBLIC CHAPTER HTTP 200 / SSR STILL BINDS TARGET TRANSCRIPTION + TARGET PAGE ID / ORDINARY ANONYMOUS BROWSER SOURCE-EMITS `paragraphs/v3` + `pages/v3` / ALL CAPTURED READ-API RESPONSES HTTP 200 BUT APPLICATION BODY IS ONLY `errorCode=31000` / SOURCE-EMITTED `pages/v3` REQUEST RANGE COVERS THE TARGET REGION BUT RETURNS NO PAGE DATA / 15 SIGNED `/ref/` IMAGE RESPONSES OBSERVED, TARGET PAGE ID ABSENT / NO TARGET FULL-PAGE IMAGE / NO URL-PATTERN INFERENCE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BK closed the National Archives route at a clean boundary: the exact official fascicle-three object and 69-canvas manifest are known, but the 56-page Shidian transcription cannot be ordinally mapped onto those canvases, and the first-party image surface is HTTP 403 from the GitHub runner.

Batch 12BL therefore tests a different, narrower route: **what does an ordinary anonymous browser receive when it opens the public Shidian volume-three chapter and lets the page make its own requests?**

The probe is passive. It does not manually replay the observed APIs, regenerate anti-bot parameters, infer adjacent page URLs, enumerate IDs, inject cookies/tokens, or use a hidden/private interface.

## 2. The public SSR still binds the target locus exactly

Ordinary navigation to:

`https://www.shidianguji.com/zh/book/NA06425/chapter/1m44zy4jwa4ab`

returns HTTP 200. The rendered/SSR HTML still contains both:

- target paragraph ID `7649191097545588762`
- target page ID `7640563520069697576`
- transcription `巳上是上四亥。`

The same target page continues with `巳上是下四刻。` and the following section `論子時隔界` states `上四刻屬本日管，下四刻屬第二日管`.

This remains a strong **locator/transcription layer**, not physical-glyph authority.

## 3. What the ordinary browser itself requested

Without manual replay, the public page emitted HTTP requests including:

- `book/dynamic-info/get`
- `review/chapter-list/`
- `book/paragraphs/v3/`
- `book/pages/v3/`

The source-emitted `pages/v3` POST payload scoped itself to:

```text
bookId       NA06425
pageIndex    1
pageSize     40
startPageNum 353
endPageNum   409
version      1
```

A page token was present in the browser-generated request, but it is not copied into the durable evidence because it is ephemeral and unnecessary to the historical adjudication.

This is important provenance: the browser itself attempted to obtain the relevant opening page block of volume three. It does **not** authorize us to replay or reconstruct that request.

## 4. HTTP 200 is not page availability here

Four selected read responses were captured exactly as received by the browser. Every one had HTTP 200 and every body was the same 33-byte JSON object:

```json
{"errorCode":31000,"errorMsg":""}
```

The identical body SHA-256 is:

`460a68650881f42750a8226fdd4a5ed610e1b7a200d4a4a95735c0724cd90572`

Therefore:

- `paragraphs/v3` returned no target text or target page record;
- `pages/v3` returned no page list, no target page ID, no `picUrl`, no `thumbUrl` and no target image metadata;
- HTTP status alone must not be misclassified as a successful page-data response.

## 5. Source-emitted signed images do not expose the target page

The same ordinary browser session successfully loaded sixteen image responses. One is the site's no-network placeholder. Fifteen are signed `.../ref/...` image resources emitted by the public page.

Across those fifteen `ref` responses, the observed unique embedded page IDs are:

- `7640563520069746728`
- `7640563520069763112`
- `7640563520069795880`
- `7640563520069812264`
- `7640563520069828648`
- `7640563520069845032`
- `7640563520069861416`
- `7640563520069877800`

The target page ID `7640563520069697576` is absent.

These are `ref` resources, not an observed target full-page image. Their URL structure must **not** be extrapolated backward to manufacture a target-page URL. That would replace evidence with pattern inference.

## 6. Effect on HPA-ZDATE-006

No rule vote changes:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- exact Shiqie target glyph observed: `false`
- Hai glyph/witness increment: `0`
- upper/night Zi → Hai directly attested by this batch: `false`
- runtime winner: `false`
- candidate collapse: `false`
- algorithm reopen: `false`

The isolated `上四亥` remains a quarantined transcription anomaly candidate. The surrounding mechanics still say `上四刻 / 下四刻`, and Batch 12BI's independently collated physical parallel remains consistent with `刻`, but neither fact licenses silently rewriting the exact Shiqie glyph before that leaf is read.

## 7. Durable evidence

Machine-readable record:

`docs/research/ZIWEI-SHIQIE-SHIDIAN-SOURCE-EMITTED-READ-API-BOUNDARY-R1.json`

Hosted evidence:

- ordinary public-browser passive network probe: run `34765718210`, artifact `10320391963`, digest `sha256:1665c297d024f7cf234574a5f38e6594168c7c1ab8c3742eb8546d586364060a`
- source-emitted read-response body capture: run `34765824117`, artifact `10320861185`, digest `sha256:79ba56e995d27d26e7fb83fdf243c46ef3a03c4d43e261def860e30e9c5f29ae`

The second artifact preserves the response bodies and exact browser-emitted request metadata. The durable repository evidence intentionally omits ephemeral anti-bot/signature token values.

## 8. Next gate

Promotion now requires either:

1. a directly source-emitted and readable full-page image bound to target page ID `7640563520069697576`; or
2. an independently bound physical witness resolving the same glyph/rule question.

Until then, do not replay the 31000-producing request, do not derive an image URL from neighboring `ref` resources, and do not convert the transcriptional `亥` into a mechanical Hai-branch rule.
