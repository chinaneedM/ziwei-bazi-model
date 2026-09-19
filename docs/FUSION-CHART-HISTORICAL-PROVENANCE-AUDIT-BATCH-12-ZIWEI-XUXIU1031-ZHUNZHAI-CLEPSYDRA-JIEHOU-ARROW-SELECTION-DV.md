# Fusion Chart Historical Provenance Audit R1 — Batch 12DV

## 《準齋心製几漏圖式》：節候參照 → 二十五箭離散選擇機制物理閉合

Status: **RECEIVED CALENDAR/SOLAR-TERM → DISCRETE ARROW-SELECTION MECHANISM DIRECTLY CLOSED IN QING PHYSICAL RECENSION / SONG WORK ATTRIBUTION KEPT SEPARATE FROM QING COPY DATE / 25-ARROW 38↔62 NUMERIC FAMILY DIRECTLY MISMATCHES 1578 SANMING 59↔41 / 《銅壺漏箭制度》 PARALLEL 60↔40 CONTROL DIRECTLY OBSERVED / PRE-1578 PHYSICAL WITNESS NOT PROVED / EXACT 大寒十三後・雨水後四日 FINGERPRINT UNRESOLVED / ZERO DIRECT SANMING-PARENT VOTE / NO RUNTIME CHANGE / NO ALGORITHM REOPEN**

## 1. Why this batch

12CX–12DQ established a missing historical layer between fine calendar day-length quantities and the whole-ke display used by the 1578 Sanming table:

```text
fine calendrical/astronomical quantity
        ↓
historical discretization / arrow-state selection
        ↓
whole-ke day/night display
```

12CZ proved one explicit threshold-driven arrow-change family; 12DQ proved that a single global fractional threshold cannot reproduce the complete C-II-N interior plus Nanjing 59 endpoint. The remaining question is whether a historical operating text directly says to select discrete arrows by the calendar/solar-term state itself.

Batch 12DV answers that narrower mechanism question positively in a received physical recension, while preserving the chronology firewall.

## 2. Source-bound acquisition and locator correction

Public source:

```text
《續修四庫全書》第1031冊
SOURCE_PDF_SHA256=07348e40ec26ca38efe9c9736a69c403c61f9b07a2c89a847fc68d00ce6d8c25
```

The initial p625–p740 assumption was rejected after direct contact-sheet review because that range remained inside another work. A full-volume structural scan then localized the targets to p70–p89, and the final 220-dpi pass rendered p68–p90.

```text
FULL_VOLUME_LOCATOR_RUN=35437953746
FULL_VOLUME_LOCATOR_ARTIFACT=10583026334
FINAL_HIGHRES_RUN=35438178430
FINAL_HIGHRES_JOB=105884323863
FINAL_HIGHRES_ARTIFACT=10583226243
FINAL_HIGHRES_ARTIFACT_DIGEST=sha256:771155d081d669f1d1020213e2edc17d56d81594e625c267ce68b4f191cac6ce
OCR_USED_FOR_FINAL_GLYPH_OR_MECHANISM_CLAIMS=false
```

## 3. Chronology firewall

Xuxiu metadata identifies:

- 《準齋心製几漏圖式一卷》 as a work attributed to Song Sun Fengji, reproduced from an NLC-held Qing Daoguang-3 Huang-family Shiliju manuscript;
- 《銅壺漏箭制度一卷》 as reproduced from an NLC-held Qing Daoguang-3 Huang-family Shiliju manuscript.

Therefore:

```text
Song work attribution
    !=
date of reviewed physical manuscript

reviewed physical manuscript = Qing Daoguang 3 / 1823
secure pre-1578 physical witness = NOT_PROVED
```

Huang Pilie's received paratext describing an older source copy as likely ying-Song is retained only as Qing bibliographic/transmission control. It does not move the reviewed physical object backward in time.

## 4. Direct physical readings

### PDF p70

SHA-256:

```text
5c08716faa8a83e37c6ab71ff76b194b6165c64d1f944b0b3fb7ea7af84c75b1
```

Direct title:

```text
準齋心製几漏圖式
```

### PDF p71 — decisive operating rule

SHA-256:

```text
19b74ff13076bc80d0518e6c843a7fe95a85c4d97d63ab2d051aacf4167168f2
```

