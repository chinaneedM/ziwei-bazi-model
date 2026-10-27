# Fusion Chart Historical Provenance Audit R1 — Batch 12AN

## 《儒門崇理折衷堪輿完孝錄》：二十四山—二十四時—太陽到處的明代術數時間座標橋

Status: **MING SHUSHU TIME-SECTOR SEMANTIC BRIDGE CONFIRMED / SOURCE-EMITTED PHYSICAL PAGE LOCATOR BOUND / NO DIRECT TARGET GLYPH AUTHORITY / SOLAR-ASTRONOMICAL ANCHOR REQUIRED / FULLBOOK INCLEMENT-WEATHER TIME ACQUISITION STILL OPEN / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Research question

Batch 12AM established from direct facsimile that `臬測以景` and `針以氣` are mechanically distinct. That makes a magnetic needle an orientation device, not a standalone clock.

Batch 12AN asks the next narrower question:

> Can a Ming shushu source explain how a Luojing-like 24-direction plate nevertheless carries a time coordinate, without equating the magnetic needle itself with timekeeping?

The answer is yes.

## 2. Source family and edition-scoped control

The relevant witness is 《儒門崇理折衷堪輿完孝錄》, chapter `第四十二章論定時`.

CText exposes the chapter text and, through its own search result, directly emits the physical-page locator:

`https://ctext.org/library.pl?if=gb&file=100720&page=144`

The page number was not enumerated or guessed. The unauthenticated page HTML does not expose the scan-image object, so this route is a physical-page locator but not target glyph authority.

A second structured route is Shidian book object `NGJ892411999007380140073`, chapter `1lr8vrbiuyale`. Its source-emitted `window._ROUTER_DATA` identifies:

- book: `續道藏`
- image source/library: `國家圖書館`
- edition: `內府明萬曆35年刻本`
- dynasty: 明
- total pages: 11570
- target chapter source-emitted page span: 5577–5707

The same router data attaches the target transcription to explicit physical `PageId` transitions. Following the source-emitted page sequence gives target pages around 5607–5611; this mapping is deterministic from the source data, not hidden-ID guessing.

The Shidian target image bytes have not been directly obtained, therefore its text remains edition-scoped OCR/transcription evidence, not direct glyph collation.

## 3. Textual semantic result

The chapter explicitly coordinates time sectors with mountain sectors:

`時與山每每相應`

It then subdivides the normal twelve branch-hours by interstitial stem/trigram sectors, yielding a 24-position timing scheme. Examples include the sequence around 子:

- 亥正三刻至子初二刻 → 壬時
- 子初三刻至子正二刻 → 子時
- 子正三刻至丑初二刻 → 癸時

The text also requires:

`凡定時之法，必須逐時逐刻考驗`

and describes the operational anchor as:

`每日皆從太陽到處數，卯時起，一時到一山`

with solstitial adjustments, then states its purpose:

`此是查時刻以考星躔之要法`

Because the current Shidian/CText surfaces contain OCR/transcription variants, apparent readings such as `四十四山` are **not** silently corrected to `二十四山`; glyph-level normalization remains blocked until the physical target image is directly reviewed.

## 4. Mechanical adjudication

This source materially clarifies a point left open after Batch 12AM:

1. A 24-mountain directional ring can also function as a **24-sector temporal coordinate ring**.
2. The ring does not generate time by itself.
3. The source anchors the calculation to `太陽到處`, repeated temporal checking, and stellar/ephemeris reasoning.
4. Therefore `羅經` can plausibly participate in time determination as a directional/sector coordinate aid without being a magnetic standalone clock.

The following equalities remain rejected or unproved:

```text
羅經 != standalone clock
羅經 != automatically true solar time
羅經 != automatically local apparent solar runtime
24-mountain/time-sector coordinate != independent current-time acquisition
```

## 5. Relation to the Fullbook cloudy/rainy sentence

The Fullbook's source-scoped sentence says that in cloudy/rainy conditions one must use 羅經 to determine the exact time.

Batch 12AN narrows the semantics but does not close the missing operational chain:

```text
24-mountain/time-sector ring
+ orientation/reference
+ ??? current-time acquisition under cloud/rain ???
-> actual birth-time reading
```

The witness itself still depends on solar/astronomical reference. It does not say how cloud/rain supplies the absent current-time input.

Therefore Batch 12AN does **not** authorize:

- apparent-solar-time runtime selection;
- civil-time runtime selection;
- mean-solar-time runtime selection;
- magnetic-compass-as-clock interpretation;
- Fullbook authorial inheritance from this exact source;
- candidate selection or collapse;
- deterministic algorithm reopen.

## 6. Evidence firewall

CText and Shidian are not double-counted as two independent target-glyph witnesses. Neither route currently supplies a directly reviewed target scan image in this batch.

The Shidian structured page map is valuable because it binds the transcription to a specific edition and source-emitted physical PageIds, but it does not become glyph authority merely because the page IDs are known.

## 7. HPA-ZDATE-006 effect

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_TIME_STANDARD_BINDING=MING_SHUSHU_24_MOUNTAIN_TIME_SECTOR_MAPPING_CONFIRMED_SOLAR_ASTRONOMICAL_ANCHOR_REMAINS_REQUIRED_FULLBOOK_INCLEMENT_CHAIN_AND_RUNTIME_BINDING_STILL_OPEN
NEW_FULLBOOK_TEXTUAL_WITNESS=0
NEW_HAI_GLYPH_WITNESS=0
NEW_MING_SHUSHU_TIME_SECTOR_SEMANTIC_CONTROL=1
CANDIDATE_SELECTION=NO
CANDIDATE_COLLAPSE=0
ALGORITHM_REOPEN=NO
```

Accounting remains 198 rows / 166 audited / 10 current MISSING_FROM_PRODUCT / 14 cumulative missing candidate families / provenance defects 10 confirmed and 10 repaired / algorithm defect-reopen-collapse all zero.

## 8. Next gate

The next gate is now sharper:

> Find a Fullbook-line or sufficiently early Ziwei source that explicitly supplies the **inclement-weather current-time acquisition mechanism**. A 24-mountain/time-sector ring explains the coordinate framework, but it does not provide the missing clock input by itself.

Machine evidence: `docs/research/ZIWEI-WANXIAOLU-TIME-MOUNTAIN-BRIDGE-R1.json`.
