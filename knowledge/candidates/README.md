# Knowledge candidates

This directory contains immutable candidate knowledge releases. A candidate must use a unique version directory and must never overwrite `knowledge/base` or an earlier candidate.

A candidate may use either of two storage forms:

1. **Fully materialized candidate** — twenty canonical S00–S19 files are stored directly in the candidate directory.
2. **Content-addressed composite candidate** — unchanged files reuse exact immutable parent-release paths and hashes, while changed files are defined by deterministic composition objects such as `BYTE_PREPEND`. The candidate must include the overlay, expected final file hash and size, parent paths and hashes, source-content commit, materialization receipt, and a manifest containing exactly twenty final logical source rows.

Composite storage does not reduce the release proof burden. Before source-catalog construction, shadow execution, promotion, or scoring, the repository runner must materialize all twenty canonical files into an isolated versioned knowledge directory and verify every final SHA256 and byte size against the candidate manifest. Missing parents, unsupported composition modes, overlay mutation, output mismatch, or incomplete readback fail closed.

Required candidate contents:

- exactly twenty final logical S00–S19 source rows;
- `release-manifest.json` with canonical names, final raw SHA256 values, byte sizes, repository paths or materialization recipes, parent release, source-content commit, and S19 binding hash;
- complete materialization provenance for every reused or composed row;
- rebuilt S00 locator/index artifacts when source knowledge changes require them;
- rebuilt S19 active control binding when the prompt or runtime contract changes;
- anti-answer-leak scan receipt;
- source, method, prompt and materialization validation receipts;
- explicit unresolved conditions.

Promotion is fail-closed. It requires manifest validation, full twenty-file materialization and readback, rebuilt S00/S19 validation, answer-isolated repository-only shadow validation, causal-use validation, regression gates, and an approval identifier. Promotion creates a new immutable object under `knowledge/releases/<release-id>` and atomically advances `knowledge/active-release.json`. It never mutates the candidate or historical R16 baseline.

Rollback never deletes a release. It creates a rollback receipt and atomically moves the active pointer to a previously validated immutable release. Scored runs remain bound to the release they originally consumed.
