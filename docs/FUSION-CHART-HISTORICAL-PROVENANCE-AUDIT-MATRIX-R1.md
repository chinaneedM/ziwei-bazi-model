# Fusion Chart Historical Provenance Audit Matrix R1

## State

```text
FUSION_CHART_HISTORICAL_PROVENANCE_AUDIT_R1=IN_PROGRESS
HISTORICAL_PROVENANCE_INVENTORY=COMPLETE
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

Baseline branch: `agent/fusion-chart-core-r1-20260822`  
Baseline HEAD: `9bf1f4f82d5c43b40fad29bd3d0a210fae4ed9ec`  
Baseline tree: `3a83f5da19144a448371686311ea66cdf5ccb8e8`

This stage audits **why every deterministic chart-affecting rule exists, which text/school/version supports it, how competing methods differ, and whether the released implementation actually matches its cited source**. It does not reopen a closed algorithm merely because a historical audit has started.

## Matrix contract

Machine-readable source of truth: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json`.

Every row carries:

- rule ID and module/system;
- current implementation and current profile;
- primary source route;
- verbatim quote slot and exact source location;
- historical period/version slot;
- later witnesses and school attribution;
- competing methods;
- implementation-match result;
- confidence;
- audit status;
- proposed action;
- explicit algorithm-reopen authorization, which is **false for every inventory row at creation**.

The initial inventory contained **107 rule/field families**. After Batches 01–12E and explicit splitting of historically distinct candidate families, the current machine-readable inventory contains **198 rows**, with **166 audited rows**. It intentionally keeps unresolved source work explicit rather than converting uncertainty into a chart defect. The current audit ledger records **9 confirmed provenance metadata defects repaired forward-only at the provenance/hash-lineage layer, 0 chart algorithm defects, 0 algorithm reopens, 14 cumulatively identified missing candidate families, 10 rows currently `MISSING_FROM_PRODUCT`, 6 historical candidate extensions, 3 source-scoped historical candidate registries, and 3 runtime-resolver components**.

## Research-corpus authority

S00–S19 are now explicitly classified as the **project research corpus**, not as
infallible historical authority. The repository path `sources/canonical/` retains
its legacy storage/freeze meaning only. For historical claims, each S00–S19 rule
must be traced to the underlying witness it actually contains or cites, and that
witness remains externally auditable.

Accordingly:

- an S-number alone cannot close a historical claim;
- internal transcription, attribution and normalization can be wrong;
- a stronger edition-specific or bibliographic witness may refine or contradict
  the project corpus;
- conflicting historical witnesses remain scoped candidates rather than being
  collapsed to whichever rule happened to be in S00–S19 first;
- modern software remains compatibility evidence only.

The governing policy is
`docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md`.

## Allowed audit statuses

- `HISTORICALLY_SUPPORTED`
- `SUPPORTED_BUT_SCHOOL_SPECIFIC`
- `DISPUTED_MULTIPLE_CANDIDATES`
- `MODERN_COMPATIBILITY_ONLY`
- `SOURCE_INSUFFICIENT`
- `IMPLEMENTATION_REVIEW_REQUIRED`
- `MISSING_FROM_PRODUCT`
- `NOT_YET_FORMALIZED`

## Reopen gate

A deterministic rule may be locally reopened only when all of the following are bound in the matrix:

1. exact primary or high-quality historical evidence;
2. edition/date/location and verbatim text;
3. school attribution and competing-method classification;
4. a reproducible mismatch between that rule and the released implementation;
5. defect scope limited to the affected rule/profile;
6. forward-only source/profile/tests/docs change.

Reference-product differences alone cannot authorize a reopen.

## Initial inventory findings

- Time/Calendar contains both modern astronomical/civil standards and doctrinal charting policies. These must not be conflated.
- Bazi late-Zi, Xiaoyun and several support/anchor questions are explicitly candidate-shaped and remain unranked.
- Bazi Dayun has a canonical-oriented profile plus a separately named Wenzhen compatibility realization; the compatibility profile is not historical authority.
- Ziwei production currently binds several `WENMO_DEFAULT_*` rule-set identities. Historical audit must determine, row by row, whether those bindings represent source-supported school rules, compatibility-only calibration, or a profile-labeling debt.
- Ziwei dynamic Kui/Yue preserves strict-source and Wenmo-compatible candidates; Tianma remains case-method-only.
- Ziwei flow-hour and self/inward transformation direction remain unresolved rather than fabricated.
- Structural R1/R2 are neutral computational geometry; historical claims start only when named source semantics are attached downstream.
- Combined Fusion/lineage/hashing are software provenance mechanisms, not classical doctrine.

## Module order

Historical research proceeds in evidence-risk order:

1. Time / Calendar doctrine-vs-modern-standard separation.
2. Bazi natal core + Dayun + Xiaoyun.
3. ShenSha source-by-source audit.
4. Ziwei natal stars / minor stars / dignity / four transformations.
5. Ziwei temporal layers and dynamic auxiliaries.
6. Structural R1–R8.
7. Combined Fusion lineage closure.
8. Final missing-product scan against audited historical rule families.

No winner is selected for a genuinely disputed school rule solely to simplify product output.


## Progress through Batch 11O

