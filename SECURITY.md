# Security policy

## Scope

Security includes conventional software vulnerabilities and project-specific
integrity failures:

- exposure of `FORTUNE_PUBLIC_ANSWER_KEY`;
- access to unrevealed answer plaintext before group freeze;
- bypass of independent-track seals or answer-isolation gates;
- modification of immutable prediction or training receipts;
- path traversal from public encrypted envelopes;
- workflow execution using a private or cross-repository dependency;
- secret exfiltration through pull requests, logs, artifacts, caches, or error
  messages;
- publication of personal data or content without redistribution permission.

## Supported versions

Only the current default branch and explicitly identified release tags are
supported. Candidate branches and draft pull requests are engineering objects,
not formal releases.

## Reporting

Do not place an active key, unrevealed answer, exploit payload, or personal data
in a public issue.

Use GitHub's private vulnerability reporting feature for this repository. If
that feature is unavailable, open a public issue containing only a neutral
request for a private security channel; do not include sensitive details.

A useful report includes:

- affected commit or release;
- affected workflow, module, schema, or object path;
- reproducible steps using synthetic data;
- expected and actual isolation behavior;
- whether any real answer, key, or personal record may have been exposed;
- proposed remediation, when available.

## Secret handling

The official runtime may use the repository Actions secret
`FORTUNE_PUBLIC_ANSWER_KEY` only to decrypt same-repository public ciphertext
after `GROUP_PREDICTION_FREEZE_PASS`.

The key must never be:

- committed to Git;
- printed to logs;
- exposed to pull-request workflows;
- stored in artifacts or caches;
- copied into issues, discussions, or documentation;
- reused for synthetic public examples.

Rotate the key after any suspected disclosure. Existing encrypted envelopes
must be re-encrypted or retired under an auditable migration receipt.

## Disclosure and remediation

Confirmed vulnerabilities should receive a public post-remediation advisory
that describes impact, affected versions, mitigation, and the fixing commit
without publishing live secrets or unrevealed answers.
