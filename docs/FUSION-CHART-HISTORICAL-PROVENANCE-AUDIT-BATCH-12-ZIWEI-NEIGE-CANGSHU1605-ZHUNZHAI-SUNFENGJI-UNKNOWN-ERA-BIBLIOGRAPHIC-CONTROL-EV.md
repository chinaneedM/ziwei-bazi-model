# Fusion Chart Historical Provenance Audit R1 — Batch 12EV

## 1605《內閣藏書目錄》直接閉合《準齋几漏新式》—孫逢吉—莫詳時代書目控制

Status: **MING 1605 CATALOG-TEXT TITLE/AUTHOR/UNKNOWN-ERA CONTROL CLOSED / 準齋几漏新式一冊 + 孫逢吉著莫詳時代 DIRECTLY READ ON SOURCE-BOUND P105 / REVIEWED COPY IS NOT TREATED AS A 1605 ORIGINAL / 九漏≠几漏 AND 新式≠圖式 REMAIN VARIANT-SCOPED / YUAN 1281 PERSON IDENTITY STILL POSSIBLE_NOT_PROVED / PRE-1578 EXACT 25-ARROW PROSE STILL OPEN / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12EU closed a 1602 original-print bibliographic pairing:

    準齋几漏圖式一卷 / 孫逢吉

It left two immediately valuable questions open:

1. whether another Ming bibliographic text independently preserves the same author name;
2. whether an early catalog itself claims a historical era for that author.

The next remote probe therefore targeted 《內閣藏書目錄》 rather than extending the deterministic chart runtime.

## 2. Source binding

The reviewed source-bound object is:

- 《內閣藏書目錄》八卷, 明孫能傳、張萱等撰;
- catalog-text compilation event: 萬曆三十三年 / 1605;
- public file: `NLC892-1084-204844 內閣藏書目錄 第2冊.pdf`;
- provider route: National Library of China digitization via Wikimedia Commons;
- source PDF SHA-256: `7d0ff9994a0a49c41e7ab287e5c355c343ffbd80573ce1aac69491b2e4639a43`;
- target: PDF p105;
- p105 SHA-256: `b71944e1baa0c86a9801e441779b4d1f57956062f58cf35d39418e9304675db0`;
- render size: 8117 × 6971;
- workflow run `35784888865`;
- artifact `10718814910`, digest `sha256:39ea2d7d7cc8612917cc4e14757e69f47cc2666cdaea0a7ecdc6d3ddb96c60a9`;
- extraction commit `f014a8872a6ec7ca8ced7d8dcf3030081acf9af4`.

Final glyph adjudication is direct image review. OCR is not used as authority.

The exact date/recension identity of the reviewed physical copy behind this public scan is not closed in this batch. The 1605 date belongs to the catalog-text compilation event and must not be silently converted into a 1605 surviving-copy date.

## 3. Direct physical reading

PDF p105 directly reads:

    準齋几漏新式一冊

The attached annotation directly reads:

    孫逢吉著莫詳時代

The next entry begins:

    皇極經世衍數四十八冊不全

This page-order control prevents the author/era annotation from being detached from the target title.

Adjudication:

    MING_1605_CATALOG_TEXT_TITLE_AUTHOR_UNKNOWN_ERA_CONTROL = CLOSED

## 4. What this changes

The Ming catalog-text layer now supplies a second nearby historical bibliographic control for the author name:

    1602 《國史經籍志》:
        準齋几漏圖式一卷 / 孫逢吉

    1605 《內閣藏書目錄》:
        準齋几漏新式一冊 / 孫逢吉著莫詳時代

The important new evidence is not merely the repeated name. The 1605 catalog explicitly says:

    莫詳時代

Therefore later assignments of the work/author to Song or Yuan cannot be projected backward as though the Ming 1605 catalog had already settled the person's era.

This does not disprove a Yuan attribution. It strengthens the existing identity firewall:

    1281 嚴陵孫逢吉 == 準齋作者
        = POSSIBLE_NOT_PROVED

## 5. Title-variant firewall

The currently source-bound title forms are kept distinct:

    1441 catalog-text family, surviving 1799 transmission:
        準齋九漏新式

    1602 original-print catalog:
        準齋几漏圖式一卷

    1605 catalog text, current source-bound copy:
        準齋几漏新式一冊

    1823 operational manuscript:
        準齋心製几漏圖式

No silent normalization is authorized:

- `九漏` is not automatically rewritten as `几漏`;
- `新式` is not automatically equated with `圖式`;
- title-family continuity is supported, exact text-state identity is not closed.

These variants are now explicit collation targets rather than editorial noise.

## 6. Chronology and physical-copy firewall

The following layers remain separate:

    1605 catalog-text compilation event
        != reviewed surviving physical-copy date
        != original Zhunzhai work-composition date
        != 1281 Yanling person identity
        != pre-1578 exact 25-arrow operational prose

The reviewed source proves what the transmitted 1605 catalog text says on p105. It does not prove the reviewed copy was written or printed in 1605.

## 7. Transmission-genealogy consequence

Batch 12EV adds:

- `PHYSICAL-COPY-NLC-NEIGE-CANGSHU-NLC892-1084-204844-V2`;
- `PASSAGE-NEIGE1605-ZHUNZHAI-SUNFENGJI-UNKNOWN-ERA`;
- `TG-E0099`: physical copy **ATTESTS** the p105 passage;
- `TG-E0100`: the 1605 passage **PARALLEL_COEXISTS_WITH** the 1602 Guoshi bibliographic passage.

The parallel edge records coexistence and convergent author naming only. It does not assert independent stemmatic voting or direct copying in either direction.

The Zhunzhai rule-family node gains a Ming-1605 bibliographic control, but no operational rule is backdated from a catalog entry.

## 8. Sanming and product firewall

This witness contains no Dahan/Rainwater numerical fingerprint, no Nanjing-59 endpoint rule, and no deterministic birth-time mapping.

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

1. Collate additional physical recensions of 《內閣藏書目錄》 and 《文淵閣書目》 for `九/几` and `新式/圖式` stability.
2. Seek a Yuan or otherwise identity-closing primary person-title bridge.
3. Continue searching for a securely pre-1578 carrier of the exact 25-arrow / winter-forward / summer-reverse / 日曆節候 prose.
4. Continue the independent Sanming/Yueling Dahan/Rainwater fingerprint and Nanjing-59 search.

Research record: `docs/research/ZIWEI-NEIGE-CANGSHU1605-ZHUNZHAI-SUNFENGJI-UNKNOWN-ERA-BIBLIOGRAPHIC-CONTROL-R1.json`.
