# Fusion Chart Historical Provenance Audit R1 — Batch 12BI

## 《類編曆法通書大全》「上四刻／下四刻」原葉物理校讀

Status: **DIRECT PUBLIC-DOMAIN FACSIMILE COLLATION / CADAL02094403 SCAN P82–83 / PHYSICAL GLYPHS CONFIRM 上四刻 + 下四刻 AND 本日 + 第二日 DATE ORIENTATION / STRONGLY CORROBORATES BATCH 12BH TRANSCRIPTION-ANOMALY DIAGNOSIS / DOES NOT PHYSICALLY COLLATE THE SHIQIE TARGET LEAF / DOES NOT ATTEST UPPER-ZI -> HAI BRANCH / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BH quarantined the public-transcription token `上四亥` in the Jiajing-44 (1565) 《筮篋理數日抄》. The same passage is internally symmetric with `下四刻` and then repeatedly uses `上四刻/下四刻` for the date-boundary mechanics. Because the exact Shiqie physical leaf was unavailable, Batch 12BH deliberately refused to call the token either a confirmed `亥` glyph or a confirmed OCR/transcription error.

Batch 12BI asks a narrower question: can an independent physical calendrical witness from the same technical discourse directly establish that `上四刻/下四刻` is an actual printed terminology pair, rather than a normalization invented by modern editors?

## 2. Public-domain physical witness

The reviewed object is the Wikimedia Commons public-domain CADAL scan:

- `CADAL02094403 類編曆法通書大全（一）.djvu`
- 89 scan pages
- DJVU SHA-256: `50535ad31514f733a4aebaf39824b2128e4fb1ebdc6a2fc33d9e7813d912a63e`
- target scan pages: `82–83`

The DJVU has no usable embedded text layer for this purpose. Final glyph judgment was therefore made by direct visual inspection of rendered scan pages; OCR was not used as glyph authority.

The exact impression date of this scanned copy is **not established in this batch**. The source is used only as an independent physical witness to the technical vocabulary and date-boundary mechanics printed on the reviewed leaves.

## 3. Direct collation — scan p.82

The leaf directly reads:

> 論定半夜子時隔界
>
> 子初初刻、初二刻、初三刻、初四刻，係上四刻，屬本日管。
>
> 子正一刻、正二刻、正三刻、正四刻，係下四刻，屬第二日管。

The glyphs relevant to this audit are physically unambiguous:

```text
上四刻    physically observed
下四刻    physically observed
本日      physically observed for the upper four-ke segment
第二日    physically observed for the lower four-ke segment
上四亥    not observed in this physical parallel
```

Scan p.83 continues the calendrical examples across the boundary and the instruction to distinguish the upper/lower four-ke division when selecting times.

## 4. Effect on the Batch 12BH anomaly

This physical witness materially strengthens—but does not over-close—the Batch 12BH diagnosis.

The combined evidence is now:

1. Shiqie public transcription contains the isolated token `上四亥` in a counting-label slot.
2. Its immediately parallel lower label is `下四刻`.
3. The same Shiqie passage then repeatedly says `上四刻屬本日管`, `下四刻屬第二日管`, and `是上四刻作二十六日管`.
4. The independent physical 《類編曆法通書大全》 leaf directly prints the symmetric pair `係上四刻` / `係下四刻` in the same night-Zi date-boundary discourse.
5. Other public transcription/OCR surfaces reviewed in Batch 12BH show that `刻` can be misrecognized as `亥` in this technical environment.

Therefore `上四亥` is now best classified as a **strongly corroborated transcription anomaly pending direct Shiqie physical-leaf collation**.

The remaining caution is essential: this batch has **not** observed the exact Shiqie target leaf. It therefore does not authorize the statement “the Shiqie original definitely prints 刻.”

## 5. Effect on HPA-ZDATE-006

None of the above supplies the missing mechanical bridge:

```text
upper/night Zi -> Hai earthly branch
```

Accordingly:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- explicit new Hai-branch vote: `0`
- runtime winner selected: `false`
- candidate collapsed: `false`
- algorithm reopen: `false`

The literal public-transcription string `上四亥` remains barred from use as evidence for branch reassignment unless the exact physical Shiqie leaf or another direct mechanical historical source independently validates that reading and semantics.

## 6. Durable evidence

Machine-readable record:

`docs/research/ZIWEI-LEIBIAN-LIFA-TONGSHU-UPPER-FOUR-KE-PHYSICAL-COLLATION-R1.json`

Hosted physical-render evidence:

- run `34760486843`, job `103732346260`, artifact `10319085691` — pages 1–35
- run `34760591933`, job `103732623688`, artifact `10318299257` — pages 36–89, including target p82–83

## 7. Next gate

Stop spending evidence weight on transcription-only `亥` hits. Priority remains:

1. direct physical acquisition of the Jiajing-44 Shiqie target leaf; or
2. an independent early physical source that explicitly says the upper/night-Zi segment is reassigned to the Hai earthly branch.

Until then the candidate remains source-scoped and unimplemented.
