# Bazi Late-Zi Natal Profile Productization R1

Issue: #273

## Scope

Additive productization only. The existing `BAZI-FOUNDATION-V1-R1` remains the released `MIDNIGHT + CLASSICAL_CONTINUOUS` candidate. A second explicit natal profile exposes the already-supported `ZI_START_23 + ZI_START_ROLLOVER` policy combination without changing global policy defaults.

## New profile

- Profile ID: `BAZI-FOUNDATION-ZI-START-23-R1`
- Day boundary: `ZI_START_23`
- Late-Zi hour stem: `ZI_START_ROLLOVER`
- Year boundary: inherited existing `START_OF_SPRING`
- Civil ambiguity policy: inherited existing registry default
- Time coordinate: existing `LOCAL_APPARENT_SOLAR`
- Natal algorithms, registries, hidden stems, Ten Gods, affinities, and raw relations: unchanged

## Product exposure

- `fortune-bazi-app`: explicit natal-profile selector.
- `fortune-chart-app`: independent explicit Bazi natal-profile selector; combined composition remains identity-only.

## Calibration regression

Shanghai male, reported civil `2008-11-03 22:50`, `31.2304, 121.4737`, `Asia/Shanghai`:

- local apparent solar time remains the same under both profiles and is in the 23:00 Zi period;
- `BAZI-FOUNDATION-V1-R1` must remain `戊子 壬戌 丁未 壬子`;
- `BAZI-FOUNDATION-ZI-START-23-R1` must produce `戊子 壬戌 戊申 壬子`;
- ordinary non-boundary natal semantics must remain identical between the two profiles apart from explicit profile/computation lineage.

External application agreement observed during calibration is witness evidence only and is not encoded as source authority.

## Explicit non-goals

No policy-registry default change, no classical-truth declaration, no Ziwei change, no Dayun algorithm change, no prediction semantics, no Classical Interaction resolver semantics.
