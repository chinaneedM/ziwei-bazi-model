# R17 prompt and repository cutover status

## Active result

R17 was activated after explicit user approval and compare-and-swap readback.

```text
MAIN_PROMPT_RUNTIME_ID=MP-PROFESSIONAL-REASONING-20260718-R17
ACTIVATION_STATUS=PASS
FORMAL_RELEASE=YES
TRAINING_PERMISSION=YES_WITH_FRESH_GROUP_MANIFEST_SOURCE_PACKET_METHOD_PACKET_AND_PER_CASE_CAUSAL_PASS
```

Canonical prompt fingerprint:

- SHA256: `e7e33e69fec7258b538eaf2698755f901b73933d67bcd86ca45e9bc2a66fce79`
- bytes: `11702`
- non-whitespace Unicode code points: `5253`

## Active repository bindings

- knowledge: `KNOWLEDGE-R17`
- method: `METHOD-R17`
- model: `MODEL-R17-REPOSITORY-ACTIVE-V1`
- runtime configuration: `FORTUNE-RUNTIME-R17-ACTIVE-V1`

The active pointers and runtime configuration were updated by compare-and-swap and read back successfully. The activation receipt is:

`model/releases/MODEL-R17-REPOSITORY-ACTIVE-V1/activation-receipt.json`

Receipt object hash:

`124b1df97f1e0100e3ee10726cd5daaa06d4a4db486f7a523ba108cb441d4a4b`

## Source delivery

S00–S18 reuse exact immutable R16 parent files. S19 is reconstructed from the canonical R17 gzip/base64 control-root overlay plus immutable R16 S19.

Materialized S19:

- SHA256: `59a0c04a282125929317b7166f9137b440f1f6d239bf27aec5b740d20b5c6a91`
- bytes: `10283817`

Remote Git-blob verification passed for all source parents and the canonical overlay container.

## Validation boundary

The non-scoring repository-only shadow run `RUN-R17-ENDPOINT-001` passed causal-use, no-fallback and answer-isolation validation. It did not create a training accuracy observation.

GitHub Actions remain classified as `PRESTEP_PLATFORM_OR_RUNNER_FAILURE_UNRESOLVED_NOT_USED_AS_PASS`. No CI PASS is claimed; the scoped exception is recorded under `governance/activation-exceptions/`.

## Training rule

Activation does not make historical or shadow predictions scoreable. Every real training group must begin with a fresh `GROUP_MANIFEST`; every case requires a new input freeze, SOURCE_PACKET, METHOD_PACKET and RUN_CONTRACT before reasoning. Score eligibility remains conditional on that case's own `CAUSAL_USE_RECEIPT=PASS`.

Case count, question count, training rounds and mastery thresholds are not fixed globally. They are controlled by the frozen group and learning contracts.
