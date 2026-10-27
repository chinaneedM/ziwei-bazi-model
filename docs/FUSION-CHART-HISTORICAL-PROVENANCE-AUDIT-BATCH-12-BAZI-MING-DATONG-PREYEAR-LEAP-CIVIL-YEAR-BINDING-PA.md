# Fusion Chart Historical Provenance Audit R1 — Batch 12PA

## Ming Datong pre-year leap / civil-year binding

Status: **FOUR 12OZ TENSIONS RESOLVED / PRE-YEAR CIVIL OWNERSHIP BRANCH IDENTIFIED / G09 STILL OPEN**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
HPA_DAYUN_CAL_002=MISSING_FROM_PRODUCT
PRIMARY_1569_RUNYU_THRESHOLD=RECOLLATED_SOURCE_SCOPED
MINGSHI_PREYEAR_BRANCH=BOUND_AS_RECEIVED_RULE
12OZ_TENSION_LABELS_1384_1385_1479_1480=RESOLVED
FULL_MING_PREYEAR_FORMULA_CANDIDATES=15
G09_STATUS=OPEN_BLOCKING_GENERAL_ADAPTER
RUNTIME_SELECTION_AUTHORIZED=NO
```

Research record: `docs/research/MING-DATONG-PREYEAR-LEAP-CIVIL-YEAR-BINDING-R1.json`  
Research-only census: `scripts/research_ming_datong_preyear_leap_civil_year_binding_r1.py`

The direct Zhou Xiang 1569 facsimile re-closes `推閏餘分法`: form the Tianzheng `閏餘`, compare it with `閏限=186552.09`, and recur to the next year with `通閏=108753.84`. This primary page does not itself bind the numeric threshold label to civil/regnal-year ownership.

The missing bridge is preserved in the Qing-compiled `明史·曆志` step `推閏在何月`. For an already-intercalary year it computes `朔策-閏餘`, divides by `月閏=9062.82`, and says cases not reaching one month-run **or reaching only one month-run** are `閏在年前`. 12PA uses that only as a received placement bridge, never as 1569 direct wording.

For the two paired 12OZ tensions:

- 1385: `閏餘=290824.02`, residual `4481.91`, quotient 0 → leap belongs before that threshold label. The Ming official veritable-record tradition records `洪武十七年閏十月乙未朔`, i.e. civil 1384 leap 10.
- 1480: `閏餘=286731.27`, residual `8574.66`, quotient 0 → leap belongs before that threshold label. The Ming official veritable-record tradition records `成化十五年閏十月癸丑朔`, i.e. civil 1479 leap 10.

Therefore 1384/1385 and 1479/1480 are not D1-precision failures and do not invalidate the primary runyu threshold. They expose a missing civil-year ownership branch in the research generator.

A formula-level 1368–1644 census of `閏餘>=閏限 AND floor((朔策-閏餘)/月閏)<=1` yields 15 threshold labels: 1385, 1404, 1423, 1442, 1461, 1480, 1499, 1518, 1537, 1556, 1575, 1594, 1613, 1632, 1643. Only two pairs are directly controlled in this batch. The fixed shortcut “sequence k=2 is always civil month 1” is therefore rejected as a universal civil-year anchor.

G09 remains `OPEN_BLOCKING_GENERAL_ADAPTER`; runtime remains fail-closed. Matrix stays 222/222, MISSING_FROM_PRODUCT=4, provenance defects 45/45 repaired, with no algorithm reopen or candidate collapse.

Next: **12PB** validates all 15 pre-year candidates against Ming civil/regnal chronology or direct almanac controls, replaces fixed-k=2 civil-year extraction with explicit ownership logic, and reruns 1368–1644 before any G09 closure.

