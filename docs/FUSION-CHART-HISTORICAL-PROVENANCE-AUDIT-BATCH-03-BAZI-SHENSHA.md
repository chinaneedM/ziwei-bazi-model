# Historical Provenance Audit R1 — Batch 03: BaZi ShenSha

## State

```text
BATCH_ID=BATCH-03-BAZI-SHENSHA
CUMULATIVE_AUDITED_ROW_COUNT=40
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=3
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=3
HISTORICAL_CANDIDATE_EXTENSION_COUNT=1
IDENTIFIED_MISSING_CANDIDATE_FAMILY_COUNT=1
ALGORITHM_REOPEN_COUNT=0
```

## Audit principle

ShenSha is not audited only as a name-to-table lookup. Each rule is split into:

1. trigger table;
2. anchor basis (year/day/month/hour stem or branch);
3. target scope (day-only vs all pillars);
4. extra qualification conditions;
5. source family / school;
6. whether a result is a base identity or a fully qualified traditional construction.

## Key findings

### Tianyi

The received Yuanhai five-group table is valid, but Ming `三命通会` preserves additional Tianyi formulations including yin/yang and day/night style derivations. The current simple table is therefore not declared universal. These additional families are recorded as a missing formalized candidate family; they are not half-implemented.

### Tiande

Yuanhai's verse/commentary permits the value to appear across year/month/day/hour contexts, while Ming `三命通会` uses a day-position restriction. R1 now emits two explicit candidates:

- Yuanhai all-pillars scope;
- Sanming day-only scope.

No winner is selected.

### Yuancheng

The runtime formula exactly replays the source example: day-stem Twelve-Growth start at the hour branch plus Liuhe with the day-branch Yima. Its old provenance dependency pointed to `YHZP-CH-016`; this is the same stale Twelve-Growth chapter error found in Batch 02. `PROV-DEFECT-003` repairs it to `YHZP-CH-015`.

### Sanqi

The product intentionally emits only the ordered three-stem **base sequence** and marks auxiliary conditions as unarbitrated. This is correct: the source also requires additional qualification conditions. The audit therefore does not falsely upgrade a base sequence to a complete Sanqi qualification.

### Yangren / Feiren

The corpus contains more than one blade tradition. The current five-yang-stem Yangren family remains school-scoped, while Feiren is independently preserved with explicit ten-stem source enumeration. These are not silently merged.

## Conclusion

The ShenSha audit validates the architecture of preserving source-scoped candidates and qualification states. The first product change produced by historical research is additive, not destructive: a historically attested Tiande candidate was added without changing any existing winner/default.