- Batch 01: Time / Dayun / Xiaoyun.
- Batch 02: Bazi natal / derived foundations; repaired Twelve-Growth and NaYin provenance metadata.
- Batch 03: Bazi ShenSha; repaired Yuancheng lineage and preserved source-scoped variants.
- Batch 04: Ziwei early-print core; registered the 1581 Jielan candidate family and isolated historically distinct Kui/Yue, Fire/Bell, dignity and Four-Transformation families.
- Batch 05: Ziwei roles / limits / rings; distinguished Jielan birth-year Mingzhu from received-Fullbook Life-palace Mingzhu, kept Zi/Wu Shenzhu unresolved, verified Daxian/Xiaoxian/Boshi geometry, repaired stale Jielan registry-version lineage, and added a source-scoped deterministic candidate runtime that remains `PRESERVED_NOT_SELECTED`.
- Batch 06: Ziwei natal foundations; promoted Life/Body placement, the twelve-palace sequence, Five-Tigers palace stems and the Life-palace NaYin bureau chain to direct received-text support, while quarantining the normalized Fullbook attribution for the 23:00 day-boundary sentence until edition/facsimile evidence closes it.
- Batch 07A: Ziwei minor-star decomposition; split eight independent minor-star families out of the broad R4 bundle. TianKu/TianXu, HongLuan/TianXi, LongChi/FengGe, TaiFu/FengGao, TianXing/TianYao and the year-based TianDe/JieShen geometry are directly received-text supported; TianChu and TianShou remain disputed candidates.
- Batch 07B: Ziwei early-print minor-star closure; added eleven granular families bound to the 1581 《新刻纂集紫微斗数捷览》 witness: TianGuan/TianFu, TianKong, Xun void-pair geometry, JieLu KongWang/JieKong, GuChen/GuaSu, JieSha, HuaGai, the TaoHuaSha→XianChi geometry/name bridge, DaHao, PoSui and TianCai. All eleven current placement geometries match the scoped witness; XunKong main/sub display ordering remains explicitly outside the 1581 claim, and TianShou remains disputed under 07A.
- Batch 07C: completed rule-family decomposition of the operational minor-star R4 bundle. LongDe is mechanically supported by the 1581 TaiSui-12 sequence; YueDe is a genuine historical split (巳-start family vs received-Fullbook 子-start family); standalone FeiLian plus month JieShen/YueJie, TianWu, TianYue and YinSha remain SOURCE_INSUFFICIENT rather than being upgraded from modern repetition. HPA-ZIWEI-008 therefore leaves IMPLEMENTATION_REVIEW_REQUIRED and becomes a fully decomposed SOURCE_INSUFFICIENT parent summary, with no chart-algorithm reopen.
- Batch 08A: Ziwei dynamic auxiliaries A; decomposed flowing LuCun/QingYang/TuoLuo, Chang/Qu, Kui/Yue and Tianma by temporal layer and authority class. Annual 流禄流羊流陀 has a received-Fullbook witness; Daxian/finer flowing-star rules and 流昌流曲/运马/流马 are explicitly Zhongzhou-school methods bound to Wang Tingzhi's modern manual. Wenmo Kui/Yue remains compatibility-only. The misleading runtime label CANONICAL_SOURCE_TABLE was repaired to S01_STRICT_PROJECT_CORPUS_METHOD with no coordinate or selection change (PROV-DEFECT-007).
- Batch 08B: Ziwei temporal frames B; applied the formal 训诂 method to distinguish wording identity from mechanical identity. Flow-year TaiSui palace, Five-Tigers month Ganzhi and flow-day palace geometry are historically supported. The 1581 Jielan `日上起子时` day-anchored hour method and the Zhongzhou leap-month `1–15 previous month / 16–end next month, day sequence continuous` method were source-closed here as two product gaps. Productization follow-up now closes both gaps through `ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-REGISTRY-R1`: the 1581 method is emitted only as a time-standard-specific-parent, replay-gated `PRESERVED_NOT_SELECTED` candidate; the Zhongzhou leap candidate emits month assignment plus `half_split_reset=false` but deliberately does **not** invent leap-month daily-origin geometry. The pre-existing fixed-branch hour candidates and production defaults remain unchanged; no algorithm reopen.
- Batch 08C: Ziwei time-standard decomposition. Wang Tingzhi's Luoyang/Zhongzhou time is preserved as a school-scoped **mean-solar** longitude standard; local apparent/true solar time is separately audited as a modern astronomical + modern Ziwei-practice candidate. USNO terminology confirms apparent solar time = mean solar time + equation of time. The two clocks remain unranked and orthogonal to the flow-hour active-palace method; no algorithm reopen.
- Batch 08D: decomposed Ziwei effective calendar date into two independent axes: Gregorian-date index basis and late-Zi chart-date boundary. `LOCAL_SOLAR_DATE_INDEXED` / `ABSOLUTE_CALENDAR` are modern operational date-index candidates; `ZI_START_23` / `MIDNIGHT` remain disputed Ziwei late-Zi candidates. The S01 sentence attributed to Fullbook stays quarantined, and 1581 Jielan `日上起子时` is explicitly barred from being misused as a 23:00 calendar-rollover witness. Combined runtime independence between Ziwei and Bazi day boundaries remains intact.
- Batch 09A: separated modern solar-term astronomy from Bazi doctrinal consumption. The 24-term apparent-solar-longitude realization remains `MODERN_COMPATIBILITY_ONLY`; received Bazi year-pillar switching at the exact Lichun instant, Jie-only month switching, and same-date before/after-交节 semantics are historically supported by Ming seasonal structure plus explicit later Ziping witnesses. No algorithm reopen.
- Batch 09B: closed the Bazi Dayun Ganzhi sequence independently of Jiaoyun timing. Explicit Ziping examples take the natal month pillar as sequence base, use the adjacent sexagenary pillar as formal Dayun #1 in the resolved direction, then advance one pillar per subsequent luck frame. Runtime `month_index ± index` matches exactly; no algorithm reopen.
- Batch 10A: audited neutral Bazi affinity/exposure projections and the raw relation core. Exact hidden-stem/same-element affinity remains a neutral identity projection rather than 通根/strength doctrine. Five stem combinations, six harmonies, six clashes, four standard trines, 相穿 and punishment geometries are historically supported. `穿/害` is recorded as a terminology bridge over one mechanical geometry, and the 无恩/恃势 label swap across received texts is preserved instead of normalized. A new source-closed candidate gap was identified: `辰戌丑未土局`, which must be modeled as an arity-4 four-earth bureau rather than forced into a three-member trine. No existing coordinate defect.
- Batch 10B: audited relation families intentionally excluded from the raw core. Ming `属象/一方之气` is normalized to the later `方/三会` mechanical groups without merging them with 三合. Song 《五行精纪》 preserves an early four-break method and explicitly excludes the later-added harmony pairs, so a universal six-break table remains disputed. Modern 半合/拱合 remains compatibility-only while the classical complete-trine boundary stays strict. Ming `座下自化` and later `干支暗合` close a same-pillar stem↔hidden-stem combination candidate. Three new source-closed product gaps were added; no existing algorithm reopened.
- Batch 10C: productized four source-closed Bazi relation families through `BAZI-HISTORICAL-RELATION-CANDIDATES-R1`, an opt-in `PRESERVED_NOT_SELECTED` sidecar: four-earth bureau, directional triads, early four-break, and same-pillar stem-hidden five-combination. Raw-core defaults remain unchanged. `PROV-DEFECT-008` repaired the 《命理探源》 relation-chapter source-ID scope.
- Batch 11A: decomposed hidden-stem membership from textual/display ordering. Received YHZP source order is historically attested; the repository normalized tuple remains lineage-only with no root-strength meaning; later `本气/余气` language is preserved as a distinct hierarchy concept rather than inferred from ordinal. Dynamic layers are confirmed to reuse the natal membership table. `PROV-DEFECT-009` moved dynamic hidden-stem order out of FactHash and into ComputationHash lineage, with no chart-coordinate change.
- Batch 11B: decomposed Dayun calendar realization from the already-audited Jie interval and three-days-one-year symbolic ratio. Song 《五行精纪》 and Ming 《三命通会》 close the discrete day/shichen conversion family at source resolution; the current microsecond ×120 mapping remains an engineering interpolation. 《三命通会》 also preserves explicit small-month/leap-month correction and ten-anniversary recurrence, while 《千里命稿》 preserves a distinct later calendar-age-plus-remainder-days method. These historical calendarized schedules remain source-scoped missing-product candidates until an edition/regime-aware historical-calendar adapter exists; modern `ChineseCalendarEngine`, Gregorian anniversaries and Wenzhen compatibility are not relabeled as classical calendar authority.
- Batch 11C: added the fail-closed `HISTORICAL-CHINESE-CALENDAR-ADAPTER-CONTRACT-R1`. The 1578 Ming `三命通会` context is researched against the Ming Datong calendar family, while the 1645 Shixian transition is registered as a distinct later regime boundary. The contract defines date mapping, Jiaoyun realization and calendar-year recurrence as required future operations, but implements no historical calendar arithmetic and explicitly forbids modern-Chinese-calendar fallback, cross-regime back-projection and implicit Gregorian anniversaries. HPA-DAYUN-CAL-002/003/004 remain `MISSING_FROM_PRODUCT`; no algorithm reopen.

