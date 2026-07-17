# Group training state machine

```text
DEFINED
→ INPUT_FROZEN
→ CASES_IN_PROGRESS
→ CASES_COMPLETE
→ GROUP_FROZEN
→ REVEALED
→ DIAGNOSED
→ PATCH_PROPOSED
→ CLEAN_RERUN_COMPLETE
→ REGRESSION_COMPARED
→ ACCEPTED | ROLLED_BACK
```

## Transition rules

- `INPUT_FROZEN` requires the ordered answer-free group manifest and all case snapshot hashes.
- `CASES_IN_PROGRESS` may advance case by case inside one CHAT/WORK session, but every case starts with a fresh whitelist.
- `CASES_COMPLETE` requires one immutable prediction child for every expected case.
- `GROUP_FROZEN` requires all child validation and freeze receipts. No partial authorization exists.
- `REVEALED` requires a group-bound answer payload and two-path literal replay for every case.
- `DIAGNOSED` must distinguish original prediction accuracy, method validity, shadow rebuild, and reproducible interface defects.
- `PATCH_PROPOSED` may contain only general reproducible interface repairs.
- `CLEAN_RERUN_COMPLETE` requires new group/case run IDs and answer-free contexts.
- `REGRESSION_COMPARED` evaluates the configured group policy without rewriting old selections.
- `ACCEPTED` installs the candidate only after validation; `ROLLED_BACK` preserves the previous authoritative commit.

Any failed prerequisite moves the affected run to `FAIL_CLOSED`; it may not skip forward to reveal, scoring, acceptance, or release.
