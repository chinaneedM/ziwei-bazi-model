# Fusion Chart Historical Provenance Audit R1 — Batch 12PB

## Ming Datong pre-year leap civil-year global validation

Status: **15/15 q=0/1 PRE-YEAR CONTROLS BOUND / FIXED-k=2 SHORTCUT REMOVED / FULL-ERA 進退 RESIDUAL EXPOSED / MD-G09 REMAINS OPEN / RUNTIME FAIL-CLOSED**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
HPA_DAYUN_CAL_002=MISSING_FROM_PRODUCT
MD_G09_MULTI_YEAR_LEAP_GENERALIZATION=OPEN_BLOCKING_GENERAL_ADAPTER
MING_DATONG_GENERAL_EXECUTABLE_ADAPTER=CERTIFICATION_BLOCKED
RUNTIME_SELECTION_AUTHORIZED=NO
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

## 1. Scope

12PA identified fifteen Ming-era Runyu threshold labels whose received `推閏在何月` quotient takes the `閏在年前` branch. 12PB binds every label to the preceding civil/regnal year, checks the observed intercalary month, and removes the research generator's fixed `k=2` civil-year start shortcut. Production Bazi/Ziwei algorithms are unchanged.

## 2. Explicit civil-year ownership

The research month generator now defines a civil year as the first **regular month 1** through the interval immediately before the next **regular month 1**. This preserves late intercalations such as leap month 12 and prevents pre-year intercalation from being misread through a fixed sequence index.

## 3. Fifteen chronology controls

| threshold label | civil/regnal year | leap month |
|---:|---|---:|
| 1385 | 1384 洪武十七年 | 10 |
| 1404 | 1403 永樂元年 | 11 |
| 1423 | 1422 永樂二十年 | 12 |
| 1442 | 1441 正統六年 | 11 |
| 1461 | 1460 天順四年 | 11 |
| 1480 | 1479 成化十五年 | 10 |
| 1499 | 1498 弘治十一年 | 11 |
| 1518 | 1517 正德十二年 | 12 |
| 1537 | 1536 嘉靖十五年 | 12 |
| 1556 | 1555 嘉靖三十四年 | 11 |
| 1575 | 1574 萬曆二年 | 12 |
| 1594 | 1593 萬曆二十一年 | 11 |
| 1613 | 1612 萬曆四十年 | 11 |
| 1632 | 1631 崇禎四年 | 11 |
| 1643 | 1642 崇禎十五年 | 11 |

Digital transcriptions are used as textual chronology controls/locators, not physical-glyph authority.

## 4. Machine closure

The 12PB harness enforces 15 candidate years × 4 precision profiles = **60 profile-year controls**, verifies preceding-civil-year assignment, reruns 1368–1644 for profile-structural invariance, and checks formula ownership against generated civil-year leap existence through 1368–1643. The 1644 structure is still generated/profile-compared, but the owner comparison does not import a post-Ming 1645 threshold label across the regime boundary.

## 5. Full-era residual and G09 firewall

The 15 q=0/1 pre-year controls close exactly as intended, but the full 1368–1644 rerun exposes **10 remaining mismatches** between a provisional received quotient-based owner mapping and the generated no-Zhongqi civil-year structure. The first is civil 1373, generated as leap 11, while the provisional q=0/1 owner mapping assigns no threshold label to that civil year.

This is not a D1 profile instability: all four precision profiles remain structurally aligned. It is a placement/ownership scope error in treating the received quotient as final. The received text itself states that leap placement may advance or retreat and is finally determined by **定朔無中氣**. Therefore `MD-G09-MULTI-YEAR-LEAP-GENERALIZATION` remains **OPEN_BLOCKING_GENERAL_ADAPTER**.

The next batch must bind the remaining 進退 boundary against Ming chronology before G09 can be reconsidered. G03, G05, G07 and G08 also remain open; G10/G11 remain dependency-blocked. `FailClosedHistoricalCalendarAdapter` remains mandatory.

## 6. Transmission impact

The fifteen controls strengthen compatibility among the 1569 threshold mechanism, the received pre-year placement branch and Ming chronology. They do not establish direct copying or a single textual lineage; no genealogy edge is added.

## 7. Accounting and next

Matrix remains **222/222 audited / 4 MISSING_FROM_PRODUCT**; provenance defects **45/45 repaired**; candidate extensions **14**; registries/runtime resolvers **5/5**; algorithm defects/reopens/candidate collapses **0**.

Next: **12PC — MD-G09 Runyu 進退 boundary closure**. Bind the 10 residual provisional-owner mismatches against Ming chronology and the received final no-Zhongqi rule. The already-acquired G03 physical qishuo evidence is retained for the following batch.

Research: `docs/research/MING-DATONG-PREYEAR-LEAP-CIVIL-YEAR-GLOBAL-VALIDATION-R1.json`.
