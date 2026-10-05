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

The initial inventory contained **107 rule/field families**. Through Batch 12NR and explicit splitting of historically distinct candidate families, the current machine-readable inventory contains **220 rows**, with **220 audited rows**. It intentionally keeps unresolved source work explicit rather than converting uncertainty into a chart defect. The current audit ledger records **40 confirmed provenance metadata defects repaired forward-only at the provenance/hash-lineage layer, 0 chart algorithm defects, 0 algorithm reopens, 14 cumulatively identified missing candidate families, 10 rows currently `MISSING_FROM_PRODUCT`, 6 historical candidate extensions, 3 source-scoped historical candidate registries, and 3 runtime-resolver components**.

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


### Batch 12AE — Republic Huiwentang physical + Jinzhang catalog routes

- Kongfz source-emitted physical title image directly reads `上海會文堂書局印行`; no target late-Zi leaf is shown.
- `《重刊術藏》` directly catalogs the Fullbook in volume 59 as a Republic Jinzhang lithograph, four juan in one volume, beginning at p333; this is bibliographic identity only.
- Artron reviewed physical-set photos do not directly show a Jinzhang imprint or target leaf. Jinyuan's modern TOC locates `論人生時要審的確` at p175 but does not show its body page.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; zero new target-text/Hai votes and no algorithm effect.

### Batch 12AF — Guangyi/Yulgok direct late-Zi collation

- Yulgok first-party tree directly lists `B005_01_B00320_001..004` as the four books of `新鑴希夷陳先生紫薇斗數全書`; public viewers embed 19 representative `imgItems`.
- Direct image `B005_01_B00320_001_004` reads `上海廣益書局印行`. Direct image `B005_01_B00320_003_003` shows `卷三 / 論人生時要審的確` and directly reads `如子時有十刻上五刻屬昨夜亥時下五刻屬今日子時`. No OCR.
- This adds one direct Fullbook physical target-text witness and one Hai-glyph physical witness. Nanyangtang↔Guangyi physical-edition agreement is closed; global all-edition stability and stemmatic independence are not claimed.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; 198/166/10/14 and all algorithm invariants remain unchanged.

### Batch 12AG — Jiaojingshanfang/Hanauction physical-edition provenance

- Hanauction exact historical rows bind Shanghai Jiaojingshanfang `《改良紫微斗數全書》` as a four-juan/four-book lithographic physical-edition route in 2012 (auction 65, lot 173, stable object `27427`) and 2026 (auction 227, lot 127, stable object `101926`).
- Research run `34319318823` / artifact `10091275632` captures exact source-emitted target thumbnails and, on the 2012 exact detail page, two 300×225 JPEG objects with SHA-256 `c8705995...21c2` and `a22d0017...5260`. The current execution did **not** directly visually adjudicate those detail photos, so no target heading, late-Zi page or `亥` glyph is claimed.
- NCKU 2021 scholarly genealogy places the Jiaojingshanfang late edition, like Guangyi, on the Baohutang-derived Fullbook line. It is therefore provenance breadth, not a stemmatically independent textual vote.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; target-text increment = 0, Hai-glyph increment = 0, 198/166/10/14 and all algorithm invariants remain unchanged.
- Evidence: `docs/research/ZIWEI-JIAOJINGSHANFANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-R1.json`.


### Batch 12AH — Jiaojingshanfang/Hanauction detail-photo visual adjudication

- The Batch 12AG artifact was reopened at evidence-scope level only. Direct review of artifact `10091275632` binds browser HTML SHA-256 `93e6d80f...fec65` and screenshot SHA-256 `8a5bc72c...771dd`.
- The two previously labeled 300×225 “exact detail photos” are explicitly placed by the archived HTML under `제65회 우리 얼 찾기 경매전 풍경`, with roles `7/7 경매 전시 동영상` and `7/7 경매 진행 동영상`.
- Direct no-OCR visual review shows, respectively, an auction-room/exhibition scene and an auction-event presenter at a lectern. They are not lot-173 object photographs and do not expose the target book page.
- `PROV-DEFECT-010=EVIDENCE_SCOPE_MISCLASSIFICATION` is confirmed and repaired forward-only: the hashes remain preserved for archive lineage, but target-object/detail-photo authority is revoked.
- Exact 2012/2026 Jiaojingshanfang auction-row provenance remains valid. Target-text increment = 0; Hai-glyph increment = 0; `HPA-ZDATE-006=MISSING_FROM_PRODUCT`; 198/166/10/14 and algorithm invariants remain unchanged.
- Provenance accounting is now 10 confirmed / 10 repaired metadata defects; confirmed chart algorithm defects remain 0.
- Evidence: `docs/research/ZIWEI-JIAOJINGSHANFANG-HANAUCTION-DETAIL-PHOTO-VISUAL-ADJUDICATION-R1.json`.


### Batch 12AI — Ziwei late-Zi historical time-coordinate narrowing

- Machine probe `34322850489` / artifact `10092539912` binds three public witness surfaces: 《明史·天文志》 time determination, 《明史·历志》 geographic gnomon/clepsydra differences, and USNO's modern apparent-vs-mean solar-time definition.
- The received Ming institutional clock family is observational rather than a modern zone clock: daytime sundial/true-Sun and nighttime stellar observation are treated as fundamental; clepsydra is supplementary, and north-south geography materially changes historical gnomon/clepsydra realization.
- USNO is a translation control only. A calibrated local sundial maps most directly to local apparent solar time; this does not prove that the Fullbook natal-hour rule inherits that regime or that the current Ziwei runtime should select apparent solar time.
- `HPA-ZDATE-006` is therefore narrowed to `LOCAL_OBSERVATIONAL_ASTRONOMICAL_TIME_COORDINATE`, while nighttime runtime equivalence, natal birthplace locality and exact Fullbook clock-regime inheritance remain unresolved.
- `HPA-ZDATE-006=MISSING_FROM_PRODUCT`; runtime binding = `PARTIALLY_NARROWED_NOT_CLOSED`; no candidate selection/collapse and no algorithm reopen. Counts remain 198/166/10/14; provenance defects remain 10 confirmed / 10 repaired.
- Evidence: `docs/research/ZIWEI-LATE-ZI-HISTORICAL-TIME-COORDINATE-NARROWING-R1.json`.


### Batch 12AJ — Fullbook 羅經 timekeeping semantics

- Final decisive probe `34325691911` / artifact `10093682981` promotes Xu Guangqi et al. `《新法算書》`卷一 as the controlling primary/near-primary technical witness; `《皇明經世文編》` carries the same memorial and is explicitly non-independent. The dynamic Siku catalog is non-controlling.

- Direct no-OCR re-review confirms the same third line in both Nanyangtang p320 / 卷五 and Guangyi/Yulgok `B005_01_B00320_003_003` / 卷三: `如天氣陰雨之際必須羅經以定真確時候若差訛則命不凖矣`.
- The same two physical copies were already counted as target-text witnesses; Batch 12AJ adds zero textual/Hai votes and records only a new semantic collation.
- 《皇明經世文編》卷493 `制器測晷` separates functions: 日晷=daytime time, 星晷=nighttime time, 正線羅經=子午 direction, 行漏=cloud/rain supplement. It also warns that exclusive compass use gives indeterminate timing error and generally runs early.
- Ming 徐之鏌《新鐫徐氏家藏羅經頂門針》 directly anchors 羅經 in magnetic-needle/directional semantics.
- Therefore `羅經以定真確時候` cannot be mechanically normalized to `羅經 itself is a clock`, `true solar time`, or `local apparent solar runtime`. The exact Fullbook operational procedure remains source-scoped and unresolved.
- `HPA-ZDATE-006=MISSING_FROM_PRODUCT`; runtime binding becomes `PARTIALLY_NARROWED_WITH_FULLBOOK_INSTRUMENT_SEMANTIC_TENSION_NOT_CLOSED`; no candidate selection/collapse and no algorithm reopen.
- Evidence: `docs/research/ZIWEI-FULLBOOK-LUOJING-TIMEKEEPING-SEMANTICS-R1.json`.


### Batch 12AK — Gaohou Mengqiu operational timekeeping bridge

- Waseda first-party catalog binds 徐朝俊《高厚蒙求》, call no. `ニ05 02158`, 雲閒徐氏, 嘉慶12-14[1807-1809], with third-collection contents 日晷測時図法 / 星月測時図表 / 揆日正方図表 / 自鳴鐘表図法.
- Waseda's archive directory source-emits `ni05_02158.pdf`; Batch 12AK captures the 74,443,272-byte / 221-page physical scan, SHA-256 `53ee7b0e...7f1e4`.
- Direct no-OCR p143 review shows `一曰羅經平晷 / 此即徽地所製牽線取影晷也` with an embedded compass/orientation element: 羅經 participates in sundial orientation, while shadow geometry reads time.
- Direct no-OCR p195 `鐘表圖說自序` separates `日晷諸法以測晝時`, `星月儀表諸法以測夜時`, then addresses `陰雨晦冥` and states `所以辨子亥定支干`.
- This is a later 嘉慶 operational bridge, not proof of Ming Fullbook authorial practice. No Fullbook witness/Hai vote is added; true/apparent-solar runtime remains unselected.
- `HPA-ZDATE-006=MISSING_FROM_PRODUCT`; current runtime-binding status = `LATER_OPERATIONAL_BRIDGE_CONFIRMED_FULLBOOK_SOURCE_SPECIFIC_BINDING_STILL_OPEN`.
- Evidence: `docs/research/ZIWEI-GAOHOU-MENGQIU-OPERATIONAL-BRIDGE-R1.json`.


### Batch 12AL — Korea CNTS full target-section re-collation

- Same already-counted physical manuscript: Korea National Library / CNTS `CNTS-00047996572`, 《紫微斗數方書》, 筆寫本, exact copying date unresolved. No new physical witness vote.
- Direct no-OCR p125 re-review reads `命有稱兩時者可詳之子有十刻上五刻屬昨夜下五刻屬今夜`; the immediately adjacent next column changes to a `交限十年...` topic.
- Direct p126 review is already a different limit-period surface, so the p125 birth-hour passage does not continue with the Fullbook `如天氣陰雨之際必須羅經以定真確時候...` clause.
- This establishes only that explicit Hai/current-Zi wording **and** the Fullbook Luojing clause are not universal across broader received Ziwei transmission. Nanyangtang + Guangyi Fullbook stability remains intact.
- No Fullbook interpolation claim, no Korean-copy error claim, no candidate collapse and no algorithm reopen are authorized.
- `HPA-ZDATE-006=MISSING_FROM_PRODUCT`; current runtime-binding status = `BROADER_ZIWEI_TRANSMISSION_VARIANT_CONFIRMED_FULLBOOK_OPERATIONAL_PROCEDURE_REMAINS_SOURCE_SCOPED_AND_RUNTIME_UNRESOLVED`.
- Evidence: `docs/research/ZIWEI-KOREA-CNTS-FULL-TARGET-SECTION-RECOLLATION-R1.json`.


- Batch 12AM: early-Ming shushu semantics are now directly bound to a 510-page facsimile of 徐善繼、徐善述《人子須知》. The composite is source-labelled 隆慶三年刊 / 萬曆十一年梅墅石渠閣補刊本; CiNii BB17866565 independently corroborates the 梅墅石渠閣 / 萬暦11 [1583] edition family without claiming the same physical copy. Direct no-OCR review locates 三昧論有引 at PDF p414 and 正針縫針 at p415; p416 directly reads `臬測以景針以氣故不能符` and `推七政之纏次皆准於臬`. This strengthens the mechanical firewall: the gnomon/shadow astronomical reference and qi-responsive magnetic needle are distinct operations, so 羅經 cannot be normalized to a standalone clock, 真太陽時 or local apparent-solar runtime. The Fullbook cloudy/rainy time-generation chain remains source-scoped and unresolved; `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`, counts remain 198/166/10/14, and algorithm defect/reopen/collapse remain 0.


- Batch 12AN: 《完孝錄》〈論定時〉 confirms a Ming shushu 24-mountain/time-sector coordinate bridge. CText source search emits physical locator `file=100720&page=144`; Shidian ROUTER_DATA binds the route to 國家圖書館 / 內府明萬曆35年刻本 and target PageIds mapping to global pages about 5607-5611. The text anchors time checking to 太陽到處 / 逐時逐刻考驗 / 考星躔, so a Luojing-like 24-sector ring is a coordinate aid, not a standalone clock. Target scan image bytes remain unobserved; no glyph authority is claimed. `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`; 198/166/10/14 and algorithm invariants remain unchanged.

### Batch 12AO — 1581 Jielan complete public-transcription inclement-time boundary

- Source-emitted Tianji pagination p1-p5 was fully traversed; the public surface declares 246 chapters / 67,533 characters.
- Birth-time positive controls are present, while configured Fullbook inclement-Luojing terms are not attested on that complete current public transcription surface.
- No whole-1581-physical-book negative, glyph authority or interpolation claim is authorized without direct facsimile review.
- Nanyangtang + Guangyi direct Fullbook facsimile evidence remains controlling for the physical Fullbook clause; Ming technical control still uses clepsydra rather than magnetic compass as the inclement clock input.
- HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; runtime-binding status = EARLY_1581_JIELAN_COMPLETE_PUBLIC_TRANSCRIPTION_NONATTESTATION_CONFIRMED_FULLBOOK_INCLEMENT_LUOJING_CLAUSE_REMAINS_SOURCE_SCOPED_AND_CLOCK_INPUT_UNRESOLVED.
- Counts remain 198/166/10/14; algorithm defect/reopen/collapse remain 0.
- Evidence: docs/research/ZIWEI-JIELAN-INCLEMENT-TIME-ACQUISITION-R1.json.



## Batch 12AP — Jielan PT49 scope correction

- `PROV-DEFECT-011=EVIDENCE_SCOPE_MISCLASSIFICATION` is confirmed and repaired forward-only.
- Batch 12AO's exact Tianji aggregate-pagination pages 1–5 nonattestation remains valid **only for that finite surface**.
- Google Books Jielan volume `rZRcCwAAQBAJ` source-emits `PT49` for `陰雨`; index text places the hit under `論十二生時難定訣` with inclement birth-time semantics. The AO transmission-level absence inference is therefore retracted.
- PT49 physical glyph authority remains unavailable. Directly reviewed Google Books PT47/PT48 and NCC/Heart-One public facsimile samples do not include the target leaf.
- `羅經 / 真確時候 / 行漏 / 壺漏` remain nonattested only on reviewed Jielan public index surfaces; no physical negative is authorized.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; runtime winner, candidate collapse and algorithm reopen remain forbidden.
- Accounting: 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families / provenance defects 11 confirmed + 11 repaired / chart algorithm defect-reopen-collapse 0.
- Machine evidence: `docs/research/ZIWEI-JIELAN-BIRTH-TIME-CHAPTER-SCOPE-CORRECTION-R1.json`.


## Batch 12AQ — Jielan bibliographic imprint reconciliation

- Direct no-OCR review of 《中國古籍善本書目·子部三》 PDF p40 confirms `新刻纂集紫微斗數捷覽四卷` as catalog item **4051**.
- The printed edition line directly reads `明萬曆九年金陵書坊王洛川刻本`.
- Search-engine extraction `王德川` and row `4052` are rejected as OCR/table-alignment artifacts; 4052 is visibly the adjacent 《上官拜命玉曆大全不分卷》.
- Taiwan NCL independently records an unrelated Ming book as `明金陵王氏洛川校刊本`; this is a bookseller/imprint-name control only, not Jielan copy identity.
- Existing repository Jielan imprint metadata is therefore preserved. No repository provenance defect, Matrix-row status, candidate selection or algorithm state changes.
- Anhui holding remains secondary-locator scope pending an official item-level record.
- Accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families / provenance defects 11 confirmed + 11 repaired / chart algorithm defect-reopen-collapse 0.
- Machine evidence: `docs/research/ZIWEI-JIELAN-BIBLIOGRAPHIC-IMPRINT-RECONCILIATION-R1.json`.


## Batch 12AR — Jielan PT49 public preview access boundary

- Classic Google Books PT49 is HTTP 200 and index-positive, but its returned public surface does not emit a PT49 target image.
- Public Google Play reader directly emits signed image URLs for PT48/PT49/PT50 without authentication or signature construction.
- PT48 direct response is a genuine facsimile JPEG (`4d95bcc7a8c14d842d1d735faa83cfbb33cc16773cc35ddb4ef18d3c679d95d0`).
- PT49 and PT50 direct responses are the identical visible `image not available` PNG placeholder (`3efa8c43e5b4348f303a528c81adf435f0111ea752fe9f0f6241478b60987fa6`), so no PT49 physical glyph authority is obtained.
- English accessible mode is HTTP 403; the historically source-emitted new-Books link redirects to classic Books and emits no PT49 image object. iRead runner timeout is access-boundary only, not a content negative.
- No physical-book negative, runtime selection, candidate collapse, algorithm reopen or provenance-defect increment is authorized.
- Accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families / provenance defects 11 confirmed + 11 repaired / chart algorithm defect-reopen-collapse 0.
- Machine evidence: `docs/research/ZIWEI-JIELAN-PT49-PUBLIC-PREVIEW-ACCESS-BOUNDARY-R1.json`.


## Batch 12AW — Zhangguo 1594 night-Zi physical witness

- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; Matrix counts are unchanged.
- NIJL/Tohoku BID `100238879`, 《新編評註通玄先生張果星宗大全》, 陸位, 萬曆22/1594, canvas 195 was directly visually collated.
- Main text securely attests `人命多有生時不定，以子為亥，亥為子，以初為末，末為初，則坐度不同……` in a birth-time uncertainty/error context.
- The upper annotation securely attests `七政曆所載，有夜子時之分，有上四刻下四刻之法；上四刻正陰，下四刻正陽。`
- This strengthens the pre-1697 genealogy of the night-Zi split and Zi/Hai confusion, but does **not** itself prove `upper four ke -> Hai branch`, does not select a modern time coordinate, and adds no runtime winner or algorithm reopen.
- Durable collation: `docs/research/ZIWEI-ZHANGGUO-1594-NIGHT-ZI-PHYSICAL-COLLATION-R1.json`; batch decision: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-1594-NIGHT-ZI-FOUR-KE-PHYSICAL-COLLATION-AW.md`.

## Progress through Batch 12BO

- Batch 12BO directly collates the Qing Kangxi-manuscript 《孫子彙徵》 PDF p44 without OCR as glyph authority.
- The physical sentence reads `若子時則上半時在夜半前屬昨日下半時在夜半後為今日`; the public transcription regularizes the second relation verb to `屬今日`.
- This is `DIFFERENT_WORDING_SAME_MECHANICAL_RULE`: it corroborates generic midnight previous/current-day orientation, does not reassign upper Zi to Hai, and is not counted as an independent Ziwei/Bazi doctrinal lineage vote.
- HPA-ZDATE-006 remains `MISSING_FROM_PRODUCT`; row/audit/candidate counts and all algorithm invariants are unchanged.

## Progress through Batch 12BP

- Historical Tianyige catalogs independently record `筮箧理数日钞二十卷`; the Jiaqing catalog preface describes an actual cabinet-by-cabinet pavilion inventory, and the late-Qing `見存` catalog still lists the title.
- The late-Qing Tianyige and Zhejiang collection catalogs attribute the work to `明柯佩編/輯`; the NAJ/Shidian copy carries `一壺天俱道人` responsibility wording. The identity/role relationship is unresolved and is not collapsed.
- This is a historical holding-lineage advance only. Present survival, current shelfmark, textual identity with the NAJ 1565 copy, and the exact `上四亥` target glyph remain unresolved.
- HPA-ZDATE-006 remains `MISSING_FROM_PRODUCT`; Hai vote, candidate, runtime and algorithm invariants are unchanged.

## Progress through Batch 12BQ

- 《永樂大典》卷18764 `前定數 → 諸家序 → 四字經序` preserves a pre-1581 textual attestation combining `子丑寅亥` hour-discrimination difficulty with the formula `古經云天陰雨露時難定，便是神仙也有差`.
- The extant physical-recension layer is the Ming Jiajing duplicate tradition; do not call the current scan an extant 1408 physical leaf. The textual incorporation layer belongs to the Yongle Dadian compilation tradition, while the internally cited `古經` remains unidentified and undated.
- The wording is closely parallel to 1581 Jielan `天陰雨下時難定，便是神仙也有差`, establishing an early shared inclement-birth-time motif/formula but not direct copying or a single school lineage.
- Public scan page 3 is located, but direct project screenshot/no-OCR glyph collation was not completed; HPA-ZDATE-006 remains `MISSING_FROM_PRODUCT`, Hai vote is unchanged, and the Fullbook cloudy/rain operational mechanism remains open.

## Progress through Batch 12BR

- Independent Ming-print transmission of 《四字經》 is now confirmed outside 《永樂大典》: Taiwan NCL catalogs a one-juan Ming-Wanli Jinling Jingshan-shulin object (15275-0058), while an NLC-sourced 1597 《夷門廣牘》 scan independently contains 《四字經》.
- CText explicitly binds its automatic OCR to the 《夷門廣牘》 base. Despite OCR corruption, the opening `唐明皇論` preserves the same long ordered architecture as the Yongle-Dadian `四字經序`: fate/八字 and five-phase framing, seasonal/day-night analogies, weather and travel imagery, simultaneous-number wealth/rank/longevity differences, difficult 亥子丑寅 hours, inclement-weather time uncertainty, `便是神仙也有差`, and month-length/time reasoning.
- This upgrades the evidence from a shared proverb/motif to a demonstrable Sizijing transmission/text-family bridge. It does not prove exact recension identity, direct copying, Tang authorship/date, or exact glyph variants.
- Apparent variants `古經/古人`, `雨露/雨落`, and `子丑寅亥/亥子丑寅` remain OCR-bound and unadjudicated. HPA-ZDATE-006 remains `MISSING_FROM_PRODUCT`; Hai vote, runtime and algorithm invariants remain unchanged.


## Progress through Batch 12BS

- The 1597 NLC/Yimen 《四字經》 opening is now directly collated from a hashed physical DjVu render with no OCR used for final glyph judgment. Page 28 prints `四字經 / 唐德行禪師著 / 明周履靖校正 / 唐明皇論`.
- Page 29 directly resolves the three Yimen-side Batch-12BR variants as `古人云`, `天陰雨落難定`, and contiguous hour order `亥子丑寅`. CText OCR is corroborated for these exact loci only.
- The Yongle-Dadian readings `古經云 / 雨露 / 子丑寅亥` remain a separate recension/transmission witness; Batch 12BS does not call them errors or select a stemmatic winner.
- The literal `亥` belongs to a difficult-hour list, not an upper-Zi-to-Hai reassignment rule. HPA-ZDATE-006 remains `MISSING_FROM_PRODUCT`; Hai-branch mechanical vote, runtime selection, candidate collapse and algorithm reopen remain unchanged.
- Next high-value gate is direct Taiwan NCL 15275-0058 target-leaf collation for edition/impression comparison, while the Fullbook inclement-current-time acquisition chain remains independently open.


## Progress through Batch 12BT

- The complete 21-page Taiwan NCL 15275-0058 public 《四字經》 PDF derivative is now rendered and directly reviewed without OCR. Page 1's physical TOC lists `唐明皇論` before `甲甲`, independently strengthening the internal-unit bridge to the 1597 Yimen witness.
- Page 3 directly reads `四字經目錄終`; the next public page 4 opens the visible body as `四字經 / 甲甲`, and the remaining pages continue the stem-pair body through `癸癸`. No `唐明皇論` prose body leaf is exposed in the 21-page public derivative.
- The admissible finding is a public-scan target-leaf lacuna, not proof that the physical holding lacks the leaf. Taiwan contributes no direct glyph vote for `古人/古經`, `雨落/雨露`, or hour ordering from this derivative, and same-impression/disbound identity with the Yimen object remains unproved.
- HPA-ZDATE-006 remains `MISSING_FROM_PRODUCT`; Hai-branch mechanical vote, runtime selection, candidate collapse and algorithm reopen remain unchanged. Next gate is another Taiwan image route or direct Yongle physical collation, while the Fullbook operational-current-time chain remains separate.


## Progress through Batch 12BU

- The current Taiwan NCL first-party `rbook.ncl.edu.tw` record is directly rebound to 《四字經》 / 15275-0058 and advertises an image-viewer target for the same holding.
- Entry to image enumeration is guarded by an interactive puzzle captcha. The official page only navigates to the hidden viewer URL on successful verification; direct image=1 GETs without that human-verification state return the detail surface and expose zero `.ImageC` page entries.
- The admitted-viewer JavaScript expects `.ImageC` page links and per-image watermark tokens, but no captcha bypass, fabricated solution or session replay was attempted. Therefore first-party target-leaf presence is `UNRESOLVED_AT_HUMAN_VERIFICATION_BOUNDARY`, not a negative holding result.
- Batch 12BT's public-scan lacuna remains intact. Taiwan contributes no new target-variant glyph vote; HPA-ZDATE-006 stays `MISSING_FROM_PRODUCT`, with Hai mechanical vote/runtime selection/candidate collapse/algorithm reopen unchanged.


## Progress through Batch 12BV

- The public facsimile of 《永樂大典》卷18764 has now been directly rendered and reviewed without OCR. Page 3 physically reads `四字經序`, `且子丑寅亥`, `四箇時辰難以推分`, `古經云`, `天陰雨露時難定`, and `便是神仙也有差`.
- This closes the exact-glyph authority gap left by Batch 12BQ. Combined with Batch 12BS, both sides of the Sizijing comparison now have physical glyph authority: Yongle/Jiajing-duplicate recension `古經 / 雨露 / 子丑寅亥` versus 1597 Yimen `古人 / 雨落 / 亥子丑寅`.
- The differences are therefore genuine recension variation, not OCR/transcription noise. No archetype, copying direction, stemmatic winner or runtime winner is selected.
- The four-hour ordering remains a textual list, not an operational late-Zi-to-Hai reclassification rule. HPA-ZDATE-006 remains `MISSING_FROM_PRODUCT`; Hai mechanical vote, candidate collapse and algorithm reopen remain unchanged.


## Progress through Batch 12BW

- Ming institutional timekeeping is now closed at the technical-context layer: the Zhengde and Wanli Huidian traditions record leak-clock time determination, hour-tablet changes, drum watch reporting, and bell/drum dawn-dusk signaling, with Qintianjian leak-clock personnel maintaining the system.
- Xu Guangqi's Chongzhen technical memorandum supplies the weather fallback explicitly: sun dial by day, star dial by night, corrected compass for meridian orientation, and calibrated running clepsydra for dawn/dusk/cloud/rain when the dials cannot operate.
- This establishes a historically attested inclement-weather current-time mechanism in Ming technical practice, but does not rewrite the Fullbook physical reading `羅經` into `行漏` or prove what exact instrument composition Fullbook practitioners intended.
- HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; no runtime winner, Hai mechanical vote, candidate collapse or algorithm reopen follows from this contextual closure.


## Progress through Batch 12BX

- The end of the Sizijing inclement-time passage now has a two-recension physical reading: Yongle `旦夕將月建長短而推言` versus 1597 Yimen `旦夕時刻且將月運長短定推言之`; `月建/月運` is a genuine recension variant, not OCR noise.
- Premodern technical controls place `旦夕/長短` in a real seasonal timekeeping domain: Sui Shu says leak-clock allocation changes with qi and winter/summer day-night length, while Song Qunshu Kaosuo explicitly links 斗建 and seasonal progression to leak-arrow length and 48 arrows keyed to 24 qi.
- Classical `月運` also means lunar motion (`方言`: 日運為躔、月運為逡; Tang 海濤論: 月運朔望), so the Yimen reading cannot be silently converted into a modern monthly-fortune cycle.
- Semantic domain is narrowed, but exact 月建↔月運 operational equivalence and a numeric birth-time recovery formula remain unproved. HPA-ZDATE-006 and runtime invariants do not change.


## Progress through Batch 12BY

- Song official timekeeping evidence makes the seasonal-timekeeping interpretation more constrained: Wang Pu's Guanli Kelou Tu preface says Yue-tai is the standard, but regional solstitial day/night ke and even 24-qi arrow-change dates can differ across the realm.
- Songshi likewise states geographic distance affects gnomon results and records Lin'an parameters differing from Yue-tai; separate calendar procedures compute daily dawn/dusk, sunrise/sunset and midnight leak for the standard location.
- Therefore any future attempt to operationalize Sizijing `旦夕/月建/長短` must identify a geographic calibration basis. A universal month-only correction table is historically under-specified.
- No direct bridge authorizes importing Song Yue-tai formulae into Sizijing, so no new runtime candidate, winner, Hai vote or algorithm reopen is created.


## Progress through Batch 12BZ

- The 1578 physical Sanming Tonghui witness already directly connects natal birth-time adjudication to Shoushi-calendar division after a seasonal sunrise/sunset/day-night-ke table; Batch 12BZ integrates that primary bridge with the later Sizijing seasonal-timekeeping research.
- A separate China National Library Ming-Wanli physical holding (juan 2 upper/lower across volumes 3–4) was rendered without OCR and reconfirms the same structural/textual sequence. Its exact identity with the 1578 impression is not assumed and it adds no independent textual vote.
- HPA-ZDATE-006 historical time-standard provenance is therefore significantly narrowed to a Shoushi-calendar/seasonal-ke horizon, but no deterministic inverse birth-time formula, locality binding, modern-instant mapping, or upper-Zi-to-Hai reassignment is closed.
- Result: HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; no runtime candidate, winner, collapse, or algorithm reopen.


## Progress through Batch 12CA

- Yuan Shoushi-calendar methods explicitly support regional realization: nine-region day/night ke depend on local pole altitude, and local solstitial leak values can be fixed by instruments or water clocks.
- A Ming technical transmission explicitly distinguishes a 地中 40/60 standard from the Yandu Shoushi 62/38 standard. Sanming Tonghui's displayed mantic table is therefore not automatically the exact Yandu table; its summer-solstice line is 59/41.
- Tianyige's Ming-print Huqianjing physically confirms that 40/60-style seasonal leak-arrow tables belong to a wider historical timekeeping tradition, but no direct genealogy from Huqianjing to Sanming is claimed.
- Locality capability is closed at the calendar-system level; Wan Minying's selected locality/table genealogy and any modern-instant binding remain unresolved. HPA-ZDATE-006 stays MISSING_FROM_PRODUCT with no new candidate, winner, Hai vote, collapse or reopen.


## Progress through Batch 12CB

- A no-OCR physical review of the 1533 Chengqiao-print 《運氣易覽·論四時氣候》 directly confirms `晝夜分五十刻`, `夏至日長不過六十刻`, and `冬至日短不過四十刻` in a pre-1578 medical-yunqi witness.
- This closes an earlier 50/50 + 60/40 conceptual/disciplinary parallel, but the reviewed locus does not print Sanming Tonghui's distinctive multi-point 42/58...59/41 table. Exact table identity and direct genealogy are therefore not established.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; no Hai-branch vote, runtime candidate, winner, collapse or algorithm reopen is introduced.


## Progress through Batch 12CC

- The complete 45-page public 1569 Zhou-Xiang 《大明大統曆法》 volume was rendered and visually reviewed without OCR. It directly strengthens the pre-1578 Ming Datong method-source stack.
- The reviewed physical object does not directly expose the distinctive Sanming seasonal 42/58...59/41 table. This is strictly a volume-scoped nonattestation; it does not authorize a claim that the wider Datong tradition, other fascicles, official almanacs or separately transmitted tables lack such material.
- Exact Sanming table provenance/locality therefore remains open. `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`; no Hai-branch vote, runtime candidate, winner, collapse or algorithm reopen is introduced.


## Progress through Batch 12CD

- Direct no-OCR review of received 《革象新書》 pp78-80 physically locks the near-verbatim hundred-ke / half-Zi prose lineage later seen in the 1578 《三命通會》, while preserving the `屬昨日` versus Sanming `為昨日` recension difference.
- Re-reading the Tianyige Ming-print 《虎鈐經·傳箭》 as a complete sequence shows an older 40↔60 one-ke-step ladder containing many exact Sanming numeric pairs. Sanming changes term/date anchors and caps summer solstice at 59/41 rather than Huqianjing's 60/40.
- The composite model—older prose lineage + older leak-arrow numeric ladder + Ming adaptation—is materially strengthened, but the exact pre-1578 Ming/Nanjing 59/41 parent remains open. `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`; no Hai vote or algorithm reopen is introduced.


## Progress through Batch 12CE

- An independent NLC-derived Ming-print physical copy of 《類編曆法通書大全》第1冊 directly confirms two day/night-ke systems in the same volume: a coarse 24-qi copper-pot 40/60 family and a fine `四時加減晝夜節氣` 38/62 one-ke ladder.
- The coarse table physically includes `小滿 59/41`, `夏至 60/40`, `大暑 59/41`; the fine table reaches `62/38`. Therefore Sanming's `夏至 59/41` equals neither table exactly, while dual-table coexistence materially strengthens a mixed/adapted lineage model.
- A later Ming control, Xing Yunlu's 《古今律曆考》卷47, explicitly distinguishes Nanjing Datong `59/41` from Yandu Shoushi `62/38`. Because the work is later than the 1578 Sanming witness, this is explanatory control, not ancestor proof.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; no Hai vote, runtime winner, candidate collapse or algorithm reopen is introduced.


## Progress through Batch 12CF

- NLC physical collation of 《明英宗睿皇帝實錄》卷160, 正統十二年十一月甲寅 (1447), directly records Nanjing solstitial 59-ke extrema, Beijing 62-ke extrema, and states that palace/government clepsydra arrows were still the Nanjing old style.
- This closes the pre-1578 Ming/Nanjing 59-ke locality layer. The complementary 41/38 values are explicitly classified as hundred-ke complements, not numerals directly printed in this memorial.
- The exact bridge from the 1447 Nanjing endpoint to Sanming's 1578 multipoint solar-term sequence remains open; no Fullbook upper-five-ke -> Hai vote, runtime winner, candidate collapse or algorithm reopen is introduced.

## Progress — Batch 12CG

- Direct no-OCR review of NCL-06267 `《大統日出分》` closes a physical daily Nanjing Datong numerical substrate. Li Liang's independent table study classifies `大統日出入分` as 1380s Type `C-II-N` (Nanjing) and its published C-II-N opening/end fingerprints agree with the NCL object.
- Converting `半晝分` to full daylight ke replays multiple distinct integer anchors across the 42→59 ladder seen in the 1578 `《三命通會》` seasonal table. This is a generative/numerical bridge, not proof that Wan Minying copied this exact surviving object or used modern nearest-integer rounding.
- Song 日新 `《盂蘭盆經疏鈔餘義》` self-dates its lecture/republication to 熙寧元年 (1068); its received `〈節氣加減刻漏規式〉` says `今依本朝定景福殿秤漏` and assigns integer 40/60→60/40 day/night pairs to explicit intra-solar-term day ranges. It independently proves the stepped integer-bin algorithmic form long predates Sanming, while its exact change-days are not equated to Sanming.
- Therefore the pre-1578 mechanical bridge is materially closed one layer: older integer-bin leak-clock practice + a Ming/Nanjing daily Datong numerical table can explain the form and value range of the Sanming ladder. Exact textual parent, compositing event and quantization thresholds remain unresolved.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; upper-Zi→Hai vote +0; runtime winner/candidate collapse/algorithm reopen remain none/0. Matrix counts remain 198/166/10/14 and provenance defects remain 11/11.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-DATONG-RICHU-DAILY-TABLE-SANMING-MULTIPOINT-REPLAY-CG.md`. Research record: `docs/research/ZIWEI-DATONG-RICHU-DAILY-TABLE-SANMING-MULTIPOINT-REPLAY-R1.json`.

## Progress — Batch 12CH

- Direct no-OCR review of `CADAL02090387 四時氣候集解` closes a securely pre-1578 printed Tongshu-labelled coarse day/night-ke branch. Bibliographic reproduction metadata binds the object to the Shanghai Library `明景泰六年胡廷璨刻本`; physical p123 independently preserves `景泰六年龍集乙亥孟春吉日` dated end matter.
- Physical p41/p47/p57 read `立夏 57/43`, `小滿 59/41`, `夏至 60/40`. This is the same coarse `40↔60` family independently observed in Batch 12CE and is **not** the 1578 Sanming table at the summer-solstice anchor: Sanming prints `夏至 59/41`.
- Batch 12CF already closed an official Nanjing solstitial `59` layer in 1447. Its coexistence with a 1455 printed Tongshu `夏至 60/40` branch proves that early-Ming technical transmission remained layered; one locality/calendar standard did not simply replace all older seasonal tables.
- NCL-03164 is retained as an `舊鈔本` transmission control only. Its internal 1425 preface and 1455 postface do not by themselves date that surviving manuscript copy, so the earlier acquisition-manifest `DIRECT_PRE1578` label is explicitly narrowed rather than propagated.
- The composite-transmission model is strengthened but direct genealogy remains open: coarse 40↔60 seasonal lineage + Nanjing/Datong 59-ke locality layer + unresolved selection/quantization/editorial recomposition may explain Sanming, but no direct-copy edge is asserted.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; upper-Zi→Hai vote +0; runtime winner/candidate collapse/algorithm reopen remain none/0. Matrix counts remain 198/166/10/14 and provenance defects remain 11/11.
- Batch 12CH also records an explicit `transmission_impact` graph section in its research JSON so future lineage work can distinguish attestation, coexistence, candidate ancestry and unproved direct-copy edges.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SISHI-QIHOU-JINGTAI6-TONGSHU-TABLE-CONTROL-CH.md`. Research record: `docs/research/ZIWEI-SISHI-QIHOU-JINGTAI6-TONGSHU-TABLE-CONTROL-R1.json`.

## Progress — Batch 12CI

- Direct no-OCR review of `CADAL06060929 宋史·卷六十九~卷七十` physically closes the received `《宋史》卷七十` witness recording that in `大中祥符三年` (1010) 春官正韓顯符 submitted `《銅渾儀法要》` with a 24-qi day/night advance-retreat and sunrise/sunset ke-number established method. The 1010 date is the recorded technical event, not the date of the surviving scanned copy.
- The 24-term day/night rows conserve exactly 100 ke. In every non-equinox row the integer parts total 99 and the residuals total 147, so the residual denominator is mechanically inferable as 147 per ke. `59刻142` must therefore not be misread as modern decimal `59.142`.
- Re-review of the Ming-print `《類編曆法通書》` coarse table on physical pp18–24 closes all 24 integer term anchors. The entire table is compatible with one quantization threshold on the Song residuals: residuals `<=78` remain at the lower integer and residuals `>=81` advance one ke. No 79/80 residual occurs, so the exact threshold is only bounded to `(78,81]/147`.
- Modern nearest-integer rounding is explicitly rejected as the historical explanation: it matches 22/24 but fails at `大寒` and `小雪`, where `41 + 78/147 ~= 41.531` would round to 42 while the direct Ming coarse table prints 41.
- This establishes a full 24/24 **mechanical quantization compatibility** between the recorded 1010 precision table and the later coarse `40<->60` family. It does not prove direct textual copying, a specific historical rounding instruction, or the exact stemma.
- The result explains the older coarse table family, not the 1578 `《三命通會》` Nanjing-like display: Sanming still differs materially (`小寒 42/58`, `立春 45/55`, `夏至 59/41`) and continues to require the separately evidenced Ming/Nanjing locality/daily-table adaptation layer.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; upper-Zi->Hai vote +0; runtime winner/candidate collapse/algorithm reopen remain none/0. Counts remain 198/166/10/14 and provenance defects 11/11.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SONGSHI-HANXIANFU-1010-DAYNIGHT-KE-PHYSICAL-COLLATION-CI.md`. Research record: `docs/research/SONGSHI-HANXIANFU-1010-DAYNIGHT-KE-PHYSICAL-COLLATION-R1.json`.


## Progress — Batch 12CJ

- A new no-OCR physical review of `CADAL06049792《虎鈐經·卷七~卷十一》` provides an independent Siku-recension control for `卷七《傳箭》第七十六`. It preserves the same core mechanics already observed in the Tianyige Ming-print witness: `每時有八刻二十分`, `一刻六十分`, `一日十二時合一百刻`, winter `40/60`, summer `60/40`, and the one-ke seasonal ladder.
- Direct physical collation corrects the prior Batch 12CI shorthand `48-arrow system`. The section numbers arrows only `第一箭` through `第二十箭`; at summer solstice it resets to `第一箭` and reuses the numbering for the opposite half-year direction. This is a research-text correction, not a chart algorithm defect and not a provenance-defect counter increment.
- The two physical witnesses materially strengthen the stability of the Huqianjing operational rule family across recensions, but no direct-copy direction between Tianyige and the Siku witness is asserted, and no direct Han-Xianfu -> Huqian textual edge is asserted.
- For 1578 Sanming, the Huqian lineage remains a strong structural component candidate because it preserves the same one-ke stepwise numeric family, while its `夏至 60/40` reset and change-day schedule remain non-identical to Sanming's `夏至 59/41` display.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; upper-Zi→Hai vote +0; runtime winner/candidate collapse/algorithm reopen remain none/0. Matrix counts and deterministic product invariants are unchanged.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-HUQIANJING-TIANYIGE-SIKU-CROSS-RECENSION-COLLATION-CJ.md`. Research record: `docs/research/ZIWEI-HUQIANJING-TIANYIGE-SIKU-CROSS-RECENSION-COLLATION-R1.json`.


## Progress — Batch 12CK

- Seoul National University Kyujanggak directly catalogs `奎貴894-v.1-3《七政算內篇》` as 李純之、金淡受命編, `甲寅字`, publication year `1444`. A provider-renderer-bound no-OCR review of volume 0003 pages `039b..044b` localizes and reads the complete `二至後日出入晝夜辰刻` table family.
- The physical 1444 witness gives winter-solstice first-day `晝39 / 夜61`, pre-summer day 159 `晝60 / 夜40`, and summer-solstice first-day `晝61 / 夜39`. This is not a Nanjing `59/41` table.
- The official National Institute of Korean History Sillok route is now exactly bound: `wda_50034001` = 冬至後 and `wda_50034002` = 夏至後 + the statement that the Inner Chapter uses the Hanyang solstitial gnomon to derive daily sunrise/sunset and day/night values `定爲本國所用`. The previously probed `wda_50018...` prefix is recorded as a locator inference error only.
- Combined with the already audited 1447 Ming memorial (`南京59`, `北京62`), the evidence establishes near-contemporary regional calibration as a first-order variable: Hanyang 61, Nanjing 59, Beijing 62. Numeric similarity alone is therefore insufficient for lineage claims.
- For the 1578 Sanming `59/41` table, Hanyang becomes a parallel regional negative control rather than a proposed direct parent. The next ancestry gate should prioritize securely localized Nanjing/Jiangnan or other 59-ke-cap intermediaries with Huqian-like step ladders/change-day fingerprints.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; upper-Zi→Hai vote +0; runtime winner/candidate collapse/algorithm reopen remain none/0. Matrix counts and deterministic product invariants are unchanged.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-CHILJEONGSAN-G894-HANYANG-DAYNIGHT-REGIONAL-CALIBRATION-CK.md`. Research record: `docs/research/ZIWEI-CHILJEONGSAN-G894-HANYANG-DAYNIGHT-REGIONAL-CALIBRATION-R1.json`.


## Progress — Batch 12CL

- NLC/Wikimedia volume 18 of `《明英宗睿皇帝實錄》` was rendered in GitHub Actions without OCR. Physical-surrogate page `090` binds `卷之一百八十六`; page `091` directly contains `詔更定大統曆晷刻` and the order `今後造曆，宜悉照洪武、永樂間舊式`.
- The same official passage explicitly states that the Beijing adjustment differed from Nanjing by three degrees of polar altitude and by `冬至晝短三刻 / 夏至晝長三刻`. This is an official regional-calibration and policy-restoration statement, not a modern reconstruction.
- The passage itself does **not** print `59/41` or `62/38`. Combined with Batch 12CF's direct 1447 `南京59 / 北京62` evidence, it strengthens the interpretation that the Nanjing 59-ke branch belonged to an older standard family restored after the Beijing-adjusted regime, while leaving row-for-row identity unresolved.
- For the 1578 Sanming table, Batch 12CL upgrades the regional/policy continuity candidate but does not close the missing Huqian-style daily ladder, change-day fingerprint, or rounding/selection bridge. No direct-copy edge is asserted.
- A separate continuation control rendered NLC volume 19 and confirmed that it begins with the卷187 sequence; the earlier suspicion that the target might continue into volume 19 is closed as a locator-scope correction only.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; upper-Zi→Hai vote +0; runtime winner/candidate collapse/algorithm reopen remain none/0.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YINGZONG-SHILU-1449-DATONG-OLD-STYLE-RESTORATION-CL.md`. Research record: `docs/research/ZIWEI-YINGZONG-SHILU-1449-DATONG-OLD-STYLE-RESTORATION-R1.json`.


## Progress — Batch 12CM

- A public reproduction of Zhou Xiang's `《大明大統曆法》` book 6 was fetched and all `45` pages were rendered/reviewed without OCR (run `35009608549`, artifact `10412298745`, source SHA-256 `4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c`).
- Direct page-level collation separates the date layers: p7 visibly bears `隆慶三年七月` (1569) and Zhou Xiang's reprint layer, while p9 `步氣朔卷第一` explicitly computes to `大明成化十三年丁酉` (1477). The modern PDF surrogate is dated 2019 and is not collapsed into either historical date.
- The fascicle is a strong pre-1578 Datong technical-transmission witness: p14/p19 preserve solar winter/summer standing tables and later leaves preserve lunar/朔 and related computational tables. However, no independent `晨昏分 / 日出入 / 晝夜刻` table was observed within the finite 45-page public reproduction.
- That nonattestation is strictly fascicle-scoped. It closes Zhou Xiang vol6 as a direct target-table shortcut, not the wider Datong tradition. The next gate moves to direct `大統曆通軌/日通軌` 晨昏立成, pre-1578 annual almanacs, and `閑中錄`.
- `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; no runtime candidate, winner, candidate collapse, chart algorithm defect, or algorithm reopen is created.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHOUXIANG-DAMING-DATONG-1569-1477-COMPUTATION-REPRINT-CONTROL-CM.md`. Research record: `docs/research/ZIWEI-ZHOUXIANG-DAMING-DATONG-1569-1477-PHYSICAL-COLLATION-R1.json`.

## Progress — Batch 12CN (corrected by Batch 12CO)

- KOSTMA `DIC_A3_000150` remains a valid `大統曆日通軌` institutional record in a Sejong-era `1433–1445` calendrical-reform context.
- Exact-record re-audit shows that the record lists `太陽冬至前後二象盈初縮末限`, `太陽夏至前後二象縮初盈末限`, `太陰遲疾度立成`. It does **not** list `日出入晨刻表`, `晝夜刻分表`, or `四方每時初昏去中星度數表` in the audited record.
- The source-emitted Kyujanggak identifier is `GK12437_00`. The prior `GR35954_00` attribution is withdrawn.
- Therefore Batch 12CN no longer establishes a pre-1578 Datong-line day/night-table-class witness. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; no runtime change is authorized.

## Progress — Batch 12CO

- Exact attribution audit: GitHub Actions run `35058829315` / job `104674602946`.
- Provenance defect repaired across the external-source registry, matrix progress, research record, transmission graph, Batch 12CN narrative, continuity state, and formalizer guard.
- Defect class: `PROVENANCE_METADATA_WRONG_RECORD_FIELD_AND_HOLDING_ATTRIBUTION`.
- The valid evidence retained is bibliographic/computational (`大統曆日通軌`, its three solar/lunar computational tables, and metadata binding `GK12437_00`), not a day/night-ke numerical table witness.
- The next gate returns to direct table discovery and page-level collation; `59/41`, daily ladders, change days, rounding, and direct Sanming parentage remain unresolved.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-DATONG-RITONGGUI-KOSTMA-ATTRIBUTION-REPAIR-CO.md`. Research record: `docs/research/ZIWEI-DATONG-RITONGGUI-KOSTMA-ATTRIBUTION-REPAIR-R1.json`.


## Progress — Batch 12HX

- FID070 first-book physical scans now provide two independent complete large-type main-text lines on different pages, p12 and p16, each directly counted at 17 characters without OCR.
- GB/T 3792.7—2008《古籍著录规则》8.7.1.4(b) specifies that line-count metadata is based on full half-leaves and full lines; the standard applies to Chinese ancient-book cataloging and lists the National Library of China among its principal drafting institutions.
- These object-level controls converge with the Tieqin historical catalog, the 1987 Beijing Library catalog and the 2017 Shanghai Ancient Books publication preview, all of which describe the main-text line as 17 characters while preserving 23-character double-line commentary.
- `PROV-DEFECT-016=CURRENT_PROVIDER_FORMAT_NOTE_MAIN_TEXT_FULL_LINE_CHARACTER_COUNT_ERROR` is therefore confirmed and repaired forward-only. The current NLC raw `10行16字` provider value remains preserved as observed metadata; project adjudication uses `10行17字 / 小字雙行23字` for the exact physical witness.
- Accounting advances to 16 confirmed / 16 repaired provenance metadata defects. Matrix rows remain 198, audited rows 166, current MISSING_FROM_PRODUCT rows 10, chart algorithm defects/reopens/candidate collapses remain 0.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NLC-ZUOZHUAN-FID070-SECOND-17CHAR-LINE-GBT-FORMAT-DEFECT-CLOSURE-HX.md`. Research record: `docs/research/ZIWEI-NLC-ZUOZHUAN-FID070-SECOND-17CHAR-LINE-GBT-FORMAT-DEFECT-CLOSURE-R1.json`.


## Progress — Batch 12HY

- The exact 1959 Beijing Library target entry for FID070 remains direct no-OCR evidence for `瞿捐`; this closes Qu-surname donation provenance at target-entry level but supplies no donation year, batch or exact accession date.
- NLC-hosted 2024 scholarship records Qu-family donation activity in 1950, 1953 and 1954 without enumerating target contents. Ji Shuying-derived secondary recounting reports 1950-01-07, 1950-03 and 1953-03 events, but neither layer names FID070/book no.3368; no target date is selected.
- Zhao Wanli's 1951 quotation bridge naming a Qu-donated `宋刻《春秋左传注疏》` among 62 titles is preserved as a candidate object bridge only. Exact identity with the physically re-adjudicated Yuan-impression FID070 remains unproved, so it cannot supply the target's exact transfer date.
- The target-specific `1959 3368 → 1987 3288` mechanism remains unresolved; no public object-level card/correction/preparation record was recovered, and negative search is not treated as absence evidence.
- Matrix/accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 16 of 16 provenance defects repaired; chart algorithm defects/reopens/candidate collapses remain 0.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NLC-ZUOZHUAN-FID070-QUDONATION-CHRONOLOGY-FIREWALL-HY.md`. Research record: `docs/research/ZIWEI-NLC-ZUOZHUAN-FID070-QUDONATION-CHRONOLOGY-FIREWALL-R1.json`.


## Progress — Batch 12HZ

- Direct no-OCR cross-collation of the hash-bound 1959 pp.55–56 and 1987 p.104 scans expands the local number control around FID070 from one stable neighbor to three.
- The shared local core preserves order as `7283 → 8643 → TARGET → 10010`. The three flanking records retain `7283`, `8643`, and `10010` in both catalogs; only the target changes `3368 → 3288`.
- This disproves a blanket local arithmetic offset and wholesale local resequencing for the shared four-record core, and closes the observed scope as `TARGET_SPECIFIC_WITHIN_SHARED_LOCAL_NEIGHBORHOOD`.
- The exact causal mechanism remains unresolved: no 1959/1987 correction card, preparation slip or accession/crosswalk record has yet been recovered, so 1959 error vs 1987 correction vs target-specific reassignment is not ranked.
- Matrix/product accounting is unchanged: 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 16 of 16 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-BEITU1959-1987-ZUOZHUAN-LOCAL-NEIGHBOR-SEQUENCE-CROSSWALK-HZ.md`. Research record: `docs/research/ZIWEI-BEITU1959-1987-ZUOZHUAN-LOCAL-NEIGHBOR-SEQUENCE-CROSSWALK-R1.json`.


