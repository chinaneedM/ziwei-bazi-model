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

## Implemented as case-method candidates: 流天马

S01 supplies a complete twelve-branch Tianma placement table, while S10 keeps
two different temporal uses only at case-method authority. They are therefore
preserved as separate, unselected branch-basis candidates rather than promoted
to universal facts.

- Daxian method: `S10-LIMIT-PALACE-BRANCH-TIANMA-CASE-R1`; its basis is the
  Daxian life-palace branch (`S10:ZZTERM-P-0121`, `S10:ZZTERM-P-0122`,
  `S10:ZZTERM-TIME-05`).
- Annual method: `S10-ANNUAL-BRANCH-TIANMA-CASE-R1`; its basis is the annual
  branch, preserved from the 庚申→寅 example (`S10:ZZTERM-P-0204` through
  `S10:ZZTERM-P-0206`).
- Placement table: `S01:ZZQS-A-1808`, `S01:ZZQS-A-1809`.
- authority status: `CASE_METHOD_ONLY`.
- selection status: `CASE_METHOD_CANDIDATE_PRESERVED_NO_SELECTION`.

The candidate-set contract records `source_basis_type=BRANCH` and the exact
source branch. Daxian and Annual candidates have separate method, activation,
source and hash identities. No Month, Day, or Hour Tianma is generated because
S10 does not close those layer rules.

## Implemented as a read-only Minor-Limit encounter: 博士／将前／岁前三环

S05 explicitly names the natal 博士十二神、将前十二神、岁前十二神 rings as
the three groups used when a Minor Limit encounters them (`S05:S05-AUX-P-0537`,
`S05:S05-AUX-P-0542`). It does not provide a rule that re-anchors or regenerates
those rings from the Minor-Limit palace. The shared target projection therefore
intersects the selected Minor-Limit address with the three already generated
natal rings and returns exactly one source member per ring.

The projection preserves the Minor-Limit frame, active address and frame source,
plus each natal ring's ID, anchor, direction, generator/version, source chain and
original member fact. Its authority status is
`SOURCE_DIRECTED_NATAL_RING_ENCOUNTER_NO_REGENERATION`. Fact and computation
hashes are replayed independently; changing a member, ring lineage, frame or
rule remains detectable even after local rehashing. No ring nature,
auspiciousness or prediction text enters the runtime.

## Dynamic-star closure decision

The S10 implementation audit is now closed for the formal dynamic-star set.
No additional dynamic star is eligible merely because its name occurs in S10
prose, examples, or interpretive passages.

The source-closed set is:

| Dynamic item | Rule basis | Runtime disposition |
|---|---|---|
| 四化 | source-layer stem | implemented at every legal layer |
| 流禄存 | source-layer stem | implemented |
| 流擎羊 | source-layer stem / 禄存 relation | implemented |
| 流陀罗 | source-layer stem / 禄存 relation | implemented |
| 流天魁 | source-layer stem | strict S01 + compatibility candidates, unselected |
| 流天钺 | source-layer stem | strict S01 + compatibility candidates, unselected |
| 流文昌 | source-layer stem | implemented |
| 流文曲 | source-layer stem | implemented |

Counting the four independent transformation activations, the formal released
dynamic entity/type inventory is eleven. Every member is already represented
by a released deterministic activation or an explicit unselected candidate.

### Explicit non-implementation findings

- `流天马` is not promoted into the formal source-closed set. S10 only supports
  the separately recorded Daxian-palace-branch and Annual-branch case methods.
  They remain case candidates and do not authorize Month/Day/Hour expansion.
- Names or groups such as `天月`, `月解`, `日月` do not create a temporal
  placement rule by themselves. S10 explicitly distinguishes star names from
  flow-layer labels; no Month/Day activation is inferred from wording.
- The unresolved flow-hour discussion and editorial note that the source did
  not fully elaborate the section do not constitute an executable table.
- No explanatory judgment, example outcome, customary mnemonic, or external
  software display is allowed to fill a missing placement matrix.
- A future S10 addition requires all three gates: a complete placement table,
  an explicit temporal-layer input/basis, and stable source identity. If any
  gate is missing, the item remains `NOT_IMPLEMENTED_SOURCE_NOT_CLOSED`.

## Excluded

S10 names no further dynamic star for implementation here unless it has a
complete placement table, an explicit time-layer basis, and stable source
identity. No rule is completed from customary knowledge or from interpretation.

This closure is intentionally about implementation eligibility, not historical
correctness or school preference. Historical criticism, correctness comparison,
and school selection remain a later project phase after the deterministic
Ziwei+Bazi fusion chart is structurally complete.
