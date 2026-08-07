# Time / Calendar Foundation R1

## Scope and repository fit

This phase adds deterministic chart-input infrastructure inside the existing
`fortune_training` package. It does not create a second controller, does not
change training state or `model-learning`, and does not read or modify
`sources/canonical/`.

R1 implements:

- typed birth input and explicit time precision;
- IANA civil-time resolution, including DST folds and gaps;
- local mean and local apparent solar datetimes with date rollover;
- global UTC instants for all 24 solar terms;
- an astronomical modern Chinese calendar adapter for 1901–2100;
- year, month, day and hour time pillars under named policies;
- separate civil-date and local-solar-date Ziwei calendar mappings;
- machine-readable policy metadata and audit traces.

R1 deliberately does not implement Ziwei palace construction, life/body
placement, five-element bureau, stars, transformations, periods, interpretation,
historical dynastic calendars, or a UI.

## Architecture

| Layer | Implementation | Output role |
|---|---|---|
| BirthInput | `models.py` | Reported wall time, place, coordinates, IANA zone, precision and input type |
| CivilTimeResolver | `timezone.py` | UTC candidate(s), offset, DST, fold/gap state, tzdb confidence |
| SolarTimeEngine | `solar.py` | LMT, equation of time and full local apparent solar datetime |
| SolarTermEngine | `astronomy.py` | Apparent geocentric longitude events in UTC |
| ChineseCalendarEngine | `calendar.py` | Raw lunar year/month/day/leap flag and month length |
| BaziTimeResolver | `bazi.py` | Four time pillars plus effective day and boundary facts |
| ZiweiCalendarResolver | `ziwei.py` | Civil and solar lunar mappings, selected effective date, divergence event |
| PolicyRegistry | `config/time-calendar-policies.json` | Named, versioned conventions and scope limits |
| AuditTrace / orchestrator | `engine.py` | End-to-end fact/policy provenance and uncertainty branches |

## Fact/policy separation

Facts are retained independently:

```text
reported civil datetime
→ IANA timezone rule / DST / fold
→ UTC instant
→ longitude-derived local mean solar datetime
→ equation of time
→ complete local apparent solar datetime
→ civil-date and solar-date Chinese-calendar mappings
```

Policies are applied only after the relevant facts exist. The effective Ziwei
date never overwrites either raw mapping. `life_body_leap_month_policy` is
recorded but is not applied in R1 because its only allowed scope is the later
`ZIWEI_LIFE_BODY_PLACEMENT` phase.

The civil-time layer and Chinese-calendar day boundary intentionally use two
different time concepts. Birth-wall-time resolution uses the historical IANA
zone (including DST where applicable). The modern Chinese calendar uses fixed
**Beijing Standard Time, UTC+08:00 (120°E standard time)** for its calendar-day
boundary; historical Chinese civil DST must not shift a new moon, solar term,
or lunar date into another official calendar day.

## Astronomy, calendar and timezone dependencies

| Component | Choice | License / authority | R1 precision and portability decision |
|---|---|---|---|
| Timezone | Python `zoneinfo` + first-party `tzdata` | Python / IANA tzdb | Cross-platform; exact tzdata version is emitted. Pre-1970 results carry reduced confidence because IANA defines location-zone agreement primarily since 1970. |
| Solar and lunar events | Astronomy Engine 2.1.x | MIT; VSOP87/NOVAS-based, tested upstream against JPL Horizons | Pure Python, no downloaded ephemeris, advertised position accuracy within 1 arcminute; exact installed version and accuracy claim are emitted. |
| Modern Chinese calendar | Repository algorithm using astronomical events; fixed UTC+08:00 calendar standard time | GB/T 33661-2017 governance; HKO rules/oracles | Month starts, winter-solstice month and no-principal-term leap rule are calculated, not table-looked-up. R1 validated range is 1901–2100. Historical civil DST is not used as the lunar-calendar day boundary. |

Authority fixtures live in
`tests/fixtures/time-calendar-foundation-r1.json`. HKO tables and an independent
USNO/NOAA-style equation-of-time calculation are regression oracles, not the
production algorithm. Wenmo/Wenzhen observations are explicitly tagged as
compatibility-only.

## Policy registry

