# Fortune V1 automation runtime

Repository-driven, answer-isolated orchestration for **紫微斗数＋四柱八字综合相对预测**. V1 automates deterministic ingest, immutable snapshots, run validation, group freeze/reveal ordering, literal answer replay, scoring, iterative reasoning correction, patch leak scanning, regression selection, state transitions, and audit reporting. It does not pretend that a CHAT continues reasoning after the response ends.

> **Current release boundary:** the R17 repository candidate has passed immutable source readback and one complete non-scoring repository-only shadow run. `CAUSAL_USE=PASS`, `NO_FALLBACK=PASS`, and `ANSWER_ISOLATION=PASS` for `RUN-R17-ENDPOINT-001`; no accuracy observation was created. R16 remains active until explicit user approval and compare-and-swap activation. `FORMAL_RELEASE=NO` and no predictive-improvement claim is made.

The frozen activation plan is `model/candidates/MODEL-R17-REPOSITORY-SHADOW-V1/promotion-plan.json`. It binds the current R16 knowledge, method, model, and runtime-config blob SHAs and will stop if any pointer moves before activation.

## Execution model

The prediction engine is the active ChatGPT project session in either:

- `CHAT_ONLY` — the normal and preferred operating mode;
- `WORK` — an optional higher-capacity interactive mode when available.

No OpenAI API key, separate model endpoint, paid server, or background process is required. GitHub does not start ChatGPT autonomously. The user starts a frozen training-group conversation, ChatGPT processes every answer-free case permitted by that group's contract with fresh per-case isolation, and the repository validates and freezes the resulting run objects.

Group size, case count, question count, training rounds, mastery threshold and regression scope are not fixed by the R17 runtime. They are determined by the frozen `GROUP_MANIFEST`, `RUN_CONTRACT` and `LEARNING_POLICY`.

## R17 candidate bindings

- Project prompt: `MP-PROFESSIONAL-REASONING-20260718-R17`
- Knowledge: `KNOWLEDGE-R17-PROMPT-CUTOVER-CANDIDATE-V2`
- Method: `METHOD-R17`
- Model: `MODEL-R17-REPOSITORY-SHADOW-V2`
- Runtime config candidate: `config/runtime-r17-candidate.json`

S00–S18 reuse exact immutable R16 parent files. S19 is reconstructed from a canonical gzip/base64 R17 control-root overlay plus immutable R16 S19 bytes. The materialized S19 SHA256 is `59a0c04a282125929317b7166f9137b440f1f6d239bf27aec5b740d20b5c6a91` and its size is `10283817` bytes.

## Shadow validation

`RUN-R17-ENDPOINT-001` validated the complete precontent and reasoning chain without a personal chart or answer key:

- frozen input, coverage plan, SOURCE_PACKET, METHOD_PACKET and RUN_CONTRACT before reasoning;
- two independent local seals;
- five evidence-ledger rows;
- twelve method-stage receipts;
- one required pairwise comparison;
- relative TOP1/TOP2 release with FORMAL exact assertion null;
- causal-use, no-fallback and answer-isolation PASS;
- ten runtime objects read back from GitHub with exact Git-blob matches;
- no score and no accuracy observation.

## Activation boundary

The active pointers still reference R16. R17 activation requires the exact approval phrase recorded in the promotion plan, PR history cleanup or an explicit exception, CAS updates for all three active pointers and `config/runtime.json`, post-activation readback, and an activation receipt.

After activation, the first real training group must create a fresh `GROUP_MANIFEST`, per-case input snapshots, SOURCE_PACKET, METHOD_PACKET and RUN_CONTRACT before any reasoning. Every scored case remains conditional on its own causal-use PASS.

## GitHub Actions incident

Recent GitHub Actions jobs still fail before recording executable steps, logs or artifacts. This remains classified as `PRESTEP_PLATFORM_OR_RUNNER_FAILURE_UNRESOLVED` and is not represented as test PASS or as a code assertion failure. The R17 source and shadow proofs instead use immutable Git blob readback and deterministic local reconstruction.

See [R17 cutover status](docs/r17-cutover-status.md), [operations](docs/operations.md), [architecture](docs/architecture.md), [external runner](docs/external-runner.md), [single-session group training](docs/group-training-single-session.md), and [learning cycle v2](docs/learning-cycle-v2.md).