- Batch 11D: upgraded the Ming Dayun historical-calendar evidence stack without pretending the adapter is executable. A 1569 Ming-period facsimile of Zhou Xiang's 《大明大統曆法》 now supplies a primary `步氣朔` method witness, while Taiwan NCL catalog evidence locates the exact 1578 `大明萬曆六年歲次戊寅大統曆` as a Ming Imperial Astronomical Bureau printed same-year oracle target. CAS/IHNS critical-collation guidance explicitly warns that the later 《明史·曆志》 Datong text differs from Ming official works and contains later alteration/recompilation. Because the 1578 month/leap/time values are not yet extracted and the exact arithmetic/clock/enforcement semantics are not fully collated, HPA-DAYUN-CAL-002 remains `MISSING_FROM_PRODUCT` and the adapter remains fail-closed; no algorithm reopen.

- Batch 11E: converted the 1578 Wanli-6 monthly oracle from prose research into a machine-replayable evidence fixture. 《明神宗顯皇帝實錄》 volumes 71–82 plus Wanli-7 volume 83 preserve the complete month-start Ganzhi chain `癸丑→壬午→壬子→壬午→辛亥→辛巳→庚戌→庚辰→己酉→戊寅→戊申→丁丑→丁未`; the mod-60 transitions reproduce month lengths `29/30/30/29/30/29/30/29/29/30/29/30`, total 354 days, with twelve consecutively numbered months and no leap month in the represented year. 《萬曆起居注》 independently corroborates multiple starts and within-month dates. This closes a target-year oracle layer only: the exact 1578 Qintianjian almanac images and general 1569 Datong arithmetic/clock semantics are still unclosed, so `HPA-DAYUN-CAL-002` remains `MISSING_FROM_PRODUCT`, the adapter remains fail-closed, and algorithm reopen remains 0.

- Batch 11F: adjudicated the Ming Datong D1/D2 conjunction conflict instead of preserving false equivalence. The 1569 Zhou Xiang primary facsimile itself, at `推加减差分法`, divides the correction by the matching lunar `迟/疾行度` (D1). Xing Yunlu's Ming `万历二十四年…〈大统〉` worked example independently divides by `迟行度`. The later Qing-compiled 《明史》 received text instead creates `定限度=迟疾限行度-820` (D2). A modern check against 56 conjunction times in six surviving Ming official Datong almanacs reports 56/56 D1 agreement and widespread D2 mismatch, including a wrong-day near-midnight case. Therefore D1 is now historically adjudicated as the Ming official production conjunction subrule; D2 remains a later received-text transmission variant, not an equal candidate. The general adapter still remains fail-closed pending complete 1569 table/carry transcription, 1578 replay, historical clock/day-boundary and multi-year semantics.

- Batch 11G: separated the Ming Datong **internal computational time coordinate** from its still-unresolved geographic realization. The 1569 Zhou Xiang facsimile directly gives `推合朔時刻法`: event `小餘` lives in a `日周一萬` day, the 12-shichen conversion is counted from `子正`, half-shichen labeling uses `子初`, and the received Datong text independently states `日周一萬=一百刻`. Xing Yunlu's Ming Datong worked example replays `定朔` small remainder to `乙丑日午正初刻`. Thus the historical astronomical/computational day boundary is now source-closed at `子正`; this is explicitly forbidden from being imported into Bazi/Ziwei astrological day-boundary policy. Geography is a separate axis: Ming records and international reconstructions show Nanjing/Beijing clock and sunrise-sunset tables differ, but the qishuo/conjunction meridian reference is not yet source-closed. The general historical adapter remains fail-closed.

- Batch 11H: completed a source-derived 1578 D1 target-year replay instead of merely comparing an oracle after the fact. Reconstructed 1569 solar 盈缩 and lunar 迟疾/D1 tables reproduce all twelve Wanli-6 month starts plus the Wanli-7 first-month anchor, 13/13 at day resolution with zero mismatch. The exact same-year NCL 06313 Qintianjian physical scan is now bound as an independent evidence layer: eleven of twelve month-calendar pages were directly rendered and all eleven visible 大/小 labels match the replay/oracle, while the June page remains an explicit renderer gap and is not inferred. A second exact-year Peking University copy (528.7/1578) is independently catalogued but not yet page-collated. This closes the target-year D1 replay milestone only; row-by-row 1569 collation, universal precision/carry, qishuo meridian, multi-year leap/recurrence semantics and historical-calendar runtime remain open. `HPA-DAYUN-CAL-002` stays `MISSING_FROM_PRODUCT`; algorithm reopen remains 0.

- Batch 11I: closed the sole remaining same-year physical-page access gap for NCL 06313 without rewriting Batch 11H's historical snapshot. Reopening the same Wikimedia PDF through a fresh page context allowed zero-based page 13 to render directly; the page visibly reads `六月小`. All twelve month pages are therefore now directly rendered and all 12 month identities / 大小 labels match the official-record oracle and D1 replay, with zero mismatch. This closes only the 1578 physical month-page identity/size layer: fine first-day Ganzhi glyph transcription, exact conjunction subday values, qishuo meridian, generalized fixed-point arithmetic, multi-year leap/recurrence behavior and executable historical-calendar runtime remain open. No chart algorithm defect, reopen or candidate collapse is introduced.

- Batch 11J: closed the **1569 primary table-generation fixed-point precision map** without pretending that one rounding function governs the whole calendar. Direct primary-ledger comparison gives day-rate floor 168/168 (78 rows discriminate against half-up), 損益捷法 truncation 168/168 (76 discriminate), 遲/疾行度 generic ceiling 334/334 with two central primary overrides (180 discriminate against half-up; floor matches 0/334), and 行度捷法 truncation 336/336 (178 discriminate). Solar three-difference and lunar accumulated/adjacent-difference relations are exact at their stored source precision. These incompatible stage-scoped operators reject a single global rounding rule. Xing Yunlu's 1596 `〈大統〉` worked example remains a local dynamic truncation control; his 1605 `〈授時〉` example preserves different intermediate precision widths and is used only as a cross-context warning, not as Datong production authority. Table-generation precision is closed for the 1569 primary, but dynamic interpolation/D1 precision generalization, cross-edition image causes, qishuo geography and executable historical-calendar runtime remain open. No chart algorithm defect or reopen is introduced.

- Batch 11K: established a native-resolution no-OCR evidence package for the NDL 1673 Ogawa witness. The solar D16 control is structurally non-comparable because the printed `太陽盈縮立成` schema has no separate 日差/消息分-type field; L114 directly reads `九日三四八九`. L8/L101/L132 remain NDL-copy split-place surfaces whose linear serialization is deliberately unforced. The earlier inability to identify a separate L124 field/table is explicitly scoped to the inspected NDL digital-volume sequence rather than generalized to every 1673 Ogawa holding. Kyushu University's independent same-year public IIIF holding was identified as the next direct-image route; no runtime effect.

