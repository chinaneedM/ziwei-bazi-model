# Fortune V1 automation runtime

Repository-driven, answer-isolated orchestration for **紫微斗数＋四柱八字综合相对预测**. V1 automates deterministic ingest, immutable snapshots, run validation, group freeze/reveal ordering, literal answer replay, scoring, iterative reasoning correction, patch leak scanning, regression selection, state transitions, and audit reporting. It does not pretend that a CHAT continues reasoning after the response ends.

> **Current release boundary:** R25 C01–C05A interfaces and the R17 cutover candidate are installed on the development branch only. The active ChatGPT project instruction is `MP-PROFESSIONAL-REASONING-20260718-R17`; its user-confirmed canonical UTF-8/LF snapshot is bound under `model/candidates/MODEL-R17-REPOSITORY-SHADOW-V1`. `METHOD-R17` and `KNOWLEDGE-R17-PROMPT-CUTOVER-CANDIDATE` now exist as non-promoted candidates. The knowledge candidate uses content-addressed R16 parent reuse plus an S19 byte-prepend overlay and has passed full local 20-file materialization. Remote immutable-checkout readback, MODEL-R17 construction, one repository-only non-scoring shadow run, causal-use PASS, no-fallback PASS and explicit promotion approval remain required. `FORMAL_RELEASE=NO`; no predictive improvement is claimed.

Audit dependencies are one-way. Historical R16 objects remain immutable; R17 candidates point to their exact parents and never overwrite them.

## Execution model

The prediction engine is the active ChatGPT project session in either:

- `CHAT_ONLY` — the normal and preferred operating mode;
- `WORK` — an optional higher-capacity interactive mode when available.

No OpenAI API key, separate model endpoint, paid server, or background process is required. GitHub does not start ChatGPT autonomously. The user starts a session; validated repository objects provide knowledge, method, contracts, state and receipts; the current ChatGPT conversation performs reasoning.

A formal prediction may start only after the exact MODEL_RELEASE, RUN_CONTRACT, SOURCE_PACKET, METHOD_PACKET, frozen input and answer-isolation objects are available before reasoning. Missing or mismatched objects fail closed without project-upload fallback.

## R17 prompt and knowledge cutover

The R17 prompt is method-decoupled: stable gates remain in the project instruction, while variable knowledge and procedure come from the bound repository releases and packets.

Current candidate objects:

- prompt snapshot: `model/candidates/MODEL-R17-REPOSITORY-SHADOW-V1/main-prompt.txt`;
- prompt receipt: `model/candidates/MODEL-R17-REPOSITORY-SHADOW-V1/prompt-snapshot.json`;
- method candidate: `method/candidates/METHOD-R17/method-release.json`;
- knowledge candidate: `knowledge/candidates/KNOWLEDGE-R17-PROMPT-CUTOVER-CANDIDATE/release-manifest.json`;
- S19 overlay: `knowledge/candidates/KNOWLEDGE-R17-PROMPT-CUTOVER-CANDIDATE/S19-R17-control-root-overlay.txt`.

The knowledge candidate does not duplicate roughly 178 MB of unchanged source bytes. S00–S18 reuse exact content-addressed R16 parent files. S19 is deterministically materialized as:

```text
R17_S19 = R17_CONTROL_ROOT_OVERLAY_BYTES + R16_S19_BYTES
```

Expected materialized S19:

```text
SHA256=59a0c04a282125929317b7166f9137b440f1f6d239bf27aec5b740d20b5c6a91
BYTES=10283817
```

Materialize and verify the complete 20-file candidate before source-catalog construction:

```bash
fortune-repository-delivery knowledge-materialize \
  --manifest knowledge/candidates/KNOWLEDGE-R17-PROMPT-CUTOVER-CANDIDATE/release-manifest.json \
  --repository-root . \
  --output-dir knowledge/candidates/KNOWLEDGE-R17-PROMPT-CUTOVER-MATERIALIZED \
  --receipt knowledge/candidates/KNOWLEDGE-R17-PROMPT-CUTOVER-MATERIALIZED/materialization-receipt.json
```

Any missing parent, changed overlay, unsupported composition mode, or final hash/size mismatch fails closed.

## Learning and scoring model

Revealed development examples are training material. An incorrect answer is used to diagnose and correct the reasoning path; it is never erased or converted into a retrospective blind success.

The active sequence is:

> **汲取 → 拆解 → 填充 → 重塑 → 化用 → 生发**

Core rules:

- each distinct question contributes at most one blind accuracy observation: its immutable first prediction before reveal;
- post-reveal replay measures training fit and execution stability only;
- repeating a revealed question cannot improve blind accuracy;
- TOP2 is diagnostic and does not replace TOP1 scoring;
- unseen generalization requires a later frozen set not used to revise knowledge or method;
- historical reports, revealed traces, `SHADOW_REBUILD`, training state and unpromoted hypotheses are not active prediction sources.

## Security boundary

The runtime repository has no answer-vault credential. Repository-bound source packets or predictions referencing project uploads, answer-vault paths, historical `reports/`, `data/training/`, post-reveal objects, `SHADOW_REBUILD`, or unpromoted research hypotheses fail closed and are score-ineligible.

Transport suffixes such as `(8)`, `(9)` and `(59)` are not source identity. Library ID, exact SHA256, byte size, immutable repository binding and manifest membership determine identity.

## Current status

```text
CUTOVER_STATUS=HOLD_PENDING_REMOTE_IMMUTABLE_READBACK_MODEL_R17_AND_CAUSAL_SHADOW
FORMAL_RELEASE=NO
SCORE_ELIGIBILITY=PROHIBITED
```

Local isolated validation completed:

- repository delivery, contamination and prompt binding: 7 tests PASS;
- R17 prompt/S19 cutover: 3 tests PASS;
- composite materialization and tamper rejection: 2 tests PASS;
- complete local R17 source materialization: 20/20 files PASS.

GitHub Actions currently fail before recording any job steps, logs or artifacts. Full CI is therefore unconfirmed rather than reported as a code-test failure or PASS.

## Quick start

```bash
./scripts/install.sh
PYTHONPATH=src python -m fortune_v1.cli --help
fortune-learning-cycle --help
fortune-repository-delivery --help
```

Formal group execution remains blocked until the R17 model and causal-use gates pass.

See `docs/operations.md`, `docs/architecture.md`, `docs/external-runner.md`, `docs/group-training-single-session.md`, and `docs/learning-cycle-v2.md`.