## Progress — Batch 12IA

- Current NLC `meta.nlc.cn` ANY numeric search was calibrated against known-positive current `905s` values `03288` and `08643`; both return `no matching result`. Therefore the same result for disputed `03368` is an index-capability boundary, not absence evidence.
- Google Books SearchWithinVolume2 for the 1959 catalog is retained only as a navigation locator. `三二八八` returned PP34/PP36/PP60, while title+3368 and title+3288 returned the same PP61/PP64 tokens, demonstrating noisy/non-exact matching.
- Using the same-volume PP64→direct PDF56 target calibration, all three `三二八八` locator candidates were manually reviewed on the hash-bound 1959 scan at PDF26/PDF28/PDF52 without project OCR. None prints exact `三二八八 / 3288`; the three machine hits are false positives.
- This does not prove global absence of 3288 in the whole 1959 catalog. HZ remains controlling: the observed `3368→3288` change is target-specific within the stable local neighborhood, while its causal mechanism remains unresolved.
- Product/accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 16 of 16 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NLC-BEITU1959-3368-3288-SEARCH-INDEX-BOUNDARY-IA.md`. Research record: `docs/research/ZIWEI-NLC-BEITU1959-3368-3288-SEARCH-INDEX-BOUNDARY-R1.json`.


## Progress — Batch 12IB

- The complete public eight-volume 1959 《北京图书馆善本书目》 scan set is mapped through Wikimedia Commons (SSID 12335507–12335514).
- r5 completed all eight volumes and emitted zero `三二八八 / 3288` candidates, but the same locator failed the already-directly-closed positive controls on volume-1 PDF55–56, including `三三六八 = 3368`. Therefore the zero-candidate output has no absence value.
- A separate embedded-text calibration finds no usable text/font layer on the positive pages; 48 conventional OCR variants and 64 native Traditional-Chinese vertical OCR variants also produce zero positive variants.
- The tested machine-locator family is closed as `FAILED_KNOWN_POSITIVE_RECALL`; whole-catalog absence remains unproved and no future zero-result may be promoted without first passing the known-positive calibration.
- HZ and IA remain controlling for historical adjudication: the observed `3368→3288` change is target-specific within a stable local neighborhood, but the causal mechanism is still unresolved.
- Product/accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 16 of 16 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-BEITU1959-CROSSVOLUME-3288-LOCATOR-CALIBRATION-BOUNDARY-IB.md`. Research record: `docs/research/ZIWEI-BEITU1959-CROSSVOLUME-3288-LOCATOR-CALIBRATION-BOUNDARY-R1.json`.


## Progress — Batch 12IC

- Official NOPSS project-report evidence directly binds Zhang Lijuan's `国图藏元刻十行本《附释音春秋左传注疏》` to `《国学季刊》第十一期 / 山东人民出版社 / 2018年9月` at article-citation and research-summary level; the reviewed page is not the article full text.
- Current public-route probes recover no usable full text: Google Books has no candidate volume; Open Library has no positive record; Internet Archive's sole exact-full-title hit is directly adjudicated as an unrelated 太平天国 text-object false positive.
- Public retail metadata is contradictory: Kongfz binds target contents to issue 11 / ISBN `9787209115018` / `2018-12`, while Sanmin binds the same ISBN to issue 12 / `2019-05-01`. ISBN-to-issue11 identity and exact publication month remain unresolved; retail metadata cannot overwrite the official NOPSS report.
- Highest next gate is an institutional-library or publisher-level issue-11 object plus lawful article full text/page images; recovered article pages are to be checked for object-level NLC shelfmark/book-number/catalog-preparation detail relevant to `3368→3288`.
- Product/accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 16 of 16 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANG-LIJUAN-GUOXUEJIKAN11-PUBLIC-FULLTEXT-ROUTE-BOUNDARY-IC.md`. Research record: `docs/research/ZIWEI-ZHANG-LIJUAN-GUOXUEJIKAN11-PUBLIC-FULLTEXT-ROUTE-BOUNDARY-R1.json`.


## Progress — Batch 12ID

- `PROV-DEFECT-017` is confirmed and repaired forward-only: Batch 12IC used page-level co-occurrence on a multi-item Kongfz listing and incorrectly assigned adjacent issue-12 metadata to `《国学季刊》第十一期`.
- Direct single-item review corrects issue 11 to `ISBN 9787209115001 / 2018-09 / 222 pages`, with Zhang Lijuan's target article in the contents. The adjacent issue 12 item is `ISBN 9787209115018 / 2018-12 / 277 pages`.
- The official NOPSS project report independently gives the target article as `《国学季刊》第十一期 / 山东人民出版社 / 2018年9月`, agreeing with the corrected issue-11 month.
- Batch 12IC remains preserved as historical audit trace. Its public-fulltext boundary, Internet Archive false-positive closure, Google Books no-candidate route and Open Library no-positive route remain valid; only the issue-11 ISBN/date conflict adjudication is superseded.
- Sanmin's issue-12 record keeps ISBN `9787209115018` but gives `2019-05-01`; this is now an issue-12 secondary publication-date tension, not an issue-11/issue-12 ISBN conflict.
- Accounting advances to 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 17 of 17 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-GUOXUEJIKAN11-ITEM-LEVEL-ISBN-FORWARD-CORRECTION-ID.md`. Research record: `docs/research/ZIWEI-GUOXUEJIKAN11-ITEM-LEVEL-ISBN-FORWARD-CORRECTION-R1.json`.


## Progress — Batch 12IE

- Public discovery routes were rerun with corrected issue-11 ISBN `9787209115001` after `PROV-DEFECT-017`.
- Google Books API requests for corrected ISBN/title are HTTP 429 rate-limited. Current status is `RATE_LIMITED_UNRESOLVED`; 429 must never be normalized to a zero-result claim.
- Open Library exact ISBN returns HTTP 404 and corrected ISBN/title searches return `numFound=0`; Internet Archive exact ISBN, quoted ISBN and exact `国学季刊 第十一期` queries return 0. These are public-route boundaries only, not nonexistence evidence.
- Internet Archive's exact target-article-title query again returns identifier `3_20260926_202609`, already adjudicated in 12IC as an unrelated 太平天国 text-object false positive.
- No target article full text or publisher/institutional issue-11 object is recovered. The corrected public-fulltext boundary remains open, and `3368→3288` causal mechanism remains unresolved.
- Product/accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 17 of 17 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-GUOXUEJIKAN11-CORRECTED-ISBN-PUBLIC-ROUTE-RECHECK-IE.md`. Research record: `docs/research/ZIWEI-GUOXUEJIKAN11-CORRECTED-ISBN-PUBLIC-ROUTE-RECHECK-R1.json`.


## Progress — Batch 12IF

- Cambridge University Library's first-party `Chinese Periodicals` union catalogue directly lists `文物参考资料` with holdings `卷2i-xii` under call `FB.252:14`; target 1951 volume 2 issue 9 is therefore explicitly contained.
- The separate Needham Research Institute `1951-58` row on the same union catalogue is not counted as a second exact issue-9 closure because it does not enumerate issue-level gaps.
- This adds one independent original-periodical physical holding route beyond the NDL original-bundle route and Ryukoku 1986 facsimile backup; it adds zero direct article-text evidence.
- Zhao Wanli 1951 pp.221-233, NDL-held 2011 `赵万里文集` vol.1 p.197 and the Qu-family 62-title original wording remain not directly collated. FID070 exact Qu donation batch/date and `3368→3288` causal mechanism remain unresolved.
- Product/accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 17 of 17 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENWU-CANKAO-CAMBRIDGE-1951-V2-HOLDING-ROUTE-IF.md`. Research record: `docs/research/ZIWEI-WENWU-CANKAO-CAMBRIDGE-1951-V2-HOLDING-ROUTE-R1.json`.


## Progress — Batch 12IG

- Zhejiang Library's official `《图书馆研究与工作》` 2026 issue-4 PDF is directly retrieved and hash-bound (`SHA-256 2e0b9c1d59ccc95523b48144964cb8f528161c3b9201cb28da0cee41de9cd776`), with a readable text layer and no OCR.
- A page-level probe closes the Zhao Wanli donation quotation on official-PDF page 92: `瞿济苍 / 凤起 / 旭初 / 捐赠 / 宋刻 / 春秋左 + 传注疏 / 六十二种 / [2]197` are co-located. Reference `[2]` is the 2011 `《赵万里文集：第一卷》`.
- This upgrades the existing 12HJ/12HY quotation bridge to official-journal direct article text only. It does not equal direct review of 2011 p.197 or the 1951 original `《文物参考资料》第9期 pp.221–233`.
- The quoted `宋刻《春秋左传注疏》` is not collapsed into FID070, whose physical research adjudication is `元刻元印十行本`; exact FID070 Qu-donation batch/date and the `3368→3288` causal mechanism remain unresolved.
- Highest next gate is lawful direct-page recovery rather than further holding-count expansion. NDL remote-copy is a viable account/fee-dependent route for the already-located 1951 article, but no login/request/payment is authorized without explicit user approval.
- Product/accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 17 of 17 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHAO-WANLI-P197-OFFICIAL-JOURNAL-QUOTE-AUTHORITY-UPGRADE-IG.md`. Research record: `docs/research/ZIWEI-ZHAO-WANLI-P197-OFFICIAL-JOURNAL-QUOTE-AUTHORITY-UPGRADE-R1.json`.


## Progress — Batch 12IH

- NDL's current first-party remote-copy policy is now directly adjudicated against the two already-located paper targets: 2011 `《赵万里文集》第1卷` p.197 (`UM11-C247 / 023434359`) and 1951 `《文物参考资料》第9期` pp.221–233 (`Z8-AC150 / 2(7)-2(12) 1951`). The service requires a registered user, fees and precise page/article specification; both target locators are already complete.
- NDL's copyright/copy-scope guidance keeps book copying at a partial-work layer while permitting a whole article from a sufficiently old periodical. This closes service-policy eligibility only; it does not declare public-domain status and does not prove exact-item staff acceptance.
- No login, account action, identity transmission, copy request, delivery-mode selection or payment was executed. Direct 2011 p.197 and direct 1951 pp.221–233 remain `NOT_REVIEWED`.
- The 12IG object firewall remains unchanged: quoted `宋刻《春秋左传注疏》` is not collapsed into FID070 (`元刻元印十行本`); exact Qu donation batch/date and `3368→3288` mechanism remain unresolved.
- Product/accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 17 of 17 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NDL-DIRECT-PAGE-REMOTE-COPY-POLICY-BOUNDARY-IH.md`. Research record: `docs/research/ZIWEI-NDL-DIRECT-PAGE-REMOTE-COPY-POLICY-BOUNDARY-R1.json`.

## Progress — Batch 12II

- Zhejiang Library's first-party 2024 article/index surface directly binds 蔡成普、李静《郑振铎与铁琴铜剑楼藏书捐献》 to `2024(7):46`, article id `1783`, and visibly advertises `PDF(549 KB)`.
- The site's own download contract is closed at code/request level: `showArticleFile.do` returns `status=1` for `PDF`, `PDF_CN` and `PDF_Mobile`, and emits tokenized route families; `mag_request()` defaults to HTML-form POST with no extra hidden PDF data.
- Exact source-emitted route probes for all three families return the identical 3,241-byte `text/html;charset=UTF-8` server `HTTP404 无法找到页面` wrapper (SHA-256 `9c47ea7957afef955da0248c47be6a49c274287abcbe061a7710d7bcbb9ca999`) and no PDF magic. This is a current public-route materialization boundary, not proof that the PDF does not exist.
- No article full text, 2011 p.197, 1951 pp.221–233 or Ji Shuying chapter-9 direct page is newly reviewed; no shopping/payment endpoint, login or fee action is executed.
- FID070 remains non-collapsed from the quoted Song-print object; exact Qu donation batch/date and `3368→3288` mechanism remain unresolved. Product/accounting remains 198 / 166 / 10 and 17/17 provenance repairs, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZJLIB-TIEQIN-2024-OFFICIAL-PDF-TOKEN-ROUTE-ACCESS-BOUNDARY-II.md`. Research record: `docs/research/ZIWEI-ZJLIB-TIEQIN-2024-OFFICIAL-PDF-TOKEN-ROUTE-ACCESS-BOUNDARY-R1.json`.


## Progress — Batch 12IJ

- Public pagination calibration for the exact 2009 《冀淑英古籍善本十五讲》 edition now has scoped anchors at Chapter 3 pp.39–50, Chapter-8-region pp.125–126 (secondary locator only), Chapter 12 p.190 (direct academic PDF citation), and Chapter 15 p.223 (direct institutional PDF citation).
- The anchors are not promoted into an inferred Chapter-9 range. 《铁琴铜剑楼藏书的收购入藏》 exact pagination and direct text remain unresolved / not reviewed.
- Tokyo Metropolitan holding C/022.3/6011/2009 / material 4001029913 remains the lawful fallback; no account, request, identity or fee action is executed.
- No 3482/3483 transaction assignment, FID070 donation-date/batch upgrade, 3368→3288 causal upgrade, genealogy-topology change or product/runtime change occurs.
- Accounting remains 198 / 166 / 10 and 17/17 provenance repairs, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JI-SHUYING-2009-PUBLIC-PAGINATION-CALIBRATION-BOUNDARY-IJ.md. Research record: docs/research/ZIWEI-JI-SHUYING-2009-PUBLIC-PAGINATION-CALIBRATION-BOUNDARY-R1.json.


## Progress — Batch 12IK

- A public commercial package manifest now supplies a stable filename locator for the exact 1951 issue-9 target: `KW143 / 1951.8-9 / wwck195109.pdf / 9.73 MB`.
- This is access-locator metadata only. No PDF bytes, hash, page count, scan provenance, completeness or lawful public-download status is established; the package's `原刊扫描` wording is not promoted to provenance authority.
- A second search-indexed xy980 surface reproduces the same manifest pattern but currently fetches as HTTP 502 and is treated only as a duplicated locator, not an independent scan witness.
- Exact-filename and Internet Archive-domain discovery recovered no public direct object; those zero results remain route observations, not nonexistence evidence. No unverified mirror/commercial download is executed.
- 1951 pp.221–233, 2011 p.197 and Ji Shuying Chapter 9 remain not directly reviewed. Accounting remains 198 / 166 / 10 and 17/17 provenance repairs, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENWU-CANKAO-1951-WWCK195109-SCAN-PACKAGE-LOCATOR-BOUNDARY-IK.md`. Research record: `docs/research/ZIWEI-WENWU-CANKAO-1951-WWCK195109-SCAN-PACKAGE-LOCATOR-BOUNDARY-R1.json`.


## Progress — Batch 12IL

- Google Books Volumes API probes for Ji 2009 and Zhao 2011 ISBN/title routes return explicit HTTP 429 `RESOURCE_EXHAUSTED` with daily project quota limit value `0`; this is an access/quota boundary, never a no-volume result.
- Public `SearchWithinVolume2` on known Ji route `bAnzzgEACAAJ` was tested with 14 high-information terms. Every response is HTTP 200 with `number_of_results=0` and `searchable=false`; the zero counts therefore carry zero textual-absence authority.
- No page ID, snippet, Chapter-9 text/range, Zhao 2011 p.197, or 1951 pp.221–233 is recovered. No account/purchase/bypass action is executed.
- Highest next gate leaves this nonsearchable route and returns to lawful direct page/object discovery and the `wwck195109.pdf` locator.
- Accounting remains 198 / 166 / 10 and 17/17 provenance repairs, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-GOOGLE-BOOKS-JI15-NONSEARCHABLE-AND-API-QUOTA-BOUNDARY-IL.md`. Research record: `docs/research/ZIWEI-GOOGLE-BOOKS-JI15-NONSEARCHABLE-AND-API-QUOTA-BOUNDARY-R1.json`.


## Progress — Batch 12IM

- The exact 2009 Ji Shuying pagination calibration gains scoped anchors at p.83 (Lun Ming; first-party journal reference) and pp.210–211 (Zhang Shouyong / Ming Ruyintang 《洛阳伽蓝记》; authorized author-text citation with institutional publication confirmation).
- Existing chapter-structure control binds these contexts to Chapters 5 and 14 respectively. They are topical-page anchors only, not chapter start/end pages.
- The six-point calibration remains anti-interpolation: Chapter 9 exact start/end pages and direct text remain unresolved/not reviewed.
- No target-acquisition, genealogy, runtime or product change occurs; accounting remains 198 / 166 / 10 and 17/17 provenance repairs, with zero algorithm defects/reopens/candidate collapses.

Batch document: docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JI-SHUYING-2009-PAGINATION-ANCHOR-EXTENSION-IM.md. Research record: docs/research/ZIWEI-JI-SHUYING-2009-PAGINATION-ANCHOR-EXTENSION-R1.json.


## Progress — Batch 12IN

- A secondary Wikisource discovery control records another 1951 `《文物参考资料》` item as `CNKI WENW195106001`; this establishes only a legacy identifier-pattern lead, not the target issue-9 code.
- Probe 1 attempted hypothetical `WENW195109001–040` static URLs and all failed before content retrieval on TLS certificate hostname mismatch. The resulting zero positives have no negative authority.
- Probe 2 first calibrated known-positive `WENW195106001` on four safe public variants: HTTPS www = certificate hostname mismatch; HTTPS apex = timeout; HTTP www = empty HTTP 418; HTTP apex = timeout. With zero viable positive-control routes, target enumeration was deliberately skipped.
- TLS verification was never disabled; no insecure curl, login, captcha bypass, paid/download endpoint or account action was used. Exact target CNKI ID, static page and direct 1951 article text remain unresolved/not reviewed.
- Product/accounting remains 198 / 166 / 10 and 17/17 provenance repairs, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-CNKI-WENW195109-LEGACY-INDEX-TRANSPORT-BOUNDARY-IN.md`. Research record: `docs/research/ZIWEI-CNKI-WENW195109-LEGACY-INDEX-TRANSPORT-BOUNDARY-R1.json`.

## Progress — Batch 12IO

- National Library of China Press first-party `ProductList.aspx` paging was calibrated using the source-emitted ASP.NET postback contract. The exact July-2009 window resolves to list page 361, which directly emits `ProductView.aspx?Id=4660` for 《冀淑英古籍善本十五讲》; no product-id guessing was used.
- Product 4660 directly closes 冀淑英著 / 李文洁插图, ISBN `978-7-5013-4063-7`, publication date 2009-07-29, edition B1 and print date 2009-07-01. This is a first-party publisher identity upgrade, not direct Chapter-9 page evidence.
- The product-page `CatalogPrecisFile` “目录附件下载” anchor has no `href`, no matching script assignment and no matching hidden attachment field on the reviewed HTML. The `Booktext` TXT postback was not invoked.
- The publisher's current public Rid=2 “目录及部分内容页” list contains exactly one unrelated item, 《中国图书馆馆史》（全四册）综合索引. Target nonlisting is route-scoped only and does not authorize a no-attachment-ever inference.
- Chapter 9 《铁琴铜剑楼藏书的收购入藏》 exact page range remains `UNRESOLVED`; direct Chapter-9 text remains `NOT_REVIEWED`. Linear/proportional interpolation remains forbidden.
- Product/accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 17 of 17 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NLCPRESS-JI15-FIRST-PARTY-PRODUCT-IDENTITY-AND-TOC-ATTACHMENT-BOUNDARY-IO.md`. Research record: `docs/research/ZIWEI-NLCPRESS-JI15-FIRST-PARTY-PRODUCT-IDENTITY-AND-TOC-ATTACHMENT-BOUNDARY-R1.json`.


## Progress — Batch 12IP

- National Library of China Press Product 4660's source-emitted public `Booktext` postback is now directly tested. The metadata-only probe returns HTTP 200 / `application/octet-stream` / `Content-Length: 739` with a repaired `Content-Disposition` filename `冀淑英古籍善本十五讲.txt`; no response body was read in that phase.
- Because the declared object is only 739 bytes, a second probe allows a maximum 4096-byte read. It recovers exactly 739 bytes, SHA-256 `c79284ab5f39ed7b8b48e8b1071b008990c583314455c7abf00699cd1fe4d1d3`, decodes as GB18030 and normalizes to 382 characters. Raw text is neither logged nor saved.
- The bounded payload contains the target book title and a `目录` marker, but none of the exact Chapter 9, 10, 11, 12 or 15 titles. It is therefore not promoted to full-book text or a page-numbered fifteen-lecture TOC witness.
- Chapter 9 exact page range remains `UNRESOLVED`; direct Chapter-9 text remains `NOT_REVIEWED`; Chapter 10/11 exact pagination remains `UNRESOLVED`. Anti-interpolation controls remain unchanged.
- Product/accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 17 of 17 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NLCPRESS-JI15-FIRST-PARTY-BOOKTEXT-BOUNDED-PAYLOAD-BOUNDARY-IP.md`. Research record: `docs/research/ZIWEI-NLCPRESS-JI15-FIRST-PARTY-BOOKTEXT-BOUNDED-PAYLOAD-BOUNDARY-R1.json`.


## Progress — Batch 12IQ

- CiNii NCID `BB00252412` closes the exact 2009 / 241p / ISBN `9787501340637` object and source-emits Japanese university-library OPAC routes. This batch uses those routes for content-enhancement inspection, not for holding-count inflation.
- Kyoto KULINE exact record source-emits both openBD and BOOKデータASP calls. A same-session headless-Chrome render returns `目次・あらすじの電子情報はありません。` for openBD and `あらすじ・目次の情報はありません。` for BOOKデータASP.
- Ritsumeikan RUNNERS source-emits BOOKデータASP and the rendered block likewise returns `あらすじ・目次の情報はありません。`. Tenri exposes exact bibliographic identity but no observed content-enhancement block; UTokyo currently returns HTTP 202 with an empty body and carries no negative-content authority.
- Official public openBD GET for ISBN `9787501340637` returns HTTP 200 / 6-byte JSON `[null]`, SHA-256 `1d8fc6ceb1f94c6326d6d5483d258fcb2e179e9869325b245d105c2219bf69fd`.
- These results close only the tested current public content-enhancement routes. They do not prove the physical book lacks a contents page. Chapter 9 exact page range and direct text, plus Chapter 10/11 exact pagination, remain unresolved; interpolation remains forbidden.
- Product/accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 17 of 17 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JI-SHUYING-2009-JAPAN-OPAC-OPENBD-BOOKDATA-PUBLIC-CONTENT-BOUNDARY-IQ.md`. Research record: `docs/research/ZIWEI-JI-SHUYING-2009-JAPAN-OPAC-OPENBD-BOOKDATA-PUBLIC-CONTENT-BOUNDARY-R1.json`.


## Progress — Batch 12IR

- National Library of China Press ProductList page 315 source-emits `ProductView.aspx?Id=5325` for 《赵万里文集·第一卷》. Product 5325 directly matches the target series/first-volume identity and ISBN `9787501346653`; no product-id guessing is used.
- Product 5325's public `Booktext` postback returns HTTP 200 / `application/octet-stream` / 464 bytes. The complete sub-4-KiB payload hashes to `6cc2f2aecebdbb31294bad9149075dba0aa0aa2bb2a9e778474fb44e9b43529e`, decodes as GB18030 to 245 normalized characters, and contains neither literal p.197 nor the target Yongle-exhibition or Qu-donation term sets. Raw text is not logged or saved.
- `CatalogPrecisFile` has no href. The publisher's current public `Rid=3` ebook resource center has one page and lists neither the target title nor ISBN and exposes zero `DownloadView.aspx` objects. This is route-scoped nonlisting only.
- Open Library independently binds ISBN `9787501346653` to edition `/books/OL30454631M` / work `/works/OL22369963W`, 2011, volume 1, first edition; current `ocaid=null` and covers=null, so no linked scan object is observed. Internet Archive exact-ISBN search returns zero, while Google Books remains HTTP 429 quota-limited.
- Direct 2011 p.197 remains `NOT_REVIEWED`. Batch 12IG's official 2026 quotation bridge and Batch 12HG's NDL physical holding remain separate evidence layers; NDL paid remote copying remains explicit-authorization-gated by Batch 12IH.
- Product/accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 17 of 17 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHAO-WANLI-WENJI-V1-NLCPRESS-OPENLIBRARY-PUBLIC-PREVIEW-BOUNDARY-IR.md`. Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENJI-V1-NLCPRESS-OPENLIBRARY-PUBLIC-PREVIEW-BOUNDARY-R1.json`.


## Progress — Batch 12IS

- Batch 12HI's NDL physical identity is not double-counted. The same exact paper bound volume `R100000002-Ia0000051292-i25241426` remains 《文物参考资料》 `2(7)-2(12) 1951`, call `Z8-AC150`, material form `紙`, and explicitly contains target volume-2 issue 9.
- NDL OpenSearch `dpid=ndl-dl` is positive-controlled with 《吾輩は猫である》: HTTP 200 / 165 results and direct `dl.ndl.go.jp/pid/` references, proving the provider route is functioning.
- Against that control, target serial traditional/simplified forms under `ndl-dl` return zero, target serial under `ndl-dl-open` returns zero, and the Zhao Wanli article title under `ndl-dl` returns zero. Without provider restriction, the 1951 serial query returns 8 results including the exact NDL paper bound volume.
- The exact public item page has no `dl.ndl.go.jp` or PID link. This closes only the current NDL Digital/provider route; it is not a global no-digitization claim.
- `wwck195109.pdf`, a direct issue-9 scan and Zhao Wanli pp.221–233 remain unrecovered/not reviewed. 2011 《赵万里文集》第1卷 p.197 remains not reviewed.
- Product/accounting remains 198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 17 of 17 provenance defects repaired / zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NDL-WENWU-CANKAO-1951-H2-DIGITAL-PROVIDER-BOUNDARY-IS.md`. Research record: `docs/research/ZIWEI-NDL-WENWU-CANKAO-1951-H2-DIGITAL-PROVIDER-BOUNDARY-R1.json`.


