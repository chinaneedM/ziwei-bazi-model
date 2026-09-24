# Fusion Chart Historical Provenance Audit R1 — Batch 12FF

## 國圖 OPAC《準齋心製几漏圖式》縮微／原善本鏈：閉合伴隨記錄與「銅壺＋準齋」原文獻合裝，保留索書號分類防火牆

Status: **NLC OPAC ZHUNZHAI COMPANION RECORD CLOSED / MICROFILM DOC 002597934 -> ORIGINAL RARE-BOOK DOC 001775083 CLOSED / SOURCE CONTROL 001411999008601 OBSERVED / ORIGINAL-DOCUMENT 03482 TONGHU + 03483 ZHUNZHAI ONE-VOLUME BINDING CLOSED / 00O003570 SEPARATE TONGHU PHOTOGRAPH REFERENCE OBSERVED / UNIQUE PHYSICAL CALL NUMBER NOT CLOSED / RARECATX↔OPAC IDENTIFIER EQUIVALENCE NOT PROVED / TIEQIN UNIQUE-OBJECT FIREWALL PRESERVED / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12FE closed the public Chinese Rare Books Union Catalog record for `銅壺漏箭制度 / 抄本 / 清黃丕烈跋 / rarecatx0514818 / 中國國家圖書館`, but it still lacked:

- an official `準齋心製几漏圖式` companion record;
- an NLC object-level statement that Copper and Zhunzhai belong to the same source volume;
- a physical shelfmark, accession/donation number or other explicitly labelled unique physical identifier.

12FF follows the China NLC OPAC route without promoting database/control numbers into physical shelfmarks by appearance alone.

## 2. Source-bound OPAC capture

Workflow `36008292540`, artifact `10810554622`, digest:

`sha256:cf95715cd7f92c3df9fce626c716d32b3bbe4bfd8a4a4c86dda080a2f44c7ccb`

captured the first-party NLC OPAC page for:

`准斋心制几漏图式 [缩微品] : 一卷 / (宋)孙逢吉撰`

The captured HTML is hash-bound:

`sha256:5bf2bc998414724c8d52d869f615114c8cd83762afc13a4f850ff1a9e4baefc0`

Direct fields include:

```text
OPAC doc_number = 002597934
ID号            = 602003002862
版本项          = 发行拷贝片
出版项          = 北京 : 全国图书馆文献缩微中心, 1985
                 (北京 : 国家图书馆, 1985)
载体形态项      = 1盘卷片 : 正像, 1:10 ; 35mm
附加款目        = 黄丕烈 清 跋
馆藏            = 南区善本阅览室
```

The reviewed microfilm record's displayed `CALL-NO` field is blank. That blank must not be replaced by a guessed number from another field.

## 3. The decisive copied-from field

The same official OPAC page directly exposes a `复制自` link to original rare-book `doc_number=001775083`, followed by source metadata:

```text
001411999008601
准斋心制几漏图式
善本
抄本
黄氏士礼居 清道光三年[1823]
1册
原文献03482铜壶漏箭制度、03483准斋心制几漏图式为一册，
铜壶漏箭制度另拍在00O003570
```

This closes two questions that 12FE left open:

1. an official China NLC `準齋心製几漏圖式` companion/source record exists;
2. NLC itself states that original-document `03482 銅壺漏箭制度` and `03483 準齋心製几漏圖式` are **one volume**.

Therefore the companion-binding layer is no longer merely inferred from Huang/Tieqin provenance convergence.

## 4. Identifier-class adjudication

The evidence supports only the labels the source actually supplies:

```text
002597934      = OPAC microfilm bibliographic doc_number
602003002862   = displayed OPAC ID for that microfilm record
001775083      = linked original rare-book OPAC doc_number
001411999008601= source-control value in the copied-from field;
                 exact subtype not explicitly labelled on the reviewed surface
03482          = "原文献" number for 銅壺漏箭制度
03483          = "原文献" number for 準齋心製几漏圖式
00O003570      = "另拍在" reference for the separately photographed Copper item;
                 exact identifier class not explicitly labelled
```

Not authorized:

```text
03482/03483 == physical call numbers          NOT PROVED
001411999008601 == physical shelfmark          NOT PROVED
00O003570 == physical shelfmark                NOT PROVED
any of the above == acquisition/donation no.   NOT PROVED
rarecatx0514818 == 03482                       NOT PROVED
```

This is the same identifier firewall established in 12FE: record ID, source-control value, original-document number, microfilm reference, call number and accession/donation number are separate classes until the first-party source labels them.

## 5. Object-level consequence

The OPAC source field directly binds:

```text
黃氏士禮居
清道光三年 [1823]
1冊
03482 銅壺漏箭制度
03483 準齋心製几漏圖式
為一冊
```

This materially strengthens the current NLC 1823 composite-object reconstruction and closes the **official OPAC one-volume companion binding**.

It does not, by itself, close:

- `rarecatx0514818 ↔ 03482` as an exact cross-system identifier mapping;
- the exact physical shelfmark of the source volume;
- the acquisition/donation path into China NLC;
- which Huang layer is `原書舊鈔` versus `錄副`;
- formal unique-object identity with the specific physical copy described in the Tieqin catalog.

The Tieqin-object status therefore remains:

`VERY_STRONGLY_SUPPORTED_NOT_FORMALLY_UNIQUE_OBJECT_CLOSED`

rather than being silently promoted to a unique-object collapse.

## 6. Retry boundary

A follow-up workflow `36009054595` attempted to traverse the live source-record link and item page. It failed because `opac.nlc.cn` timed out before acquisition.

This failure has **zero negative content authority**. It does not negate the already captured first-party `复制自` field and does not prove that the source record lacks a physical call number.

## 7. Transmission-genealogy consequence

12FF adds:

- `CATALOG-NLC-OPAC-ZHUNZHAI-MICROFILM-002597934`;
- `TG-E0109` as an `ATTESTS` edge to the current NLC 1823 Huang Shiliju physical-object node.

The edge attests the official NLC reproduction/source-record chain and one-volume composite statement. It is **not** a `SAME_OBJECT` or direct-copy lineage collapse.

## 8. Chronology and product firewall

Nothing in this catalog/microfilm chain dates the work's composition or supplies a pre-1578 exact Zhunzhai rule witness.

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
MISSING_FROM_PRODUCT=10
PROVENANCE_DEFECTS=13/13_REPAIRED
CONFIRMED_CHART_ALGORITHM_DEFECTS=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
DIRECT_SANMING_PARENT_VOTE_INCREMENT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 9. Next gate

1. when the legacy OPAC is reachable, acquire original record `001775083` and its item page and capture any explicitly labelled call number/barcode/accession field;
2. resolve the exact first-party identifier classes of `001411999008601`, `03482`, `03483`, and `00O003570`;
3. seek acquisition/donation or Qu-family transfer documentation explaining how the composite object entered China NLC;
4. keep the pre-1578 Zhunzhai rule search and the independent Sanming/Yueling Dahan–Rainwater + Nanjing-59 lines active.

Research record: `docs/research/ZIWEI-NLC-OPAC-ZHUNZHAI-MICROFILM-SOURCE-CROSSBINDING-R1.json`.
