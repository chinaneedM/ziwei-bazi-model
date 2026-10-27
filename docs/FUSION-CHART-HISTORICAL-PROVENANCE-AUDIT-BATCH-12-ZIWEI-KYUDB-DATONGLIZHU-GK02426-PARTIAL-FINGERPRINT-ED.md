# Fusion Chart Historical Provenance Audit R1 — Batch 12ED

## 奎章閣 GK02426_00《大統曆註》：朝鮮木活字異本的閾值架構、大寒十三日收斂與雨水分歧

Status: **DIRECT KYUDB PHYSICAL RECENSION / 冬至餘…已上為退 ARCHITECTURE CONFIRMED / DAHAN 後十三日 -> 44/56 DIRECTLY ATTESTED / RAINWATER 後六日 -> 47/53 DIRECTLY ATTESTED / PARTIAL SANMING HIGH-INFORMATION CONVERGENCE BUT EXACT TABLE IDENTITY DISPROVED / CURRENT FIRST-PARTY IMPRESSION YEAR UNRESOLVED / SECONDARY 1434 POSTFACE SIGNAL NOT PROMOTED TO CALENDAR-TEXT DATE / ZERO EXACT SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12EC established that NCL-06627《大統曆註》contains the same compound architecture sought by the reconstruction:

    term-specific 冬至餘…已上為退 state thresholds
    + day/night whole-ke schedule
    + later 59/41 endpoint

but its Rainwater and Dahan change-day loci diverged from the exact 1578 Sanming target.

The repository already contained an earlier catalog-level lead for a Korean《大統曆註》. Batch 12ED upgrades that lead to direct physical collation from Kyujanggak's current original-image service and asks whether the Korean recension preserves a different change-day state closer to Sanming.

## 2. Exact reviewed object

    PROVIDER=Kyujanggak Institute for Korean Studies, Seoul National University
    BOOK_CD=GK02426_00
    CALL_NUMBER=奎2426-v.1-4
    TITLE=大統曆註
    EDITION=觀象監木活字
    CATALOG_YEAR=[刊年未詳]
    EXTENT=12卷 4冊
    RUN=35513697961
    ARTIFACT=10606122789
    ARTIFACT_DIGEST=sha256:1bd3da37f801446ad3c60ef3eb1d058708d50b5f71aef39bc564255f26486db8
    OCR_USED_FOR_FINAL_CLAIMS=false
    PAGE_TEXT_NONEMPTY_COUNT=0

The empty pageText layer is not used as negative evidence. Final readings below are from source-bound physical images.

## 3. Volume 1: threshold architecture and Rainwater divergence

Direct physical page `0001/002a`:

    SHA256=b66c814cbb541565bd53103ec7e2db00926b4c0cc961f4244c43cfb21e237d07

Direct sequence:

    大統曆註卷第一
    立春正月節
    冬至餘三十四刻四十五分已上為退
    雨水正月中
    後六日 晝四十七刻 夜五十三刻

This independently confirms the same **term-state threshold + whole-ke schedule architecture** as NCL-06627.

But it is not the Sanming/Yueling Rainwater fingerprint. The 1578 target is:

    雨水 47/53
    後四日 48/52

whereas this reviewed Korean recension explicitly places 47/53 at **後六日**.

Therefore unchanged exact-table identity with Sanming is already excluded at Rainwater.

## 4. Volume 12: Dahan day-13 convergence

Direct volume-12 opening:

    0004/050b SHA256=16a756be8f87a70f1dd5d696dfcbff3c3ccaf42b33e5dd33e7e9116f15c111ad
    大統曆註卷第十二

Direct Dahan neighborhood:

    0004/051a SHA256=c903772c986b40b8ea9b5a61226cf62b9bf995294326bcbb0fb23b7bb60e009d
    大寒十二月中

The continuation on `0004/051b`:

    SHA256=16d138415c6792b17dce14cd1095f2d725f239c96bb35efcf95aad2ff1c4fda4

directly preserves:

    後十三日 晝四十四刻 夜五十六刻
    冬至餘五十六刻三十分已上為退

This is materially important because:

    NCL-06627 reviewed text state: 後十四日 -> 44/56
    Kyujanggak GK02426:          後十三日 -> 44/56
    Sanming/Yueling target:      day-13 / 十三後 timing -> 44/56

So the Korean recension **moves the Dahan 44/56 transition onto the target day-13 timing**.

