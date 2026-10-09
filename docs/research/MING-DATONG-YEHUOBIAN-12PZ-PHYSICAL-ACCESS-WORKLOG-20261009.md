# 12PZ in-progress physical-source access worklog — 2026-10-09

**Status: RESEARCH_IN_PROGRESS; NOT A COMPLETED BATCH.** This is an additive research worklog; it does not update the audit Matrix, source authority, graph edges, candidate selection, batch chronology or PROJECT-CURRENT-STATE. The latest *completed* batch remains 12PY until the physical target / access subtask is source-closed and its gates pass.

## Newly verified access routes

1. **Taiwan National Central Library 02260 / second PDF component**:
   https://commons.wikimedia.org/wiki/File:NCL-02260_2_%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8.pdf
   The public Commons object identifies a **35-page, 5.68 MB** second segment of the 02260 old-manuscript digital surrogate, separate from the 1,000-page / 179.47 MB first segment. Direct visual inspection of **PDF pages 2, 11, 18 and 35 (1-based PDF pages; sampled, non-contiguous)** succeeded through the public PDF screenshot route. The inspected leaves contain unrelated narrative text or ending material, not a positively identified 〈改造漏刻〉 target leaf. **No whole-file absence claim:** 31 other pages were not checked, nor has the original-20-volume heading-to-leaf concordance been established. The ability to render selected leaves proves only limited page-level access, not target glyph closure.

2. **Shanghai Library 30-volume scan route**:
   https://commons.wikimedia.org/wiki/Category:%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8
   This public inventory enumerates *Shanghai 萬曆野獲編三十卷* in three separate surrogate objects: part 1 = 550 pages / 301.06 MB; part 2 = 550 pages / 169.03 MB; part 3 = 357 pages / 59.38 MB. Part 2:
   https://commons.wikimedia.org/wiki/File:Shanghai_%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8%E4%B8%89%E5%8D%81%E5%8D%B7_part_2.pdf
   Commons attributes these physical images to Shanghai Library, but the public file-level label by itself does **not** prove this scanned copy is exactly the Daoguang-7 (1827) 扶荔山房 impression. No target folio or colophon has been visually checked for these three files in this worklog. The very large source object was not retrieved in the current web PDF reader. Maintain **EDITION_IDENTITY_UNVERIFIED**, **TARGET_LEAF_UNVERIFIED**, **NO_INDEPENDENT_GLYPH_VOTE**.

3. **Received-text numeric/lexical variants, not physical witnesses**:
   - Wikisource, modern organized volume 20 / 改造漏刻: https://zh.wikisource.org/wiki/%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8/%E5%8D%B720 — received digital text reads the Beijing winter sunrise as **辰初二刻** and the palace-clock sentence as **禁中宮漏循用新製**.
   - Shidian, received chapter page: https://www.shidianguji.com/book/NA09843/chapter/1lwjva2l98soe — received digital text reads Beijing winter sunrise **辰初一刻** and **禁中宮漏，循用新制**.
   - These two web transcriptions disagree on a potentially operational Beijing winter ke value; this is an **additional received-text collation target**, not yet a verified edition-specific historical numerical variant. Distinct web pages cannot be counted as independent physical copies. Existing 12PW CText 官漏/宮漏 observations also remain unresolved without target-page images.

## Evidence / scope firewall

- A 30-volume **categorized** 卷二十 heading does not locate 〈改造漏刻〉 in any particular 20-volume **old** manuscript.
- Visible PDF samples outside a target page do not authenticate the target glyph and are not negative proof of absent chapter.
- A Shanghai Library scanned 30-volume object is not automatically the 1827 Kyoto/Tokyo printed copy.
- Received digital variants (宮漏/官漏, 辰初一刻/二刻) are collation prompts, not mechanical rule or transmission-lineage verdicts.
- 1447 *order* to rebuild, retrospective later-Ming claim of adoption and the 1450 court's corrected eclipse clock reading must remain three distinct evidence propositions.
- No new Jingtai-1 actual observer, clepsydra, absolute time, solar longitude or realization formula is established.
- **MD-G03** remains OPEN_BLOCKING_GENERAL_ADAPTER; **HPA-DAYUN-CAL-002** remains MISSING_FROM_PRODUCT; historical runtime remains fail-closed; deterministic R1 remains CLOSED.

## Exact next proof obligation

