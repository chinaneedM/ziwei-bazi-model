# Batch 12DB — 《神道大編曆宗通議》卷十一趙緣督百刻文字與地域校準橋梁物理校勘

## Status

```text
SHENDAO_FASC4_SOURCE_BOUND_PHYSICAL_OBJECT=166_PAGES
VOLUME_11_START_P115=DIRECT_PHYSICAL
ZHAO_YUANDU_ATTRIBUTION=DIRECT_PHYSICAL
HUNDRED_KE_HALF_ZI_TEXT_P145_P146=DIRECT_PHYSICAL
REGIONAL_DAYNIGHT_CALIBRATION_P154_P155=DIRECT_PHYSICAL
SHENDAO_TO_SANMING_DIRECT_COPY=UNPROVED
CURRENT_MANUSCRIPT_PRE1578_DATE=UNRESOLVED
EXACT_SANMING_59_41_PARENT=UNRESOLVED
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
```

## 1. Why this batch matters

Batch 12CD had already separated two Sanming timekeeping components:

- a Zhao Youqin / Gexiang-like hundred-ke and half-Zi prose lineage;
- an older 40↔60 integer seasonal ladder.

Batch 12DA then found the exact Sanming change-day fingerprint still alive in a different 1589 work, but that witness postdates Sanming and therefore cannot be promoted to an ancestor.

The present batch asks a different question:

> Is there a Ming scholarly layer that explicitly identifies the Zhao Yuandu tradition and preserves wording closer to the 1578 Sanming timekeeping prose, while also explaining why day/night extrema vary by locality?

The answer is yes, but with strict chronology limits.

## 2. Source-bound acquisition

The controlled object is the fourth fascicle of Zhou Shuxue's `《神道大編曆宗通議》十八卷`, held by the Fung Ping Shan Library / HKU rare-book collection and available through its public scan route.

Library metadata identifies the work as a **manuscript (鈔本)** by Ming author Zhou Shuxue. Public surrogate metadata assigns the broad range `明嘉靖萬曆間 [1522-1619]`. That range straddles 1578 and therefore does **not** authorize a pre-1578 date for the current physical copy.

Evidence chain:

```text
LOCATOR_RUN=35339641540
LOCATOR_ARTIFACT=10543984573
LOCATOR_DIGEST=sha256:a777240874eb605f03b45dcb2e09ae8561ef12b46b17b7ad90ae24d88dcaff87

HIGHRES_RUN=35340809937
HIGHRES_ARTIFACT=10544578416
HIGHRES_DIGEST=sha256:dffbdf976f5a252f313d694592fdb31657568ad4efca34e734cae1b44a4048ce

FASCICLE4_PDF_SHA256=a186efb679325d5e26ff240550b475a951dd1e3bc5cb2ce8ee32fc00ddedb4da
PAGES=166
OCR_USED_FOR_FINAL_GLYPH_CLAIMS=false
```

## 3. p115 — direct Zhao Yuandu attribution

High-resolution p115:

```text
SHA256=69b725a1d073db1194511bdaef70b2ad70f469c36bd854f70b43ce0dfd115e0d
```

The physical page directly shows:

```text
神道大編曆宗通議卷十一
趙緣督
革象論
凡十八   [small note/layout]
```

A public transcription linearizes the layout as `趙緣督十八篇論 / 革象論`. This batch does **not** replace the physical layout with that normalization.

What is physically secure is:

- Zhao Yuandu is directly named at the head of the group;
- `革象論` opens the group;
- a small `凡十八` note is present.

This is materially stronger than merely observing similar prose elsewhere: the Ming manuscript itself explicitly preserves the Zhao-attribution layer.

## 4. pp145–146 — hundred-ke / half-Zi prose

### p145

```text
SHA256=a51d683fa491e3fb60c266eb98672648b32c559fef74a324c432bef0e6e53baa
```

Direct readings include:

```text
晝夜十二時均分百刻
一時有八大刻二小刻
大刻總九十六
小刻總二十四
小刻六準大刻一
故此為百刻也
```

The page then lays out the upper-half and lower-half ke names.

A useful philological control: the physical p145 leaves a blank/omitted heading locus before this paragraph. Modern/received transcription labels the section `論晝夜百刻`, but this batch does not call that title a direct p145 glyph.

### p146

```text
SHA256=1daa63ecc87585bb85f6e7e0f740d86ab4fc3634e916e28448cfd90e4a678451
```

