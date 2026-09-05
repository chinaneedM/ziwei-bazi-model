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
