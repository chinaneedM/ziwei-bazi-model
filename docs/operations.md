# Operator manual

## 1. Import the active source baseline

Run `fortune-v1 import-source-package` with the expected outer ZIP SHA256. The command emits `raw-package-manifest.json`, `normalization-map.json`, `duplicate-and-quarantine-report.json`, staging/final source audits, `binding-table-recompute-receipt.json`, and `migration-receipt.json`. Do not rename the uploaded file or choose versions by suffix number or mtime.

After the baseline commit is immutable, record its SHA and tag in the migration receipt. Build the S01–S18 locator index with that baseline SHA, then run `fortune-v1 index-validate` to check every parent file hash, byte range and parent-segment hash.

## 2. Install the answer vault package

Upload the generated `fortune-answer-vault-init.zip` to the existing private `chinaneedM/fortune-answer-vault`. Do not provide the token value to ChatGPT or commit it. Keep `RUNTIME_REPO_TOKEN` scoped only to `chinaneedM/ziwei-bazi-model`, Contents read/write and Metadata read-only.

Read back the installed workflow and compare every file hash. From the vault, probe that the runtime token receives 200 for the runtime repository and 403/404 for the vault. Also probe the repository-local token in the opposite direction. Save only HTTP statuses and file hashes, never token values.

## 3. Freeze before reveal

`fortune-v1 freeze` writes a non-overwritable run directory and receipt. The vault workflow calls `fortune-v1 verify-freeze --run-id ...` before answer checkout. Missing Schema, mismatched RUN_ID, failed runtime validation, changed prediction/contract, or non-immutable state blocks grading before the answer object is read.

TOP1 remains formal score. TOP2 is diagnostic only. `ANSWER_VECTOR_LITERAL_REPLAY` uses two literal parsers and an answer JSON must bind the same authorized RUN_ID.

## 4. Prompt snapshot and external runner

Export the exact active project instruction bytes through an approved operator path, then run `fortune-v1 prompt-snapshot --config config/runtime.json`. The receipt reports BOM, LF/CRLF, leading/trailing whitespace, UTF-8 validity, byte size, visible non-whitespace codepoint count and actual SHA256. Never change S19 expectations to fit a bad export.

Register and test a real no-answer dual-track runner before changing `config/external-runner.json` to `INSTALLED`. A contract-only placeholder is not installation.

## 5. Final install check

Run `make install-check`. The checker never edits S19. It emits no installed-status candidate unless the source baseline/tag, prompt snapshot, two-repository machine probes, answer-vault workflow readback, external runner, synthetic tests and receipt Schema all pass together.
