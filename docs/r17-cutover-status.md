# R17 prompt and repository cutover status

## Current result

The active ChatGPT project instruction is `MP-PROFESSIONAL-REASONING-20260718-R17`.

Canonical prompt fingerprint:

- SHA256: `e7e33e69fec7258b538eaf2698755f901b73933d67bcd86ca45e9bc2a66fce79`
- bytes: `11702`
- non-whitespace Unicode code points: `5253`

The repository candidate chain now contains:

- `KNOWLEDGE-R17-PROMPT-CUTOVER-CANDIDATE-V2`;
- `METHOD-R17`;
- `MODEL-R17-REPOSITORY-SHADOW-V2`;
- R17 runtime configuration candidate;
- a completed repository-only non-scoring shadow run.

## Source delivery

S00–S18 reuse exact immutable R16 parent files. S19 is reconstructed from a canonical gzip/base64 R17 control-root overlay plus the immutable R16 S19 file.

Materialized S19:

- SHA256: `59a0c04a282125929317b7166f9137b440f1f6d239bf27aec5b740d20b5c6a91`
- bytes: `10283817`

Remote Git blob verification passed for all 20 parent files and the canonical overlay container. The original plain-text overlay candidate remains retained as a failed audit object because of a trailing-LF byte mismatch; it is superseded by manifest V2.

## Shadow validation

Shadow run:

`RUN-R17-ENDPOINT-001`

Status:

```text
PASS_NONSCORING_REPOSITORY_ONLY_SHADOW
CAUSAL_USE=PASS
NO_FALLBACK=PASS
ANSWER_ISOLATION=PASS
ACCURACY_OBSERVATION_CREATED=NO
```

The run froze its input, coverage plan, SOURCE_PACKET, METHOD_PACKET and RUN_CONTRACT before reasoning. It then materialized two independent local seals, five evidence-ledger rows, twelve method-stage receipts, one required pairwise comparison and a null formal assertion. All ten runtime objects passed remote Git-blob readback.

## Activation boundary

The active repository pointers still reference R16:

- knowledge: `KNOWLEDGE-R16`;
- method: `METHOD-R16`;
- model: `MODEL-R16-REPOSITORY-SHADOW-V2`;
- runtime configuration: R16.

The frozen activation plan is:

`model/candidates/MODEL-R17-REPOSITORY-SHADOW-V1/promotion-plan.json`

It requires compare-and-swap checks against the current R16 pointer and configuration blobs, PR history cleanup, explicit user approval, post-update readback and an activation receipt.

Current state:

```text
ACTIVATION_STATUS=READY_NOT_EXECUTED_EXPLICIT_USER_APPROVAL_REQUIRED
FORMAL_RELEASE=NO
TRAINING_PERMISSION=BLOCKED_UNTIL_ACTIVATION_AND_FRESH_GROUP_CONTRACT
```

After activation, case count, question count and training thresholds are not fixed by this configuration. They are controlled by the frozen `GROUP_MANIFEST`, `RUN_CONTRACT` and `LEARNING_POLICY` for each training group.
