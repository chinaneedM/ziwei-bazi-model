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

The initial inventory contained **107 rule/field families**. After Batches 01–11C and explicit splitting of historically distinct candidate families, the current machine-readable inventory contains **197 rows**, with **165 audited rows**. It intentionally keeps unresolved source work explicit rather than converting uncertainty into a chart defect. The current audit ledger records **9 confirmed provenance metadata defects repaired forward-only at the provenance/hash-lineage layer, 0 chart algorithm defects, 0 algorithm reopens, 13 identified missing candidate families, 2 source-scoped historical candidate registries, and 2 runtime resolvers**.

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
- Batch 08B: Ziwei temporal frames B; applied the formal 训诂 method to distinguish wording identity from mechanical identity. Flow-year TaiSui palace, Five-Tigers month Ganzhi and flow-day palace geometry are historically supported. The 1581 Jielan `日上起子时` day-anchored hour method is source-closed but missing from runtime; the current fixed-branch hour method remains a separate Zhongzhou case method. Zhongzhou leap-month `1–15 previous month / 16–end next month, day sequence continuous` is now a source-closed `MISSING_FROM_PRODUCT` candidate rather than `SOURCE_INSUFFICIENT`. No algorithm reopen.
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

The 1581 edition identity is independently corroborated by Shanghai Library linked-data instance `EXT-SHANGHAI-LIB-JIELAN-1581` (子4051; 明万历九年金陵书坊王洛川刻本). This is a bibliographic witness, not a substitute for chapter/facsimile rule-text collation.

## Cross-chat continuity

Long-running audit state is persisted in `docs/PROJECT-CURRENT-STATE-R1.json` and restored according to `docs/PROJECT-CONTINUITY-PROTOCOL-R1.md`. CI runs `scripts/verify-project-continuity-state-r1.py` so Matrix progress, completed batches, defect counts and non-negotiable invariants cannot drift from the handoff state unnoticed.
