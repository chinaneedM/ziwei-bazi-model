# Fusion Chart Historical Provenance Audit R1 — Batch 12HA

## 国图《文津流觞》2023：铁琴铜剑楼“善本20种 / 收购190种”现代馆方回顾作用域

Status: **NLC FIRST-PARTY INSTITUTIONAL RETROSPECTIVE DIRECT PDF-TEXT CONTROL / QU-TIEQIN 20-TITLE + 190-PURCHASED-TITLE CLUSTER CLOSED AT MODERN RETROSPECTIVE LEVEL / NOT A CONTEMPORANEOUS ACCESSION LEDGER / COUNT RECONCILIATION FORBIDDEN / TARGET 3482-3483 TRANSACTION MODE STILL UNRESOLVED / ZERO PRODUCT, MATRIX, RUNTIME OR GENEALOGY CHANGE**

## 1. Why this batch matters

The repository already knows that the Qu/Tieqin transfer program contained both donation and priced-acquisition components. Batch 12FP deliberately kept later reported batch counts secondary because the direct Ji Shuying chapter and accession ledgers have not yet been collated.

A first-party National Library retrospective adds a new count-level institutional control.

## 2. First-party source

国家图书馆《文津流觞》2023年第4期 / 第八十四期 publishes:

- author: 马涛;
- affiliation: 国家图书馆研究院;
- article: 《王重民与鼎新之际的国家图书馆》.

The first-party issue index independently lists the article under the 王重民先生诞辰120周年纪念 section.

PDF:
`https://www.nlc.cn/upload/attachments/2023-12-18/56d6e51d.pdf`

Printed page 18 is inside:

```text
一、珍贵典籍的搜访与整理
```

The paragraph says Wang Zhongmin, while acting as Beijing Library director, supplemented holdings through several channels. Its first channel is government allocation of precious materials.

## 3. Tieqin cluster on printed p.18

Within that first channel, the PDF text layer directly exposes the contiguous sequence:

```text
江苏瞿氏铁琴一张、铁琴铜剑楼匾额1方、善本书20种及收购书190种
```

It is followed by a separately named Culture Ministry allocation of Song/Yuan/Ming rare books, 53 titles / 240 volumes.

Current adjudication:

```text
NLC_2023_QU_TIEQIN_20_190_CLUSTER
  = CLOSED_AT_MODERN_INSTITUTIONAL_RETROSPECTIVE_LEVEL

RARE_BOOK_TITLE_COUNT_DISPLAY
  = 20

PURCHASED_BOOK_TITLE_COUNT_DISPLAY
  = 190

SOURCE_IS_CONTEMPORANEOUS_1950_ACCESSION_LEDGER
  = false
```

The grammatical continuity strongly associates the 20-title and 190-title expressions with the immediately preceding Qu/Tieqin object cluster, but this is not an itemized ledger.

## 4. Visual-access boundary

The first-party PDF text layer was directly reviewed. The web PDF screenshot service was attempted twice for the target page and timed out; a secondary direct-container download also failed.

Therefore:

```text
PDF_TEXT_LAYER_DIRECTLY_REVIEWED = true
TARGET_PAGE_IMAGE_VISUALLY_REVIEWED = false
SCREENSHOT_TIMEOUT_COUNT = 2
```

For this modern born-digital wording, the text layer is usable as a direct first-party textual control, but the project does not claim visual glyph collation.

## 5. Count-reconciliation firewall

Batch 12FP records later secondary recountings such as a 1950 March purchase count of 123 titles and a 1953 purchase count of 300+ titles.

The NLC 2023 retrospective's `收购书190种` must **not** be silently normalized to either of those numbers.

Likewise, public accounts that mention a 20-title Qu donation must not be silently declared identical to this p.18 `善本书20种` until a direct batch/date/accession link is recovered.

```text
190 == 123
  = NOT_AUTHORIZED

190 == 1953_300_PLUS
  = NOT_AUTHORIZED

NLC_2023_20 == SPECIFIC_MARCH_1950_20_TITLE_DONATION
  = PLAUSIBLE_BUT_NOT_PROVED

COUNT_NORMALIZATION
  = FORBIDDEN_PENDING_DIRECT_LEDGER_SCOPE
```

## 6. Target-volume firewall

The target remains the single bound 1823 Huang Pilie / Shiliju manuscript associated with historical catalog nos. 3482 and 3483.

The NLC 2023 passage does not print:

- 《铜壶漏箭制度》;
- 《准斋心制几漏图式》;
- 3482 / 3483;
- 03482 / 03483;
- the 1823 Huang/Shiliju one-volume fingerprint;
- an itemized acquisition list or price ledger.

Therefore:

```text
TARGET_IN_20_TITLE_COMPONENT = UNRESOLVED
TARGET_IN_190_TITLE_COMPONENT = UNRESOLVED
TARGET_PURCHASE_SELECTED = false
TARGET_DONATION_SELECTED = false
TARGET_EXACT_ACQUISITION_DATE = UNRESOLVED
```

## 7. Product / genealogy consequence

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

Accounting remains `198 / 166 / 10`, provenance metadata defects `14 / 14 repaired`, chart algorithm defects `0`.

## 8. Highest next gate

1. Trace the 20/190 counts back to Beijing Library/NLC work reports, accession ledgers, acquisition lists or transfer records.
2. Do not reconcile `190` with the secondary `123` or `300+` reports without direct batch scope.
3. Search direct records for the target titles/numbers or the 1823 one-volume fingerprint.
4. Continue direct 1997 pp.446–449, Ji Shuying chapter 9, 2004 p.335/final 《編后記》 and the 2010 supplement route in parallel.

Research record: `docs/research/ZIWEI-NLC-WANGCHONGMIN-TIEQIN-20-DONATION-190-PURCHASE-INSTITUTIONAL-RETROSPECTIVE-SCOPE-R1.json`.
