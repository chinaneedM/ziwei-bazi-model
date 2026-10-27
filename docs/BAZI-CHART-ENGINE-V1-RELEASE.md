# Bazi Chart Engine V1 Release

## Release decision

```text
RELEASE_ID=BAZI-CHART-ENGINE-V1
RELEASE_VERSION=1.0.0
STATUS=FROZEN_V1
PRODUCTION_PROFILE=BAZI-FOUNDATION-V1-R1@1.1.0
ISSUE=#354
```

Bazi Chart Engine V1 is the released deterministic Natal engine built on the
shared Time / Calendar Foundation. Its public typed and JSON contracts are
frozen subject to the gates below.

This release statement does not add a calculation algorithm and does not alter
any existing Natal fact or hash. It names the already released default profile
as the production authority and records the completed Foundation boundary.

## Production profile authority

Product/default callers use:

```python
build_production_bazi_profile(policy_registry)
```

The selector is exported by `fortune_training.bazi_chart` and is an exact alias
of the established `bazi_foundation_v1_profile` builder. Both names therefore
produce the same immutable profile and retain the computation-hash identity:

```text
BAZI-FOUNDATION-V1-R1@1.1.0
```

The production profile remains bound to:

- `LOCAL_APPARENT_SOLAR` time coordinates;
- the Policy Registry default Bazi selection;
- the released sexagenary, hidden-stem, Ten-God, affinity and raw-relation rule sets;
- the released Natal, hidden-stem, Ten-God, affinity and raw-relation algorithms.

`BAZI-FOUNDATION-ZI-START-23-R1@1.0.0` remains a separately selectable,
explicit late-Zi profile. It is not silently substituted for the production
default and is not removed by this freeze.

## Frozen public boundary

The V1 boundary consists of:

- `BaziChartFoundation.resolve_typed()`;
- `BaziChartFoundation.resolve()`;
- `BaziChartCandidate`, `BaziNatalState` and `BaziTemporalSeed`;
- `validate_natal_state()`;
- `BaziNatalFactHash` and `BaziNatalComputationHash`;
- `schemas/bazi-chart-foundation-v1.schema.json`;
- `build_production_bazi_profile()`.

Candidate preservation, time-coordinate provenance, exact pillar identities,
hidden-stem membership, Ten-God bindings, affinity facts, raw relation
occurrences, integrity replay and hash separation are frozen behavior.

## Product routing

The standalone Bazi example, standalone Bazi local applications, target-flow
application and combined Ziwei+Bazi application use the production builder for
their default profile. Interfaces that accept a profile id continue to honor the
explicit late-Zi alternative.

No product entry point may construct a different unnamed Bazi default or infer a
late-Zi policy from display conventions.

## Completed downstream handoff

The deterministic Foundation Exit Audit has already passed. Released downstream
layers provide Jiaoyun/Dayun, Annual/Monthly, explicit target coordinates,
Daily/Hourly coordinates, application bundles and combined-shell composition.
Those layers bind and replay the Natal identity; they do not rewrite it.

The next work after this freeze is product/runtime use of released identities or
a separately governed semantic layer. It is not an open-ended expansion of Natal
Foundation.

## Explicit exclusions

This release does not include or authorize:

- strength/body-strength verdicts;
- Pattern, Useful God, favorable/unfavorable element selection;
- successful transformation or final Classical relation resolution;
- ShenSha or other optional annotations inside Natal identity;
- event interpretation or prediction;
- Ziwei+Bazi semantic synthesis;
- changes to `sources/canonical/`, training state or model-learning.

## Freeze gates

`STATUS=FROZEN_V1` remains valid only while all of these gates pass:

1. production and legacy builders remain the same callable and resolve to
   `BAZI-FOUNDATION-V1-R1@1.1.0`;
2. every frozen policy, rule-set and algorithm binding validates;
3. the public JSON result validates against the released schema;
4. typed and JSON resolutions preserve the same facts and hashes;
5. Natal integrity replay passes and tampering fails closed;
6. product defaults use the production authority while explicit profile
   alternatives remain available;
7. `fortune-train verify`, the complete unittest suite and required CI pass;
8. no freeze change mutates canonical sources, training/model state, prediction
   controls or downstream semantic behavior.

If a future change alters a frozen fact, profile binding, public schema, hash or
integrity contract, it requires a separately versioned release rather than an
in-place V1 rewrite.
