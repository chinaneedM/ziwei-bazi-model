# Training data registry

`training-data/` stores reusable, answer-free training and regression case objects.

Rules:

- Each case is immutable and identified independently from its display filename.
- Each group contains a manifest, immutable revisions and a `HEAD.json` pointer.
- Runtime case objects may contain Ziwei charts, verified structured Bazi transcriptions, literal questions and option text, but never answers.
- Answers live only in `chinaneedM/fortune-answer-vault`.
- A group is not revealable until every case has a registered frozen baseline prediction.
- New uploads are classified and imported under `config/training-example-ingest-policy.json` and `docs/training-example-ingest-standard.md`.
- Exact duplicates reuse existing references; changed content creates a new immutable revision or case ID.
