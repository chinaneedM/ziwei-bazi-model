# Fusion Chart Historical Provenance Audit R1 — Batch 12EU

## 1602《國史經籍志》原刊本直接閉合《準齋几漏圖式》—孫逢吉書名著者綁定

Status: **MING 1602 ORIGINAL-PRINT TITLE/AUTHOR PAIRING DIRECTLY CLOSED / 準齋几漏圖式一卷 + 孫逢吉 READ ON SAME PHYSICAL ENTRY / OCR NOT USED FOR FINAL GLYPHS / YUAN 1281 YANLING PERSON IDENTITY STILL POSSIBLE_NOT_PROVED / PRE-1578 EXACT 25-ARROW PROSE STILL OPEN / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12ET left a specific authorship gate open. The repository already had:

- a 1441 catalog-text title-family antecedent for Zhunzhai;
- a source-bound 1823 operational manuscript with the 25-arrow mechanism;
- a received Yuan Fang Hui passage naming a Yanling Sun Fengji interested in astronomy and the Yan Su clepsydra tradition;
- modern specialist scholarship proposing that this Yuan person was the Zhunzhai author.

The missing bridge was a directly readable historical bibliographic witness pairing the Zhunzhai title itself with the author name 孫逢吉.

## 2. Source binding

The reviewed witness is:

- 《國史經籍志》卷三;
- (明) 焦竑撰;
- NCL call/object: `NCL-04980 03`;
- provider metadata: 明萬曆壬寅（三十年，1602）原刊本;
- source PDF SHA-256: `cc40a6517e748707a5af77535e073a11450da986cb7add0528916178d4e6bdd2`;
- target: PDF p19;
- 300-dpi full-page render SHA-256: `b0069785c581a37dafe2ab84799e4f60bfb36b79decd935632e72f60339b6a04`;
- target-band SHA-256: `3e7e665942c1b634d0d2fb8ee7dd44e440f9bb29df15ee2602bf5d6c60715625`;
- workflow run `35732165452`;
- artifact `10696230809`, digest `sha256:f1fc82267322bd77405d246249a95849df892845e6e4ec270ccac880148f9458`.

Final glyph adjudication is direct image review. OCR is not used as authority.

## 3. Direct physical reading

The p19 target column directly reads:

    準齋几漏圖式一卷

The small author annotation attached to that same entry directly reads:

    孫逢吉

The neighboring entry provides a layout control: `燕几圖一卷` carries `黃伯思` in the same small-author-annotation format. The target therefore does not depend on assigning loose nearby characters to the wrong title.

Adjudication:

    MING_1602_ORIGINAL_PRINT_TITLE_AUTHOR_ATTRIBUTION = CLOSED

## 4. What is now proved

At the physical 1602 bibliographic layer, the work title and author attribution are directly paired:

    準齋几漏圖式一卷  ->  孫逢吉

This is stronger than relying on a modern transcription or on Wang Xiaohu's quotation of the catalog.

It also supplies an independent historical control against the later `孫逢古` bibliographic reading discussed in modern scholarship: the reviewed 1602 original-print witness itself has `孫逢吉`.

## 5. What is not proved

This batch does **not** collapse the following distinct questions:

    1602 title-author attribution
        != work composition date
        != exact identity of the historical person
        != pre-1578 exact 25-arrow prose
        != direct textual ancestry

In particular, Fang Hui's received Yuan passage names a Yanling Sun Fengji with relevant astronomical/clepsydra interests, but does not name 《準齋几漏圖式》.

Therefore:

    1281 Yanling Sun Fengji == Zhunzhai author
        = POSSIBLE_NOT_PROVED

The 1602 witness materially strengthens the name side of the bridge, but does not by itself close personal identity across the two sources.

## 6. Chronology firewall

The 1602 witness is post-1578. It therefore does not satisfy the still-open requirement for a securely pre-1578 physical carrier of the exact Zhunzhai 25-arrow / winter-forward / summer-reverse / 日曆節候 wording.

The earlier 1441 《文淵閣書目》 title-family antecedent remains separately scoped:

- title-family existence before 1578: closed at catalog-text layer;
- exact identity of all title variants: not forced;
- exact 25-arrow wording before 1578: not closed;
- direct author attribution in the 1441 physical textual layer: not claimed here.

## 7. Transmission-genealogy consequence

Batch 12EU adds two evidence-scoped nodes:

- `PHYSICAL-COPY-NCL-GUOSHI-JINGJIZHI-WANLI30-1602-V3`;
- `PASSAGE-GUOSHI1602-ZHUNZHAI-SUNFENGJI-ENTRY`.

And one confirmed evidence edge:

    TG-E0098
    1602 physical copy
      -- ATTESTS -->
    Zhunzhai title/author catalog passage

The Zhunzhai rule-family node is strengthened only with a bibliographic author-attribution field. No operational rule is backdated from this catalog entry.

## 8. Sanming and product firewall

This witness contributes no Dahan/Rainwater numeric fingerprint and no Nanjing-59 endpoint evidence.

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

1. Continue direct physical collation of the 《內閣書目》 author line and other early bibliographic witnesses.
2. Seek a Yuan or otherwise identity-closing primary bridge that names both the historical person and the Zhunzhai work.
3. Continue searching for a securely pre-1578 carrier of the exact 25-arrow operational prose.
4. Continue the independent Sanming/Yueling Dahan/Rainwater fingerprint and Nanjing-59 searches.

Research record: `docs/research/ZIWEI-GUOSHI1602-ZHUNZHAI-SUNFENGJI-DIRECT-AUTHOR-TITLE-BINDING-R1.json`.