## Progress — Batch 12IT

- Internet Archive Advanced Search returns zero for exact 1951 serial title, exact filename `wwck195109.pdf`, and the exact Zhao Wanli article title.
- Open Library title/year search, Wikimedia Commons file-namespace search and Chinese Wikisource search also return zero on the tested public routes.
- Google Books returns HTTP 429 quota exceeded and HathiTrust's tested catalog export returns HTTP 403; neither route is assigned negative evidentiary authority.
- No open object ID, bytes, hash, page count or scan provenance is recovered for `wwck195109.pdf`; the commercial manifest remains locator-only.
- Product/accounting remains 198 / 166 / 10 and 17/17 provenance repairs, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENWU-1951-V2N9-OPEN-REPOSITORY-CATALOG-BOUNDARY-IT.md`. Research record: `docs/research/ZIWEI-WENWU-1951-V2N9-OPEN-REPOSITORY-CATALOG-BOUNDARY-R1.json`.


## Progress — Batch 12IU

- Kansai University Library, Kyoto University KULINE and NIJL OPAC directly bind 《趙萬里文集》 volume 1 to NCID `BB08679512` and ISBN `9787501346653`.
- Static and rendered public pages expose neither literal p.197 nor the configured target quotation terms.
- Kansai renders that no electronic contents/summary information is available; Kyoto's openBD and BOOKデータASP blocks independently report no contents/summary information.
- Saitama and Tohoku are current anonymous-route access boundaries (HTTP 403 in the static probe) and receive no negative textual authority.
- Direct 2011 p.197 remains NOT_REVIEWED. Product/accounting remains 198 / 166 / 10 and 17/17 provenance repairs, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHAO-WANLI-WENJI-V1-JAPAN-OPAC-PUBLIC-CONTENT-BOUNDARY-IU.md`. Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENJI-V1-JAPAN-OPAC-PUBLIC-CONTENT-BOUNDARY-R1.json`.


## Progress — Batch 12IV

- Google Books non-API public ISBN VID HTML returns HTTP 200 and visibly binds 《趙万里文集》 / ISBN `9787501346653` / 國家圖書館出版社 / 2011, while stating that no ebook is provided.
- No literal p.197, configured target quotation term, or actual page-level preview is exposed.
- The same Google aggregation page displays “第3卷” / 526 pages, conflicting with publisher/Open Library/CiNii institutional volume-1 identity. That Google display is quarantined as an external metadata conflict and cannot overwrite volume identity.
- HathiTrust is 403; WorldCat is 429/403; LOC exact ISBN/LCCN web searches return zero current results; Stanford's current ISBN search shell does not bind the target; Princeton redirects to a challenge page. These are route-scoped boundaries only.
- Direct 2011 p.197 remains NOT_REVIEWED. Product/accounting remains 198 / 166 / 10 and 17/17 provenance repairs, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHAO-WANLI-WENJI-V1-INSTITUTIONAL-CATALOG-HTML-BOUNDARY-IV.md`. Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENJI-V1-INSTITUTIONAL-CATALOG-HTML-BOUNDARY-R1.json`.


## Progress — Batch 12IW

- Stanford SearchWorks record locator `8440171` was probed only through anonymous normal access. Static GET returns HTTP 200 but a 5101-byte frontend shell; no target title/ISBN/page-count field or source-emitted export route is present in that runner response.
- Headless Chrome renders a 336-byte `Request Rejected` page rather than the bibliographic record, with zero source-emitted links. This is an execution-environment access boundary, not evidence that Stanford's underlying record lacks contents or pagination.
- Public search indexing remains discovery-locator scope only and is not promoted to direct Stanford first-party record content. No Chapter 9 or Chapter 10/11 page inference is authorized.
- Chapter 9 exact page range remains UNRESOLVED / direct text NOT_REVIEWED; accounting remains 198 / 166 / 10 and 17/17 provenance repairs, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JI-SHUYING-2009-STANFORD-EXACT-RECORD-ACCESS-BOUNDARY-IW.md`. Research record: `docs/research/ZIWEI-JI-SHUYING-2009-STANFORD-EXACT-RECORD-ACCESS-BOUNDARY-R1.json`.


## Progress — Batch 12IX

- Google Books exact ISBN public HTML source-emits object `k4MzlCiOPIcC`, `output=html_text`, an alternate object `8vHm2Qj1JO8C`, and the in-book `q=` search contract. No guessed object ID or endpoint is used.
- Direct page-numbered TOC text closes Chapter 9 at p.133, Chapter 10 at p.163, Chapter 11 at p.179, Chapter 12 at p.189, with later starts p.201 / p.209 / p.223 and postscript p.239.
- Direct in-book snippets show Chapter-9 material at p.162 while Chapter 10 starts p.163; Chapter 9 is therefore directly closed as pp.133–162. The three-batch sale/donation narrative is directly page-bound at p.139, and the first 304-sale / 52-donation figures at p.140.
- Chapter 10 start p.163 is direct; its current structural interval is [163,179), while p.178 itself is not claimed as directly reviewed. Chapter 11 is directly closed as pp.179–188 because p.188 content is observed and Chapter 12 starts p.189.
- Product/accounting remains 198 / 166 / 10 and 17/17 provenance repairs, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JI-SHUYING-2009-GOOGLE-BOOKS-PAGE-NUMBERED-SNIPPET-ANCHORS-IX.md`. Research record: `docs/research/ZIWEI-JI-SHUYING-2009-GOOGLE-BOOKS-PAGE-NUMBERED-SNIPPET-ANCHORS-R1.json`.


## Progress — Batch 12IY

- Ji Shuying Chapter 9 page-numbered snippets now directly support the three-batch mixed sale+donation program: p.139 states three batches with sale and donation paired; p.162 reviews the three batches.
- p.140 directly closes first-batch 304 sold + 52 donated. p.143 directly closes second-batch 123 sold and the Ding Fubao six-book purchase-to-donation intermediary route. p.155 directly establishes a third batch of purchased books.
- Exact 1950-01-07, 1950-03 and 1953-03 strings are not directly closed on the current snippet surface. 97-title donation and 300-plus third-batch figures remain secondary/unresolved and are not promoted.
- NLC 20/190, Study Times 699, NLC 700-plus and Zhao-1951 62-title scopes remain unreconciled; no arithmetic normalization is authorized.
- No target 3482/3483 transaction mode or date is selected. Product/accounting remains 198 / 166 / 10 and 17/17 provenance repairs, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JI-SHUYING-2009-TIEQIN-DIRECT-TRANSACTION-CHRONOLOGY-IY.md`. Research record: `docs/research/ZIWEI-JI-SHUYING-2009-TIEQIN-DIRECT-TRANSACTION-CHRONOLOGY-R1.json`.


## Progress — Batch 12IZ

- Exact Google Books object `BZ0M0gEACAAJ` preserves the 1997 bibliographic identity but exposes no usable in-book q= contract; its source-emitted html_text route returns HTTP 403.
- The primary object source-emits alternate `RuGEAAAAIAAJ`, which does expose in-book q= search links. Targeted search is therefore source-authorized, not guessed.
- The alternate does **not** expose usable printed page numbers for pp.446–449. Searches for target titles and 3482/3483/03482/03483 do not produce direct target snippets, but zero hits carry no full-text absence authority.
- Positive-looking hits are explicitly classified as false positives: 瞿氏 → 1932 瞿兑之 deposit record; 赵万里 → staff chronology; 这些善本入藏本馆 → tokenized unrelated 善本/入藏 passages; 可为全国之冠 → unrelated general library-takeover statement.
- NLC-2024 pp.446–449 citation bridge remains intact, but direct 1997 page text/images and exact internal document identity remain unresolved. Target item transaction mode remains unresolved.
- Product/accounting remains 198 / 166 / 10, provenance defects 17/17, and zero chart-algorithm defects/reopens/candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-BEITU1997-GOOGLE-BOOKS-ALTERNATE-INBOOK-SEARCH-BOUNDARY-IZ.md`. Research record: `docs/research/ZIWEI-BEITU1997-GOOGLE-BOOKS-ALTERNATE-INBOOK-SEARCH-BOUNDARY-R1.json`.


## Progress — Batch 12JA

- Exact ISBN Google Books HTML for 9787501346653 source-emits concrete object `swWenQAACAAJ`; the object ID is not guessed.
- The object carries the same ISBN but visibly displays 第3卷 and exposes no usable in-book q= contract or alternate object. It therefore upgrades the existing 12IV Google metadata conflict to a source-emitted-object conflict, not a volume-1 recovery.
- Volume-1 identity remains controlled by National Library of China Press Product 5325, NDL UM11-C247, Open Library OL30454631M and CiNii/Japanese institutional OPAC bindings.
- `swWenQAACAAJ` is forbidden as a volume-1/p.197 witness. Direct 2011 p.197 remains NOT_REVIEWED.
- Product/accounting remains 198 / 166 / 10, provenance defects 17/17, with zero chart-algorithm defects/reopens/candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHAO-WANLI-WENJI-V1-GOOGLE-BOOKS-SOURCE-EMITTED-OBJECT-CONFLICT-JA.md`. Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENJI-V1-GOOGLE-BOOKS-SOURCE-EMITTED-OBJECT-CONFLICT-R1.json`.


## Progress — Batch 12JB

- CiNii NCID `AA11467834` source-emits the 奈良文化財研究所 OPAC route; the first-party item closes the target as `Vol.2, no.9 / 1951`, local bib `SB00333452`, hold `TS00027259`, Document ID `10024273`, request number `202.505||3||1951-9C`.
- Anonymous runner probe `36752861983` / artifact `11115411027` / digest `sha256:062324181d463477152c18c189152474d334ec842ac41ae09a0bf52304455884` reproduces both exact-item identity and the current Nabunken remote-copy policy.
- The public item surface exposes no direct Zhao pp.221–233 page surrogate; original 1951 pages and direct 1951-vs-2011 textual identity remain NOT_REVIEWED / UNRESOLVED.
- Current official policy does not accept direct copy inquiries from individuals; individuals are directed through an institution library or nearest public library, with listed B/W ¥60/page + shipping and color ¥200/page + shipping and an institutional NACSIS-ILL route. No request, ILL, identity transmission or payment was made.
- This is an item/access-policy precision upgrade only. Product/accounting remains 198 / 166 / 10, provenance defects 17/17, with zero chart-algorithm defects, reopens or candidate collapses and no transmission-graph change.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENWU-CANKAO-1951-V2N9-NABUNKEN-EXACT-ISSUE-AND-REMOTE-COPY-BOUNDARY-JB.md`. Research record: `docs/research/ZIWEI-WENWU-CANKAO-1951-V2N9-NABUNKEN-EXACT-ISSUE-AND-REMOTE-COPY-BOUNDARY-R1.json`.


## Progress — Batch 12JC

- Current university-library access guides document CNBKSY entry surfaces at `https://www.cnbksy.com/`, `/home` and `/v1`; Fudan describes campus-network access with off-campus VPN/proxy, while Tsinghua's 2026 trial notice describes campus-IP control.
- Anonymous probe run `36757445087` / artifact `11116971947` / digest `sha256:cf98bdd869640721fddc9fe8b39719b859ea040b9055a6c4734e031d6f9fdfbf` returns HTTP 412 on all three documented entry URLs.
- None of the three response surfaces emits a public search form or candidate search/query/article link. The probe therefore submits **no Zhao Wanli target query** and does not guess an API endpoint.
- This is a current public access/search-contract boundary only. HTTP 412 is not a zero-result search and has no authority for target absence, corpus absence or text absence.
- Direct 2011 p.197, direct 1951 pp.221–233, direct 1997 pp.446–449 and public `wwck195109.pdf` bytes all remain unresolved/not reviewed. Product/accounting remains 198 / 166 / 10 and provenance defects 17/17, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENWU-1951-CNBKSY-PUBLIC-SEARCH-CONTRACT-ACCESS-BOUNDARY-JC.md`. Research record: `docs/research/ZIWEI-WENWU-1951-CNBKSY-PUBLIC-SEARCH-CONTRACT-ACCESS-BOUNDARY-R1.json`.

## Progress — Batch 12JD

- NLC 2019 official reprint explicitly attributes Zheng Zhenduo's 《关于〈永乐大典〉》 to People's Daily 1951-08-13.
- NLC 2025 official PDF exposes a conflicting 1951-08-31 bibliography-line date for that separate Zheng article while independently preserving the Zhao Wanli 1951 issue-9 pp.221–233 locator.
- Probe run 36759879758 / artifact 11118018737 / digest sha256:27cbf81f6a2a68128afa7f7bb935532085d85f16c846cbea0d3edbed6fc4ac7d follows source-emitted August navigation. The public transcription contains the article on 8/13 page 3 and not on the source-emitted 8/31 page.
- Current control: 1951-08-13 HIGH confidence; NLC-2025 1951-08-31 quarantined pending official newspaper-image review. No absolute physical 8/31 absence claim is made.
- No change to direct-review status of 2011 p.197, 1951 pp.221–233 or 1997 pp.446–449; accounting remains 198 / 166 / 10 and provenance defects 17/17.

Batch document: docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHENG-YONGLE-1951-0813-0831-PUBLICATION-DATE-CONFLICT-JD.md. Research record: docs/research/ZIWEI-ZHENG-YONGLE-1951-0813-0831-PUBLICATION-DATE-CONFLICT-R1.json.


## Progress — Batch 12JE

- Official People Data / People's Daily entry `https://data.people.com.cn/rmrb` returns HTTP 200 and directly emits a same-host GET search form to `/rmrb/s` plus a source-emitted search-center link.
- Probe run `36766920501` / artifact `11120444534` / digest `sha256:4cbe562934dfc3e4ee4cbb06bc93ca8493a8dd586290051de5ca3e101f4829e0` first calibrates the form with a current article title directly emitted by the same official entry page.
- Positive control fails at the application layer: HTTP transport is 200, but the body is an 846-byte `500页面 / 网络不给力` wrapper with SHA-256 `d7aae3f0a88b671c7f7617d3ef8639f141e389d2396bfa967a743671cd9c8a7a`, no query literal and no result anchors.
- `关于《永乐大典》`, `关于永乐大典` and `永乐大典` all return the identical 846-byte / identical-hash wrapper. Therefore these are not zero-result searches and cannot support 1951-08-31 absence or 1951-08-13 official-archive hit claims.
- Batch 12JD remains unchanged: 1951-08-13 stays HIGH-confidence controlling date; 1951-08-31 remains quarantined pending official newspaper image review.
- Direct 2011 p.197, direct 1951 pp.221–233 and direct 1997 pp.446–449 remain unresolved. Product/accounting remains 198 / 166 / 10 with provenance defects 17/17 and zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-RMRB-OFFICIAL-ARCHIVE-PUBLIC-SEARCH-EXECUTION-BOUNDARY-JE.md`. Research record: `docs/research/ZIWEI-RMRB-OFFICIAL-ARCHIVE-PUBLIC-SEARCH-EXECUTION-BOUNDARY-R1.json`.


## Progress — Batch 12JF

- Hardened anonymous probe run `36774331720` / artifact `11125625596` / digest `sha256:2f2fcfb3976b2198ac36bf86cff46bd7c434e947191d4e6d5ac5b2409a405dd3` directly rechecks the 51古书网 `wwck195109.pdf` manifest without login, payment, download-link following or TLS bypass.
- The page is HTTP 200 / 48,390 bytes / SHA-256 `959db6931f9f51cce7f1349abd08829a4cfa261144d2076c4292f6ed5d9e82c0`, and directly contains the exact filename plus `9.73 MB`. It has only 2 anchors total and emits zero candidate PDF/download/sample/attachment/net-disk links and zero direct-PDF candidates.
- Therefore `wwck195109.pdf` remains a commercial manifest filename/size locator; no open-object ID, bytes, hash of the target PDF, page count, scan provenance or lawful public-download identity is recovered. Direct Zhao pp.221–233 remain NOT_REVIEWED.
- The separately indexed xy980 route is connection-refused from the controlling runner and remains an unresolved discovery lead only; this is not negative evidence and not an independent object witness.
- Direct 2011 p.197 remains the highest next gate, with 1951 pp.221–233 and 1997 pp.446–449 in parallel. Product/accounting remains 198 / 166 / 10 and provenance defects 17/17, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENWU-1951-WWCK195109-COMMERCIAL-MANIFEST-SOURCE-EMITTED-ROUTE-BOUNDARY-JF.md`. Research record: `docs/research/ZIWEI-WENWU-1951-WWCK195109-COMMERCIAL-MANIFEST-SOURCE-EMITTED-ROUTE-BOUNDARY-R1.json`.


## Progress — Batch 12JG

- NLC homepage and resource-search page are both HTTP 200 and directly source-emit `http://find.nlc.cn/search/doSearch` as the “文津搜索” destination, closing route identity at first-party level.
- Neither reviewed NLC page emits an HTML form or named query parameter. The visible search input is JavaScript-controlled and has no reproducible field name.
- Controlling probe run `36816684951` / job `110223169684` / artifact `11141249055` / digest `sha256:6bc3cb1978f42e452b0845edd65839ac55aa67b4e866fa19b957126885ad1ec4` gets a timeout on `https://find.nlc.cn/` and HTTP 500 on the exact source-emitted `http://find.nlc.cn/search/doSearch` route with no invented parameters.
- No target title/ISBN query is submitted. Therefore no Wenjin zero-result/absence conclusion is authorized, and direct 2011 p.197 remains NOT_REVIEWED.
- Product/accounting remains 198 / 166 / 10 and provenance defects 17/17, with zero chart-algorithm defects, reopens or candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHAO-WANLI-WENJI-V1-NLC-WENJIN-PUBLIC-SEARCH-CONTRACT-BOUNDARY-JG.md`. Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENJI-V1-NLC-WENJIN-PUBLIC-SEARCH-CONTRACT-BOUNDARY-R1.json`.

## Progress — Batch 12JH

- Official NDL Reference Cooperative Database directly source-emits the NDL Digital Collection search URL and full public keyword parameter structure; endpoint/parameters are not guessed.
- Controlling run `36819382858` / job `110231432661` / artifact `11142424009` / digest `sha256:26e3cd1c25d2a755d753feda03b6faef8c5c49c18f92975b5b4a47504d9bb1bc` executes the positive control and seven target variants.
- Every query returns the identical 4,298-byte static shell (`sha256:9464957293e820db57d597624e2797b50402f0c3434d62d6de9d656f7a187b4f`) with no query echo, result count or PID; the positive control therefore does not calibrate a result surface.
- No target zero-result/absence conclusion is authorized, no digital object is recovered, and direct 2011 p.197 / 1951 pp.221–233 remain NOT_REVIEWED.
- Product/accounting remains 198 / 166 / 10, provenance defects 17/17, and zero chart-algorithm defects/reopens/candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NDL-DIGITAL-ZHAO-WANLI-WENWU-SOURCE-EMITTED-SEARCH-BOUNDARY-JH.md`. Research record: `docs/research/ZIWEI-NDL-DIGITAL-ZHAO-WANLI-WENWU-SOURCE-EMITTED-SEARCH-BOUNDARY-R1.json`.


## Progress — Batch 12JI

- National Library of China Press Product 11443 directly binds Liu Bo's 2021 《赵万里传》, ISBN 9787501371655, and a source-emitted public Booktext postback.
- The same first-party page states Liu Bo joined the 《赵万里文集》 editorial team in 2010 and exposes Chapter 8 headings `劝导藏家捐赠图书 / 255` and `大举购入善本古籍 / 258`.
- The literal `197` on this biography page is not the target 2011 Wenji page: the first-party TOC binds it to the unrelated entry `弢翁挚友 / 197`. Same page number therefore cannot be collapsed across works.
- Probe run `36824880534` / job `110248229760` / artifact `11144523100` / digest `sha256:a734134d74bbe1de922954f1b4f0977168827ce3320a03ee2ae45e3db69cf885` follows only the source-emitted Booktext postback. It returns 6,496 bytes, GB18030, SHA-256 `3da910b9bd88ef8fe6fe3318c814faeda10e2283b12e038760b0b523aa4a4312`; raw text is neither logged nor stored.
- The bounded public payload contains none of the configured Qu/Ding/1951 target quotation tokens. This is a payload-scoped boundary, not an absence claim about the physical biography.
- Direct 2011 《赵万里文集》第1卷 p.197, direct 1951 pp.221–233 and direct 1997 pp.446–449 remain NOT_REVIEWED. Product/accounting remains 198 / 166 / 10, provenance defects 17/17, and zero chart-algorithm defects/reopens/candidate collapses. `TRANSMISSION_IMPACT=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHAO-WANLI-ZHUAN-NLCPRESS-EDITORIAL-BRIDGE-JI.md`. Research record: `docs/research/ZIWEI-ZHAO-WANLI-ZHUAN-NLCPRESS-EDITORIAL-BRIDGE-R1.json`.


## Progress — Batch 12JJ

- Shanghai Academy of Social Sciences Library's first-party old-newspaper directory directly closes a Shanghai 《文汇报》 holding covering 1951年1－12月. The same page separately lists 《文汇报(香港)》 with 1951年1－3月, so the Shanghai/Hong Kong same-title ambiguity is controlled at holding level.
- Tsinghua Alumni's institutional retrospective independently corroborates that Zhao Wanli hosted the 《永乐大典》 exhibition in 1951 and wrote 《〈永乐大典〉展览的意义》. It does not provide an August 18 date or Wenhui publication venue.
- Public Web discovery supplies a secondary chronology lead claiming publication on 1951-08-18 in Shanghai 《文汇报》, but the controlling GitHub runner cannot directly retrieve that secondary page under the tested public HTTPS/HTTP routes. It remains discovery scope only.
- Probe run `36828765852` / job `110260317546` / artifact `11146151782` / digest `sha256:c922718224ac493d59328c98e49fd99f1a181158e6855e13a982736106578f61` closes the SASS exact-year holding/disambiguation route and the Tsinghua article-identity control; it recovers no 1951-08-18 newspaper page or article text.
- Therefore 1951-08-18 Shanghai Wenhui publication remains `SECONDARY_LEAD_UNVERIFIED_BY_PRIMARY_PAGE`; first-publication status and the textual relationship to 《文物参考资料》 vol.2 no.9 pp.221-233 remain unresolved.
- Direct 2011 p.197 and direct 1951 《文物参考资料》 pp.221–233 remain NOT_REVIEWED. Product/accounting remains 198 / 166 / 10, provenance defects 17/17, zero chart-algorithm defects/reopens/candidate collapses, and `TRANSMISSION_IMPACT=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHAO-WANLI-WENHUIBAO-1951-0818-SASS-HOLDING-ROUTE-JJ.md`. Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENHUIBAO-1951-0818-SASS-HOLDING-ROUTE-R1.json`.


## Progress — Batch 12JK

- National Library of China's official-hosted Liu Peng review PDF is directly recovered: 755,701 bytes / 17 pages / SHA-256 `08bf6adcf9a2d200128a80b26156f9de06731094426a116c44ae02386822af20`.
- No-OCR extraction of PDF page 5 / printed page 10 closes the bibliographic bundle: Zhao Wanli, 《永乐大典展览的意义——一九五一年八月北京图书馆举办》, 《文物参考资料》, 1951年第9期, pp.221–233.
- Probe run `36829969296` / job `110264093618` / artifact `11147240797` / digest `sha256:4c19f7cff9fdec4c2e24b8fef12578345ba8c195cc3594810924311a2a215c60` reproduces the official PDF and target text-layer bundle without OCR.
- The target review page contains neither 《文汇报》 nor 8月18日, but that omission has zero authority to disprove the Batch 12JJ secondary newspaper lead. Modern review bibliography is not primary 1951 publication evidence.
- Therefore Wenwu issue-9 is HIGH-confidence modern institutional bibliographic control; 1951-08-18 Shanghai Wenhui remains `SECONDARY_LEAD_UNVERIFIED_BY_PRIMARY_PAGE`; first-publication status and Wenhui↔Wenwu textual/transmission relation remain unresolved.
- No direct 1951 target page or 2011 p.197 is newly reviewed. Product/accounting remains 198 / 166 / 10, provenance defects 17/17, and zero chart-algorithm defects/reopens/candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHAO-WANLI-WENWU-WENHUI-BIBLIOGRAPHIC-TENSION-JK.md`. Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENWU-WENHUI-BIBLIOGRAPHIC-TENSION-R1.json`.


## Progress — Batch 12JL

- Open Library exact ISBN `7805314705` closes the 1997 《文汇报史略：1949.6–1966.5》 edition as `OL61042343M` / work `OL44697053W`, 330 pages, but `ocaid=null` and no linked scan.
- Google Books exact-ISBN HTTP 200 binds the same title/ISBN/year and source-emits object `4bmRAAAACAAJ`. The controlling probe follows that object directly.
- The followed object emits zero forms, zero `SearchWithinVolume`-style links, no snippet/full-view marker and no configured 1951 Zhao/Yongle target terms. The exact-ISBN page's sole `q=` link is a Google library-link redirect to WorldCat OCLC `1462561249`, not an in-book search contract.
- CiNii exact CRID currently returns HTTP 202 / empty body on the controlling runner; this is a transport boundary only and carries zero negative bibliographic authority.
- No 1951-08-18 newspaper page, no 《文物参考资料》 pp.221–233 text and no 2011 Wenji p.197 are recovered. First-publication/transmission status remains unresolved. Product/accounting remains 198 / 166 / 10; provenance defects 17/17; zero chart-algorithm defects/reopens/candidate collapses. `TRANSMISSION_IMPACT=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENHUI-SHILUE-1997-PUBLIC-PREVIEW-BOUNDARY-JL.md`. Research record: `docs/research/ZIWEI-WENHUI-SHILUE-1997-PUBLIC-PREVIEW-BOUNDARY-R1.json`.


## Progress — Batch 12JM

