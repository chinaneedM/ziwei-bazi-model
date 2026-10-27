# Fusion Chart Historical Provenance Audit R1 — Batch 12BV

## 《永樂大典》卷18764《四字經序》目標頁直接字形校勘：`古經云`、`雨露`、`子丑寅亥`

Status: **DIRECT NO-OCR PHYSICAL-GLYPH COLLATION COMPLETE FOR YONGLE-DADIAN 18764 PUBLIC FACSIMILE PAGE 3 / PHYSICAL PAGE DIRECTLY READS 四字經序 AND 且子丑寅亥 / 四箇時辰難以推分 / 古經云 / 天陰雨露時難定 / 便是神仙也有差 / BATCH-12BQ TRANSCRIPTION NOW PHYSICALLY ADJUDICATED / 1597 YIMEN PHYSICAL READINGS REMAIN 古人云 / 雨落 / 亥子丑寅 / REAL RECENSION VARIATION NOW PHYSICALLY CONFIRMED ON BOTH SIDES / NO STEMMATIC OR RUNTIME WINNER SELECTED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI-BRANCH MECHANICAL VOTE +0 / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope and exact evidence chain

Batch 12BQ located the inclement-birth-time passage on public scan page 3 of 《永樂大典》卷18764 but deliberately withheld glyph authority because the project had not yet rendered the facsimile directly. Batch 12BS subsequently established the 1597 《夷門廣牘》 side from physical glyphs. Batch 12BV closes the missing Yongle-side physical collation.

Exact evidence chain:

- source: Wikimedia Commons `永樂大典18764.pdf`, 42 pages;
- Commons file page: `https://commons.wikimedia.org/wiki/File:%E6%B0%B8%E6%A8%82%E5%A4%A7%E5%85%B818764.pdf`;
- Wikisource target-page binding: `https://zh.wikisource.org/wiki/Page:%E6%B0%B8%E6%A8%82%E5%A4%A7%E5%85%B818764.pdf/3`;
- source PDF SHA-256: `69a2f0e63685d674fd5e0ddcd7a5ccd687a725f19cc601f8e77d6d446beb9f87`;
- renderer commit/tree: `0f5a6daa9e7e0bc3901412083c07dd0183f58a88` / `0c2f707d6dcea3e8e8b2b542c7bab427954b1006`;
- successful GitHub Actions run: `34826953257`;
- artifact: `10340044845`, digest `sha256:7ba40557f877f583830ee7d66838473ad5bbd73f99fb73cc679f220e8b83f05b`;
- rendered target page 3 SHA-256: `12e3f12fc9aeeeab06c459788757de0325f0f6214e1d062a77cc4c77483d038f`;
- final glyph judgment was made by direct visual review of the 300-dpi rendered facsimile; no OCR was used.

## 2. Direct page-3 reading

Direct visual review of physical scan page 3 reads the local sequence as:

```text
四字經序
...
內有同時共數者有富有貴有壽有夭殊不知刻差時別且子丑寅亥
四箇時辰難以推分古經云天陰雨露時難定便是神仙也有差
旦夕將月建長短而推言萬無一失矣
```

The material loci are therefore physically adjudicated on the Yongle-Dadian extant facsimile side as:

| Locus | Direct physical reading |
| --- | --- |
| quoted-source formula | `古經云` |
| inclement phrase | `天陰雨露時難定` |
| difficult-hour order | `子丑寅亥` |
| positive continuation | `便是神仙也有差` |

This upgrades Batch 12BQ from convergent transcription plus facsimile locator to direct no-OCR physical-glyph authority for these exact loci.

## 3. Two-sided physical recension comparison

Batch 12BS directly read the securely dated 1597 《夷門廣牘》 《四字經》 witness as:

```text
唐明皇論
...
亥子丑寅
古人云
天陰雨落難定
便是神仙也有差別
```

Batch 12BV now establishes that the apparent differences are not artifacts of CText OCR on one side or Wikisource transcription on the other. The admissible classification is:

```text
SAME_SIZIJING_TEXT_FAMILY_AT_LONG_SEQUENCE_LEVEL
+ REAL_RECENSION_VARIATION_PHYSICALLY_CONFIRMED_ON_BOTH_SIDES
+ YONGLE_EXTANT_PHYSICAL_RECENSION = JIAJING_DUPLICATE_LINEAGE
+ YIMEN_PHYSICAL_PRINT = 1597
+ NO_STEMMATIC_WINNER_SELECTED
```

The physical readings do not establish that either recension is the archetype. `古經` identity remains unresolved, Taiwan NCL 15275-0058 target-body glyphs remain inaccessible at the current lawful public-route boundary, and no direct-copying direction is inferred.

## 4. Effect on HPA-ZDATE-006

The sequence `子丑寅亥` is a list of four difficult birth hours. It does **not** say that the upper half of Zi hour becomes Hai, nor does it define a runtime branch-reclassification function. Likewise `天陰雨露時難定` describes uncertainty under inclement conditions but gives no complete current-time acquisition mechanism.

Therefore:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`;
- direct Yongle-Dadian target-page physical-glyph witness increment: `+1` at the textual-variant layer;
- two-sided physical recension-variation confirmation: `true`;
- Hai-branch mechanical vote increment: `0`;
- Fullbook cloudy/rain current-time acquisition mechanism closed: `false`;
- runtime winner selected: `false`;
- candidate collapsed: `false`;
- algorithm reopen authorized: `false`.

Global accounting remains `198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families`; provenance defects remain `11/11`; chart algorithm defect/reopen/collapse remain `0/0/0`.

## 5. Next gate

1. Continue the distinct Fullbook-line operational question: find an explicit cloudy/rainy **current-time acquisition procedure**, not merely a statement that time is difficult to determine.
2. Continue lawful search for a Taiwan NCL 15275-0058 target-body image route; if eventually obtained, compare it against both physically adjudicated recensions without assuming impression identity.
3. Treat the Yongle/Yimen physical differences as genuine recension evidence for philology and provenance only; do not convert their four-hour order into a late-Zi-to-Hai mechanical vote without an explicit operational rule.

Research record: `docs/research/ZIWEI-YONGLE-DADIAN-18764-DIRECT-GLYPH-COLLATION-R1.json`.
