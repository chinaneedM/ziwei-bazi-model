# Ming Datong Qishuo Geographic Reference Research R1

Status: **RESEARCH-ONLY / GEOGRAPHIC REFERENCE STILL UNRESOLVED / NO RUNTIME SELECTION**

Date: 2026-09-05

This note continues Batch 11G without claiming a new completed historical-audit batch. It isolates the unresolved question:

> What geographic/meridian reference, if any, is encoded by the Ming Datong `定朔` / `朔小餘` time coordinate?

The internal clock/day coordinate is already source-closed in Batch 11G as `子正` / 100-ke. This note addresses only the independent longitude/geography problem.

## 1. Evidence now securely distinguished

### 1.1 Yuan Shoushi location-specific material explicitly names Dadu

`《元史·授時曆經下·步中星第五》` explicitly begins with the Dadu polar altitude (`大都北極，出地四十度太強`) and gives Dadu-linked day/night material. Received historical summaries likewise state that Shoushi used Dadu as the standard for sunrise/sunset day-length calculations.

This proves that **some Shoushi modules are explicitly location-scoped to Dadu**.

It does **not** by itself prove that every qishuo small remainder is a Dadu-meridian local apparent solar time.

### 1.2 Ming received material explicitly distinguishes Nanjing/Beijing daylight regimes

Ming historical material records the dispute after the move of the capital: Beijing and Nanjing have different polar altitude, sunrise/sunset and clepsydra behavior; at points Beijing values were introduced and at points policy reverted to older Hongwu/Yongle practice.

This proves that **location-dependent daylight/timekeeping parameters were consciously distinguished by Ming calendar officials**.

It does **not** license inheritance from the sunrise/sunset table location to the qishuo conjunction coordinate.

### 1.3 Peer-reviewed modern reconstruction separates longitude explicitly

Byeong-Hee Mihn, Ki-Won Lee and Young-Sook Ahn, “Analysis of interval constants in calendars affiliated with the Shoushili,” *Research in Astronomy and Astrophysics* 14 (2014), 485–496, DOI 10.1088/1674-4527/14/4/009, compares Shoushili/Datongli/Naepyeon with modern astronomical calculations.

The authors:

- convert modern UT to local apparent solar time;
- explicitly adopt Beijing, Nanjing and Seoul coordinates;
- state that longitude differences can be used to convert Beijing time to other locations (example: Seoul is +42.26 min for a 10.566° longitude difference);
- evaluate new-moon timing separately at Beijing and Seoul;
- independently verify that Shoushili-Licheng sunrise/sunset data fit Beijing while the Mingshi/Tonggui sunrise/sunset data fit Nanjing.

This is strong **modern computational evidence that longitude matters when comparing the historical numerical time coordinate with modern ephemerides**.

It is not a primary Ming statement defining the qishuo meridian.

### 1.4 Korean Datong transmission is an important control case

Ki-Won Lee, Young-Sook Ahn, Byeong-Hee Mihn and Young-Ran Lim, “Study on the Period of the Use of Datong-li in Korea,” *Journal of Astronomy and Space Sciences* 27 (2010), 55–68, reconstructs Datong-li calendar dates and compares them with Korean historical records and surviving almanacs.

The Korean transmission demonstrates that Datong computational rules and constants could be received and reused outside Ming China. This makes it methodologically unsafe to infer an implicit geographic reference merely from the place where a later copy or implementation was used.

Again, this is a control on inference, not a primary definition of the Ming qishuo meridian.

## 2. Current evidence classification

