# Fusion Chart Historical Provenance Audit R1 — Batch 12EC

## NCL-06627《大統曆註》：冬至餘閾值—整刻表共頁架構與《三命通會》變日指紋分歧

Status: **MING NCL-06627 PHYSICAL TEXT STATE DIRECTLY CO-LOCATES TERM-SPECIFIC 冬至餘…已上為退 THRESHOLDS WITH DAY/NIGHT WHOLE-KE SCHEDULE / SUMMER-SOLSTICE 59/41 DIRECTLY ATTESTED / DAHAN AND YUSHUI HIGH-INFORMATION CHANGE-DAY LOCI MISMATCH SANMING 1578 / UNCHANGED-TABLE IDENTITY DISPROVED FOR THIS TEXT STATE / EXACT COPY DATE UNRESOLVED / NOT SECURE PRE-1578 / ZERO EXACT SANMING-PARENT VOTE / NO RUNTIME CHANGE / NO ALGORITHM REOPEN**

## 1. Why this batch

Batch 12EB physically closed a later-Ming bridge between Datong endpoint coordinates and 59/41 whole-ke display, but the remaining gate still required:

    pre-1578 chronology
    + state-dependent selection/recomposition
    + preferably the Sanming/Yueling high-information change-day fingerprint

The next exact-HEAD probe therefore returned to NCL-06627《大統曆註》. The first artifact fixed the summer endpoint at p66; the follow-up exact-HEAD artifact added p179-p180 so the Dahan fingerprint could be adjudicated on the same remote evidence chain.

## 2. Exact remote evidence

    WORK=大統曆註
    AUTHOR=(明)不著撰人
    NCL=NCL-06627 / 索書號 6627
    RUN=35509501620
    ARTIFACT=10605095954
    ARTIFACT_DIGEST=sha256:2e38447cba4ead0885a0f6c0a84de965c7f01d17f0a7fb0f4b73fe1ed60baf83
    PDF_SHA256=a9bc6bd645f327afde884cb87dc35b48dfd9080bce96bf6f425fd4af205c22a2
    PDF_PAGES=195
    P1_SHA256=90b16f62961ddb57fe90e8f562b06f0738068cf77d373dd4ec2b40d89f490cd1
    P2_SHA256=1c0ab772ac469a26e2621953b20cd8a1d7b5da0268d2bfef6cad36ab49155cf0
    P66_SHA256=cfe70aef0b6cbdcc337e789ffe9d109eabffe3534744673b28d6b5547e6c24da
    P179_SHA256=2efc7a5fedb470656fc7376691508e248c30c760ec6fb520424fa47c0e070c61
    P180_SHA256=4e5547e6ab9b14bc87cc093f56d3de05d2593506972469894ea1df2e3c04f708
    OCR_USED_FOR_FINAL_GLYPH_NUMERIC_OR_LINEAGE_CLAIMS=false

Selected p1-p12 and p184-p195 front/back review did not yield a secure internal year, colophon date or copy note capable of placing this reviewed physical/textual state before 1578. “明” attribution is therefore not promoted into a pre-1578 physical date.

## 3. Direct term-threshold layer

Direct visual review closes on p1:

    立春 冬至餘三十四刻四十分已上為退
    雨水 冬至餘一十二刻六十分已上為退

On p66:

    芒種五月節
    冬至餘一十八刻一十五分已上為退

On p179:

    大寒十二月中
    大寒 冬至餘五十六刻三十分已上為退

The safe philological/mechanical reading is narrow: individual solar terms are accompanied by winter-solstice-remainder thresholds with an 已上為退 condition. This closes existence of a state-dependent term-threshold layer in the reviewed text state.

It does **not** prove that this threshold is itself the numerical operator generating the adjacent daylight/night whole-ke bins.

## 4. Direct whole-ke layer and summer endpoint

The same p66 physically preserves:

    夏至五月中
    初日 日出寅正四刻
    日入戌初初刻
    晝五十九刻 夜四十一刻

Thus the reviewed《大統曆註》text state puts a term-specific threshold regime and the 59/41 endpoint schedule inside the same monthly rule architecture.

This materially strengthens the architectural bridge sought after 12EB, but “same page / same rule system” is not equivalent to “threshold mathematically produces 59.”

## 5. Rainwater fingerprint: direct mismatch

