# License and provenance manifests

The repository `LICENSE` applies to project-authored software and original
project documentation unless a file states otherwise. It does not automatically
relicense third-party or user-supplied knowledge and data.

## Active knowledge release

The exact 20 S00-S19 files bound by the active `KNOWLEDGE-R17` release are
published under `CC0-1.0` through these objects:

- `knowledge/active-release.json` — active release authority;
- `knowledge/releases/KNOWLEDGE-R17/release-manifest.json` — exact S00-S19
  source paths, hashes, byte lengths, and release binding;
- `licenses/knowledge-packs/KNOWLEDGE-R17/rights-declaration.json` — immutable
  record of the user's A2 rights representation and CC0 instruction;
- `licenses/knowledge-packs/KNOWLEDGE-R17/manifest.json` — machine-generated
  exact-file license manifest;
- `licenses/knowledge-packs/KNOWLEDGE-R17/CC0-NOTICE.md` — public notice;
- `reports/open-source-migration/knowledge-rights/open-source-release-verification.json`
  — verifier result.

The license manifest is valid only while it exactly matches the active release
pointer, the formal knowledge release manifest, all 20 file hashes and byte
lengths, and the recorded rights declaration.

## Manifest requirements

Every knowledge or data pack eligible for an official public release must have
a manifest validated against `knowledge-pack-manifest.schema.json`.

A manifest must bind the exact distributed files and record:

- stable pack and release identifiers;
- SHA-256 and byte length;
- active release pointer and release-manifest hashes;
- source and rights-holder information;
- SPDX license, public-domain basis, or documented permission;
- attribution and notice requirements;
- redistribution, modification, and public-display permissions;
- personal-data and consent status;
- whether public distribution is allowed.

`UNKNOWN`, `UNVERIFIED`, missing, conflicting, or stale rights states are
fail-closed. Historical or candidate packs are not licensed merely because an
active release is licensed. They may be investigated in an engineering branch
but may not enter an official open-source release artifact without their own
exact binding.

Manifests describe legal/provenance status only. They do not grant predictive
weight or replace SOURCE_PACKET and EVIDENCE_USAGE_LEDGER provenance. The user
rights declaration is a recorded representation and licensing instruction, not
an independent legal opinion; it cannot waive rights the declarant does not own.
