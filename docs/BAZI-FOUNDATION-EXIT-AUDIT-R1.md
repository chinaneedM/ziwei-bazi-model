# Bazi Foundation Exit Audit R1

## Decision

```text
AUDIT_ID=BAZI-FOUNDATION-EXIT-AUDIT-R1
STATUS=PASS
MANDATORY_DETERMINISTIC_FOUNDATION=COMPLETE
NEXT_PHASE=BAZI-APPLICATION-FLOW-INTEGRATION-R1
ISSUE=#298
BASELINE_MAIN=280036ac50d8eef64571243b72a3984b5af1564c
```

This audit closes the open-ended deterministic Bazi Foundation phase at the stated baseline. The current repository already provides the machine-consumable Natal, Jiaoyun/Dayun, Annual/Monthly, explicit target-coordinate, and Daily/Hourly coordinate layers needed for an application handoff.

Future work must not reopen deterministic Foundation merely because another traditional annotation, interpretive method, Classical semantic rule, product feature, or UI convention is discovered. A Foundation reopen requires evidence that a missing or incorrect item changes deterministic chart/time-coordinate output, a frozen state/hash/integrity contract, candidate preservation, or the correctness of the typed application handoff.

This audit adds no prediction, interpretation, source doctrine, or new calculation algorithm.

## Gate A — Time / Calendar + Natal: PASS

The released Time / Calendar and Bazi Natal path provides a typed computation route from `BirthInput` through civil-time resolution and local-apparent-solar coordinates to Bazi Natal candidates.

The current deterministic Natal boundary already provides:

- explicit birth civil/spatial input identity;
- IANA-timezone-aware civil resolution, including historical confidence and warnings;
- explicit fold/gap handling and uncertainty sampling rather than silent time collapse;
- local-apparent-solar provenance under released calculation-profile policies;
- deterministic year, month, day, and hour Natal pillars;
- typed stem and branch occurrence identities;
- hidden-stem instances;
- visible and hidden Ten-God identities;
- released neutral Natal relation facts;
- independent integrity validation;
- deterministic Natal FactHash and ComputationHash;
- machine-readable public schemas and export paths.

The public schema boundary includes `schemas/time-calendar-foundation-v1.schema.json` and `schemas/bazi-chart-foundation-v1.schema.json`.

The Foundation does not require a new Natal engine.

## Gate B — Jiaoyun / Dayun: PASS

The released Bazi temporal layer provides deterministic Jiaoyun and Dayun state downstream of a validated Natal candidate.

The current temporal contract includes:

- explicit direction semantics;
- auditable Jie anchor selection;
- profile-bound Jiaoyun interval-coordinate semantics;
- explicit calendar realization rules;
- typed `PRE_DAYUN` and Dayun frame identities;
- contiguous half-open Dayun intervals;
- candidate preservation when birth-time uncertainty produces distinct legal temporal lineages;
- independent temporal integrity validation;
- deterministic Temporal FactHash and ComputationHash;
- exact binding back to the Natal candidate without rewriting Natal facts or hashes.

The public schema boundary includes `schemas/bazi-temporal-v1.schema.json`.

Real-machine calibration and subsequent regression work have already exercised mixed-clock Jie boundaries, historical time behavior, uncertainty, and transition edge cases. No new Jiaoyun/Dayun algorithm is required for Foundation Exit.

## Gate C — Annual / Monthly Flow: PASS

`BaziFlowContext` is a separate deterministic target-UTC layer downstream of Natal and Dayun identities.

It provides:

- target UTC identity;
- active `PRE_DAYUN` or Dayun frame selection;
- typed `AnnualFrame`;
- typed `MonthlyFrame`;
- exact Start-of-Spring and monthly-Jie half-open boundary semantics;
- candidate-lineage preservation;
- independent Flow integrity validation;
- deterministic Flow FactHash and ComputationHash;
- upstream Natal/Temporal hash binding without mutation.

The public package `fortune_training.bazi_flow` exposes `BaziFlowEngine`, `BaziFlowRequest`, `BaziFlowCandidate`, `BaziFlowContext`, `AnnualFrame`, `MonthlyFrame`, hash helpers, and integrity replay.

The public schema boundary includes `schemas/bazi-flow-context-v1.schema.json`.

Annual and Monthly identity remains the absolute target-UTC / solar-term authority. Later Daily/Hourly projection does not mint a competing Annual/Monthly truth.

## Gate D — Explicit Target Coordinate + Daily / Hourly: PASS

Issues #292 and #294 complete the missing target-place and sub-month temporal coordinate layers without extending the released Flow identity in place.

### Target Temporal Coordinate Foundation

