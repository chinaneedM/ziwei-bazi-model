# Combined Workbench Real-Machine Calibration R1

## 1. Purpose

This runbook is the operator-facing acceptance procedure for the released local Ziwei + Bazi workbench.

It covers packaging, composition, loopback startup and browser interaction only. It does **not** perform prediction, interpretation, scoring, training, source mutation or model-learning updates.

The daily-use entry point is:

```text
fortune-chart-app
```

The package binding is defined in `pyproject.toml` as:

```text
fortune-chart-app = fortune_training.combined_chart_application.workbench_local_app:main
```

The default local address is:

```text
http://127.0.0.1:8767/
```

Health endpoint:

```text
GET http://127.0.0.1:8767/health
```

The server is loopback-only. Offline location lookup is part of the released local application; this calibration workflow does not require public geocoding, GitHub credentials or external web access.

## 2. Install / update the local package

From the current Git checkout:

```bash
python -m pip install -e .
```

Before real-machine calibration, verify repository integrity:

```bash
fortune-train verify
```

`fortune-train verify` is a read-only/preflight verification command in this workflow. Do not run training start, scoring, learning, maintenance or state-advance commands as part of workbench calibration.

## 3. Command-level smoke

Run:

```bash
python scripts/combined-workbench-smoke.py
```

Optional explicit repository root:

```bash
python scripts/combined-workbench-smoke.py --repository-root /path/to/ziwei-bazi-model
```

The smoke harness constructs the released `CombinedChartWorkbenchApplication` and exercises only its released application boundaries. It checks all of the following with one deterministic fixture:

1. workbench health / loopback policy;
2. combined base Ziwei + Bazi resolution;
3. Ziwei Sanhe interaction resolution;
4. Bazi explicit target-flow resolution;
5. Shared Target → Ziwei selector projection;
6. source manifest / Ziwei bundle / Bazi bundle / target-coordinate hash agreement across the composed surfaces.

A successful run exits `0` and prints one JSON receipt with:

- `status = PASS`;
- Combined manifest hash;
- Ziwei and Bazi bundle hashes;
- Ziwei interaction bundle hash;
- Bazi target-flow bundle hash;
- target-coordinate FactHash;
- shared projection FactHash;
- Bazi target-flow and shared-projection candidate counts.

The smoke harness does not choose a prediction, interpret a chart, mutate training state, or contact an external service. A mismatch exits nonzero with a compact `FAIL` diagnostic.

## 4. Launch the daily-use browser workbench

Normal launch, opening the default browser:

```bash
fortune-chart-app
```

Launch without opening a browser automatically:

```bash
fortune-chart-app --no-browser
```

Use another loopback port when `8767` is already occupied:

```bash
fortune-chart-app --port 8877
```

Then open the printed `http://127.0.0.1:<port>/` URL manually.

Stop the server with `Ctrl+C` in the terminal that launched it.

## 5. Five distinct application actions

The workbench intentionally keeps these actions separate.

### A. Combined base chart

`联合排盘` resolves the shared birth input into independent Ziwei and Bazi application bundles and displays both surfaces.

This is the source identity for later sidecars. Editing source birth/profile fields makes previously displayed sidecar results stale until the base chart is resolved again.

### B. Ziwei Sanhe interaction

The Ziwei interaction pane exposes:

- Daxian selector;
- Annual selector;
- Minor-limit selector;
- palace-origin / 立太极 click interaction;
- 12 rotated relative palace roles;
- exact released Sanfang/Sizheng SELF / +4 trine / +6 opposition / +8 trine highlight.

These interactions change the Ziwei application/interation view; they do not rewrite Bazi target input.

### C. Bazi explicit target-flow

The Bazi target-flow pane uses an explicit target local datetime/place/coordinates/timezone/precision input.

Resolving target-flow preserves released candidate lineage. A fold or uncertainty window may therefore expose more than one candidate. No visible-equality deduplication or candidate-0 winner is implied.

### D. Shared Target projection calculation

`计算共享 Projection` consumes the released target-coordinate candidates and the released Ziwei application bundle to calculate candidate-preserving Ziwei selector projections.

The selected target candidate's Daxian, Annual, and regular-Month layers are shown as read-only source projections. Each line exposes the source stem, parent frame, four transformations, independent 禄存／擎羊／陀罗 instances, temporal rule identity, and layer FactHash. A pre-Daxian target has no fabricated Daxian layer; a leap-month target has no fabricated regular-Month layer.

**Calculation alone does not change Ziwei Daxian / Annual / Minor selectors.** It also does not change the regular-Lunar-Month selector.

When more than one projection candidate exists, each lineage remains separately selectable even when visible Ziwei selector values happen to be identical.

### E. Explicit Apply to Ziwei

Only the explicit `应用目标时间到紫微` action may apply one selected server-returned projection candidate to the Ziwei Daxian / Annual / regular-Lunar-Month / Minor selectors. A projected leap month leaves the regular-month selector empty and visibly unresolved.

Apply is one-way and opt-in:

