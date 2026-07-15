# V1 architecture and trust model

## Repositories

| Repository | Contents | Prediction identity | Grader identity |
| --- | --- | --- | --- |
| `fortune-runtime` | Source baseline, prompt audit snapshot, no-answer cases, code, run packages, patches and reports | Read source/input; write new run artifacts | Read frozen runs; write reveals/reports |
| `fortune-answer-vault` | Original ZIP, every original member, answers, authorization and private reveal input | **No access** | Read only after freeze authorization |

`config/github-topology.json` is the desired state. `verify-topology` uses two separately supplied tokens to prove that the prediction identity receives 403/404 from the vault while the grader can read both private repositories. Tokens are never written to reports.

## Runtime bindings

A run contract binds four independent coordinates:

- `CASE_INPUT_HASH`
- `ACTIVE_LIBRARY_BINDING_HASH`
- `MAIN_PROMPT_RUNTIME_ID` plus an optional non-authoritative snapshot hash
- immutable code commit and Schema version

The static-cache key is exactly the hash of case input hash, binding hash and Schema version. A changed input, source binding or Schema cannot reuse an older cache.

## Prompt snapshot

The project custom instruction is runtime authority. `prompt-snapshot` copies an explicitly exported text file and records `AUDIT_COPY_ONLY_NOT_RUNTIME_AUTHORITY`. Installation also needs a runtime attestation or external comparison procedure; repository presence alone never proves the project is executing that snapshot.

## Knowledge index

The locator index covers S01–S18. S00 routes and S19 governs, so neither is indexed as fortune knowledge. Every locator retains the complete source hash and Git commit, exact byte/line range, root atom, parent-segment hash and detected condition/negation/limitation/exception/alternative clauses. `source-read` reopens the full source, verifies its hash, and returns exact bytes. Index text never substitutes for source text.

## Dataset separation

DEV permits reveal, diagnosis and repeated regression. REGRESSION detects damage. FROZEN_EVAL uses a separate state machine and frozen binding. Release promotion is a third state machine: CANDIDATE → DEV_PASS → REGRESSION_PASS → FROZEN_EVAL_PASS → RELEASED. No state name from one machine is accepted as another machine's state.