- Batch 11L: completed direct no-OCR collation of the independent Kyushu 1673 Ogawa holding at exact workflow run `34010515542` / artifact `9982311056`. It independently repeats the D16 structural omission and L114=`九日三四八九`. Same-copy L8↔L159 and L35↔L132 controls preserve matching numeric glyph layouts after the expected 益/損 reversal, while L67↔L101 preserves a visible zero/place-group surface difference in a symmetric mechanical context, strengthening the rule that surface-string inequality does not imply mechanical inequality. Crucially, the separate `遲疾限行度` table prints a numeric layer matching the Ming-1569 reciprocal/捷法 layer rather than the raw 1e-4-degree 行度 layer: at L124 its printed derived pair is 疾 `0.0797587` / 遲 `0.0704164`, exactly corresponding to Ming raw `1.0281` / `1.1645`; the received Goryeosa raw `1.0821` counterfactual would yield `0.0757785`. This is therefore mechanically linked derived evidence supporting the Ming 1.0281 lineage, **not** a direct raw `1.0281` glyph. G893 and earlier transmission causality remain open; no chart algorithm or historical-calendar runtime is reopened.

- Batch 11M: resolved two prerequisites around the early Kyujanggak G893 witness without inventing a target value. First, copy chronology is now fail-closed: the live Kyujanggak provider dates the surviving 甲寅字 copy only to the first half of the 15th century / Sejong 1418-1450, while KOSTMA and Li 2018 report 1434 and Li's later 2022 numerical-table chapter cites collection no. 893 as printed in 1444. Therefore the exact surviving-copy print year is `UNRESOLVED_WITHIN_1418_1450_PROVIDER_RANGE`, and neither 1434 nor 1444 may be used as a numeric-variant tie-breaker. Second, Li 2023 Figure 1 is now bound as a public secondary reproduction of the actual Kyujanggak Shoushi-licheng object: it directly shows cover `授時曆`, `授時曆立成卷上`, `嘉儀大夫太史令臣王恂奉敕撰`, `太陽冬至前後二象盈初縮末限`, and the opening solar columns 初日–八日. This narrows the solar search to a later page containing 十六日 but does not bind D16, any lunar target, any exact folio token, or any target numeric value. All six G893 controls remain pending direct target-page reading; no runtime or algorithm effect.

- Batch 11N: established two **independent early-Joseon comparison routes** adjacent to, but explicitly not substituting for, G893. Kyujanggak directly catalogs `七政算內篇 奎貴894-v.1-3` as 李純之/金淡受命編, 甲寅字, **1444**, with original-image/original-text services; call-number adjacency `893/894` is forbidden as a genealogy inference. Separately, the National Institute of Korean History official `世宗實錄 卷156` service binds `太陽冬至前後二象盈初縮末限` to Taebaeksan `60冊 156卷 6張 A面` and `太陰限數遲疾度` to `60冊 156卷 13張 A面`, with an original-image route. These create a same-period official Joseon computational/received-table control for future cross-edition adjudication, but no D16/L8/L101/L114/L124/L132 target glyph has yet been read from G894 or Sillok. G894≠G893, Sillok≠G894 physical glyph surface, source count is not adjudication, and runtime/algorithm effect remains none.

- Batch 11O: directly collated five lunar controls from the National Institute of Korean History's official Taebaeksan native Sillok JPEGs, with no OCR. L8 reads `益一十〇分五六〇一七七五` (=10.5601775); L101 reads `五度二十〇四八一一二五` (=5.20481125) with explicit positional zero; L114 reads `九日三四八九`; L124 reads `疾一度〇二八一` (=1.0281); L132 reads `損七分八八六〇七五` (=7.886075). The evidence is mixed at cell level: L8 follows the Goryeosa received branch while L124 follows Ming 1569 / mechanically linked Ogawa evidence, so source-bloc voting is rejected. The directly bound solar 6A page does not contain D16; a physical-span transport probe and the official viewer next-node API walk were network-unavailable, so D16 remains pending and no guessed continuation filename/page/value is admitted. G894 and G893 remain independently pending; runtime and algorithm state are unchanged.

- Batch 11P: directly bound Kyujanggak `七政算內篇 奎貴894-v.1-3` to its live official digital object (`BOOK_CD=GK00894_00`, `ITEM_CD=GJB`) and closed five lunar controls from renderer-returned native-image pages with no OCR. G894's own `018a/041b` method text closes the six-column mechanics `限數 / 遲疾曆日率 / 損益分 / 遲疾度 / 疾曆限行度 / 遲曆限行度`: L8=`益一十〇分五六〇一七七五` (=10.5601775), L101=`五度二十〇四八一一二五` (=5.20481125), L114=`九日三四八九`, L124=`疾一度〇二八一` (=1.0281), and L132=`損七分八八六〇七五` (=7.886075). The solar D16 control is not assigned a value because G894's directly visible winter-solar schema prints `積日 / 盈縮加分 / 盈縮積` and structurally omits the active second difference/message-difference field. The cell-level evidence is again mixed—L8 follows the Goryeosa/Sillok branch while L124 follows Ming 1569/Sillok—so whole-copy variant inheritance and source-count voting remain forbidden. G894 remains separate from G893 and Sillok; runtime and algorithm state remain unchanged.

- Batch 11Q: closed the execution-environment access boundary around Kyujanggak G893 without reading or inferring any target value. Read-only G893 renderer probes now cover GitHub-hosted Ubuntu, macOS and Windows; all reset before a usable application response, so equivalent GitHub-hosted transports are explicitly exhausted and their failures remain network-only evidence. A separate 2026-08-26 Wikimedia Commons upload sourced from the same Kyujanggak renderer family for another object proves only non-GitHub feasibility, not G893 access. A legacy `奎章閣漢文文獻珍藏` DVD04 catalog listing `授時曆立成` is retained solely as an unverified mirror locator because the underlying PDF/DJVU file has not been retrieved or bound to `GK00893_00`. Yu Gyung Ro 1997 independently lists `授時曆立成` and 姜保 `授時曆捷法立成` as separate books, reinforcing the no-merge boundary. All six G893 controls remain `PENDING_DIRECT_TARGET_PAGE`; Matrix remains 197 rows / 165 audited, with no runtime or algorithm effect.

- Batch 11R: closed the prewar **collection-level** custody chain around the G893 research object without collapsing it into individual-copy identity. SNU Kyujanggak's official institutional history records the 1928-1930 transfer of the Kyujanggak collection to the Keijo Imperial University library and its 1946 reception by SNU without change in volume count or place of preservation. Rufus 1936 independently reports that the Keijo University Library held a separate undated `授時曆立成` credited to Wang Xun alongside a later-looking Kang Bo `授時曆成捷法立成`, establishing a prewar Wang-Xun Shoushi-licheng object family in that collection. However, Rufus supplies no `奎貴893`, `GK00893_00`, 102-leaf extent, 38×24.8 cm dimensions, microfilm identifier, seals or target page, so exact identity with the current G893 object remains `UNRESOLVED`. The official 1930 Keijo `奎章閣圖書番號順目錄` (`奎26775-v.1-7`) is registered as the next item-level locator, but its internal G893 entry has not yet been directly read. All six target controls remain `PENDING_DIRECT_TARGET_PAGE`; Matrix stays 197 / 165 and runtime/algorithm state is unchanged.

- Batch 11S: directly bound and reviewed the official 1908 `貴重圖書目錄` (`古016.09-G995 / GR35006_00 / BBG`) through the provider's own M/F PDF route, with no OCR. The original PDF is 1,746,005 bytes, SHA-256 `b4b7b14229a82f3f5da12dc069cf8943b1d4c1ff7ca0aa87e85eb3e5d2b06328`. Visual section boundaries show `子部` beginning on PDF page 9 and `集部` beginning on PDF page 12; across the complete bounded `子部` range neither `授時曆立成` nor shortened `授時曆` is visibly listed. This is retained only as a direct negative title-presence catalog witness: it does not prove physical absence of G893 in 1908, does not back-project modern precious-book status, does not establish exact-copy discontinuity from the Rufus 1936 Wang-Xun object, and has no print-year or target-value effect. Exact identity to current `奎貴893 / GK00893_00` remains `UNRESOLVED`; all six targets remain `PENDING_DIRECT_TARGET_PAGE`, and Matrix stays 197 / 165.

