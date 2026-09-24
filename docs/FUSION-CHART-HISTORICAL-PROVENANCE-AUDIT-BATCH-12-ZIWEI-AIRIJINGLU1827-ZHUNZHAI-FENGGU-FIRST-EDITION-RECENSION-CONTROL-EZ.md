# Fusion Chart Historical Provenance Audit R1 — Batch 12EZ

## 道光七年（1827）《愛日精廬藏書志》初刻本直接前推「孫逢古」并分离 1827/1887 正文层

Status: **1827 FIRST-EDITION FENGGU BIBLIOGRAPHIC VARIANT CLOSED / NLC SET NLC892-001947627 EDITION DATE + 卷二十三 + 準齋 TARGET DIRECTLY READ / 準齋心製几漏圖式一卷 + 抄本 + 宋孫逢古撰 + 文淵閣書目著錄 + 從吳門黃氏藏舊抄本影寫 DIRECT / BOUNDED 1827 TARGET ENTRY DOES NOT SHOW THE 1887 BODY PHRASE 由此逢吉以心法創茲小壺 / RECENSION DIFFERENCE CLOSED BUT DIRECTION UNRESOLVED / EARLIER 1602/1605 孫逢吉 CONTROLS RETAIN PRIORITY / NO SILENT NORMALIZATION / PRE-1578 EXACT RULE PROSE STILL OPEN / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12EY closed a Qing Tieqin manuscript witness for 孫逢古 but could not date that manuscript exactly. Its first next gate was therefore a source-bound 1827 first-edition 愛日精廬藏書志 target page.

Batch 12EX had also established an internal conflict in the 1887 Lingfenge edition:

    header -> 孫逢古撰
    same-entry body -> 由此逢吉以心法創茲小壺

The present batch asks two separate questions:

1. Is 孫逢古 already physically attested in the 1827 edition?
2. Does the bounded 1827 Zhunzhai entry already contain the 1887 body-form 逢吉 sentence?

## 2. Source binding

The reviewed NLC alternate set is NLC892-001947627.

Edition control, 第1冊:
- source SHA-256: 4d9ee8a1c6e9234daeedbb22b6dc9eec99a18f676684168321e8483e691214a6;
- direct 300-dpi PDF p5 SHA-256: c7dce87293230fdc79f6fcc0428d19d88a124b7e66f1709fdcd2668b54184433;
- p5 directly reads 道光七年歲在丁亥秋九月.

Target volume, 第5冊 / 317258:
- source SHA-256: c866354e719ab018a86e70181cbadf3b03fb6787c86cb0239d036782a0ae17a0;
- PDF p48 SHA-256: 98ce34e66b32a5c41ec3e190158250bf8dc51acf358c4da8c3bedf98a2eece12;
- PDF p50 SHA-256: 61ec3229c322de643eaefd81e0bb1a392ae1a6bb9fed326928e4bcf343bdacdc;
- PDF p51 SHA-256: 1c4282036fa8f43faa9fbfefe59449c2f46b4a306b3614bb5252582ce3f62d7c;
- workflow run 35955986758;
- artifact 10790402505;
- artifact digest sha256:6017c478ff5473bf71c6ccb0ebb752475215be34ba863d78974eb6105ac72a28;
- extraction commit a293343b93f2aee9c5616a9ff5c2bfefc2ef1343.

No OCR reading is final authority. All conclusions below come from direct source-bound 300-dpi page review.

A separate CADAL/Peking University scan also exposes 道光七年/丁亥 edition evidence, but it is not counted as an independent textual vote here.

## 3. p48 direct structure

PDF p48 directly opens:

    愛日精廬藏書志卷二十三
    子部
    天文算法類

The same page contains the preceding 新儀象法要 / 銅壺漏箭制度 neighborhood, physically binding the target to 卷二十三 rather than relying on OCR or modern indexing.

## 4. p50 direct Zhunzhai header

PDF p50 directly reads:

    準齋心製几漏圖式一卷
    抄本
    宋孫逢古撰
    文淵閣書目著錄
    從吳門黃氏藏舊抄本影寫

