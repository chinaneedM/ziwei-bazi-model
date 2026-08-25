# Bazi Target-Flow Structural Projection R1

## Scope

This projection exposes the released `Bazi Structural Context R1` inside each
explicit Bazi target-flow candidate. It is a read-only composition layer, not a
second relation calculator:

```text
Natal + active Dayun/Annual/Monthly Flow
  -> Bazi Structural Context R1
    -> Bazi Target-Flow Structural Projection R1
```

The projection covers only the layers supported by the released Structural
Context: `DAYUN`, `ANNUAL`, and `MONTHLY`. `XIAOYUN`, `DAILY`, and `HOURLY`
are recorded in `excluded_layers`; this version does not silently extend the
structural tables to those layers. A `PRE_DAYUN` interval creates no Dayun
participant.

## Preserved facts and lineage

Every projected temporal participant retains its occurrence `instance_id`,
source layer, source Ganzhi, parent `source_frame_id`, and upstream Flow
FactHash. Equal characters in different frames therefore remain different
participants. The full neutral active Structural Context fact surface is
projected, including:

- active temporal stem and branch instances with element/polarity metadata;
- ordered temporal hidden-stem memberships and their rule/source identity;
- day-master-relative Ten God bindings for visible and hidden temporal stems;
- every dynamic hidden-stem exposure link involving a temporal occurrence;
- every dynamic stem-branch affinity involving a temporal occurrence;
- every neutral dynamic raw relation occurrence;
- stable IDs for the referenced natal exposure, affinity, and raw-relation
  facts.

Every neutral relation occurrence retains:

- occurrence and semantic relation IDs;
- relation family, arity, orientation, and neutral scope;
- participant instance IDs and participant layers;
- rule-set ID and version;
- stable source references;
- nominal transformation element when present.

`nominal_transformation_element` is registry metadata only. It does not mean
that a combination transformed successfully. No effect, priority, strength,
winner, cancellation, prediction, or interpretation field is permitted.

## Candidate preservation

Structural Context may aggregate only byte-identical structural facts with the
same computation lineage. The projection retains every contributing source
Flow candidate index. Each application-flow candidate must point to exactly one
such Structural candidate containing its own Flow index; missing, duplicate, or
out-of-range lineage fails closed.

## Hashes and replay

The application candidate directly binds the source Structural FactHash and
ComputationHash. Both are included in candidate identity; the fact hash enters
the application source hash and the computation hash enters the bundle hash.

The projection additionally owns an independently recomputable FactHash and
ComputationHash. Structural validation checks its schema/profile/algorithm,
coverage boundary, parent-frame provenance, exact visible-stem/branch registry
metadata, ordered hidden-stem membership, Ten God binding, exposure and
affinity identities/endpoints, participant-layer replay, relation arity/scope,
rule identity, sources, forbidden interpretive fields, and both projection
hashes. Full application replay then reconstructs the Structural Context from
Natal and Flow inputs and compares the exact final output. A locally modified
and rehashed projection therefore fails either local structural replay or the
independent full replay.

## Read-only workbench

The target-flow pane lists each active temporal pillar with its visible Ten God,
ordered hidden stems and hidden-stem Ten Gods, followed by every dynamic
exposure, affinity, and neutral relation fact with stable IDs, rule identity,
and sources. A nominal transformation element is labeled as a
non-transformation conclusion. The pane also displays the Structural and
projection hashes; it does not offer editing or rule-selection controls.

Machine-readable contract:

- `schemas/bazi-application-flow-integration-r1.schema.json`

## Non-goals

R1 does not calculate relation effects, transformation success, strength,
seasonal weighting, pattern, useful/favorable elements, ShenSha meanings,
judgments, training data, or predictions. It does not extend Structural Context
to Xiaoyun, Daily, or Hourly without a separately sourced and versioned runtime
contract. The downstream `Bazi Structural Support Foundation R1` remains a
separate evidence layer and is not mixed into this Structural Context
projection; its own target-flow projection is documented in
`docs/BAZI-TARGET-FLOW-STRUCTURAL-SUPPORT-PROJECTION-R1.md`.
