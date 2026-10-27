# Fusion Chart Historical Provenance Audit R1 — Batch 12PC

## Ming Datong Runyu 進退 / 定朔無中氣 final placement

Status: **Q=2 BOUNDARY 10/10 SOURCE CONTROLLED / 5 RETREAT + 5 STAY / MD-G09 CLOSED SOURCE-SCOPED / HISTORICAL RUNTIME STILL FAIL-CLOSED**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
HPA_DAYUN_CAL_002=MISSING_FROM_PRODUCT
MD_G09_MULTI_YEAR_LEAP_GENERALIZATION=CLOSED_SOURCE_SCOPED
MING_DATONG_GENERAL_EXECUTABLE_ADAPTER=CERTIFICATION_BLOCKED
RUNTIME_SELECTION_AUTHORIZED=NO
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

12PB correctly closed all fifteen q=0/1 pre-year controls but exposed a remaining boundary: the received placement quotient is provisional because the same received rule says **閏有進退，仍以定朔無中氣為定**. The complete q=2 census has ten threshold labels.

The ten controls split exactly in half:

| threshold label | final civil/regnal owner | leap month | disposition |
|---:|---|---:|---|
| 1374 | 1373 洪武六年 | 11 | retreat |
| 1393 | 1392 洪武二十五年 | 12 | retreat |
| 1412 | 1411 永樂九年 | 12 | retreat |
| 1431 | 1430 宣德五年 | 12 | retreat |
| 1450 | 1450 景泰元年 | 1 | stay |
| 1469 | 1469 成化五年 | 2 | stay |
| 1488 | 1488 弘治元年 | 1 | stay |
| 1507 | 1507 正德二年 | 1 | stay |
| 1526 | 1525 嘉靖四年 | 12 | retreat |
| 1545 | 1545 嘉靖二十四年 | 1 | stay |

This directly disproves both shortcuts “q=2 always belongs to the preceding year” and “q=2 always stays in the label year”. Final placement must use the old-Datong no-Zhongqi civil structure.

The 12PC harness validates ten boundary controls × four precision profiles = **40 profile-controls**, then reruns 1368–1644. Expected closure conditions are 102 Runyu threshold labels, 102 unique final owners, zero owner ambiguity, zero profile-structural divergence and zero final-owner/existence mismatch through 1368–1643.

With 12OY/12OZ/12PA/12PB/12PC combined, `MD-G09-MULTI-YEAR-LEAP-GENERALIZATION` closes **source-scoped**. This does not authorize a historical runtime: G03, G05, G07 and G08 remain open, while G10/G11 remain dependency-blocked. `HPA-DAYUN-CAL-002` therefore remains `MISSING_FROM_PRODUCT`.

No production algorithm, default, candidate registry or runtime resolver changes. The next batch is **12PD — G03 qishuo geographic reference**, using the already re-acquired complete Kyujanggak `GK12437_00` physical method block.

Research record: `docs/research/MING-DATONG-RUNYU-JINTUI-FINAL-PLACEMENT-R1.json`. Oracle: `docs/research/MING-DATONG-RUNYU-JINTUI-BOUNDARY-ORACLE-R1.json`.
