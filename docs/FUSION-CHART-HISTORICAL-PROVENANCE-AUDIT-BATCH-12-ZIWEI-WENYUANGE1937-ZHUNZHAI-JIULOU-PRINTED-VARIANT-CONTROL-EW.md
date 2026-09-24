# Fusion Chart Historical Provenance Audit R1 — Batch 12EW

## 1937 商務本《文淵閣書目》直接復核《準齋九漏新式》字形

Status: **1937 PRINTED RECEIVED-TEXT JIULOU READING CLOSED / 準齋九漏新式一部一冊完全 DIRECTLY READ ON PDF P194 / 1799 九漏 IS NO LONGER SINGLE-SURFACE OR OCR-DEPENDENT / NOT A SECOND INDEPENDENT 1441 WITNESS / 九↔几 DIRECTION UNRESOLVED / PRE-1578 EXACT 25-ARROW PROSE STILL OPEN / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12EV made title variation an explicit collation target:

- 1441 《文淵閣書目》 received line: `準齋九漏新式`;
- 1602 《國史經籍志》: `準齋几漏圖式一卷`;
- 1605 《內閣藏書目錄》: `準齋几漏新式一冊`;
- 1823 operational manuscript: `準齋心製几漏圖式`.

The immediate next question was whether the `九漏` reading in the source-bound 1799 《文淵閣書目》 witness could be independently re-seen on another physical printed surface, rather than remaining vulnerable to a one-copy or transcription error.

## 2. Source binding

The reviewed later printed surface is:

- 《文淵閣書目》;
- 商務印書館《國學基本叢書》本;
- provider metadata/publication layer: 中華民國二十六年二月初版 / 1937;
- public file: `NLC511-023031404016761-25273 文淵閣書目.pdf`;
- source PDF SHA-256: `f8ff2c2bb82bd10fb3fb65e8f02f43d3eed76b609dfe6d821b6ebb2656e7924a`;
- target: PDF p194;
- target page SHA-256: `e8795fd55ed09d45dbb2819f0684a7197a140fe2b9445fbeb36c6d3c6bd0e611`;
- target image: 1408 × 2240;
- neighbor p193 SHA-256: `e4d0fc73f745bbeae23ff6ab7c875e7c809e20c45695b079fb47667086458301`;
- neighbor p195 SHA-256: `dbdf850126fbcbb591d0817d63c4fff8e8aefb1d48b9fc9f3957c8caa91cba63`;
- extraction commit `5ef6d91802dd3a6ac1f05b5de05d4952ca27da8d`;
- workflow run `35949137241`;
- artifact `10788136324`, digest `sha256:adf4f3e9c42646e21a41f1d7a1546e37ef99f363f571a8a8b7e486edba5b0e79`.

Final glyph adjudication is direct page-image review. OCR is not used as authority.

## 3. Direct physical reading

The page is headed:

    文淵閣書目 卷十五

The target column directly reads:

    準齋九漏新式一部一冊完全

Immediate page-order controls are:

    官歷漏刻圖一部一冊
    準齋九漏新式一部一冊完全
    年日月通用一部一冊完全

Adjudication:

    1937_PRINTED_WENYUANGE_JIULOU_TITLE_READING = CLOSED

## 4. Relation to the 1799 physical witness

Batch 12EQ directly reviewed the 1799 physical transmission witness and read:

    準齋九漏新式

Batch 12EW now directly reads the same title core on the 1937 printed edition:

    準齋九漏新式

Safe conclusion:

    WENYUANGE_RECEIVED_TEXT_JIULOU_READING
        = DIRECTLY RECONFIRMED ON A LATER PRINTED SURFACE

This is useful because the `九` reading no longer rests on a single physical scan, OCR output, or modern transcription.

However:

    1799 + 1937
        != two independent 1441 witnesses

The 1937 edition is a late received-text print. Its exact stemmatic dependence on the 1799 line or another recension is not closed here.

## 5. 九/几 title-variant firewall

Current direct evidence remains:

    文淵閣書目 received line:
        1799 -> 準齋九漏新式
        1937 -> 準齋九漏新式

    國史經籍志 1602:
        準齋几漏圖式

    內閣藏書目錄 1605:
        準齋几漏新式

    1823 operational manuscript:
        準齋心製几漏圖式

This establishes real received-title divergence. It does **not** yet determine:

- whether `九` is a corruption of `几`;
- whether `几` is a later correction;
- whether `新式` and `圖式` mark textual states or ordinary catalog variation;
- the copy direction among the catalog traditions.

Therefore no editorial normalization is authorized.

## 6. Chronology firewall

The 1937 print adds no pre-1578 physical chronology.

The 1441 date remains the catalog-text event control established separately from the received preface tradition. The 1799 and 1937 objects remain later transmission witnesses.

Likewise, this batch does not backdate the exact 25-arrow / winter-forward / summer-reverse / 日曆節候 wording now directly read in the 1823 operational manuscript.

## 7. Transmission-genealogy consequence

Batch 12EW adds:

- `PHYSICAL-COPY-WENYUANGE-SHUMU-BUSINESS-PRESS-1937`;
- `PASSAGE-WENYUANGE1937-ZHUNZHAI-JIULOU-ENTRY`;
- `TG-E0101`: the 1937 physical print **ATTESTS** the printed `九漏新式` passage.

The Zhunzhai rule-family node gains a received-title variant control. No operational rule, author identity, or composition date is inferred from this late bibliographic print.

## 8. Sanming and product firewall

This source contains no Dahan/Rainwater numerical fingerprint, no Nanjing-59 endpoint rule, and no natal-time runtime mapping.

Therefore:

    direct Sanming-parent vote increment = 0
    algorithm reopen = 0
    candidate collapse = 0

Project accounting remains:

    MATRIX_ROWS=198
    AUDITED_ROWS=166
    MISSING_FROM_PRODUCT=10
    PROVENANCE_DEFECTS=12/12_REPAIRED
    CONFIRMED_CHART_ALGORITHM_DEFECTS=0
    DETERMINISTIC_PRODUCT=CLOSED

## 9. Next gate

1. Find another **premodern physical** 《文淵閣書目》 recension to test `九/几` independently of the 1799 received line.
2. Collate Qing bibliographies and Huang Pilie transmission notes, especially 《愛日精廬藏書志》, without treating their Song attribution as primary dating proof.
3. Continue the Yuan person-title bridge and securely pre-1578 exact 25-arrow prose searches.
4. Continue the independent Sanming/Yueling Dahan/Rainwater fingerprint and Nanjing-59 search.

Research record: `docs/research/ZIWEI-WENYUANGE1937-ZHUNZHAI-JIULOU-PRINTED-VARIANT-CONTROL-R1.json`.