This is a high-information partial convergence, not a complete exact fingerprint closure: the physical wording/order is not identical to the Sanming witness, the full preceding state sequence is not promoted as identical, and Rainwater still mismatches.

## 5. Direct recension difference from NCL-06627

The two reviewed《大統曆註》text states are not unchanged copies of one another.

At Lichun:

    Kyudb GK02426: 冬至餘三十四刻四十五分已上為退
    NCL-06627:     冬至餘三十四刻四十分已上為退

At the Dahan 44/56 transition:

    Kyudb GK02426: 後十三日
    NCL-06627:     後十四日

Thus:

    same work title
    + same threshold architecture
    + same whole-ke mechanism class

does not imply one invariant received numerical schedule.

The safe transmission model is **branching recensional transmission / shared common-ancestor candidate**, not direct unchanged copying.

## 6. Chronology firewall

The current first-party Kyujanggak catalog states:

    版式=觀象監木活字
    刊年=[刊年未詳]

The earlier project locator recorded a KOSTMA / Encyclopedia of Korean Culture lead saying that a Kim Bin postface written in 1434 is attached at the end of a 12-juan / 4-book《大統曆註》object. That same secondary description also states that the postface concerns type, not the Datong-calendar content.

Batch 12ED deliberately does **not** turn that into:

    calendar rule composed in 1434
    physical print securely dated 1434
    secure pre-1578 Sanming parent

The current Kyujanggak image sequence directly reaches:

    0004/074b
    SHA256=4b9b3965453bd0722ccd872c4a34f73db1d456ed46a6410c40254d6eac592734
    大統曆註卷第十二終

The attempted `075a-080b` route did not yield substantive physical pages, so the 1434 postface was not directly recovered in this workflow.

Therefore:

    SECURE_PRE1578_WITNESS=false
    EXACT_SANMING_PARENT_VOTE_INCREMENT=0

## 7. Transmission consequence

New nodes:

    PHYSICAL-COPY-KYUDB-DATONGLIZHU-GK02426-GWANSANGGAM-WOODTYPE
    RULE-FAMILY-KYUDB-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE

New confirmed edge:

    TG-E0093
      PHYSICAL-COPY-KYUDB-DATONGLIZHU-GK02426-GWANSANGGAM-WOODTYPE
      --ATTESTS-->
      RULE-FAMILY-KYUDB-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE

New recension-family edge:

    TG-E0094
      PHYSICAL-COPY-KYUDB-DATONGLIZHU-GK02426-GWANSANGGAM-WOODTYPE
      --SHARED_COMMON_ANCESTOR_CANDIDATE-->
      PHYSICAL-COPY-DATONGLIZHU-NCL06627-MING-MANUSCRIPT

Two unchanged-identity shortcuts are rejected:

    RULE-FAMILY-KYUDB-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE
      --DIRECT_UNCHANGED_TABLE_IDENTITY_WITH-->
      TABLE-SANMING-1578-DAYNIGHT-KE
      = DISPROVED

    RULE-FAMILY-KYUDB-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE
      --DIRECT_UNCHANGED_TABLE_IDENTITY_WITH-->
      RULE-FAMILY-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE
      = DISPROVED

The first is disproved by Rainwater timing. The second is disproved by the Lichun threshold and Dahan day-count differences.

## 8. Product firewall

    MATRIX_ROWS=198
    AUDITED_ROWS=166
    MISSING_FROM_PRODUCT=10
    PROVENANCE_DEFECTS=12/12_REPAIRED
    CONFIRMED_CHART_ALGORITHM_DEFECTS=0
    ALGORITHM_REOPEN=0
    CANDIDATE_COLLAPSE=0
    DETERMINISTIC_PRODUCT=CLOSED

This batch changes historical transmission knowledge only.

## 9. Next gate

The next highest-value gate is now narrower:

    securely date the GK02426 physical/text state
    OR
    find another secure pre-1578 Datonglizhu/Tongshu recension
        + Rainwater term-anchor 47/53 -> 後四日 48/52
        + Dahan day13 -> 44/56
        + an explicit operator connecting 冬至餘 state selection to whole-ke output

The Kyujanggak recension shows that **Dahan day13 can exist inside the same Datonglizhu threshold architecture even when Rainwater remains different**. That makes recensional recomposition—not a single invariant table—the more productive search model.

Research record: `docs/research/ZIWEI-KYUDB-DATONGLIZHU-GK02426-PARTIAL-FINGERPRINT-R1.json`
