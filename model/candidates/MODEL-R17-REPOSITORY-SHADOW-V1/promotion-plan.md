# R17 activation plan

Status: `READY_NOT_EXECUTED_EXPLICIT_USER_APPROVAL_REQUIRED`

No active pointer or runtime configuration is changed by this document.

## Verified candidate chain

- Project instruction: `MP-PROFESSIONAL-REASONING-20260718-R17`
- Knowledge: `KNOWLEDGE-R17-PROMPT-CUTOVER-CANDIDATE-V2`
- Method: `METHOD-R17`
- Model: `MODEL-R17-REPOSITORY-SHADOW-V2`
- Runtime configuration: `config/runtime-r17-candidate.json`
- Shadow run: `RUN-R17-ENDPOINT-001`

The shadow run passed causal-use, no-fallback and answer-isolation validation. It did not use an answer key and did not create an accuracy observation.

## Current active state

The repository still points to R16. Activation uses compare-and-swap checks against the exact current Git blobs for:

- `knowledge/active-release.json`
- `method/active-release.json`
- `model/active-release.json`
- `config/runtime.json`

If any expected blob or release ID changes before activation, the operation stops without updating any pointer.

## Required approval

The exact approval phrase recorded in the machine plan is:

`批准晋升R17并执行活动指针CAS更新`

After approval, execution must re-read the four current objects, clean or explicitly exempt the PR history, merge the approved candidate commit, update all pointers/configuration by CAS, read them back, and create an activation receipt. A partial failure requires rollback to the recorded R16 state.

## Training boundary

Activation does not make past shadow results scoreable. The first real training group must create a new frozen group manifest, new per-case snapshots, new source and method packets, and new run contracts before reasoning. Each scored case remains conditional on its own causal-use PASS.
