# Governance

## Principles

The project is governed through public repository objects:

- proposals and defects are discussed in issues;
- changes are reviewed in pull requests;
- releases are identified by immutable commits and tags;
- runtime state is carried by versioned schemas and receipts;
- formal claims require machine-verifiable evidence;
- no contributor, maintainer, model, or workflow may silently bypass a gate.

## Roles

### Maintainers

Maintainers may triage issues, review and merge pull requests, manage releases,
and configure repository settings and secrets. Maintainer authority does not
permit rewriting immutable run records or declaring a formal PASS without the
required receipts.

### Contributors

Any person may propose code, tests, documentation, schemas, knowledge packs,
or audit findings. Contributions are evaluated by the same public criteria,
regardless of author.

### Release steward

A release steward checks the exact release commit, license/provenance manifests,
CI results, synthetic end-to-end receipt, migration notes, and active pointers.
The steward may be a maintainer, but the release checklist remains public and
machine-verifiable.

## Decision process

Routine changes use normal pull-request review. Changes to answer isolation,
licensing policy, release gates, active schemas, or scoring semantics require:

1. a public design note;
2. tests covering successful and fail-closed behavior;
3. an explicit migration plan;
4. review of compatibility and contamination risks;
5. an immutable post-merge verification receipt.

When maintainers disagree, the default is to preserve the current active
release and keep the candidate in HOLD until the disagreement is resolved by
additional evidence or a documented decision.

## Release policy

A release is not created merely because code is public or merged. A formal
release requires:

- repository visibility `public`;
- Apache-2.0 license and required notices;
- complete public dependency lock or reproducible environment definition;
- public source/data provenance manifests;
- passing unit, integration, policy, and synthetic end-to-end tests;
- an immutable release receipt binding all artifacts and hashes;
- no unresolved answer-isolation or licensing violation.

## Model and method changes

Knowledge and method candidates must remain separate from active releases until
promotion gates pass. Revealed answers may diagnose deficiencies, but may not
be converted into case IDs, answer letters, option positions, chart
fingerprints, or single-case absolute rules.

## Amendments

Changes to this governance document are made through a public pull request and
become effective only after merge. Historical governance versions remain in
Git history.