| Policy ID | R1 default | Status / scope |
|---|---|---|
| `civil.ambiguous_time_policy` | `REJECT` | Operational fail-closed default |
| `bazi.year_boundary_policy` | `START_OF_SPRING` | UTC instant of longitude 315° |
| `bazi.day_boundary_policy` | `MIDNIGHT` | Explicit convention; alternative `ZI_START_23` |
| `bazi.late_zi_hour_stem_policy` | `CLASSICAL_CONTINUOUS` | Core candidate, not settled classical truth |
| `ziwei.calendar_date_policy` | `LOCAL_SOLAR_DATE_INDEXED` | Core candidate, not settled classical truth |
| `ziwei.life_body_leap_month_policy` | `FULLBOOK_NEXT_MONTH` | Textual candidate; life/body placement only |

The complete alternatives and descriptions are held only in the registry.
Boolean aliases and unnamed constants are rejected by repository verification.

## Machine-readable AuditTrace example

Run:

```bash
PYTHONPATH=src python scripts/time-calendar-example.py
```

The Kashgar fixture emits seven ordered trace steps. The central facts include:

```json
{
  "reported_civil_datetime": "2000-12-26T01:40:00",
  "utc_instant": "2000-12-25T17:40:00Z",
  "local_mean_solar_datetime": "2000-12-25T22:43:57.552",
  "local_apparent_solar_datetime": "2000-12-25T22:43:36.23778",
  "events": ["CALENDAR_DATE_DIVERGENCE"],
  "effective_ziwei_lunar_date": {
    "year": 2000,
    "month": 11,
    "day": 30,
    "is_leap_month": false
  },
  "bazi_time_pillars": ["庚辰", "戊子", "丁巳", "辛亥"]
}
```

The full result conforms to
`schemas/time-calendar-foundation-v1.schema.json` and includes installed
algorithm/tzdb versions and the selected registry version.

## Boundary and regression coverage

`tests/test_time_calendar_foundation.py` and
`tests/test_time_calendar_standard_time.py` cover:

1. standard modern China time;
2. true-solar hour change and full-second retention;
3. true-solar date rollover;
4. 23:00, 00:00 and 01:00 plus all late-Zi policies;
5. the microsecond before/after a solar-term instant using UTC comparison;
6. historical China DST for birth civil-time resolution;
7. fixed UTC+08:00 Beijing Standard Time for Chinese-calendar day boundaries during historical DST;
8. an overseas IANA zone;
9. an ambiguous DST fold;
10. a nonexistent DST gap;
11. a new-moon date boundary;
12. civil/solar calendar-date divergence;
13. a leap month under every scoped policy value;
14. the 2033 leap-eleventh-month anomaly;
15. reported-time uncertainty crossing a classification boundary;
16. approximate reported times failing closed unless an explicit uncertainty interval is supplied;
17. Astronomy Engine results cross-checked against HKO and an independent EOT formula;
18. already-true-solar input failing closed when UTC cannot be reconstructed;
19. repository policy/schema integrity.

## Open questions

- Certify the acceptable astronomical guard band for births extremely close to
  a solar term or a new moon at China-calendar midnight. R1 exposes the
  upstream accuracy contract; a DE440/JPL reference job can be added without
  replacing the portable production engine.
- Decide whether commercial operation requires a separately pinned tzdb release
  per deployment instead of recording the installed release in every output.
- Confirm whether worldwide Ziwei work always indexes the unified official
  Chinese calendar using fixed Beijing Standard Time (UTC+08:00), or needs a
  second explicitly named local-calendar policy. R1 does not guess.
- Validate the late-Zi and Ziwei effective-date Core candidates against the
  selected classical texts and additional independent software fixtures.
- Add historical Chinese calendar strategy objects before accepting dates
  outside the R1 modern range.
- Determine proven scopes, one algorithm at a time, for leap-month treatment
  beyond life/body placement. No propagation is currently allowed.

## Phase-02 readiness

The repository is ready to begin the **Ziwei twelve-palace skeleton** as a
separate layer consuming R1 outputs. The next phase can safely implement life
palace, body palace, palace stems and five-element bureau only if it:

- consumes `effective_ziwei_lunar_date` and the complete apparent-solar time;
- records the selected policy IDs and registry version;
- keeps raw civil/solar lunar mappings in its parent trace;
- applies leap-month policy only to the exact algorithm scope being implemented;
- branches or fails closed when R1 returns multiple/unresolved candidates.
