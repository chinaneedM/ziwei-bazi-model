# Fortune V1 automation runtime

Repository-driven, answer-isolated orchestration for **紫微斗数＋四柱八字综合相对预测**. V1 automates deterministic ingest, immutable snapshots, run validation, group freeze/reveal ordering, literal answer replay, scoring, iterative mastery learning, patch leak scanning, regression selection, state transitions, and audit reporting. It does not pretend that a CHAT continues reasoning after the response ends.

## Execution model

The prediction engine is the active ChatGPT project session in either:

- `CHAT_ONLY` — the normal and preferred operating mode;
- `WORK` — an optional higher-capacity interactive mode when available.

No OpenAI API key, separate model endpoint, paid server, or background process is required. GitHub does not start ChatGPT autonomously. The user starts one frozen training-group conversation, ChatGPT processes every answer-free case in that group with fresh per-case isolation, and the repository validates and freezes the resulting child `PREDICTION-RUN-V1` objects under one `GROUP-TRAINING-RUN-V1`.

`CHAT_STATELESS_COLD_START` applies between groups, not between cases within one group. The fixed development group may therefore run five cases and 25 questions continuously in one CHAT/WORK session without five new conversations or five separate continue commands.

## Mastery learning model

Revealed development examples are training material. They are not considered finished merely because an audit object or regression report exists.

The active learning sequence is:

> **汲取 → 拆解 → 填充 → 重塑 → 化用 → 生发**

The repository implements this as `LEARNING-CYCLE-V2`:

- `QUESTION` mode trains one question at a time;
- `CASE` mode trains one case at a time;
- `GROUP` mode trains a full development group.

The default QUESTION gate requires five clean cold-start attempts, TOP1 at least 80%, TOP2 at least 90%, full provenance/pairwise replay, and retention of every previously mastered unit. Low scores cause another learning round; they do not trigger an arbitrary retry-limit HOLD.

Training mastery, cold-start stability and unseen blind generalization are reported separately. See [learning-cycle-v2.md](docs/learning-cycle-v2.md).

## Installation state

The authoritative runtime state is the machine-generated `reports/install-state.json`, validated by `reports/install-state-validation.json` and bound to the versioned installation receipt. Installed components include:

- the S00–S19 source baseline and exact S19 binding-table recomputation;
- the R16 main-prompt audit snapshot, explicitly marked as an audit copy rather than runtime authority;
- the physically separate answer vault and reverse-grading workflows;
- bidirectional token-scope denial and absence of any vault credential in the runtime repository;
- static and synthetic validation;
- the `CHAT_WORK_INTERACTIVE_EXECUTOR` registration;
- the deterministic single-case `fortune-v1 chat-work-import` handoff adapter;
- the installed group commands `fortune-v1 group-chat-work-run` and `fortune-v1 group-verify-freeze`;
- the mastery command `fortune-learning-cycle`;
- complete-group freeze before any answer access;
- the answer-vault `grade-frozen-group` workflow for one-dispatch whole-group reveal and per-case literal grading.

The phrase `EXTERNAL_PREDICTION_RUNNER` in the installation schema refers to the **external-to-GitHub ChatGPT project session**, not to an API service. See [external-runner.md](docs/external-runner.md).

Transport suffixes such as `(8)`, `(9)` and `(59)` are never source identity. The importer reads the first active internal `LIBRARY_ID`, raw SHA256 and size, then selects only the version bound by the first current S19 table. Non-active byte versions are historical/quarantine records.

## Security boundary

```mermaid
flowchart TD
    ZIP["Complete ZIP"] --> IMP["Deterministic importer"]
    IMP --> V["Answer vault: raw + answers"]
    IMP --> N["Runtime: no-answer normalized group"]
    N --> S["Immutable prediction snapshots"]
    S --> C["One user-initiated CHAT_ONLY or WORK group session"]
    C --> H["Per-case CHAT/WORK validators"]
    H --> F["Complete group freeze receipt"]
    F --> G["Vault starts group grader"]
    G --> R["Runtime receives group reveal"]
    R --> L["Six-phase learning cycle"]
    L --> CR["Clean cold-start replay"]
    CR --> M["Mastery and retention gate"]
    M --> U["Frozen unseen blind test"]
```

The runtime repository has no vault credential and no workflow that checks out the vault. On GitHub Free private repositories, the answer vault manually dispatches reverse grading with `RUNTIME_REPO_TOKEN`, scoped only to the runtime repository. Paid branch/ruleset/environment protections are recorded as unavailable, never as PASS.

## Quick start

```bash
./scripts/install.sh
PYTHONPATH=src python -m fortune_v1.cli --help
fortune-learning-cycle --help
```

Import, normalize, audit and migrate the one source ZIP:

```bash
PYTHONPATH=src python -m fortune_v1.cli import-source-package \
  --package /path/to/fortune-source-baseline-S00-S19-R16.zip \
  --expected-zip-sha256 4bd8bf03cceeb2ca03d096fbebda9f4174f2e9f7879667bef228acd2770b09be \
  --config config/runtime.json \
  --work-root .source-import-work \
  --reports-dir reports \
  --migrate-destination knowledge/base
```

Run one complete answer-free training group in one active CHAT/WORK session:

```bash
fortune-v1 group-chat-work-run \
  --manifest data/group-submissions/<group-run-id>.json \
  --group-root data/dev-groups/<group-id> \
  --output-root data/group-runs \
  --mode CHAT_ONLY \
  --session-id <session-id> \
  --group-run-id <new-group-run-id>
```

See [operations.md](docs/operations.md), [architecture.md](docs/architecture.md), [external-runner.md](docs/external-runner.md), [group-training-single-session.md](docs/group-training-single-session.md), and [learning-cycle-v2.md](docs/learning-cycle-v2.md).

## Immutable object layers

1. `RAW_PACKAGE` — vault-only original ZIP and members.
2. `NORMALIZED_CASE` — deterministic classification result; runtime copy omits answer details.
3. `PREDICTION_INPUT_SNAPSHOT` — the only case object visible to prediction.
4. `PREDICTION_RUN` — TOP1/TOP2, two local seals, coverage, evidence ledger, direction matrix and all pairwise rows.
5. `GROUP_PREDICTION_FREEZE` — every expected child run and hash, complete before any answer reveal.
6. `REVEAL_AND_DIAGNOSIS` — literal replay and TOP1 scoring; never overwrites the run.
7. `LEARNING_CYCLE` — append-only six-phase diagnosis, candidate, clean replay, mastery and retention objects.
8. `PATCH_AND_REGRESSION` — candidate patch, leak scan, mastery metrics and regression decision.
9. `UNSEEN_BLIND_TEST` — frozen evaluation performed only after training mastery.

Every rerun requires a new `GROUP_RUN_ID` and new child `RUN_ID` values; existing run paths are rejected.

The answer-vault initialization template is under `templates/answer-vault/`. Its generated ZIP is an installation package only; it contains no real answers, real examples, token value, prior prediction or SHADOW_REBUILD payload.
