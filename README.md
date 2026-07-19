# Ziwei-Bazi Model

An open-source, repository-driven system for auditable **紫微斗数＋四柱八字综合相对预测** training and regression.

The project is designed to be public, inspectable, forkable, and reproducible. It does not depend on a private repository, private package server, hidden database, paid model API, or background ChatGPT execution.

## Open-source model

Project-authored software, tests, workflows, schemas, configuration, and original documentation are licensed under **Apache-2.0**. See `LICENSE`, `NOTICE`, and `docs/open-source-architecture.md`.

Knowledge and data packs use per-pack provenance and license manifests. An official public release may include only material with verified public-domain status, an open license, or documented redistribution permission. Unverified rights are fail-closed.

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

## Current candidate bindings

- Project prompt: `MP-PROFESSIONAL-REASONING-20260718-R17`
- Knowledge candidate: `KNOWLEDGE-R17-PROMPT-CUTOVER-CANDIDATE-V2`
- Method: `METHOD-R17`
- Model candidate: `MODEL-R17-REPOSITORY-SHADOW-V2`
- Runtime configuration candidate: `config/runtime-r17-candidate.json`

Candidate status is not equivalent to a formal release. Formal training remains blocked until the public-repository policy, complete test suite, synthetic public-envelope end-to-end run, immutable receipt, and active release bindings all pass.

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
```

Verify the open-source/public-only repository policy:

```bash
python scripts/verify-public-only-repository.py \
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
- claim PASS, release, or training readiness without repository-bound receipts.

## Contributing and governance

- `CONTRIBUTING.md` — contribution and provenance requirements
- `GOVERNANCE.md` — public decision and release process
- `SECURITY.md` — vulnerability and answer-isolation reporting
- `licenses/README.md` — knowledge/data licensing policy
- `docs/open-source-architecture.md` — complete open-source architecture
- `docs/end-to-end-training-pipeline.md` — runtime pipeline

## License

Apache License 2.0 for project-authored software and original project documentation, except where otherwise stated. Third-party and user-supplied content remains under its own declared terms.
