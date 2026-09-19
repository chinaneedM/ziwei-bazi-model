# Fusion Chart Historical Provenance Audit R1 — Batch 12DZ

## 京都《蘭盆疏鈔餘義》40↔60整刻表物理闭合 + 天一阁《虎鈐經》独立册次控制

Status: **KYOTO MANUSCRIPT DIRECTLY ATTESTS A 40↔60 WHOLE-KE SEASONAL TABLE / 雨水後四日至後九日=46/54 DIRECT / 59/41 DIRECTLY PRESENT BUT TABLE CONTINUES TO 60/40 / 1716 INTERNAL COLOPHON CLAIMS COLLATION AGAINST 宋刻古本 / CLAIM ≠ SURVIVING PRE-1578 PHYSICAL WITNESS / TIANYI HUQIAN MING REPROBE CONFIRMS DISTINCT 47/53→48/52 + 60/40 FINGERPRINT / SECOND TIANYI OBJECT 0004676 IS JUAN11–20 ONLY / NO SECOND JUAN7 VOTE / NO NANJING-59 RECOMPOSITION RULE / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE / NO ALGORITHM REOPEN**

## 1. Why this batch

12DY closed a 1518 institutional multisource/locality-calibration proposal but left the numerical gate unchanged:

    pre-1578 continuous/fractional value
        -> historical whole-ke reduction/recomposition
        -> Nanjing 59-ke terminal display
        -> exact Sanming/Yueling change-day fingerprint

Three probe commits followed 12DY: a Kyoto manuscript whole-ke table, a re-probe of the Tianyi Ming-print Huqian target section, and a second Tianyi Huqian census object. This batch adjudicates those probe artifacts as one forward-only research unit.

## 2. Kyoto physical manuscript — direct table

Source:

    Kyoto University Rare Materials Digital Archive
    record: RB00017646
    title: 蘭盆疏鈔餘義
    catalog author: (宋僧)日新録
    copy type: 写
    shelfmark: 藏||14||ラ||2
    public catalog copy date: unresolved
    RUN=35445786963
    ARTIFACT=10585318567
    ARTIFACT_DIGEST=sha256:a15f4752a7f6cc1f8af694b495ad21a2722787de4a23eb5f7676cc4af4e04bfe
    OCR_USED_FOR_FINAL_GLYPH_OR_NUMERIC_CLAIMS=false

Canvas 34, SHA256=0d7f3461d82129b154f25101550c22a05b30705fac16eb9f8daa989f13a1b2db, directly shows:

    節氣加減刻漏規式
    46/54 bucket:
        雨水後四日至後九日

Canvas 35, SHA256=cc4a2356cfafe21b61545a09e01db256f1e1f3523098d2f82b5283cd6a7dff0f, directly carries the upper end of the integer ladder, including:

    五十九刻 / 四十一刻
    六十刻 / 四十刻

Therefore 59/41 is physically present in this table, but it is not the terminal cap. The same table continues to 60/40.

This matters because it directly blocks another shortcut:

    occurrence of 59/41
        ≠
    proof of Nanjing-style 59-ke terminal quantization.

## 3. Kyoto canvas 40 — Song-print collation claim, with chronology firewall

Canvas 40, SHA256=12beea4d2c26aec7a826acb7f069f3712990d0ef342f1c0971a872e2de65a71b, directly reads the internal note:

    享保元丙申稔仲冬上旬以宋刻古本校正訖
    日本國南京沙門秀慶識

The safe reading is narrow:

    explicit 1716 claim of collation against a Song printed old book = DIRECTLY ATTESTED
    surviving Kyoto object = manuscript, copy date unresolved
    surviving Song printed exemplar = NOT PRESENT
    every target-table numeral unchanged from that Song print = NOT PROVED
    pre-1578 physical carrier for this exact table = NOT CLOSED

The colophon is valuable transmission evidence, but it cannot be promoted into a surviving Song or pre-1578 physical table witness.

## 4. Tianyi Ming-print Huqian re-probe

Existing physical witness:

    Tianyi census: 330000-1705-0004205
    call number: 馮善1426
    edition metadata: 明刻本; exact Ming impression year unresolved
    RUN=35444357383
    ARTIFACT=10584312941
    ARTIFACT_DIGEST=sha256:5d790574d4d0adddfbdbb6bee9c0373213b1181394fd132a18c9d1bb906cff19

