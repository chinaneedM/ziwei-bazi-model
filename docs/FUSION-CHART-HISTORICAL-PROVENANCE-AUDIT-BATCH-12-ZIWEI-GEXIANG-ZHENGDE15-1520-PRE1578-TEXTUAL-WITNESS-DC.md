# Batch 12DC — 正德十五年（1520）《重刊革象新書》百刻／半子文字前1578物理见证

## Status

```text
SOURCE=NCL-06265 重刊革象新書
CATALOG_EDITION=明正德庚辰(十五年)宣威公署刊本
INTERNAL_ZHENGDE15_DATE_P5=DIRECT_PHYSICAL
SHIFEN_BAIKE_P36=DIRECT_PHYSICAL
HALF_ZI_YESTERDAY_TODAY_P37=DIRECT_PHYSICAL
SECURE_PRE1578_TEXTUAL_WITNESS=CLOSED
DIRECT_GEXIANG_TO_SANMING_COPY=UNPROVED
DIRECT_GEXIANG_TO_SHENDAO_COPY=UNPROVED
NLC892_PINGTU_CROSSCOPY_IDENTITY=UNRESOLVED_AND_QUARANTINED
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
```

## 1. Why this batch matters

Batch 12DB left one textual-stemma gate open: find a **securely pre-1578 physical witness** of the Zhao/Gexiang hundred-ke and half-Zi wording, preferably the closer `若子時則上半時...` recension rather than relying only on a later received facsimile.

Batch 12DC closes that gate with a separate source-bound object: National Central Library call number **6265**, public surrogate `NCL-06265 重刊革象新書.pdf`. The public file metadata identifies the edition as **明正德庚辰（十五年）宣威公署刊本** and the scan contains an internal `正德十五年歲次庚辰` dated control.

This is a 1520 witness, 58 years earlier than the exact 1578 `《三命通會》` physical witness.

## 2. Source identity and acquisition

```text
SOURCE_ID=EXT-NCL-GEXIANG-NCL06265-ZHENGDE15-1520
TITLE=重刊革象新書
CALL_NUMBER=6265
CATALOG_EDITION=明正德庚辰(十五年)宣威公署刊本
PDF_PAGES=78
SOURCE_PDF_SHA256=97b3f060e2c78229c113c4f6854cbd5fb27b95999144486a84bbeaf2d1a5e5bf
OCR_USED_FOR_FINAL_GLYPH_CLAIMS=false
```

Public metadata route: `https://commons.wikimedia.org/wiki/File:NCL-06265_重刊革象新書.pdf`.

The public file description gives the edition string above and call number 6265. Its author field is preserved verbatim in the machine record as `(元)趙敬撰 (明)王禕刪定`; this batch does **not** use that metadata string to normalize the Zhao author identity. Zhao Youqin/Yuandu attribution remains controlled by the independent textual/bibliographic evidence already in the project.

```text
LOCATOR_RUN=35345078553
LOCATOR_ARTIFACT=10546224557
LOCATOR_DIGEST=sha256:3b86af218995de4589df338dee50e8f0c05b18878db5eef723877b31f4f5d3b3
HIGHRES_RUN=35345404531
HIGHRES_ARTIFACT=10546499551
HIGHRES_DIGEST=sha256:50331f7591658b15ca02f2bbafc9d6f4f89aaa88bf6a3fa84791cbdfdfd7e878
RENDER_DPI=360
```

## 3. p5 — internal Zhengde-15 control

```text
SHA256=a46be69e41452488857bf5365310686598a93b0c514c69aeb6228ba1aaa720ba
正德十五年歲次庚辰
```

Only this clearly visible date phrase is promoted; the remainder of the partially difficult paratext is not normalized.

## 4. p36 — 《時分百刻》

```text
SHA256=159f16034b3776ff5b9c13a246bb8671352f4edca38b029018bfc95a468a95fb
時分百刻
晝夜十二時均分百刻
一時有八大刻二小刻
大刻總九十六
小刻總二十四
```

This directly fixes the hundred-ke arithmetic architecture in a securely pre-1578 print witness.

## 5. p37 — decisive half-Zi wording

```text
SHA256=908d0c1162f46090c1e57d1a4d2279b934a957db1e5fec0bb3900276c5b2bc3c
若子時則上半時在夜半前屬昨日
下半時在夜半後屬今日
古曆每時以二小刻為始乃各繼以四大刻
重刊革象新書上終
```

This is direct page-level evidence; OCR/text extraction is not used as glyph authority.

## 6. Recension comparison

```text
1520 Gexiang: 若子時則上半時在夜半前屬昨日 / 下半時在夜半後屬今日
later CADAL Gexiang: 子時之上一半在夜半前屬昨日 / 下一半在夜半後屬今日
Shendao v11: 若子時則上半時在夜半前屬昨日 / 下半時在夜半後屬今日
Sanming 1578: 若子時則上半時在夜半前為昨日 / 下半時在夜半後屬今日
```

Therefore the closer `若子時則上半時...` construction is physically attested inside Gexiang by 1520; the 1520 Gexiang and reviewed Shendao wording are identical at this clause; exact Sanming preserves the same construction with `為昨日 / 屬今日`. The later CADAL wording proves recension variation within Gexiang and must not be projected backward onto every witness.

## 7. Stemma adjudication

```text
SECURELY_PRE1578_GEXIANG_HALF_ZI_PHYSICAL_WITNESS=YES
CLOSER_RUO_ZISHI_ZE_WORDING_PRE1578=YES
NCL06265_1520_TO_SHENDAO_DIRECT_COPY=UNPROVED
NCL06265_1520_TO_SANMING1578_DIRECT_COPY=UNPROVED
```

Chronology and near-verbatim mechanics materially strengthen Gexiang as a textual antecedent, but direct transmission direction still requires citation, copy statement, or an independently closed stemmatic intermediary. The existing Gexiang -> Sanming edge therefore remains a textual ancestry candidate, not a direct-copy edge.

## 8. Probe-metadata firewall and repair

The exploratory `NLC892-1253-204870/204871` workflows had initially copied `平圖011907-011908` / Zhengde-15 identity from a separate catalog line without proving cross-copy identity. Batch 12DC corrects those workflow manifests: NLC892 remains literal, Pingtu cross-copy identity is unresolved, and Zhengde-15 must not be promoted onto that surrogate without a source-bound bridge.

No durable Matrix/source-registry/graph adjudication had promoted that exploratory overbinding, so this repair does **not** increment the formal provenance-defect counter. The controlling 1520 evidence for this batch is NCL-06265.

## 9. Product adjudication

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
HPA_ZDATE_006=MISSING_FROM_PRODUCT
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=12
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=12
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

This batch strengthens provenance/stemma only. It does not choose a runtime time standard, implement upper-Zi -> Hai branch reassignment, or collapse candidates.

## 10. Next gate

The textual pre-1578 gate from Batch 12DB is now closed. Highest-value work returns to the unresolved numeric/mechanical stemma:

1. locate a pre-1578 Chinese carrier of the exact Sanming/Yueling `十三後 / 雨水後四日` change-day fingerprint;
2. continue the pre-1578 Nanjing/Datong **59/41** table-level carrier search;
3. identify the historically attested threshold/selection rule mapping the C-II-N daily curve to the whole-ke Sanming ladder.

Research record: `docs/research/ZIWEI-GEXIANG-ZHENGDE15-1520-PRE1578-TEXTUAL-WITNESS-R1.json`.
