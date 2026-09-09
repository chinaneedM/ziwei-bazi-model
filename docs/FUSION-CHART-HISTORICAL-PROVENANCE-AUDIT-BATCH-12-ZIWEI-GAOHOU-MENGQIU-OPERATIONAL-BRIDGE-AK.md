# Fusion Chart Historical Provenance Audit R1 — Batch 12AK

## 嘉慶徐朝俊《高厚蒙求》：羅經—晷器—陰雨鐘表—辨子亥 operational bridge

Status: **WASEDA FIRST-PARTY PHYSICAL SCAN BOUND / SOURCE-EMITTED 221-PAGE PDF DIRECTLY REVIEWED / 羅經 EMBEDDED IN SUNDIAL CONFIRMED / INCLEMENT-TIME CLOCK USE TO 辨子亥定支干 DIRECTLY CONFIRMED / LATER OPERATIONAL BRIDGE ONLY / NO FULLBOOK AUTHORIAL BINDING / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12AJ closed the philological firewall that `羅經` is not itself a clock and does not directly mean true/apparent solar time.

Batch 12AK asks a different question:

> Is there later historical evidence showing how Chinese technical practitioners actually combined compass orientation, astronomical time measurement, and no-sky fallback clocks in a way relevant to 子／亥 discrimination?

Yes — but only as a **嘉慶-period operational bridge**, not as a Ming Fullbook authorial specification.

## 2. First-party physical source

Waseda University Library directly catalogs:

- title: `高厚蒙求. 初集,2-3集`
- author: 徐朝俊
- call number: `ニ05 02158`
- imprint: `雲閒 : 徐氏, 嘉慶12-14[1807-1809]`
- third collection: `日晷測時図法. 星月測時図表. 揆日正方図表. 自鳴鐘表図法`

The Waseda archive page itself emits `ni05_02158.pdf`; the filename was not guessed.

```text
PDF_BYTES=74443272
PDF_SHA256=53ee7b0e59fbb92304af08d6f1b58226bee6fff85f23e5b43e830b76b967f1e4
PDF_PAGES=221
WORKFLOW_RUN=34327928353
ARTIFACT=10094524731
ARTIFACT_ZIP_SHA256=cf81d001e0a2022afd560f3fedc060aefbc8ecdc8bc9b14fb88f745b0633dec8
```

## 3. Direct no-OCR physical collation

### PDF p130

The third-collection title surface directly shows:

```text
定時儀器
高厚蒙求
嘉慶己巳鐫
雲間徐氏藏版
```

and the four technical groups:

```text
日晷測時圖法
星月測時圖表
揆日正方圖表
自鳴鐘表圖法
```

### PDF pp131–132

The 日晷 preface treats accurate time as instrument work tied to celestial motion, local `北極出地`, and alternative constructions using `羅經` and/or `節氣`.

The corresponding public transcription preserves:

```text
用羅經可不用節氣
用節氣可不用羅經
要未有不本北極出地而可隨處得實在真時者也
```

This is not used to equate `實在真時` with a modern runtime field; it describes Xu Chaojun's later sundial engineering framework.

### PDF p143 — 羅經平晷

The physical scan directly shows:

```text
一曰羅經平晷
此即徽地所製牽線取影晷也
```

with a diagram in which a circular compass/orientation component is integrated into the sundial plate.

Mechanical reading:

```text
羅經 = orientation component
晷影 geometry = time-reading mechanism
羅經 alone = not the clock
```

### PDF pp194–195 — 自鳴鐘表

p194 directly titles `自鳴鐘表圖法`.

p195 `鐘表圖說自序` directly reads:

```text
余既述日晷諸法以測晝時
復述星月儀表諸法以測夜時
而于陰雨晦冥之時尚未之及
因輯是編所以辨子亥定支干
非以供陳設玩好也
```

This is unusually close to the project question: a historical practitioner explicitly treats **inclement/dark-condition 子／亥 discrimination** as a precision timekeeping engineering problem.

## 4. What AK proves

The later 嘉慶 technical system explicitly separates functions:

```text
COMPASS / 羅經 -> orientation in sundial construction
SUN / 日晷 -> daytime time measurement
STAR/MOON INSTRUMENT -> nighttime time measurement
MECHANICAL CLOCK -> cloudy/dark fallback continuity
APPLICATION -> 辨子亥定支干
```

This supplies a concrete historical operational bridge for understanding why a Ziwei source could care intensely about accurate 子/亥 birth-time discrimination.

## 5. What AK does not prove

AK does **not** prove:

- that the Ming/Fullbook author used Xu Chaojun's procedure;
- that Fullbook `羅經以定真確時候` is shorthand for this exact later instrument stack;
- that Fullbook specifies civil time, local mean solar time, or local apparent solar time;
- that the runtime should select true/apparent solar time;
- that 嘉慶 practice may be projected backward as Ming authorial doctrine.

Therefore:

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_TIME_STANDARD_BINDING=LATER_OPERATIONAL_BRIDGE_CONFIRMED_FULLBOOK_SOURCE_SPECIFIC_BINDING_STILL_OPEN
CANDIDATE_SELECTION=NO
CANDIDATE_COLLAPSE=0
ALGORITHM_REOPEN=NO
```

## 6. Evidence hierarchy

1. Waseda first-party physical scan — controlling physical witness.
2. Shidian volume-three transcription — text-navigation/control surface bound to the physical work.
3. CText OCR — discovery/cross-check only; no glyph-level authority.

No same-work transcription is counted as another physical witness.

## 7. Accounting

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
PROVENANCE_METADATA_DEFECTS=10_CONFIRMED_10_REPAIRED
CHART_ALGORITHM_DEFECTS=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

## 8. Next gate

The remaining high-value gate is now sharper:

> Find a Fullbook-line or sufficiently early Ziwei/术数 witness that explains the **source-scoped operational procedure** behind `羅經以定真確時候`, rather than merely demonstrating that later compass+sundial+clock systems existed.

Machine evidence: `docs/research/ZIWEI-GAOHOU-MENGQIU-OPERATIONAL-BRIDGE-R1.json`.
