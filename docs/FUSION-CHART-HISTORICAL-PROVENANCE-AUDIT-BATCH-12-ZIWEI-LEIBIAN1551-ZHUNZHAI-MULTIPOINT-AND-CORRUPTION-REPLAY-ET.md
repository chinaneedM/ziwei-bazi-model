# Fusion Chart Historical Provenance Audit R1 — Batch 12ET

## 1551《類編》×1823《準齋》多點實物重放：三個精確錨點與兩處傳承訛讀控制

Status: **3 DISTRIBUTED EXACT DATE/VALUE ANCHORS CLOSED / 1551 P20 TWO SEQUENCE-BREAKING READINGS PHYSICALLY LOCALIZED / ZHUNZHAI ARROWS 8–9 SUPPLY CLEAN PARALLEL BOUNDARIES / SHARED SHOUSHI FINE-TABLE SOURCE FAMILY STRONGLY SUPPORTED / TG-E0097 SHARED_COMMON_ANCESTOR_CANDIDATE=PROBABLE / FULL 25-ARROW REPLAY OPEN / DIRECT COPY DIRECTION UNPROVED / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

12ES closed one exact bridge: the source-bound 1551 《類編曆法通書大全》 p20 explicitly says `依授時曆抄白`, and its first 38/62 state exactly matches the 1823 《準齋》 first arrow.

12ET asks whether that agreement survives away from the first row, and whether apparent disagreements can be separated into genuine rule differences versus transmission corruption.

## 2. Source bindings

The 1551 control is unchanged:

- NLC set `411999026677`
- p20 SHA-256 `ac71e579493ff892476c1534aabd3b53cb26d64f185d6bb12a837476ba3f6fa9`
- high-res run `35359354362`, artifact `10554051966`
- final glyph claims: direct image review, no OCR authority.

The 1823 Zhunzhai controls are from the already source-bound 12DV artifact `10583226243`:

- p72 SHA-256 `39f1e8d6605fc6926a67299a085edd8700d6b3c3cd98061033853f8bb2b42014`
- p73 SHA-256 `1984fab868257d433464ef4ef4bf219c876b8b4872d882e5e55ca949266eb526`
- p76 SHA-256 `64aad110e3cba4984cb784e9f97c99044fbc25e39a06744000a7a606ba73ffeb`

## 3. Three distributed exact anchors

### 38/62 — winter start

1551:

    冬至節日連小寒後四日同
    晝38 / 夜62

1823 Zhunzhai arrow 1:

    自冬至用至小寒後四日
    晝38 / 夜62

Result: exact date-range/value match.

### 45/55 — Rainwater spring range

1551:

    雨水節日至後五日同
    晝45 / 夜55

1823 Zhunzhai arrow 8:

    自雨水日用至雨水後五日
    晝45 / 夜55

Result: exact spring date-range/value match.

### 62/38 — summer terminal range

1551:

    夏至節日連小暑後六日同
    晝62 / 夜38

1823 Zhunzhai arrow 25:

    自夏至日用至小暑後六日
    晝62 / 夜38

Result: exact date-range/value match.

The match therefore spans the beginning, an interior Rainwater state, and the terminal summer state. It is no longer a single-anchor coincidence.

## 4. Two physical corruption controls in the 1551 table

### 45/55 autumn locus

1551 p20 physically prints:

    霜降前十日至後四日同

Zhunzhai arrow 8 directly prints:

    自霜降前一日用至霜降後四日

Wang Xiaohu 2014 independently emended the 1551 reading from `前十日` to `前一日` on sequence-continuity grounds.

The later independent physical Zhunzhai parallel supplies exactly that clean boundary. Tianwen therefore classifies the `十 -> 一` locus as:

    TRANSMISSION_ERROR_STRONGLY_SUPPORTED

This is not silently rewritten: the 1551 physical reading remains preserved as the observed witness.

### 46/54 spring locus

1551 p20 physically prints:

    雨水前八日至後十日同

Zhunzhai arrow 9 directly begins:

    自雨水後六日用至驚蟄前五日

Wang 2014 independently emended the 1551 starting phrase `雨水前八日` to `雨水後六日`.

The Zhunzhai physical parallel strongly supports that starting-boundary correction. The terminal phrase is expressed against the next solar term, so 12ET does **not** claim literal full-row identity without an explicit term-length/calendar normalization.

## 5. Transmission consequence

The evidence now supports:

    shared Shoushi fine-table source family = STRONGLY SUPPORTED

A new candidate edge is added:

    TG-E0097
    Zhunzhai 25-arrow family
      -- SHARED_COMMON_ANCESTOR_CANDIDATE -->
    Leibian 1551 Shoushi fine table

with:

    status      = PROBABLE
    confidence  = MEDIUM_HIGH

This deliberately does not state:

- Zhunzhai copied Leibian;
- Leibian copied Zhunzhai;
- the exact Yuan common exemplar has been identified;
- the whole 25-arrow sequence is closed.

## 6. Chronology firewall

Still open:

    exact pre-1578 Zhunzhai 25-arrow prose = NOT CLOSED
    secure pre-1578 physical Zhunzhai rule witness = NOT PROVED
    exact Yuan common exemplar = NOT IDENTIFIED
    full 25-arrow replay = OPEN

The result strengthens the Yuan/Shoushi substrate and transmission model, not the surviving-copy date.

## 7. Sanming firewall

The 1551 fine table remains numerically nonidentical to the Sanming/Yueling target at Dahan/Rainwater. It also does not supply the Nanjing 59-ke endpoint binding.

Therefore:

    direct Sanming-parent vote increment = 0
    algorithm reopen = 0
    candidate collapse = 0

## 8. Product consequence

    MATRIX_ROWS=198
    AUDITED_ROWS=166
    MISSING_FROM_PRODUCT=10
    PROVENANCE_DEFECTS=12/12_REPAIRED
    CONFIRMED_CHART_ALGORITHM_DEFECTS=0
    DETERMINISTIC_PRODUCT=CLOSED

## 9. Next gate

1. Continue only those additional 1551/Zhunzhai row replays whose physical glyphs are unambiguous.
2. Do not convert calendar-normalization-dependent equivalences into literal textual identity.
3. Seek a securely pre-1578 carrier of the exact Zhunzhai 25-arrow / winter-forward / summer-reverse / 日曆節候 prose.
4. Continue the Yuan Yanling Sun Fengji primary author/title link search.
5. Continue the independent exact Sanming/Yueling Dahan/Rainwater fingerprint and Nanjing-59 searches.

Research record: `docs/research/ZIWEI-LEIBIAN1551-ZHUNZHAI-MULTIPOINT-AND-CORRUPTION-REPLAY-R1.json`.
