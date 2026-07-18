# Knowledge releases

Each child directory is an immutable promoted knowledge release. A release is the sole eligible repository knowledge authority only when `knowledge/active-release.json` points to its validated manifest and the current run contract binds that exact manifest, source packet, method release, and code commit.

A release directory must contain the complete 20-file S00–S19 baseline, its manifest, S00 catalog/index artifacts, S19 binding reconstruction, promotion receipt, validation receipts, and rollback ancestry. No file is edited in place after promotion.

The original R16 material remains under `knowledge/base` as an immutable historical control. It is not assumed to remain permanently active. Project-uploaded S00–S19 files are outside this release tree and are forbidden in scored repository-bound runs.