The p1 Rainwater threshold continues onto p2, where direct review preserves:

    後六日 晝四十七刻 夜五十三刻
    後十四日 晝四十八刻 夜五十二刻

The controlling 1578《三命通會》physical target is:

    雨水 47/53
    後四日 48/52

Therefore the high-information Rainwater change-day fingerprint **does not match**.

This is stronger negative evidence than an endpoint mismatch because both traditions can share 59/41 while still exposing different internal bin-change timing.

## 6. Dahan fingerprint: direct mismatch

On p179 the reviewed text state preserves Dahan's 43/57 state. The following p180 explicitly states:

    後十四日 晝四十四刻 夜五十六刻

The controlling 1578《三命通會》physical sequence before 44/56 is literally:

    十三後日

The word order in the 1578 witness must remain unnormalized. Regardless of how a modern reader might paraphrase it, NCL-06627's explicit 後十四日 is not that physical fingerprint.

So the Dahan high-information locus also mismatches.

## 7. Historical adjudication

What is now closed for the reviewed NCL-06627 text state:

    term-specific 冬至餘…已上為退 threshold layer = DIRECT PHYSICAL
    adjacent day/night whole-ke schedule = DIRECT PHYSICAL
    summer-solstice 59/41 endpoint = DIRECT PHYSICAL
    Dahan 43/57 -> 後十四日 -> 44/56 = DIRECT PHYSICAL
    Rainwater-side 後六日 47/53 -> 後十四日 48/52 = DIRECT PHYSICAL

What is disproved:

    this reviewed NCL-06627 text state
        == unchanged Sanming 1578 seasonal table
        = DISPROVED BY TWO HIGH-INFORMATION CHANGE-DAY LOCI

What remains unresolved:

    exact date of this NCL-06627 manuscript/text state
    secure pre-1578 status
    exact operator connecting term-state thresholds to whole-ke bins
    exact pre-1578 source of Sanming's 十三後日 / 後四日 fingerprint
    direct copy ancestry into Sanming 1578

Therefore the source is retained as a strong structural/mechanical control and a strong divergent-recension control, not promoted as the Sanming parent.

## 8. Transmission consequence

New nodes:

    PHYSICAL-COPY-DATONGLIZHU-NCL06627-MING-MANUSCRIPT
    RULE-FAMILY-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE

New edges:

    TG-E0091
        PHYSICAL-COPY-DATONGLIZHU-NCL06627-MING-MANUSCRIPT
        --ATTESTS-->
        RULE-FAMILY-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE

    TG-E0092
        RULE-FAMILY-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE
        --STRUCTURAL_MECHANISM_CANDIDATE_FOR-->
        RULE-FAMILY-NANJING-CII-INTEGER-THRESHOLD-PLUS-59-ENDPOINT-ANCHOR

New explicit non-edge:

    RULE-FAMILY-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE
        --DIRECT_UNCHANGED_TABLE_IDENTITY_WITH-->
        TABLE-SANMING-1578-DAYNIGHT-KE
        = DISPROVED

The negative edge is text-state scoped. It does not prove that no earlier common ancestor existed; it proves that this reviewed NCL-06627 schedule is not the unchanged 1578 Sanming table.

## 9. Product firewall

    MATRIX_ROWS=198
    AUDITED_ROWS=166
    MISSING_FROM_PRODUCT=10
    PROVENANCE_DEFECTS=12/12_REPAIRED
    CONFIRMED_CHART_ALGORITHM_DEFECTS=0
    ALGORITHM_REOPEN=0
    CANDIDATE_COLLAPSE=0
    DETERMINISTIC_PRODUCT=CLOSED

No runtime candidate, winner, candidate collapse, or algorithm reopen is authorized.

## 10. Next gate

The next search should not reward another source merely for sharing 59/41.

Priority becomes:

    securely pre-1578 Datong / Tongshu / Datonglizhu witness
        + exact Dahan / Rainwater change-day fingerprint
        + explicit state-selection or recomposition operator
        + compatibility with closed C-II-N interior thresholds and Nanjing 59 endpoint

NCL-06627 remains an important negative control against silently normalizing divergent change-day schedules into the Sanming table.

Research record: `docs/research/ZIWEI-NCL06627-DATONGLIZHU-THRESHOLD-FINGERPRINT-R1.json`
