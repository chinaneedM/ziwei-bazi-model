# R17 prompt and repository cutover status

## Confirmed project instruction

The active project instruction is `MP-PROFESSIONAL-REASONING-20260718-R17`.

The user supplied the complete active instruction verbatim in the running project conversation. Its canonical UTF-8/LF representation matches the previously calculated candidate fingerprint:

- SHA256: `e7e33e69fec7258b538eaf2698755f901b73933d67bcd86ca45e9bc2a66fce79`
- bytes: `11702`
- non-whitespace Unicode code points: `5253`
- LF count: `84`

This proves the user-confirmed canonical content. It does not claim access to an unavailable raw export of the platform's internal project-setting storage bytes.

## Candidate bindings

- prompt snapshot receipt status: `PASS`
- method candidate: `METHOD-R17`
- method rule change: `NO_RULE_CHANGE_PROMPT_BINDING_ONLY`
- knowledge candidate: `KNOWLEDGE-R17-PROMPT-CUTOVER-CANDIDATE`
- source-content commit: `3f823756b2cb9479e5cd9d27978459b7e537eaa8`
- knowledge manifest object hash: `6d62b5781da2b7be0ef2f0b772b5cf379f1ef4ce3054df7992e160b3d55c00dc`

## Composite source materialization

S00–S18 reuse exact R16 parent files. S19 is produced by byte-prepending the R17 control-root overlay to the immutable R16 S19 file.

Expected S19 output:

- SHA256: `59a0c04a282125929317b7166f9137b440f1f6d239bf27aec5b740d20b5c6a91`
- bytes: `10283817`

Full local materialization using uploaded files whose hashes matched the GitHub R16 manifest passed 20/20 source rows. The generic materializer and overlay-tamper rejection tests passed 2/2.

## Current hard boundary

```text
CUTOVER_STATUS=HOLD_PENDING_REMOTE_IMMUTABLE_READBACK_MODEL_R17_AND_CAUSAL_SHADOW
FORMAL_RELEASE=NO
SCORE_ELIGIBILITY=PROHIBITED
```

Remaining gates:

1. Materialize the composite candidate from an immutable GitHub checkout and verify all 20 files.
2. Build `MODEL-R17-REPOSITORY-SHADOW-V1` with the resulting code and materialization bindings.
3. Generate a fresh answer-isolated RUN_CONTRACT, SOURCE_PACKET and METHOD_PACKET before reasoning.
4. Execute one real non-scoring repository-only shadow run.
5. Obtain causal-use and no-fallback PASS receipts.
6. Obtain explicit promotion approval.

The R16 active pointers remain unchanged until these gates pass.
