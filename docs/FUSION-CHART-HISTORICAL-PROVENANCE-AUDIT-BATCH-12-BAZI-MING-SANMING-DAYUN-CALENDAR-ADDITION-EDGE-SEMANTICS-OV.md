# Fusion Chart Historical Provenance Audit R1 — Batch 12OV

## Ming / Sanming Dayun calendar-addition edge semantics

Status: **WORKED-EXAMPLE SEMANTICS PARTIALLY CLOSED / INVALID-DATE AND DUPLICATE-LEAP IDENTITY STILL OPEN / RUNTIME FAIL-CLOSED**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
HPA_DAYUN_CAL_002=MISSING_FROM_PRODUCT
SMALL_MONTH_DEFICIT_CORRECTION=CLOSED_RECEIVED_TEXT_WORKED_EXAMPLE
INTERCALARY_EXTRA_MONTH_AGGREGATE_CORRECTION=CLOSED_RECEIVED_TEXT_WORKED_EXAMPLE
INVALID_TARGET_DAY_POLICY=UNRESOLVED
DUPLICATE_REGULAR_INTERCALARY_MONTH_IDENTITY=UNRESOLVED
TEN_ANNIVERSARY_STATEMENT=CLOSED_TEXTUAL_EXECUTION_DEPENDENCY_BLOCKED
GENERAL_HISTORICAL_CALENDAR_RUNTIME=FAIL_CLOSED
```

Research record: `docs/research/MING-SANMING-DAYUN-CALENDAR-ADDITION-EDGE-SEMANTICS-R1.json`.

## 1. Question

12OU deliberately split the Ming Datong adapter into independent certification gates. 12OV asks a narrower question: what does the classical `三命通會·論大運` worked example actually tell us about calendar addition, and where does the text stop?

The answer is narrower than “use the lunar calendar”, but also more executable than a vague reminder to consider small and leap months.

## 2. Explicit worked-example operations

The received text gives a concrete one-year counting example.

It first takes the same lunar month/day/shichen in the next year as a nominal one-year coordinate. It then says that six small months require advancing six days. This closes the worked-example arithmetic that a small month contributes a one-day deficit relative to nominal 30-day-month counting.

The same example then observes that the year contains an intercalary fourth month, hence one extra actual month. It moves the corrected coordinate back one month so that only twelve elapsed months are counted. This closes **aggregate intercalary insertion counting** in the worked example.

Finally, the passage states that after this first handover coordinate the next luck frame changes after ten full anniversaries. This closes the textual recurrence structure, not a universal `ADD_CALENDAR_YEARS` algorithm.

## 3. What the passage does not say

The reviewed passage does not state what to do if a carried target day is 30 but the target month has only 29 days. Therefore none of the following may be invented:

- clamp to day 29;
- roll to the next month;
- roll backward;
- inherit the invalid-date behavior of a modern Chinese-calendar package;
- use Gregorian anniversary semantics.

The passage also does not define a typed identity rule for a month number that appears twice as regular and intercalary. Its leap-fourth-month example proves that the inserted leap month counts as an extra actual elapsed month, but the handover target itself is not “fourth month”, so it does not answer whether a duplicated target should mean regular fourth month or intercalary fourth month.

The same problem remains for a birth or first-handover anchor that itself lies inside an intercalary month.

## 4. Witness discipline

The registered `EXT-CTEXT-SANMING-V2-DAYUN` rule witness is sufficient to preserve the explicit action logic already recognized by the Matrix. A public Siku transcription and the downstream `古今圖書集成` reuse show the same fingerprint, but they are not independent Ming votes.

A 1926 physical printed scan is useful only as a later transmission control.

Two Wanli physical holdings are already registered in the repository, including the 1578 Taiwan NCL object and a separate China NLC Wanli juan-2 holding. 12OV does **not** claim that the `論大運` target page was directly collated from those physical objects. Their identification is retained as a future evidence-strengthening path; it is not used to fake primary-page closure.

## 5. Effect on 12OU gates

No 12OU gate changes status.

- **G07 invalid target date:** remains `OPEN_BLOCKING_GENERAL_ADAPTER`.
- **G08 intercalary identity/traversal:** remains `OPEN_BLOCKING_GENERAL_ADAPTER`; aggregate insertion is closed, typed duplicate identity is not.
- **G10 ten-year recurrence:** remains `DEPENDENCY_BLOCKED`; the textual ten-anniversary statement is closed, execution is not.

Therefore the required adapter result remains:

`UNRESOLVED_NO_CERTIFIED_HISTORICAL_CALENDAR_ADAPTER`.

## 6. Accounting / invariants

No Matrix status change, no runtime profile, no default change, no candidate collapse, no algorithm reopen.

- Matrix: **222 / 222 audited**
- current `MISSING_FROM_PRODUCT`: **4**
- provenance defects: **45 / 45 repaired**
- historical candidate extensions: **14**
- candidate registries/runtime resolvers: **5 / 5**
- chart algorithm defects: **0**

## 7. Next batch

**12OW — dynamic D1 precision generalization.**

Seek additional Ming authorial or official arithmetic controls beyond the single 1596 Datong worked example, with special attention to boundary-sensitive cases. A local printed precision pattern must not become a universal runtime rule without additional source closure.

