# Full training-pipeline audit

## Scope

- Repository: `chinaneedM/ziwei-bazi-model`
- Audited run: `GROUP-RUN-20260719T112500JST-3BBBF55AA880`
- Audit time: `2026-07-19T12:16:01+09:00`
- Result: `HOLD_END_TO_END_TRAINING_PIPELINE_INCOMPLETE`

This is an engineering audit. It is not a prediction, freeze, reveal, score, causal-use PASS, or training-success claim.

## Executive finding

The repository contains validated components for clean-start creation, preblind option isolation and dual-track release gating. It does not currently expose a complete connected path from a clean-start request through staged runtime-packet generation, official preblind seal submission, postblind option release, prediction freeze, group freeze, reveal and learning-cycle execution.

`INSTALLED_VALIDATED` therefore overstates the operational state. The installed receipt validates the staged-access components and three targeted unit tests, while explicitly recording GitHub Actions as a zero-step pre-execution platform failure. It does not contain an end-to-end group-training receipt.

## Blocking findings

### B1 — Current run was engineering-only manual materialization

`data/group-clean-starts/GROUP-RUN-20260719T112500JST-3BBBF55AA880/manual-materialization-receipt.json` states:

- `role=ENGINEERING_ONLY_NO_PREDICTION_PERMISSION`
- `future_prediction_context_started=false`
- formal release is forbidden until preblind packets and dual-track seals are completed.

The manual materialization copied only preblind inputs and chart sidecars. It did not produce the complete official staged runtime objects.

### B2 — Official preblind skeletons are missing

The required path family

`data/group-clean-starts/<GROUP_RUN_ID>/preblind-skeletons/<CASE_ID>.json`

is absent for the audited run. The clean-start hardening code normally creates `PREBLIND-PREDICTION-SKELETON-V1` objects with per-question Ziwei and Bazi seal slots.

### B3 — Staged runtime packets are missing

No runtime-packet request exists at:

`runtime/runtime-packet-requests/GROUP-RUN-20260719T112500JST-3BBBF55AA880.json`

Consequently the run has no official per-case:

- `preblind-source-packet.json`
- `method-packet.json`
- `run-contract.json`
- `stage-access-plan.json`
- group retrieval transport plan.

### B4 — Runtime-packet workflow is still wired to the legacy generator

`.github/workflows/repository-group-runtime-packets.yml` calls:

`python scripts/create-group-runtime-packets.py`

and expects `READY_FOR_BLIND_PREDICTION`.

The staged implementation introduced by the active install is:

`python scripts/create-staged-group-runtime-packets.py`

and should expect `READY_FOR_PREBLIND_MODELING`, PREBLIND transport status, withheld postblind paths and a required postblind receipt. The workflow was not rewired to the staged script.

### B5 — The validation request written under the run directory has no consumer

The file:

`data/group-clean-starts/<GROUP_RUN_ID>/preblind-submission/validation-request.json`

is not watched by any workflow. The clean-start workflow watches only `runtime/clean-start-requests/*.json`; the runtime-packet workflow watches only `runtime/runtime-packet-requests/*.json` and PR request paths. Therefore the request is inert.

### B6 — Custom preblind submission does not match the official release contract

The official release code requires, per case:

- `FORTUNE-STAGED-ACCESS-PLAN-V1`
- `PREBLIND-SEAL-BUNDLE-V1`
- seal bundle `status=PASS`
- `option_access_before_all_seals=false`
- every question `sealed_before_option_access=true`
- Ziwei and Bazi receipts each with `status=PASS`, `model_hash`, and `seal_hash`.

The manually written `GROUP-PREBLIND-SUBMISSION-V1` and case files use custom schemas and `SEALED_PENDING_R17_REPOSITORY_VALIDATOR`. They cannot be accepted by `release-postblind-stage.py`.

### B7 — Source-packet and provenance gates were not completed

The custom submission contains route templates with `source_body_use_status=NOT_YET_STARTED`, not actual `FORTUNE-PREBLIND-SOURCE-PACKET-V1` items. It therefore does not establish packet-item provenance, parent excerpts, evidence-usage ledger rows or downstream source effects required for formal causal-use validation.

### B8 — Existing clean-start shortcut can preserve an incomplete manual object

`.github/workflows/repository-group-clean-start.yml` checks whether `clean-start.json` already exists. If it exists, the workflow re-reads it instead of rebuilding or verifying all required staged child objects. An incomplete manually materialized clean start can therefore remain accepted at the top-level status check while required skeletons and stage plans are absent.

### B9 — Connector-authored writes do not provide a proven Actions trigger path

The current clean-start request and later validation writes produced no visible workflow runs or commit statuses. PR35 introduced a same-repository PR / `pull_request_target` fallback specifically because connector-authored push events may not start Actions. Equivalent fallback wiring is absent from the staged runtime-packet and postblind-release path.

### B10 — Training code exists, but is not connected to the staged prediction runtime

The repository contains learning-cycle specifications and CLI operations for create, evaluate and advance. Those operations require an immutable first-blind freeze and later reveal/evidence objects. The current staged runtime has no connected workflow that produces:

- official postblind prediction bundles;
- all-option pairwise adjudication objects;
- group prediction freeze and freeze receipt;
- controlled reveal;
- literal answer-vector replay;
- learning-cycle evidence and advancement.

## Current-run disposition

This audit required reading pull requests and commit history, which are forbidden resources for an active pre-freeze prediction context. The audited run has therefore been closed by:

`data/group-clean-starts/GROUP-RUN-20260719T112500JST-3BBBF55AA880/contamination-receipt.json`

with `status=FAIL_CLOSED_CONTAMINATED` and `restart_required=true`.

## Required remediation before a new formal run

1. Rewire `repository-group-runtime-packets.yml` to the staged runtime-packet script and PREBLIND assertions.
2. Add same-repository PR / `pull_request_target` fallback for runtime-packet requests.
3. Make clean-start existing-object handling validate all required child objects or fail closed; never silently accept an incomplete manual object.
4. Define and validate an official model-output path for `PREBLIND-SEAL-BUNDLE-V1` per case.
5. Add a repository workflow/request interface that validates all five seal bundles and runs `release-postblind-stage.py` without exposing answers.
6. Add the postblind prediction, case freeze, group freeze and freeze-receipt orchestration.
7. Add controlled reveal and literal answer-vector replay only after group freeze PASS.
8. Connect the frozen prediction/reveal outputs to the active learning-cycle engine.
9. Run one synthetic answer-free end-to-end integration test from clean request through group freeze, plus a separate synthetic reveal/training test.
10. Restore `INSTALLED_VALIDATED` only after an immutable end-to-end receipt proves the entire chain.

## Required next formal run

After remediation, start with a fresh group run ID in a fresh isolated conversation. The audited group run is non-reusable.
