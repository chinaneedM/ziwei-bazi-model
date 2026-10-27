# Fusion Chart Historical Provenance Audit R1 — Batch 12EA

## 嘉靖十七年《舊唐書》軌漏百母半上進一取整規則物理閉合

Status: **1538 PHYSICAL WITNESS DIRECTLY PRESERVES BASE-100 HALF-UP / BELOW-HALF-DISCARD RULE AND EXPLICITLY EXTENDS IT TO 軌漏 / PRE-1578 REDUCTION-MECHANISM CLASS CLOSED / 58.6332→59 ENDPOINT COMPATIBLE / 57.9862→58 BREAKS C-II-N INTERIOR THRESHOLD STATE / 59.86→60 DOES NOT EXPLAIN WHOLE-59 / NO EXACT SANMING PARENT VOTE / NO RUNTIME CHANGE / NO ALGORITHM REOPEN**

## 1. Why this batch

Batch 12DZ left one high-value numerical gate open:

    pre-1578 fractional or continuous quantity
        -> historically attested integer reduction / recomposition
        -> official Nanjing 59-ke terminal display
        -> exact Sanming/Yueling change-day fingerprint

The next probe targeted a received calendrical rule in 《舊唐書》卷三十四. After an exploratory fascicle-location detour, direct physical boundary review fixed the target in fascicle 06, PDF p17. This batch adjudicates the successful exact-HEAD artifact and mechanically replays the rule against the already closed C-II-N and Nanjing controls.

## 2. Physical witness

    work: 舊唐書
    target: 卷三十四 志第十四 歷三
    edition: 明嘉靖十七年（1538）聞人詮吳郡刊本
    NCL call: 201.242 01535
    fascicle: NCL-01535 06
    RUN=35451542592
    ARTIFACT=10587006903
    ARTIFACT_DIGEST=sha256:33f879bcf4e1c7365caed7e4a9e6a8216fd0377fbda215940548a0b5283759e6
    PDF_SHA256=c08bb69617c00205f07f3c65cfdbfbcab45ba73d061cd5393947d421d8153df3
    TARGET_PDF_PAGE=17
    TARGET_PAGE_SHA256=93ace6d015b0b3cc55545652dce917f38b901c0060abf2ea80749f474ec15ec5
    OCR_USED_FOR_FINAL_GLYPH_OR_MECHANICAL_CLAIMS=false

The physical witness is the catalogued 1538 print. The earlier composition history of 《舊唐書》 is deliberately separated from the date of this surviving reviewed carrier.

## 3. Direct p17 rule

Direct no-OCR visual review closes the sequence:

    用百為母
    半已上從一
    已下棄之

The following instruction explicitly continues:

    下求軌漏
    餘分不滿准此

The safe mechanical normalization is therefore:

    denominator / mother = 100
    fractional remainder >= 1/2 -> advance one
    fractional remainder < 1/2 -> discard
    the following guilou remainder follows the same rule

The same physical page then proceeds into 推二十四氣定日, providing local calendrical-context control.

This is materially stronger than a generic later arithmetic analogy: it is a securely pre-1578 physical calendrical witness that explicitly attaches the rounding convention to 軌漏.

## 4. Forward-only locator correction

The probe history temporarily moved from fascicle 06 to 05 because OCR did not locate the target. Direct boundary inspection then showed that the 05→06 boundary merely continues the preceding lunar/phase procedure, while fascicle 06 p17 itself visibly contains the target rule.

The final workflow therefore fixes p14–p20 into the direct-review artifact window even when OCR returns zero hits. The locator correction is preserved forward-only rather than rewriting the exploratory history.

## 5. Mechanical replay against C-II-N

The historically attested rule can be represented, for this comparison only, as:

    Q(x) = floor(x) + 1  if fractional_part(x) >= 0.5
           floor(x)      otherwise

This is a replay model of the direct wording, not a claim that the source uses modern function notation.

### Interior control

From the closed C-II-N physical replay:

    day160 = 57.9862 ke
    clean stepped state before first 58 crossing = 57

Half-up gives:

    Q(57.9862) = 58

Therefore a global half-up mapping would promote the 58-ke bucket too early. It cannot be the universal generator of the already closed 42–58 C-II-N interior threshold sequence.

### Official Nanjing endpoint

The same C-II-N substrate has:

    summer endpoint = 58.6332 ke

The independently attested 1447 Nanjing official endpoint is:

    59 ke

Half-up gives:

    Q(58.6332) = 59

So the Jiutangshu rule is mechanically compatible with the endpoint **at this single layer**.

### Liu Zhuo near-59 control

The pre-1578 Liu Zhuo received value is:

    59.86 ke

Half-up gives:

    Q(59.86) = 60

Therefore this rule also does not explain a hypothetical 59.86 -> whole 59 route.

## 6. Adjudication

What is now closed:

    pre-1578 physical base-100 half-up/discard-below-half mechanism = CLOSED
    direct extension of that remainder rule to guilou = CLOSED
    endpoint compatibility for 58.6332 -> 59 = YES

What is now disproved:

    one universal Jiutangshu half-up rule
        generating the complete C-II-N 42–58 interior ladder
        plus the Nanjing 59 endpoint
        = DISPROVED BY REPLAY

What remains unresolved:

    exact Ming Nanjing/Datong use of this Jiutangshu rule
    exact state-dependent endpoint/recomposition binding
    exact Sanming/Yueling 大寒十三後 / 雨水後四日 fingerprint
    direct copy/ancestry into Sanming 1578

This batch therefore adds a real historical mechanism component without manufacturing a false full-lineage closure.

## 7. Transmission consequence

New nodes:

    PHYSICAL-COPY-JIUTANGSHU-NCL01535-JIAJING17-1538
    RULE-FAMILY-JIUTANGSHU-GUILOU-BASE100-HALFUP

New edges:

    TG-E0087 physical 1538 Jiutangshu copy
        --ATTESTS-->
        base-100 half-up guilou rule family

    TG-E0088 Jiutangshu half-up guilou rule family
        --SYNTHESIS_COMPONENT_CANDIDATE_FOR-->
        Nanjing C-II-N interior-threshold + 59-endpoint composite mechanism

The second edge is explicitly endpoint/reduction-class scoped. It is not a direct ancestry edge and does not override the replay contradiction in the C-II-N interior sequence.

## 8. Product firewall

    MATRIX_ROWS=198
    AUDITED_ROWS=166
    MISSING_FROM_PRODUCT=10
    PROVENANCE_DEFECTS=12/12_REPAIRED
    CONFIRMED_CHART_ALGORITHM_DEFECTS=0
    ALGORITHM_REOPEN=0
    CANDIDATE_COLLAPSE=0
    DETERMINISTIC_PRODUCT=CLOSED

No runtime candidate, winner, candidate collapse, or algorithm reopen is authorized.

## 9. Next gate

The search is now narrower again.

Priority is no longer merely "find any pre-1578 rounding rule." That class is now physically closed.

The unresolved target is:

    pre-1578 Nanjing/Datong or Tongshu source
        + state-dependent whole-ke selection/recomposition
        + preserves C-II-N interior thresholds
        + yields official 59-ke endpoint
        + preferably reproduces 大寒十三後 / 雨水後四日

Research record: docs/research/ZIWEI-JIUTANGSHU-JIAJING17-GUILOU-HALFUP-ROUNDING-R1.json