| Proposition | Status | Reason |
|---|---|---|
| `MING_DATONG_INTERNAL_DAY_BOUNDARY = 子正` | CLOSED | Primary 1569 arithmetic + Ming worked replay; Batch 11G |
| `SHOUSHI_SOME_LOCATION_DEPENDENT_TABLES = DADU` | SUPPORTED | Explicit Dadu wording in `《元史·授時曆經》` and later historical summaries |
| `MING_SUNRISE_SUNSET_TABLES_CAN_BE_NANJING_SCOPED` | SUPPORTED | Ming received text + modern numerical verification |
| `MING_QISHUO_REFERENCE = NANJING` | UNRESOLVED | No direct qishuo-meridian statement found |
| `MING_QISHUO_REFERENCE = BEIJING/DADU` | UNRESOLVED | Inheritance from Shoushi epoch/lineage is plausible but not yet textually or algorithmically closed |
| `MING_QISHUO_REFERENCE = CAPITAL_OF_YEAR` | UNRESOLVED | Ming capital/daylight policy changes do not by themselves prove qishuo retiming |
| `MING_QISHUO_REFERENCE = MODERN_CHINA_STANDARD_TIME/UTC+8` | FORBIDDEN | Anachronistic unless explicitly used only as a modern conversion layer |

## 3. Strongest working hypotheses — preserved, not selected

### H1 — inherited Shoushi/Dadu-origin coordinate

Rationale:

- Datong qishuo arithmetic is descended from Shoushi;
- Shoushi epoch work was tied to Yuan observatory/measurement practice centered on Dadu, while the Shoushi corpus explicitly carries Dadu location data in some modules;
- modern researchers commonly compare the inherited interval-constant chronology in Beijing apparent solar time.

Required closure evidence:

1. a primary/near-primary Shoushi or early Datong statement linking qishuo small remainder, epoch, `子正`, or `夜半` to Dadu local time/meridian; or
2. a source-faithful replay showing that the printed official Ming qishuo clock labels consistently require the Dadu/Beijing longitude and fail under Nanjing by the longitude offset, across enough near-boundary cases to exclude coincidence.

### H2 — Ming Nanjing/official-Tonggui coordinate

Rationale:

- Ming received Datong daylight tables are demonstrably Nanjing-scoped;
- Hongwu-era institutional production began at Nanjing, and historical records preserve continued Nanjing/Hongwu-Yongle standards in parts of the calendar system.

Required closure evidence:

- direct qishuo wording or replay showing that conjunction clock labels were retimed to Nanjing rather than merely carrying Nanjing sunrise/sunset tables.

### H3 — module-specific mixed geography

This may be historically correct: qishuo epoch arithmetic could preserve a Shoushi/Dadu-origin time coordinate while sunrise/sunset/eclipses use a Ming Nanjing table, with later Beijing policy changes affecting only selected modules.

This hypothesis is especially important because the surviving evidence already demonstrates that historical calendar systems could mix inherited interval constants with location-specific tables.

It must remain explicit until source genealogy and replay decide it.

## 4. Next decisive tests

1. Search `《授時曆議》`, `《授時曆經》`, `《大統曆法通軌》`, Zhou Xiang 1569 `《大明大統曆法》`, Xing Yunlu `《古今律曆考》`, official Ming almanacs and Qintianjian memorials specifically for `大都/北京/南京/應天/順天/子正/夜半/合朔/定朔/經度/里差/地差` co-occurrence.
2. Transcribe the full 1569 qishuo tables and carry/interpolation semantics so qishuo clock labels can be reproduced source-faithfully.
3. Build a research-only replay of official almanac conjunction clock labels for years with surviving printed times (1531, 1532, 1604, 1616, 1629, 1639, plus 1524/1578 targets).
4. For each replayed event, compare the source-derived clock label under:
   - no longitude adjustment / inherited source coordinate,
   - Dadu/Beijing local apparent solar time,
   - Nanjing local apparent solar time.
5. Prioritize events near `子正` where the Beijing–Nanjing longitude difference can move the event across a historical clock label or sexagenary-day boundary. These are much more diagnostic than midday cases.
6. Collate exact official almanac page images, not modern tables alone, before adjudicating.

## 5. Runtime firewall

Until the above closes:

```text
MING_DATONG_QISHUO_GEOGRAPHIC_REFERENCE = UNRESOLVED
MING_DATONG_QISHUO_GEOGRAPHIC_RUNTIME_SELECTION = FORBIDDEN
NO_MODERN_TIMEZONE_SUBSTITUTION = TRUE
NO_SUNRISE_TABLE_LOCATION_INHERITANCE = TRUE
HISTORICAL_CALENDAR_ADAPTER = FAIL_CLOSED
```

