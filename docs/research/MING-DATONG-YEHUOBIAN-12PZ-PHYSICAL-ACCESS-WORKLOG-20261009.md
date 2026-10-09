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


## Follow-up source-navigation check: NLC 411999003250 original-20v physical fascicle 10

- [Wikimedia Commons / NLC scan](https://commons.wikimedia.org/wiki/File:NLC892-411999003250-383067_%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8_%E2%96%A1%E2%96%A1%E5%8D%B7_%E7%AC%AC10%E5%86%8A.pdf) is expressly a **145-page, 44.32 MB** scan of an **old manuscript**, fascicle **第10冊**, carrying **卷十八／卷十九／卷二十**. Commons' hand-entered section hyperlinks take the browser to PDF page **1**, **80**, and **136**, respectively. These are **navigation bookmarks**, not independently checked exact physical title-page positions.
- [Page 136 thumbnail/viewer](https://commons.wikimedia.org/w/index.php?page=136&title=File%3ANLC892-411999003250-383067_%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8_%E2%96%A1%E2%96%A1%E5%8D%B7_%E7%AC%AC10%E5%86%8A.pdf) was successfully opened as a **PDF-derived page image**. The visible page contains unrelated continuous vertical manuscript narrative; **no clear 卷二十 title-page header nor 〈改造漏刻〉 target was identified** on this *one* page. Do not convert the link bookmark into a verified printed/handwritten folio beginning.
- The Wikimedia original PDF link is a 46,469,798-byte object rejected by the current public web-PDF retrieval path as above the size limit. Attempts to display the site-generated 960-pixel **pages 80 and 137** timed out; attempts to open pages **140 and 145** failed. These are **current tool access outcomes, not evidence of missing textual content**. PDF source digest is **NOT_COMPUTED**; page-136 thumb digest is also **NOT_COMPUTED**. There was no systematic 145-page folio inspection and no full-heading negative search.
- **Useful precise next acquisition plan:** use Commons' page parameter on the **original-twenty-volume item**, first validate both end/start of each volume with visible headings, then search the actual manuscript's article/subject transition by short targeted page groups. Keep the 1827/30v regrouped section independently identified and never reuse this PDF's page 136 as a locator for 30v 卷二十.
- **Result state:** `ORIGINAL_20V_FASCICLE10_NAVIGATION_BOOKMARKS_CONFIRMED`; `ORIGINAL_20V_TARGET_HEADING_TO_LEAF=UNRESOLVED`; `PAGE136_TARGET_GLYPH=NOT_OBSERVED_IN_REVIEWED_PAGE`; `WHOLE_DOCUMENT_NEGATIVE_CLAIM=FORBIDDEN`; `PRINTED_1827_TARGET_GLYPH=UNRESOLVED`. Batch 12PZ is still open; no independent manuscript target witness and no source-level numeric/官宮 glyph judgement added. Audit matrix/graph/implementation/runtime remain unchanged.


## Corrective direct visual collation: old-20v NLC fascicle 10 volume headings (forward-only)

**Evidence upgrade (NOT TARGET LEAF):** The 2026-10-09 previous worklog recorded Commons navigation bookmarks at PDF pages 1/80/136, expressly warning that they were not independently verified physical starts. This *later* targeted visual inspection now resolves the actual manuscript volume-heading positions as **PDF pages 1/81/137**. Preserve the original access observations above as a historical worklog; do not silently overwrite them.

| Manuscript object | Commons navigation bookmark (not a source reading) | **Directly read physical heading**, 1-based PDF page | Physical text visible in rendered source-derived image |
| --- | ---: | ---: | --- |
| 411999003250 fascicle 10 / 卷十八 | 1 | **1** | 萬曆野獲編卷十八 (visible at right-hand vertical heading) |
| 411999003250 fascicle 10 / 卷十九 | 80 | **81** | 萬曆野獲編卷十九 (heading at right/left image leaf top); page 80 has preceding continuing prose, and page 79 contains an unrelated heading 奪工部 |
| 411999003250 fascicle 10 / 卷二十 | 136 | **137** | 萬曆野獲編卷二十 (heading at left image leaf top); page 136 contains preceding continuous prose |

**Verified image-derived references:** [page 1](https://commons.wikimedia.org/w/index.php?title=File%3ANLC892-411999003250-383067_%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8_%E2%96%A1%E2%96%A1%E5%8D%B7_%E7%AC%AC10%E5%86%8A.pdf&page=1), [page 79](https://commons.wikimedia.org/w/index.php?title=File%3ANLC892-411999003250-383067_%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8_%E2%96%A1%E2%96%A1%E5%8D%B7_%E7%AC%AC10%E5%86%8A.pdf&page=79), [page 80](https://commons.wikimedia.org/w/index.php?title=File%3ANLC892-411999003250-383067_%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8_%E2%96%A1%E2%96%A1%E5%8D%B7_%E7%AC%AC10%E5%86%8A.pdf&page=80), [page 81](https://commons.wikimedia.org/w/index.php?title=File%3ANLC892-411999003250-383067_%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8_%E2%96%A1%E2%96%A1%E5%8D%B7_%E7%AC%AC10%E5%86%8A.pdf&page=81), [page 136](https://commons.wikimedia.org/w/index.php?title=File%3ANLC892-411999003250-383067_%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8_%E2%96%A1%E2%96%A1%E5%8D%B7_%E7%AC%AC10%E5%86%8A.pdf&page=136), [page 137](https://commons.wikimedia.org/w/index.php?title=File%3ANLC892-411999003250-383067_%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8_%E2%96%A1%E2%96%A1%E5%8D%B7_%E7%AC%AC10%E5%86%8A.pdf&page=137). Inspecting the Wikimedia Commons **PDF-derived 960-pixel rendered thumbnails**, without OCR, was sufficient to read the three volume headings. The file-level bibliography is the [National Library of China manuscript fascicle 10](https://commons.wikimedia.org/wiki/File:NLC892-411999003250-383067_%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8_%E2%96%A1%E2%96%A1%E5%8D%B7_%E7%AC%AC10%E5%86%8A.pdf), 145 PDF pages, not a separately identified 1827 printed copy. These are **physical-heading / document-navigation attestations**, NOT target 《改造漏刻》 text glyph attestations. Original PDF bytes and image SHA-256 digests were not acquired in this session: **DIGEST_NOT_COMPUTED**.

**Critical scope clarification:** An earlier viewer failure on PDF page 137 and uninspected page 81 must *not* be construed as negative visual proof. We have now directly viewed these page images, superseding previous `not yet reviewed` observations. The website's links for 卷十九/卷二十 are each **one PDF page earlier** than the page on which the explicit manuscript volume heading appears. This is a site-bookmark offset, **NOT** proof that the original scribal text is shifted/missing, nor a source-transmission variant.

The first page of 卷二十 (PDF p137) begins unrelated literary/biographical narrative; it is **not** the 〈改造漏刻〉 target. Attempts to inspect p138/p140/p143/p145 through this public viewer were inaccessible or timed out, and **no complete p137–145 exclusion/absence claim is made**. Physical old-20v `改造漏刻` heading-to-leaf, 官漏/宮漏, 北京冬至日出一/二 remain **UNRESOLVED**. Under the already-collated 1447 official report, `辰初一刻` is source-scoped to that 1447 record only; does not prove either source glyph for later received 30v 《野獲編》.

**Result:** source-identified old-20v volume heading positions closed at navigation level; target-leaf collation, 1827 Fuli edition page, printing/copy relationship and historical clock realization all remain open. Batch 12PZ still in progress; no new independent *target passage* witness, no Matrix/graph/candidate/runtime/algorithm change.

## New cross-region holding routes: 1700-catalog Korean woodblock / Hokkaido 1827 / CADAL 23 fascicles

This is **bibliographic and image-access route discovery**, not 〈改造漏刻〉 physical target collation. The [Korean National Digital Library record](https://www.dlibrary.go.kr/content/viewDetail.do?master_bib_no=21559119) explicitly reports `野獲編`, `[刊寫者未詳]`, year `1700`, an old-book object; its [NL digital-surrogate catalogue](https://commons.wikimedia.org/wiki/File:CNTS-00047974753_10_%E9%87%8E%E7%8D%B2%E7%B7%A8.pdf) scopes the surviving holding to **木板本(中國) / 18卷12冊**, KOL000010372 / CNTS-00047974753, with separate 12 surrogate fascicles. The year is **catalog-assigned**, not target-page-verified impression year; 18v is neither 20v manuscript nor regrouped 30v by default.

A **new distinct 1827 physical holding locator** appears in [Hokkaido University / CiNii BB10385966](https://ci.nii.ac.jp/ncid/BB10385966): `扶茘山房 道光七年 [1827]` 30巻+補遺4巻, with **卷19-20 bound together at 史6-2/YA/2, item 0181427762**. The catalogue documents 姚祖恩's dated `校刋野獲編` preface, 扶茘山房版心 and 10行21字 print format. This is an independent named **holding**, not yet an independent visibly collated target passage, and must not be conflated with the Kyoto or Tokyo copies.

[Wikimedia Commons' 82-object `野獲編` category](https://commons.wikimedia.org/wiki/Category:%E9%87%8E%E7%8D%B2%E7%B7%A8) additionally identifies two parallel CADAL image series (02096900–02096922 and 02112247–02112269), each labeled with 23 fascicle numbers. [CADAL02096919](https://commons.wikimedia.org/wiki/File:CADAL02096919_%E9%87%8E%E7%8D%B2%E7%B7%A8%EF%BC%88%E4%BA%8C%E5%8D%81%EF%BC%89.djvu) = 77 pages, Commons SHA1 da6bd71dc31801b70572eb4aff16792f93234096; [CADAL02112266](https://commons.wikimedia.org/wiki/File:CADAL02112266_%E9%87%8E%E7%8D%B2%E7%B7%A8%EF%BC%88%E4%BA%8C%E5%8D%81%EF%BC%89.djvu) = 77 pages, Commons SHA1 dc07d0ea84a7f20c9baca2944a411a583664cdc5. **Two digital file checksums or item numbers do not prove independent source copies.** CADAL `(二十)` is a file/fascicle label, not validated original 20v `卷二十` or classified 30v `卷二十`. Wikimedia rendering timed out; no source target leaf or imprint has been seen.

Three smaller [1959 中華書局 NLC modern printed objects](https://commons.wikimedia.org/wiki/File:NLC511-023031404016661-24957_%E8%90%AC%E6%9B%86%E9%87%8E%E7%8D%B2%E7%B7%A8_%E4%B8%AD%E5%86%8A.pdf) are **modern edition reception routes**, not original woodblock/1827 physical-glyph votes. They are not to be promoted from smaller file size to stronger historical authority.

No direct target page, original folio, title, `官/宮` or `一/二` text has been newly physically collated in this section. The machine log with copy/fascicle distinction and inference firewalls is `docs/research/MING-DATONG-YEHUOBIAN-12PZ-NEW-INDEPENDENT-HOLDING-ROUTES-R1.json`. Batch 12PZ remains in progress; Matrix/current-state/graph/runtime unchanged.


## Received-text four-field dependency probe: winter sunrise, summer sunset and clock nouns

**Scope:** received online transmission vs already-verified 1447 official physical report. This is **NOT** a new original-20v or 1827 image witness. Search evidence: [Shidian full target](https://www.shidianguji.com/book/NA09843/chapter/1lwjva2l98soe), [Wikisource categorized v20 target](https://zh.wikisource.org/wiki/萬曆野獲編/卷20), [CText target indexed excerpt](https://ctext.org/wiki.pl?chapter=418967&if=gb). The direct CText page was HTTP 403 in this session; the indexed excerpt is **OCR/user transcription, not a verified physical page**.

| Field | 1447 `明英宗實錄` physical p28 (previous Batch 12CF) | Shidian received | Wikisource received | CText OCR/index received |
| --- | --- | --- | --- | --- |
| 北京冬至日出 | 辰初**一**刻 | 辰初**一**刻 | 辰初**二**刻 | 辰初**二**刻 |
| 北京夏至日入 | 戌初**一**刻 | 戌初**一**刻 | 戌初**一**刻 | 戌初**二**刻 |
| 今宮禁/官禁及官府漏箭 | **宮**禁 | **宮**禁 | **宮**禁 | **官**禁 |
| 禁中宮漏/官漏 | **not present in the 1447 court memorial** | **宮**漏 | **宮**漏 | **官**漏 |

The **second numerical variant (summer 戌初一/二)** is a new collation discriminant not covered by the earlier 12PZ winter-only table. It prevents a simplistic grouping of received texts into just two edition lineages. CText's simultaneous 官禁 and 官漏 renderings might reflect correlated OCR glyph substitution or an editorial copying pathway; **no causal finding or direct-transmission edge is established**. Any correction of digital 二 to 一 requires edition-identified physical target text rather than automatic substitution of earlier official wording. A 1447 source-level value cannot settle a distinct later-Ming writer's physical textual recension.

**Failed acquisition boundaries this session:** source PDF for NLC original-20v no.411999003250 fascicle 10 remains 44.32MB / 145 pages and was rejected by the web PDF reader; direct container network cannot resolve upload.wikimedia.org; original PDF SHA256 **not computed**. Nagoya 2019/2020 version-study PDFs returned HTTP 429 in this session. This means **unavailable by current tools**, not historically missing passage. Sampled volume-title pages 1/81/137 from the earlier 12PZ work remain physically identified but do **not** locate 改造漏刻.

Next: compare four-field *physical* readings of an identified old-20v manuscript copy and a separately identity-bound 1827 30v printed copy; attach source digest, page and original folio. Research proof registry: `docs/research/MING-DATONG-YEHUOBIAN-12PZ-FOUR-FIELD-RECEIVED-COLLATION-R1.json`. No Matrix, state, genealogy, historical candidate/runtime or deterministic chart reopen.
