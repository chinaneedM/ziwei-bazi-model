# Group-training migration checklist

This checklist converts the existing single-case CHAT/WORK handoff into a group-level single-session loop without changing prediction knowledge.

## Required code changes

- Add `GROUP-TRAINING-RUN-V1` validation around a frozen ordered set of `PREDICTION-RUN-V1` children.
- Add a group import command that accepts the complete five-case submission and rejects partial, duplicate, or reused case rows.
- Create a fresh prediction whitelist before each case and prohibit references to prior case prediction/reveal objects.
- Add group freeze verification that requires every expected child run to pass before any reveal authorization is emitted.
- Change reverse grading authorization from one case run to one group run while preserving per-case literal answer replay.
- Add group diagnosis and patch-candidate records that cannot mutate original predictions.
- Require new group and case run IDs for every clean rerun.
- Add accept/rollback state transitions using the existing group training policy.

## Required failure tests

- early reveal before all cases freeze;
- partial group submission;
- duplicate case ID;
- missing expected case;
- reused group or case run ID;
- later-case reference to prior-case prediction;
- later-case reference to prior-case reveal;
- prediction body changed after child freeze;
- patch leak containing answers, old selections, reveal explanations, or case-direction rules;
- rejected candidate fails to restore the previous authoritative runtime commit.

## Installation gate

The current installation seal remains authoritative until all code changes and tests above pass and a new installation receipt is generated. Merely adding this contract does not claim that group execution is already installed.