- Shanghai University Library's first-party 《报纸（合订本）馆藏目录》 is directly retrieved: HTTP 200 / 164,150 bytes / SHA-256 `a3a9b77e4eb0ab5b53d0c35ea7c9fc0de9bd6401eabf585a13da52c0f8734198`.
- Row 7 directly lists Shanghai 《文汇报》 with `1951(5-8)`, 新校区 / 嘉定校区 and shelves `6--10`. That holding range includes the calendar date 1951-08-18.
- The same first-party page separately lists row 53 《文汇报(香港版)》, so the Shanghai and Hong Kong newspaper identities are not collapsed.
- This closes an independent physical bound-volume access route only. No specific 1951-08-18 issue/page, Zhao article, or article text is directly reviewed; the secondary publication claim is not upgraded to primary-text status.
- Direct Wenhui 1951-08-18, direct Wenwu pp.221–233 and direct 2011 Wenji p.197 remain NOT_REVIEWED. Product/accounting remains 198 / 166 / 10; provenance defects 17/17; zero chart-algorithm defects/reopens/candidate collapses. `TRANSMISSION_IMPACT=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENHUIBAO-1951-0818-SHU-BOUND-VOLUME-HOLDING-ROUTE-JM.md`. Research record: `docs/research/ZIWEI-WENHUIBAO-1951-0818-SHU-BOUND-VOLUME-HOLDING-ROUTE-R1.json`.


## Progress — Batch 12JN

- Shanghai University Library's first-party `馆藏报纸目录（2025.10更新版）` is HTTP 200 / 338,548 bytes / SHA-256 `f421d3fbfdf3b508f50f8e4298e0d34f7649e8e3206e8da129c5841b65816a9c`.
- The current row 7 keeps Shanghai 《文汇报》 coverage `1951(5-8)` but now exposes rack `A7-1` and B/L under binding/holding columns. The same page legend maps B to 新校区期刊室 and L to 嘉定校区期刊室.
- Batch 12JM's legacy `6--10` locator is preserved as an earlier directory capture; present access planning uses the 2025.10 A7-1/B-L metadata. Coverage has not changed.
- SHU's first-party Digital Doubling Platform page is HTTP 200 / SHA-256 `9a9a79219c8271c13db9c31248d7d8fc4e32c5be773b8320442464e2e2c92ae5` and explicitly requires email appointment, staff reply and on-site fifth-floor terminal use. It does not bind the target Wenhui object and exposes no public remote target page.
- No email/appointment action is performed. Direct Wenhui 1951-08-18, Wenwu pp.221–233 and 2011 Wenji p.197 remain NOT_REVIEWED. Product/accounting remains 198 / 166 / 10; provenance defects 17/17; zero algorithm defects/reopens/candidate collapses. `TRANSMISSION_IMPACT=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENHUIBAO-SHU-2025-CURRENT-LOCATOR-AND-DIGITAL-ACCESS-BOUNDARY-JN.md`. Research record: `docs/research/ZIWEI-WENHUIBAO-SHU-2025-CURRENT-LOCATOR-AND-DIGITAL-ACCESS-BOUNDARY-R1.json`.


## Progress — Batch 12JO

- Wenhui Daily's official e-paper host `dzb.whb.cn` is investigated as a possible public historical-date route without constructing a 1951 target URL.
- Controlling run `36834874380` / job `110279768574` / artifact `11148592500` / digest `sha256:fdf0f44210a45e233995e7142734ac9e7d94c124d05c30dad1fdc83bd72b3783` times out on both the root and a known modern dated control.
- No source-emitted date-selection contract can be calibrated on the runner. The target date 1951-08-18 is not submitted and no historical absence inference is authorized.
- Direct Wenhui 1951-08-18, Wenwu pp.221-233 and 2011 Wenji p.197 remain NOT_REVIEWED. Accounting remains 198 / 166 / 10; provenance defects 17/17; zero algorithm defects/reopens/candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENHUI-OFFICIAL-EPAPER-PUBLIC-DATE-CONTRACT-BOUNDARY-JO.md`. Research record: `docs/research/ZIWEI-WENHUI-OFFICIAL-EPAPER-PUBLIC-DATE-CONTRACT-BOUNDARY-R1.json`.


## Progress — Batch 12JP

- Shanghai Library's current open-data surface and 2026 first-party CNBKSY API PDF are directly recovered. The documentation exposes `https://data.cnbksy.com/competitionSearch?key=[参数1]&searchContent=[参数2]` and explicitly requires a registration-issued APIKey.
- Controlling run `36835297124` / job `110281139580` / artifact `11149230659` / digest `sha256:ba99886b0530d83d9ae9badb267ca01510315901eff56d6f70cac99120a9bcc4` confirms the endpoint is live: bare request HTTP 200/JSON; documented sample syntax with empty key HTTP 500/JSON.
- No APIKey, registration, login, email action or target query is used. Empty-key failure is not a zero-result search and has no target absence authority.
- Shanghai Library's 2025 official introduction declares 中国近代报纸数字文献全库 as 1850–1952 / 4000+ newspapers, so 1951 is inside declared temporal coverage; specific Shanghai Wenhui inclusion is still unproved.
- Direct Wenhui 1951-08-18, Wenwu pp.221-233 and 2011 Wenji p.197 remain NOT_REVIEWED. Accounting remains 198 / 166 / 10; provenance defects 17/17; zero algorithm defects/reopens/candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-CNBKSY-CURRENT-OPEN-API-AUTH-BOUNDARY-JP.md`. Research record: `docs/research/ZIWEI-CNBKSY-CURRENT-OPEN-API-AUTH-BOUNDARY-R1.json`.


## Progress — Batch 12JQ

- Shanghai Library's first-party 2020 全国报刊索引 API sample bundle is directly recovered from the official open-data host: HTTP 200 / 230,672 bytes / SHA-256 `202429192ac1eb96193595099efb585e3221cea1d89726758f521c50f3013d79`.
- The ZIP contains one directory plus two PDFs. The logged legacy ZIP filenames reversibly normalize to a 2020 API 使用样例 PDF and a 2020 API 说明书 PDF; their SHA-256 values are `66ddfa18bb82f1207dbe5baae1062344cecd15e6a4759745827ed1c2c324cde9` and `61fadcda0a8617db389f4e8fbde05025a3ebed92a7b10584157b657cceb3f301`.
- 12JQ closes only public bundle/document identity. PDF body text and any credential-like example values are NOT_REVIEWED; no credential value is logged, saved or used and no target query is submitted.
- Historical public sample distribution does not grant current authorization and does not supersede Batch 12JP's 2026 registration-issued APIKey boundary. Direct Wenhui 1951-08-18, Wenwu pp.221–233 and 2011 Wenji p.197 remain NOT_REVIEWED.
- Accounting remains 198 / 166 / 10; provenance defects 17/17; zero algorithm defects/reopens/candidate collapses. `TRANSMISSION_IMPACT=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-CNBKSY-2020-PUBLIC-API-SAMPLE-BUNDLE-JQ.md`. Research record: `docs/research/ZIWEI-CNBKSY-2020-PUBLIC-API-SAMPLE-BUNDLE-R1.json`.


## Progress — Batch 12JR

- A corrected controlling runner probe directly retrieves Shanghai Library / CNBKSY annual open-data pages for 2020–2025 plus the current 2026 page, with page bytes and SHA-256 bound in the research record.
- 《中国近代报纸数字文献全库》 is explicitly present in the 2020, 2021 and 2022 first-party open-data listings, and absent from the corresponding 2023, 2024, 2025 and current 2026 listings. This is a listing-scope observation only: omission does not prove database nonexistence.
- Every annual page continues to source-emit a CNBKSY documentation/download object. The 2024 API PDF, the API PDF linked by the 2025 page, and the current 2026 API PDF are byte-identical: 332,913 bytes / SHA-256 7fc1d1d42bf30b639a03fee1a999d201d5c42f0a5272d8130fc03ea1b1877648. The 2025 page source-emits a /2024/ document path.
- Therefore API-document persistence cannot prove current dataset-scope continuity. Batch 12JP's APIKey requirement remains controlling, but current competitionSearch coverage of 1951 newspaper data is still UNRESOLVED until an authorized query or an explicit current scope statement closes it.
- The first 12JR probe run is explicitly superseded because requests.text misdecoded the Chinese pages; no research conclusion is accepted from that run. The corrected run is 36840258132 / job 110297437835 / artifact 11150672206 / digest sha256:f37730cb3c19bc1ca8e692a3b988ae585b03c13cf13985aacc65d916970936ea.
- No key, registration, login or target query is used. Direct Wenhui 1951-08-18, Wenwu pp.221–233 and 2011 Wenji p.197 remain NOT_REVIEWED. Accounting remains 198 / 166 / 10; provenance defects 17/17; zero algorithm defects/reopens/candidate collapses. TRANSMISSION_IMPACT=NONE.

Batch document: docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-CNBKSY-2020-2026-OPEN-DATA-LISTING-SCOPE-CHRONOLOGY-JR.md. Research record: docs/research/ZIWEI-CNBKSY-2020-2026-OPEN-DATA-LISTING-SCOPE-CHRONOLOGY-R1.json.


## Progress — Batch 12JS

- A 2003 contemporary web reprint explicitly labeled as sourced from 文汇报 directly reports donation to the National Library of China of 《文汇报60年报纸光盘》: 13 discs, declared coverage 1938-01 through 1998-12, all text and images, with date/name lookup. The retrieved object is 59,026 bytes / SHA-256 `3ff35d135af4fa2976273239ce08cf10a56526b3bd6b4634f8cdad075998071f`.
- The declared date range includes 1951-08-18, but this is coverage-level evidence only. No CD-ROM target query is submitted, no target article presence is proved, and no 1951 page is directly reviewed.
- NLC's current first-party main/service surfaces are directly retrieved. The service surface exposes catalog/digital-resource context and optical-disc service language, but neither reviewed page names 《文汇报60年报纸光盘》 or exposes an item-level record for it.
- The 2005 IFLA archive PDF could not be directly retrieved on the controlling runner: tested archive routes return HTTP 503 or connection failures. Therefore the separately discovered “61年全文数据光盘” wording is not upgraded in 12JS and must not be collapsed with the 2003 60-year donated object.
- Controlling run `36842368572` / job `110304235769` / artifact `11151074382` / digest `sha256:19b9a05049bbda7dcd43b92f151ab00f7aedb90d7e70bde64e6bf16b5cf8caad`. No login, reader account, registration, payment, copy request, private endpoint or target query is used.
- Direct Wenhui 1951-08-18, Wenwu pp.221–233 and 2011 Wenji p.197 remain NOT_REVIEWED. Accounting remains 198 / 166 / 10; provenance defects 17/17; zero algorithm defects/reopens/candidate collapses. `TRANSMISSION_IMPACT=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENHUI-60YEAR-CDROM-NLC-DONATION-AND-CURRENT-SERVICE-BOUNDARY-JS.md`. Research record: `docs/research/ZIWEI-WENHUI-60YEAR-CDROM-NLC-DONATION-AND-CURRENT-SERVICE-BOUNDARY-R1.json`.


## Progress — Batch 12JT

- The current NLC homepage is directly parsed and source-emits `http://opac.nlc.cn/` plus `http://read.nlc.cn/outRes/outResList?type=电子报纸`. The corrected controlling probe therefore distinguishes source-emitted HTTP from self-upgraded HTTPS.
- Exact HTTP routes are reachable: OPAC root HTTP 200 / 318 bytes / SHA-256 `999e28e32e671494ad7a97c0a46446f192c8767264adca9d068ef0c3f4fe2a68`; electronic-newspaper page HTTP 200 / 404,829 bytes / SHA-256 `b8991f6d96bb95e8fba6dff11866ece8b146ee097fa902d9afb25b0c7d7856cf`. Both HTTPS comparison routes time out.
- The electronic-newspaper landing page exposes fields `type`, `urlType`, `searchName`, and `ourReswords`, plus search/newspaper semantics, but no form is submitted. The page itself contains no `文汇报`, `文匯報`, `文汇报60年报纸光盘`, or `文汇报61年全文数据光盘` token.
- The prior 12JT run `36843786769` is superseded for protocol adjudication because it tested HTTPS only after recovering source-emitted HTTP hrefs. Controlling run `36844080482` / job `110309901228` / artifact `11152368933` / digest `sha256:dc4f1f29fe9cff4c640b6ba34a29c7e0eab3c7a7fb20f22daaab6ef5c2c334d2`.
- No login, reader account, form submission, target query, private endpoint or TLS bypass is used. Item-level Wenhui CD-ROM identity and direct 1951-08-18 page remain unresolved. Accounting remains 198 / 166 / 10; provenance defects 17/17; zero algorithm defects/reopens/candidate collapses. `TRANSMISSION_IMPACT=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NLC-SOURCE-EMITTED-OPAC-ELECTRONIC-NEWSPAPER-HTTP-ROUTE-CALIBRATION-JT.md`. Research record: `docs/research/ZIWEI-NLC-SOURCE-EMITTED-OPAC-ELECTRONIC-NEWSPAPER-HTTP-ROUTE-CALIBRATION-R1.json`.


## Progress — Batch 12JU

- Direct inspection of the current NLC `read.nlc.cn` electronic-resource page closes the public search contract without issuing a search: the button calls `getOutResSearch()`, which reads `ourReswords`, fixes `typeName="全部"`, and navigates by GET to `/outRes/outResList?type=<typeName>&searchName=<ourReswords>`.
- The same page's pagination code reuses the public `/outRes/outResList` path with `type`, `searchName`, `pageNo` and `urlType`. No form POST, login or private endpoint is required to describe this contract.
- Controlling run `36844745344` / job `110312077411` / artifact `11152144796` / digest `sha256:1fca09b8ec9b3db9a877c3d053601f9b9b8936bb65aeeb55d2b50b1beba0275f`. No query was submitted in 12JU.
- This contract is for NLC's current outRes external-resource list; it is not the OPAC catalog contract and cannot decide physical/CD-ROM holdings.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NLC-ELECTRONIC-NEWSPAPER-PUBLIC-SEARCH-CONTRACT-JU.md`. Research record: `docs/research/ZIWEI-NLC-ELECTRONIC-NEWSPAPER-PUBLIC-SEARCH-CONTRACT-R1.json`.

## Progress — Batch 12JV

- Using only the 12JU page-emitted anonymous GET contract, four resource-title searches were executed: `文汇报60年报纸光盘`, `文汇报`, `文匯報`, and `文汇报61年全文数据光盘`.
- All four return HTTP 200 and `pageTotal=0`. The queried term appears only as the page's `searchName` echo; no Wenhui result item/link is observed.
- The zero result is therefore authoritative only for the current anonymous NLC outRes external-resource index. It does **not** prove NLC OPAC nonholding, does not invalidate the 2003 donation report, and does not establish absence of the 1951-08-18 newspaper page.
- Controlling run `36845037948` / job `110313030409` / artifact `11153465153` / digest `sha256:82a139a7312863b38bb7096d4bb87c94d0790d16155e3b9f0475b46af86d5f64`. No person/date query, login, reader account or state-changing request is used.
- Accounting remains 198 / 166 / 10; provenance defects 17/17; zero algorithm defects/reopens/candidate collapses. `TRANSMISSION_IMPACT=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NLC-WENHUI-RESOURCE-TITLE-SEARCH-ZERO-RESULT-BOUNDARY-JV.md`. Research record: `docs/research/ZIWEI-NLC-WENHUI-RESOURCE-TITLE-SEARCH-ZERO-RESULT-BOUNDARY-R1.json`.


## Progress — Batch 12JW

- The NLC-homepage-emitted OPAC HTTP root is directly reachable on the controlling runner: HTTP 200 / 318 bytes / SHA-256 `999e28e32e671494ad7a97c0a46446f192c8767264adca9d068ef0c3f4fe2a68`.
- The separately source-emitted `http://opac.nlc.cn/F/?func=file&file_name=login-session` navigation times out on the same runner after 35 seconds. Therefore no form, input field or public catalog search action can be recovered from that page in 12JW.
- This is a transport/search-contract boundary only. No `func=find-*` or other Aleph query parameter is guessed, no title/person/date query is submitted, and no OPAC holding/nonholding conclusion is authorized.
- Batch 12JV's outRes zero-result boundary remains isolated from OPAC holdings. A current first-party public catalog alternative may be pursued only from source-emitted/reproducible routes.
- Controlling run `36845686120` / job `110315142748` / artifact `11153541592` / digest `sha256:2933160c6211d76c6ea25264241975fffed1f75f719b81acd509144ea770d039`.
- Direct Wenhui 1951-08-18, Wenwu pp.221–233 and 2011 Wenji p.197 remain NOT_REVIEWED. Accounting remains 198 / 166 / 10; provenance defects 17/17; zero algorithm defects/reopens/candidate collapses.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NLC-OPAC-PUBLIC-SEARCH-CONTRACT-TRANSPORT-BOUNDARY-JW.md`. Research record: `docs/research/ZIWEI-NLC-OPAC-PUBLIC-SEARCH-CONTRACT-TRANSPORT-BOUNDARY-R1.json`.


## Progress — Batch 12MF

- CADAL 首页公开 POST 检索表单已绑定；刊名及繁简文章名三个查询，首次与同会话校准均 HTTP 302 返回首页，未恢复目标对象。
- 这是访问重定向边界，不是零结果或目标缺失；原因未决，当前请求分支停止等待新第一方机制。
- 控制性 artifact ZIP 摘要已独立核验，成员 JSON 与任务日志一致。原刊 pp.221–233、2011 p.197 与上海文汇报日期页保持未核读。
- 无规则或传承图变更：198 / 166 / 10，17/17 provenance defects repaired，算法缺陷/重开/候选折叠均 0。

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENWU1951-CADAL-PUBLIC-SEARCH-REDIRECT-BOUNDARY-MF.md`. Research record: `docs/research/ZIWEI-WENWU1951-CADAL-PUBLIC-SEARCH-REDIRECT-BOUNDARY-R1.json`.


## Progress — Batch 12MG

- Documented HathiTrust brief/full OCLC lookup restores actual serial record 007245565 / OCLC18030125 / MARC880 文物参考資料 and 39 distinct digital items. Raw public response bytes are hash-bound and stored in the repository.
- Explicit 1951 items cover no.1–4; unyear-labelled UCD aggregate no.13–18/no.19–24 remain unbound to target issue 9. MARC974 y=1958 is not promoted to individual issue date.
- US metadata descriptors are Limited (search-only) for all 39 items; one source-emitted viewer GET is HTTP403. No original page is reviewed, no global absence or unrestricted-download claim is authorized.
- Next 12MH follows the newly recovered originating UCD record identity for chronological/access bridging. Matrix/accounting and historical text lineage remain unchanged.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENWU1951-HATHITRUST-OCLC-DIGITAL-INVENTORY-MG.md`. Research record: `docs/research/ZIWEI-WENWU1951-HATHITRUST-OCLC-DIGITAL-INVENTORY-R1.json`.


## Progress — Batch 12MH

- UC Davis originating record and raw UC network MARC are bound. Published anonymous frontend catalogue retrieval expands the initially empty item summary into 12 physical bound issues.
- All 12 physical barcodes and descriptions match the corresponding HathiTrust UCD htid suffixes and MARC974 enumeration; this is copy provenance, not 12 independent text votes.
- Explicit item years remain unavailable (year filter Other..); no.19–24 is not assigned to 1951 issue9. No original page or unrestricted-access claim, circulation request or reproduction submission is added.
- Next 12MI seeks direct numbering/year evidence and the source-record MARC776 Online version OCLC647437409. Accounting and historical text lineage remain unchanged.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENWU1951-UCD-PHYSICAL-DIGITAL-COPY-BINDING-MH.md`. Research record: `docs/research/ZIWEI-WENWU1951-UCD-PHYSICAL-DIGITAL-COPY-BINDING-R1.json`.


## Progress — Batch 12MI

- New Google Books no.19–24 object -RGcXtePnoQC is bound as a locator; generic UC origin and digitization date do not bind UCD copy or publication year.
- One source-emitted thumbnail was reviewed without resolving the target date or pp.221–233. Google API quota/CAPTCHA, HathiTrust target/control 403 and NLA challenge are access observations, not absence evidence.
- Next 12MJ deduplicates known exact-issue holdings before seeking a materially new first-party page mechanism. No repeat of failed endpoints without a new mechanism; all accounting and historical text votes remain unchanged.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENWU1951-GOOGLE-AGGREGATE-YEAR-BOUNDARY-MI.md`. Research record: `docs/research/ZIWEI-WENWU1951-GOOGLE-AGGREGATE-YEAR-BOUNDARY-R1.json`.

- Batch 12MK: HPA-ZIWEI-013 closes as a modern identity projection inheriting audited HPA-ZIWEI-002/004. A UI-only malformed/duplicate guard is repaired; 1440 normal JS outputs are unchanged. Matrix now has 198 rows / 167 audited / 10 missing-product rows; no chart algorithm reopen or new historical witness. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-BODY-PALACE-GANZHI-PROJECTION-AUDIT-MK.md`.

- Batch 12ML: HPA-BAZI-FLOW-002 is audited as pure natal Ten-God reuse, with the physical NTL-9900014379 table as a bounded received witness. 4200 annotations retain the natal anchor; full replay rejects a rehashed wrong anchor. Eight stale global-count test assertions are repaired. Matrix is 198 / 168 / 10; no chart algorithm changes. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-TEMPORAL-TEN-GOD-PROJECTION-AUDIT-ML.md`.

- Batch 12MM: HPA-BAZI-014 is audited only for received five stem-pair identity and neutral instance presentation. Direct physical p23 collates the five pairs; received Wuxing Dayi / Xingli Kaoyuan corroborate identity without copy-date or ancestry claims. 100 ordered pairs, 10000 four-stem grids and 6000 occurrences match; nominal targets and transformation outcomes remain outside presentation. Matrix is 198 / 169 / 10, no algorithm changes. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-STEM-FIVE-COMBINATION-IDENTITY-AUDIT-MM.md`.


- Batch 12MN: HPA-BAZI-FLOW-004 is decomposed into HPA-BAZI-FLOW-008/009/010 for target-layer NaYin, XunKong and Twelve-Growth identity projection. The composer reuses audited HPA-BAZI-006/007/008 on legal Ganzhi; Twelve Growth keeps the natal-day-master and target-self anchors separate, Xiaoyun candidates remain unranked, and no classical seven-layer software doctrine or interpretive meaning is inferred. The row's stale profile descriptor is synchronized from 1.0.1 to live 1.0.2 as downstream bookkeeping of existing PROV-DEFECT-009, with no new defect count or runtime change. Matrix is 201 / 173 / 10. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-TEMPORAL-CLASSICAL-IDENTITY-PROJECTION-AUDIT-MN.md`.


- Batch 12MO: HPA-BAZI-FLOW-005 closes as `MODERN_COMPATIBILITY_ONLY`. The temporal ShenSha wrapper preserves the exact 1.7.1 source-candidate identity and applies only mechanical target matching; it does not establish classical Dayun/Xiaoyun/year/month/day/hour applicability. Exhaustive 60-Ganzhi replay preserves ONLY_DAY, structural exclusion, source-candidate and no-winner boundaries. The 21 upstream ShenSha profile descriptors are synchronized to live 1.7.1; Tiande's already-counted candidate extension and Yuancheng PROV-DEFECT-003 are not double-counted. Matrix remains 201 rows, now 174 audited. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-TEMPORAL-SHENSHA-SOURCE-SCOPE-PROJECTION-AUDIT-MO.md`.


- Batch 12MP: HPA-BAZI-FLOW-006 closes as `MODERN_COMPATIBILITY_ONLY`. Structural Context and its target-flow projection reuse audited hidden-stem/Ten-God/exposure/affinity/raw-core relation primitives on DAYUN/ANNUAL/MONTHLY only. HPA-BAZI-005 remains disputed: the unselected historical relation sidecar is not injected into the production Structural Context. No effect, root strength, transformation success, priority, pattern, useful-god or prediction semantics are inferred. Matrix remains 201 rows, now 175 audited. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-STRUCTURAL-CONTEXT-SOURCE-PRESERVING-PROJECTION-AUDIT-MP.md`.


- Batch 12MQ: HPA-BAZI-FLOW-007 closes as `MODERN_COMPATIBILITY_ONLY`. Exact-hidden-stem and same-element/different-stem support are preserved as two non-ranking evidence classes over audited hidden-stem/affinity/exposure primitives; they are not treated as rival historical schools or collapsed to a root verdict. Natal month-command and active Flow solar-month candidate scopes remain separate; PRE_DAYUN cannot fabricate Dayun evidence; no strength/weight/score/rank/winner semantics are authorized. Matrix remains 201 rows, now 176 audited. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-STRUCTURAL-SUPPORT-EVIDENCE-CLASS-PROJECTION-AUDIT-MQ.md`.


- Batch 12MR: HPA-BAZI-FLOW-001 and HPA-COMB-004 close together as modern composition layers. The Bazi seven-layer timeline reuses released layer facts, preserves PRE_DAYUN absence and unresolved Xiaoyun methods, and does not create a second Ganzhi calculation path. Combined Target Flow binds independent Ziwei/Bazi bundle identities and target-coordinate lineage without unifying calendars, day boundaries or uncertainty. Matrix remains 201 rows, now 178 audited. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-COMBINED-UNIFIED-TARGET-TIMELINE-COMPOSITION-AUDIT-MR.md`.


- Batch 12MS: HPA-BAZI-001 is decomposed into five independently governed natal-coordinate rules instead of being treated as one monolithic classical algorithm. HPA-BAZI-017 Five Tigers and HPA-BAZI-020 Five Rats are historically supported by received Song/Ming/Qing witnesses; HPA-BAZI-016 year integer→Ganzhi, HPA-BAZI-018 Gregorian/JDN→day Ganzhi and HPA-BAZI-019 selected modern clock→double-hour branch are explicitly modern coordinate bridges. Existing Lichun/Jie, day-boundary, late-Zi and local-apparent-solar governance remains upstream and no winner is selected. Matrix is 206 / 184 / 10; provenance defects remain 17/17; chart algorithm defects/reopens/candidate collapses remain 0. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-NATAL-FOUR-PILLAR-COMPOSITION-AUDIT-MS.md`.


