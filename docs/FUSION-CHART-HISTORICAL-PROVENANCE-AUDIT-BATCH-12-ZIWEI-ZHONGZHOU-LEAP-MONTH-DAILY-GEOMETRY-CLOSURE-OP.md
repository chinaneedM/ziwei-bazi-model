# Fusion Chart Historical Provenance Audit R1 — Batch 12OP

## Zhongzhou leap-month day-one / daily geometry closure

Status: **SOURCE-SCOPED GEOMETRY CLOSED / SCHOOL-SPECIFIC CANDIDATE PRODUCTIZED / NO PRODUCTION WINNER CHANGE**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
TRANSMISSION_IMPACT=NONE
```

## 1. Question

`HPA-ZT-015` remained `MISSING_FROM_PRODUCT` after Batch 12NQ because the live Matrix said the Zhongzhou half-split candidate did not close leap-month day-one flow-day origin or complete daily active-palace geometry.

Batch 12OP re-collates the worked leap-month example together with the immediately following general flow-day rule.

## 2. Source boundary

The source is the already registered modern Zhongzhou witness `EXT-WANGTINGZHI-ZHONGZHOU-CHUJI`, bibliographically cross-checked by `EXT-XINGQIAO-WANGTINGZHI-ZHONGZHOU-CHUJI`. S10 is an internal research collation, not infallible authority. Relevant refs are P-0280..P-0283 and P-0287. No Ming/Qing backdating is authorized.

## 3. Philological closure

The worked example closes first-half origin: normal-month counting continues past its last day into leap day 1, so the preceding regular-month length 29/30 is a deterministic input. For the lower half, the source changes the basis at leap day 16 to the following regular month's monthly palace. The general rule makes that monthly palace the day-1 basis and counts to the requested day; the basis changes but day 16 is not renumbered.

```text
days 1..15:
  leap_day_1 = previous_month_palace + previous_regular_month_day_count
  day_d       = leap_day_1 + (d - 1)

days 16..end:
  basis       = following_month_palace as ordinary day-1 basis
  day_d       = basis + (d - 1)

half_split_basis_switch=true
half_split_reset=false
direction=FORWARD
```

All additions are modulo the twelve-palace ring.

## 4. Scope firewall

This is a modern Zhongzhou flow-month/day method. Natal leap-month doctrines in other sources are not silently equated with it. Future alternative flow-time methods require separate source-bound candidate identities. No universal winner is selected.

## 5. Productization

```text
API=ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-API-R1@1.2.0
REGISTRY=ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-REGISTRY-R1@1.1.0
RUNTIME=ZIWEI-TEMPORAL-HISTORICAL-CANDIDATE-RUNTIME-R1@1.1.0
SELECTION=PRESERVED_NOT_SELECTED
```

Shared projection obtains preceding regular-month length from the actual calendar boundary and emits backend-computed daily candidate geometry. Workbench displays returned fields only. Ordinary production month/day fields remain fail-closed.

## 6. Matrix repair

`PROV-DEFECT-044` repairs forward-only the stale claim that day-one/daily geometry remained source-unclosed. `HPA-ZT-015` changes `MISSING_FROM_PRODUCT -> SUPPORTED_BUT_SCHOOL_SPECIFIC`; `HPA-ZTEMP-006` remains school-specific with updated complete geometry.

## 7. Accounting

```text
TOTAL_MATRIX_ROWS=222
AUDITED_ROWS=222
HISTORICALLY_SUPPORTED=104
SUPPORTED_BUT_SCHOOL_SPECIFIC=25
MISSING_FROM_PRODUCT=4
IDENTIFIED_MISSING_CANDIDATE_FAMILY_COUNT=14
HISTORICAL_CANDIDATE_EXTENSION_COUNT=14
HISTORICAL_CANDIDATE_REGISTRY_COUNT=5
HISTORICAL_CANDIDATE_RUNTIME_RESOLVER_COUNT=5
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=44
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=44
```

No new candidate family is counted; the batch extends an already registered candidate.

## 8. Transmission genealogy

`transmission_impact=NONE`: this closes mechanics inside an existing modern Zhongzhou witness and adds no ancestry edge.

## 9. Next

Batch 12OQ will re-rank the four remaining `MISSING_FROM_PRODUCT` rows (`HPA-ZDATE-006`, `HPA-DAYUN-CAL-002`, `HPA-DAYUN-CAL-003`, `HPA-DAYUN-CAL-004`) by evidence-acquisition readiness and dependency depth before resuming the highest-value blocked route.
