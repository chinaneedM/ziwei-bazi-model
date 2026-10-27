# Fusion Chart Historical Provenance Audit R1 — Batch 12AV

## 1697《三才發秘》人部卷一《祿命》夜子非亥、作亥論與夜生八字差謬直接物理校勘

Status: **HARVARD-YENCHING V8 INTERNAL 人部卷一 MAPPING DIRECTLY CONFIRMED / 祿命 CHAPTER DIRECTLY COLLATED / PRE-MIDNIGHT HALF-ZI EXPLICITLY `子時並非亥時` / `作為亥論` DIRECTLY LINKED TO NIGHT-BIRTH BAZI ERROR / SAME-WORK SECOND CONTEXT NOT AN INDEPENDENT LINEAGE VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Question

Batch 12AU physically established in《三才發秘》天部卷二 that Chen Wen reports a real contemporary practice:

```text
往往以夜子作亥
用于尅擇祿命
```

while rejecting that practice.

Batch 12AV asks a narrower follow-up:

> Does the same 1697 work restate this dispute inside its actual `祿命` section and directly connect `作亥論` to errors in birth Bazi?

Answer: **yes**.

## 2. Source and physical locator

Controlling Harvard-Yenching object:

```text
COMMONS_FILE=File:Harvard drs 52822721 三才發秘天部二卷 v.8.pdf
COMMONS_SHA1=3ffab4bfd0c74dbfc2a226f2cb593834323ba87d
PDF_SHA256=a223ddedf04b5befd61a96bf742b1a7b07d329142e688354fbe7398271ea5f55
PDF_PAGE_COUNT=37
```

The Commons filename keeps the generic string `天部二卷`, but the physical internal title controls the actual section. Direct review of PDF p8 reads:

```text
三才發秘人部卷一
新安陳雯耕山氏著述
祿命
```

Therefore:

```text
HARVARD_V8_PHYSICAL_OBJECT -> 人部卷一 -> 祿命
```

The filename must not override the internal physical title.

## 3. Acquisition chain

### R1 — broad opening window

```text
RUN=34559414507
ARTIFACT=10183775321
DIGEST=sha256:c4cba76fc32c65462ef5d8bf912b5df4b72a41c62993ce6b209070cf724ebbd1
RENDERED=P1-P20 @ 260 DPI
OCR_USED=false
```

Direct visual review localized the target to pp8–10.

### R2 — exact target lock

```text
RUN=34559639606
ARTIFACT=10183846953
DIGEST=sha256:6ed297ce11264c695310561f9befd4fae5aa77cbf224b039a6f311c97a874b7d
RENDERED=P8-P10 @ 400 DPI
OCR_USED=false
P8_SHA256=d1594eaee1925b7a78910738fe1745dc27d2af85ddf84a8fb8bfb0ce4bc70ff6
P9_SHA256=65c5f9f0b86935713a2eb1330874cc116b4f339bbedc50f1df5dc04dafbf3183
P10_SHA256=f74eab5d31b8ec24039d191f9b1d5a918c68ee8b3d92d47cc565f93eaad3ba01
```

Received CText/Shidian text was used only as a locator/control. Decisive glyph claims come from the Harvard page images.

## 4. Direct physical collation

The p9–p10 discussion moves from calendrical/stem-branch construction into the Zi boundary. On p10 it directly states:

```text
子時前四刻尚屬去日
交後四刻方屬今日
```

and:

```text
皇曆有正子夜子之別
```

The key branch statement is explicit:

```text
故夜半前之四刻乃是子時並非亥時
```

followed by:

```text
若立支幹當立明日子時枝幹
```

Later on the same physical page the natal consequence is stated:

```text
半夜之前卻有半個子時
時人亦不知又作為亥論
故在夜生者所生八字多有差謬
```

## 5. Mechanical reading

Within Chen Wen's own preferred system:

```text
pre-midnight four ke -> still Zi branch
pre-midnight four ke -> previous-day side for date attribution
stem/branch assignment -> use the coming/current Zi-hour stem-branch sequence described by the text
pre-midnight Zi != Hai
```

The competing historical practice is simultaneously preserved as an attested error:

```text
some practitioners -> pre-midnight/night Zi treated as Hai
application -> natal Bazi / 禄命
authorial verdict -> wrong; produces errors for night-born charts
```

This is stronger than a generic calendrical dispute because the criticism sits **inside the work's dedicated 祿命 chapter** and directly names `所生八字`.

## 6. Relationship to Batch 12AU

12AU and 12AV are two internal contexts in the **same 1697 work**:

```text
12AU 天部卷二:
  往往以夜子作亥
  用于尅擇祿命
  author rejects it

12AV 人部卷一祿命:
  夜半前之四刻乃是子時並非亥時
  時人亦不知又作為亥論
  夜生者所生八字多有差謬
```

They strongly establish authorial consistency and natal application scope.

They do **not** count as two independent lineage votes. Evidence weighting must not convert repeated passages within one work into a false majority.

## 7. Relationship to the Fullbook rule

The Fullbook physical rule remains:

```text
子時有十刻
上五刻屬昨夜亥時
下五刻屬今日子時
```

The 1697《三才發秘》authorial rule is opposed at the branch-classification level:

```text
night/pre-midnight Zi -> Zi, not Hai
```

while also directly reporting that other practitioners did use:

```text
night Zi -> Hai
```

Therefore the historical record now contains a directly documented rule controversy:

```text
Candidate A: previous-day attribution while retaining Zi branch
Candidate B: night/upper Zi reclassified to Hai branch
```

Candidate B is not a modern invention; Candidate A is not merely a modern objection. Both are historically real operations.

What remains unresolved is their chronology, textual genealogy, school scope and runtime priority.

## 8. Candidate-policy consequence

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
DISPUTED_HISTORICAL_OPERATION=true
PRESERVE_SEPARATE_CANDIDATES=true
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

No product code is changed by this batch.

## 9. Separate cloudy/rain issue remains open

This batch does not address:

```text
如天氣陰雨之際必須羅經以定真確時候
```

The missing source-scoped mechanical edge for acquiring **current time under cloudy/rain conditions** remains unresolved and must not be conflated with the late-Zi branch dispute.

## 10. Accounting

```text
ROW_COUNT=198
AUDITED_ROW_COUNT=166
MISSING_FROM_PRODUCT=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_PROVENANCE_DEFECTS=11
REPAIRED_PROVENANCE_DEFECTS=11
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

## 11. Durable artifact

```text
docs/research/ZIWEI-SANCAI-1697-LUMING-NIGHT-ZI-HAI-ERROR-R1.json
```

## 12. Next gate

Same-work corroboration is now sufficient. Do not keep mining《三才發秘》for additional votes on the same proposition unless a genuinely new mechanical detail appears.

The next late-Zi priority is an **earlier or textually independent physical witness**. A high-value route is the 1593/1594 `《新編評註通玄先生張果星宗大全》`: official bibliographic records identify Ming Wanli editions, while received text contains the same birth-time problem (`以子為亥，亥為子`) and a `七政曆` night-Zi four-ke split. Those received statements must be rebound to a physical edition before they are used as historical glyph authority.

In parallel, continue the independent Fullbook cloudy/rain current-time acquisition chain.