- Batch 12MT: HPA-STRUCT-003 R3 borrow projection is decomposed into three modern Zhongzhou-school mechanics (HPA-STRUCT-009 empty-palace eligibility, HPA-STRUCT-010 opposite all-star borrow, HPA-STRUCT-011 pre-borrow of empty structural members) and one modern engineering closure rule (HPA-STRUCT-012 immutable projection / non-recursion / fail-closed / zero-second contribution / physical-key dedup). The aggregate R3 layer is `MODERN_COMPATIBILITY_ONLY`; the three source mechanics are `SUPPORTED_BUT_SCHOOL_SPECIFIC`. Matrix is 210 / 189 / 10; provenance defects remain 18/18 after PROV-DEFECT-018; chart algorithm defects/reopens/candidate collapses remain 0. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-R3-BORROW-PROJECTION-SCHOOL-MECHANICS-AND-MODERN-CLOSURE-AUDIT-MT.md`.

- Batch 12MU: HPA-STRUCT-005 R5 closes only as a modern R3/R4 reference join. Two identity domains, no duplicated payload/second borrow/new evidence cause; R4 historical dating and source attribution remain unaudited. Matrix is 210 / 190 / 10, provenance defects 18/18, algorithm defects/reopens/collapses 0. Main-CI stale school-specific count assertion repaired by row reconciliation. See `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-R5-BORROW-RESOLVED-SANFANG-COMPOSITION-AUDIT-MU.md`.


## Progress — Batch 12MV

HPA-ZIWEI-011 leaves IMPLEMENTATION_REVIEW_REQUIRED as a decomposed SOURCE_INSUFFICIENT parent. Existing Changsheng/Boshi rows 019/024 are reused; new TaiSui 025 preserves four label bridges and Jiangqian 026 preserves primary-edition/temporal scope gaps. Natal ring members remain separate from physical stars and annual target layers. Generator replay covers 120 legal year/sex cases, 360 rings, 4320 members. Matrix 212 / 192 / 10; provenance 18/18 and algorithm defects/reopens/collapses 0. No transmission edge.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-THREE-RING-SOURCE-SCOPE-AND-IDENTITY-AUDIT-MV.md`. Research record: `docs/research/ZIWEI-THREE-RING-SOURCE-SCOPE-AUDIT-R1.json`.


## Progress — Batch 12MW

R4 HPA-STRUCT-004 is a modern composition, decomposed into HPA-STRUCT-013 school-scoped four-palace coordinates and HPA-STRUCT-014 engineering identity closure. Explicit Zi example and 144 rotated named frames agree. Local 三方/四正 inclusion and 三会局 wording are normalized only in their enumerated contexts; earliest definition, exact impression and direct lineage remain open. Old inventory row is preserved; source/runtime bytes unchanged. Matrix214/195/10, provenance18/18, algorithm defects/reopens/collapses0.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-R4-SOURCE-PHILOLOGY-SCOPE-AUDIT-MW.md`. Research record: `docs/research/ZIWEI-R4-SOURCE-PHILOLOGY-SCOPE-AUDIT-R1.json`.


## Progress — Batch 12MX

R6 HPA-STRUCT-006 is decomposed into HPA-STRUCT-015 school-scoped qishu coordinate identity and HPA-STRUCT-016 modern engineering semantic closure. Modern Heluo received text directly supports inclusive reverse ninth / each palace's relative Career palace; it does not establish a premodern origin or S04's twelve neutral fixed-support meanings. Independent 12 physical LIFE rotations × 12 named origins reproduce all 144 coordinates with ordinal 9 = clockwise offset 4. Matrix216/198/10, provenance18/18, algorithm defects/reopens/collapses0. No transmission edge.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-R6-QISHU-SOURCE-PHILOLOGY-SCOPE-AUDIT-MX.md`. Research record: `docs/research/ZIWEI-R6-QISHU-SOURCE-PHILOLOGY-SCOPE-AUDIT-R1.json`.


## Progress — Batch 12MY

R7 HPA-STRUCT-007 is decomposed into HPA-STRUCT-017 school-scoped Ziwei relative-six coordinates and HPA-STRUCT-018 modern engineering identity closure. Premodern received Hetu/geomancy texts attest the phrase 一六共宗, but do not encode Ziwei palace addresses; modern received 紫微斗数精成 explicitly gives origin-as-one, relative-six as 疾厄 and all twelve rotating palace pairs. Independent 12 physical LIFE rotations × 12 named origins reproduce all 144 coordinates with ordinal 6 = clockwise offset 7. Stronger 同视/荣损/冲六 interpretive doctrines are not imported into R7. Matrix218/201/10, provenance18/18, algorithm defects/reopens/collapses0. No transmission edge.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-R7-ONE-SIX-SOURCE-PHILOLOGY-SCOPE-AUDIT-MY.md`. Research record: `docs/research/ZIWEI-R7-ONE-SIX-SOURCE-PHILOLOGY-SCOPE-AUDIT-R1.json`.


## Progress — Batch 12MZ

R8 HPA-STRUCT-008 is corrected and decomposed into HPA-STRUCT-019 school-scoped generic adjacent-palace geometry and HPA-STRUCT-020 modern engineering/result-permission closure. Premodern received Fullbook text attests specific 夹贵/夹败/三夹六夹 patterns, but does not by itself establish the universal rotating term definition 邻宫. Modern Zhongzhou witnesses explicitly define the two adjacent palaces and separately define 相夹 through star occupation. Independent 12 physical LIFE rotations × 12 named origins reproduce 144 bilateral facts / 288 neighbor endpoints with ordinals 2 and 12 = physical offsets 11 and 1. R8 imports no flank judgment. PROV-DEFECT-019 forward-repairs the 12MY next-gate mislabel of HPA-STRUCT-008; historical snapshot retained. Matrix220/204/10, provenance19/19, algorithm defects/reopens/collapses0. No transmission edge.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-R8-ADJACENT-PALACE-SOURCE-PHILOLOGY-SCOPE-AUDIT-MZ.md`. Research record: `docs/research/ZIWEI-R8-ADJACENT-PALACE-SOURCE-PHILOLOGY-SCOPE-AUDIT-R1.json`.


## Progress — Batch 12NA

HPA-STRUCT-001 R1 neutral Z12 topology is formally audited as MODERN_COMPATIBILITY_ONLY. It is a modern interpretation-free coordinate substrate: 12 canonical branch addresses × 12 targets = 144 ordered facts, with clockwise_offset=(target-source) mod 12. The semantic rule-set binding remains disabled/fail-closed, so pure geometry is not silently renamed as 三方四正、对宫、夹宫、气数位、一六共宗 or any predictive doctrine. Runtime/schema/hash/V1 natal bytes remain unchanged. Matrix220/205/10, provenance19/19, algorithm defects/reopens/collapses0. No transmission edge.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-R1-NEUTRAL-Z12-TOPOLOGY-AUDIT-NA.md`. Research record: `docs/research/ZIWEI-R1-NEUTRAL-Z12-TOPOLOGY-AUDIT-R1.json`.


## Progress — Batch 12NB

HPA-STRUCT-002 R2 relative-palace frame is formally audited as MODERN_COMPATIBILITY_ONLY. It rotates the historically audited V1 twelve-palace designation order around each local origin and requires every physical edge to exist in the audited R1 neutral Z12 topology; it does not claim that the resulting 144-row frame matrix, hash/schema or integrity machinery is classical doctrine. Independent replay covers 12 LIFE physical rotations × 12 origins × 12 relative ordinals = 1728 rows, all matching target designation/address, relative role/ordinal and clockwise offset. Named 三方四正、对宫、气数位、一六共宗、邻宫/夹宫、借星 and predictive semantics remain fail-closed at R2. PROV-DEFECT-020 corrects the stale current-overview provenance count left at 18 after authoritative 12MZ state had reached 19/19; historical snapshots are untouched. Matrix220/206/10, provenance20/20, algorithm defects/reopens/collapses0. Structural R1-R8 current rows are fully audited.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-R2-RELATIVE-PALACE-FRAME-AUDIT-NB.md`. Research record: `docs/research/ZIWEI-R2-RELATIVE-PALACE-FRAME-AUDIT-R1.json`.


## Progress — Batch 12NC

HPA-TIME-001 Civil timezone/TZDB instant resolution is formally audited as **MODERN_COMPATIBILITY_ONLY**. IANA tzdb and Python zoneinfo are modern civil-time infrastructure, not classical Ziwei/Bazi doctrine. The location-zone design boundary is the UTC POSIX epoch; pre-1970 records remain explicitly incomplete/non-authoritative. China also preserves distinct Beijing-time (`Asia/Shanghai`) and Xinjiang-time (`Asia/Urumqi`) civil-time identities instead of a longitude-derived automatic winner.

**PROV-DEFECT-021** replaces the old local-calendar-year confidence test with a UTC-epoch test. **PROV-DEFECT-022** makes `tzdb_version` follow Python `ZoneInfo` source precedence: a system TZPATH zone is reported as `SYSTEM-TZDB-UNVERSIONED`; PyPI `tzdata` version metadata is used only for package fallback.

UTC candidate generation, offsets, DST, folds, gaps, ambiguity handling and candidate multiplicity are unchanged. This is provenance/confidence repair only; chart algorithm defects/reopens remain 0. Matrix220/207/10, provenance22/22, candidate collapses0. No traditional transmission edge is created.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-TIME-CIVIL-TZDB-INSTANT-RESOLUTION-NC.md`. Research record: `docs/research/TIME-CIVIL-TZDB-INSTANT-RESOLUTION-AUDIT-R1.json`.


## Progress — Batch 12ND

HPA-TIME-002 Ambiguous civil time fold/gap handling is formally audited as **MODERN_COMPATIBILITY_ONLY**. PEP 495 defines `fold=0` as the chronologically earlier reading and `fold=1` as the later reading of an ambiguous local wall time; Python `zoneinfo` implements those semantics for IANA transitions. The rule is modern operational time disambiguation, not classical Ziwei/Bazi doctrine.

The released resolver is generic rather than “one-hour DST” specific: New York's one-hour fold, Lord Howe's 30-minute fold/gap and Kyiv's 1990 backward offset change all preserve the expected two-real-reading / no-real-reading distinction. Gaps are rejected by UTC round-trip validation; no fold choice fabricates a missing instant.

**PROV-DEFECT-023** repairs the policy-registry wording for `REJECT`. The old text said both candidates are returned and an explicit choice is required, while the released foundation intentionally proceeds by preserving both candidates as branches. The repaired contract is “reject implicit single-winner selection”; explicit `EARLIER_OFFSET` / `LATER_OFFSET` policies may select one branch, but the source `CivilTimeStatus.AMBIGUOUS` and ambiguity provenance remain intact. The legacy policy IDs are retained and are defined by chronological UTC-reading order, not numeric UTC-offset order.

No UTC resolution algorithm, candidate count rule, chart fact, hash, candidate winner or classical rule changes. Matrix220/208/10, provenance23/23, algorithm defects/reopens/collapses0. No transmission edge.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-TIME-AMBIGUOUS-CIVIL-FOLD-GAP-HANDLING-ND.md`. Research record: `docs/research/TIME-AMBIGUOUS-CIVIL-FOLD-GAP-HANDLING-AUDIT-R1.json`.


## Progress — Batch 12NE

HPA-TIME-004 Chinese lunar calendar construction is formally audited as **MODERN_COMPATIBILITY_ONLY**. The released engine matches the modern rule structure (Beijing Standard Time, new-moon day as day 1, winter-solstice month 11, first no-principal-term month as leap when 13 months occur) but is not certified here to GB/T 33661-2017's prescribed numerical-model / 1-second event-time requirement. Astronomy Engine remains explicit modern infrastructure with emitted version provenance.

**PROV-DEFECT-024** relabels 1901–2100 from “validated range” to operational support matching HKO's published conversion-table horizon; selected HKO regression points are not exhaustive 200-year validation. **PROV-DEFECT-025** separates GB/T rule compatibility from strict numerical certification. HKO's official warning that near-midnight future moon phases/solar terms can shift dates by one day is retained, including new moons on 2057-09-28, 2089-09-04 and 2097-08-07.

Runtime calendar mechanics are unchanged. Audit trace now records standard reference, conformance scope, support range and range basis. Historical Ming/Qing calendar arithmetic remains behind the fail-closed historical-calendar adapter contract. Matrix220/209/10, provenance25/25, algorithm defects/reopens/collapses0. No transmission edge.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-TIME-MODERN-CHINESE-CALENDAR-CONSTRUCTION-AUDIT-NE.md`. Research record: `docs/research/TIME-MODERN-CHINESE-CALENDAR-CONSTRUCTION-AUDIT-R1.json`.


## Progress — Batch 12NF

HPA-TIME-011 Approximate birth-time candidate sampling is formally audited as **MODERN_COMPATIBILITY_ONLY**. The released foundation uses deterministic wall-time point sampling, not continuous interval arithmetic. Start/center/end are always retained; spans up to 24 hours use a minute grid; wider spans use at least an hourly stride and increase the step as needed to cap the set at 2001 points.

**PROV-DEFECT-026** repairs missing sampling provenance by emitting strategy ID, sample cap, nominal step, observed maximum sample gap and classification scope. **PROV-DEFECT-027** repairs the semantic overreach risk in `RESOLVED_RANGE_SINGLE_CLASSIFICATION`: the stable status ID is retained, but it now explicitly means all **sampled points** produced one observed classification, not that every instant of a continuous interval was exhaustively proven equivalent.

The actual sample set and all classification mechanics are unchanged. Non-zero uncertainty therefore reports `continuous_interval_exhaustive=false` and `classification_scope=SAMPLED_POINTS_ONLY`; a zero-width input reports exact-point scope. Matrix220/210/10, provenance27/27, chart algorithm defects/reopens/candidate collapses0. No traditional transmission edge.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-TIME-APPROXIMATE-BIRTH-TIME-SAMPLING-AUDIT-NF.md`. Research record: `docs/research/TIME-APPROXIMATE-BIRTH-TIME-SAMPLING-AUDIT-R1.json`.


## Progress — Batch 12NG

HPA-DAYUN-006 Wenzhen China Dayun compatibility realization is formally audited as **MODERN_COMPATIBILITY_ONLY**. The A7–A11 fixture is an explicitly project-captured third-party software witness: `authority_class=THIRD_PARTY_COMPATIBILITY_WITNESS`, `canonical_calendar_truth=false`, and the captured UI certifies symbolic age only to year/month/day/hour, not transition minute/second.

The compatibility profile is therefore an isolated comparison layer, not a historical Dayun authority. Its Wenzhen-specific delta consists of the mixed coordinate `BIRTH_LOCAL_APPARENT_SOLAR_CLOCK_TO_JIE_CHINA_STANDARD_CLOCK`, combined Gregorian calendar-month displacement before day/hour residuals, and China-standard-time ten-year anniversaries. Direction, Jie anchoring, the three-days-one-year symbolic ratio, and Dayun Ganzhi sequence have their own independent historical audit rows and are not re-attributed to Wenzhen by this profile.

**PROV-DEFECT-028** repairs the Matrix row's stale/nonexistent profile identifier `BAZI-TEMPORAL-V1-WENZHEN-CHINA-COMPATIBILITY-R1` to the actual runtime/fixture identity `BAZI-TEMPORAL-WENZHEN-CHINA-COMPATIBILITY-R1`. No runtime code, fixture observation, candidate, transition instant, Dayun pillar, default profile, or historical winner changes.

Matrix220/211/10, provenance28/28, chart algorithm defects/reopens/candidate collapses0. `transmission_impact=NONE`: a modern product-compatibility witness creates no historical text/school/person transmission edge.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-DAYUN-WENZHEN-COMPATIBILITY-SCOPE-AUDIT-NG.md`. Research record: `docs/research/BAZI-DAYUN-WENZHEN-COMPATIBILITY-SCOPE-AUDIT-R1.json`.


## Progress — Batch 12NH

HPA-DAYUN-007 Exact-Jie tie handling is formally audited as **MODERN_COMPATIBILITY_ONLY**. Both released Bazi temporal profiles use `exact_jie_tie_policy=FAIL_CLOSED`; when `birth_utc == previous_jie_utc`, the runtime emits `EXACT_JIE_TIE_UNRESOLVED` rather than silently assigning the equality instant to a preceding or following Jie.

The bound Song/Ming Dayun witnesses use strict relative wording: forward counting from the birth to the future Jie and reverse counting to the past Jie. That closes the directional before/after structure but does not state an equality operator or zero-interval rule. The audit therefore does not infer `>=`, `<=`, immediate handover, or an adjacent-Jie reassignment from textual silence.

**PROV-DEFECT-029** repairs the Matrix label `MODERN_STANDARD` and vague `BAZI temporal profiles` scope. The row now identifies this as a project fail-closed boundary policy over a historically unresolved equality case and binds the exact continuous + Wenzhen compatibility profiles. No runtime mechanics, candidates, Dayun coordinates, or historical winner change.

Matrix220/212/10, provenance29/29, chart algorithm defects/reopens/candidate collapses0. `transmission_impact=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-DAYUN-EXACT-JIE-TIE-HANDLING-AUDIT-NH.md`. Research record: `docs/research/BAZI-DAYUN-EXACT-JIE-TIE-HANDLING-AUDIT-R1.json`.


## Progress — Batch 12NI

HPA-ZT-016 Self/inward transformation direction has now been fully source-scope audited while intentionally remaining **NOT_YET_FORMALIZED**. The released 12×4 palace-stem transformation topology remains neutral geometry only: `SAME_PALACE`, `OPPOSITE_PALACE`, and `OTHER_PALACE` are not promoted to outward/inward direction.

S08 preserves normalized self/inward enums and a recovered source-family identity `S08-SRC-ZHONGZHOU-TRANSFORMATION / 中州派四化曜.txt`, but its own release proof remains `NOT_PROVEN`; the recovered RAW surface does not close an exact `向心力 / 離心力 / 視同自化 / 本宫宫干 / 对宫宫干` selector. Under the research-authority policy, S08 therefore remains project corpus, not a self-authenticating historical/school authority.

Modern evidence now narrows the method family without closing it. Xu Quanren's 2013 `紫微斗數命理學正解(一)` bibliography/TOC directly establishes dedicated 飛宮四化 and 自化 sections; a Xu-supervised public teaching site establishes the modern 欽天四化 teaching identity; and a secondary transcript of advanced-class episode 27 explicitly maps 自化 toward a centrifugal vocabulary and 視同自化 toward a centripetal vocabulary. However the target book pages, original audio and diagram coordinates are not directly bound. Current secondary literature also uses a three-label taxonomy that separates 向心自化 / 離心自化 / 視同自化, so terminology cannot be normalized by name alone.

No runtime selector or candidate is added. The formalization gate remains closed until an edition-bound or equivalent first-party school witness supplies a complete replayable selector, scope, diagram/coordinate semantics and terminology bridge. Matrix220/213/10; provenance29/29; chart algorithm defects/reopens/candidate collapses0. `transmission_impact=DEFERRED_NO_EDGE` because no direct lineage from the S08 Zhongzhou-labelled source family to the Xu/Qintian family is established.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SELF-INWARD-TRANSFORMATION-DIRECTION-SOURCE-SCOPE-AUDIT-NI.md`. Research record: `docs/research/ZIWEI-SELF-INWARD-TRANSFORMATION-DIRECTION-SOURCE-SCOPE-AUDIT-R1.json`.


## Progress — Batch 12NJ

HPA-COMB-001 Shared time credential is formally audited as **MODERN_COMPATIBILITY_ONLY**. The combined runtime intentionally unifies physical time facts while preserving separate Ziwei and Bazi policy chains; the released late-Zi and DST/uncertainty regressions confirm that sharing the time credential does not collapse day-boundary or calendar conventions.

**PROV-DEFECT-030** repairs an overbroad documentation claim: the shared credential `computation_hash` directly binds its schema, fact hash, policy registry, selected policy snapshots and realizations, but it does not directly contain every subsystem algorithm/profile version. Full combined provenance is layered through the combined manifest (combined algorithm/profile identities, all subsystem profile identities, shared credential and candidate lineage) plus Ziwei/Bazi bundle hashes.

No schema, hash algorithm, chart fact, candidate, policy default or subsystem computation changes. Matrix220/214/10, provenance30/30, chart algorithm defects/reopens/candidate collapses0. No historical transmission edge.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-COMBINED-SHARED-TIME-CREDENTIAL-SCOPE-AUDIT-NJ.md`. Research record: `docs/research/COMBINED-SHARED-TIME-CREDENTIAL-SCOPE-AUDIT-R1.json`.


## Progress — Batch 12NK

HPA-COMB-002 independent Ziwei/Bazi date/calendar policy preservation is audited as **MODERN_COMPATIBILITY_ONLY**. The combined runtime shares physical-time facts while preserving separate system policy namespaces.

`validate_shared_policy_contract()` requires only the same time/calendar policy registry version and the same civil ambiguous-time policy. Ziwei calendar-date, leap-month and day-boundary policies are not equated with Bazi year/day-boundary or late-Zi hour-stem policies. The combined service resolves Ziwei and Bazi time results separately, then binds both outputs into the shared credential.

The focused late-Zi regression proves the invariant on one physical local-apparent-solar instant: Ziwei uses `ZI_START_23`, Bazi uses `MIDNIGHT`, and Bazi late-Zi uses `CLASSICAL_CONTINUOUS`; the combined Ziwei/Bazi bundle hashes still match their standalone-service bundle hashes.

No new provenance defect, chart algorithm defect, algorithm reopen or candidate collapse. Matrix220/215/10; provenance30/30. `transmission_impact=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-COMBINED-INDEPENDENT-DATE-CALENDAR-POLICY-PRESERVATION-AUDIT-NK.md`. Research record: `docs/research/COMBINED-INDEPENDENT-DATE-CALENDAR-POLICY-PRESERVATION-AUDIT-R1.json`.


## Progress — Batch 12NL

HPA-COMB-003 candidate lineage preservation is audited as **MODERN_COMPATIBILITY_ONLY**. The runtime keeps one lineage row per shared `source_time_branch_index`, binding the shared realization hash, Ziwei natal fact hash and Bazi candidate IDs without score/rank/winner semantics.

DST-fold and mixed-uncertainty regressions preserve all shared branches and distinct Ziwei fact hashes; full replay rejects a forged but syntactically valid fact hash even after lineage/manifest hashes are recomputed.

**PROV-DEFECT-031** repairs a crossed source link: the Matrix row previously pointed to `COMBINED-RESOLVED-PROFILE-LINEAGE-R1.md`, whose primary subject is profile/rule/algorithm lineage. HPA-COMB-003 is now bound to the actual candidate-lineage implementation, shared-time contract, and focused replay tests. No candidate, hash algorithm or runtime behavior changes.

Matrix220/216/10, provenance31/31, chart algorithm defects/reopens/candidate collapses0. `transmission_impact=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-COMBINED-CANDIDATE-LINEAGE-PRESERVATION-AUDIT-NL.md`. Research record: `docs/research/COMBINED-CANDIDATE-LINEAGE-PRESERVATION-AUDIT-R1.json`.


## Progress — Batch 12NM

HPA-COMB-005 Shared target → Ziwei projection is audited as **MODERN_COMPATIBILITY_ONLY**. The projection reuses one shared physical target-candidate identity, then applies Ziwei's own calendar/date-boundary semantics and preserves released Ziwei layer/candidate identities without doctrinal arbitration.

The original Matrix source binding stopped at the R1.10 productization document. Current runtime also carries the separately productized `JIELAN-1581-DAY-ANCHORED-FLOW-HOUR-R1` and `ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1` candidate families. **PROV-DEFECT-032** repairs that stale provenance scope by binding HPA-COMB-005 to the live projection service, historical-candidate productization/runtime and focused regressions. Historical authority remains upstream in the corresponding Ziwei source-scoped rows/registries; the Combined projection itself gains no classical authority.

No runtime, schema, hash algorithm, chart fact, candidate selection or Ziwei placement rule changed. Matrix220/217/10; provenance32/32; chart algorithm defects/reopens/candidate collapses0. `transmission_impact=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-COMBINED-SHARED-TARGET-ZIWEI-PROJECTION-AUDIT-NM.md`. Research record: `docs/research/COMBINED-SHARED-TARGET-ZIWEI-PROJECTION-AUDIT-R1.json`.


## Progress — Batch 12NN

HPA-COMB-006 Combined Target Flow Fusion R2 is audited as **MODERN_COMPATIBILITY_ONLY**. R2 binds the immutable R1 target-flow bundle, the same replayed target-coordinate identity, the released BaZi target-flow bundle and the released shared Ziwei selector projection. It does not create a placement rule, calendar doctrine, school winner or interpretation layer.

`RESOLVED` versus `UNCERTAINTY_PRESENT` is strictly a software composition status. A unique target + unique BaZi flow + one Ziwei physical target candidate resolves; DST folds, boundary/approximate uncertainty or upstream multiplicity stay explicit. R2 binds selector content through its fact/computation hashes and validates full replay; it does not duplicate or reinterpret upstream candidate families.

**PROV-DEFECT-033** repairs the Matrix placeholder `PENDING_VERBATIM_EXTRACTION` and document-only provenance by binding HPA-COMB-006 to the live composer, local endpoint, read-only Workbench and focused integrity/full-replay regressions.

No runtime, schema, hash algorithm, status rule, candidate or subsystem computation changed. Matrix220/218/10; provenance33/33; chart algorithm defects/reopens/candidate collapses0. `transmission_impact=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-COMBINED-TARGET-FLOW-FUSION-R2-AUDIT-NN.md`. Research record: `docs/research/COMBINED-TARGET-FLOW-FUSION-R2-AUDIT-R1.json`.


## Progress — Batch 12NO

HPA-COMB-007 Resolved profile / RuleSet / algorithm lineage is audited as **MODERN_COMPATIBILITY_ONLY**.

The combined runtime lineage is a software reproducibility namespace: the combined profile plus six resolved subsystem profiles are carried by the validated resolution; `ManifestHash` directly binds profile identities, while profile validators and subsystem replay/profile equality checks bind the supported RuleSet/Algorithm snapshot. The Workbench renders only the backend-provided snapshot after integrity PASS and does not maintain a browser-side rule registry or choose a doctrinal winner.

Historical source / edition / school / person / transmission identity remains in the Historical Provenance Matrix, external-source registry and Transmission Genealogy Graph. Those evidence namespaces should cross-reference runtime rule identities where warranted, but must not be merged into runtime Profile/RuleSet/Algorithm IDs.

**PROV-DEFECT-034** repairs the prior `PENDING_VERBATIM_EXTRACTION` and the proposed action that would have conflated runtime computation lineage with historical source/edition/school lineage. Compatibility profiles remain compatibility witnesses unless independently supported by historical evidence.

No runtime, profile, schema, hash, rule, candidate or algorithm changed. Matrix220/219/10; provenance34/34; chart algorithm defects/reopens/candidate collapses0. `transmission_impact=NONE`.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-COMBINED-RESOLVED-PROFILE-RULE-ALGORITHM-LINEAGE-AUDIT-NO.md`. Research record: `docs/research/COMBINED-RESOLVED-PROFILE-RULE-ALGORITHM-LINEAGE-AUDIT-R1.json`.


