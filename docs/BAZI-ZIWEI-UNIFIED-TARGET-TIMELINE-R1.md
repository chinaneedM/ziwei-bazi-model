# Bazi + Ziwei Unified Target Timeline R1

## Scope

This release links deterministic temporal coordinates to one explicit target-time credential. It does not unify the two traditions' calendar rules and does not generate interpretation or prediction.

The Bazi application-flow candidate now carries an auditable ordered timeline:

```text
Natal -> Dayun -> Xiaoyun candidates -> Annual -> Monthly -> Daily -> Hourly
```

The existing Natal, Dayun, Annual/Monthly Flow, and Daily/Hourly sidecar objects remain authoritative. The timeline repeats those released facts for composition and commits them to the application-flow view hash; it does not mint a second sexagenary calculation path.

## Xiaoyun linkage boundary

Both released Xiaoyun methods remain separate candidates. For target-time display, the application layer uses

```text
target local civil year - birth local civil year + 1
```

as an explicit engineering nominal-age coordinate. This is not a classical age-boundary ruling. The output therefore records `classical_age_boundary_status=NOT_ARBITRATED` and keeps selection status `UNRESOLVED_CLASSICAL_METHOD_ALTERNATIVES`. A frame outside the materialized Xiaoyun range is reported rather than regenerated or guessed.

## Independent Ziwei projection

The same target-coordinate candidate can be projected into the existing Ziwei selector domain, but Ziwei recomputes its own effective lunar date with its own:

- calendar-date policy;
- day-boundary policy;
- life/body leap-month policy;
- target local apparent solar time.

The projection preserves the existing civil-year annual selector behavior and adds the regular lunar-month frame identity, Ganzhi, and active address. For a regular month it also emits a read-only daily frame: the flow-month life address is lunar day one and the target lunar day is counted forward. Its day Ganzhi is calculated from the effective Gregorian date selected by the Ziwei profile, not copied from the Bazi daily frame. The day stem activates four immutable physical-star transformation facts through the calculation profile's explicitly bound S08 rule set. The output records the selected rule-set identity and the S01 transformation-variant conflict reference; it does not silently treat that profile choice as a universal table. A regular lunar month can be explicitly applied to the existing Ziwei interaction refresh path; the daily fact is displayed but is not written into a selector that the current interaction UI does not materialize.

S10's general rule text does not provide a runtime-authoritative flow-hour active-address rule. The only available Five-Rats description is case-method evidence. R1 therefore preserves two named hour-coordinate candidates, `ZHONGZHOU_LUOYANG_MEAN_SOLAR_TIME` (fixed at S01's 112°26′ reference longitude) and `LOCAL_APPARENT_SOLAR_TIME`, with their own clocks, effective dates, day/hour Ganzhi, and S01 conflict references. Each candidate carries its own case-scoped S08 four-transformation activation facts, because S10's example explicitly uses the hour stem for a transformation; those facts remain inside the unselected candidate. Both remain `ACTIVE_ADDRESS_NOT_GENERATED_CASE_METHOD_ONLY`; neither is silently selected or promoted to a complete hourly chart.

If the effective date is in a leap month, R1 returns `LEAP_MONTH_UNRESOLVED_NO_FRAME` and `PARENT_LEAP_MONTH_UNRESOLVED_NO_FRAME` for the daily layer. It does not silently map the leap month to a regular-month or daily frame and therefore emits no daily transformation activations; the browser leaves the regular lunar-month selector empty while still allowing the annual, Daxian, and minor-limit coordinates to be applied.

## Candidate and lineage preservation

Civil folds and uncertainty samples stay distinct throughout both projections. Every Bazi timeline is bound to its target-coordinate candidate ID. Every Ziwei projection candidate records the same upstream target candidate ID plus its Ziwei application/temporal hashes. Browser calculation never auto-applies a candidate, and multiple candidates require an explicit selection.

The link is therefore a shared target identity, not a shared calendar verdict:

- Bazi year/month/day/hour boundaries remain governed by the Bazi calculation profile;
- Ziwei lunar date and late-Zi handling remain governed by the Ziwei calculation profile;
- neither side overwrites the other's target facts or policy lineage.

## Integrity and schemas

The application-flow replay validates all seven Bazi layers, Xiaoyun candidate preservation, and exact equality with the upstream Dayun/Flow/Daily-Hourly facts. The shared Ziwei projection replay independently reconstructs its effective lunar date, regular-month and daily frames, and both time-standard hour candidates (or the unresolved leap-month parent state).

Machine-readable contracts:

- `schemas/bazi-application-flow-integration-r1.schema.json`
- `schemas/shared-ziwei-selector-projection-r1.schema.json`

## Non-goals

R1 does not decide a Xiaoyun school, decide leap-month Ziwei flow doctrine, promote case-only flow-hour evidence into a global active-address rule, merge Bazi and Ziwei day boundaries, calculate strength/pattern/useful-god/favorable elements, activate ShenSha meanings, or produce event judgments, interpretations, training data, or predictions.
