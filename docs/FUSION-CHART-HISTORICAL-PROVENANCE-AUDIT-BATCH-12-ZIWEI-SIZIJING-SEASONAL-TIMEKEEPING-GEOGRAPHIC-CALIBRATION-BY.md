# Fusion Chart Historical Provenance Audit R1 — Batch 12BY

## 《四字經》季节取时语义的地域校准约束：王普《官历刻漏图》、岳台与临安

Status: **SONG OFFICIAL TIMEKEEPING SOURCES CONFIRM SEASONAL DAY-NIGHT / LEAK-CLOCK LENGTH IS GEOGRAPHICALLY CALIBRATED / WANG PU GUANLI KELOU TU SELF-PREFACE SAYS YUETAI IS THE STANDARD BUT NINE-REGION SOLSTICE DAY-NIGHT KE DIFFER AND 24-QI ARROW-CHANGE DATES SHIFT / SONGSHI SAYS LINAN GNOMON PARAMETERS DIFFER FROM YUETAI / DAILY SUNRISE-SUNSET-LEAK FORMULAE EXIST FOR A SPECIFIC STANDARD LOCATION / UNIVERSAL MONTH-ONLY TABLE REJECTED AS HISTORICAL TECHNICAL MODEL / NO DIRECT PROOF SIZIJING USED WANG-PU TABLE / NO SOURCE-SPECIFIC BIRTH-TIME FORMULA RECOVERED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Why this batch follows 12BX

Batch 12BX established that Yongle `旦夕將月建長短而推言` sits naturally in a premodern seasonal-timekeeping semantic field, but did not recover an operational formula. The next question is whether such `長短` could historically be treated as a universal monthly schedule.

Song official timekeeping evidence answers no: the seasonal schedule itself was geographically calibrated.

## 2. Wang Pu's 《官曆刻漏圖》

Wang Yinglin's 《玉海》 records the bibliography and substance of Northern/Southern Song official leak-clock work. For early Shaoxing it states that 太常博士王普 wrote 《官曆刻漏圖》 and that its preface said:

```text
百刻分十二辰，晝夜長短以岳臺為定。
九服之地，冬夏至晝夜刻數或與岳臺不同，
則二十四氣前後易箭之日亦皆少差。
```

Evidence: `https://zh.wikisource.org/wiki/%E7%8E%89%E6%B5%B7_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%8D%B7011`.

The Siku catalogue independently describes the same work as an `永樂大典本`, attributes it to Song Wang Pu, and preserves the same geographical-calibration statement. Evidence: `https://zh.wikisource.org/wiki/%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E7%B8%BD%E7%9B%AE%E6%8F%90%E8%A6%81/%E5%8D%B7107`.

The critical point is operational: even when one starts from the same 24-qi seasonal framework, different regions do not necessarily use the same solstitial day/night ke counts or the same dates for changing seasonal leak-clock arrows.

## 3. Songshi control: Yue-tai versus Lin'an

《宋史》卷48's gnomon discussion explicitly says `地里遠近古今亦不同` and records criticism that Lin'an's gnomon shadow should not simply reuse Yue-tai's parameters. It gives a distinct Lin'an winter-solstice initial-limit proposal rather than the Yue-tai value. Evidence: `https://zh.wikisource.org/wiki/%E5%AE%8B%E5%8F%B2_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%8D%B7048`.

《宋史》 calendrical material also preserves full daily calculation procedures for Yue-tai, including daily gnomon shadow, dawn/dusk, sunrise/sunset and `每日夜半定漏`. Evidence: `https://zh.wikisource.org/wiki/%E5%AE%8B%E5%8F%B2_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%85%A8%E8%A6%BD3`.

This proves that a real technical implementation of seasonal `旦夕/長短` was not merely `month -> fixed clock value`; it depended on a defined observing/calibration location and calendrical parameters.

## 4. Constraint on interpreting the Sizijing clause

If Yongle `旦夕將月建長短而推言` reflects this broad technical tradition, then the minimum historically defensible model would require:

```text
calendrical seasonal position / qi
+ geographical observing location or calibrated regional table
+ day/night or dawn/dusk length model
+ a rule for mapping the uncertain event to that model
```

Only the first and general `長短` idea are textually visible in the Sizijing clause. No Sizijing witness currently supplies the location standard, table, formula, or mapping rule.

Therefore it is forbidden to manufacture a universal `month -> birth-hour correction` table from the one sentence, and equally forbidden to import Yue-tai's Song official formula as though it were the Sizijing author's own procedure.

## 5. Product effect

This batch adds a **future implementation constraint**, not a runtime candidate:

- any future candidate claiming to operationalize the seasonal-timekeeping reading must declare its geographical calibration basis;
- a location-free universal monthly correction is historically under-specified;
- current shared time credentials already make geographic/time-coordinate provenance representable, but that engineering capacity is not evidence for the missing historical rule;
- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT` remains unchanged;
- no Hai-branch mechanical vote, runtime winner, candidate collapse or algorithm reopen.

## 6. Next gate

1. Locate a pre-Ming/Song-Ming fate-calculation source that explicitly applies seasonal day/night or sunrise/sunset tables to recover an uncertain **birth hour**, not merely civil timekeeping.
2. Search surviving/quoted material from 《官曆刻漏圖》 and related `日出入氣刻立成` works for a formula that could explain the Sizijing's compressed wording, while preserving the no-import firewall unless a textual bridge is found.
3. Search additional early Sizijing recensions for the `月建/月運` locus to establish whether the geographical-timekeeping-compatible `月建` reading has broader textual support.

Research record: `docs/research/ZIWEI-SIZIJING-SEASONAL-TIMEKEEPING-GEOGRAPHIC-CALIBRATION-R1.json`.