## Progress — Batch 12NP

HPA-COMB-008 Fact / computation / view / manifest hashes is audited as **MODERN_COMPATIBILITY_ONLY**. The current integrity architecture deliberately separates shared-time realization/fact/computation hashes, candidate-lineage hash, combined ManifestHash and target-flow source-fact/view/bundle hashes. These identify different deterministic payload domains rather than one undifferentiated notion of truth.

Structural integrity verifies local payload/hash consistency. Full replay independently re-resolves the released objects and rejects self-consistently rehashed tampering. A valid runtime hash therefore identifies an exact deterministic state; it does not by itself establish upstream authenticity or historical authority.

Historical PDF/page/image/artifact/response checksums and edition/catalog identifiers already live in the external-source/evidence namespace. They identify the reviewed digital object or bytes, but do not prove authorship, physical-copy date, transmission, school authority or doctrinal correctness.

**PROV-DEFECT-035** repairs the prior `PENDING_VERBATIM_EXTRACTION`, non-specific `README + engine integrity docs` source binding and ambiguous action by separating runtime deterministic hash namespaces from historical evidence-object checksums. The two layers connect by explicit audit cross-reference, not namespace merger.

No runtime, schema, hash algorithm, hash payload, rule, candidate or chart algorithm changed. Matrix220/220/10; provenance35/35; chart algorithm defects/reopens/candidate collapses0. `transmission_impact=NONE`.

The existing Historical Provenance Matrix is now **220/220 audited**. Next is **12NQ**, a post-audit reconciliation of the 10 current `MISSING_FROM_PRODUCT` rows against live runtime/product surfaces, beginning with HPA-ZT-015 because later Zhongzhou leap-month candidate productization may make its old status stale.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-COMBINED-FACT-COMPUTATION-VIEW-MANIFEST-HASH-AUDIT-NP.md`. Research record: `docs/research/COMBINED-FACT-COMPUTATION-VIEW-MANIFEST-HASH-AUDIT-R1.json`.


## Progress — Batch 12NQ

Post-audit reconciliation of HPA-ZT-015 confirms that the row should remain **MISSING_FROM_PRODUCT**, but its old gap description was stale.

The source-scoped `ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1` month-assignment candidate is already productized through the temporal historical-candidate runtime, Shared Ziwei Selector Projection and read-only Workbench as `PRESERVED_NOT_SELECTED`. Days 1–15 map to the previous regular month; days 16–end map to the following regular month.

The broader HPA-ZT-015 gap remains real because ordinary leap-month monthly/daily projection still fails closed as `LEAP_MONTH_UNRESOLVED_NO_FRAME` / `PARENT_LEAP_MONTH_UNRESOLVED_NO_FRAME`, and the source does not close leap-month day-one flow-day origin or a complete daily active-address frame.

HPA-ZTEMP-006 now cleanly represents the productized school-scoped half-split candidate, while HPA-ZT-015 represents only the still-missing complete leap-month temporal frame.

**PROV-DEFECT-036** repairs the stale Matrix action that still said to implement a candidate already released. No runtime, schema, hash, candidate selection or chart algorithm changed.

Matrix220/220/10; provenance36/36; chart algorithm defects/reopens/candidate collapses0. `transmission_impact=NONE`.

Next: **12NR** — reconcile HPA-ZIWEI-015 / 016 / 022 against the Jielan 1581 source-scoped runtime and actual API/Workbench product surfaces.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-POST-AUDIT-MISSING-PRODUCT-RECONCILIATION-LEAP-MONTH-NQ.md`. Research record: `docs/research/ZIWEI-LEAP-MONTH-MISSING-PRODUCT-RECONCILIATION-R1.json`.


## Progress — Batch 12NR

Post-audit product-surface reconciliation confirms that **HPA-ZIWEI-015 Kui/Yue**, **HPA-ZIWEI-016 Fire/Bell**, and **HPA-ZIWEI-022 Mingzhu basis** remain `MISSING_FROM_PRODUCT`.

The Jielan 1581 source-scoped resolver already materializes these facts deterministically with source refs and `PRESERVED_NOT_SELECTED`. However, the general Jielan resolver/registry is not exported from the `fortune_training.ziwei_chart` package root, the local combined request exposes no Ziwei historical candidate-profile selector, `/api/profiles` exposes no Jielan candidate profiles, and Workbench has no corresponding candidate selector.

Therefore internal runtime availability is not treated as product closure. Product closure still requires an explicit candidate-profile API/Workbench lineage that preserves method/source identity without changing the production default.

No new provenance defect was found: these rows already correctly described the internal-runtime-versus-product-surface gap. Matrix220/220/10; provenance36/36; chart algorithm defects/reopens/candidate collapses0. `transmission_impact=NONE`.

Next: **12NS** — reconcile HPA-ZIWEI-014 competing Four-Transformation tables and HPA-ZIWEI-018 Jielan historical dignity table.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-POST-AUDIT-JIELAN-SOURCE-SCOPED-CANDIDATE-PRODUCT-SURFACE-RECONCILIATION-NR.md`. Research record: `docs/research/ZIWEI-JIELAN-SOURCE-SCOPED-CANDIDATE-PRODUCT-SURFACE-RECONCILIATION-R1.json`.

## Progress — Batch 12NS

Post-audit reconciliation confirms that **HPA-ZIWEI-014 competing Four-Transformation table families** and **HPA-ZIWEI-018 Jielan historical dignity table** both remain `MISSING_FROM_PRODUCT`, but their partial internal coverage is now stated precisely.

For Four Transformations, Jielan 1581 is already preserved in `ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATES-R1@1.1.0` and the source-scoped resolver; regression tests prove its complete ten-stem target table exactly equals current `S08_CURRENT_40_ASSIGNMENT_R1`. That does **not** close the row: the genuinely divergent received-Fullbook/Zhongzhou families still lack complete source-bound selectable candidate profiles and Workbench/API table-family selection. **PROV-DEFECT-037** repairs the stale wording that failed to distinguish this partial internal source-family coverage.

For dignity, the Jielan registry/resolver already preserves CH69/CH70 as `SOURCE_TABLE_PRESENT_NORMALIZATION_PENDING` with `runtime_normalized=false`. Production remains the distinct `OPERATIONAL-ZIWEI-DIGNITY-R4@4.0.0`; no source-faithful Jielan historical cell table has been normalized or exposed as a selectable profile. **PROV-DEFECT-038** updates the stale Matrix registry identity from Jielan `1.0.0` to live `1.1.0` without coercing ambiguous historical wording into the modern seven-grade scale.

Matrix220/220/10; provenance38/38; chart algorithm defects/reopens/candidate collapses0. No runtime/schema/hash/rule/candidate-selection/production-default change. `transmission_impact=NONE`.

Next: **12NT** — reconcile HPA-ZDATE-006 Nanyangtang Fullbook ten-ke Zi/Hai split natal birth-hour candidate against the live time-coordinate runtime/product surfaces and current source-scoped acquisition boundary.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-POST-AUDIT-FOUR-TRANSFORMATION-DIGNITY-PRODUCT-BOUNDARY-RECONCILIATION-NS.md`. Research record: `docs/research/ZIWEI-FOUR-TRANSFORMATION-DIGNITY-PRODUCT-BOUNDARY-RECONCILIATION-R1.json`.

## Progress — Batch 12NT

Post-audit reconciliation confirms **HPA-ZDATE-006 Nanyangtang Fullbook ten-ke Zi/Hai split natal birth-hour candidate** remains `MISSING_FROM_PRODUCT`.

The current natal runtime still maps local-apparent-solar **23:00..00:59 uniformly to Zi** in `NatalStructureGenerator._hour_branch_index`. `ResolvedZiweiCalculationProfile` has no natal hour-branch reclassification policy, and the time/calendar registry exposes only Ziwei calendar-date and life/body leap-month policy dimensions. Production still uses one frozen Ziwei calculation profile.

The existing historical temporal-candidate API does not close this gap: its Jielan candidate is target **flow-hour** geometry and its Zhongzhou candidate is **leap-month month assignment**. Neither is a natal upper-half-Zi→Hai branch candidate, the package root exports no Nanyangtang resolver, the combined local request exposes no Ziwei historical natal-candidate selector, and Workbench has no Nanyangtang late-Zi selector.

The historical evidence is stronger than the original Batch 12A snapshot but still does not authorize runtime selection. Nanyangtang and Guangyi directly attest the explicit Hai wording and generic upper/lower-half orientation is closed; however explicit Hai is not universal across the broader received Ziwei transmission, and the source-scoped runtime time-standard / inclement-current-time binding remains unresolved.

No new provenance defect was found. The current Matrix description is materially correct; existing `PROV-DEFECT-010` remains the already repaired Batch 12AH auction-media scope defect. Matrix220/220/10; provenance38/38; chart algorithm defects/reopens/candidate collapses0. No runtime/schema/hash/rule/candidate-selection/production-default change. `transmission_impact=NONE`.

Next: **12NU** — reconcile HPA-DAYUN-CAL-002 / 003 / 004 historical Jiaoyun calendarization and ten-year recurrence candidates against the live historical-calendar adapter contract and product surfaces.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-POST-AUDIT-NANYANGTANG-LATE-ZI-NATAL-CANDIDATE-PRODUCT-SURFACE-RECONCILIATION-NT.md`. Research record: `docs/research/ZIWEI-NANYANGTANG-LATE-ZI-NATAL-CANDIDATE-PRODUCT-SURFACE-RECONCILIATION-R1.json`.

## Progress — Batch 12NU

Post-audit reconciliation confirms **HPA-DAYUN-CAL-002 / 003 / 004** all remain `MISSING_FROM_PRODUCT`.

The repository does have a real historical-calendar boundary: `HISTORICAL-CHINESE-CALENDAR-ADAPTER-CONTRACT-R1` registers **Ming Datong** and **Qing Shixian** contexts, exposes `REALIZE_DAYUN_HANDOVER` and `ADD_CALENDAR_YEARS`, and fail-closes with `UNRESOLVED_NO_CERTIFIED_HISTORICAL_CALENDAR_ADAPTER`. But this contract is not wired into `BaziTemporalEngine`; the released engine/profile/product surface still supports only continuous and Wenzhen compatibility profiles, both with modern Gregorian operational realization.

For **HPA-DAYUN-CAL-002**, the Ming descriptor and fail-closed contract are genuine partial infrastructure, but no certified Ming arithmetic adapter, historical temporal profile or product selector exists.

For **HPA-DAYUN-CAL-003**, **PROV-DEFECT-039** was confirmed and repaired. The previous Matrix wording said the adapter contract “preserves the unresolved regime”; in fact the live registry has no Republican/Qianli descriptor. The contract vocabulary can accommodate such a future regime, but the Qianli method currently exists only as a Matrix/source candidate, not a registered historical-calendar runtime context.

For **HPA-DAYUN-CAL-004**, `ADD_CALENDAR_YEARS` and the no-Gregorian-substitution firewall exist at the contract layer, but actual Dayun recurrence in `BaziTemporalEngine` still has only `PROLEPTIC_GREGORIAN_10Y_UTC_ANNIVERSARY` and `PROLEPTIC_GREGORIAN_10Y_CHINA_STANDARD_ANNIVERSARY` branches.

All **10 current MISSING_FROM_PRODUCT rows now have explicit post-audit product-surface reconciliation**. Matrix220/220/10; provenance39/39; chart algorithm defects/reopens/candidate collapses0. No runtime/schema/hash/rule/candidate-selection/production-default change. `transmission_impact=NONE`.

Next: **12NV** — prioritize the remaining unresolved historical statuses: 30 `DISPUTED_MULTIPLE_CANDIDATES`, 11 `SOURCE_INSUFFICIENT`, and 1 `NOT_YET_FORMALIZED`; then continue the highest-value evidence closure without collapsing candidates.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-POST-AUDIT-DAYUN-HISTORICAL-CALENDAR-CANDIDATE-PRODUCT-SURFACE-RECONCILIATION-NU.md`. Research record: `docs/research/BAZI-DAYUN-HISTORICAL-CALENDAR-CANDIDATE-PRODUCT-SURFACE-RECONCILIATION-R1.json`.

## Progress — Batch 12NV

With all 10 current `MISSING_FROM_PRODUCT` rows now product-surface reconciled, the remaining Historical Audit work was re-ranked rather than treated as a flat unresolved queue.

Current unresolved historical-status inventory: **30 `DISPUTED_MULTIPLE_CANDIDATES` / 11 `SOURCE_INSUFFICIENT` / 1 `NOT_YET_FORMALIZED`**. The priority rule is now explicit: **active production output with insufficient historical provenance outranks behavior that is already fail-closed or absent from runtime**. Broad parent rows already decomposed into child rows are not selected for duplicate re-audit, and disputed candidate families are not collapsed merely to reduce status counts.

The highest-priority next target is **HPA-ZIWEI-023 — Zi/Wu Shenzhu Fire/Bell textual composite**. Strict QS correctly throws `QS_SHENZHU_ZI_WU_TEXTUAL_AMBIGUITY`, while production Wenmo resolves Zi/Wu to Fire. The 1581 Jielan historical registry explicitly preserves `TEXTUAL_COMPOSITE_FIRE_BELL_NOT_UNIQUELY_ARBITRATED` from CH32 and its source-scoped resolver selects no winner. This creates a higher active-output provenance risk than fail-closed HPA-ZT-016.

Next tiers are HPA-ZIWEI-026 Jiangqian temporal/source scope, HPA-ZMINOR-020 standalone Feilian identity collision, then the active month-table source gaps HPA-ZMINOR-023/024/025/026. HPA-ZT-016 remains important but runtime currently emits no inward/outward direction, so its immediate deterministic-output risk is lower.

No Matrix status, runtime, candidate selection, production default, provenance count or transmission graph changed. Matrix220/220/10; provenance39/39; algorithm defects/reopens/candidate collapses0.

Next: **12NW — HPA-ZIWEI-023 Zi/Wu Shenzhu Fire/Bell evidence closure**. A Fire or Bell winner remains forbidden unless edition/source/commentary evidence actually closes it.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-UNRESOLVED-HISTORICAL-STATUS-PRIORITIZATION-NV.md`. Research record: `docs/research/HISTORICAL-UNRESOLVED-STATUS-PRIORITIZATION-R1.json`.

## Progress — Batch 12NW

HPA-ZIWEI-023 **Zi/Wu Shenzhu Fire/Bell textual composite** remains `SOURCE_INSUFFICIENT`.

The 1581 Jielan source still reads `子午生人铃火宿` and then glosses Zi/Wu as `火铃为身主`; the received Fullbook corpus likewise preserves `火玲/火铃` composite wording. Nothing in those source surfaces uniquely selects Fire. Public modern commentary does not close the gap: one editorial surface calls `火玲星` the base reading and Fire the common reading, while another current rules surface maps Zi/Wu to Bell. These are modern interpretation/compatibility surfaces, not Ming textual arbitration.

The repository boundary is now explicit. Strict QS continues to raise `QS_SHENZHU_ZI_WU_TEXTUAL_AMBIGUITY`; the Jielan sidecar keeps `TEXTUAL_COMPOSITE_FIRE_BELL_NOT_UNIQUELY_ARBITRATED` and `winner_selected=false`; production still maps Zi/Wu to Fire. Existing Wenmo role fixtures do **not** independently test Zi/Wu Shenzhu: the role fixture observes a Si-year Tianji binding, while Zi-year fixtures only discriminate the separately placed Fire/Bell stars.

**PROV-DEFECT-040** repaired a documentation/provenance-scope overclaim: `WenmoDefaultRoleGenerator` previously described the full table as matching Wenmo's default convention without identifying the unverified Zi/Wu branch pair. The runtime docstring/comment now records Zi/Wu Fire as an operational compatibility default inherited from S01 normalization, not historical closure or independently observed Wenmo compatibility.

No role value, source_refs tuple, rule-set identity, fact/computation hash, candidate selection or chart algorithm changed. Matrix220/220/10; provenance40/40; chart algorithm defects/reopens/candidate collapses0. `transmission_impact=NONE`.

Next: **12NX — HPA-ZIWEI-026 Jiangqian temporal/source-scope evidence closure**.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZI-WU-SHENZHU-FIRE-BELL-EVIDENCE-CLOSURE-NW.md`. Research record: `docs/research/ZIWEI-ZI-WU-SHENZHU-FIRE-BELL-EVIDENCE-CLOSURE-R1.json`.

## Progress — Batch 12NX

`HPA-ZIWEI-026` **Jiangqian twelve-member trine-wang ring and temporal/source scope** remains `SOURCE_INSUFFICIENT`.

The runtime boundary is now explicit: `RING.JIANGQIAN12` is a natal fact. `ZiweiChartFoundation` passes `structure.ziwei_birth_year_branch` into `WenmoDefaultRingGenerator.jiangqian()`, which applies the four trine-wang anchors and the fixed twelve-member forward order. No annual-target ring is currently materialized.

Historical/received evidence requires a separate temporal-scope distinction. The 1581 Jielan line has an explicitly titled `定流年太岁所值凶星图` chapter whose 驿马 rule is computed from the year-branch trine; this closes an early Ziwei **flow-year related shensha context**, but the reviewed public chapter does not contain the complete Jiangqian twelve-member sequence. A modern Zhongzhou received manual does preserve the complete `将星三合起旺地...指背咸池月煞亡` sequence, and modern derived rule surfaces apply the same geometry both to birth-year and flow-year branches.

Therefore natal and annual use are **distinct temporal applications, not mutually exclusive winner candidates**. The existence of the annual layer does not authorize rewriting the natal ring, while the natal product does not erase annual practice. The unresolved gate is narrower: an edition-bound early complete twelve-member Jiangqian passage plus explicit scope instruction remains unclosed.

No new provenance defect was confirmed because Batch 12MV already required separately sourced annual-target implementation. Provenance remains 40/40. No runtime/profile/schema/hash/rule/candidate/chart-algorithm change; Matrix 220/220 audited / 10 current missing; chart algorithm defects/reopens/candidate collapses 0. `transmission_impact=NONE`.

Next: **12NY — HPA-ZMINOR-020 standalone Feilian identity collision**, preserving identity boundaries among Boshi 飞廉, year-branch 蜚廉 and same-coordinate facts.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JIANGQIAN-TEMPORAL-SOURCE-SCOPE-EVIDENCE-CLOSURE-NX.md`. Research record: `docs/research/ZIWEI-JIANGQIAN-TEMPORAL-SOURCE-SCOPE-CLOSURE-R1.json`.

## Progress — Batch 12NY

`HPA-ZMINOR-020` **standalone 蜚廉 birth-year-branch table vs 博士十二神 飞/蜚廉 identity** is upgraded from `SOURCE_INSUFFICIENT` to `HISTORICALLY_SUPPORTED` for the standalone placement geometry.

The current `STAR.FEILIAN` table matches the premodern received year-deity rule **12/12**. Cao Zhengui's `历事明原` Feilian passage explicitly cites `广圣历` for the table; the 1713 `御定星历考原` repeats the same twelve positions; the Qing `钦定协纪辨方书` again repeats them and explains the reverse traversal through trine 生/旺/墓 states. The Songshi bibliography separately records Miao Rui's `新删定广圣历` in two juan, but the exact cited recension remains unresolved and is not treated as directly reviewed rule text.

Identity remains fail-closed. `STAR.FEILIAN` is keyed by birth-year branch. `RING.BOSHI12.FEILIAN` is ordinal 6 from Lucun, hence the Lucun-opposite palace regardless of ring direction. Across all 60 legal Jiazi, only 甲子、乙丑、庚午、辛未 happen to share coordinates. Same/variant glyph or coordinate coincidence does not merge the two facts.

The transmission graph now records the premodern calendrical Feilian rule family, explicit Guangshengli citation layer, Qing transmission witnesses, and a disproved same-mechanical-rule edge against the Ziwei Boshi member. What remains open is the **Ziwei adoption path**, not the standalone geometry.

No runtime/profile/rule-set/hash/candidate change and no algorithm reopen. Matrix remains 220/220 audited / 10 current missing; provenance defects 40/40; chart algorithm defects/reopens/candidate collapses 0. Status distribution becomes HISTORICALLY_SUPPORTED 95 and SOURCE_INSUFFICIENT 10.

Next: **12NZ — HPA-ZMINOR-023 month Jieshen/Yuejie provenance**, preserving the month-table identity separately from year-based 解神/年解.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-STANDALONE-FEILIAN-HISTORICAL-IDENTITY-CLOSURE-NY.md`. Research record: `docs/research/ZIWEI-STANDALONE-FEILIAN-HISTORICAL-IDENTITY-CLOSURE-R1.json`.

## Progress — Batch 12NZ

`HPA-ZMINOR-023` **month-based 解神 / 月解** is upgraded from `SOURCE_INSUFFICIENT` to `HISTORICALLY_SUPPORTED` for its month geometry.

The current table `正二申、三四戌、五六子、七八寅、九十辰、十一十二午` matches premodern received calendrical tradition **12/12**. `历事明原` defines 解神 as a month deity and attributes the table to `历例`; the 1713 `御定星历考原` and Qing `钦定协纪辨方书` preserve a clean exact table, while `协纪辨方书` also supplies the opposing-yang-branch mechanical explanation. The Lishimingyuan public transcription has OCR noise, so it is not used alone for glyph adjudication.

Identity remains separated from `HPA-ZMINOR-006`: received Ziwei also has a year-based 解神 rule, represented in the product as `STAR.NIANJIE / 年解`. Month 解神 is keyed by lunar month; year 解神 is keyed by birth-year branch. The product label 年解 is a modern disambiguation label and is not back-projected as fixed ancient terminology.

The transmission graph now records the month Jieshen rule family, explicit `总要历` / `历例` citation layers, three premodern/Qing transmission passages, parallel coexistence with the year rule, and a DISPROVED same-mechanical-rule non-edge. Exact cited-source identities and the Ziwei adoption route remain open.

No runtime/profile/rule-set/hash/candidate change and no algorithm reopen. Matrix 220/220 audited / 10 current missing; provenance defects 40/40; chart algorithm defects/reopens/candidate collapses 0. Status distribution becomes HISTORICALLY_SUPPORTED 96 and SOURCE_INSUFFICIENT 9.

Next: **12OA — HPA-ZMINOR-024 Tianwu lunar-month table**. First mechanically test whether the premodern phrase `常居月建前二辰` reproduces the runtime four-palace table; same-name evidence alone is insufficient.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-MONTH-JIESHEN-HISTORICAL-IDENTITY-CLOSURE-NZ.md`. Research record: `docs/research/ZIWEI-MONTH-JIESHEN-HISTORICAL-IDENTITY-CLOSURE-R1.json`.


## Progress — Batch 12OA

`HPA-ZMINOR-024` **Tianwu lunar-month table** remains `SOURCE_INSUFFICIENT`.

Premodern same-name Tianwu is now mechanically separated from the current Ziwei rule. `历事明原`, the 1713 `御定星历考原`, and Qing `钦定协纪辨方书` preserve Tianwu as a calendrical month deity with `常居月建前二辰`. The Xingli Kaoyuan neighborhood disambiguates that phrase through explicit Fude examples as month-build branch plus two positions.

Replaying that mechanic gives `辰巳午未申酉戌亥子丑寅卯` for lunar months 1..12. Current `STAR.TIANWU` uses `巳申寅亥` repeated every four months. The tables match only in months 8 and 11 (**2/12**) and differ in the other ten months. The classical Tianwu homonym is therefore **disproved as the direct mechanical source** of the current Ziwei four-horse table.

This is source-domain closure, not an algorithm change. The historical calendrical Tianwu remains valid in its own tradition; the current Ziwei table still lacks an edition-bound premodern Ziwei placement witness. Same name and two coordinate coincidences do not authorize identity collapse.

No runtime/profile/rule-set/hash/candidate/default change and no algorithm reopen. Matrix remains 220/220 audited / 10 current missing; provenance defects 40/40; status distribution remains HISTORICALLY_SUPPORTED 96 / SOURCE_INSUFFICIENT 9 / DISPUTED_MULTIPLE_CANDIDATES 30 / NOT_YET_FORMALIZED 1.

Next: **12OB — HPA-ZMINOR-025 Tianyue lunar-month twelve-value table**, preserving the source-domain firewall against 天月德 / 天月德合 and other homonyms.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TIANWU-HOMONYM-MECHANICAL-SEPARATION-OA.md`. Research record: `docs/research/ZIWEI-TIANWU-HOMONYM-MECHANICAL-SEPARATION-R1.json`.


## Progress — Batch 12OB

`HPA-ZMINOR-025` **Tianyue lunar-month twelve-value table** remains `SOURCE_INSUFFICIENT`.

The current mnemonic `一犬二蛇三在龙，四虎五羊六兔宫，七猪八羊九在虎，十马冬犬腊寅中` is stable across modern Ziwei received material. A current open-source implementation reproduces the same table while explicitly marking the classical provenance as `古籍待考、后世悬曜增补`. These are useful modern compatibility witnesses, not premodern authority.