The decisive direct wording is:

```text
若子時則上半時在夜半前屬昨日
下半時在夜半後屬今日
```

The same page continues:

```text
古曆每時以二小刻為始乃各繼以四大刻
然不若今曆之便於算策也
世謂子午卯酉各九刻餘皆八刻者非是
```

and then Zhou's own `愚謂` comment proposes clearer ke names.

## 5. Three-stage textual comparison

### Received Gexiang witness — Batch 12CD

The reviewed received Zhao Youqin work preserves:

```text
晝夜十二時均分為百刻
一時有八大刻二小刻
子時之上一半在夜半前屬昨日
下一半在夜半後屬今日
```

### Shendao v11 — this batch

```text
晝夜十二時均分百刻
一時有八大刻二小刻
若子時則上半時在夜半前屬昨日
下半時在夜半後屬今日
```

### Sanming 1578 — Batch 12AT

```text
大晝夜十二時均分百刻一時有八大刻二小刻
若子時則上半時在夜半前為昨日
下半時在夜半後屬今日
```

The mechanical identity is extremely stable.

The phraseology is also informative:

- Shendao and Sanming both use the `若子時則上半時...` construction;
- the reviewed Gexiang recension uses `子時之上一半...`;
- Shendao has `屬昨日 / 屬今日`;
- exact 1578 Sanming has the recension asymmetry `為昨日 / 屬今日`.

This strengthens a **Zhao/Gexiang textual lineage with a Ming mediation/rephrasing layer**.

It still does not prove:

```text
current Shendao manuscript -> Sanming direct copying
```

because the current manuscript's date is only broadly assigned within 1522–1619 and no explicit Sanming citation/copy statement exists.

## 6. pp154–155 — locality calibration is explicit

p154:

```text
SHA256=e5495b22fe64390d59347dd431a0e2a1f31ea9a9415d1cd1dbc436c4f40bcb86
```

directly carries the heading:

```text
論地域遠近
```

and explicitly compares latitude/locality. The decisive sequence begins:

```text
舊曆晝永極於六十刻
晝短極於四十刻
今授時曆以驗於燕地稍偏北
故其永...
```

p155:

```text
SHA256=da70e15827df1c129c34b3c31f8756a1961bba0d7d025e02a08408956a77585a
```

continues:

```text
至六十二刻
短至三十八刻
蓋偏南則長短較少
偏北則所較漸多
```

Therefore a Ming Zhao-line received discourse directly and explicitly understands day/night extrema as geographically calibrated.

This matters to the Sanming composite model because locality adaptation is historically explicit, not a modern explanatory patch.

But the numbers also impose a firewall:

```text
old-calendar branch = 60/40
Yandu Shoushi branch = 62/38
Sanming 1578 = 59/41
```

So Shendao v11 is a **theory/prose bridge**, not the unchanged numeric parent of the Sanming table.

## 7. Transmission adjudication

What this batch strengthens:

```text
Zhao/Gexiang hundred-ke + half-Zi textual lineage
        ↓
Ming scholarly mediation / rephrasing visible in Shendao v11
        ↓
Sanming-like wording family
```

with the important caveat that the final arrow is a lineage candidate, not proven direct copying.

It also strengthens:

```text
historical locality awareness
  -> different day/night extrema by region
```

What remains unresolved:

- a physically pre-1578 Chinese witness of the closer Ming wording;
- the exact pre-1578 carrier of Sanming's 59/41 numerical layer;
- the exact C-II-N -> integer change-day threshold/selection rule;
- the common source behind the exact Sanming/Yueling `十三後 / 後四日` fingerprint.

## 8. Product adjudication

No deterministic chart rule changes:

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
HPA_ZDATE_006=MISSING_FROM_PRODUCT
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 9. Next gate

Highest-value next work is now split cleanly:

1. **textual stemma** — find a securely pre-1578 physical witness of the Zhao/Gexiang-derived `若子時則上半時...` Ming recension;
2. **numeric stemma** — independently continue the pre-1578 Nanjing/Datong 59-ke carrier and exact Sanming/Yueling change-day fingerprint search;
3. **mechanical bridge** — identify the historically attested threshold/selection rule that maps the C-II-N daily curve to the Sanming integer ladder.

Research record: `docs/research/ZIWEI-SHENDAO-ZHAOYUANDU-TIMEKEEPING-TEXTUAL-BRIDGE-R1.json`.
