# Batch 12DA — 1589《月令通攷》與 1578《三命通會》換檔指紋同源性物理校勘

## Status

```text
YUELING_1589_SOURCE_BOUND_PHYSICAL_OBJECT=979_PAGES_CLOSED
YUELING_VOLUME14_DECEMBER_LOCATOR=DIRECT_PHYSICAL
YUELING_YUSHUI_47_53_POST4_48_52=DIRECT_PHYSICAL
YUELING_DAHAN_43_57_LITERAL_SHISAN_HOU_44_56=DIRECT_PHYSICAL
SANMING_1578_FINGERPRINT_HOMOLOGY=HIGH_INFORMATION_MATCH
YUELING_AS_ANCESTOR_OF_SANMING=CHRONOLOGICALLY_IMPOSSIBLE
SANMING_TO_YUELING_DIRECT_COPY=UNPROVED
COMMON_PRE1578_TONGSHU_SOURCE=UNRESOLVED
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
```

## 1. Why this follows 12CZ

Batch 12CZ physically closed the existence of a historical fine-argument → threshold → integer-arrow discretization architecture, but the exact Nanjing/Sanming threshold remained unidentified.

A separate search then surfaced a different kind of evidence: Lu Han's `《月令通攷》`, in a securely post-Sanming 1589 edition, appears in public transcription to preserve not merely the same summer cap, but the two most distinctive internal Sanming transition fingerprints.

Because a post-1578 witness cannot be promoted into a 1578 ancestor, the correct question is not “is Yueling the source?” but:

> Does the 1589 physical edition really preserve the same rare change-day fingerprint, and if so what does that tell us about transmission persistence and the still-missing earlier source?

## 2. Exact physical acquisition

```text
SOURCE=NCL-03165 月令通攷
COMPILER=盧翰
EDITION=明萬曆十七年（1589）王道增臨海刊本
RUN=35335857137
ARTIFACT=10542996657
ARTIFACT_DIGEST=sha256:2efb115d5359d93860cbf3914c416243ad5b5aee1f654f463802b2bcae48d801
SOURCE_PDF_SHA256=bc95f32afb2bfe52b69ea4fb249481f6deee49d33b7b51f37f39ae9b383516a4
PAGES=979
ARTIFACT_FILES=1011
OCR_USED_FOR_FINAL_GLYPH_CLAIMS=false
```

The PDF text layer returned zero hits for the target terms. That is a failed locator only and has no negative textual authority. The complete 979-page object was rendered and target pages were located visually.

## 3. Volume 14 / December physical locator

PDF p797 directly shows:

```text
月令通攷
卷十四
十二月
```

Artifact page hash:

```text
p797=28e7b05c0cee838f632983474849bd5413790b89c59572a4cb6090b614362884
```

This binds the December/Dahan passage to the physical volume rather than a web transcription.

## 4. Rain Water fingerprint: physical p27

Artifact page hash:

```text
p27=3a732796e9a7a2a074bd9a5488ed554781a5726a4d92a2ea0234b875e5667c5c
```

Direct visual reading includes:

```text
雨水日日在危九度
...
晝四十七刻夜五十三刻
後四日
...
晝四十八刻夜五十二刻
```

Mechanically:

```text
雨水 47/53 -> 後四日 -> 48/52
```

This is the same high-information transition already closed on the exact 1578 Sanming physical target.

## 5. Great Cold fingerprint: physical p802

Artifact page hash:

```text
p802=5b451701c299daa05f737250a351f4cfb1dd3bbac92fff89a581573181df8544
```

The physical page directly prints the Dahan sequence:

```text
晝四十三刻夜五十七刻
十三後晝四十四刻夜五十六刻
```

The critical philological point is that `十三後` is physically present in the 1589 witness. It is not reconstructed from Sanming and is not silently normalized into Huqian's `後三日`.

Thus the second high-information fingerprint also matches the exact 1578 Sanming physical target.

## 6. Why this matters more than another 59/41 match

A shared endpoint such as `59/41` can arise from regional calibration and does not prove common table identity.

The present evidence is different:

```text
fingerprint A:
  雨水 47/53 -> 後四日 -> 48/52

fingerprint B:
  大寒 43/57 -> literal 十三後 -> 44/56
```

Two internal transition signatures surviving in a different late-Ming work are much stronger evidence that this was a transmissible table/textual layer, not an isolated error in one Sanming copy.

## 7. Chronology firewall

The exact controlled dates are:

```text
Sanming physical witness = 1578
Yueling controlled edition = 1589
gap = +11 years
```

Therefore:

```text
1589 Yueling -> 1578 Sanming direct ancestry = impossible
```

But chronology alone does **not** prove the reverse:

```text
1578 Sanming -> 1589 Yueling direct copying = not proved
```

Nor does it yet prove a common pre-1578 source.

The safe current alternatives are:

1. Yueling inherited the table after 1578 through a route that may or may not include Sanming;
2. both works inherited an earlier Tongshu/calendar source;
3. an unidentified intermediary recension supplied both.

## 8. Source-family signal, kept below ancestry threshold

Yueling Tongkao is a broad monthly/calendrical compilation and elsewhere explicitly labels some monthly material as `通書`. This makes a shared Tongshu/almanac substrate plausible.

However the target Dahan/Yushui physical loci have not yet been directly tied to a named source label in the surviving edition. Therefore this batch does **not** create a confirmed common-source edge.

The next search should move **upstream from both works**, not assume one copied the other.

## 9. Transmission graph impact

New nodes:

- `PHYSICAL-COPY-YUELING-TONGKAO-NCL03165-1589`
- `TABLE-YUELING-1589-DAYNIGHT-FINGERPRINT`

New confirmed edge:

```text
1589 physical copy
  ATTESTS
1589 Yueling day/night fingerprint table
```

The relation to the Sanming table is recorded as a postdated homolog in the research/hypothesis layer with explicit directionality firewalls, not as a parent-child graph edge.

## 10. Product adjudication

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

No runtime rule changes.

## 11. Next gate

Priority becomes:

1. search pre-1578 Chinese `通書 / 月令 / 曆法` witnesses for **both** `大寒 十三後` and `雨水 後四日` fingerprints;
2. determine whether the Yueling target passages themselves are source-labelled `通書` or attributed elsewhere in the same physical recension;
3. continue the independent Chinese C-II-N physical-carrier and Nanjing threshold/reduction-rule search.

Research record: `docs/research/ZIWEI-YUELING-TONGKAO-1589-SANMING-FINGERPRINT-HOMOLOG-COLLATION-R1.json`.
