# Clean group start

A blind group session must begin from one generated `GROUP-CLEAN-START-V1` object. The model must not discover inputs or templates by searching repository history.

## Create the clean-start package

```bash
PYTHONPATH=src python scripts/create-group-clean-start.py create \
  --group-manifest training-data/DEV-GROUP-002/manifest.json \
  --install-state reports/install-state.json \
  --output-root data/group-clean-starts \
  --group-run-id <new-group-run-id> \
  --session-id <new-session-id> \
  --mode CHAT_ONLY
```

The command writes:

- `data/group-clean-starts/<group-run-id>/clean-start.json`;
- one empty `PREDICTION-RUN-V1` skeleton for every case;
- an exact-path allowlist;
- explicit forbidden path prefixes and resource types;
- null-output fail-closed rules for contamination.

The skeletons are transport templates only. Their status is `EMPTY_SKELETON_NOT_VALID_FOR_FREEZE`; TOP1, TOP2, local seals, evidence ledgers, coverage, direction matrices and pairwise decisions must be completed before normal prediction validation and group freeze.

## Model retrieval rule

After reading `clean-start.json`, the prediction session may fetch only paths listed under `retrieval_policy.exact_allowed_paths` plus the active S00–S19 source paths explicitly supplied by the clean-start launcher. It must not call repository search, list or inspect pull requests/issues/commits, or read prior runs, reveals, grades, diagnoses, relative replays or shadow rebuilds.

Historical score summaries and prior prediction metadata are forbidden even when they do not contain literal answer letters.

## Contamination

When forbidden material becomes visible before complete group freeze, write a receipt and stop:

```bash
PYTHONPATH=src python scripts/create-group-clean-start.py contaminate \
  --clean-start data/group-clean-starts/<group-run-id>/clean-start.json \
  --output data/group-clean-starts/<group-run-id>/contamination.json \
  --resource-type pull_request \
  --resource-reference <reference>
```

The receipt forces both prediction vectors to `null`, records `group_freeze=NOT_PERFORMED`, and requires a fresh conversation and new IDs.