The 1581 edition identity is independently corroborated by Shanghai Library linked-data instance `EXT-SHANGHAI-LIB-JIELAN-1581` (子4051; 明万历九年金陵书坊王洛川刻本). This is a bibliographic witness, not a substitute for chapter/facsimile rule-text collation.

- Batch 12A: directly collated a public no-OCR Nanyangtang seven-juan 《紫微斗數全書》 facsimile (SHA-256 `32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7`). PDF p.320 / 卷五《論人生時要審的確》 visibly records `如子時有十刻上五刻屬昨夜亥時下五刻屬今日子時`. This does **not** validate the S01 exact sentence `子時乃一日之始，當從新日計`; PROV-DEFECT-005 remains quarantined. More importantly, the page defines a mechanically distinct half-Zi Hai/Zi hour-classification family that the current natal runtime cannot express because `_hour_branch_index` maps 23:00..00:59 uniformly to Zi. New row `HPA-ZDATE-006=MISSING_FROM_PRODUCT` is therefore registered, with modern `上五刻/下五刻` clock mapping and cross-edition scope still fail-closed. Matrix becomes 198 rows / 166 audited; current missing-product rows 10; cumulative missing candidate families 14; algorithm defect/reopen/candidate-collapse remain 0.

- Batch 12B: closes the generic timekeeping interpretation around `HPA-ZDATE-006` without productizing it. Ming 《三命通会》卷二《论时刻》 states that a shichen contains eight large plus two small ke, divides them into upper/lower halves, and explicitly places Zi's upper half before midnight/on the previous day and lower half after midnight/on the current day. Gu Yanwu's later 《日知录·百刻》 independently explains why “每时有十刻” is a mixed big/small-ke naming structure rather than ten equal-duration ke. NAOJ's calendar-history reference supplies only a modern coordinate translation: fixed Zi shichen ≈ 23:00–01:00 with Zi-zheng at midnight, hence the two halves map approximately to 23:00–24:00 / 00:00–01:00. None of these non-Ziwei witnesses is allowed to become Ziwei doctrinal authority. Shidian's received transcription agrees with direct-facsimile `上五刻/下五刻`; Wikisource has `上午刻/下午刻`, retained as a transcription discrepancy rather than glyph authority. The remaining blockers are additional physical Fullbook editions, Hai-vs-Zi textual lineage, and source-closing the runtime time standard. Counts remain 198 / 166 / 10 missing-product / 14 cumulative missing families; no algorithm reopen.

- Batch 12C: closes the independent Fullbook edition-route map without claiming a target-page collation. Heart-One's official 2017 Fullbook publication (ISBN `9789888266944`) explicitly combines two 虛白廬 late-Ming/early-Qing 文光堂 woodblock witnesses, `敦化堂刊本` and `繼述堂刊本`; the publisher says the former is somewhat earlier and the latter carries red/black collation marks. Its official Jielan publication separately documents a 虛白廬清中期`文誠堂刊本《紫微斗數全書》` used as a collation base, establishing a distinct Qing Fullbook route. A secondary 2017 comparison reports `文盛堂` and `繼述堂` surface similarity but remains locator-only. Research workflow run `34120317222` / artifact `10017909080` successfully captured the publisher/retailer route pages; however Books.com and all 13 preview-image URLs returned 403, Google Books API returned 429, and zero preview images were saved. Consequently no independent physical target page has been observed and `HPA-ZDATE-006.hai_glyph_cross_edition_status=UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES`. Counts remain 198 / 166 / 10 missing-product / 14 cumulative missing families; no algorithm reopen.

