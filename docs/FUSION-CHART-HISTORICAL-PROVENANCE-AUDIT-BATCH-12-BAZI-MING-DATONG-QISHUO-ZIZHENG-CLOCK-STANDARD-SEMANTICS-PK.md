# Fusion Chart Historical Provenance Audit R1 — Batch 12PK

## Qishuo 子正 / clock-standard semantics

Status: **UNIFORM INTERNAL 100-KE CLOCK CLOSED / APPARENT-vs-MEAN-vs-CLEPSYDRA ABSOLUTE REALIZATION UNRESOLVED / MD-G03 OPEN**

12PJ established that modern ephemeris precision is sufficient but that the historical time-standard mapping is not. 12PK audits the historical formulas themselves.

### 1. What Shoushi directly says

《元史》卷54《授時曆經上》 gives 日周=10000 and converts a requested fractional remainder into clock labels by multiplying by 12, reducing by the shichen law, collecting the remainder into ke, and **命子正算外**; a half-shichen offset is labeled from 子初.

This closes a uniform internal computational coordinate: 10000 day units → 12 shichen / 100 ke, with 子正 as the arithmetic clock origin.

The reviewed qishuo/falian rule does not state an equation-of-time correction, does not name apparent solar time or mean solar time, does not name a longitude/place, and does not instruct the operator to read a physical water clock at the qishuo conversion step.

### 2. Shoushi has a separate locality-sensitive clock module

《元史》卷55《授時曆經下》 explicitly fixes the Dadu polar altitude and Dadu day/night fractions, then says the nine regions' day/night and culminational-star rates are to be computed from local polar altitude. Its `求九服所在漏刻` even allows each locality to establish the local solstitial difference by instrument observation or water-clock measurement.

This proves Shoushi has explicit locality-sensitive daylight/clepsydra machinery. It does not prove that the qishuo small remainder inherits Dadu as an absolute longitude.

### 3. Late-Ming authorial control

朱載堉《黃鍾曆議》 explicitly says Shoushi's rising/setting and seasonal day/night behavior used Dadu gnomon/clepsydra parameters, while early Ming Datong changed sunrise/sunset and day-length behavior to Nanjing parameters. He criticizes the resulting mixture because eclipse east/west and related procedures retained Yuan methods.

This strongly supports a module-specific geography model. It still does not equate the Datong 定朔 small remainder with either Dadu or Nanjing apparent/mean solar time.

### 4. Cross-calendar positive control

《元史》卷56 is **庚午元曆**, not 授時曆. Its `求朔弦望中日` explicitly uses 尋斯干城 as the reference and computes a `里差` from east/west distance to add/subtract from the mean new-moon/quarter/full-moon remainder.

This is a useful positive control: historical calendrical methods can explicitly encode a geographic reference and longitude-like correction at the new-moon step when intended. The rule must not be imported into Shoushi/Datong.

### 5. Adjudication

Closed: qishuo 子正/刻 is a uniform internal 100-ke computational clock coordinate.

Not closed: whether that internal coordinate is physically realized as local apparent solar time, local mean solar time, calibrated clepsydra time, or another bureau convention; nor the absolute longitude to which it is attached.

Therefore modern ephemeris longitude fitting remains unauthorized. MD-G03 remains OPEN_BLOCKING_GENERAL_ADAPTER; HPA-DAYUN-CAL-002 remains MISSING_FROM_PRODUCT.

Next: **12PL — Ming Qintianjian institutional almanac clock-standard / capital-binding audit**.

Research record: docs/research/MING-DATONG-QISHUO-ZIZHENG-CLOCK-STANDARD-SEMANTICS-R1.json
