# Fusion Chart Historical Provenance Audit R1 — Batch 12FA

## 1823 士禮居《準齋》黃丕烈跋：把「原書舊鈔」與「錄副」分層，阻止黃氏舊抄本身份誤合併

Status: **1823 HUANG PILIE PARATEXT DIRECTLY CLOSED / 原書舊鈔 vs 錄副 EXPLICITLY SEPARATED / 原書舊鈔當是影宋 RETAINED AS QING BIBLIOGRAPHIC JUDGMENT NOT PHYSICAL-DATE PROOF / 1827 從吳門黃氏藏舊抄本影寫 != CURRENT 1823 SHILIJU OBJECT BY DEFAULT / EXACT SOURCE-COPY IDENTITY REMAINS OPEN / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12EZ fixed the 1827 《愛日精廬藏書志》 wording:

    從吳門黃氏藏舊抄本影寫

but still could not decide whether that phrase names the exact Qing Daoguang-3 / 1823 Huang-family Shiliju manuscript physically reviewed in Batch 12DV.

The decisive next question is therefore not merely “did Huang Pilie own the book?” It is:

> Does Huang Pilie's own received paratext distinguish an older source copy from a newly made circulation copy?

If it does, then all later “黃氏舊抄” references must preserve that source/copy distinction rather than collapsing every Huang-family object into one physical manuscript.

## 2. Direct physical source binding

The controlling physical surface is the same Batch 12DV source-bound reproduction:

- 《續修四庫全書》第1031冊;
- underlying catalogued object: National Library of China-held Qing Daoguang-3 Huang-family Shiliju manuscript;
- source PDF SHA-256: `07348e40ec26ca38efe9c9736a69c403c61f9b07a2c89a847fc68d00ce6d8c25`;
- target PDF p76 SHA-256: `64aad110e3cba4984cb784e9f97c99044fbc25e39a06744000a7a606ba73ffeb`;
- high-resolution workflow run: `35438178430`;
- artifact: `10583226243`;
- artifact digest: `sha256:771155d081d669f1d1020213e2edc17d56d81594e625c267ce68b4f191cac6ce`.

No OCR is final authority. The paratext below was re-adjudicated from the preserved source-bound p76 image.

A separate 2026-09-24 acquisition of NLC `NLC892-001926727-315344` 《士禮居藏書題跋記》 (workflow `35964719021`, artifact `10793847186`, digest `sha256:56bcaeef97c3cfc131acd989213f639ed831e52d54bf1a6219d7305df28aeb35`) confirms the title is present in that received collection, but its OCR hit is used only as a locator/control and is not needed for the decisive glyph claims.

## 3. p76 direct paratext

The p76 Huang paratext directly preserves the following high-information phrases:

    此銅壺漏箭制度準齋心製几漏圖式共二種見諸文淵閣書目
    此本敘次先後互易從其古本之流傳也
    原書舊鈔當是影宋
    余恐流傳未廣錄副以便傳觀或互相鈔錄
    道光癸未仲冬月蕘夫書

The date is explicit:

    道光癸未 = 道光三年 = 1823

The decisive philological distinction is equally explicit:

    原書舊鈔
        !=
    錄副

Huang is discussing an older source copy and separately describes making/circulating a duplicate copy so the work can be seen and recopied.

## 4. “影宋” chronology firewall

The phrase:

    原書舊鈔當是影宋

is a Qing-period bibliographic judgment by Huang Pilie about the character of the older source copy.

It does **not** prove:

- that the physically reviewed 1823 manuscript was copied in the Song;
- that a currently surviving source object is a Song physical manuscript;
- that the exact 25-arrow wording is physically attested before 1578.

Therefore:

    HUANG "當是影宋"
        = QING BIBLIOGRAPHIC / TEXTUAL-ASSESSMENT EVIDENCE

    secure Song physical witness
        = NOT PROVED

    secure pre-1578 exact 25-arrow physical witness
        = NOT PROVED

## 5. Huang source-copy / recopy firewall

Batch 12EZ gives:

    1827 Airijinglu:
    從吳門黃氏藏舊抄本影寫

Batch 12FA now gives, from the 1823 Huang paratext:

    原書舊鈔
    +
    錄副以便傳觀

This means a one-object shortcut is unsafe.

The currently reviewed 1823 Shiliju manuscript is a Huang-family Daoguang-3 manuscript carrying the 1823 paratext, but the evidence does not yet prove whether this exact surviving object is:

1. Huang's upstream `原書舊鈔`;
2. the `錄副` made for circulation;
3. another manuscript carrying/copying the same paratext.

Accordingly:

    1827 "吳門黃氏藏舊抄本"
        ==
    currently reviewed 1823 Shiliju physical object

        = NOT_PROVED

The reason is now stronger than generic caution: the source tradition itself explicitly contains at least two copy layers.

## 6. Transmission consequence

Batch 12FA adds:

- `PASSAGE-SHILIJU1823-ZHUNZHAI-HUANG-PILIE-OLD-COPY-RECOPY`;
- `TG-E0105`: the already registered 1823 Shiliju physical-copy node **ATTESTS** Huang's old-copy/recopy distinction.

The existing 1827 and Tieqin Huang/Raoweng provenance routes remain valid, but they must now pass through an identity firewall:

    Huang-family provenance convergence = STRONG

    exact surviving-object identity = OPEN

    old-source vs circulation-recopy distinction = DIRECTLY CLOSED

No direct-copy edge from the reviewed 1823 object to the 1827 Airijinglu source copy is authorized.

## 7. Author and rule chronology remain separate

This batch does not alter the established author-name chronology:

    1602 國史經籍志 -> 孫逢吉
    1605 內閣藏書目錄 -> 孫逢吉
    1827 愛日精廬藏書志 -> 孫逢古
    1887 愛日精廬藏書志 header -> 孫逢古
    1887 same-entry body -> 逢吉

Nor does Huang's “影宋” judgment identify the Yuan 1281 Yanling Sun Fengji with the Zhunzhai author.

## 8. Sanming and product firewall

The new evidence changes manuscript transmission modeling, not the deterministic chart runtime.

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

1. Identify a physical/call-number/provenance marker that distinguishes Huang's `原書舊鈔` from the `錄副`, and determine which layer Zhang Jinwu used by 1827.
2. Search pre-1887 Airijinglu intermediate recensions for first appearance of `由此逢吉以心法創茲小壺`.
3. Continue the Yuan person-title bridge and securely pre-1578 exact 25-arrow prose search.
4. Continue the independent Sanming/Yueling Dahan-Rainwater + Nanjing-59 search.

Research record: `docs/research/ZIWEI-SHILIJU1823-ZHUNZHAI-HUANG-PILIE-OLD-COPY-RECOPY-FIREWALL-R1.json`.