- it does not rewrite target fields;
- it does not rewrite Bazi target-flow output;
- later manual Ziwei navigation does not rewrite target fields;
- it reuses the existing Ziwei interaction refresh path rather than running a second temporal algorithm in the browser.

## 6. Browser real-machine acceptance checklist

After the command-level smoke passes, perform this short visual/interaction check in the actual browser.

### Base composition

- [ ] `fortune-chart-app` starts and opens/binds only to `127.0.0.1`.
- [ ] `/health` returns `status: ok` and loopback-only policy.
- [ ] An ordinary exact birth input resolves both the Ziwei and Bazi panes.
- [ ] No prediction/interpretation text is produced by the workbench.

### Ziwei Sanhe interaction

- [ ] Changing Daxian updates the Ziwei interaction view without relocating natal physical placements.
- [ ] Changing Annual updates the Ziwei interaction view.
- [ ] Changing regular Lunar Month updates the Ziwei interaction view.
- [ ] Changing Minor-limit updates the Ziwei interaction view.
- [ ] Clicking a natal palace changes the current palace-origin / 立太极.
- [ ] The highlighted Sanfang/Sizheng set contains SELF, two trines and one opposition at the released +0/+4/+8/+6 geometry.
- [ ] The 12 rotated relative-role labels change with the selected origin.

### Bazi explicit target-flow

- [ ] Target-flow cannot be resolved from an old/stale base after source birth fields are edited.
- [ ] Explicit target datetime/place/coordinates/timezone are shown as a separate target input from birth input.
- [ ] An ordinary exact target produces at least one Bazi flow candidate with both Xiaoyun candidates, Daily/Hourly frames, and lineage/hash display.
- [ ] Every resolved Bazi temporal layer shows read-only Ten God, hidden-stem Ten Gods, Nayin, Xunkong, day-master Twelve Growth, self Twelve Growth and an annotation FactHash; both Xiaoyun candidates remain separate.
- [ ] If a fold/uncertainty fixture produces multiple candidates, the candidate selector preserves them individually.

### Shared projection and Apply

- [ ] Clicking `计算共享 Projection` does **not** change Ziwei Daxian / Annual / regular-Lunar-Month / Minor selectors.
- [ ] A one-candidate projection may be preselected, but Ziwei still does not change until Apply is clicked.
- [ ] A multi-candidate projection requires explicit candidate selection; candidate 0 is not auto-applied.
- [ ] Clicking `应用目标时间到紫微` changes exactly the server-returned Ziwei Daxian / Annual / regular-Lunar-Month / Minor selectors and refreshes the existing Ziwei interaction view.
- [ ] A leap-month target does not fabricate or apply a regular Ziwei monthly frame.
- [ ] Daxian / Annual / regular-Month read-only lines expose separate source stems, parent frames, four transformations, 禄羊陀／流昌曲 instances, unselected strict/compatibility 流魁钺 candidates, rule identities and 64-character hashes.
- [ ] Same-named transformations and auxiliaries in different layers remain separate instances rather than collapsing into one display fact.
- [ ] Apply does not change target datetime/place/coordinates/timezone, Bazi profile fields, or Bazi target-flow result.
- [ ] Manual Ziwei navigation after Apply does not rewrite target fields.
- [ ] Editing any birth/source input invalidates stale target-flow/projection eligibility.
- [ ] Editing any target input invalidates stale projection eligibility.

## 7. Suggested ambiguity fixture

For a visual candidate-preservation check, use a target timezone/date that has a legal civil fold or use a small explicit uncertainty interval that crosses a meaningful boundary. Do not invent expected astrological results in this runbook.

The acceptance target is the **behavioral contract**:

- multiple legal upstream candidates remain multiple downstream candidates;
- the browser does not silently choose a winner;
- Apply remains explicit.

The automated test suite already contains exact DST-fold and Dec-31/Jan-1 discrimination fixtures. The operator does not need to recreate every boundary manually on every launch.

## 8. Recording a real-machine discrepancy

If the browser result disagrees with an external reference application or behaves unexpectedly, record the smallest reproducible packet:

- current Git `main` commit;
- OS / Python / browser version;
- exact birth input and selected profiles;
- exact target input when target-flow/shared projection is involved;
- action sequence;
- observed output/status text;
- screenshot when the discrepancy is visual;
- smoke receipt when available.

Open a new narrow calibration issue for that discrepancy. Do not change canonical sources, model-learning, training state or unrelated engine semantics merely because a visual/reference difference was observed.

## 9. Release boundary

This calibration runbook treats the current released workbench as a deterministic application composition:

```text
Birth Input
  -> Combined base Ziwei + Bazi bundles
  -> Ziwei Sanhe interaction sidecar
  -> Bazi explicit Target-Flow sidecar
  -> Shared Target -> Ziwei selector projection
  -> explicit user Apply to Ziwei selectors
```

It is not a Ziwei+Bazi prediction/synthesis engine. Cross-system interpretation, winner selection and prediction remain outside this R1 workbench calibration contract.