This closes the key chronology result:

    孫逢古 in Airijinglu bibliographic header
        = DIRECTLY ATTESTED BY THE 1827 EDITION

It is therefore no longer accurate to localize the received Fenggu form only to the 1887 Lingfenge edition or to an undated Qing manuscript layer.

## 5. p50-p51 bounded recension comparison

The Zhunzhai entry starts on p50 and continues across p50-p51. On p51 the next bibliographic entry directly begins:

    大宋寶祐四年丙辰歲會天萬年具注曆一卷
    抄本

Direct review of the complete bounded Zhunzhai entry surface on p50-p51 does not show the 1887 sentence:

    由此逢吉以心法創茲小壺

This is a finite source-surface nonattestation, not a whole-book OCR claim.

Therefore the two physically reviewed Airijinglu editions differ:

    1827 header = 孫逢古
    1827 bounded entry = no observed 由此逢吉以心法創茲小壺 sentence

    1887 header = 孫逢古
    1887 same-entry body = 由此逢吉以心法創茲小壺

The safe conclusion is:

    1827/1887 RECENSION DIFFERENCE = CLOSED
    direction / insertion source / intermediate state = UNRESOLVED

The 1887 body phrase must not be projected backward into the 1827 edition.

## 6. Author-variant chronology

The direct chain now reads:

    1602 國史經籍志 -> 孫逢吉
    1605 內閣藏書目錄 -> 孫逢吉
    1827 愛日精廬藏書志 header -> 孫逢古
    1887 愛日精廬藏書志 header -> 孫逢古
    1887 same-entry body -> 逢吉
    Qing Tieqin manuscript, exact copy year unresolved -> 孫逢古

Thus the currently closed physical chronology is:

    Fengji direct Ming controls: by 1602/1605
    Fenggu direct Airijinglu print control: by 1827

This narrows the bibliographic mutation/variant window but does not prove a single copying event, an exact mutation year, or a unique direction of textual descent.

The evidence still materially favors 孫逢吉 as the earlier directly controlled form. Automatic normalization remains forbidden.

## 7. Huang-copy route

The 1827 target directly gives:

    從吳門黃氏藏舊抄本影寫

This materially strengthens Batch 12EY's Huang/Raoweng provenance bridge and is chronologically fixed to 1827.

It still does not by itself prove:

- exact physical identity with the reviewed NLC 1823 Huang Shiliju manuscript;
- exact identity with the Tieqin-described 郡中黃氏舊藏 copy;
- a direct-copy chain from one surviving object to another.

## 8. Transmission-genealogy consequence

Batch 12EZ adds:

- PHYSICAL-COPY-NLC-AIRIJINGLU-DAOGUANG7-1827-SET001947627;
- PASSAGE-AIRIJINGLU1827-ZHUNZHAI-FENGGU-RECENSION;
- TG-E0104: the dated 1827 physical print ATTESTS the Zhunzhai/Fenggu/Huang-copy passage.

The Zhunzhai rule-family node is strengthened only at bibliographic variant chronology and recension-control level.

TG-E0102 for the 1887 print is not rejected. Its scope remains the 1887 physical surface; 12EZ prevents that later body sentence from being silently back-projected into 1827.

## 9. Sanming and product firewall

No Sanming/Yueling Dahan-Rainwater fingerprint or Nanjing-59 rule is added.

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

## 10. Next gate

1. Trace the Huang Pilie/Raoweng paratext itself, especially the dated collation/preface evidence around the 1823 Shiliju manuscript, to bind the exact manuscript route if possible.
2. Search intermediate pre-1887 Airijinglu recensions/reprints or manuscript copies for the first appearance of the body phrase 由此逢吉以心法創茲小壺.
3. Continue the Yuan person-title bridge and securely pre-1578 exact 25-arrow prose search.
4. Continue the independent Sanming/Yueling Dahan-Rainwater + Nanjing-59 search.

Research record: docs/research/ZIWEI-AIRIJINGLU1827-ZHUNZHAI-FENGGU-FIRST-EDITION-RECENSION-CONTROL-R1.json
