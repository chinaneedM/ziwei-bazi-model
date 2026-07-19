# License and provenance manifests

The repository `LICENSE` applies to project-authored software and original
project documentation unless a file states otherwise. It does not automatically
relicense third-party or user-supplied knowledge and data.

Every knowledge or data pack eligible for an official public release must have
a manifest validated against `knowledge-pack-manifest.schema.json`.

A manifest must bind the exact distributed files and record:

- stable pack and release identifiers;
- SHA-256 and byte length;
- source and rights-holder information;
- SPDX license, public-domain basis, or documented permission;
- attribution and notice requirements;
- redistribution, modification, and public-display permissions;
- personal-data and consent status;
- whether public distribution is allowed.

`UNKNOWN`, `UNVERIFIED`, missing, or conflicting rights states are fail-closed.
They may be investigated in an engineering branch but may not be included in an
official open-source release artifact.

Manifests describe legal/provenance status only. They do not grant predictive
weight or replace SOURCE_PACKET and EVIDENCE_USAGE_LEDGER provenance.