Directly visible phrases include:

```text
凡晝夜百刻節序短長
分界定數二十有五箭
如冬至後自第一箭順數用之
夏至後自二十五箭逆數用之
却依日曆參照節候
```

This is a direct operational rule of the form:

```text
calendar / solar-term state
        ↓
select one of a finite arrow sequence
        ↓
discrete day/night-ke operating state
```

### PDF p72 — first arrow

SHA-256:

```text
39f1e8d6605fc6926a67299a085edd8700d6b3c3cd98061033853f8bb2b42014
```

Directly:

```text
第一箭
自冬至用至小寒後四日
晝三十八刻
夜六十二刻
```

### PDF p76 — twenty-fifth arrow

SHA-256:

```text
64aad110e3cba4984cb784e9f97c99044fbc25e39a06744000a7a606ba73ffeb
```

Directly:

```text
第二十五箭
自夏至日用至小暑後六日
晝六十二刻
夜三十八刻
```

Thus the directly reviewed received family is 25-arrow / 38↔62, not the Sanming 59↔41 endpoint family.

### PDF p78 / p86 — companion 《銅壺漏箭制度》

p78 SHA-256:

```text
43f91f0d11eb88a014bb1a5fe53bc5ec696df540cfc2318cc9e80ba04e4c1329
```

directly opens:

```text
銅壺漏箭制度
```

p86 SHA-256:

```text
9ffe81b435665c81cc18536fe1efb443f3aa32ddf3082eff820c70942e0a3714
```

A directly visible seasonal table prints:

```text
晝六十刻
夜四十刻
```

This is retained as a parallel received numerical control only. It is not silently merged with the 《準齋》 25-arrow sequence.

p90 already begins 《天文精義賦》, closing the target block.

## 5. What this changes

The historical mechanism architecture is stronger:

```text
12CZ:
astronomical threshold → 改箭

12DV:
日曆 / 節候 reference → finite arrow-state selection
```

So discrete arrow-state choice need not be modeled merely as modern rounding. Historical technical texts can explicitly use calendar/season state to choose an operational arrow.

But the exact Sanming parent is still not closed.

## 6. What this disproves

An unchanged direct-table shortcut from this received 《準齋》 family to the 1578 Sanming table is mechanically false:

```text
準齋 first/solstitial extrema: 38/62 → 62/38
Sanming target summer endpoint: 59/41
```

The companion 《銅壺漏箭制度》 also exposes 60/40 rather than 59/41 at the reviewed seasonal locus.

Therefore this batch contributes:

```text
mechanism-class evidence = YES
exact Sanming numeric parent vote = 0
exact Nanjing 59 endpoint binding = NO
exact 大寒十三後 / 雨水後四日 fingerprint = NO
```

## 7. Transmission consequence

New graph objects:

```text
PHYSICAL-COPY-NLC-ZHUNZHAI-JILOU-DAOGUANG3-HUANG-SHILIJU-MS
RULE-FAMILY-ZHUNZHAI-25ARROW-JIEHOU-SELECTION-38-62
```

New supported edges:

```text
TG-E0072  physical Qing manuscript -> ATTESTS -> received 25-arrow rule family
TG-E0073  received 25-arrow rule family -> STRUCTURAL_MECHANISM_CANDIDATE_FOR -> 1578 Sanming table
```

The second edge is explicitly structural/mechanistic only. A direct unchanged table identity is recorded as disproved.

## 8. Product firewall

No deterministic chart behavior changes.

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
MISSING_FROM_PRODUCT=10
PROVENANCE_DEFECTS=12/12_REPAIRED
CONFIRMED_CHART_ALGORITHM_DEFECTS=0
ALGORITHM_REOPEN=0
CANDIDATE_COLLAPSE=0
DETERMINISTIC_PRODUCT=CLOSED
```

## 9. Next gate

The search is now narrower:

> Find a securely pre-1578 carrier that explicitly combines calendar/solar-term-driven discrete arrow selection with the Ming Nanjing/Datong 59-ke endpoint, and ideally reproduces the exact `大寒十三後 / 雨水後四日` transition fingerprint.

The received Qing copy of a Song-attributed mechanism is not allowed to satisfy that chronology gate by itself.
