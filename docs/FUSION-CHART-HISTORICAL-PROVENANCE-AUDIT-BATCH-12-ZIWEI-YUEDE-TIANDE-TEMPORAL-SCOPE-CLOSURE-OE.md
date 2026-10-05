# Historical Provenance Audit — Batch 12OE

## Scope

Batch ID: `BATCH-12-ZIWEI-YUEDE-TIANDE-TEMPORAL-SCOPE-CLOSURE-OE`

Target: `HPA-ZMINOR-022` YueDe start-anchor dispute, with the adjacent `HPA-ZMINOR-006` TianDe/JieShen provenance bundle reviewed because the decisive received-Fullbook passage contains all three formulas.

This batch is a **temporal-scope closure**, not a natal algorithm reopen.

## Decisive source distinction

The received Fullbook passage does not present three equivalent birth-year rules:

- 天德: `天德星从酉上起子，顺数至流年太岁上是也。`
- 月德: `月德星从子上起子，顺数至流年太岁上是也。`
- 解神: `解神从戌上起子，逆数至当生年太岁上是也。`

The local contrast is controlling. TianDe and YueDe are explicitly attached to the **flow-year TaiSui**; JieShen is explicitly attached to the **birth-year TaiSui**. Therefore the Fullbook Zi-start YueDe is not a same-layer natal competitor to the production Si-start YueDe, and the Fullbook You-start TianDe line cannot by itself prove the production natal TianDe scope.

`神峰通考` independently preserves the premodern geometry `欲求天德顺从酉，月德要依巳顺逢`. That closes the existence of You-start TianDe / Si-start YueDe geometry outside the current product, but it does not establish an edition-bound Ziwei **natal adoption**.

## Runtime preservation

The already-landed received-Fullbook annual YueDe candidate is retained:

- `RECEIVED-FULLBOOK-ANNUAL-YUEDE-ZI-START-R1`
- source layer: `ANNUAL`
- selection: `SOURCE_SCOPED_CANDIDATE_PRESERVED_NO_SELECTION`

12OE adds the corresponding annual TianDe candidate:

- `RECEIVED-FULLBOOK-ANNUAL-TIANDE-YOU-START-R1`
- source layer: `ANNUAL`
- Zi-year -> You; then forward by annual branch
- selection: `SOURCE_SCOPED_CANDIDATE_PRESERVED_NO_SELECTION`

Both are projected through `AnnualFrame.auxiliary_candidate_sets`, shared candidate projection and the existing read-only candidate rendering. Neither changes `STAR.YUEDE` or `STAR.TIANDE` natal production placement.

## Matrix repair

**PROV-DEFECT-041** is repaired forward-only.

Old `HPA-ZMINOR-006` bundled TianDe and year-based JieShen and claimed the direct received text matched the selected year-branch geometry. That was too broad: its TianDe sentence is explicitly flow-year while JieShen is explicitly birth-year.

12OE therefore:

1. narrows `HPA-ZMINOR-006` to year-based JieShen / modern display `STAR.NIANJIE`;
2. reclassifies `HPA-ZMINOR-022` natal YueDe from `DISPUTED_MULTIPLE_CANDIDATES` to `SOURCE_INSUFFICIENT`, because the apparent Fullbook Zi-start competitor belongs to the annual layer;
3. adds `HPA-ZMINOR-027` for natal TianDe provenance, also `SOURCE_INSUFFICIENT`;
4. adds `HPA-ZTEMP-007` for the received-Fullbook annual TianDe/YueDe candidate pair, `HISTORICALLY_SUPPORTED` within that source-scoped annual interpretation.

No chart algorithm defect is confirmed. No production default, natal coordinate, winner selection or candidate collapse changes.

## Result

After 12OE:

- Matrix: **222 / 222 audited**
- HISTORICALLY_SUPPORTED: **97**
- DISPUTED_MULTIPLE_CANDIDATES: **29**
- SOURCE_INSUFFICIENT: **11**
- current MISSING_FROM_PRODUCT: **10**
- provenance defects: **41 / 41 repaired**
- historical candidate extensions: **8**
- chart algorithm defects / reopens / candidate collapses: **0 / 0 / 0**

Transmission impact is material: the genealogy graph now separates natal and annual TianDe/YueDe rule families and records the received-Fullbook passage as annual evidence rather than natal proof.

## Next

**12OF — HPA-ZMINOR-008 TianShou Body/Life basis source and candidate closure.**

Research record: `docs/research/ZIWEI-YUEDE-TIANDE-TEMPORAL-SCOPE-CLOSURE-R1.json`.
