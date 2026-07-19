# Contributing

Thank you for contributing to the Ziwei-Bazi Model project.

## Development model

The project is developed in public. Issues, design discussions, pull requests,
workflow results, release receipts, and regression evidence should be recorded
in this repository whenever they do not contain an unrevealed answer, personal
secret, private key, or unlawfully redistributable material.

## Contribution requirements

A contribution must:

1. preserve answer isolation and group-freeze-before-reveal ordering;
2. avoid case-specific answer rules, answer letters, option positions, or
   personal chart fingerprints in general methods;
3. preserve independent Ziwei and Bazi tracks before local sealing;
4. include tests for new behavior and fail-closed paths;
5. use deterministic, reviewable repository objects rather than hidden state;
6. include provenance and licensing information for every new knowledge or
   data source;
7. avoid committing secrets, plaintext unrevealed answers, personal data, or
   content without redistribution permission.

## Licensing of contributions

Unless explicitly marked otherwise before submission, contributions to
project-authored software, tests, workflows, configuration, and documentation
are submitted under Apache-2.0, as described by the repository `LICENSE`.

Knowledge packs and data contributions require a separate manifest describing:

- source identity and stable locator;
- copyright or public-domain status;
- license identifier or permission basis;
- attribution requirements;
- modification and redistribution permissions;
- whether the material may appear in public release artifacts;
- SHA-256 and byte length of the exact submitted object.

A knowledge or data contribution without this manifest is not eligible for an
active public release.

## Pull request checklist

- [ ] The change contains no unrevealed answer data or secret material.
- [ ] Tests cover successful and fail-closed behavior.
- [ ] No private repository or cross-repository runtime dependency is added.
- [ ] New source material has a complete provenance/license manifest.
- [ ] Existing immutable run objects are not rewritten.
- [ ] Documentation and schemas are updated.
- [ ] The public-only repository policy passes.

## Security reports

Do not disclose an active secret, unrevealed answer, or exploitable isolation
bypass in a public issue. Follow `SECURITY.md`.

## Conduct

Be respectful, evidence-driven, and specific. Critique code, claims, methods,
and evidence rather than people. Harassment, threats, discrimination, or
publication of personal information are not accepted.