The source-domain firewall is explicit: `三命通会` Tian-De / Yue-De / Tian-Yue-De-He material belongs to a different shensha/day-selection rule family and is not merged with `STAR.TIANYUE_MOON` merely by lexical proximity.

No edition-bound premodern Ziwei exact-table witness was established in the reviewed public surfaces, so the row is not upgraded. This non-finding is scoped to the reviewed search surface and is not an absolute assertion that no earlier witness exists.

No runtime/profile/rule-set/hash/candidate/default change and no algorithm reopen. Matrix remains 220/220 audited / 10 current missing; provenance defects 40/40; status distribution remains HISTORICALLY_SUPPORTED 96 / SOURCE_INSUFFICIENT 9 / DISPUTED_MULTIPLE_CANDIDATES 30 / NOT_YET_FORMALIZED 1.

Next: **12OC — HPA-ZMINOR-026 Yinsha lunar-month six-value cycle**.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TIANYUE-MODERN-RECEIVED-SOURCE-BOUNDARY-OB.md`. Research record: `docs/research/ZIWEI-TIANYUE-MODERN-RECEIVED-SOURCE-BOUNDARY-R1.json`.


## Progress — Batch 12OC

`HPA-ZMINOR-026` **Yinsha lunar-month six-palace cycle** remains `SOURCE_INSUFFICIENT`.

The current cycle `正七寅、二八子、三九戌、四十申、五十一午、六十二辰` is stable in modern Ziwei received material. A modern open-source implementation reproduces the exact cycle and explicitly marks its provenance as `古籍待考、后世悬曜增补`. This is useful evidence for modern compatibility and source uncertainty, not premodern authority.

No qualifying premodern Ziwei exact-cycle witness was established in the reviewed public surfaces. Same-name Yinsha material from other systems remains outside this rule identity unless input dimension and placement mechanics can be bridged explicitly.

No runtime/profile/rule-set/hash/candidate/default change and no algorithm reopen. Matrix remains 220/220 audited / 10 current missing; provenance defects 40/40; status distribution remains HISTORICALLY_SUPPORTED 96 / SOURCE_INSUFFICIENT 9 / DISPUTED_MULTIPLE_CANDIDATES 30 / NOT_YET_FORMALIZED 1.

Next: **12OD — re-rank the remaining SOURCE_INSUFFICIENT / NOT_YET_FORMALIZED work queue after completing the active month-table provenance trio.**

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YINSHA-MODERN-RECEIVED-SOURCE-BOUNDARY-OC.md`. Research record: `docs/research/ZIWEI-YINSHA-MODERN-RECEIVED-SOURCE-BOUNDARY-R1.json`.


## Progress — Batch 12OD

After 12NZ–12OC, unresolved work is re-ranked rather than continued by row number. Current inventory remains **30 DISPUTED_MULTIPLE_CANDIDATES / 9 SOURCE_INSUFFICIENT / 1 NOT_YET_FORMALIZED**.

The remaining source-insufficient set is now mostly decomposed parents, recently source-bounded month rows, non-semantic display ordering, fail-closed/absent behavior, or rows already deeply audited in 12NW/12NX. Its marginal closure value is lower than active disputed production selections.

The next priority therefore shifts back to the disputed queue. **HPA-ZMINOR-022 YueDe** is selected first: production currently uses the Zi-year-Si-start family, while received Fullbook preserves a competing Zi-start family, and temporal scope still needs explicit typing. This is a compact, directly product-relevant candidateization problem.

Second tier: HPA-ZMINOR-008 TianShou Body/Life basis and HPA-ZMINOR-007 TianChu competing tables. High-impact late-Zi/date-boundary families remain important but already have extensive candidate preservation and historical-coordinate audits.

No Matrix status, runtime, default, candidate selection or algorithm changed.

Next: **12OE — HPA-ZMINOR-022 YueDe Si-start vs Zi-start historical families and natal/flow temporal candidate closure**.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-UNRESOLVED-HISTORICAL-STATUS-REPRIORITIZATION-OD.md`. Research record: `docs/research/HISTORICAL-UNRESOLVED-STATUS-REPRIORITIZATION-OD-R1.json`.

## Progress — Batch 12OE

`HPA-ZMINOR-022` **YueDe start-anchor conflict** is now decomposed by temporal layer instead of treated as one natal winner contest.

The decisive received-Fullbook local sequence says:

- TianDe: `从酉上起子，顺数至流年太岁`;
- YueDe: `从子上起子，顺数至流年太岁`;
- JieShen: `从戌上起子，逆数至当生年太岁`.

The contrast is explicit. Fullbook TianDe/YueDe are flow-year rules; JieShen is birth-year. Therefore Fullbook YueDe Zi-start is **not** a same-layer natal competitor to the current birth-year Si-start YueDe.

`神峰通考` preserves the premodern verse `欲求天德顺从酉，月德要依巳顺逢`. It is retained as a cross-domain geometry witness, not promoted into edition-bound Ziwei natal adoption proof.

Runtime preservation is now symmetric. `RECEIVED-FULLBOOK-ANNUAL-YUEDE-ZI-START-R1` and `RECEIVED-FULLBOOK-ANNUAL-TIANDE-YOU-START-R1` are emitted as `ANNUAL`, source-scoped, unselected candidate sets. They are visible through the existing candidate surface and do not rewrite natal `STAR.YUEDE` / `STAR.TIANDE`.

**PROV-DEFECT-041** is repaired forward-only. `HPA-ZMINOR-006` previously bundled TianDe with year-based JieShen and used the Fullbook flow-year TianDe sentence as support for natal TianDe. It now retains only year-based JieShen / modern `STAR.NIANJIE`. Natal TianDe is split into new `HPA-ZMINOR-027`, while the annual Fullbook pair is tracked by new `HPA-ZTEMP-007`.

Status changes:

- `HPA-ZMINOR-022`: `DISPUTED_MULTIPLE_CANDIDATES -> SOURCE_INSUFFICIENT` for **natal** YueDe adoption;
- `HPA-ZMINOR-027`: new `SOURCE_INSUFFICIENT` natal TianDe provenance row;
- `HPA-ZTEMP-007`: new `HISTORICALLY_SUPPORTED` received-Fullbook annual TianDe/YueDe source-scoped candidate row;
- `HPA-ZMINOR-006`: remains `HISTORICALLY_SUPPORTED` for birth-year JieShen/NianJie after removing the TianDe scope overclaim.

No production default, natal coordinate, candidate winner or chart algorithm changed.

Matrix becomes **222/222 audited / 10 current missing**. Status distribution is HISTORICALLY_SUPPORTED 97 / SUPPORTED_BUT_SCHOOL_SPECIFIC 24 / DISPUTED_MULTIPLE_CANDIDATES 29 / MODERN_COMPATIBILITY_ONLY 50 / SOURCE_INSUFFICIENT 11 / MISSING_FROM_PRODUCT 10 / NOT_YET_FORMALIZED 1. Provenance defects are **41/41 repaired**; historical candidate extensions are **8**; chart algorithm defects / reopens / candidate collapses remain **0/0/0**.

The transmission graph now separates natal and annual TianDe/YueDe rule families, binds the Fullbook passage to annual rule families and birth-year JieShen separately, and records only a possible cross-domain structural bridge from Shenfeng to the natal start-anchor mechanics.

Next: **12OF — HPA-ZMINOR-008 TianShou Body/Life basis source and candidate closure.**

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YUEDE-TIANDE-TEMPORAL-SCOPE-CLOSURE-OE.md`. Research record: `docs/research/ZIWEI-YUEDE-TIANDE-TEMPORAL-SCOPE-CLOSURE-R1.json`.

## Progress — Batch 12OF

`HPA-ZMINOR-008` **TianShou Body/Life basis conflict** is closed as a provenance overclaim rather than a real two-candidate rule dispute.

1581 `EXT-ZIWEI-JIELAN-1581`, chapter 35 `安天才天寿台辅封诰星诀`, states `命宫起子天才顺，身宫起子天寿堂`. The same chapter then gives two worked examples: for 甲子, Body in 午 gives TianShou in 午; for 乙丑, Body in 午 advances one palace to 未. The Life/Body distinction is therefore repeated by both mnemonic and examples.

The current S01 extraction is likewise internally consistent: `ZZZA-A-0830`, `0831`, `0833`, and `0834` all use Body palace as TianShou's 子-year origin. The old normalized `ZZZA-PR-042` note that a source-body/table-header basis conflict existed does not identify or locate a competing Life-basis source side.

The frozen Wenmo discriminator independently separates the formulas operationally: with Life=亥, Body=丑, birth-year branch=申, Wenmo gives TianShou=酉; Body-basis yields 酉 while Life-basis would yield 未. This is compatibility evidence only, but it agrees with the early-print rule.

**PROV-DEFECT-042** is repaired forward-only. The current Matrix no longer manufactures an unbound Life-basis candidate. This does not assert global nonexistence of another tradition; any future Life-basis method must arrive with a quoted, located, source-scoped witness before entering the candidate registry.

`HPA-ZMINOR-008` changes `DISPUTED_MULTIPLE_CANDIDATES -> HISTORICALLY_SUPPORTED`. `HPA-ZMINOR-019` is also updated so its TianCai row no longer claims TianShou remains disputed.

No production coordinate, default or chart algorithm changes. Matrix remains **222/222 audited / 10 current missing**. Status distribution becomes HISTORICALLY_SUPPORTED 98 / SUPPORTED_BUT_SCHOOL_SPECIFIC 24 / DISPUTED_MULTIPLE_CANDIDATES 28 / MODERN_COMPATIBILITY_ONLY 50 / SOURCE_INSUFFICIENT 11 / MISSING_FROM_PRODUCT 10 / NOT_YET_FORMALIZED 1. Provenance defects are **42/42 repaired**; historical candidate extensions remain **8**.

The transmission graph now records the Jielan chapter as one passage transmitting two complementary rules: Life-basis TianCai and Body-basis TianShou.

Next: **12OG — HPA-ZMINOR-007 TianChu competing heavenly-stem tables and source closure.**

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TIANSHOU-BODY-BASIS-EARLY-PRINT-CLOSURE-OF.md`. Research record: `docs/research/ZIWEI-TIANSHOU-BODY-BASIS-EARLY-PRINT-CLOSURE-R1.json`.

## Progress — Batch 12OG

`HPA-ZMINOR-007` **TianChu heavenly-stem table** is upgraded from `DISPUTED_MULTIPLE_CANDIDATES` to `HISTORICALLY_SUPPORTED` for placement geometry.

Ming Wan Minying's `星學大成` received Siku text, juan 1 `論天厨`, preserves the TianChu verse and identifies the star as `食神祿`. Parsed across all ten heavenly stems, its table is:

`甲巳、乙午、丙子、丁巳、戊午、己申、庚寅、辛午、壬酉、癸亥`.

The current runtime table matches **10/10**. Star identity and input dimension also agree: TianChu keyed by birth-year heavenly stem.

This closes the existence and exact geometry of the premodern TianChu table. It does **not** close the exact documentary path by which the table entered Ziwei. The transmission graph therefore records a high-confidence premodern rule witness and only a `PROBABLE` structural mechanism bridge into the modern Ziwei TianChu rule family.

**PROV-DEFECT-043** is repaired forward-only. The old Matrix described a competing “Fullbook variant table pending extraction” based solely on the normalized S01 note `标记与全书异表`. No verbatim competing table, frozen `ZZQS` atom, locator or edition-bound source side is currently bound. The live Matrix therefore no longer manufactures that unbound method as a historical candidate.

This is a bounded conclusion, not a global claim that every Fullbook recension lacks TianChu. Any future competing variant must be quoted, located and edition-bound before entering candidate state.

No runtime, production default or chart algorithm changes.

Matrix remains **222/222 audited / 10 current missing**. Status distribution becomes HISTORICALLY_SUPPORTED 99 / SUPPORTED_BUT_SCHOOL_SPECIFIC 24 / DISPUTED_MULTIPLE_CANDIDATES 27 / MODERN_COMPATIBILITY_ONLY 50 / SOURCE_INSUFFICIENT 11 / MISSING_FROM_PRODUCT 10 / NOT_YET_FORMALIZED 1. Provenance defects are **43/43 repaired**; historical candidate extensions remain **8**.

Next: **12OH — re-rank the remaining active DISPUTED_MULTIPLE_CANDIDATES queue after TianShou/TianChu closure.**

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TIANCHU-PREMODERN-TABLE-AND-SOURCE-BOUNDARY-OG.md`. Research record: `docs/research/ZIWEI-TIANCHU-PREMODERN-TABLE-AND-SOURCE-BOUNDARY-R1.json`.

## Progress — Batch 12OH

The remaining unresolved queue is re-ranked by source closure, deterministic readiness, product impact and shared implementation leverage.

**Tier 1** is the shared Jielan 1581 source-scoped natal candidate surface:

- `HPA-ZIWEI-015` Jielan Kui/Yue Geng variant;
- `HPA-ZIWEI-016` Jielan Fire/Bell 巳酉丑 variant;
- `HPA-ZIWEI-022` Jielan Mingzhu birth-year-branch basis.

All three already have deterministic `PRESERVED_NOT_SELECTED` resolution inside `historical_candidates.py`; Batch 12NR confirmed the remaining gap is public package/API/Workbench lineage. One shared product surface can therefore close three rows without changing production defaults.

Four-Transformation candidate families, Jielan dignity and TaiSui/Suiqian label variants form Tier 2. Late-Zi/date-boundary, historical Dayun calendarization and complete leap-month temporal frames remain high-impact but are currently source-semantics constrained rather than implementation-ready.

No Matrix status, production default, candidate selection or provenance-defect count changes in 12OH.

Next: **12OI — productize the Jielan 1581 source-scoped natal candidate runtime as an explicit read-only candidate-profile API / Workbench lineage surface.**

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-UNRESOLVED-CANDIDATE-PRODUCTIZATION-REPRIORITIZATION-OH.md`. Research record: `docs/research/HISTORICAL-CANDIDATE-PRODUCTIZATION-REPRIORITIZATION-OH-R1.json`.

## Progress — Batch 12OI

The Tier-1 action selected by 12OH is now productized: the existing Jielan 1581 historical candidate resolver has an explicit **read-only** candidate-profile API and Workbench surface.

Closed product gaps:

- `HPA-ZIWEI-015` — Jielan Kui/Yue Geng-stem variant;
- `HPA-ZIWEI-016` — Jielan Fire/Bell 巳酉丑 start-family variant;
- `HPA-ZIWEI-022` — Jielan Mingzhu birth-year-branch basis.

The public identity is:

`ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATE-API-R1@1.0.0`

over:

- registry `ZIWEI-JIELAN-1581-HISTORICAL-CANDIDATES-R1@1.1.0`;
- runtime resolver `ZIWEI-JIELAN-1581-SOURCE-SCOPED-CANDIDATE-RUNTIME-R1@1.0.0`;
- `selection_status=PRESERVED_NOT_SELECTED`.

Only `kui_yue`, `fire_bell` and `mingzhu` are released. The browser renders backend-returned facts and does not contain candidate placement formulas. No production selector, rank, winner or chart mutation was added.

The payload binds the exact combined manifest, Ziwei source bundle, natal fact/computation hashes, registry hash and candidate-runtime hash. Product visibility therefore remains auditable without becoming historical arbitration.

Accounting after 12OI:

- Matrix: **222/222 audited**;
- HISTORICALLY_SUPPORTED: **102**;
- current MISSING_FROM_PRODUCT: **7**;
- historical candidate extensions: **11**;
- candidate registries / runtime resolvers: **3 / 3**;
- provenance defects: **43 / 43 repaired**;
- production default / candidate winner / algorithm reopen: **unchanged / none / 0**.

Next: **12OJ — HPA-ZIWEI-014 whole-table Four-Transformation source families and candidate readiness.**

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JIELAN-SOURCE-SCOPED-NATAL-CANDIDATE-PRODUCTIZATION-OI.md`.

## Progress — Batch 12OJ

`HPA-ZIWEI-014` now has complete deterministic **whole-table** candidate readiness for the two genuinely divergent families that Batch 12NS had identified as missing.

Internal identities:

- `ZIWEI-FOUR-TRANSFORMATION-HISTORICAL-CANDIDATES-R1@1.0.0`;
- `ZIWEI-FOUR-TRANSFORMATION-SOURCE-SCOPED-CANDIDATE-RUNTIME-R1@1.0.0`;
- `selection_status=PRESERVED_NOT_SELECTED`;
- `whole_table_only=true`;
- `cell_level_hybridization_allowed=false`.

Source-scoped received Fullbook candidate `RECEIVED-FULLBOOK-SHIDIAN-V3-FOUR-TRANSFORMATION-R1` differs from production at exactly three cells: 庚化科 太阴→天同, 庚化忌 天同→天相, 壬化科 左辅→天府.

Modern Zhongzhou candidate `ZHONGZHOU-WANGTINGZHI-FOUR-TRANSFORMATION-R1` differs at exactly three cells: 戊化科 右弼→太阳, 庚化科 太阴→天府, 壬化科 左辅→天府.

The received Fullbook candidate is deliberately tied to the Shidian received transcription. Other received surfaces preserve other Geng readings, so 12OJ does not collapse them into a universal Fullbook table.

The transmission graph now contains separate Jielan 1581, Shidian received-Fullbook and Wang Tingzhi Zhongzhou whole-table rule families and only asserts parallel coexistence among them; no direct copying direction or historical winner is inferred.

`HPA-ZIWEI-014` remains **MISSING_FROM_PRODUCT** because the two divergent families are internal candidates only. Accounting: **222/222 audited**, **7 current missing**, candidate extensions **13**, candidate registries/runtime resolvers **4/4**, provenance defects **43/43**, algorithm reopens **0**.

Next: **12OK — read-only Four-Transformation whole-table candidate productization.**

## Progress — Batch 12OK

`HPA-ZIWEI-014` competing Four-Transformation table families now have an explicit read-only product surface.

Public contract:

`ZIWEI-FOUR-TRANSFORMATION-HISTORICAL-CANDIDATE-API-R1@1.0.0`

The endpoint `/api/ziwei-four-transformation-candidates` derives the natal source stem from the exact validated Ziwei bundle and returns **both** divergent whole-table candidates simultaneously. It takes no historical winner input.

The response binds the combined manifest, Ziwei bundle, natal FactHash/ComputationHash, registry hash, candidate runtime hashes and source refs. The Workbench renders only returned assignment fields; it contains no Four-Transformation table constants or cell-level calculation rules.

Firewalls remain:

- `whole_table_only=true`;
- `cell_level_hybridization_allowed=false`;
- `selection_status=PRESERVED_NOT_SELECTED`;
- production `S08_CURRENT_40_ASSIGNMENT_R1` unchanged;
- no winner button or production profile selector.

Accordingly `HPA-ZIWEI-014` changes `MISSING_FROM_PRODUCT -> HISTORICALLY_SUPPORTED`. Matrix remains **222/222 audited**, HISTORICALLY_SUPPORTED becomes **103**, current MISSING_FROM_PRODUCT becomes **6**, candidate extensions remain **13**, registries/runtime resolvers **4/4**, provenance defects **43/43**.

Next: **12OL — re-rank the six remaining product gaps.**

## Progress — Batch 12OM

`HPA-ZIWEI-018` now has an internal **source-lexeme** dignity candidate rather than a forced modern-grade table.

Registry:

`ZIWEI-JIELAN-1581-DIGNITY-LEXEME-CANDIDATES-R1@1.0.0`

Candidate:

`JIELAN-1581-DIGNITY-CH70-SOURCE-LEXEME-R1`

Runtime:

`ZIWEI-JIELAN-1581-DIGNITY-LEXEME-RUNTIME-R1@1.0.0`

The CH70 star-oriented table is represented as 25 entities/groups × 12 branches = **300 cells**. Each cell preserves its source lexeme set, attested/un-stated status and conflict flag. Explicit gloss relations are stored as lexical relations only; no OPERATIONAL-ZIWEI-DIGNITY-R4 grade is inferred.

Preserved anomalies include 紫微午宫 `庙 + 平`, 巨门丑宫 `局 + 陷`, and 天机巳宫 `UNSTATED_IN_CH70_STAR_VERSE`.

CH69 remains a parallel palace-oriented source table and is not used to silently fill or adjudicate CH70. That cross-collation is the next batch.

Accounting: **222/222 audited**, **6 current missing**, candidate extensions **14**, registries/runtime resolvers **5/5**, provenance defects **43/43**.

Next: **12ON — CH69/CH70 cell-level dignity cross-collation.**

## Progress — Batch 12ON

`HPA-ZIWEI-018` now has complete **CH69↔CH70 cell-level cross-collation**.

The comparison grid is 25 CH70 entities/groups × 12 branches = **300 cells**. The frozen relation counts are:

- 97 exact lexeme overlaps;
- 37 source-explicit direct equivalents;
- 54 source-local polarity conflicts;
- 21 cells where both chapters attest values but no direct gloss proves equivalence;
- 82 CH69 unstated cells;
- 8 CH69 text-unresolved cells;
- 1 CH70 unstated cell.

The eight CH69 unresolved cells are not silently repaired. The parser refuses to split singular `文` into 文昌/文曲, refuses to assign the ambiguous 丑 `羊陀火破` group a category, refuses to rewrite 辰 `午` to `日`, and refuses to infer 文昌 from the truncated 寅 `曲与`.

The three controlling anomalies remain explicit: 紫微午 keeps CH70 `庙+平`; 巨门丑 keeps CH70 `局+陷`; 天机巳 remains CH70-un-stated even though CH69 records `兴`. CH69 is therefore parallel evidence, **not a fill source**.

No production R4 grade/status is inferred. No chapter is allowed to overwrite the other. No historical winner is selected.

`HPA-ZIWEI-018` remains `MISSING_FROM_PRODUCT`, but the remaining gap is now only the explicit read-only candidate API / Workbench surface. Internal raw candidate plus source reconciliation are complete.

Next: **12OO — read-only Jielan dignity candidate product surface.**

## Progress — Batch 12OO

`HPA-ZIWEI-018` **1581 Jielan historical dignity table** now has a complete read-only product surface.

Endpoint:

`POST /api/ziwei-jielan-1581-dignity-candidate`

The sidecar returns 300 CH70 raw-source-lexeme rows and 300 CH69↔CH70 cross-collation rows, bound to the exact combined manifest / Ziwei bundle / natal fact and computation hashes. It also exposes registry, candidate-runtime and cross-collation hashes.

The Workbench groups backend-returned rows by star/entity and displays branch, CH70 lexemes, CH69 lexemes and relation classification. Browser JavaScript contains no source table constants, no cross-collation formula and no production dignity grade conversion.

The historical firewall remains unchanged: `PRESERVED_NOT_SELECTED`; no CH69->CH70 fill; no CH70 overwrite of CH69; no production-grade mapping; no winner control; no production profile change.

Accordingly `HPA-ZIWEI-018` changes `MISSING_FROM_PRODUCT -> HISTORICALLY_SUPPORTED`. This is a **product representation closure**, not a historical-winner claim.

Matrix remains **222/222 audited**. Status now includes HISTORICALLY_SUPPORTED **104** and current MISSING_FROM_PRODUCT **5**. Candidate extensions remain 14, registries/runtime resolvers 5/5, provenance defects 43/43, algorithm reopens 0.

Next: **12OP — HPA-ZT-015 leap-month day-one daily-origin geometry / historical candidate closure.**


## Progress — Batch 12OP

`HPA-ZT-015` Zhongzhou leap-month day-one/daily geometry is now source-closed as a **school-scoped historical candidate**, without selecting it as the production default.

Direct Wang Tingzhi text and S10 P-0282 close the first-half origin: after the preceding regular month's last flow day, counting continues forward, so leap day 1 depends on whether that regular month had 29 or 30 days. P-0283 switches leap day 16+ to the following regular month's monthly-palace basis. The general flow-day clause controls the arithmetic: the monthly palace is the day-1 basis and the actual requested day ordinal is counted forward, so the 15/16 switch changes basis but does not renumber day 16 as a new day 1.

The existing `ZHONGZHOU-LEAP-MONTH-HALF-SPLIT-R1` candidate is extended in place through API 1.2.0 / registry 1.1.0 / runtime 1.1.0. Shared projection supplies the preceding regular-month length, emits `leap_day_one_active_branch` and `daily_active_address_branch`, and preserves `half_split_basis_switch=true`, `half_split_reset=false`, `PRESERVED_NOT_SELECTED`.

Workbench now exposes the backend-computed daily palace and basis-switch fields without browser placement math. Ordinary production leap-month monthly/daily fields remain fail-closed.

`PROV-DEFECT-044` repairs the stale live Matrix claim that day-one/daily geometry was still source-unclosed. It also narrows scope: natal leap-month doctrines are not silently treated as the same rule as flow-month/day geometry.

`HPA-ZT-015` moves `MISSING_FROM_PRODUCT -> SUPPORTED_BUT_SCHOOL_SPECIFIC`; `HPA-ZTEMP-006` remains `SUPPORTED_BUT_SCHOOL_SPECIFIC` with its now-complete daily geometry. Matrix remains **222/222 audited**; `SUPPORTED_BUT_SCHOOL_SPECIFIC=25`, `MISSING_FROM_PRODUCT=4`, candidate extensions 14, registries/runtime resolvers 5/5, provenance defects 44/44, chart algorithm defects/reopens/candidate collapses 0.

`transmission_impact=NONE`: this is a semantic/mechanical closure inside an already registered modern Zhongzhou witness, not a new ancestry edge.

Next: **12OQ** — re-rank the four remaining product gaps (`HPA-ZDATE-006`, `HPA-DAYUN-CAL-002/003/004`) by evidence-acquisition readiness and dependency depth before resuming the highest-value blocked source route; do not repeat exhausted public-preview searches.

Batch document: `docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHONGZHOU-LEAP-MONTH-DAILY-GEOMETRY-CLOSURE-OP.md`. Research record: `docs/research/ZIWEI-ZHONGZHOU-LEAP-MONTH-DAILY-GEOMETRY-CLOSURE-R1.json`.