Direct pages reconfirm the already registered target:

    p74 SHA256=9afad08f340b2241057241e1818238f55b29d72e9a76d8707fb8786b3d7793a6
        傳箭第七十六
        每時有八刻二十分
        一日十二時合一百刻

    p74-p75
        雨水初日改第八箭 -> 47/53
        後第九日改第九箭 -> 48/52

    p76 SHA256=1acee7f93d714eedafeb11b2cfbf9883e56e388ea7c8384b3f2c89eec0b7724c
        夏至前三日改第一箭 -> 60/40

This is a successful physical re-confirmation, not a new witness vote. Batch 12CY already closed the decisive Huqian fingerprint. The new probe does not recover an exact pre-1578 impression date.

## 5. Second Tianyi object — independent-copy control

Second object:

    Tianyi census: 330000-1705-0004676
    call number: 善2313
    old collection note: 朱鼎煦舊藏
    edition metadata: 明刻本; exact Ming impression year unresolved
    RUN=35445786995
    ARTIFACT=10585408471
    ARTIFACT_DIGEST=sha256:f680d383623635d0cb25d82fa52ebac1bd371dd8eaa9de6431563fba86820408

Direct endpoint review:

    p1 SHA256=f1b7039f6b2f0195993391b7684c0df91a9c6f83afad66df3335eba7ee502107
        虎鈐經卷第十一

    p99 SHA256=7251f88551eff284fae50daf2f5396e46fe3964f081f2ddd1ebb3e935cd2d8f0
        虎鈐經卷第二十終

Therefore the reviewed one-volume object is physically scoped to juan 11–20. It does not contain juan 7 《傳箭》 and cannot be counted as a second independent target-section witness.

## 6. Mechanism comparison

The new Kyoto direct physical table and the already closed Huqian family share a broad architecture:

    whole-ke seasonal ladder
    100-ke day context
    integer day/night pairs
    summer progression to 60/40

But their numeric/change-day fingerprints are not identical:

    Kyoto Lanpen:
        雨水後四日至後九日 = 46/54
        59/41 occurs inside the ladder
        terminal maximum = 60/40

    Huqian:
        雨水初日 = 47/53
        後第九日 = 48/52
        terminal maximum = 60/40

    Sanming 1578:
        terminal maximum = 59/41
        exact parent/recomposition rule remains unresolved

This strengthens the historical breadth of discrete whole-ke seasonal binning, while further demonstrating that a bare 59/41 occurrence is not sufficient to identify the Sanming/Nanjing lineage.

## 7. Transmission consequence

New graph objects:

    PHYSICAL-COPY-LANPEN-KYOTO-RB00017646
    PASSAGE-LANPEN-KYOTO-1716-SONG-PRINT-COLLATION-COLOPHON
    RULE-FAMILY-LANPEN-JINGFUDIAN-WHOLEKE-40-60

Edges:

    TG-E0084 Kyoto physical copy -> ATTESTS -> Lanpen whole-ke 40↔60 rule family
    TG-E0085 Kyoto physical copy -> ATTESTS -> 1716 Song-print-collation colophon
    TG-E0086 Lanpen rule family -> STRUCTURAL_ANCESTRY_CANDIDATE_FOR -> Sanming 1578 table

Explicit non-edges preserve two firewalls:

    Lanpen direct unchanged table identity -> Sanming = DISPROVED
        because Lanpen continues to 60/40 while Sanming terminates at 59/41.

    Lanpen direct unchanged table identity -> Huqian = DISPROVED
        because the reviewed Rainwater change-day/value fingerprints differ.

Structural ancestry remains researchable; unchanged-table identity does not.

## 8. Product firewall

    MATRIX_ROWS=198
    AUDITED_ROWS=166
    MISSING_FROM_PRODUCT=10
    PROVENANCE_DEFECTS=12/12_REPAIRED
    CONFIRMED_CHART_ALGORITHM_DEFECTS=0
    ALGORITHM_REOPEN=0
    CANDIDATE_COLLAPSE=0
    DETERMINISTIC_PRODUCT=CLOSED

## 9. Next gate

Do not spend the next pass merely collecting additional generic 40↔60 tables.

The unresolved high-value gate remains:

    securely pre-1578 source
        + explicit numerical reduction/recomposition
        + continuous/fractional or C-II-N input
        + terminal Nanjing 59-ke display
        + preferably the exact Sanming/Yueling Dahan/Yushui change-day fingerprint.

12DZ closes a new physical received-table witness and a Song-print-collation claim, while explicitly refusing to convert either into the missing pre-1578 59-ke quantization parent.
