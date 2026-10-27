# Fusion Chart Historical Provenance Audit R1 — Batch 12BW

## 明代陰雨時刻取得與報時制度鏈：漏刻、時牌、鼓更、鐘鼓，及《新法算書》「晨昏陰雨用行漏」

Status: **MING INSTITUTIONAL CURRENT-TIME ACQUISITION / DISSEMINATION CHAIN CLOSED AT TECHNICAL-CONTEXT LEVEL / ZHENGDE AND WANLI HUIDIAN TRANSMISSIONS RECORD 定時刻有漏・換時有牌・報更有鼓・晨昏有鐘鼓 / QINTIANJIAN LEAK-CLOCK PERSONNEL 調壺換牌 AND 報時 / XINFA-SUANSHU EXPLICITLY ASSIGNS DAY TO SUN-DIAL, NIGHT TO STAR-DIAL, MERIDIAN TO CORRECTED COMPASS, AND DAWN-DUSK-CLOUD-RAIN TO CALIBRATED RUNNING CLEPSYDRA / ORDINARY COMPASS-ALONE CLOCK EQUIVALENCE REJECTED / FULLBOOK 羅經 WORDING REMAINS SOURCE-SCOPED AND OPERATIONALLY UNRESOLVED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12AJ established a semantic tension: two directly reviewed Fullbook physical routes agree on `如天氣陰雨之際必須羅經以定真確時候`, whereas contemporary Ming astronomical practice assigns the compass to meridian orientation and a running clepsydra to dawn/dusk/cloud/rain timekeeping. Batch 12BW asks a narrower historical-operations question: what did Ming state timekeeping actually use to maintain and publish current time when celestial observation was unavailable?

The answer is now sufficiently explicit to close the **institutional technical-context layer**, while leaving the Fullbook author's source-scoped use of `羅經` unresolved.

## 2. Zhengde 《明會典》 institutional chain

The Zhengde 《明會典》 tradition, 欽天監 section, records:

```text
凡定時刻有漏
換時有牌
報更有鼓
警晨昏有鐘鼓
...
輪差漏刻博士提調陰陽人如法調壺換牌
```

Electronic witness: `https://ctext.org/wiki.pl?chapter=934432&if=gb`.

This is an operational chain rather than a loose instrument list: the leak establishes time, hour tablets are changed, night watches are announced by drum, dawn/dusk by bell/drum, and designated Qintianjian personnel maintain the water clock and tablets.

## 3. Wanli 《大明會典》 continuity

The Wanli recompilation preserves the same institutional structure:

```text
凡定時刻有漏、換時有牌、報更有鼓、警晨昏有鐘鼓
...
輪差漏刻博士、提調陰陽人、如法調壺換牌
```

It separately describes court ceremony with the `漏刻博士` responsible for timing and a `五官司晨` reporting the hour/holding the time tablet.

Electronic witness: `https://ctext.org/wiki.pl?chapter=242488&if=gb`.

Zhengde and Wanli are treated as transmitted/recompiled institutional controls, not as two statistically independent votes for one physical manuscript.

## 4. Chongzhen technical specification closes the inclement-weather function

Xu Guangqi and the calendar bureau's 《新法算書》 technical memorandum makes the functional division explicit:

```text
日晷以定晝時
星晷以定夜時
正線羅經以定子午
若晨昏陰雨，當造如式行漏 ... 以濟二晷所不及
```

It further says the water clock must be calibrated against celestial time; a normal compass gives direction rather than time and exclusive reliance on a compass can introduce variable time error.

Electronic witness: `https://www.shidianguji.com/zh/book/SK1525/chapter/1lasu1xyun8dl`.

Therefore a historically attested Ming technical current-time chain is:

```text
celestial calibration / true meridian
  -> sun dial by day
  -> star dial by night
  -> calibrated running clepsydra when dawn/dusk/cloud/rain blocks the two dials
  -> institutional time tablet / drum / bell dissemination
```

## 5. Firewall against rewriting the Fullbook sentence

This batch does **not** emend `羅經` to `行漏`, `壺漏`, `鐘`, or any other word. Two Fullbook physical edition routes already agree on `羅經`; there is presently no source-close physical variant showing an alternative glyph.

The admissible conclusion is instead:

```text
MING_INSTITUTIONAL_INCLEMENT_CURRENT_TIME_MECHANISM = CLOSED
FULLBOOK_SOURCE_SCOPED_LUOJING_OPERATIONAL_MECHANISM = UNRESOLVED
LUOJING_AS_STANDALONE_CLOCK = NOT_SUPPORTED_BY_CONTEMPORANEOUS_TECHNICAL_CONTROL
```

This distinction matters: technical context can constrain interpretation, but it cannot silently replace the wording of the Ziwei witness.

## 6. Relation to the newly collated Sizijing line

Batch 12BV physically closed `天陰雨露時難定` in the Yongle-Dadian recension, while the 1597 Yimen witness physically reads `天陰雨落難定`. Both establish the historical problem of inclement-weather birth-time uncertainty. Their following `旦夕/月建~月運/長短` wording may encode a seasonal or calendrical heuristic, but its exact mechanics are not yet proved and Batch 12BW does not use it to substitute for an instrument-based clock.

## 7. Effect on HPA-ZDATE-006

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`;
- Ming institutional inclement-current-time acquisition mechanism closed at technical-context level: `true`;
- Fullbook source-scoped `羅經` operational mechanism closed: `false`;
- ordinary compass-alone clock equivalence: `rejected`;
- local apparent solar time runtime winner: `false`;
- Hai-branch mechanical vote increment: `0`;
- candidate collapsed: `false`;
- algorithm reopen authorized: `false`.

Global accounting remains `198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families`; chart algorithm defect/reopen/collapse remain `0/0/0`.

## 8. Next gate

1. Search Fullbook-adjacent Ming/Qing Ziwei, fate-calculation, compass and calendrical witnesses for a source-close explanation of why `羅經` is invoked in cloudy/rainy birth-time determination.
2. Continue philological work on the `旦夕將月建長短` versus `旦夕時刻且將月運長短` recension difference; do not call it a day-length algorithm until an operational parallel is found.
3. Preserve the institutional clock chain as context only until a documented bridge connects it to the Fullbook practice statement.

Research record: `docs/research/ZIWEI-MING-INSTITUTIONAL-INCLEMENT-TIMEKEEPING-CHAIN-R1.json`.
