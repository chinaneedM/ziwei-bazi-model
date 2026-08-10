# Ziwei Application V1

## Status

```text
APPLICATION_ID=ZIWEI-APPLICATION-V1
APPLICATION_VERSION=1.0.0
STATUS=CANDIDATE_NOT_ACTIVE
ACTIVATION_CONDITION=MERGED_TO_MAIN
FOUNDATION_EXIT=ZIWEI-FOUNDATION-EXIT-AUDIT-R1/PASS
ISSUE=#206
```

Ziwei Application V1 is the first product-facing orchestration layer after Foundation Exit. It does not introduce a second calculation engine and does not alter V1 / Temporal / Structural R1-R5 semantics.

## Public path

```text
ApplicationBirthRequest
        ↓
ZiweiChartService.resolve(...)
        ↓
ZiweiChartFoundation.resolve_typed()
        ↓
unique validated ZiweiChartCandidate
        ↓
TemporalNatalContext + ZiweiTemporalEngine
        ↓
R1 → R2 → R3 → R4 → R5
        ↓
ZiweiViewProjectionCompiler
        ↓
ApplicationChartBundle
```

This replaces manual application-side wiring of the independent runtime layers with one public service call.

## Request boundary

`ApplicationBirthRequest` wraps the existing authoritative `BirthInput`; it does not invent a second birth/calendar schema. It adds only application-level selection metadata:

- sex and V1 calculation profile;
- presentation profile;
- selected Daxian frame id;
- selected Annual year;
- selected Minor Limit age;
- temporal generation range controls.

Ambiguous/multi-candidate natal results are not silently collapsed. Application V1 requires exactly one typed natal candidate before downstream orchestration.

## Bundle boundary

`ApplicationChartBundle` keeps typed object references to:

- the resolved natal candidate and hashes;
- Temporal context/state/hashes;
- R1 state;
- R2 state;
- R3 state;
- R4 state;
- R5 state;
- renderer-neutral ChartViewModel.

The bundle is not a flattened mega-state. Existing physical and semantic facts remain owned by their source runtime objects.

## Application identity

`bundle_hash` commits to references rather than duplicated payload:

- application profile/version;
- natal/temporal/R1-R5 FactHash and ComputationHash identities;
- typed natal candidate branch indices;
- selected Daxian/Annual/Minor parameters;
- ViewHash;
- Application Bundle Hash algorithm identity.

The hash therefore changes if the selected view or any upstream computation identity changes without claiming ownership of upstream facts.

## Fail-closed replay

Before a bundle is returned, rendered or exported, Application V1 checks:

- natal candidate PASS integrity;
- Temporal integrity and hash replay;
- R1 integrity and natal binding;
- R2 integrity;
- R3 integrity;
- R4 integrity;
- R5 integrity;
- ViewModel natal binding;
- exact ViewModel replay from stored presentation/temporal selection;
- exact application bundle hash replay.

Application validators delegate source-specific correctness to existing runtime validators. They do not duplicate placement, borrow or semantic rule logic.

## Export boundary

`ZiweiChartService.export()` returns `ZIWEI-APPLICATION-CHART-EXPORT-V1` containing:

- application profile identity;
- resolution status and branch indices;
- temporal selection metadata;
- natal/temporal/R1-R5 hash references;
- ViewHash and BundleHash;
- renderer-neutral ViewModel JSON.

Structural payload is not duplicated in the export. A future twelve-palace UI can consume the ViewModel for chart display and request R5 structural state separately when a structural overlay is required.

The existing plain-text renderer is exposed immediately through `render_plain_text()`.

## Explicit non-goals

Application V1 does not add:

- prediction or interpretation;
- 气数位 / 一六共宗 / 夹宫;
- new placement/dignity rules;
- dynamic borrowing beyond NATAL;
- graphical UI;
- Bazi integration;
- persistence/auth/cloud deployment.

## Candidate validation gate

Before activation:

- branch based on current Foundation Exit `main`, behind=0;
- application package/schema/test/doc additions only;
- one-call end-to-end bundle fixture PASS;
- deterministic replay PASS;
- Temporal selection/ViewHash regression PASS;
- R5 and View tamper rejection PASS;
- application export schema PASS;
- existing ViewModel schema PASS;
- repository bootstrap PASS;
- `fortune-train verify` PASS;
- full unittest PASS;
- no canonical/training/model-learning/prediction mutation.

After activation the next application slice should focus on the artifact needed for daily use: a graphical twelve-palace renderer/UI or a stronger deterministic ChartDiff/export fixture layer, without reopening Foundation.
