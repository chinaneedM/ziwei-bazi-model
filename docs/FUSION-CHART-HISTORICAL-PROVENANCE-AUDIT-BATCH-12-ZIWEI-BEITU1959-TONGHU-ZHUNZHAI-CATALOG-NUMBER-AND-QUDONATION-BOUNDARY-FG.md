# Fusion Chart Historical Provenance Audit R1 — Batch 12FG

## 1959《北京圖書館善本書目》3482/3483 與國圖 OPAC「原文獻03482/03483」跨接：閉合歷史目錄號，並限定「瞿捐」負證據邊界

Status: **BEITU-1959 TARGET ENTRIES DIRECTLY COLLATION-CLOSED / 3482 TONGHU + 3483 ZHUNZHAI HISTORICAL CATALOG-NUMBER LAYER CLOSED / OPAC 03482↔1959 3482 AND 03483↔1959 3483 CROSSWALK CLOSED AT BIBLIOGRAPHIC-NUMBER LEVEL / TARGET ENTRIES NOT MARKED 瞿捐 / SAME CATALOG EXPLICITLY USES 瞿捐 ELSEWHERE / QU-DONATION ROUTE NOT ATTESTED BY THIS CATALOG BUT NOT HISTORICALLY DISPROVED / CURRENT PHYSICAL SHELFMARK STILL NOT CLOSED / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12FF closed the NLC OPAC reproduction/source-record chain and directly exposed:

```text
原文献03482铜壶漏箭制度、03483准斋心制几漏图式为一册
```

but intentionally refused to classify `03482/03483` as physical call numbers because the reviewed OPAC surface labelled them only as `原文献` numbers.

12FG returns to the 1959 printed `《北京圖書館善本書目》` and asks two narrower questions:

1. do the exact target titles carry printed numbers 3482/3483 in the historical catalog?
2. does that same catalog explicitly use `瞿捐` as an acquisition/provenance notation on other entries, and if so are the target entries so marked?

## 2. Source-bound target-page collation

Volume 4 of the 1959 catalog was acquired from the public-domain Wikimedia scan `SSID-12335510`.

Controlling workflow:

```text
RUN      = 36013592896
ARTIFACT = 10813571631
DIGEST   = sha256:769638c723dc1bacbb2b385b1669fc1cbc103866b2eff800184b346ddf05386f
SOURCE   = sha256:f762a4d2f0f1c96e5f8543f6b572988b0a0e17125f491522a1f2a035d4145ddb
PAGE 60  = sha256:722fce53457f722df9d2d7184646e2bf53427f56fa23ed518818d9ffdf2756c1
OCR_USED = false
```

Direct 400-dpi review of PDF p60, under `天文算法類`, reads the two adjacent target entries:

```text
銅壺漏箭制度一卷
清道光三年黃氏士禮居抄本
與準齋心製几漏圖式合一冊
printed number: 三四八二

準齋心製几漏圖式一卷
宋孫逢古撰
清道光三年黃氏士禮居抄本
黃丕烈跋
與銅壺漏箭制度合一冊
printed number: 三四八三
```

The page therefore independently reconfirms the 1823 Huang Shiliju provenance and the one-volume Copper+Zhunzhai binding already seen in the NLC OPAC chain.

## 3. 3482 / 3483 identifier adjudication

The 1959 printed catalog places the target records at sequential numbers:

```text
3482 = 銅壺漏箭制度
3483 = 準齋心製几漏圖式
```

NLC OPAC 12FF independently states:

```text
原文献03482铜壶漏箭制度
原文献03483准斋心制几漏图式
```

Exact title + exact number pair + exact 1823 Huang Shiliju provenance + exact one-volume relationship converge. Therefore:

```text
OPAC 原文献03482 ↔ 1959 printed catalog 3482 = CLOSED_AT_HISTORICAL_BIBLIOGRAPHIC_NUMBER_LEVEL
OPAC 原文献03483 ↔ 1959 printed catalog 3483 = CLOSED_AT_HISTORICAL_BIBLIOGRAPHIC_NUMBER_LEVEL
```

The leading zero is treated as OPAC formatting, not a new object identity.

This does **not** authorize:

```text
3482/3483 == current NLC physical shelfmark/barcode      NOT PROVED
3482/3483 == acquisition/donation number                 NOT PROVED
001411999008601 == physical shelfmark                    NOT PROVED
00O003570 == physical shelfmark                          NOT PROVED
rarecatx0514818 == 3482                                  NOT PROVED
```

The safe classification is **historical Beijing Library catalog/book-number layer, later reused by OPAC as the 原文献 number**. Modern scholarship sometimes describes such 1959 numbers as 書號 or 索書號; 12FG does not silently equate that historical retrieval/catalog number with a current NLC item barcode or present shelfmark.

