# Fusion Chart Historical Provenance Audit R1 — Batch 12EB

## 《古今律曆考》卷二：大統日出分端點與 59/41 整刻顯示物理綁定

Status: **MING NLC PHYSICAL PAGE DIRECTLY BINDS DATONG SOLSTITIAL SUNRISE-FEN 2068.30 / 2931.70 TO 59/41 / 41/59 WHOLE-KE DISPLAY / LATER-MING MECHANICAL BRIDGE CLOSED / SECURE PRE-1578 BINDING STILL OPEN / INTERIOR 42–58 SELECTION RULE STILL OPEN / SANMING-YUELING CHANGE-DAY FINGERPRINT STILL OPEN / ZERO EXACT SANMING-PARENT VOTE / NO RUNTIME CHANGE / NO ALGORITHM REOPEN**

## 1. Why this batch

12EA closed a real pre-1578 fractional-reduction rule, but its global replay failed the C-II-N interior threshold sequence. The remaining question was whether any source explicitly places the Datong continuous/fractional endpoint layer and the whole-ke 59/41 display in one passage.

The next probe targeted 邢雲路《古今律曆考》卷二. The exact-HEAD artifact succeeded and fixed the target at PDF p52.

## 2. Physical witness

    work: 古今律曆考
    author: 邢雲路
    target: 卷二
    provider: National Library of China surrogate via Wikimedia Commons
    provider date: 明萬曆[1573-1620]
    exact impression year of reviewed object: unresolved
    RUN=35506520386
    ARTIFACT=10603956470
    ARTIFACT_DIGEST=sha256:98e2aa1b9d8a415aa04242e662d490fad5d261dbf61ec6e777d2296db30abf01
    PDF_SHA256=ad413ec420d9f3713a1a6a10e747173992b4ca0e8c55c30a96205b40ae3affbf
    TARGET_PDF_PAGE=52
    TARGET_PAGE_SHA256=e7e5289a0912b37c8c011a1d7b5f3b1235fd7d31c121cff61695c8f39fb445b9
    OCR_USED_FOR_FINAL_GLYPH_OR_NUMERIC_CLAIMS=false

Chronology firewall: this object is not securely dated before 1578. It is therefore a later-Ming mechanical/transmission control, not a Sanming ancestor.

## 3. Direct p52 binding

Direct visual review closes the following same-page sequence:

    大統曆推夏至日出分二千六十八分三十秒
    冬至日出分二千九百三十一分七十秒

and the corresponding whole-ke display:

    夏至日出寅正四刻日入戌初初刻
    晝五十九刻 夜四十一刻

    冬至日出辰初初刻日入申正四刻
    晝四十一刻 夜五十九刻

This is stronger than the previous received-text semantic control because the numerical input layer and the 59/41 endpoint display are physically bound on one source-controlled page.

## 4. Mechanical consequence

The existing C-II-N physical replay gives a summer endpoint of 58.6332 ke. The 1447 official Nanjing record independently gives a 59-ke summer endpoint.

12DQ therefore created a composite hypothesis:

    C-II-N continuous/interior layer
    + official Nanjing 59 endpoint
    + unresolved binding/recomposition

12EB now closes that **a later-Ming Datong tradition physically contains such an endpoint binding**:

    Datong solstitial sunrise-fen values
        -> whole-ke 59/41 / 41/59 display

This does not yet prove the exact numerical operator. The passage supplies the linked input/output states, not a complete universal reduction function.

## 5. What this does not close

The following remain unresolved:

- a securely pre-1578 physical binding witness;
- the exact state-dependent rule that preserves the C-II-N interior 42–58 thresholds;
- whether the endpoint is produced by table lookup, cap, arrow selection, special-term recomposition, or another operation;
- the Sanming/Yueling 大寒十三後 / 雨水後四日 transition fingerprint;
- direct copying or ancestry into Sanming 1578.

Accordingly, this batch narrows chronology and mechanism scope without manufacturing a lineage winner.

## 6. Transmission consequence

New nodes:

    PHYSICAL-COPY-XINGYUNLU-NLC371920-MING-WANLI
    RULE-FAMILY-XINGYUNLU-DATONG-ENDPOINT-FEN-TO-59_41

New edges:

    TG-E0089 physical NLC Xingyunlu object
        --ATTESTS-->
        Datong endpoint fen-to-59/41 rule family

    TG-E0090 Xingyunlu endpoint-binding rule family
        --STRUCTURAL_MECHANISM_CANDIDATE_FOR-->
        Nanjing C-II-N interior-threshold + 59-endpoint composite mechanism

TG-E0090 is a later-Ming mechanical bridge only. It is not an ancestry edge into Sanming.

## 7. Product firewall

    MATRIX_ROWS=198
    AUDITED_ROWS=166
    MISSING_FROM_PRODUCT=10
    PROVENANCE_DEFECTS=12/12_REPAIRED
    CONFIRMED_CHART_ALGORITHM_DEFECTS=0
    ALGORITHM_REOPEN=0
    CANDIDATE_COLLAPSE=0
    DETERMINISTIC_PRODUCT=CLOSED

No runtime candidate, winner, candidate collapse, or algorithm reopen is authorized.

## 8. Next gate

The missing link is now more precise:

    securely pre-1578 source
        + Datong/Nanjing endpoint binding
        + state-dependent interior/endpoint selection logic
        + preferably 大寒十三後 / 雨水後四日

Research record: `docs/research/ZIWEI-XINGYUNLU-DATONG-ENDPOINT-BINDING-R1.json`
