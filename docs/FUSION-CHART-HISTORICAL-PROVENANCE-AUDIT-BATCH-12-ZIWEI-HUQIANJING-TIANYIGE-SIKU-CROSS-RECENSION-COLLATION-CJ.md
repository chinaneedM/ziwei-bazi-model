# Fusion Chart Historical Provenance Audit R1 — Batch 12CJ

## 《虎鈐經·傳箭》天一閣明刻本 × 四庫系受傳本跨版本機械校勘

Status: **TWO INDEPENDENT PHYSICAL WITNESSES DIRECTLY COLLATED / CORE CHUANJIAN OPERATIONAL SEQUENCE CROSS-RECENSION STABLE / ARROWS NUMBERED 1 THROUGH 20 AND REUSED AFTER SOLSTITIAL RESET / PRIOR 48-ARROW SHORTHAND REJECTED / 40↔60 ONE-KE LADDER STRENGTHENED AS A STABLE TRANSMISSION LAYER / DIRECT COPY DIRECTION AND HAN-XIANFU PARENTAGE NOT PROVED / SANMING STRUCTURAL ANCESTRY CANDIDATE STRENGTHENED BUT EXACT TABLE IDENTITY REJECTED / HPA-ZDATE-006 UNCHANGED / NO ALGORITHM REOPEN**

## 1. Why this batch follows 12CI

Batch 12CI closed a recorded 1010 Han Xianfu precision 24-qi table and a 24/24 mechanical bridge to the later coarse integer family. Its next gate called for an independent audit of the near-contemporary `《虎鈐經·傳箭》` operational lineage. During that follow-up the earlier shorthand `48-arrow system` proved inaccurate and therefore requires an explicit forward-only research correction.

## 2. New independent physical witness

`CADAL06049792《虎鈐經·卷七~卷十一》` was rendered page-by-page without OCR.

```text
RUN=34933201296
JOB=104265544592
ARTIFACT=10382093979
ARTIFACT_DIGEST=sha256:7e5eeffd870581275a9e4968bb5061ae864142ad1e3dcdaac80068702c611eac
SOURCE_DJVU_SHA256=287547b1867829d35a6c788f20e73714b1fbce80e4c81717b0fb2eaa6a3e2707
DERIVED_PDF_SHA256=e6e191136e71a4bb2d2e6f1fc220830a5863c8c89c12ddf09b4aa6d8ffcb381d
PAGES=152
TARGET=P14-P23 / 卷七 傳箭第七十六
OCR_USED_FOR_GLYPH_CLAIMS=false
```

Date firewall:

```text
《虎鈐經》宋代作品脈絡 != 當前四庫系物理副本年代
四庫系受傳本 != 宋代原本
CADAL modern surrogate != historical physical copy date
```

## 3. Direct mechanical readings

The CADAL/Siku-recension witness directly preserves:

```text
傳箭第七十六
每時有八刻二十分
一刻六十分
一日十二時合一百刻
冬至前三日改第一箭 ... 晝四十刻 / 夜六十刻
...
小寒初日改第三箭 ... 42/58
...
雨水初日改第八箭 ... 47/53
...
第二十箭 ... 59/41
夏至前三日改第一箭 ... 60/40
```

After the summer-solstice reset, the text again advances from `第一箭` while daylight decreases one ke at a time toward winter.

Therefore the mechanically safe description is:

```text
ARROW_NUMBER_DOMAIN=1..20
SOLSTITIAL_RESET=summer solstice -> 第一箭
ANNUAL_MODEL=two opposite half-year sequences reusing arrow numbers 1..20
```

It is **not** a 48-arrow numbering system.

## 4. Cross-recension control with the Tianyige Ming print

Batch 12CD had already physically reviewed the Tianyige Ming-print witness. Re-collation against pp74–78 confirms the same core operational architecture:

- the same hundred-ke day and sixty-fen-per-ke framework;
- winter first arrow `40/60`;
- one-ke stepwise seasonal changes;
- numbered-arrow progression;
- `夏至前三日改第一箭` at `60/40`;
- the descending return sequence after summer.

This closes **core mechanical stability across two distinct received physical witnesses**. It does not authorize a character-for-character identity claim for every locus, and it does not identify one surviving physical copy as the direct parent of the other.

## 5. Research-text correction

Batch 12CI used the shorthand:

```text
integer 48-arrow system
```

Direct cross-recension physical evidence rejects that wording. The corrected description is:

```text
20-number arrow cycle, reused across opposite half-year directions
```

Classification:

```text
RESEARCH_TEXT_CORRECTION=true
PROVENANCE_METADATA_DEFECT_INCREMENT=0
CHART_ALGORITHM_DEFECT_INCREMENT=0
```

## 6. Relationship to Han Xianfu and Sanming

The evidence now separates three mechanical forms more cleanly:

```text
1010 Han Xianfu precision 24-qi table
    = fine values with residuals

Huqianjing Chuanjian operational ladder
    = intra-term arrow changes + integer one-ke steps + 40/60 <-> 60/40

1578 Sanming display
    = shares many one-ke pairs but has different anchoring and Xiazhi 59/41
```

Near chronology and shared technical vocabulary are insufficient to prove `Han Xianfu -> Huqianjing` copying. Likewise the stable Huqian ladder is a materially strengthened **structural ancestry candidate** for Sanming, not an exact table parent: Huqian reaches `夏至 60/40`; Sanming prints `夏至 59/41`.

## 7. Tianwen transmission impact

The graph now adds/strengthens:

```text
Tianyige Ming physical witness ─┐
                               ├─ ATTESTS -> Huqianjing 20-number-arrow 40↔60 rule family
CADAL/Siku physical witness ───┘

Huqianjing rule family
    -> STRUCTURAL_ANCESTRY_CANDIDATE_FOR -> Sanming 1578
```

The two surviving witnesses receive only a `SHARED_COMMON_ANCESTOR_CANDIDATE` relation; direct-copy direction remains unresolved.

## 8. Product adjudication

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
UPPER_ZI_TO_HAI_VOTE_INCREMENT=0
NEW_RUNTIME_CANDIDATE=false
RUNTIME_WINNER=false
CANDIDATE_COLLAPSE=false
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 9. Next gate

1. search specifically for a pre-1578 intermediary that combines a Huqian-style intra-term step ladder with the Nanjing/Datong `59`-ke cap or Sanming-like change-day fingerprint;
2. search for an explicit historical selection/rounding instruction capable of explaining the Batch 12CI `(78,81]/147` precision-to-coarse threshold;
3. continue the independent Fullbook upper-five-ke -> previous-night Hai lineage without conflating it with seasonal-table ancestry.

Research record: `docs/research/ZIWEI-HUQIANJING-TIANYIGE-SIKU-CROSS-RECENSION-COLLATION-R1.json`.