- Batch 12D: binds the exact public Google Play/Books distribution volume `aIRbDgAAQBAJ` to Heart-One ISBN `9789888266944`. Public `SearchWithinVolume2` locates 《論人生時要審的確》 at `PT165` and returns index text containing `上五刻 / 下五刻 / 亥時` consistent with the directly read Nanyangtang page. This is **search-index/OCR-like text, not glyph authority** and does not identify whether PT165 derives from the 敦化堂 or 繼述堂 base copy. Official Embedded Viewer run `34123161798` / artifact `10019011766` loaded the volume and accepted `goToPageId("PT165")`, but ended on PT166 and the saved screenshot shows unavailable-preview placeholders; no target glyph was directly visible. Earlier search run `34121750009` / artifact `10018452113` and the viewer run also demonstrate that zero-result queries cannot be treated as negative textual proof because query-result instability occurs. Physical-locator run `34121401508` / artifact `10018315848` saved seven Xinyi public sample JPEGs, all directly visually reviewed with no target page; Kongfz image routes redirected to login and were not bypassed. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`, cross-physical-edition 亥-glyph stability remains unresolved, and counts remain 198 / 166 / 10 / 14 with no algorithm reopen.

- Batch 12E: adds an independent Qing Jingluntang route without claiming a target-page reading. Shanghai Library public linked data binds instance `1pjr6vy1ffsq3l1y` / `子30814110` to `新鋟希夷陳先生紫微斗數全書四卷`, edition label `清經綸堂刻本`, consistently across HTML/JSON-LD/Turtle/RDF/XML. The reviewed public metadata exposes no explicit IIIF/manifest/itemId/dhapi page object; anonymous `gj` and `dhapi/pdfview` root controls returned HTTP 412, so no identifier guessing, login, token reuse or page enumeration was attempted. Kumyo auction `BBAA18036` independently exposes an approximately 19th-century `經綸堂梓行` four-volume physical set. Research run `34124948029` / artifact `10019806060` extracted 36 embedded JPEG occurrences collapsing to 8 unique public physical images; all eight were directly visually reviewed without OCR and visibly establish the Jingluntang physical edition family, including a cover/label with `陳希夷先生著 / 紫微斗數 / 經綸堂梓行`. None is 《論人生時要審的確》, so `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT` and cross-physical-edition 亥-glyph stability remains unresolved. Counts remain 198 / 166 / 10 / 14; no algorithm reopen.


- Batch 12F: closes the seven post-12E probe commits without overpromoting route evidence. Nankai University Library directly binds the public label `辽宁省图书馆古籍书目查询` to Liaoning Library's legacy `/gj/index.htm` route, while the Wenchengtang title/edition/Liaoning holding remains secondary-locator-only because current Liaoning official surfaces timed out. Dalian Library directly records a Republican Shanghai `廣益書局 / 石印本 / 四卷 / 四冊一函` Fullbook witness; six saved image candidates were directly visually reviewed without OCR and are all site UI assets, not book pages. Its published GET form was also exercised normally, but returned pages did not reflect query terms, so no negative-catalog inference is allowed. Google Books volume `rZRcCwAAQBAJ` exposes PT176 editorial index text explicitly naming the Qing Wenchengtang Fullbook (`文本斗數全書`) as a Jielan collation base, but exact target-heading/ten-ke searches do not bind the late-Zi passage and index text is not glyph authority. `HPA-ZDATE-006` therefore remains `MISSING_FROM_PRODUCT`, cross-physical-edition 亥-glyph stability remains unresolved, counts remain 198 / 166 / 10 / 14, and no algorithm reopen occurs. Machine evidence: `docs/research/ZIWEI-QUANSHU-WENCHENGTANG-DALIAN-COLLATION-ROUTES-R1.json`.


- Batch 12G: closes the Qing Lianyuange 《紫微斗數全集》 editorial route without promoting a received transcription to glyph authority. Heart-One's official Jielan page and Google Books volume `rZRcCwAAQBAJ` PT176/PT177 directly bind `連元閣刊本《紫微斗數全集》` as a collation/supplement source; PT205 demonstrates that the editorial layer can quote labeled Quanji variants elsewhere. DestinyNet supplies a secondary received transcription under `五凶神` with `子有十刻 / 上五刻屬昨夜 / 下五刻屬今夜子`, but no physical Lianyuange target page is observed and the wording does not explicitly reclassify the upper half as `亥時`. Exact late-Zi index searches return zero and are not negative proof; the short `子有十刻` hit maps to an unrelated PT88 snippet and is treated as index mismatch. Therefore no new candidate row is created, `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`, counts remain 198 / 166 / 10 / 14, and no algorithm reopen occurs. Machine evidence: `docs/research/ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-R1.json`.


- Batch 12H: binds a high-quality Japan Ming Fullbook route without claiming the target glyph. The National Archives of Japan public index identifies `新鋟希夷陳先生紫微斗数全書 / 子０６０－０００１ / 紅葉山文庫 / 刊本:明 / 2冊 / 公開` and first digital item `4468520`; GitHub-runner run `34134081787` / artifact `10023248966` shows the documented file/item/img and RDF/JSON routes are uniformly HTTP 403 from that execution environment, which is an access boundary only. SDU's official `《子海珍本编·日本卷》` catalog, captured in run `34134328002` / artifact `10023353526`, directly states that the seven-juan Fullbook is facsimile-reproduced from the Naikaku Bunko Ming printed copy. NCKU's Chen Zhaoyin paper visually links this Fullbook to the Qihetang/Nanyangtang publishing family, while Toyo Bunko's current `VII-3-157` Quanji records are labeled `鈔本/寫本`; the latter are therefore not conflated with the printed Jinling Yixuan Tang Qian genealogy without a provenance bridge. No Japan target page is yet observed, `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`, counts remain 198 / 166 / 10 / 14, and no algorithm reopen occurs. Machine evidence: `docs/research/ZIWEI-JAPAN-MING-FULLBOOK-FACSIMILE-ROUTES-R1.json`.


- Batch 12I: adjudicates all committed post-12H late-Zi probes as provenance/dedup/locator controls rather than new historical rule evidence. The Batch 12A Nanyangtang mirror and Batch 12H National Archives/Naikaku route are highly supported as the same physical-copy/digitization lineage, so they are explicitly **not double-counted** as independent Hai-glyph witnesses until a distinct copy is proven; an official NAAJ JP2/page hash would close file-level provenance only. Google Books `kxdy0QEACAAJ` closes a 2016 seven-juan Fullbook bibliographic object but not its exact 15-volume Zihai subvolume or target page. 潘國森 `RISpDgAAQBAJ` strengthens Wenguangtang/Dunhuatang/Jishutang edition locators but yields no late-Zi target reading, and unrelated `亥時` index hits are excluded. Shidian run `34138050721` / artifact `10024763004` reaches the known public target page and APIs but returns zero image URLs/objects, so it adds no physical-glyph authority. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; counts remain 198 / 166 / 10 / 14; no candidate selection or algorithm reopen. Machine evidence: `docs/research/ZIWEI-LATE-ZI-DEDUP-LOCATOR-CONTROLS-R1.json`.


- Batch 12J: upgrades the later Shanghai Guangyi route from Batch 12F's official-library catalog identity to a directly photographed physical set. Workflow `34140027356` / artifact `10025522997` captures the public seller page and four JPEGs; no-OCR visual review directly binds `校正紫薇斗數全書 / 紫薇斗數全書 / 上海廣益書局印行` and a four-book set, but none of the photos is `論人生時要審的確`. The photographed `薇` title surface is preserved separately from catalog/scholarly `微`, and exact identity to Dalian's `廣益書局 民國 / 石印本 / 四卷 / 四冊一函` object remains unresolved pending printing-specific controls. NCKU genealogy places Guangyi as a later Ronghetang-based printing and Ronghetang/Nanyangtang in the same Jianyang origin family, so this physical route is not promoted to a fully independent textual-stemma vote. `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`; counts stay 198 / 166 / 10 / 14; no algorithm reopen. Machine evidence: `docs/research/ZIWEI-GUANGYI-PHYSICAL-SET-COLLATION-R1.json`.


- Batch 12K: tests whether the Heart-One combined Wenguangtang target page PT165 can be assigned to Dunhuatang or Jishutang from public evidence. Run `34174455835` / artifact `10036772401` captures the Sanmin product page, publisher page and eight large public color facsimile samples; direct no-OCR review finds conspicuous red collation marks on samples 4 and 6 but none of the eight is `論人生時要審的確`. Fresh index replay gives 敦化堂/敦化堂藏板 = PT10/PT11, 繼述堂藏板 = PT10, while the target remains PT165. Since PT10 itself contains mixed editorial source-name hits, source-name index positions are not base-copy switch boundaries; red marks likewise are not an exclusive page-level Jishutang identifier. PT165 therefore remains `UNRESOLVED_DUNHUATANG_VS_JISHUTANG`: its search index corroborates the Hai reading but supplies neither target glyph authority nor two independent base-copy votes. `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`; counts stay 198 / 166 / 10 / 14; no algorithm reopen. Machine evidence: `docs/research/ZIWEI-WENGUANG-PUBLIC-SAMPLE-BASE-COPY-PROVENANCE-R1.json`.


- Batch 12L: closes the public Xuelin/Chen Ming `《康节说易全书·紫微斗数》` route as a **modern received-text witness**, not an old-edition facsimile. Front-matter images directly show `康节说易全书·紫微斗数 / 陈明点校 / 学林出版社`. A finite page-offset replay verifies PDF p165 = printed p151; direct no-OCR visual review of that page reads `上五刻属昨夜亥时 / 下五刻属今日子时`. This corroborates the Nanyangtang mechanical reading at modern transmission level, but simplified modern typesetting cannot establish old printed glyph identity, physical-edition independence, or historical punctuation. Independent Hai-glyph witness count added = 0; `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; counts remain 198 / 166 / 10 / 14; no algorithm reopen. Machine evidence: `docs/research/ZIWEI-KANGJIE-MODERN-TYPESET-LATE-ZI-WITNESS-R1.json`.


