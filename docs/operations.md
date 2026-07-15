# Operator manual

## 1. Bootstrap repositories

Run `scripts/create-repositories.sh OWNER` from an administrator workstation with `gh`. Provision two GitHub App installations or fine-grained tokens:

- prediction token: runtime repository only;
- grader token: runtime plus answer vault;
- administrator: both repositories.

Then export the two tokens only for a topology check and run:

```bash
fortune-v1 verify-topology --config config/github-topology.json --output reports/topology.json
```

## 2. Source and prompt baseline

Run `audit-sources`; inspect missing/duplicate/control-root/binding-table rows. Only a PASS report can feed `migrate-sources`. Tag the resulting commit. Export the live project instruction text through an approved operator path and run `prompt-snapshot`; keep its audit-only disclaimer.

## 3. Complete ZIP ingest

```bash
fortune-v1 ingest --package group.zip --runtime-root ./data/runtime \
  --vault-root /separate/fortune-answer-vault --dataset-type DEV
```

V1 accepts ZIP only. Paths, symlinks, encryption, duplicate member names, suspicious ratios and unclassified/ambiguous types fail or quarantine. The importer stores the ZIP and all members read-only in the vault. Runtime receives only purple-chart text, Bazi images, questions and optional notes.

## 4. Bazi freeze and snapshot

Create a transcription JSON conforming to `bazi-transcription.schema.json`; critical ambiguous/missing/conflicting fields quarantine that version. Freeze it, then generate the prediction snapshot. This V1 provides a deterministic transcription entry and verification boundary; it does not claim an OCR model is installed.

## 5. Static case cache

Supply a fully materialized Ziwei/Bazi static object and run `cache-freeze`. Required Ziwei and Bazi sections are checked. Cache keys include case input, active binding and Schema version.

## 6. Prediction and freeze

`prepare-run` writes the only contract visible to an external model runner. The runner must return a complete `PREDICTION-RUN-V1`. `freeze` verifies TOP1/TOP2, 3–5 distinct public evidence families, two independent parent-library chains, full evidence-ledger fields and all N×(N−1)/2 pairwise rows. An existing `RUN_ID` cannot be overwritten.

## 7. Reveal and score

Only the grader identity runs `grade`, with a valid freeze receipt. Prefer an answer JSON containing only `schema`, `answers`, and optional `authorized_run_id`. Literal replay uses two parsers, preserves the original string/codepoints/offsets, does no case conversion, and requires exact question count and legal option membership. TOP1 is formal; TOP2 is diagnostic.

## 8. Patch and regression

Run `scan-patch` before execution. A case ID, answer vector, option-memory phrase, unique literal/date/identity or missing universal source parent chain rejects the patch as `PATCH_REJECTED_CASE_SPECIFIC`. `regression-select` orders defect reproduction, affected failures, current group, related history, core history and optional full regression. `regress` holds if the external runner is absent and rejects any historical damage.

## 9. Installation receipt

Run `install-check` last. It does not modify S19. Only an all-PASS receipt emits an S19 status-update candidate. Missing source roots, topology, tests, commit or runner retains `SCHEMA_DEFINED_NOT_INSTALLED`.

