# Bazi Classical Relation Lifecycle Evidence Matrix R1 — Dependency / Gap Report

Status: source-grounded audit artifact; no Classical lifecycle semantic evaluator is released.

## Authority and coverage

- Source: `S14` / `b225e64fcf7238b27a634e653a6904403d518335aeca59372b32e02f4a560407`
- Canonical bytes: `3354845`
- Access segments reviewed in index order: `52/52`
- Evidence records: `775`
- Conflict groups: `2`
- Unresolved one-sided conflict records: `1`
- Profile-candidate records: `5`
- Pass-1 vocabulary closure: `合局, 战局, 方局, 暗会, 暗冲`
- Pass-2 vocabulary-only records: `20`
- Coverage claim: exhaustive for the declared R1 scan method and target relation/lifecycle scope, not for every Bazi doctrine.

## Evidence distribution

### Primary statement classes

| Statement class | Records |
|---|---:|
| `AMBIGUOUS` | 1 |
| `CLASH_OR_RELEASE_DEPENDENCY` | 25 |
| `COEXISTING_RELATION_DEPENDENCY` | 24 |
| `COMMENTARY_OR_EXPLANATION` | 73 |
| `CONTRADICTORY_OR_ALTERNATIVE_STATEMENT` | 5 |
| `DEFINITION_OR_NOMINAL_RELATION` | 86 |
| `ELIGIBILITY_CONDITION` | 58 |
| `EXAMPLE_ONLY` | 19 |
| `EXCEPTION_OR_LIMIT` | 35 |
| `EXPOSURE_OR_HIDDEN_STEM_DEPENDENCY` | 12 |
| `MULTIPLICITY_OR_COMPETITION` | 15 |
| `NON_TRANSFORMATION_OR_BINDING_CONDITION` | 88 |
| `ORDER_OR_PROXIMITY_DEPENDENCY` | 7 |
| `PUNISHMENT_DEPENDENCY` | 113 |
| `RESULT_OR_EFFECT_STATEMENT` | 60 |
| `ROOT_OR_SUPPORT_DEPENDENCY` | 7 |
| `RUNTIME_RELATION_GAP` | 53 |
| `SEASONAL_OR_MONTH_COMMAND_DEPENDENCY` | 21 |
| `TEMPORAL_CONTEXT_HINT` | 1 |
| `TRANSFORMATION_CONDITION` | 72 |

### Relation families

| Relation family | Records |
|---|---:|
| `BRANCH_BREAK` | 5 |
| `BRANCH_CHONG` | 86 |
| `BRANCH_DIRECTIONAL_PUNISHMENT` | 21 |
| `BRANCH_DIRECTIONAL_TRIAD` | 26 |
| `BRANCH_HARM` | 13 |
| `BRANCH_LIUHE` | 28 |
| `BRANCH_PARTIAL_TRINE` | 3 |
| `BRANCH_SANHE_COMPLETE` | 62 |
| `BRANCH_SELF_PUNISHMENT` | 9 |
| `BRANCH_ZIMAO_PUNISHMENT` | 14 |
| `CROSS_FAMILY_RELATION_LIFECYCLE` | 354 |
| `HIDDEN_COMBINATION` | 5 |
| `OTHER_UNRELEASED_RELATION` | 8 |
| `STEM_FIVE_COMBINATION` | 215 |

## Dependency findings

| Candidate family | Current exact input | Neutral-only input | Missing / unresolved | Recommended next slice |
|---|---|---|---|---|
| Stem combination eligibility / transformation | Stem occurrence IDs and raw Five-Combination occurrences | Month/support/exposure references | transformation success, binding, competition, profile choice | profile-explicit eligibility candidates without outcome verdicts |
| Branch harmony / complete trine | Exact Liuhe and complete-Sanhe occurrences | seasonal/support context | successful state change and precedence | candidate-preserving harmony eligibility schema |
| Clash interaction | Exact clash occurrences and BEFORE/AFTER sets | `PERSISTING/ENTERED/EXITED` frame-change evidence | release/cancellation/rescue semantics | separate clash-interaction evidence issue |
| Punishment interaction | Exact Zi-Mao, directed, and self-punishment occurrences | coexisting relation topology | precedence, suppression, result semantics | punishment-specific profile audit |
| Multiplicity / shared participant | exact incidence degree and `SHARED_PARTICIPANT/DISJOINT` | topology is neutral | competition/dominance/winner semantics | source-profile competition candidates |
| Month / season | `NATAL_MONTH_COMMAND` and separate `ACTIVE_FLOW_SOLAR_MONTH` | support-touch references | seasonal strength and role ambiguity | retain typed roles; add no score |
| Root / support / exposure | hidden-stem membership and exact exposure | `EXACT_HIDDEN_STEM_MATCH`, `SAME_ELEMENT_HIDDEN_SUPPORT` | root/strength grades | independent root semantics issue |
| Temporal layer | Dayun/Annual/Monthly frame identities | neutral frame-change evidence | automatic layer priority | profile-explicit temporal interaction issue |
| Unreleased relation families | none in current registry | none | Harm, Break, partial trine, directional triad, hidden combination | separate registry-governance issues only |

## Missing primitives

- `BINDING_OR_NON_TRANSFORMATION_OUTCOME`: 91 evidence record(s)
- `BRANCH_BREAK`: 5 evidence record(s)
- `BRANCH_DIRECTIONAL_TRIAD`: 26 evidence record(s)
- `BRANCH_HARM`: 13 evidence record(s)
- `BRANCH_PARTIAL_TRINE`: 3 evidence record(s)
- `CLASH_RELEASE_OR_CANCELLATION_SEMANTICS`: 30 evidence record(s)
- `CLASSICAL_COMPETITION_SEMANTICS`: 22 evidence record(s)
- `CLASSICAL_ORDER_OR_PROXIMITY`: 17 evidence record(s)
- `COEXISTING_RELATION_PRECEDENCE`: 33 evidence record(s)
- `HIDDEN_COMBINATION`: 5 evidence record(s)
- `OTHER_UNRELEASED_RELATION`: 8 evidence record(s)
- `PUNISHMENT_INTERACTION_OR_PRECEDENCE`: 195 evidence record(s)
- `ROOT_OR_SUPPORT_GRADE`: 13 evidence record(s)
- `STRENGTH_OR_WANGSHUAI_GRADE`: 21 evidence record(s)
- `TEMPORAL_LAYER_PRIORITY_SEMANTICS`: 11 evidence record(s)
- `TRANSFORMATION_SUCCESS`: 82 evidence record(s)

## Source conflicts and profile candidates

Alternative and contradictory statements are linked only when a shared explicit source conflict identifier and distinct source-side roles prove the pairing. One-sided conflict markers remain `CONFLICT_REQUIRES_REVIEW` without an invented counterpart. No majority vote, chronology guess, or universal default is selected. Records marked `PROFILE_CANDIDATE` require a later CHAT design decision.

## Semantic boundary

This audit does not rename neutral runtime facts. In particular, participant degree is not strength; `SHARED_PARTICIPANT` is not competition; `ENTERED` is not activation; `EXITED` is not release or cancellation; and active Flow month never replaces Natal month command.

No canonical source, model-learning, training state, prediction control, relation registry, or existing Natal/Temporal/Flow/Structural/Support/Incidence/Transition semantic contract is changed by this artifact.
