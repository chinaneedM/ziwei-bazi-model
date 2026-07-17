# Group training acceptance criteria

The group-level runtime is installable only when all criteria pass together.

## Functional

- One user start can process the complete frozen development group in one CHAT/WORK session.
- No per-case new conversation or per-case continue message is required.
- Each case still has an independent whitelist, run ID, Ziwei seal, Bazi seal, adjudication body, and freeze receipt.
- The group can freeze only after all expected cases pass.
- Reveal and grading occur only after group freeze.
- Diagnosis, patch proposal, clean rerun, regression comparison, and accept/rollback are represented by immutable objects.

## Isolation

- Prediction repository has no answer-vault credential.
- Answers and reveal explanations are physically unavailable until group freeze.
- A later case cannot reference any earlier case prediction, score, reveal, diagnosis, or shadow rebuild.
- Group administrative state is the only cross-case state permitted.

## Immutability

- Original case and group predictions are never overwritten.
- Every rerun receives new group and case run IDs.
- Duplicate paths, IDs, or object hashes fail closed.

## Learning boundary

- No answer-derived case-direction rule is added.
- No base astrological knowledge is changed from this fixed group alone.
- Only reproducible general interface defects are eligible for candidate patches.
- A candidate is accepted only when group policy passes without prohibited regression damage; otherwise it is rolled back.

## Release

- New static and synthetic tests pass.
- Group-level leak scan passes.
- Workflow and validator readback hashes pass.
- A new installation receipt and installation-state seal bind the implementation commit.
- Until then, status remains `CONTRACT_DEFINED_IMPLEMENTATION_PENDING_VALIDATION`.
