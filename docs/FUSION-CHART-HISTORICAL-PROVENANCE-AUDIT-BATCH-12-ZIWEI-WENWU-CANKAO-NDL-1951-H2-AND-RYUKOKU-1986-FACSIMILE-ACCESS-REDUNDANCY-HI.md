# Fusion Chart Historical Provenance Audit R1 — Batch 12HI

## 《文物参考资料》1951年第9期：NDL原刊合订对象 + 龙谷1986影印本访问冗余

Status: **NDL ORIGINAL 1951 H2 PAPER BUNDLE CLOSED / TARGET V2N9 EXPLICITLY INSIDE NDL 2(7)-2(12) OBJECT / RYUKOKU 1986 WENWU-PRESS FACSIMILE ROUTE CLOSED / NO ITEM-SPECIFIC DIGITAL SURROGATE EXPOSED ON REVIEWED NDL RECORD / DIRECT ARTICLE TEXT NOT REVIEWED / ZERO PRODUCT, MATRIX, RUNTIME OR GENEALOGY CHANGE**

## 1. Why this batch matters

12HH already closed five exact original-issue physical holdings for `1951年第9期 / volume 2 issue 9`.

12HI adds two different access redundancies:

1. an NDL **original-serial paper object** whose held range explicitly contains issue 9;
2. a separately cataloged **1986 Wenwu Press facsimile** covering the whole 1951 volume 2.

Neither is counted as direct text review.

## 2. NDL original second-half object

NDL Search directly exposes:

```text
文物参考资料
2(7)-2(12) 1951
call: Z8-AC150
material: 紙
publisher display: 文物出版社
```

Record:
`https://ndlsearch.ndl.go.jp/books/R100000002-Ia0000051292-i25241426`

Because the target is `2巻9期`:

```text
2(9) ∈ 2(7)-2(12)
```

Therefore:

```text
NDL_ORIGINAL_TARGET_ISSUE_PHYSICAL_ROUTE = CLOSED
```

The record remains a paper-material record.

## 3. NDL digital-access boundary

The reviewed object page did not expose a target-specific digital-surrogate URL or page viewer. Following the generic `インターネットで資料を読む` label led to NDL's general help page rather than target page images.

So:

```text
ITEM_SPECIFIC_DIGITAL_SURROGATE_EXPOSED = false
PUBLIC_DIGITAL_AVAILABILITY_PROVED_FALSE = false
DIRECT_SCAN_BYTES_RECOVERED = false
```

Absence of a target-specific digital link on the reviewed record is not proof that no digital surrogate exists anywhere.

## 4. Ryukoku 1986 facsimile route

龍谷大学図書館's first-party OPAC records:

```text
文物参攷資料
影印本
北京 : 文物出版社, [1986]
13冊
NCID AN10296217
```

大宮図書館 holding:

```text
call 054/638
1-12;2;1952-1958
1950-1950;1951-1951;1952-1958
```

The bibliographic record explicitly states the original 1951 numbering as:

```text
2巻1期 (1951.1)-2巻12期 (1951.12)
```

Thus the facsimile holding covers the target 1951 volume 2.

## 5. Facsimile firewall

A facsimile catalog record is not page collation.

```text
FACSIMILE_ROUTE = CLOSED
TARGET_PAGE_TEXT = NOT_REVIEWED
PAGE_FOR_PAGE_FIDELITY_TO_ORIGINAL = NOT_INDEPENDENTLY_COLLATED
```

The facsimile must not be used to assert a textual reading until the target pages themselves are inspected.

## 6. Ding-six status

No new title was recovered in this batch.

```text
HF NAMED = 东家杂记 / 太平乐府
REMAINING FOUR = UNRESOLVED
HC/HF SIX IDENTITY = STRONGLY_COMPATIBLE_NOT_PROVED
```

## 7. Access-action firewall

```text
COPY_REQUEST_SENT=false
ILL_REQUEST_SENT=false
LIBRARY_ACCOUNT_ACTION=false
IDENTITY_TRANSMITTED=false
FEE_INCURRED=false
SCAN_BYTES_RECOVERED=false
```

## 8. Product / genealogy consequence

```text
NODES_ADDED=0
EDGES_ADDED=0
ACQUISITION_EDGE_AUTHORIZED=false
RUNTIME_RULE_CHANGE=false
ALGORITHM_REOPEN=false
CANDIDATE_COLLAPSE=false
MATRIX_COUNT_CHANGE=false
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains `198 / 166 / 10`; provenance metadata defects `14 / 14 repaired`; chart algorithm defects `0`.

## 9. Highest next gate

1. Directly inspect Zhao pp.221–233 in an original 1951 issue or lawfully accessible facsimile.
2. Compare against NDL-held 2011 `《赵万里文集》第1卷` p.197.
3. Recover the remaining four Ding titles before merging HC/HF traditions.
4. Continue 2018 pp.309–310, 1997 pp.446–449, Ji chapter 9, 2004 p.335/final `《編后記》` and the 2010 supplement route.

Research record: `docs/research/ZIWEI-WENWU-CANKAO-NDL-1951-H2-AND-RYUKOKU-1986-FACSIMILE-ACCESS-REDUNDANCY-R1.json`.