`fortune_training.bazi_target_temporal` provides a semantic input distinct from `BirthInput` for target/query/event coordinates.

The released target-coordinate contract provides:

- explicit target place identity;
- explicit latitude and longitude;
- explicit IANA timezone identity;
- target civil-time realization;
- DST fold/gap handling;
- uncertainty candidate preservation;
- target UTC;
- target local-mean/local-apparent-solar provenance;
- independent TargetCoordinate integrity and hashes;
- no silent fallback to Natal birth longitude.

The public schema boundary includes `schemas/bazi-target-temporal-coordinate-foundation-r1.schema.json`.

### Daily / Hourly Flow Sidecar

`fortune_training.bazi_daily_hourly_flow` consumes one compatible Flow candidate, one explicit TargetCoordinate candidate, and one released Bazi calculation profile.

It provides:

- typed `DailyFrame`;
- typed `HourlyFrame`;
- shared-resolver replay through the released Bazi day/hour calculation path;
- explicit day-boundary and late-Zi policy binding;
- target-LAS and longitude provenance;
- candidate/source-index lineage preservation;
- independent Daily/Hourly FactHash and ComputationHash;
- resolution-level replay/tamper detection;
- fail-closed Flow/Target/Profile compatibility checks;
- byte-stable upstream Flow Annual/Monthly identity.

The public schema boundary includes `schemas/bazi-daily-hourly-flow-sidecar-r1.schema.json`.

The required deterministic temporal chain is therefore complete:

```text
BirthInput
  -> Time / Calendar
  -> Bazi Natal
  -> Jiaoyun / Dayun

Natal + Dayun + target UTC
  -> Bazi Flow
     -> PRE_DAYUN / Dayun
     -> Annual
     -> Monthly

TargetTemporalInput
  -> Target Temporal Coordinate
     -> target civil realization
     -> target UTC
     -> target LAS

Flow + TargetCoordinate + Bazi calculation profile
  -> Daily / Hourly Sidecar
     -> Daily
     -> Hourly
```

## Gate E — Neutral Structural Substrate: PASS

The repository also contains separately versioned deterministic structural substrates, including:

- Bazi Structural Context;
- Structural Support Foundation;
- Relation Incidence Foundation;
- Relation Transition Foundation;
- Stem Relation Positional Context;
- Branch Relation Positional Context.

These layers preserve exact participant/frame identities, provenance, multiplicity, topology, source hashes, and candidate lineage while remaining neutral about final Classical outcomes.

Their relevant public schema boundaries include:

- `schemas/bazi-structural-context-r1.schema.json`;
- `schemas/bazi-structural-support-foundation-r1.schema.json`;
- `schemas/bazi-relation-incidence-foundation-r1.schema.json`;
- `schemas/bazi-relation-transition-foundation-r1.schema.json`;
- `schemas/bazi-stem-relation-positional-context-foundation-r1.schema.json`;
- `schemas/bazi-branch-relation-positional-context-foundation-r1.schema.json`.

These are machine-consumable structural facts, not final interpretive verdicts.

Foundation Exit does **not** require these neutral structures to decide:

- 旺衰 final grade;
- 格局;
- 用神 / 喜忌;
- 调候 / 病药;
- 合化 success or failure;
- relation operability;
- precedence, suppression, release, or cancellation;
- winner/loser selection;
- global relation lifecycle state;
- 吉凶 or event interpretation.

The repository's existing Classical assertion, graph, admission, closure, candidate, and disposition layers remain separately governed pre-resolver research. Their existence does not turn completion of a global Classical resolver into a deterministic chart-foundation prerequisite.

## Gate F — Serialization / Application Handoff: PASS WITH APPLICATION INTEGRATION GAP

The underlying deterministic layers have public typed APIs, integrity replay, hashes, and schemas sufficient for machine composition.

However, the current `BaziChartService` application orchestration is an earlier vertical slice. At this baseline, `BaziChartService.resolve()` performs:

```text
Birth/Application request
  -> Bazi Natal Foundation
  -> Bazi Temporal Engine
     -> Jiaoyun / Dayun
  -> Application candidate/view
```

It does not yet orchestrate:

- `BaziFlowEngine`;
- `TargetTemporalCoordinateFoundation`;
- `BaziDailyHourlyFlowEngine`.

This is an **Application Architecture / integration gap**, not a missing deterministic Foundation algorithm.

The next application slice should compose existing identities rather than flatten or recalculate them:

```text
Birth/Application request
  -> existing Bazi Natal + Dayun application path

explicit TargetTemporalInput
  -> TargetTemporalCoordinateFoundation

Natal + Dayun + target UTC
  -> BaziFlowEngine

Flow + TargetCoordinate + Bazi calculation profile
  -> BaziDailyHourlyFlowEngine

Application bundle/view
  -> references Natal identity
  -> references Temporal identity
  -> references Flow identity
  -> references TargetCoordinate identity
  -> references DailyHourly identity
  -> does not rewrite upstream facts or hashes
```

Therefore the absence of one all-in-one Bazi target-time application function does not block Foundation Exit. It defines the next narrow product-integration issue.

## Optional Annotation Governance — Issue #293

Issue #293 already closed the boundary for four familiar traditional output families. They remain non-blocking for deterministic Foundation Exit:

- **Nayin / 纳音** — optional deterministic downstream annotation;
- **Taiyuan / Minggong / Shenggong / 胎元命宫身宫** — optional profiled derived coordinates;
- **Twelve Changsheng / 十二长生** — optional profiled annotation;
- **ShenSha / 神煞** — optional registry/profile/plugin family.

These families must not be folded into Natal, Temporal, Flow, TargetCoordinate, or DailyHourly identity merely to make a display look more complete.

A future application profile may explicitly require one of them, but that would be a versioned downstream dependency decision rather than evidence that the current deterministic coordinate foundation was incomplete.

## Explicitly Non-Blocking Backlog

Unless future evidence demonstrates a deterministic contract defect, the following items do not block Foundation Exit:

- 纳音;
- 胎元 / 命宫 / 身宫;
- 十二长生;
- 神煞;
- target-location doctrine selection among birth/current/event/query place;
- 旺衰;
- 格局;
- 用神 / 喜忌;
- 调候 / 病药;
- final Classical relation operability / precedence / resolver;
- event interpretation or prediction;
- Ziwei + Bazi semantic synthesis;
- graphical UI completeness.

The target-coordinate core intentionally requires an explicit target coordinate. It does not decide which real-world doctrine should supply that coordinate.

## Integrity and Identity Boundary

The completed deterministic stack is intentionally identity-separated:

```text
Natal identity
  != Temporal/Jiaoyun-Dayun identity
  != Flow Annual/Monthly identity
  != TargetCoordinate identity
  != DailyHourly identity
```

Downstream objects bind upstream identities and replay their integrity; they do not silently rewrite them.

This separation is a completion criterion, not an unfinished feature. It prevents later Application, annotation, Classical semantic, or prediction layers from retroactively changing the meaning of earlier deterministic facts.

## Next Phase

The default next phase is:

```text
BAZI-APPLICATION-FLOW-INTEGRATION-R1
```

Its purpose should be product/application composition, not new calendrical doctrine or interpretation.

A narrow first slice should make the standalone Bazi application able to accept an explicit target-time/target-place request and return one deterministic bundle referencing:

1. Natal candidate identity;
2. Jiaoyun/Dayun temporal identity;
3. active Flow Annual/Monthly identity;
4. TargetCoordinate identity;
5. Daily/Hourly identity;
6. renderer-neutral target-time view/export data;
7. independent application-level integrity that replays, rather than duplicates, those upstream layers.

Combined Ziwei+Bazi application integration can remain a later identity-only composition step unless a separate issue explicitly changes that boundary.

## Foundation Reopen Rule

After this audit is merged, future discoveries are classified by the following rule:

```text
new discovery
    ↓
does it change or invalidate
  - deterministic Natal output,
  - civil / LAS coordinate correctness,
  - Jiaoyun / Dayun boundaries,
  - Annual / Monthly / Daily / Hourly coordinates,
  - frozen state/hash/integrity identity,
  - candidate preservation,
  - or typed machine handoff correctness?
    ├── YES -> evaluate as deterministic Foundation/runtime defect
    └── NO  -> Application / optional annotation /
              Classical semantic runtime / interpretation /
              prediction / product backlog
```

A new traditional term, display convention, interpretive school, or optional annotation is not sufficient by itself to reopen Foundation.

## Audit Scope Integrity

This audit records the current architecture only. It does not modify:

- `sources/canonical/`;
- `sources/canonical-manifest.json`;
- `model-learning/`;
- `training/state.json`;
- prediction controls;
- Ziwei runtime semantics;
- Bazi Classical resolver semantics;
- released Natal, Temporal, Flow, TargetCoordinate, or DailyHourly production code.

## Exit Statement

At baseline `280036ac50d8eef64571243b72a3984b5af1564c`, the mandatory deterministic Bazi Foundation is complete for a machine-consumable application handoff.

The next missing capability is not another Bazi calculation foundation. It is orchestration of the already-released target-time layers into the standalone Bazi application.
