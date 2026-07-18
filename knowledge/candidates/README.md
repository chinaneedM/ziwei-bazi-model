# Knowledge candidates

This directory contains immutable candidate knowledge releases. A candidate must use a unique version directory and must never overwrite `knowledge/base` or an earlier candidate.

Required candidate contents:

- a complete S00–S19 file set;
- `release-manifest.json` with exactly 20 canonical source rows, raw SHA256 values, byte sizes, repository paths, parent release, and S19 binding hash;
- rebuilt S00 locator/index artifacts;
- rebuilt S19 active binding table;
- anti-answer-leak scan receipt;
- source and method validation receipts;
- explicit unresolved conditions.

Promotion is fail-closed. It requires manifest validation, complete file readback, rebuilt S00/S19 validation, answer-isolated repository-only shadow validation, causal-use validation, regression gates, and an approval identifier. Promotion copies the candidate into a new immutable `knowledge/releases/<release-id>` directory and atomically advances `knowledge/active-release.json`. It never mutates the candidate or historical R16 baseline.

Rollback never deletes a release. It creates a rollback receipt and atomically moves the active pointer to a previously validated immutable release. Scored runs remain bound to the release they originally consumed.
