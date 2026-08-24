# Bazi + Ziwei Unified Target Timeline R1

## Scope

This release links deterministic temporal coordinates to one explicit target-time credential. It does not unify the two traditions' calendar rules and does not generate interpretation or prediction.

The Bazi application-flow candidate now carries an auditable ordered timeline:

```text
Natal -> Dayun -> Xiaoyun candidates -> Annual -> Monthly -> Daily -> Hourly
```

The existing Natal, Dayun, Annual/Monthly Flow, and Daily/Hourly sidecar objects remain authoritative. The timeline repeats those released facts for composition and commits them to the application-flow view hash; it does not mint a second sexagenary calculation path.

## Bazi temporal classical annotations

Every resolved Dayun, Annual, Monthly, Daily, and Hourly Ganzhi now has a
read-only annotation projection relative to the immutable Natal day master.
Each Xiaoyun method receives its own annotation and remains a separate
candidate. A pre-Dayun interval reports `PRE_DAYUN_NO_GANZHI_ANNOTATION`
instead of inventing a Dayun pillar.

Each projection contains visible-stem Ten God, ordered hidden stems and their
Ten Gods, Nayin identity, Xunkong, day-master Twelve Growth, and self Twelve
Growth. These facts reuse the released registries and retain rule/profile IDs,
stable sources, semantic scope, per-layer FactHash/ComputationHash, and an
aggregate projection hash. They do not modify the upstream temporal frames.

Structural integrity reconstructs the entire annotation projection from the
timeline Ganzhi and recorded Natal day master. Full application replay binds
that day master back to the Natal candidate, so locally rehashing a changed
hidden stem, Ten God, Nayin, Xunkong, or growth phase cannot conceal tampering.
See `docs/BAZI-TEMPORAL-CLASSICAL-ANNOTATIONS-R1.md`.

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

The projection preserves the existing civil-year annual selector behavior and adds the regular lunar-month frame identity, Ganzhi, and active address. It also carries immutable Daxian, Annual, and regular-Month layer projections instead of reducing those layers to selector IDs. Every layer projection records its own source layer, source stem, frame and parent-frame identity, temporal rule-set and algorithm identity, stable frame sources, four transformation activations, three independent 禄存／擎羊／陀罗 activations, two independent 流文昌／流文曲 activations, and a non-selected 流魁／流钺 method-candidate set. The strict S01 table and the Wenmo compatibility method keep separate method IDs, activation IDs, source chains, fact hashes, and computation hashes even when their non-辛 placements coincide. Equal-named transformations or auxiliaries in different layers retain different activation IDs and are never merged. The integrity path reconstructs every layer projection from the released source frame and compares every field, so recomputing local hashes cannot conceal a changed parent, stem, rule identity, source chain, transformation, auxiliary, or candidate method.

For a regular month the projection also emits a read-only daily frame: the flow-month life address is lunar day one and the target lunar day is counted forward. The resulting daily life address anchors an immutable twelve-designation overlay (命、兄弟、夫妻 through 父母); this is a coordinate map only. Its day Ganzhi is calculated from the effective Gregorian date selected by the Ziwei profile, not copied from the Bazi daily frame. Under S10's instruction to place daily moving auxiliaries from that day's Ganzhi, the day stem materializes the source-complete 禄羊陀 and 流昌曲 facts and preserves strict-S01 versus Wenmo-compatible 流魁钺 as unselected candidates. No candidate is promoted to a unique fact. The day stem also activates four immutable physical-star transformation facts through the calculation profile's explicitly bound S08 rule set. The output records the selected rule-set identity and the S01 transformation-variant conflict reference; it does not silently treat that profile choice as a universal table. A regular lunar month can be explicitly applied to the existing Ziwei interaction refresh path; all projected layer facts are displayed read-only but are not rewritten by the browser.

S10's general rule text does not provide a runtime-authoritative flow-hour active-address rule. The only available Five-Rats and hour-palace description is case-method evidence. R1 therefore preserves two named hour-coordinate candidates, `ZHONGZHOU_LUOYANG_MEAN_SOLAR_TIME` (fixed at S01's 112°26′ reference longitude) and `LOCAL_APPARENT_SOLAR_TIME`, with their own clocks, effective dates, day/hour Ganzhi, and S01 conflict references. Inside each unselected candidate, `S10:ZZTERM-P-0316` is represented literally as a case-scoped hour-branch life-address candidate and a derived twelve-designation overlay; it is explicitly marked `CASE_METHOD_ACTIVE_ADDRESS_CANDIDATE_NO_COMPLETE_CHART`, not promoted to a global rule. S10's 丙午时 example independently confirms hour-stem 擎羊 placement, so the same candidate also carries the case-scoped 禄存、擎羊、陀罗 trio from the locked S01 table. Each candidate additionally carries its own case-scoped S08 four-transformation activation facts. Neither time standard is silently selected, and neither partial coordinate candidate is promoted to a complete hourly chart.

If the effective date is in a leap month, R1 returns `LEAP_MONTH_UNRESOLVED_NO_FRAME` and `PARENT_LEAP_MONTH_UNRESOLVED_NO_FRAME` for the daily layer. It keeps the Daxian and Annual layer projections, but emits neither a regular-Month layer projection nor daily transformation activations. It does not silently map the leap month to a regular-month or daily frame; the browser leaves the regular lunar-month selector empty while still allowing the annual, Daxian, and minor-limit coordinates to be applied.

## Candidate and lineage preservation

Civil folds and uncertainty samples stay distinct throughout both projections. Every Bazi timeline is bound to its target-coordinate candidate ID. Every Ziwei projection candidate records the same upstream target candidate ID plus its Ziwei application/temporal hashes. Browser calculation never auto-applies a candidate, and multiple candidates require an explicit selection.

The link is therefore a shared target identity, not a shared calendar verdict:

- Bazi year/month/day/hour boundaries remain governed by the Bazi calculation profile;
- Ziwei lunar date and late-Zi handling remain governed by the Ziwei calculation profile;
- neither side overwrites the other's target facts or policy lineage.

## Integrity and schemas

The application-flow replay validates all seven Bazi layers, Xiaoyun candidate preservation, exact equality with the upstream Dayun/Flow/Daily-Hourly facts, and the complete temporal classical annotation projection. The shared Ziwei projection replay independently reconstructs its Daxian/Annual/regular-Month layer projections and their hashes from source frames, then reconstructs its effective lunar date, daily frame, daily twelve-designation and 禄羊陀／流昌曲 facts, and both time-standard hour candidates with their case-scoped address/designation/禄羊陀／流昌曲 facts (or the unresolved leap-month parent state).

Machine-readable contracts:

- `schemas/bazi-application-flow-integration-r1.schema.json`
- `schemas/shared-ziwei-selector-projection-r1.schema.json`

## Non-goals

R1 does not decide a Xiaoyun school, decide leap-month Ziwei flow doctrine, promote case-only flow-hour evidence into a global active-address rule, merge Bazi and Ziwei day boundaries, calculate strength/pattern/useful-god/favorable elements, activate ShenSha meanings, or produce event judgments, interpretations, training data, or predictions.
