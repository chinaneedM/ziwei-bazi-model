# Fusion Chart Historical Provenance Audit R1 — Batch 12AW

## 1594《新編評註通玄先生張果星宗大全》夜子四刻与子亥互误物理校勘

Status: **NIJL / TOHOKU WANLI-22 (1594) PHYSICAL WITNESS DIRECTLY COLLATED / BIRTH-TIME 子亥互誤 DIRECTLY ATTESTED / 七政曆 NIGHT-ZI UPPER-LOWER FOUR-KE DIVISION DIRECTLY ATTESTED / UPPER-ZI→HAI NOT DIRECTLY PROVEN BY THIS PAGE / EARLIER INDEPENDENT GENEALOGY STRENGTHENED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Question

Batch 12AV closed the same-work 1697《三才發秘》 evidence and explicitly required the next late-Zi step to be an earlier or textually independent physical witness. It named the 1593/1594《新編評註通玄先生張果星宗大全》 as a high-value target because received text contains both a birth-time 子/亥 confusion statement and a `七政曆` night-Zi four-ke split.

Batch 12AW asks:

> Can those received statements be rebound to a dated physical 1594 edition, and if so, how much of the later Zi/Hai candidate can that page actually prove?

Answer: **yes for the physical wording; no for an automatic upper-Zi→Hai equivalence**.

## 2. Controlling physical object

NIJL official IIIF manifest:

```text
BID=100238879
TITLE=新編評註通玄先生張果星宗大全
AUTHOR=陸位
DATE=万暦22
CANVAS_COUNT=439
ATTRIBUTION=東北大学附属図書館 国文学研究資料館
MANIFEST_SHA256=349da96570f24e59f8a875d6bbd806d5b4e0eee29344abc2769de7afb151a108
```

Therefore the reviewed target is not an undated web transcription or a later manuscript shortcut. It is directly bound to a **Wanli 22 / 1594 physical witness**.

The decisive leaf is:

```text
CANVAS=195
IIIF_SERVICE=https://kokusho.nijl.ac.jp/api/iiif/100238879/v4/THKW/THKW-04306/THKW-04306-00195.tif
2400PX_REVIEW_SHA256=39c22d31e99d950f4cfd81680fb12b537c55fa2425503a9b6f6c844a3f4fbfb6
```

OCR was used only as a locator. Final glyph claims come from direct visual review of the page image.

## 3. Direct physical collation

### 3.1 Main text

The natal/birth-time discussion directly reads:

```text
人命多有生時不定，以子為亥，亥為子，以初為末，末為初，則坐度不同……
```

This establishes that the 1594 work directly knows a **birth-time 子/亥 reciprocal misidentification problem**.

The syntax matters. This sentence is discussing inaccurate or uncertain birth time. It does **not** authorize us to convert `以子為亥` into a universal authorial rule.

### 3.2 Upper annotation

The same physical leaf contains an upper annotation whose securely legible core reads:

```text
七政曆所載，有夜子時之分，有上四刻下四刻之法；上四刻正陰，下四刻正陽。
```

This directly establishes a `七政曆`-framed **night-Zi upper/lower four-ke division** in the 1594 witness.

Only the mechanically necessary, securely legible core is normalized here. Damaged or unnecessary continuation characters are not silently supplied.

## 4. What the 1594 page proves

The following conclusions are direct:

```text
1594 physical witness exists and is date-bound.
Birth-time 子/亥 mutual misidentification is explicitly discussed.
A night-Zi upper/lower four-ke division is explicitly discussed.
The night-Zi split predates the 1697 Sancai discussion by more than a century.
```

The following stronger conclusions are **not** licensed by this page alone:

```text
upper four ke -> Hai branch
lower four ke -> Zi branch
modern 23:00/00:00 clock mapping
civil time vs mean-solar vs apparent-solar runtime binding
universal cross-edition Fullbook glyph stability
```

This distinction is required by the project's philological rule: nearby concepts and later mechanically explicit formulations cannot be backfilled into an earlier text unless the earlier syntax actually says them.

