# Fusion Chart Historical Provenance Audit R1 — Batch 12FB

## 鐵琴目錄 × 國圖 1823 士禮居本：以合裝、黃氏藏印與蕘翁跋建立「複合物件指紋」，但不越權閉合同一物理冊

Status: **TIEQIN COMPOSITE-OBJECT SIGNATURE DIRECTLY CLOSED / COPPER VOLUME-HEAD HUANG SEALS 士禮居藏・黃印丕烈・蕘圃 DIRECTLY CLOSED / NLC1823 == TIEQIN-CATALOGUED OBJECT STRONGLY SUPPORTED NOT FORMALLY CLOSED / FOURTH NLC SEAL UNADJUDICATED / 原書舊鈔 vs 錄副 FIREWALL PRESERVED / 1827 AIRIJINGLU SOURCE IDENTITY NOT PROVED / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12EY closed the Qing Tieqin catalog wording for the Zhunzhai entry, and Batch 12FA proved from Huang Pilie's 1823 paratext that the tradition itself distinguishes `原書舊鈔` from `錄副`.

The remaining question is object-level:

> Does the Tieqin catalog describe a sufficiently distinctive composite book that the currently reviewed NLC Daoguang-3 / 1823 Shiliju manuscript can be identified with it?

A single Huang ownership phrase is not enough. This batch therefore tests a compound fingerprint: title pairing, one-volume binding, Huang/Raoweng paratext, and the actual seal set at the Copper volume head.

## 2. Direct Tieqin source binding

The controlling Tieqin surface is the Tianyi Pavilion Qing manuscript of 《鐵琴銅劍樓藏書目錄》:

- source object: `330000-1705-0004561 / 善2088`;
- source PDF SHA-256: `29d6774b33087ee8140d7141ca85bd60d25d1872bc636a33da35be9b75dbfc6f`;
- new source-bound window: PDF p383–389 at 400 dpi;
- decisive p387 render SHA-256: `1a27cb70651956d59e847f0161e45ccc2749992910f11bda5a2feaa86667b227`;
- decisive p388 render SHA-256: `859162f056d140d1bdce6e288ca79ec5f72bb786b2b0d4710157fd10788b9f00`;
- extraction commit: `5f12da4b0815c76cebdb9076e09f6ec3658e6c7a`;
- workflow run: `35968905286`;
- artifact: `10795545616`;
- artifact digest: `sha256:ddd321789cc420f2342a883efce0ee8e60514b79794a0476de0b783b2f901611`.

No OCR is final authority.

## 3. p387–388 direct compound signature

The p387 Copper entry directly gives:

    銅壺漏箭制度一卷
    影鈔宋本
    卷首有「士禮居藏」、「黃印丕烈」、「蕘圃」諸朱記

The same p387 surface then opens:

    準齋心製几漏圖式一卷
    影鈔宋本
    宋孫逢古撰并序

and directly states that the Zhunzhai copy is bound with Copper:

    是本與銅壺漏箭制度合裝

The continuation on p388 closes the remaining components:

    一冊
    郡中黃氏舊藏
    蕘翁有跋
    卷首有士禮居藏朱記

Therefore the Tieqin catalogued object is not merely “a Huang copy.” It has a multi-feature signature:

    Copper + Zhunzhai
    + 合裝一冊
    + 郡中黃氏舊藏
    + 蕘翁有跋
    + Copper 卷首: 士禮居藏 / 黃印丕烈 / 蕘圃

## 4. Direct comparison with the current NLC 1823 object

The comparator remains the Batch 12DV/12FA NLC-held Daoguang-3 Huang Shiliju manuscript reproduced in 《續修四庫全書》第1031冊:

- source PDF SHA-256: `07348e40ec26ca38efe9c9736a69c403c61f9b07a2c89a847fc68d00ce6d8c25`;
- Zhunzhai Huang-colophon p76 SHA-256: `64aad110e3cba4984cb784e9f97c99044fbc25e39a06744000a7a606ba73ffeb`;
- Copper volume-head p78 SHA-256: `43f91f0d11eb88a014bb1a5fe53bc5ec696df540cfc2318cc9e80ba04e4c1329`.

Direct review of p78 visibly gives the same first three Huang seal identities beside the Copper title:

    士禮居藏
    黃印丕烈
    蕘圃

The same composite reproduction also carries Huang's dated 1823 Zhunzhai paratext, including:

    道光癸未仲冬月蕘夫書

Thus multiple object features converge, rather than only one ownership phrase.

## 5. Identity adjudication

The evidence now warrants:

    current NLC 1823 composite object
        ==
    object described by the Tieqin catalog

        = STRONGLY_SUPPORTED_NOT_FORMALLY_CLOSED

Confidence is high, but the project remains fail-closed because:

1. no unique Tieqin-era shelfmark/call-number or unambiguous later ownership mark has yet been directly matched across both surfaces;
2. a fourth lower seal is visible on the current NLC Copper title page, but its text is not securely adjudicated;
3. Huang's own 1823 paratext proves that more than one copy layer existed (`原書舊鈔` versus `錄副`), so multiple Huang-related physical copies remain logically possible.

The fourth seal must **not** be labeled `鐵琴銅劍樓` merely from shape or expectation.

## 6. Copy-layer firewall remains intact

This batch strengthens object identity with the Tieqin *catalogued* composite book. It does not decide which Huang copy-layer the current object represents.

Therefore:

    reviewed 1823 object = 原書舊鈔 or 錄副
        = UNRESOLVED

    reviewed 1823 object
        ==
    1827 Airijinglu 從吳門黃氏藏舊抄本
        = NOT_PROVED

No direct-copy edge to the 1827 Airijinglu source is authorized.

Huang's `原書舊鈔當是影宋` remains a Qing bibliographic judgment, not physical dating.

## 7. Transmission graph consequence

Batch 12FB adds:

- `PASSAGE-TIEQIN-QING-MS-TONGHU-HUANG-SEALS-COMPOSITE-BINDING`;
- `TG-E0106`: the Tianyi physical catalog manuscript **ATTESTS** the Copper seal set and composite binding/provenance passage.

It strengthens, without merging:

- the Tianyi Tieqin catalog manuscript node;
- the NLC 1823 Shiliju physical-copy node;
- the Zhunzhai 25-arrow rule-family provenance control.

No same-object graph edge is authorized yet. The identity result remains a strongly supported candidate field, not a collapsed node.

## 8. Sanming and product firewall

This is provenance/object-identity work only:

    direct Sanming-parent vote increment = 0
    algorithm reopen = 0
    candidate collapse = 0

Project accounting remains:

    MATRIX_ROWS=198
    AUDITED_ROWS=166
    MISSING_FROM_PRODUCT=10
    PROVENANCE_DEFECTS=12/12_REPAIRED
    CONFIRMED_CHART_ALGORITHM_DEFECTS=0
    DETERMINISTIC_PRODUCT=CLOSED

## 9. Next gate

1. Identify the lower fourth seal on the current NLC Copper title page from an independent seal specimen or object-specific catalog record.
2. Search NLC/Tieqin acquisition, shelfmark and provenance records for a unique object-level signature.
3. Keep `原書舊鈔`, `錄副`, the current 1823 object, and the 1827 Airijinglu source separated until direct evidence joins them.
4. Continue Yuan person-title / securely pre-1578 exact 25-arrow prose work and the independent Sanming/Nanjing-59 line.

Research record: `docs/research/ZIWEI-TIEQIN-NLC1823-COMPOSITE-OBJECT-FINGERPRINT-CONTROL-R1.json`.