- Batch 12M: binds the 1870 Mingjingge `《飛星策天紫微斗數全集》` to a concrete SNU Ilsa physical-copy/digitization lineage. Direct public-image review closes `一簑古 523.5 J562b` v.1 identity and visible `同治九年新鐫 / 飛星紫微斗數 / 陳希夷先生著 / 羊城明經閣板` imprint controls; Pduola v.4 pages 0001–0005 visibly carry SNU Kyujanggak branding and bind `523.5 J562b V.4`, but only reach early volume-four material including `太微賦總括`, not `五凶神`. Pduola/Shenjige/Scribd are therefore governed as one SNU digitization lineage, not three votes. A direct Scribd browser run stops at CAPTCHA and is not bypassed; a Kyudb runner probe ends in TLS reset and is treated only as an execution-environment boundary. AKS Sillokwiki independently locates another 1870 Mingjingge six-volume woodblock copy at Hanyang University. No physical `五凶神` target page is obtained, independent Hai-glyph witness added = 0, and `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`. Machine evidence: `docs/research/ZIWEI-MINGJINGGE-SNU-PHYSICAL-COPY-PROVENANCE-R1.json`.

- Batch 12N: upgrades Hanyang from the Batch 12M secondary holding locator to a first-party physical-copy record. Public UI/API binds `新刻合倂十八飛星策天紫微斗數全集. 卷4` to biblio `484926`, item `872523`, barcode `HOM000001861`, call number `133.3 진412ㅅ v.4`, `木板本 / 羊城明經閣 / 同治九年(1870)`, with six-volume/six-book set and detailed block-format metadata. The exact `/resources` request naturally emitted by the detail UI returns HTTP 200 + `success.noRecord`, closing only the current public catalogue resource-object route. No `五凶神` target page or late-Zi line is exposed, so Hanyang is independent at physical-holding level but adds zero independent target-text/Hai-glyph votes. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; counts remain 198 / 166 / 10 / 14; no algorithm reopen. Machine evidence: `docs/research/ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-R1.json`.


- Batch 12O: closes the committed post-12N access probes and adds Korea University as a first-party independently held physical-set route, without converting holding count into textual votes. Exact public detail `CAT000000737166` records `新刻合倂十八飛星策天紫微斗數全集 / 木板本(中國) / [刊寫地未詳] : 江左書林 / [刊寫年未詳] / 6卷6冊`; six items are held at `中央도서관/한적실/` under `대학원 C10 B8 1–6`, registrations `465000245–465000250`, and are non-circulating but readable. Workflow `34211567451` / artifact `10050023318` is the positive first-party record. KLIN/old-book search controls do not bind a target digital object and cannot support absence claims. SNU run `34209828645` / artifact `10049328514` binds the exact volume-4 filename but does not open preview; Hanyang run `34189277789` / artifact `10041642791` finds generic preservation/copy service pages whose rare-book applicability is unresolved, and no request was submitted. Korea University is independent only at holding-object level until direct target-page collation. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; independent target-text/Hai-glyph increment = 0; counts remain 198 / 166 / 10 / 14; no candidate selection or algorithm reopen. Machine evidence: `docs/research/ZIWEI-KOREA-UNIVERSITY-INDEPENDENT-PHYSICAL-COPY-PROVENANCE-R1.json`.

- Batch 12P: binds a new **secondary commercial physical-edition locator**, not a textual witness. Hanauction's public 229th-auction DOM directly exposes lot `134` / stable object `102923` / auction `260` as `청판목판본 역학서 味經堂藏板 [新刻合倂十八飛星紫微斗數全集] 6卷 6冊 완질(函)`, dated 2026-04-04. Run `34214086632` / artifact `10051026199` also binds the exact rendered thumbnail `shopimage/102923S.JPG` (114×66, 7832 bytes, SHA-256 `59973f47a016dc114c967506673b3e053681a6d4a3824ecb8385f7b450fd1385`). Direct visual review without OCR treats the thumbnail only as a low-resolution physical-set photograph; it exposes no `五凶神` target page or `亥` glyph. The same stable object appeared with `ac_num=120` and later `117`, so `ac_num` is a dynamic presentation parameter and not bibliographic identity; an earlier search-engine `ac_num=297` route is deprecated. `味經堂藏板` / Qing-woodblock labeling remains seller/auction-description scope, not institutional catalog or stemma proof. `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`; independent target-text/Hai-glyph increment = 0; counts remain 198 / 166 / 10 / 14; no candidate creation/selection/collapse or algorithm reopen. Machine evidence: `docs/research/ZIWEI-WEIJINGTANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-R1.json`.

- Batch 12Q: KOSTMA first-party `TOYO_1646 / Ⅶ-3-157` is a manuscript (`필사본`), one volume 100 leaves; exact cover image SHA-256 `e0fc07b305e12a5fe3636aafd727b0c27407006bb88f883f7f426c5ea54cff04` exposes no target text. Scribd stops at CAPTCHA with no bypass. Six Fozhu public previews were visually reviewed without OCR and none is `五凶神`. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; Hai-glyph increment = 0; counts remain 198 / 166 / 10 / 14; no candidate or algorithm reopen. Machine evidence: `docs/research/ZIWEI-KOSTMA-TOYO1646-MANUSCRIPT-AND-SCRIBD-FOZHU-ACCESS-CONTROLS-R1.json`.


### Batch 12R — Toyo Bunko VII-3-157 detail/provenance tension

- First-party Toyo detail forms bind targetid `502596` as `新刊希夷陳先生紫微斗數全集 / 寫本 / 1册` and targetid `471894` as `新刊希夷陳先生紫微斗數全集不分卷 / 鈔本 / 1册`, both under `VII-3-157`.
- Two bibliographic target IDs are **not** counted as two physical/textual witnesses; physical multiplicity remains unresolved.
- The generic `貴重書` notice on detail pages is not an item-specific rare marker; the actual request-number field contains only `VII-3-157`.
- NCKU 2021, PDF SHA-256 `17d0089c3328253230cb2f110ac40527abe41fbb97183483215a5e633e5b2e2e`, preserves `金陵益軒唐謙梓` plus a June-1942 Toyo acquisition statement as **secondary scholarly genealogy/provenance**, not target-text authority.
- HPA-ZDATE-006 remains `MISSING_FROM_PRODUCT`; direct Hai-glyph increment = 0; 198/166/10/14 and algorithm invariants are unchanged.
- Evidence: `docs/research/ZIWEI-TOYO-VII3-157-FIRST-PARTY-DETAIL-AND-SCHOLARLY-PROVENANCE-TENSION-R1.json`.


### Batch 12S — Toyo Bunko Media Repository public search-route control

- First-party Media Repository run `34221594363` / artifact `10053963935` binds the provider-emitted general advanced search and the `東洋文庫コレクション` restricted route `item_set_id=42942`.
- Five target terms were searched in both scopes (10 valid HTTP-200 queries). Every page visibly reports `0 件`, and the hardened parser finds zero concrete item/document links plus zero resource nodes.
- Earlier query-echo, pagination-field and `/item/search` self-link false positives are explicitly rejected; only run 4 is controlling.
- This is a current public access-surface boundary, **not** proof of no digitization, no internal image, or target-text absence.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; Hai-glyph increment = 0; counts remain 198 / 166 / 10 / 14; no candidate selection/collapse or algorithm reopen.
- Evidence: `docs/research/ZIWEI-TOYO-MEDIA-REPOSITORY-PUBLIC-SEARCH-ROUTE-CONTROL-R1.json`.

## Cross-chat continuity

Long-running audit state is persisted in `docs/PROJECT-CURRENT-STATE-R1.json` and restored according to `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`. CI runs `scripts/verify-project-continuity-state-r1.py` so Matrix progress, completed batches, defect counts and non-negotiable invariants cannot drift from the handoff state unnoticed.


