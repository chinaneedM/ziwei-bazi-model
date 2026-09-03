# Fusion Chart Product R1 Final Acceptance — 2026-09-04

## Immutable audit source

```text
AUDIT_ID=FUSION-CHART-PRODUCT-R1-FINAL-ACCEPTANCE-20260904
BASELINE_BRANCH=agent/fusion-chart-core-r1-20260822
AUDIT_SOURCE_COMMIT=e720be2aa11b619ef52f81b2fb4f8bedbe864be9
AUDIT_SOURCE_TREE=a6d4d7ebde6e092028b9a8a288b1997c719d272b
AUDIT_SOURCE_CI_RUN=33782770369
AUDIT_SOURCE_CI_STATUS=SUCCESS
```

This acceptance audit uses the immutable GitHub tree above as its evidence source. It does not reopen already-closed deterministic calculation layers merely to perform product or platform packaging work.

## Final R1 state

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
WINDOWS_BINARY_PLATFORM_ACCEPTANCE=PENDING_PLATFORM_ACCEPTANCE
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
DISPUTED_CANDIDATE_POLICY=NO_WINNER
```

The two acceptance domains are intentionally separate. The deterministic fusion-chart product is closed at R1. The emitted Windows portable binary still requires platform-level execution acceptance; that pending state is not a chart-algorithm blocker and must not reopen the deterministic chart product by itself.

## Scope frozen by this audit

The following already-released foundations remain closed and are not redesigned in this acceptance pass:

- shared time/calendar credentials and independent Ziwei/Bazi policy projections;
- Bazi natal deterministic chart identity and target-flow chain;
- Ziwei natal deterministic chart identity;
- Ziwei Structural Runtime R1–R8;
- Combined Target-Flow Fusion R2;
- released candidate-preserving sidecars and Workbench projections.

A future product or packaging defect may reopen the relevant presentation, desktop, updater or release contract. A deterministic calculation layer is reopened only when evidence demonstrates incorrect chart output, broken replay/hash lineage, broken candidate preservation, or an incorrect typed handoff in that layer.

## Deterministic product evidence

### Field parity

`docs/FUSION-CHART-FIELD-PARITY-MATRIX-R1.json` contains no actual field row with status `ALREADY_RELEASED_NOT_YET_VISIBLE`. The status name remains in the schema definition, but the current field inventory has no released deterministic field waiting only for Workbench visibility.

`ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION` remains exactly `NOT_YET_FORMALIZED`. Existing SAME/OPPOSITE/OTHER palace-stem topology and structural geometry are not promoted into OUTWARD_DISSIPATION / INWARD_RECEPTION.

Rows intentionally classified as `DISPUTED_CANDIDATE_ONLY` remain candidate-preserving. Product closure does not select a school, collapse method identities, or create a winner.

### Desktop runtime boundary

The Windows portable desktop runtime is already defined as a thin product shell around the released combined Workbench:

- packaged runtime-root resolution is independent of the current working directory;
- runtime repository data is explicitly inventoried and excludes training, answer-vault, model-learning and canonical source trees;
- packaged build metadata binds application identity, semantic version and the exact 40-character source commit;
- the desktop launcher requests an ephemeral port and enforces `127.0.0.1` loopback binding;
- browser opening is optional and no chart rule is recomputed in the launcher;
- source execution does not invoke the packaged update path.

These contracts are covered by `tests/test_windows_portable_desktop_launcher_r1.py`.

### Update and integrity boundary

The verified update path is already closed as a packaging/integrity mechanism:

- fixed stable manifest location and fixed repository release route;
- strict semantic-version parsing and no downgrade/prerelease acceptance;
- manifest binding of version, exact source commit, asset URL, SHA-256 and byte size;
- archive size/entry bounds plus path-traversal, symlink and case-collision rejection;
- staged bundle verification requiring the application, standalone updater and build metadata;
- staged version/source-commit equality with the manifest;
- standalone updater execution outside the installation tree;
- complete-tree activation with rollback to the known-good installation on activation failure.

These contracts are covered by `tests/test_windows_verified_auto_update_r1.py` and the stable-promotion control tests.

### Build and release gates

`.github/workflows/windows-portable.yml` builds on `windows-latest`, checks out the exact source commit, runs the Windows-focused contract tests, validates the release ref against the packaged application version, builds the PyInstaller onedir portable bundle, and validates source commit / SHA-256 / size before release publication.

The stable release is split into an immutable versioned release plus a mutable stable-channel manifest pointer. The final R1 machine gate is also required by the normal CI and Windows release workflow so future field-status or acceptance-state drift fails closed.

### Workbench acceptance evidence

`docs/COMBINED-WORKBENCH-REAL-MACHINE-CALIBRATION-R1.md` defines the source/runtime browser acceptance contract, including loopback startup, base chart composition, Ziwei interaction, Bazi target-flow, shared-target projection, explicit Apply, stale-view invalidation, and candidate preservation. The automated Workbench smoke and HTTP smoke remain release gates for the deterministic product composition.

## Why Windows binary platform acceptance remains pending

The current Windows workflow proves that a portable artifact can be built and structurally validated on a Windows GitHub runner. It does not currently provide acceptance evidence that the generated `FortuneChart.exe` and `FortuneChartUpdater.exe` were launched from the emitted ZIP as end-user binaries and completed the full platform interaction/update activation contract.

Therefore the correct state is:

```text
WINDOWS_BINARY_PLATFORM_ACCEPTANCE=PENDING_PLATFORM_ACCEPTANCE
```

This is deliberately narrower than product closure. It concerns PyInstaller/Windows runtime behavior such as executable launch, packaged dependency loading, browser/loopback behavior from the binary, process replacement and updater activation on Windows. It is not evidence that Ziwei, Bazi, time/calendar or fusion algorithms are incomplete.

## Platform acceptance exit criteria

A later Windows platform acceptance record should bind all evidence to one immutable source commit and one built artifact, and should at minimum record:

1. Windows edition/build and architecture;
2. `FortuneChart` application version and packaged `source_commit`;
3. ZIP SHA-256 and size matching the release manifest;
4. successful launch of the emitted `FortuneChart.exe` from the extracted portable bundle;
5. loopback-only health/startup behavior and browser/no-browser startup behavior;
6. one ordinary deterministic combined-chart smoke from the packaged binary;
7. verified updater activation using a manifest-bound newer test/release artifact, or an explicitly documented release-calibration equivalent;
8. rollback/recovery evidence for an induced or controlled activation failure where practical;
9. the final operator/platform acceptance disposition.

Until that evidence exists, Windows binary distribution remains pending even though deterministic product R1 is closed.

## Non-negotiable semantic boundaries

Product or platform work must not:

- select a winner among disputed candidate methods;
- infer `ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION` from geometry alone;
- unify Ziwei and Bazi day-boundary or calendar rules;
- add strength, favorable-element, auspiciousness, interpretation or prediction semantics;
- treat a commercial reference product as authority over the released deterministic source/profile contracts.

## Acceptance decision

No remaining deterministic/product blocker was identified in the audited tree. Field visibility, Workbench composition, desktop runtime boundaries, update integrity, packaging contracts, and release controls are sufficient to close the deterministic fusion-chart product R1 while preserving all explicit unresolved/candidate boundaries.

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
WINDOWS_BINARY_PLATFORM_ACCEPTANCE=PENDING_PLATFORM_ACCEPTANCE
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
DISPUTED_CANDIDATE_POLICY=NO_WINNER
```
