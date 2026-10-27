# Fusion Chart Historical Provenance Audit R1 — Batch 12EY

## 天一閣清抄本《鐵琴銅劍樓藏書目錄》直接閉合「孫逢古」與黃氏／蕘翁傳承線索

Status: **QING TIEQIN MANUSCRIPT FENGGU + HUANG/RAOWENG PROVENANCE CONTROL CLOSED / 準齋心製几漏圖式一卷 + 影鈔本 + 宋孫逢古撰并序 DIRECTLY READ / 郡中黃氏舊藏 + 蕘翁有跋 DIRECTLY READ / EXACT COPY YEAR UNRESOLVED / EARLIER MING 孫逢吉 CONTROLS RETAIN PRIORITY / NO SILENT NORMALIZATION / PRE-1578 EXACT RULE PROSE STILL OPEN / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12EX showed that the 1887 《愛日精廬藏書志》 itself is internally inconsistent:

    header -> 孫逢古撰
    same-entry body -> 由此逢吉以心法創茲小壺

The next gate was to determine whether `孫逢古` is confined to that one late printed surface or occurs in another Qing bibliographic transmission.

## 2. Source binding

The reviewed source is Tianyi Pavilion Museum's Qing manuscript of 《鐵琴銅劍樓藏書目錄》:

- census no. `330000-1705-0004561`;
- call no. `善2088`;
- five-volume Qing manuscript;
- exact manuscript copy year unresolved;
- source PDF SHA-256: `29d6774b33087ee8140d7141ca85bd60d25d1872bc636a33da35be9b75dbfc6f`;
- target p387 SHA-256: `984fe54f6a2ffd660594eac4fbb656b835921f6fd61ca700a201f7fe8ae156cb`;
- target p388 SHA-256: `8b150e774ad68e06bc81e53e3f8608b977f686055c479faa30b6d1ba2cb376b6`;
- 300-dpi render size: 3096 × 2768;
- workflow run `35952843891`;
- artifact `10789681401`, digest `sha256:6ab81cb019c423fd9842198e41b937ac1a104f83161b2ed5107c3cf1e42d544a`.

OCR failed on the handwritten scan and was not used for final glyph claims. Volume 15 was localized by direct structural contact-sheet review, then p386-p405 were rendered at 300 dpi.

## 3. Direct p387 reading

The entry directly reads:

    準齋心製几漏圖式一卷
    影鈔本
    宋孫逢古撰并序

The summary continues:

    逢古創為小壺
    分二十五箭
    按時而用
    以正晷刻
    可置坐隅
    故曰几漏
    因繪箭式而刻之
    曾著錄文淵閣書目
    是本與銅壺漏箭制度合裝

This independently closes `孫逢古` in the Qing Tieqin bibliographic text tradition.

## 4. Direct p388 continuation

The first columns of p388 directly continue the same entry:

    一冊
    郡中黃氏舊藏
    蕘翁有跋

The next title then begins 《大宋寶祐四年丙辰歲會天萬年具注曆》, so the Huang/Raoweng statement is physically bounded to the Zhunzhai entry.

## 5. Author-variant consequence

The direct evidence now separates cleanly:

    1602 《國史經籍志》 -> 孫逢吉
    1605 《內閣藏書目錄》 -> 孫逢吉
    1887 《愛日精廬藏書志》 header -> 孫逢古
    1887 same-entry body -> 逢吉
    Tianyi Qing Tieqin manuscript -> 孫逢古

Therefore:

    孫逢古 as a Qing bibliographic/recensional variant
        = CONFIRMED

and:

    孫逢古 as the original author name
        = NOT PROVED

The earlier Ming witnesses and the 1887 internal self-reference continue to make a late `逢吉 -> 逢古` mutation/corruption strongly plausible. The exact mutation point is still open, so automatic normalization remains forbidden.

## 6. Huang / Raoweng transmission route

The Qing Tieqin manuscript says:

    郡中黃氏舊藏
    蕘翁有跋

Batch 12EX separately read:

    從吳門黃氏藏舊抄本影寫

The operational manuscript reviewed in Batch 12DV is catalogued as a Qing Daoguang-3 Huang Shiliju manuscript.

These three lines strongly converge on a Huang-family/Raoweng transmission route, but they do not yet prove that all descriptions refer to the **same physical manuscript**.

Therefore:

    exact Huang-copy identity across Tieqin / Airijinglu / NLC 1823
        = NOT_PROVED

## 7. Chronology firewall

The Tianyi object is catalogued only as a Qing manuscript. Its exact copy year remains unresolved.

It must therefore not be used to claim:

- a pre-1827 date for `孫逢古`;
- a Song/Yuan physical witness;
- a pre-1578 physical carrier of the exact 25-arrow prose;
- exact identity of the 1281 Yanling Sun Fengji.

## 8. Transmission-genealogy consequence

Batch 12EY adds:

- `PHYSICAL-COPY-TIANYIGE-TIEQIN-QING-MS-0004561`;
- `PASSAGE-TIEQIN-QING-MS-ZHUNZHAI-FENGGU-HUANG-PROVENANCE`;
- `TG-E0103`: the Qing manuscript **ATTESTS** the Zhunzhai/Fenggu/Huang-Raoweng bibliographic passage.

The Zhunzhai rule-family node is strengthened only at author-variant and provenance-route level.

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

1. Directly collate an **1827 first-edition** 《愛日精廬藏書志》 target page, which can materially date the `孫逢古` bibliographic variant.
2. Bind the Huang/Raoweng paratext route to a specific physical manuscript if possible.
3. Continue the Yuan person-title bridge and securely pre-1578 exact 25-arrow prose search.
4. Continue the independent Sanming/Yueling Dahan-Rainwater + Nanjing-59 search.

Research record: `docs/research/ZIWEI-TIEQIN-QING-MS-ZHUNZHAI-FENGGU-HUANG-PROVENANCE-R1.json`.
