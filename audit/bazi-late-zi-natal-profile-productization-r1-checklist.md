# Acceptance checklist — Issue #273

- [x] Existing `BAZI-FOUNDATION-V1-R1` preserved as `MIDNIGHT + CLASSICAL_CONTINUOUS`.
- [x] New explicit `BAZI-FOUNDATION-ZI-START-23-R1` uses `ZI_START_23 + ZI_START_ROLLOVER`.
- [x] Global time/calendar defaults unchanged.
- [x] Standalone Bazi local app exposes both natal profiles.
- [x] Combined local shell exposes Bazi natal profile independently from Ziwei and Dayun profiles.
- [x] Combined composition service remains identity-only; no cross-system resolver added.
- [x] Focused Shanghai late-Zi regression added for old/new profile fork.
- [x] Ordinary non-boundary regression added.
- [x] Application integrity/hash replay remains in the existing services.
- [x] Ziwei algorithms untouched.
- [x] Dayun algorithms untouched.
- [x] Prediction and Classical Interaction semantics untouched.

CI status is intentionally not asserted in this file; GitHub exact-head checks remain authoritative.
