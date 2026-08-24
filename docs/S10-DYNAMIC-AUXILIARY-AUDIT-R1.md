# S10 dynamic auxiliary audit R1

This audit is limited to deterministic placement facts. It does not add
interpretation, prediction, strength, auspiciousness, or event judgement.

## Implemented: 流文昌／流文曲

S10 supplies a complete ten-stem placement table and explicitly applies the
source-layer stem at Daxian, Annual, Month, Day, and Hour scope. The released
generator therefore emits two independent activations per legal temporal frame
under `S10-STEM-FLOW-WENCHANG-WENQU-R1`.

- stable table sources: `S10:ZZZA-A-1101`, `S10:ZZZA-A-1102`
- layer/stem sources: `S10:ZZZA-A-1097` through `S10:ZZZA-A-1100`, and
  `S10:ZZZA-A-1103`
- the four grave branches omitted by that source remain omitted
- alternative-school placements are not inferred
- activation IDs contain the parent frame or hour-method candidate context, so
  equal names in different layers never share identity
- every emitted fact participates in frame, projection, and integrity replay

## Implemented as unresolved candidates: 流天魁／流天钺

S10 directs 流魁／流钺 back to the S01 static stem algorithm. S01 contains a
complete strict table, but the existing compatibility evidence reverses the 辛
stem 魁／钺 order (`午／寅` versus `寅／午`). Both are legal recorded methods in
this repository and cannot be collapsed into a single activation set.

R1 now exposes the strict S01 table and the compatibility case method as named,
independently hashed candidates with separate source chains. It does not select
either candidate. The candidate set is attached independently to Daxian,
Annual, Month, Day, and each Hour time-standard candidate.

- strict method: `S01-QS-STRICT-KUI-YUE-R1`
- compatibility method: `COMPAT-WENMO-KUI-YUE-R1`
- selection status: `CANDIDATES_PRESERVED_NO_SELECTION`
- strict stable sources: `S01:ZZQS-A-1800`, `S01:ZZQS-A-1801`,
  `S01:ZZZA-PR-019`
- compatibility evidence: `COMPAT:WENMO-CHARTDIFF-005`,
  `S01:ZZZA-PR-019`
- S10 dynamic-layer bridge: `S10:ZZZA-A-1097` through
  `S10:ZZZA-A-1099`

For 辛 the strict method emits 魁午／钺寅 while the compatibility method emits
魁寅／钺午. For the other nine stems both methods currently produce the same
visible positions, but their method, activation, source, and hash identities
remain independent. Equality of output is not treated as equality of method.

Candidate and candidate-set hashes have separate fact/computation projections.
Frame and shared-projection integrity replay reconstructs the candidates from
the source stem and method tables, so a locally rehashed placement mutation is
still rejected.

## Excluded

S10 names no additional dynamic star for implementation here unless it has a
complete placement table, an explicit time-layer stem basis, and stable source
identity. No rule is completed from customary knowledge or from interpretation.