## 5. Relationship to 1697《三才發秘》

12AU/12AV established in Chen Wen's 1697 work:

```text
pre-midnight four ke -> Zi, not Hai
some practitioners -> 夜子作亥
application -> selection / natal Bazi
1697 author -> rejects the Hai treatment
```

12AW now adds an earlier **independent work**:

```text
1594 張果星宗:
  birth-time 子/亥 mutual misidentification is already a live problem
  七政曆 night-Zi upper/lower four-ke division is already known
```

This materially strengthens the chronology and genealogy of the controversy, but it does not turn the 1594 page into a vote for either 1697 authorial winner or the later Fullbook upper-Zi→Hai rule.

## 6. Relationship to the Fullbook HPA-ZDATE-006 candidate

The directly collated Fullbook/Nanyangtang candidate remains mechanically stronger and more explicit at the branch-classification layer:

```text
子時有十刻
上五刻屬昨夜亥時
下五刻屬今日子時
```

Batch 12AW shows that an earlier 1594 astral-calendar/natal tradition already contains the two ingredients around that later controversy:

```text
night-Zi internal split
Zi/Hai birth-time confusion
```

But it does **not** close the missing bridge:

```text
1594 upper four ke == Hai branch
```

Therefore:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
HISTORICAL_GENEALOGY_STRENGTHENED=true
EXPLICIT_UPPER_ZI_TO_HAI_VOTE_INCREMENT=0
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

## 7. Jangseogak control

Digital Jangseogak separately catalogs:

```text
DATA_ID=LIB_169178
CALL_NUMBER=PC9A-20 / C9A-20
CATALOG_CLAIM=中國木板本 / 萬曆22(1594) / 10卷10冊
```

This is a distinct institutional holding record and is useful for edition/bibliographic corroboration. However, the public image API probe did not expose the target leaf.

Consequently:

```text
JANGSEOGAK_BIBLIOGRAPHIC_CORROBORATION=true
JANGSEOGAK_TARGET_GLYPH_AUTHORITY=false
JANGSEOGAK_GLYPH_VOTE_INCREMENT=0
```

Do not count NIJL/Tohoku and Jangseogak as two matching text witnesses until the Jangseogak target page is actually read.

## 8. Evidence-weight consequence

The evidence stack is now sharper:

```text
1594 張果星宗 physical page:
  earlier independent genealogy for night-Zi split + Zi/Hai confusion

1697 三才發秘 physical pages:
  explicit contemporary 夜子作亥 practice reported and rejected
  explicit pre-midnight Zi != Hai

Fullbook/Nanyangtang physical page:
  explicit upper-five Zi -> previous-night Hai
  explicit lower-five -> current-day Zi
```

This is a genuine historical controversy with multiple mechanical layers. Source counting must not replace semantic comparison.

## 9. Accounting

No Matrix count changes are authorized by this batch:

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

## 10. Durable artifact

```text
docs/research/ZIWEI-ZHANGGUO-1594-NIGHT-ZI-PHYSICAL-COLLATION-R1.json
```

The earlier route artifacts remain useful as acquisition provenance:

```text
docs/research/ZIWEI-ZHANGGUO-NIJL-100238879-IIIF-R1.json
docs/research/ZIWEI-ZHANGGUO-NIJL-VOL8-OCR-LOCATOR-R1.txt
docs/research/media/batch-12aw-nijl-target-preview/manifest.txt
```

## 11. Next gate

Do not keep mining the same 1594 NIJL/Tohoku copy for repeated votes on this proposition unless a new mechanical detail appears.

The highest-value next targets are:

1. a directly readable **Jangseogak 1594 target leaf** or another independent copy of the same edition, to test textual stability rather than to inflate vote count;
2. an earlier or independent witness that explicitly states the missing bridge `upper/night Zi -> Hai branch`;
3. the separate Fullbook cloudy/rain current-time acquisition chain, which remains mechanically unresolved and must not be conflated with the late-Zi branch dispute.
