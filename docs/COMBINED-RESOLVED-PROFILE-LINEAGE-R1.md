# Combined Resolved Profile / Rule / Algorithm Lineage R1

## Status

Read-only Workbench presentation of profile, RuleSet and algorithm identities already released by the combined deterministic chart resolution.

This release does not add a calculation rule, select a doctrinal method, alter any Ziwei/Bazi candidate, or formalize any unresolved transformation direction.

## Source of truth

`CombinedChartApplicationResolution` already releases:

- the combined profile;
- Ziwei calculation / application / presentation profiles;
- BaZi natal / temporal / application profiles;
- subsystem bundles;
- the shared time credential;
- candidate lineage;
- `manifest_hash`;
- the combined integrity report.

`combined_manifest_payload()` directly binds the combined profile identity plus the six subsystem `profile_id/profile_version` pairs into `ManifestHash`. The resolved profile validators and subsystem replay checks separately validate the RuleSet and algorithm bindings carried by those profile objects.

The Workbench therefore consumes the successful `/api/resolve` response directly. It does not maintain a parallel browser-side profile or rule registry.

## Workbench surface

Workbench 1.12 adds:

`已解析计算身份 / 规则版本`

The panel requires combined integrity `PASS` and a non-empty `manifest_hash` before displaying the resolved snapshot. It shows backend-provided identities including:

- combined profile plus composition algorithm and semantics;
- Ziwei calculation profile and its released time/rule/algorithm bindings;
- Ziwei application profile;
- Ziwei presentation profile;
- BaZi natal profile and released registry/rule/algorithm bindings;
- BaZi temporal profile and released direction/anchor/symbolic-age/calendar/Dayun-sequence identities;
- BaZi application profile;
- exact `ManifestHash`.

The panel is a presentation projection only. It does not call a new calculation endpoint and does not derive identities from user-facing labels.

## Semantic boundary

Profile identity means only: **this exact resolved chart used this versioned rule snapshot**.

It does not mean:

- canonical doctrine winner;
- a compatibility profile is classical authority;
- auspiciousness or strength judgment;
- prediction;
- automatic cross-system rule unification.

In particular, a compatibility profile remains explicitly a compatibility profile if the backend says so.

`ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION` remains `NOT_YET_FORMALIZED`. Palace-stem topology or other geometry must not be promoted into an inward/self-transformation direction rule by this presentation feature.

## Integrity boundary

The combined service validates profile-to-subsystem binding and recomputes `ManifestHash`. `ManifestHash` directly binds profile identities, while each resolved profile validator enforces its released RuleSet/algorithm identities and versions. The browser refuses the presentation when combined integrity is not `PASS`.

No browser-side hash, Profile ID, RuleSet ID or algorithm version is manufactured as chart truth.
