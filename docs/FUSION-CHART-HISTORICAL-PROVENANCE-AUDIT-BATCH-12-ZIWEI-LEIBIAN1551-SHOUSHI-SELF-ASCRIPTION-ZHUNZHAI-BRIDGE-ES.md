# Fusion Chart Historical Provenance Audit R1 — Batch 12ES

## 嘉靖三十年（1551）《類編曆法通書大全》“依授時曆抄白”实物自署与《準齋》首箭桥接

Status: **1551 PHYSICAL P20 DIRECTLY READS 四時加減晝夜節氣 / 依授時曆抄白 / FIRST STATE 冬至節日連小寒後四日同=38/62 / EXACT MATCH TO 1823 ZHUNZHAI FIRST ARROW / DIRECT PRE-1578 SHOUSHI-ASCRIBED TABLE BRIDGE CLOSED / FULL 25-ARROW REPLAY OPEN / EXACT PRE-1578 ZHUNZHAI PROSE NOT CLOSED / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

12ER used two layers: Wang Xiaohu's modern specialist argument and Tianwen's independent replay of the first Zhunzhai arrow against the 1551 Leibian table. That was enough to strongly corroborate a Yuan/Shoushi substrate, but the project had not yet promoted the 1551 table's own tiny source-ascription glyphs to a source-bound physical claim.

12ES reopens the already hash-bound 360-dpi p20 image from Batch 12DH and reads that annotation directly.

## 2. Source binding

The controlling object is unchanged:

- NLC set: `411999026677`
- public file: `NLC892-411999026677-72517 類編曆法通書大全 第1冊`
- catalog binding: 嘉靖三十年（1551）刻本遞修本
- source SHA-256: `22811dd2b2291ed4a94a63b51665c24785a4c1795637a4a89b05f979208d76f2`
- high-resolution run: `35359354362`
- artifact: `10554051966`
- artifact digest: `sha256:3c13f48b0df8b82989e765bfa8bd32f0bcf3e489838985ac75d6d7fb6cc47fb4`
- p20 SHA-256: `ac71e579493ff892476c1534aabd3b53cb26d64f185d6bb12a837476ba3f6fa9`

OCR is not final glyph authority.

## 3. Direct physical reading

At p20 the heading and adjacent narrow annotation are directly readable as:

    四時加減晝夜節氣
    依授時曆抄白

The first state on the same physical page is:

    冬至節日連小寒後四日同
    晝三十八刻
    夜六十二刻

Thus a securely pre-1578 physical Tongshu table explicitly presents this fine day/night-ke material as copied/extracted according to the Shoushi calendar tradition.

## 4. Exact first-state cross-witness bridge

The 1823 source-bound Zhunzhai first arrow directly gives:

    自冬至用至小寒後四日
    晝三十八刻
    夜六十二刻

The 1551 Shoushi-ascribed table gives:

    冬至節日連小寒後四日同
    晝三十八刻
    夜六十二刻

So the **date span and numerical state both match exactly**.

12ER's phrase “Shoushi-like fine-table substrate” can now be strengthened to:

    DIRECT_PRE1578_SHOUSHI_ASCRIPTION
      +
    EXACT_FIRST_STATE_MATCH

This is a source-bound mechanical bridge, not merely a secondary-literature inference.

## 5. What the annotation does and does not prove

The direct glyphs close:

    1551 TABLE SELF-ASCRIPTION = 依授時曆抄白
    PRE1578_SHOUSHI-ASCRIBED_FINE_TABLE = YES

They do not by themselves close:

    HISTORICAL_ACCURACY_OF_EVERY_COPIED_ROW = NOT INDEPENDENTLY PROVED
    UNCHANGED YUAN ROWSET = NOT PROVED
    DIRECT COPY DIRECTION TO/FROM ZHUNZHAI = NOT PROVED
    FULL 25-ARROW SEQUENCE REPLAY = OPEN
    EXACT PRE1578 ZHUNZHAI OPERATING PROSE = NOT CLOSED

The 1551 table is therefore evidence for the stated source tradition and for a precise first-state bridge, not a substitute for a pre-1578 Zhunzhai manuscript.

## 6. Sanming firewall

No exact Sanming/Yueling parent fingerprint is created:

- 1551 Dahan/Yushui rows still differ from the 1578/1589 target.
- Nanjing 59 endpoint is not supplied by this table.
- direct Sanming-parent vote increment = 0.

## 7. Product consequence

    MATRIX_ROWS=198
    AUDITED_ROWS=166
    MISSING_FROM_PRODUCT=10
    PROVENANCE_DEFECTS=12/12_REPAIRED
    CONFIRMED_CHART_ALGORITHM_DEFECTS=0
    ALGORITHM_REOPEN=0
    CANDIDATE_COLLAPSE=0
    DETERMINISTIC_PRODUCT=CLOSED

No runtime or candidate behavior changes.

## 8. Next gate

1. Directly replay the remaining Zhunzhai arrows against source-bound 1551 physical table rows wherever the images support unambiguous collation.
2. Continue searching for a securely pre-1578 witness of the exact Zhunzhai 25-arrow / winter-forward / summer-reverse / 日曆節候 prose.
3. Continue the primary author/title link search for Yuan Yanling Sun Fengji.
4. Continue the independent pre-1578 exact Sanming/Yueling Dahan/Rainwater fingerprint search.

Research record: `docs/research/ZIWEI-LEIBIAN1551-SHOUSHI-SELF-ASCRIPTION-ZHUNZHAI-BRIDGE-R1.json`.
