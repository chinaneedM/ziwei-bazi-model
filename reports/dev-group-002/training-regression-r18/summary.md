# DEV-GROUP-002 R18 partial remote materialization

The DEV-EXAMPLE-005 prediction was frozen before answer access under the unchanged R14 interface. Frozen ranks: `DBAC / DCBA / DBAC / ABCD / DBAC`; TOP1 `DDDAD`; TOP2 `BCBBB`.

After literal answer replay (`DADAB`), the case training score is TOP1 `3/5`, TOP2 `4/5`; group training score becomes TOP1 `8/25`, TOP2 `13/25`. The regression is preserved without answer-derived repair.

Full local objects are hash-bound: 28 source excerpts, 45 atoms, 90 track directions, 30 common-atom rows and 30 pairwise rows with zero cycles. The full safe projections are not yet all remote, and GitHub Actions is externally unverified because both attempts ended with zero executed steps and no logs. Formal validity, local seals and S03 fusion remain zero.
