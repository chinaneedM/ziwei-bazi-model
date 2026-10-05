# Historical Provenance Audit — Batch 12OL

## Remaining product-gap reprioritization

After 12OK, six Matrix rows remain `MISSING_FROM_PRODUCT`.

The ranking is based on source closure, deterministic implementation readiness, ambiguity-preserving representation and dependency depth.

1. **HPA-ZIWEI-018 — 1581 Jielan historical dignity table**
2. **HPA-ZT-015 — leap-month temporal frames**
3. **HPA-DAYUN-CAL-003 — later/Qianli Jiaoyun calendarization**
4. **HPA-ZDATE-006 — Nanyangtang ten-ke Zi/Hai natal-hour candidate**
5. **HPA-DAYUN-CAL-002 — classical lunisolar first Jiaoyun adapter**
6. **HPA-DAYUN-CAL-004 — ten-year historical recurrence**, dependent on a closed first-handover adapter.

## Why HPA-ZIWEI-018 is first

The Jielan CH69/CH70 source family is already registered and the existing resolver already exposes `SOURCE_TABLE_PRESENT_NORMALIZATION_PENDING`.

The key improvement is representational rather than interpretive: CH70 itself explicitly glosses several historical lexemes (for example 旺/利/得地 versus 庙, 平 versus 闲, 嗔 versus 陷). That permits a source-faithful candidate to preserve:

- exact source lexeme;
- exact source phrase/locator;
- source-level gloss class where the text explicitly supplies one;
- unresolved status where it does not.

No historical term needs to be forced into the production R4 seven-grade registry.

## Next

**12OM — build the 1581 Jielan dignity raw-lexeme / explicit-gloss candidate.**

Production `OPERATIONAL-ZIWEI-DIGNITY-R4@4.0.0` remains completely separate and unchanged.
