# V1 architecture and trust model

## Source identity and immutable baseline

Attachment display names and suffix numbers are transport metadata only. The source importer preserves the uploaded ZIP read-only, safely extracts raw members, reads the first active internal `LIBRARY_ID`, computes raw SHA256 and byte size, resolves the unique current S19 control root, and parses the first current S00–S18 binding table. Only an exact `LIBRARY_ID + SHA256 + SIZE + S19 row` match is copied to clean staging under the S19 canonical filename.

Identical-byte duplicates are deduplicated with provenance retained. Different-byte versions go to historical audit/quarantine; no S19 match fails closed. Audit PASS is required before migration, baseline commit/tag, index construction, or any installed-status candidate. The derived locator index covers S01–S18 only and always reopens the bound parent file and exact byte range.

## GitHub Free reverse grading

| Property | Recorded state |
| --- | --- |
| Plan | `FREE_PRIVATE_OWNER_CONTROL` |
| Topology | `ANSWER_VAULT_INITIATED_REVERSE_GRADING` |
| Runtime vault credential | `NONE` |
| Vault runtime credential | `RUNTIME_REPO_TOKEN` |
| Branch protection | `NOT_AVAILABLE_ON_CURRENT_PLAN` |
| Ruleset enforcement | `NOT_AVAILABLE_ON_CURRENT_PLAN` |
| Environment protection | `NOT_AVAILABLE_ON_CURRENT_PLAN` |
| Trigger | Owner manual `workflow_dispatch` |

The runtime repository contains no vault checkout workflow. The answer vault first checks out the runtime, validates `data/runs/<run_id>/freeze-receipt.json` and its bound prediction/contract hashes, and only then checks out the current vault. Grading creates exactly `data/reveals/<run_id>.json`, rejects overwrite, removes the vault worktree and caches, verifies the staged path allowlist, then writes the reveal to runtime.

Machine topology verification is componentized: physical repository separation, token repository scope, runtime-vault access denial, grading direction, and Free-plan limitation recording. An owner assertion is not a machine PASS; the answer-vault workflow and HTTP scope probes must be read back.

## Runtime bindings and external runner

A run contract binds `CASE_INPUT_HASH`, active source binding hash, main-prompt runtime ID/audit hash, Schema version and immutable code commit. The project custom instruction remains runtime authority; a repository prompt export is only `AUDIT_COPY_ONLY_NOT_RUNTIME_AUTHORITY`.

The deterministic importer, validator, freezer, grader and regression engine are not the prediction model. `config/external-runner.json` must register a real dual-track executor with `PREDICTION-RUN-V1` output, no-answer proof, prompt/source/code bindings, timeout, failure state, RUN_ID non-overwrite and independent Ziwei/Bazi local seals. Until then its status is `NOT_INSTALLED`.