### Batch 12T — Naikaku/National Archives Nanyangtang facsimile lineage bridge

- Re-review of Batch 12A PDF SHA-256 `32ca49bb...e7` directly reads the p1 legacy label `漢 / 子六十 / 一五八五六 / 全二` and p2 `南陽堂較梓`.
- NAJ first-party file `1078787` / item `4468520` remains `子060-0001`, Red-Leaves former holding, Ming print, 2 volumes; official 2019 digitization list confirms the call/title.
- The evidence supports high-confidence same Naikaku/National-Archives Ming Fullbook lineage, while the explicit `15856 -> 子060-0001` catalog-number crosswalk remains unobserved.
- Dedup: Batch 12A mirror and the NAJ route are not two independent witnesses. Hai-glyph increment = 0; HPA-ZDATE-006 and 198/166/10/14 are unchanged.


### Batch 12U — Naikaku 1971 revised-catalog crosswalk access route

- NDL officially binds the 1971 `改訂 内閣文庫漢籍分類目録` to `UP111-59`, bib ID `000001237342`, PID `12282052`, DOI `10.11501/12282052`.
- Minna Search exposes the existence of an uncorrected OCR derivative and legitimate transmission route, but not the unauthenticated target entry; no login/request/bypass was attempted.
- A 2009 National Archives catalog-method article confirms the revised catalog has a document-name list at the end, making it a high-value old-number crosswalk source, but it does not itself state `15856 -> 子060-0001`.
- Crosswalk remains unresolved pending the direct catalog entry. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; Hai-glyph increment = 0; 198/166/10/14 and algorithm invariants are unchanged.


### Batch 12V — Naikaku 1971 public page-access boundary

- Exact NDL item API for PID `12282052` is publicly readable and exposes 405 content/page objects; response SHA-256 is `0642e44194b40c25380a3a8476d2e92f2b52eb94dcca99d2afb5bc08f91a4a8d`.
- Run `34230231815` / artifact `10057469073` gives zero hits for all eight PID-scoped NDL Lab target queries; the documented Lab full-text JSON route returns HTTP 403. These are route boundaries, not target-entry absence proof.
- Run `34234090185` / artifact `10059056472` tests only API-emitted `publicPath` values: page 1, page 203 and pages 376–405. All 32/32 return HTTP 401 unauthenticated and zero page images are obtained.
- The old-number crosswalk therefore remains unresolved. No login/request/bypass occurred; no whole-catalog negative is authorized. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; Hai-glyph increment = 0; 198/166/10/14 and all algorithm invariants are unchanged.
- Evidence: `docs/research/ZIWEI-NAIKAKU-1971-PUBLIC-PAGE-ACCESS-BOUNDARY-R1.json`.


### Batch 12W — SNU Quark v4 exact file binding + Fozhu N16991 public route controls

- Normal public Quark browser navigation/scrolling in run `34236492659` / artifact `10060095594` accumulates all 49 filenames inside the visible `紫微斗数` folder and binds exactly one SNU Ilsa target file: `【飛星策天紫微斗數全集】一簑古523.5-J562b-v.1-6 ... 木版本（4）.pdf`, visible size `31.5M`, public row key `43681e3e477149ecb2086f2dc25d8d32`.
- This is the same SNU physical-copy/digitization lineage already controlled by Batch 12M, so it strengthens file-level acquisition provenance but adds zero independent textual votes. Normal Web double-click did not expose a PDF viewer, row-local download remained hidden, and a later download safety gate aborted when 35 mounted rows were already selected; no PDF bytes, login, cloud-save, forced hidden-control action or bypass was used.
- Fozhu N16991 run `34238366994` / artifact `10060843332` retrieves six source-emitted public AVIF old-print previews. Direct no-OCR review finds title/contents, text and diagram surfaces but no `五凶神`, `子有十刻` or `上五刻` target passage.
- These six hashes are all different from Batch 12Q's six Fozhu thread-20568 previews, but copy/scan identity remains unresolved; therefore they are not counted as an independent target witness.
- HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; Hai-glyph increment = 0; 198/166/10/14 and all deterministic-product invariants are unchanged.
- Evidence: `docs/research/ZIWEI-SNU-QUARK-V4-AND-FOZHU16991-PUBLIC-ROUTE-CONTROLS-R1.json`.

### Batch 12X — Jiwen 1982/1999 + Dayuan 2012 copy-text routes

- 集文 1999 公開頁保留周祖勇序，直接稱其提供珍藏多年、清同治九年木刻再版的六卷古本供集文複梓；1982 Google Books record `YOwLlQEACAAJ` supplies the earlier publication route. Physical-copy identity versus SNU remains unresolved, so witness increment = 0.
- 大元 2012 `9789866171680` is publicly described as a six-volume 434-page 精鈔本. Xinyi emits large internal samples; direct no-OCR visual review shows handwritten vertical copy text and a title/imprint surface reading `十八飛星策天紫微斗數全集 / 大宋扶搖子白雲先生陳摶著 / 南州草坪徐良弼校正 / 金陵益軒唐謙繡梓`.
- Public directory text gives `五神 百字千金訣`. This is quarantined as a directory-level variant/possible omission and is **not** mechanically normalized to `五凶神` before the underlying target page is directly collated.
- No target late-Zi page is observed. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; 198/166/10/14 and all deterministic-product invariants remain unchanged.
- Evidence: `docs/research/ZIWEI-JIWEN-1982-1999-AND-DAYUAN-2012-COPY-TEXT-ROUTES-R1.json`.

### Batch 12AA — Hui County Museum official illustrated-catalog route

- National Library Press's 2025 `《辉县市博物馆藏古籍珍品书录》` (ISBN `978-7-5013-7612-4`) officially binds a Hui County Museum `《新鋟希夷陳先生紫微斗數全書四卷》` holding; the directory places the entry at p233. The publisher states that each selected ancient book receives representative original-book imagery.
- The public product `Booktext` action returned only product metadata/description/directory text (32,920 bytes; SHA-256 `9172da23a2d292c9fc86965a0dad0673ac25be7bfb5e0944f628fa0ad035be10`). No p233 entry image or late-Zi target page was obtained.
- Kumyo/Jingluntang is the already-reviewed Batch 12E object; Liaoning/Wenchengtang is already Batch 12F; Shidian explicitly belongs to the Nanyangtang received-text lineage; the anonymous 33.75 MB Fullbook file is conservatively quarantined as a likely Nanyangtang black-white derivative; Buybook/Books.com.tw preview images remain a runner-access boundary. None receives a new witness vote.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; 198/166/10/14 and all algorithm invariants remain unchanged. Next gate remains a direct late-Zi target page from another Fullbook physical edition.


### Batch 12AD — Sanfenge/Quark Fullbook volume-four public-share route

- Sanfenge provider HTML directly binds `212163` → `紫薇术紫薇斗数全书卷4.pdf` → Quark `6956a639be12`, and `212173` → `紫薇术《紫微斗数全书》四卷.pdf` → Quark `9f7f6a4e7730`.
- Both exact public Quark share URLs return HTTP 200 initial SPA shells, but no filename or PDF bytes are present in that initial HTML. This is an access boundary, not content absence.
- Edition/imprint identity and the target late-Zi leaf remain unobserved; `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`, with zero new textual/Hai votes and no algorithm effect.
