# Fortune V1 interface and topology repair report

## Scope

This repair changes installation, repository topology, source transport normalization, audit, freeze validation and reverse grading only. It does not redesign the Ziwei/Bazi reasoning Schema, alter S05–S16 base knowledge, add answer-derived case rules, or open the five real-example RAR archives.

## Current result

- Source ZIP outer SHA256: exact match.
- S00–S19 normalized source count: 20.
- S00/S01/S18/S19 active control-root occurrence count: one each.
- S19 first current binding table: 19 rows; declared, recomputed and expected hashes match.
- Source baseline commit: `989ee246ef55c92a9b4a1b86ccd4b616bbbf0069`.
- Source baseline tag target: `source-baseline-S00-S19-R16`; not yet created because no Actions run was emitted for connector writes. Manual `workflow_dispatch` remains available and readback is required.
- Derived locator index: 18 parent libraries, 15,751 entries; all parent hashes, byte ranges and parent-segment hashes read back successfully; S19 excluded.
- Active S02: `80c11bbb…a5b1`, 464160 bytes. The `66ee9750…abcb`, 461193-byte version is historical only.
- Runtime vault credential/workflow path: removed from current runtime tree.
- Answer-vault reverse-grading package: generated locally, not installed or read back.
- Main-prompt exact export: not supplied; snapshot gate remains blocked.
- External dual-track prediction runner: `NOT_INSTALLED`.
- Automation install status: `SCHEMA_DEFINED_NOT_INSTALLED`.

Machine receipts under `reports/` are authoritative for byte paths, hashes, field paths, actual/expected values and status. Final GitHub commit and source-baseline tag are recorded only after remote creation and readback.
