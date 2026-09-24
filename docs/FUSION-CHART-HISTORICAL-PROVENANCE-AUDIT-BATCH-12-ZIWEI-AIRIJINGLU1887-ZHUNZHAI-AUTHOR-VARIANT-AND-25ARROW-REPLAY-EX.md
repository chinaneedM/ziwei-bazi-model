# Fusion Chart Historical Provenance Audit R1 — Batch 12EX

## 1887《愛日精廬藏書志》直接閉合「孫逢古／逢吉」內部異文與二十五箭規則重放

Status: **1887 PHYSICAL PRINT AUTHOR-VARIANT INTERNAL CONFLICT CLOSED / HEADER 孫逢古撰 VS SAME-ENTRY BODY 由此逢吉以心法創茲小壺 / 準齋心製几漏圖式一卷 + 黃氏藏舊抄本影寫 DIRECTLY READ / 25-ARROW WINTER-FORWARD SUMMER-REVERSE 日曆節候 MECHANISM REPLAYED / FENGGU LATE VARIANT-CORRUPTION STRONGLY SUPPORTED NOT ABSOLUTELY NORMALIZED / PRE-1578 EXACT PROSE STILL OPEN / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12EU and 12EV supplied two earlier Ming bibliographic controls:

    1602 《國史經籍志》:
        準齋几漏圖式一卷 / 孫逢吉

    1605 《內閣藏書目錄》:
        準齋几漏新式一冊 / 孫逢吉著莫詳時代

Modern and Qing bibliographic layers also circulate the variant `孫逢古`. The immediate question was whether a source-bound physical witness could localize that variant rather than treating the two names as interchangeable.

## 2. Source binding

The reviewed witness is:

- 《愛日精廬藏書志》卷二十三;
- 清張金吾撰;
- 吳縣徐氏靈芬閣，清光緒十三年（1887）活字本;
- source object: `NLC892-001947629-315323`, 第5冊;
- source PDF SHA-256: `e8789679d196a38b4fba60ee69e0eed35c681c9de295de5a3113952be6930d82`;
- target PDF p37 SHA-256: `4cc7daa365563b0d311a717be38160aae6bb2f5f9a0b90fc3c5912190928ca9c`;
- target PDF p38 SHA-256: `245d405a924d802045427433a81622e2d14380c211e3ae54c4f6668b9382934a`;
- high-resolution renders: 3246 × 2868;
- workflow run `35950150138`;
- artifact `10787714159`, digest `sha256:8f39f4f257bfa5f3078be5ced33d45b34d7504c2b30968e693919424dbee47f9`.

OCR was used only to locate p38. All claims below are adjudicated from the source-bound page images.

## 3. p37 direct reading: the author-name conflict is internal

The entry directly reads:

    準齋心製几漏圖式一卷
    抄本

Its bibliographic header directly gives:

    孫逢古撰

The same header area also directly gives:

    文淵閣書目著錄

and the transmission note:

    從吳門黃氏藏舊抄本影寫

But the body of that **same entry** directly reads:

    由此逢吉以心法創茲小壺

This is the central result of 12EX:

    same 1887 printed entry:
        header = 孫逢古
        body self-reference = 逢吉

The variant therefore cannot be treated as two independently coherent author identities merely because both forms occur in later bibliography.

## 4. Author-variant adjudication

The direct sequence is now:

    1602 original-print bibliographic witness -> 孫逢吉
    1605 catalog-text witness              -> 孫逢吉
    1887 bibliographic header              -> 孫逢古
    1887 same-entry operational body       -> 逢吉

Adjudication:

    孫逢古
      = LATE_BIBLIOGRAPHIC_OR_RECENSIONAL_VARIANT/CORRUPTION
        STRONGLY_SUPPORTED
        NOT_ABSOLUTELY_PROVED

This is deliberately not converted into silent normalization. The graph preserves `孫逢古` as a real received variant.

The evidence materially favors `孫逢吉` as the more stable earlier reading, but a future primary witness may still refine the mutation point.

## 5. p38 direct mechanism replay

The 1887 physical print directly preserves:

    凡晝夜百刻節序短長
    分界定數二十五箭
    如冬至後自第一箭順數用之
    夏至後自二十五箭逆數用之
    卻依日曆參照節候

This independently replays the received operating architecture already read in the 1823 Huang-family manuscript reproduction.

One small wording variant is explicit:

    1887: 分界定數二十五箭
    1823: 分界定數二十有五箭

Therefore:

    operational mechanism identity = CLOSED AT RECEIVED-TEXT LEVEL
    exact character-for-character text identity = FALSE

The variant is preserved rather than normalized away.

## 6. Huang-family source-copy firewall

The 1887 entry directly says:

    從吳門黃氏藏舊抄本影寫

That is strong transmission-route evidence, but it does not by itself prove that the source behind the 1887 statement is physically identical to the NLC-held Daoguang-3/1823 Huang Shiliju manuscript reviewed in Batch 12DV.

Therefore:

    1887 Huang-source route == 1823 reviewed manuscript
        = NOT_PROVED

No independent stemmatic vote against the 1823 manuscript is added.

## 7. Chronology and identity firewall

The following remain separate:

    1887 printed bibliographic witness
        != Song physical witness
        != Yuan physical witness
        != securely pre-1578 exact 25-arrow prose
        != 1281 Yanling Sun Fengji identity

The late header attribution cannot prove composition in the Song. The Yuan/Shoushi composition hypothesis remains separately supported by the mechanical and 1551 bridge evidence, not by this 1887 header.

The historical person identity remains:

    1281 嚴陵孫逢吉 == 準齋作者
        = POSSIBLE_NOT_PROVED

## 8. Transmission-genealogy consequence

Batch 12EX adds:

- `PHYSICAL-COPY-AIRIJINGLU-LINGFENGE-1887-V5`;
- `PASSAGE-AIRIJINGLU1887-ZHUNZHAI-FENGGU-FENGJI-25ARROW`;
- `TG-E0102`: the 1887 physical print **ATTESTS** the internal author-variant and operational passage.

The Zhunzhai rule-family node now records the header/body author conflict and the received-text mechanism replay.

## 9. Sanming and product firewall

The 1887 passage preserves the Zhunzhai 38↔62 mechanism family, not the Sanming/Yueling 59/41 target fingerprint.

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

## 10. Next gate

1. Trace `孫逢古` backward through 《鐵琴銅劍樓藏書目錄》、黃丕烈題跋及其他清代書目，定位最早可見的 mutation layer.
2. Seek a direct physical Huang-family paratext that can bind the 1887 `從吳門黃氏藏舊抄本影寫` statement to a specific manuscript.
3. Continue the Yuan person-title identity bridge.
4. Continue the securely pre-1578 exact 25-arrow prose search and the independent Sanming/Yueling Dahan/Rainwater + Nanjing-59 search.

Research record: `docs/research/ZIWEI-AIRIJINGLU1887-ZHUNZHAI-AUTHOR-VARIANT-AND-25ARROW-REPLAY-R1.json`.