Find the literal 〈改造漏刻〉 heading and line span on a **specific 20-volume manuscript copy**; record physical volume/folio, PDF 1-based page, source URL and digest, and transcribe 官/宮及日出刻 on that *physical target* image. Separately visually inspect a **source-identified printed 30-volume copy**'s 卷二十 target leaf and its edition/colophon, before making a copy-to-copy comparison. Until then **12PZ is open**.

This worklog changes **no** historical Matrix counts, candidate registry, provenance defect tally or transmission graph edge. It is not evidence of an implementation defect or authorization to reopen charting algorithms.


## New higher-priority textual collation control: 1447 official report vs received 《野獲編》

The existing **physically inspected** NLC/Wikimedia 《明英宗實錄》 卷160, 第16冊, PDF **p28** (12CF's original image SHA-256 `b7d95f00fd529468c4242f60b7255b5305df6298d14841a9d9f6ac03eccccfea`, PDF SHA-256 `1e9546177289930ae33a64793df94518fcc21c90184c935a30ea975461990268`) records the **1447 正統十二年十一月甲寅 official Peng Deqing memorandum** with:

- **北京冬至日出辰初一刻**; 北京夏至日出寅正二刻; 夏至日入戌初一刻.
- 南京冬至日出辰初初刻; 南京夏至日出寅正四刻; 夜/晝刻五十九, versus Beijing 六十二.
- **今宮禁及官府漏箭皆南京舊式不可用；上令內官監改造**.

The physical *一刻* reading was already recorded in `docs/research/ZIWEI-YINGZONG-SHILU-1447-NANJING-59-41-PHYSICAL-COLLATION-R1.json`; **it is NOT a newly acquired independent physical witness**.

| Witness/read route | 北京冬至日出 | 官/宮 reading | Evidence level |
| --- | --- | --- | --- |
| 1447 《明英宗實錄》卷160, NLC PDF p28 / Batch 12CF | 辰初**一**刻 | 宮禁及官府漏箭 | Direct physical page; earlier official record, already counted |
| [Shidian received 《明英宗實錄》](https://www.shidianguji.com/zh/book/LS0026/chapter/1k6qy33meo3za) | 辰初**一**刻 | 宮禁及官府漏箭 | Digital received transcript, not additional physical vote |
| [Shidian received 《萬曆野獲編·改造漏刻》](https://www.shidianguji.com/book/NA09843/chapter/1lwjva2l98soe) | 辰初**一**刻 | 禁中**宮**漏循用新制 | Digital received transcript; underlying edition not physically bound |
| [Wikisource received 《萬曆野獲編》卷20](https://zh.wikisource.org/wiki/%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8/%E5%8D%B720) | 辰初**二**刻 | 禁中**宮**漏循用新製 | Digital normalized text; no source-copy identity |
| [CText user/OCR transcribed 《野獲編·十六v19~20》](https://ctext.org/wiki.pl?chapter=418967&if=gb) | 辰初**二**刻 | 禁中**官**漏循用新制 | User/OCR derivative, not physical glyph authority |

**New witness-dependency control:** the CText `十六v19~20` page itself explicitly states that its transcription was prepared using **《看典古籍》 OCR** and includes `秀水沈德符景倩著　桐鄉錢枋爾載輯`. Its visible volume 20 classification (言事/京職/曆法) belongs to the **reorganized categorized 30-volume line**, *not* a sourced original-20-volume leaf. Thus CText and Shidian cannot be counted as independently collated old-manuscript evidence by virtue of different domain names. The named editorial collaboration/derivation also blocks treating a CText page named "十六v19~20" as a verified original twenty-volume witness.

**Decision:** A 1447 physically attested official `一` and later electronic `一` / `二` readings prove a **textual collation problem**. The received `二` is **not authorized** as an independent historical clock value or a corrected 1447 value; equally, the late-Ming physical 《野獲編》 `二` vs `一` glyph cannot be declared a copying error until the exact physical leaves are obtained. Never back-project later digital `二` into the 1447 memorial. Do not claim 1447 official `一` mechanically adjudicates the physical 《野獲編》 quotation.

This strengthens the 12PZ proof obligation: visually bind **both** the `一/二` numeric character and `官/宮` character on a **specific 《野獲編》 old manuscript leaf and on a specifically identified 30-volume printed leaf**; record collation provenance, PDF page, edition, source digest. It does **not** close `12PZ`, alter Matrix totals, establish an instrument/observer for Jingtai-1, select an adapter or authorize runtime.
