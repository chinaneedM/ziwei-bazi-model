# Fusion Chart Historical Provenance Audit R1 — Batch 12FO

## 周叔弢日记旁证：高熙曾实际收书角色与瞿氏善本 1953 入藏时间边界

Status: **GAO OPERATIONAL BOOK-HANDLING ROLE DIRECTLY ATTESTED FOR 1952 ZHOU-SHUTAO DONATION EVENT / QU-FAMILY BOOKS AMONG BEIJING-LIBRARY NEW RECEIPTS BY 1953-05-29 CLOSED AT COLLECTION-LABEL LEVEL / TWO EVENTS MUST NOT BE MERGED / TARGET 3482-3483 TRANSACTION ROUTE UNRESOLVED / ZERO GENEALOGY OR RUNTIME CHANGE**

## 1. Question

Batch 12FN corrected the modern source attribution for the statement that Gao Xizeng left an annotated 《铁琴铜剑楼藏书目录》: the direct author is Lin Zhenyue in his signed preface.

The next question is whether contemporaneous material independently constrains two background facts:

1. did Gao Xizeng actually participate in physical rare-book collection/acquisition work with Zhao Wanli?
2. by what date were Qu-family books already being viewed as newly received rare books at Beijing Library?

The surviving published excerpts of Zhou Shutao's diary answer both questions — but in **different events**.

## 2. Source chain and mediation level

Zhou Qiqian's article 《〈周叔弢日记〉中的祖父及其友人》 was originally published in 《文汇学人》 issue 192 on 2015-04-10. A later public reproduction preserves the relevant entries:

```text
https://www.sohu.com/a/327835586_523187
```

Wenhui's 2019 article 《周叔弢张重威日记对读合璧举隅》 independently confirms the 2015 publication and describes the surviving Zhou diary corpus:

```text
https://www.whb.cn/zhuzhan/xueren/20190802/280856.html
```

A 2016 published annotation of Zhou Shutao's letters independently reproduces the 1952-08-31 diary entry and records that the 1952–1962 diary extract manuscript was then held by Zhou Jingliang:

```text
https://www.thepaper.cn/newsDetail_forward_1472173
```

The project has **not** directly reviewed an image of the relevant original diary manuscript page. Therefore this batch is a publication-mediated collation of contemporaneous diary content, not direct manuscript-image collation.

## 3. 1952-08-31: Gao Xizeng in actual book retrieval work

Published diary wording:

```text
张葱玉、赵万里、高熙曾来取藏书。
```

Some republications/annotations print the name as `高希曾`. 12FO treats this as a textual/name-form variant referring to Gao Xizeng; it does not create a second person.

The event concerns **Zhou Shutao's donated collection**. Its evidentiary force is:

```text
GAO_PRESENT_IN_PHYSICAL_BOOK_RETRIEVAL = true
ZHAO_WANLI_PRESENT                     = true
ZHANG_HENG_PRESENT                     = true

GAO_OPERATIONAL_COLLECTION_HANDLING_ROLE
  = DIRECTLY_ATTESTED_FOR_ZHOU_SHUTAO_DONATION_EVENT
```

It does **not** prove:

```text
GAO_HANDLED_QU_FAMILY_BOOKS = false / not proved here
GAO_ANNOTATED_TIEQIN_CATALOG_SOURCE_BASIS = not proved
```

## 4. 1953-05-29: Qu-family books among Beijing Library new receipts

Published diary wording:

```text
早到北京图书馆和徐森玉看新收善本书。涵芬楼，瞿氏。
```

This supplies a useful chronological control:

```text
BEIJING_LIBRARY_NEWLY_RECEIVED_RARE_BOOKS_REVIEWED = true
HANFENLOU_COLLECTION_LABEL_PRESENT                 = true
QU_FAMILY_COLLECTION_LABEL_PRESENT                 = true

QU_FAMILY_BOOKS_AMONG_REVIEWED_NEW_RECEIPTS
  = CLOSED_AT_COLLECTION-LABEL LEVEL

TERMINUS_ANTE_QUEM
  = 1953-05-29
```

