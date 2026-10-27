# Fusion Chart Historical Provenance Audit R1 — Batch 12CF

## 1447《明英宗實錄》物理核讀：南京59刻層前推至正統十二年官方記錄

Status: **PRE-1578 OFFICIAL MING RECORD PHYSICALLY CONFIRMS NANJING SOLSTITIAL 59-KE STANDARD AND BEIJING 62-KE CONTRAST / PALACE AND GOVERNMENT CLEPSYDRA ARROWS EXPLICITLY IDENTIFIED AS NANJING OLD STYLE / 59 IS DIRECTLY PRINTED; 41 IS ONLY THE HUNDRED-KE COMPLEMENT, NOT A PRINTED NUMERAL IN THIS MEMORIAL / PRE-1578 NANJING 59 LAYER CLOSED / COMPLETE SANMING MULTIPOINT TABLE GENEALOGY STILL OPEN / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO HAI VOTE / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Why this is decisive after 12CE

Batch 12CE showed that Ming calendrical transmission could preserve multiple day/night-ke tables side-by-side, and that the later 1600 Xing Yunlu text explains a Nanjing 59-ke layer distinct from Yandu 62-ke. The remaining chronology problem was whether Nanjing 59 could be locked **before 1578**.

Batch 12CF closes that subproblem with an official 1447 record.

## 2. Physical source binding

NLC/Wikimedia object:

```text
TITLE=明英宗睿皇帝實錄 三百六十一卷 第16冊
AUTHOR=孫繼宗等纂修
EDITION=抄本, 12行24字, 平館藏書
CATALOG_DATE=明[1368-1644]
CONTENTS=卷158-169
PDF_PAGES=104
RUN=34867577915
JOB=104055174135
ARTIFACT=10357442493
ARTIFACT_DIGEST=sha256:f1bd8daba93a6c5752b99da13f465a1802ed01090dc001d2be4075bc7fa14d0f
SOURCE_SHA256=1e9546177289930ae33a64793df94518fcc21c90184c935a30ea975461990268
P21_SHA256=613e026a94949cf721088225d7215dedd94f9a8faad2529f164e8886946975fb
P28_SHA256=b7d95f00fd529468c4242f60b7255b5305df6298d14841a9d9f6ac03eccccfea
P30_SHA256=fa8f7c30b2ede6b10379fb12c4ba2366ab8b93968cfb201ae565c4ae30852b35
OCR_USED_FOR_FINAL_GLYPH_JUDGMENT=false
```

Page binding is direct: p21 opens 卷160 and 正統十二年十一月; p28 contains the target 甲寅 memorial; p30 opens 卷161 / 十二月.

## 3. Secure p28 reading

The target passage identifies `欽天監監正彭德清` and records a measured locality difference between Nanjing and Beijing. Secure core:

```text
南京北極出地三十六度，北京出地四十度強。
南京冬至 ... 夜刻五十九；夏至 ... 晝刻五十九。
北京冬至 ... 夜刻六十二；夏至 ... 晝刻六十二。
各有長短差異。今宮禁及官府漏箭，皆南京舊式，不可用。
上令內官監改造。
```

This is not a late retrospective explanation: it is an official entry dated 正統十二年十一月甲寅 (1447), about 130 years before the 1578 Sanming witness.

## 4. Precision firewall: 59 is printed; 41 is derived

The memorial itself prints the Nanjing extreme as `五十九` and the Beijing extreme as `六十二`. It does **not** print the complementary numerals `四十一` or `三十八` in this locus.

Therefore the safe formulation is:

```text
DIRECT: Nanjing solstitial extreme = 59 ke
DIRECT: Beijing solstitial extreme = 62 ke
DERIVED under the independently established 100-ke day/night total:
  Nanjing complement = 41
  Beijing complement = 38
```

This distinction is now machine-recorded so later work cannot silently turn an inferred complement into a direct quotation.

## 5. Historical consequence for Sanming

The 1578 Sanming display has `夏至 59/41`. Batch 12CF now proves that a Ming Nanjing 59-ke solstitial standard was already officially articulated in 1447. Accordingly:

- the **pre-1578 Nanjing 59 layer is closed**;
- Xing Yunlu 1600 is no longer needed to establish that layer chronologically; it remains a useful later explanatory confirmation;
- the Sanming summer-solstice 59 value has a genuine pre-1578 Ming/Nanjing technical precedent;
- but this does **not** prove Sanming copied the Yingzong Shilu memorial or any specific official table.

## 6. What remains open

The unresolved genealogy is now narrower:

```text
1447 official Nanjing 59-ke layer  ->  ?  ->  1578 Sanming multipoint table
```

We still need a pre-1578 table, manual, almanac or generative rule that links the Nanjing 59-ke endpoint to Sanming-like intermediate anchors such as `42/58`, `45/55`, `47/53`, `48/52`.

## 7. Product adjudication

For `HPA-ZDATE-006`:

- pre-1578 Nanjing 59-ke locality layer: **closed / official physical evidence**;
- exact pre-1578 Sanming multipoint table parent: **open**;
- upper-Zi -> Hai mechanical vote: **0**;
- runtime candidate/winner/collapse: **none**;
- algorithm reopen: **no**;
- status: **MISSING_FROM_PRODUCT**.

Research record: `docs/research/ZIWEI-YINGZONG-SHILU-1447-NANJING-59-41-PHYSICAL-COLLATION-R1.json`.
