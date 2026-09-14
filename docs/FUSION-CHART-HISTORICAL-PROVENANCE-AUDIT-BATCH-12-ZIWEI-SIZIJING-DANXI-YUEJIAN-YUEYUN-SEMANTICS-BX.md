# Fusion Chart Historical Provenance Audit R1 — Batch 12BX

## 《四字經》「旦夕—月建/月運—長短」訓詁：季節漏刻語義域閉合，具體取時算法仍開放

Status: **YONGLE PHYSICAL READING 旦夕將月建長短而推言 / YIMEN-1597 PHYSICAL READING 旦夕時刻且將月運長短定推言之 / 月建~月運 IS A REAL RECENSION VARIANT NOT OCR NOISE / SUI-SONG TIMEKEEPING CONTROLS DIRECTLY LINK QI/DOUJIAN TO SEASONAL DAY-NIGHT AND LEAK-CLOCK LENGTH / CLASSICAL 月運 HAS AN ASTRONOMICAL MOTION SENSE AND MUST NOT BE NORMALIZED TO MODERN MONTHLY-FORTUNE CYCLE / SEASONAL TIMEKEEPING SEMANTIC FIELD STRONGLY SUPPORTED / EXACT NUMERIC BIRTH-TIME RECOVERY ALGORITHM NOT PROVED / NO STEMMATIC WINNER / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Physical recension readings

Batch 12BV directly collated the Yongle-Dadian page without OCR. The relevant ending reads:

`...天陰雨露時難定便是神仙也有差。旦夕將月建長短而推言。萬無一失矣。`

The 1597 Yimen-Guangdu physical page directly reads across columns:

`...天陰雨落難定便是神仙也有差別旦 / 夕時刻且將月運長短定推言之萬無一失矣。`

Thus `月建` versus `月運` is a genuine recension-level glyph/wording difference, not a CText OCR artifact. The two witnesses also differ syntactically (`旦夕將...` versus `旦夕時刻且將...定推言之`).

## 2. Why `長短` belongs to a historical timekeeping semantic field

《隋書》卷19〈漏刻〉 directly states that the hundred刻 are divided between day and night, that winter/summer have different daytime/nighttime allocations, that `漏刻皆隨氣增損`, and that the winter-summer day/night difference totals twenty刻. Its arrows encode 朝/禺/中/晡/夕, night watches and 昏旦. Evidence: `https://zh.wikisource.org/wiki/%E9%9A%8B%E6%9B%B8/%E5%8D%B719`.

Song Zhang Ruyu's 《羣書考索》卷56〈刻漏〉 makes the seasonal bridge more explicit: the leak-clock arrows have winter/summer `長短`; it explains `斗建寅` / `斗建午` with north/south seasonal movement, then says spring causes the arrow to lengthen and autumn causes it to shorten, and finally binds forty-eight arrows to the twenty-four qi. Evidence: `https://zh.wikisource.org/wiki/%E7%BE%A3%E6%9B%B8%E8%80%83%E7%B4%A2_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%8D%B756`.

These controls show that a phrase combining `旦夕`, calendrical/seasonal position, and `長短` can naturally inhabit the technical vocabulary of varying day/night and leak-clock allocation. Therefore the Yongle reading `旦夕將月建長短而推言` has a strong historically grounded **seasonal-timekeeping semantic fit**.

## 3. Why 1597 `月運` cannot be mechanically read as modern fortune-cycle jargon

Western Han 《方言》卷12 glosses motion terminology with `日運為躔，月運為逡` — here `月運` is plainly the moon's movement. Evidence: `https://zh.wikisource.org/wiki/%E6%96%B9%E8%A8%80/%E5%8D%B7%E5%8D%81%E4%BA%8C`.

Tang Dou Shumeng's 《海濤論》 likewise writes `天運晦明，日運寒暑，月運朔望`, again using `月運` in an astronomical/lunar-cycle sense. Evidence: `https://zh.wikisource.org/wiki/%E5%85%A8%E5%94%90%E6%96%87/%E5%8D%B70440`.

Consequently the Yimen physical wording `月運長短` cannot be normalized, without further evidence, to the modern Bazi/Ziwei sense of a monthly fortune period. The local syntax `旦夕時刻且將...長短定推言之`, immediately after a birth-hour uncertainty discussion, also keeps time/calendar semantics active.

This does **not** prove that Yimen `月運` means exactly the same operation as Yongle `月建`. Classical `月運` can denote lunar motion, while `月建` is calendrical/seasonal. The recension may preserve synonymic compression, semantic drift, scribal substitution, or a genuinely different explanatory model. The current evidence does not choose among them.

## 4. Philological adjudication

The strongest admissible conclusion is:

```text
YONGLE 月建長短 = STRONG_SEASONAL_TIMEKEEPING_SEMANTIC_FIT
YIMEN 月運長短 = CLASSICAL_ASTRONOMICAL_SEMANTICS_POSSIBLE; MODERN_MONTHLY_FORTUNE_NORMALIZATION_FORBIDDEN
月建 ↔ 月運 = REAL_RECENSION_VARIANT
EXACT_OPERATIONAL_EQUIVALENCE = UNPROVED
EXACT_NUMERIC_BIRTH_TIME_RECOVERY_ALGORITHM = UNPROVED
STEMMATIC_WINNER = NONE
```

The premodern leak-clock parallels explain *why* seasonal `長短` can matter for `旦夕時刻`; they do not supply the missing source-specific table, birthplace coordinate, instrument procedure, or formula needed to implement a deterministic runtime resolver.

## 5. Effect on HPA-ZDATE-006

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`;
- seasonal timekeeping semantic field for `旦夕/月建/長短`: `strongly supported`;
- Yimen `月運` = modern monthly fortune: `not authorized`;
- exact Yongle/Yimen operational equivalence: `false/unproved`;
- exact numeric current-time recovery mechanism closed: `false`;
- Hai-branch mechanical vote increment: `0`;
- runtime winner selected: `false`;
- candidate collapsed: `false`;
- algorithm reopen authorized: `false`.

Global matrix/accounting counts remain unchanged.

## 6. Next gate

1. Search for an independent early 《四字經》 or close derivative that preserves the complete `旦夕/月建~月運/長短` clause, to determine whether either wording has wider recension support.
2. Search pre-Ming/Song-Ming timekeeping or fate-calculation texts for an explicit operational formula that combines 月建/節氣, day-night length and recovery of an uncertain birth hour.
3. Keep the Fullbook `陰雨必須羅經` line separate: Batch 12BX clarifies the Sizijing semantic field but does not prove that the Fullbook compass sentence uses the same mechanism.

Research record: `docs/research/ZIWEI-SIZIJING-DANXI-YUEJIAN-YUEYUN-SEMANTICS-R1.json`.
