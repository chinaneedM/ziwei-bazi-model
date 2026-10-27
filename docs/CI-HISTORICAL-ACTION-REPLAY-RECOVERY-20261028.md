# Historical action replay CI recovery — 2026-10-28

This is an engineering recovery record, not a new historical research batch.
Research semantic state remains `1.897.0`; the research queue is unchanged.

## Observed remote failure

Session startup independently read the live development ref, HEAD
`b3350e1aa798495770fa0048101f97cbc6957490` and tree
`28fc38a9caf642655bde52935e90bd4166fb8dd3`, recent commits, continuity
protocol, current state, authority/charter/genealogy documents, registries and
their 65 shards, and the omission ledger.

The exact-HEAD Actions query returned 21 runs: 20 success, one failure.
[Main CI run 40527856828](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/40527856828),
job `122272209771`, reached Full unittest and ran 5421 tests with four failures.
The failing positive checks belonged to 13HK, 13HL, 13HO and 13HQ. Each still
required its historical action label (or its predecessor's archived label) in
the rolling `TW-OPEN-0005.next_action`. That field now correctly describes the
13IR work. The corresponding `ISSUE_REVISION` entries remain in the ledger.

## Repair and retained guards

The four validators now require the historical revision in append-only
`history`, its `next_action` changed-field declaration, its original evidence
reference, and the predecessor revision where previously required. They still
check the live OPEN/P0 issue, source references, state/ledger synchronization,
source hashes, numerical NULLs and evidence scope. The optional ledger argument
permits isolated mutation tests; command-line checks still read the live file.

The 20 existing tests for these batches passed after the repair. Seven new
regression tests exercise all four validators: a later current action succeeds,
while deletion of the revision/predecessor, an unrelated event type, omission
of the changed field, unrelated evidence and false live closure fail. Retaining
old labels in current prose cannot compensate for a missing history entry.

Continuity, omission-ledger, registry-union and 13IR active-field gates passed
locally. Full-suite and exact-pushed-HEAD Actions acceptance must be checked for
the resulting commit; this record does not predeclare their outcome.

No historical source JSON, current-state JSON, issue ledger, Matrix, source
registry, genealogy graph or chart runtime is modified. Matrix remains 222/222,
registered sources 761, genealogy 252 nodes/238 edges, and 11 research issues
remain unresolved. The deterministic product stays CLOSED; there is no
algorithm reopen or candidate collapse.

## Remaining research

After exact-HEAD CI is clean, resume the live 13IR queue: source-bound GK3467
book6 winter-table title/D1–D7 and intervening folios; G893's six original
controls; NCL03130 solar D30 and D1–D6 field identity, separate summer D14 and
D5 〇/五; and holding-specific 1972 facsimile/colophon evidence. The 13IO
GK5553 book29→juan81–83 association remains RETRACTED/UNBOUND. Passing CI does
not supply any missing original page or settle any numeral.
