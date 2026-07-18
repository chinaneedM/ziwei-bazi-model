# CHAT/WORK prediction runner

## Execution model

The reasoning engine is an active ChatGPT project session operating in `CHAT_ONLY` or `WORK` mode. GitHub does not autonomously start ChatGPT, and no background model process is claimed.

The runtime now has two explicitly different handoff classes:

1. **Repository-bound shadow/scored contract** — uses `REPOSITORY-PREDICTION-RUN-CONTRACT-V1`, a frozen `MODEL_RELEASE`, `FORTUNE-SOURCE-PACKET-V1`, and `FORTUNE-METHOD-PACKET-V1`. The causal-use validator must pass before a run can be score-eligible.
2. **Legacy post-reasoning contract** — may still be archived and frozen for compatibility, but it is permanently `LEGACY_UNSCORED` because it cannot prove that repository source text or the versioned method was delivered before reasoning.

The current formal release remains `NO`, and repository-only R16 shadow validation has not yet been completed.

## Authority boundary

- GitHub repository releases are the only mutable knowledge and method authority.
- The original R16 S00–S19 set remains immutable under `knowledge/base`.
- `knowledge/active-release.json` and `method/active-release.json` identify the shadow-bound versions.
- Project-uploaded S00–S19 files remain in the old project as read-only bootstrap/archive copies. They must not be mixed with repository packets and must not be used by a repository-bound scored run.
- A repository checkout failure, packet failure, hash mismatch, missing route, missing method stage, causal-use failure, or contamination failure must fail closed. There is no fallback to project files.

## Legacy contamination quarantine

Historical files are not silently erased. They remain available for audit, defect reproduction and research, but they are not runtime knowledge or method inputs.

The following references are prohibited in source packets, method packets, predictions and scored run contracts:

- `/mnt/data`, opaque project file IDs and project-upload labels;
- answer-vault or ground-truth paths;
- `SHADOW_REBUILD` paths;
- post-reveal or revealed-case objects;
- any `reports/` path, including historical training-regression and example reports;
- `data/training/` state objects;
- `research/fortune-hypothesis-library/` objects unless the knowledge has been independently promoted into a versioned, hash-bound knowledge release.

The active eligible roots are limited to versioned `knowledge`, `method` and `model` base/candidate/release paths. A selected parent passage containing a prohibited path reference is rejected before packet creation. A later runtime reference to one of these paths makes the causal-use receipt `FAIL_CLOSED` and the run permanently unscored.

The governing object is `governance/runtime-contamination-policy-v1.json`.

## Pre-reasoning delivery chain

Before reasoning, the runtime must create and freeze:

1. an answer-isolated case and literal question/option freeze;
2. a complete knowledge-coverage plan;
3. a source catalog derived from the exact 20-file release manifest;
4. a source packet containing exact parent passages, byte ranges, conditions, negations, limitations, exceptions, alternatives, counterexamples, capability ceilings, and source hashes for all required routes;
5. a method packet containing every mandatory stage and stable rule ID;
6. a `MODEL_RELEASE` binding main prompt ID, knowledge release, method release, code commit, S19 binding hash, 20 source hashes and sizes, and source-packet protocol;
7. the complete repository prediction run contract;
8. a cleanroom declaration denying project uploads, historical training traces, post-reveal material and direct research-hypothesis access.

The source-packet builder rejects answer fields and temporary-winner fields. It may not stop after three public evidence items and may not select only material supporting a provisional winner.

## Causal-use validation

Every evidence-ledger row must resolve to one source-packet item and match its library, source-file SHA256, and source-root atom. Every mandatory prediction stage must have a method-stage receipt bound to one or more rule IDs from the method packet.

The validator also checks:

- exact model, knowledge, method, source-packet and method-packet bindings;
- packet and contract hashes;
- project-upload references such as `/mnt/data`, opaque project file IDs, or project-upload labels;
- historical report, training-state, post-reveal, SHADOW_REBUILD and direct research-hypothesis references;
- explicit no-fallback policy;
- answer isolation;
- frozen-before-reasoning status.

Only `FORTUNE-CAUSAL-USE-RECEIPT-V1` with `status=PASS` permits `score_eligibility=ELIGIBLE`. Interface installation, static tests, audit success, quarantine success, or a matching final answer do not substitute for causal proof or predictive accuracy.

## Commands

The repository delivery interface is exposed through:

```bash
fortune-repository-delivery knowledge-validate ...
fortune-repository-delivery method-validate ...
fortune-repository-delivery source-catalog ...
fortune-repository-delivery source-packet ...
fortune-repository-delivery method-packet ...
fortune-repository-delivery model-release ...
fortune-repository-delivery run-contract ...
fortune-repository-delivery causal-validate ...
fortune-repository-delivery contamination-inventory ...
fortune-repository-delivery contamination-validate ...
```

The existing single-case handoff remains:

```bash
fortune-v1 chat-work-import \
  --run data/chat-work-submissions/<run-id>.json \
  --contract data/contracts/<run-id>.json \
  --mode CHAT_ONLY \
  --session-id <non-secret-session-label> \
  --output data/chat-work-imports/<run-id>/prediction-run.json \
  --receipt data/chat-work-imports/<run-id>/handoff-receipt.json
```

For repository-bound contracts, this adapter now runs both the existing prediction-object validator and the causal-use validator. For legacy contracts it writes `score_eligibility=PROHIBITED`.

## Group-level handoff

The group adapter still requires the exact group order, complete case count, unique non-overwriting run IDs, common session identity, answer-free contracts, frozen group bindings and absence of cross-case reveal/diagnosis/shadow references. Repository-bound group scoring additionally requires a causal-use PASS for every child run.

No answer reveal or training score may be authorized until the full group freeze and every required causal-use receipt pass.

## Installation meaning

The repository delivery code, schemas and compatibility adapter are installed on the development branch. This means C01–C05 plus the C05A contamination quarantine interfaces exist; it does **not** mean:

- GitHub can run ChatGPT in the background;
- R16 repository source delivery has completed a real shadow run;
- prediction accuracy improved;
- the 25-question clean retest may begin;
- a formal release exists.
