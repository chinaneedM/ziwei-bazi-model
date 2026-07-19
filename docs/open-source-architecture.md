# Open-source architecture

## Goal

The project is designed as a completely public, inspectable, forkable, and
reproducible software system. No private repository, private package server,
proprietary runtime service, hidden database, or maintainer-only source tree is
required to build or operate the system.

The implementation follows a single-public-repository model:

```text
public Git repository
  ├── source code, tests, schemas, workflows and documentation
  ├── public open-license knowledge/data packs
  ├── answer-free run inputs and immutable prediction objects
  ├── public encrypted unrevealed-answer envelopes
  ├── post-reveal replay and training receipts
  └── public release and provenance manifests
```

## Open source versus blind evaluation

Open source requires that the preferred source form and redistribution terms of
the software are public. Blind evaluation additionally requires that the
correct answer not be available to the prediction process before freeze.

These requirements are compatible:

- all code that encrypts, stores, validates, decrypts, replays, and scores an
  answer is public;
- the public repository stores ciphertext, not unrevealed plaintext;
- each operator may create their own key and answer envelopes;
- the official project key is an operational secret, not a private source-code
  dependency;
- after reveal, the literal replay and scoring objects are public;
- synthetic examples use disposable public fixtures and never the official key.

No claim of reproducibility depends on knowing the official unrevealed answer.
Anyone can reproduce the complete mechanism using synthetic or independently
prepared answer vectors.

## Licensing model

### Software and original project documentation

Project-authored code, tests, workflows, configuration, schemas, and original
documentation are licensed under Apache-2.0 unless a file states otherwise.

### Knowledge and data packs

Knowledge, quotations, translations, source extracts, images, charts, and case
data use per-pack licensing. An active public pack must provide an exact
provenance/license manifest with:

- pack ID and release;
- file path, SHA-256, and byte length;
- source identity and locator;
- author or rights holder when known;
- SPDX license identifier, public-domain basis, or written permission basis;
- attribution and notice requirements;
- permission for modification and redistribution;
- personal-data and consent status;
- `PUBLIC_DISTRIBUTION_ALLOWED=true`.

A missing, conflicting, or unverified license state is fail-closed. The pack is
not part of an official open-source release and cannot be silently recovered
from uploads, prior conversations, local caches, or private storage.

## Public execution model

All runtime workflows operate on the same public repository and are triggered
by same-repository `push` or `workflow_dispatch` events. Write workflows do not
execute untrusted fork code and do not expose secrets to pull-request jobs.

The active sequence is:

1. freeze answer-free input;
2. build PREBLIND packets;
3. create independent Ziwei and Bazi models;
4. machine-seal both tracks;
5. release options only after all seals pass;
6. create complete pairwise prediction bundles;
7. freeze every case and the complete group;
8. decrypt the public answer envelope in a transient runner directory;
9. perform literal replay and scoring;
10. destroy plaintext and publish immutable training receipts.

## Public reproducibility

A release must provide:

- exact source commit and tag;
- Python and dependency constraints;
- all schemas and validation code;
- synthetic test fixtures;
- deterministic policy checks;
- a public synthetic end-to-end receipt;
- release manifest with object hashes;
- source/data license manifests;
- migration notes from the previous release.

The official prediction engine may remain an interactive ChatGPT project
session. GitHub does not autonomously invoke that session, and the system must
not claim background execution. Repository validation and object construction
remain reproducible without a proprietary prediction API.

## Security and privacy

A public repository must not contain:

- secret keys or credentials;
- unrevealed plaintext answers;
- unnecessary personal identifiers;
- private charts or case records without explicit public-release consent;
- content without redistribution permission;
- private repository URLs or cross-repository runtime tokens.

Personal cases intended for public regression must be anonymized or replaced by
consented/public-domain cases. A case's prediction value never overrides its
privacy or licensing status.

## Forkability

A fork must be able to:

- replace the project name and active bindings;
- create its own answer key and public encrypted envelopes;
- install alternative open-license knowledge packs;
- run the policy and synthetic end-to-end tests;
- create its own immutable releases without contacting the original maintainer.

No central approval service, private artifact, or hidden network endpoint is
part of the architecture.
