# Fusion Chart Historical Provenance Audit R1 — Batch 12BF

## 《新編評註通玄先生張果星宗大全》普林斯顿本馆目录绑定与公开图像传输边界

Status: **PRINCETON FIRST-PARTY CATALOG EXACTLY BINDS TC183/2991 / MMS 9940551833506421 / 1593 TANG QIAN + 1594 ZHOU WENGUANG IMPRESSION STATEMENT CONFIRMED / PUBLIC RECORD EMITS “FIRST PAGE OF MAIN TEXT” RESOURCE / NORMAL HTTPS VALIDATION FAILS ON HOSTNAME MISMATCH / SAME-PATH HTTP 301 RETURNS TO HTTPS / NO CERTIFICATE BYPASS / NO IMAGE BYTES / SAME PHYSICAL COPY AS 12BE, SO MATERIAL-WITNESS +0 / NO TARGET LEAF / ZERO TARGET-TEXT OR HAI-GLYPH VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BE had already established the NLC union-catalog object `NJPX95-B1857` and Princeton call number `TC183/2991` as one independent early-Wanli physical witness, with the 1593 preface/catalog date kept distinct from the Wanli 22 / 1594 cover impression. Its unresolved question was whether a legitimate Princeton-side route could independently bind the holding and expose page images.

This batch therefore asks only:

1. Does a Princeton first-party public service resolve `TC183/2991` to the same early-Wanli item?
2. Does that record expose a public image-resource contract?
3. Can the exact emitted resource be obtained with normal transport validation, without guessing hidden page IDs or bypassing access controls?

It does **not** reopen the deterministic Ziwei algorithm and does **not** treat catalog metadata or a first-page image as rule-text evidence.

## 2. Princeton first-party exact binding

The public Princeton Allsearch Catalog endpoint queried with exact call number `TC183/2991` returned exactly **1** result.

That result directly records:

- MMS/catalog ID: `9940551833506421`
- call number: `TC183/2991`
- library: `Special Collections`
- status: `Available`
- title: `Xin bian ping zhu Tongxuan xian sheng Zhang Guo xing zong da quan : shi juan / Lu Wei ji jiao.`
- creator: `Zhang, Guo, active 713-742`
- publisher statement: `[Jinling] : Tang Qian, Ming Wanli gui si [21 nian, 1593] (Zhou Wen'guang, Wanli 22 nian [1594] impression)`

This is a materially stronger institutional binding than the prior union-catalog-only route: Princeton itself now directly ties `TC183/2991` to the 1593/1594 Zhang Guo Xingzong object.

## 3. Public image-resource contract

The same first-party result reports `online_access_count = 1` and emits:

- label: `First page of main text`
- resource URL: `https://libimages1.princeton.edu/loris/CHRBPageImages/NJPX95B1857.jp2/full/full/0/default.jpg`

This establishes that Princeton's own catalog metadata knows a specific image identifier for the **first page of main text**. It does not establish a public multi-page viewer, target late-Zi leaf, or page-sequence contract.

## 4. Transport adjudication

The exact emitted HTTPS URL was requested with ordinary certificate validation. The request failed because the certificate presented for `libimages1.princeton.edu` did not validate for that hostname.

No certificate-verification bypass was used.

The exact same host and path were then tested over plain HTTP solely to distinguish transport behavior. It returned:

- HTTP `301 Moved Permanently`
- `Location` back to the same HTTPS URL
- no image bytes

Therefore the current public contract is **discoverable but not normally retrievable from the hosted research runner**. This is a transport/access observation only; it does not authorize any claim that Princeton lacks the image, that the image is permanently unavailable, or that the digitization is incomplete.

## 5. Deduplication

Batch 12BF adds **0** new independent material witnesses.

`TC183/2991` / `NJPX95-B1857` is the same Princeton physical copy already counted once in Batch 12BE. A stronger first-party catalog binding cannot be counted as a second copy.

## 6. Rule-evidence effect

No target late-Zi leaf was obtained. Consequently:

- exact-1594 independent material witness increment: `0`
- target-text witness increment: `0`
- `亥` glyph/rule vote increment: `0`
- `HPA-ZDATE-006`: remains `MISSING_FROM_PRODUCT`
- runtime winner: none
- candidate collapse: none
- deterministic algorithm reopen: none

The unresolved bridge remains the same: direct historical rule evidence must explicitly support `upper/night Zi -> Hai branch` before any source-scoped runtime candidate can be promoted.

## 7. Research boundary

The probe followed only:

1. Princeton's public first-party Allsearch API;
2. the exact catalog record returned for `TC183/2991`;
3. the exact image resource emitted by that record;
4. the same host/path over HTTP to observe redirect behavior.

It did not disable TLS verification, guess adjacent image/page identifiers, enumerate hidden files, log in, or bypass NLC/Princeton permissions.

## 8. Durable evidence

Machine-readable evidence is stored at:

`docs/research/ZIWEI-ZHANGGUO-PRINCETON-CATALOG-IMAGE-CONTRACT-R1.json`

Key hosted-run references:

- broad Allsearch probe: run `34754839962`, job `103717362110`, artifact `10315839892`
- exact transport probe: run `34755007652`, job `103717792255`, artifact `10317430095`

## 9. Next gate

1. Seek a legitimate first-party/reproduction path that exposes additional pages or the target late-Zi leaf without certificate or permission bypass.
2. Prefer an independent early 1593/1594 copy with public page images over further duplicate catalog records.
3. If a target leaf is lawfully obtained, bind provider URL/object ID/digest/page/leaf and visually collate the historical glyphs before assigning any rule vote.
4. Keep `HPA-ZDATE-006` unresolved until direct evidence supplies the missing `upper/night Zi -> Hai` mechanical bridge.