This note does not alter:

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1 = CLOSED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT = 0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION = NOT_YET_FORMALIZED
```

## 6. Critical-day controls from Ming reign records — new in this pass

The previously unresolved boundary cases were checked against `《明實錄》` rather than only later calendrical tables.

### 6.1 1370 month 2

`《明太祖高皇帝實錄》卷四十九` records:

```text
洪武三年二月辛酉朔
```

The D1 replay is `57.0024 = 辛酉`, only 3.456 minutes after 子正. The four later historical tables instead give 庚申.

This upgrades 辛酉 from a modern computational prediction to official-historiography corroboration, but **not** to same-year almanac certification.

### 6.2 1495 month 7

`《明孝宗敬皇帝實錄》卷一百二` records `弘治八年七月辛巳朔`. The D1 replay is `18.1775 = 壬午`, about 255.6 minutes after 子正.

This difference is far too large to be explained by the Beijing–Nanjing longitude difference. Therefore a simple fixed longitude shift cannot be used to “repair” every reign-record/D1 mismatch.

### 6.3 1497 month 10

`《明孝宗敬皇帝實錄》卷一百三十` records `弘治十年十月己巳朔`. The D1 replay is `4.9997 = 戊辰`, only 25.92 seconds before the next 子正.

A positive/eastward shift greater than 0.432 minutes would move this event into 己巳. The Beijing→Nanjing modern local-apparent-solar-time difference calculated from Mihn et al.'s coordinates is about 9 minutes 52 seconds, so it is **numerically compatible** with such a crossing.

But numerical compatibility is not historical identification. The source coordinate embedded in D1 is itself unresolved, and 1495 proves that longitude alone cannot explain all reign-record conflicts.

### 6.4 A known falsification control: 1462

This is the decisive warning against treating reign records as the physical calendar.

`《明英宗睿皇帝實錄》卷三百四十六` records `天順六年十一月壬辰朔`.

A surviving official Datong almanac, however, gives **辛卯**, and D1 gives `27.8143 = 辛卯`. The physical almanac therefore overrides both the reign record and the repeated later-table value.

### 6.5 A convergence control: 1581

`《明神宗顯皇帝實錄》卷一百一十七` records `萬曆九年十月辛卯朔`, agreeing with the surviving official almanac and D1 `27.9349 = 辛卯`, while the later tables give 壬辰.

Together, 1462 and 1581 prove that the evidential role of `《明實錄》` is **corroboration requiring case-by-case collation**, not automatic calendar certification.

## 7. Evidence-independence consequence

The fact that several later calendrical tables agree with one another is not equivalent to several independent witnesses. The 1462 case demonstrates a shared wrong day across multiple later tables while a surviving official almanac and source-faithful D1 replay agree against them.

Therefore:

```text
SOURCE_COUNT_VOTING = FORBIDDEN
REIGN_RECORD_AS_SAME_YEAR_ALMANAC_SUBSTITUTE = FORBIDDEN
LATER_TABLE_CONSENSUS_REQUIRES_GENEALOGY_AUDIT = TRUE
```

The machine-auditable companion artifact is:

`docs/research/MING-DATONG-QISHUO-GEOGRAPHIC-CRITICAL-CASES-R1.json`

Its regression test deliberately preserves the unresolved geographic conclusion.

## References consulted in this research pass

- `《元史·志第七·曆四·授時曆經下》`, Chinese Text Project / received historical text.
- `《明會要》卷二十七`, received Ming institutional-history witness.
- `《明太祖高皇帝實錄》卷四十九`.
- `《明英宗睿皇帝實錄》卷三百四十六`.
- `《明孝宗敬皇帝實錄》卷一百二、卷一百三十`.
- `《明神宗顯皇帝實錄》卷一百一十七`.
- Mihn, Byeong-Hee; Lee, Ki-Won; Ahn, Young-Sook. 2014. “Analysis of interval constants in calendars affiliated with the Shoushili.” *Research in Astronomy and Astrophysics* 14(4): 485–496. DOI: 10.1088/1674-4527/14/4/009.
- Lee, Ki-Won; Ahn, Young-Sook; Mihn, Byeong-Hee; Lim, Young-Ran. 2010. “Study on the Period of the Use of Datong-li in Korea.” *Journal of Astronomy and Space Sciences* 27(1): 55–68.
- Li, Yong; Zhang, Chengzhi. 1998. “Chinese syzygy calculation established in the 13th century.” *Astronomy & Astrophysics* 332: 1142–1146.
- Yuk Tung Liu, “明朝的定朔計算及曆表朔日訂正”, modern computational/source-collation research.

Research principle: modern reconstruction may test and discriminate historical hypotheses, but it does not become primary historical authority by numerical fit alone. Reign records are closer to official historical production than modern tables, but a surviving same-year Qintianjian almanac remains the stronger oracle for the calendar actually promulgated.


## 8. The exact 1497 target calendar was officially issued

`《明孝宗敬皇帝實錄》卷一百十九` records that on `弘治九年十一月甲辰朔` the Qintianjian presented the **弘治十年大統曆**. The emperor received it in the Fengtian Hall, distributed it to civil and military officials, and promulgated it throughout the realm.

This matters because the 1497 month-10 critical case is not an abstract reconstructed calendar year: a specific official Hongzhi-10 Datong almanac was produced and promulgated in late 1496.

The current research gap is therefore precise:

```text
HONGZHI_10_DATONG_ALMANAC_OFFICIALLY_ISSUED = TRUE
HONGZHI_10_DATONG_ALMANAC_PHYSICAL_COPY_LOCATED = FALSE
```

A surviving copy or page-level facsimile remains the decisive target.

## 9. Contemporary 1497 reform dispute: Zhu Sheng

The same reign year supplies an independent operational warning. `《明孝宗敬皇帝實錄》卷一百三十二` records on `弘治十年十二月丁亥` that **南京欽天監主簿諸升** complained:

```text
曆法有差，月食不驗
```

and requested a supervised reform by people skilled in astronomy and calendrical principles.

The Ministry of Rites defended the founding Datong system, explicitly invoking `推步測候`, `頒朔授時`, and the gravity of changing `歲差`. The emperor declined to change the calendar lightly.

This is strong evidence that a calendar-performance/reform dispute existed **in 1497 itself**, and that eclipse prediction was one observed point of failure.

It is **not** evidence that:

- the 1497 month-10 Shilu/D1 discrepancy was caused by the same defect;
- the qishuo meridian was Nanjing;
- a longitude shift explains the discrepancy.

The repository therefore preserves:

```text
ZHU_SHENG_1497_REFORM_CONTEXT = RELEVANT_OPERATIONAL_CONTEXT
ATTRIBUTE_1497_M10_QISHUO_MISMATCH_TO_ZHU_SHENG_MEMORIAL = FORBIDDEN_WITHOUT_DIRECT_LINK
```

## 10. 1521 Zhu Yu memorial: explicit mixed-location problem inside Datong practice

An even more diagnostic official statement appears in `《明世宗肅皇帝實錄》卷三`, dated `正德十六年六月壬辰`.

Qintianjian clepsydra doctor **朱裕** states, among other things:

- `雖以大統為名，實授時之曆`;
- accumulated calendrical values had gradually diverged and eclipse timing was no longer consistently matching;
- the Beijing observatory's instruments were difficult to use accurately;
- `推算曆數，用南京日出分杪，似相矛盾`;
- he proposed distributed gnomon observations and collation of internal/external shadow measurements with old/new almanacs;
- the stated goal was `庶幾合朔得真，交食不謬`.

This is the strongest source found so far for the **module-specific mixed-geography / inherited-system problem**. A Ming calendrical official explicitly recognized that inherited Datong/Shoushi practice and Nanjing location parameters could sit awkwardly inside the Beijing operational environment.

But the wording still identifies **南京日出分杪**, not the geographic reference of `定朔小餘` itself. Therefore:

```text
MING_DATONG_USED_NANJING_SUNRISE_PARAMETERS_IN_THE_CRITICIZED_WORKFLOW = SUPPORTED
MING_OFFICIAL_RECOGNIZED_LOCATION_PARAMETER_INCONSISTENCY = SUPPORTED
MING_QISHUO_MERIDIAN_DEFINED_BY_THIS_MEMORIAL = NO
INFER_QISHUO_MERIDIAN_FROM_NANJING_SUNRISE_PARAMETERS = FORBIDDEN
```

This substantially strengthens H3 (module-specific mixed geography), but does not close H1/H2/H3.

## 11. Updated evidential priority

The next highest-value evidence is now:

1. a physical/page-level **弘治十年大統曆**;
2. a physical/page-level **弘治八年大統曆**, because its 1495 conflict is far from the day boundary and cannot be repaired by a Beijing–Nanjing longitude shift;
3. direct primary wording connecting qishuo small remainder to a named place/meridian;
4. full source-faithful 1569 D1 replay with table interpolation and carry semantics;
5. comparison with eclipse/new-moon observations as a diagnostic layer only.

The 1497 and 1521 memorials demonstrate why a single-cause longitude model is historically unsafe: Ming officials themselves discussed accumulated error, eclipse mismatch, inherited Shoushi rules, instruments, and Nanjing location parameters as distinct interacting problems.


## 12. Hongzhi-8 target issuance and 1495 eclipse-warning context

### 12.1 The exact Hongzhi-8 calendar was officially issued

`《明孝宗敬皇帝實錄》卷九十四` records on `弘治七年十一月丙戌朔`:

```text
欽天監進弘治八年大統曆，上御奉天殿受之，給賜文武群臣，頒行天下
```

Therefore the 1495 target, like the 1497 target, was an actually produced and promulgated Qintianjian almanac. The missing evidence is the surviving physical/page-level copy, not whether such an official calendar existed.

```text
HONGZHI_8_DATONG_ALMANAC_OFFICIALLY_ISSUED = TRUE
HONGZHI_8_DATONG_ALMANAC_PHYSICAL_COPY_LOCATED = FALSE
```

### 12.2 A later Ming witness records a Hongzhi-8 lunar-eclipse prediction failure

Shen Defu's later Ming `《萬曆野獲編》卷二十九` records that on `弘治八年八月十六日望` a predicted lunar eclipse did not occur, and groups it with two later Hongzhi failures.

This is relevant operational evidence because the unresolved D1/Shilu qishuo conflict occurs in the preceding month of the same calendar year.

But temporal proximity is not causation. The later witness does not identify the computational defect, does not link it to the month-7 new moon, and does not define a qishuo meridian.

Therefore:

```text
HONGZHI_8_ECLIPSE_NON_EVENT = LATER_MING_OPERATIONAL_WARNING
CAUSALLY_LINK_HONGZHI_8_M07_QISHUO_CONFLICT_TO_M08_ECLIPSE_FAILURE = FORBIDDEN
```

## 13. Collection-scoped physical-copy screening

### 13.1 National Library of China 2007 facsimile collection

The official National Library of China Press description states that `《國家圖書館藏明代大統曆日彙編》` contains 99 kinds / 105 fascicles of Ming Datong almanacs, spanning 1446–1641.

The published contents list reaches:

- 成化二十年 / 1484;
- then jumps to 正德三年 / 1508.

No Hongzhi-year annual almanac appears in that collection's published contents. Consequently:

```text
NLC_2007_COLLECTION_HAS_HONGZHI_8 = FALSE
NLC_2007_COLLECTION_HAS_HONGZHI_10 = FALSE
INFER_GLOBAL_NONEXISTENCE_FROM_NLC_2007_ABSENCE = FORBIDDEN
```

This is a **collection-scoped negative**, not a claim that no copy survives elsewhere.

### 13.2 Seoul National University Kyujanggak

Kyujanggak's institutional feature on its calendar holdings identifies its `大明崇禎十年大統曆` (1637, 奎中 5567) as the institute's only Ming printed Datong almanac. The author further suggests it may be the only such Ming printed almanac then known in Korea.

The project uses only the institution-scoped part as a research control:

```text
KYUJANGGAK_MING_PRINTED_DATONG_TARGET_HONGZHI_8 = NOT_IN_IDENTIFIED_HOLDING
KYUJANGGAK_MING_PRINTED_DATONG_TARGET_HONGZHI_10 = NOT_IN_IDENTIFIED_HOLDING
INFER_KOREA_WIDE_NONEXISTENCE = FORBIDDEN
```

Other Korean institutional, private, and family collections remain searchable.

### 13.3 Hongzhi-17 positive survival control

A national-level catalogue and the holding institution now provide a positive control from the same reign. Entry `04638` of the second batch of the National Precious Ancient Books Register records:

```text
大明弘治十七年歲次甲子大統曆一卷
（明）韓昂等撰
明弘治十七年（1504）欽天監刻本
北京市文物局
```

The Beijing Municipal Cultural Heritage Bureau Library and Documentation Center independently confirms among its holdings a Ming-printed `《大明弘治十七年大統曆》`.

This changes the artifact-search logic in an important but narrow way:

```text
SURVIVING_HONGZHI_PERIOD_QINTIANJIAN_DATONG_ALMANAC = CONFIRMED
INFER_NO_HONGZHI_ALMANACS_SURVIVE_FROM_NLC_2007_GAP = FORBIDDEN
HONGZHI_8_TARGET_PHYSICAL_COPY_LOCATED = FALSE
HONGZHI_10_TARGET_PHYSICAL_COPY_LOCATED = FALSE
```

The Hongzhi-17 copy does **not** certify the Hongzhi-8 or Hongzhi-10 month-start values, and it does not identify the qishuo meridian. It is instead a same-reign physical-survival control showing that Hongzhi Qintianjian almanacs can survive outside the National Library of China facsimile collection.

The next artifact search should therefore include the Beijing holding lineage and national ancient-book census/catalogue data, while retaining the exact-title variants for `弘治八年歲次乙卯` and `弘治十年歲次丁巳`.

## 14. Joseon transmission lead

`《明孝宗敬皇帝實錄》卷一百三十二`, preserved in the Korean Ming-Qing Shilu interface, records on `弘治十年十二月二十二日`:

```text
己丑，賜朝鮮國大統曆一百本
```

This confirms a substantial official calendar-transmission channel from Ming to Joseon during the exact research period.

It does **not** by itself establish that a surviving copy is the Hongzhi-10 target annual, nor that the gifted copies remained in the present Kyujanggak/Jangseogak collections.

```text
JOSEON_DATONG_TRANSMISSION_CHANNEL_1497 = CONFIRMED
SPECIFIC_GIFT_COPY_IDENTITY_WITH_HONGZHI_10_TARGET = UNRESOLVED
SURVIVAL_OF_GIFTED_COPIES = UNRESOLVED
```

The Korean search path therefore remains active: Kyujanggak, Jangseogak, National Library of Korea, Academy of Korean Studies collections, institutional catalogues, and family-document corpora.

## 15. Negative-evidence discipline

The artifact search now uses a strict rule:

```text
SEARCH_RESULT_ABSENCE != HISTORICAL_NONEXISTENCE
COLLECTION_CATALOG_ABSENCE = COLLECTION_SCOPED_NEGATIVE_ONLY
INSTITUTIONAL_ONLY_COPY_STATEMENT = INSTITUTION_SCOPED_UNLESS EXHAUSTIVE NATIONAL SURVEY IS PROVEN
```

This matters because the target almanacs are ephemeral annual publications. Their documented issue and distribution can be source-closed even while currently indexed surviving copies remain unknown.

The next decisive objective remains the same: locate a physical/page-level Hongzhi-8 or Hongzhi-10 Datong almanac, with the 1495 target especially diagnostic because its D1/Shilu disagreement lies far outside any plausible Beijing–Nanjing longitude shift.