But the terse diary does not name individual Qu titles.

Therefore:

```text
TARGET_TONGHU_ZHUNZHAI_NAMED     = false
TARGET_CATALOG_3482_3483_BOUND   = false
TARGET_TRANSACTION_MODE_CLOSED   = false
TARGET_EXACT_ACQUISITION_DATE    = unresolved
```

## 5. The critical cross-event firewall

These diary entries cannot be concatenated into a synthetic event.

Forbidden inference:

```text
1952: Gao handles Zhou donation
+
1953: Qu books appear among new receipts
=
Gao handled those Qu books
```

That equation is **not authorized**.

The correct model is:

```text
EVENT A
  person-role control:
  Gao Xizeng demonstrably participated in an actual Beijing-Library-related
  physical book retrieval operation with Zhao Wanli.

EVENT B
  collection chronology control:
  some Qu-family books were already among Beijing Library's newly received
  rare books by 1953-05-29.

A != B
NO EVENT-LEVEL IDENTITY BRIDGE
```

Accordingly, Lin Zhenyue's more specific modern assertion that Gao assisted Zhao in Qu-family book work is **not independently proved merely by combining these two diary entries**.

## 6. Adjudication

```text
GAO_OPERATIONAL_BEIJING_LIBRARY_COLLECTION_HANDLING_ROLE
  = CLOSED_FOR_1952_ZHOU_SHUTAO_DONATION_EVENT

QU_FAMILY_BOOKS_AMONG_BEIJING_LIBRARY_NEW_RECEIPTS_BY_1953_05_29
  = CLOSED_AT_COLLECTION_LABEL_LEVEL

DIRECT_GAO_TO_QU_FAMILY_TRANSFER_EVENT
  = NOT_PROVED_BY_THESE_DIARY_ENTRIES

GAO_ANNOTATED_TIEQIN_CATALOG_SOURCE_BASIS
  = UNRESOLVED

TARGET_TONGHU_ZHUNZHAI_PRESENCE_IN_1953_05_29_VIEWING
  = NOT_PROVED

TARGET_3482_3483_TRANSACTION_MODE
  = UNRESOLVED

FINAL_NLC_ACQUISITION_TRANSFER_PATH
  = UNRESOLVED
```

## 7. Source-quality firewall

The diary content is contemporaneous, but the reviewed access layer is mediated by later publications.

```text
CONTEMPORANEOUS_DIARY_CONTENT = true
DIRECT_TARGET_MANUSCRIPT_IMAGE_REVIEW = false
PUBLISHED_EXCERPT_MEDIATED = true
UNPUBLISHED_CONTEXT_MAY_BE_INFERRED = false
```

The wording may be cited as a published diary excerpt, but it must not be silently upgraded to direct manuscript collation.

## 8. Product / genealogy consequence

```text
NODES_ADDED=0
EDGES_ADDED=0
ACQUISITION_EDGE_AUTHORIZED=false
SAME_OBJECT_EDGE_AUTHORIZED=false
DIRECT_SANMING_PARENT_VOTE_INCREMENT=0
PRE1578_ZHUNZHAI_RULE_WITNESS_INCREMENT=0
MATRIX_ROW_COUNT_CHANGE=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains:

```text
Matrix rows / audited / missing = 198 / 166 / 10
provenance defects repaired     = 13 / 13
chart algorithm defects         = 0
```

## 9. Highest next gate

1. continue Batch 12FN's primary task: recover Lin Zhenyue's exact source basis for the Gao annotated Tieqin-catalog statement;
2. seek a direct image/transcription chain for the relevant Zhou Shutao diary pages where lawfully public;
3. search Beijing Library/NLC 1952–1953 accession/acquisition records for Qu-family title-level or catalog-number-level lists;
4. never infer Gao→Qu event identity solely from the two independent diary controls;
5. do not select donation/sale/purchase for catalog nos. 3482/3483 without direct or near-direct item evidence.

Research record: `docs/research/ZIWEI-ZHOU-SHUTAO-DIARY-GAO-ACQUISITION-ROLE-AND-QU-1953-CHRONOLOGY-R1.json`.