## 4. Same-catalog `瞿捐` control

The earlier text-layer probe for `瞿捐` failed because the scan has no usable Chinese text layer. That failure had zero negative authority.

A complete image-only pass of volume 7 localized the relevant control to PDF p19. A bounded 400-dpi render then closed the glyph reading.

Controlling workflow:

```text
RUN      = 36015952183
ARTIFACT = 10814199731
DIGEST   = sha256:009f045ff614e835990bd84fd5c91f93a314249d8e155ab32118ab2068e07b02
SOURCE   = sha256:04a9b1e1a2aa0d3928a6facf499b76464607b26f506afc58a7b8f5325f335e0c
PAGE 19  = sha256:05b64be88917364c2528ac01f85edd02a098db0b0be34d7f233ca468cabe2467
OCR_USED = false
```

The page directly reads a `金華黃先生文集四十三卷` entry with:

```text
元黃溍撰
元刻明修本
一冊
瞿捐
```

Thus the same 1959 catalog demonstrably uses `瞿捐` as an explicit entry-level source/donation notation.

## 5. Target `瞿捐` boundary

The direct p60 target entries for 3482/3483 contain the title, edition/provenance, Huang Pilie note and one-volume binding, but no `瞿捐` annotation.

Therefore the source-bound conclusion is:

```text
1959 catalog explicitly marks some entries 瞿捐                    CLOSED
3482/3483 target entries are marked 瞿捐                           FALSE
1959 catalog directly attests Qu donation for this target volume    NO
historical Qu-family donation route absolutely disproved            NO
final acquisition/transfer path into Beijing/NLC                    UNRESOLVED
```

The last two lines are essential. Absence of an entry-level source mark is bounded negative evidence, not proof that no donation, sale, transfer, purchase, or other custody event occurred. Modern NLC scholarship itself documents 1959 entries whose provenance/source was not recorded in the catalog, so a missing notation cannot bear unlimited negative weight.

Wang Xiaohu's 2014 secondary study independently reports that he did not locate these two works in the separate `《瞿氏藏书捐赠北京图书馆书目》` and left the exact NLC acquisition route open. 12FG uses that only as secondary corroboration; the direct 1959 printed pages remain controlling for the catalog-level claim.

## 6. Object-level consequence

The historical record stack is now:

```text
1823 Huang Shiliju manuscript/composite object
  -> later Tieqin Tongjianlou ownership seal directly closed
  -> 1959 Beijing Library catalog: 3482 Copper + 3483 Zhunzhai, one volume
  -> 1985 NLC microfilm record / original-doc chain: 03482 + 03483
  -> current union-catalog record: rarecatx0514818 for Copper
```

The 1959↔OPAC historical-number bridge is closed. The exact current physical shelfmark and the legal/acquisition event by which the object entered the national library remain open.

Because the 1959 catalog itself gives the exact same 1823 Huang Shiliju one-volume signature, the NLC object-family convergence strengthens further. It still does not erase Huang's `原書舊鈔 / 錄副` multi-copy firewall or authorize a formal `SAME_OBJECT` collapse with every historical description.

## 7. Transmission-genealogy consequence

12FG adds:

- `CATALOG-BEITU-1959-TONGHU-ZHUNZHAI-3482-3483`;
- `TG-E0110` as an `ATTESTS` edge to the current NLC 1823 Huang Shiliju physical-object node.

It also refines the 12FF OPAC identifier semantics:

- `03482/03483` are no longer merely unclassified `原文献` numbers;
- they are cross-bound to the 1959 catalog's printed 3482/3483 bibliographic-number layer;
- this is **not** a current physical-shelfmark closure.

No `SAME_OBJECT`, direct-copy or Sanming-parent edge is authorized.

## 8. Chronology / product firewall

Nothing in the 1959 catalog dates the composition of Zhunzhai, proves a pre-1578 exact 25-arrow physical witness, or closes the Sanming/Yueling target-table parent.

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

1. reacquire original NLC OPAC doc `001775083` / item page when reachable and capture any explicitly labelled **current** call number, barcode or item identifier;
2. resolve `001411999008601` and `00O003570` from first-party field labels;
3. continue acquisition/transfer research beyond the 1959 catalog: Qu-family donation list, sale/transfer records, accession registers or NLC archival descriptions;
4. keep the independent pre-1578 Zhunzhai text line and Sanming/Yueling Dahan–Rainwater + Nanjing-59 lines active.

Research record: `docs/research/ZIWEI-BEITU1959-TONGHU-ZHUNZHAI-CATALOG-NUMBER-AND-QUDONATION-BOUNDARY-R1.json`.
