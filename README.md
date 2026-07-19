# Ziwei-Bazi Model

An open-source, repository-driven system for auditable **紫微斗数＋四柱八字综合相对预测** training and regression.

The project is designed to be public, inspectable, forkable, and reproducible. It does not depend on a private repository, private package server, hidden database, paid model API, or background ChatGPT execution.

## Open-source model

The repository uses a two-part licensing model:

- project-authored software, tests, workflows, schemas, configuration, and
  original documentation use **Apache-2.0**;
- the exact 20 S00-S19 files bound by the active `KNOWLEDGE-R17` release use
  **CC0-1.0**.

The active knowledge license is machine-bound through:

- `knowledge/active-release.json`;
- `knowledge/releases/KNOWLEDGE-R17/release-manifest.json`;
- `licenses/knowledge-packs/KNOWLEDGE-R17/rights-declaration.json`;
- `licenses/knowledge-packs/KNOWLEDGE-R17/manifest.json`;
- `licenses/knowledge-packs/KNOWLEDGE-R17/CC0-NOTICE.md`.

The formal verifier recomputes all 20 file hashes and byte lengths. Historical,
candidate, uploaded, personal, or third-party material is not automatically
covered by the active CC0 manifest.

## One public repository

The complete runtime operates in this repository:

```text
chinaneedM/ziwei-bazi-model
```

No active workflow may require another repository. The public-only policy rejects private-repository references, cross-repository checkouts, unauthorized answer secrets, and plaintext unrevealed answers.

## Blind evaluation in an open-source project

All answer-handling code is public. Unrevealed answer plaintext is not committed.

The repository stores public encrypted envelopes:

```text
public-answer-vault/encrypted/<GROUP_RUN_ID>.json.fernet
```

The official runtime key is stored as the GitHub Actions secret:

```text
FORTUNE_PUBLIC_ANSWER_KEY
```

The key is an operational blind-evaluation secret, not a private source-code dependency. Anyone can fork the project, generate their own key, create their own encrypted envelopes, and reproduce the complete mechanism.

The reveal workflow:

1. verifies `GROUP_PREDICTION_FREEZE_PASS`;
2. decrypts the public envelope only into a transient `/tmp` directory;
3. performs two-path literal answer replay;
4. creates public scoring and learning receipts;
5. destroys the transient plaintext.

It does not run on pull requests, so untrusted fork code cannot receive the key.

## Execution model

The prediction engine is an active user-started ChatGPT project session in `CHAT_ONLY` or `WORK` mode. GitHub does not autonomously start ChatGPT, and the project must not claim asynchronous or background reasoning.

Repository code handles deterministic ingest, immutable snapshots, source and method packets, staged access, track seals, option release, pairwise validation, group freeze, answer replay, training state, regression, and audit receipts.

## Runtime sequence

```text
answer-free group request
  -> staged PREBLIND clean start
  -> SOURCE_PACKET / METHOD_PACKET / RUN_CONTRACT
  -> independent Ziwei and Bazi preblind models
  -> machine-built local seals
  -> postblind option release
  -> complete pairwise prediction bundles
  -> case and group prediction freeze
  -> transient answer-envelope decryption
  -> literal replay and scoring
  -> LEARNING-CYCLE-V2.1
  -> public regression and release receipts
```

## Current bindings and validation

- Project prompt: `MP-PROFESSIONAL-REASONING-20260718-R17`
- Active knowledge release: `KNOWLEDGE-R17`
- Knowledge license: `CC0-1.0` for the exact active S00-S19 manifest
- Method: `METHOD-R17`
- Model candidate: `MODEL-R17-REPOSITORY-SHADOW-V2`
- Runtime configuration candidate: `config/runtime-r17-candidate.json`

Public repository CI, answer-key runtime validation, and a synthetic non-scoring
public-envelope run through `LEARNING_ACTIVE` have passed. The knowledge-rights
verifier also passed with one active manifest, 20 files, and zero failures.
Formal activation remains blocked until pull request #36 is merged and the
merged default branch passes post-merge CI and immutable readback.

## Installation

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Run the tests:

```bash
python -m unittest discover -s tests -v
pytest -q
```

Verify the public-only repository policy:

```bash
python scripts/verify-public-only-repository.py \
  --root . \
  --visibility public
```

Verify the complete open-source release and active knowledge manifest:

```bash
python scripts/verify-open-source-release.py \
  --root . \
  --visibility public
```

## Public answer envelopes

Generate a key for your own fork or synthetic environment:

```bash
fortune-public-answer-vault generate-key
```

Store it as `FORTUNE_PUBLIC_ANSWER_KEY`; do not commit it. Encrypt a locally prepared answer vector:

```bash
export FORTUNE_PUBLIC_ANSWER_KEY='<your key>'
fortune-public-answer-vault encrypt \
  --answer /secure-local-path/<GROUP_RUN_ID>.json \
  --envelope public-answer-vault/encrypted/<GROUP_RUN_ID>.json.fernet
```

Only the encrypted envelope is committed.

## Project boundaries

The system does not:

- treat astrology as scientifically validated fact;
- provide medical, legal, financial, or emergency decisions;
- convert revealed answers into case-specific prediction rules;
- count post-reveal repetitions as additional blind accuracy;
- silently fall back to uploads, prior chats, private repositories, or hidden files;
- claim PASS, release, or training readiness without repository-bound receipts;
- treat a user rights declaration as independent legal verification.

## Contributing and governance

- `CONTRIBUTING.md` — contribution and provenance requirements
- `GOVERNANCE.md` — public decision and release process
- `SECURITY.md` — vulnerability and answer-isolation reporting
- `licenses/README.md` — knowledge/data licensing policy
- `docs/open-source-architecture.md` — complete open-source architecture
- `docs/end-to-end-training-pipeline.md` — runtime pipeline

## License

Apache License 2.0 for project-authored software and original project documentation, except where otherwise stated. The exact active `KNOWLEDGE-R17` S00-S19 files are available under CC0-1.0 through their machine-bound manifest. Other content remains under its own declared terms.
