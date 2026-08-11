# Bazi Chart-Specific Exact Source Pattern Binding Candidates R1

- Source graph records: 24, each represented exactly once and in released graph order.
- `FULL_EXACT_BINDING_ENUMERATION`: 11.
- `PARTIAL_EXACT_BINDING_ENUMERATION`: 2 (`ZPZQ-CL-09-007-002`, `ZPZQ-CL-09-007-003`).
- `NOT_R1_EXACT_BINDABLE`: 11.
- Bindability is derived from released relation, participant, position, and multiplicity graph objects.
- Every plan and runtime inventory row replays upstream `unresolved_graph_requirements` in released source order as provenance, separately from binder-local structural constraints.
- Claim edges and narrative chains are carried only by stable IDs and are not candidate predicates.
- QTBJ `05347` / `05370` remain `SOURCE_GRAPH_NOT_R1_EXACT_BINDABLE`.
- Source-time contexts in `007-002` / `007-003` remain unresolved.
- Runtime enumeration uses Relation Incidence as lineage root and Branch/Stem Positional as fact projections.
- No operability, precedence, winner, activation, suppression, release, transition, or resolver semantics are emitted.
