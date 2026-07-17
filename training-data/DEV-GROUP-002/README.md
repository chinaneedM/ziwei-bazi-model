# DEV-GROUP-002

DEV-GROUP-002 is a clean reimport of the five original user-supplied training archives.

- Runtime storage: `PLAIN_CANONICAL_JSON` only.
- Five cases, five questions per case, 25 questions total.
- Ziwei text and literal question/option text come directly from the original archives.
- Bazi content is a SHA-256-bound verified structured transcription of each original chart image.
- Runtime files contain no answer payload or answer reference.
- Private answer objects live only in `chinaneedM/fortune-answer-vault`.
- DEV-GROUP-001 and its corruption reports remain unchanged for audit history.
- The group may be used only when `training-data-integrity` returns `PASS_READY` from repository-readback bytes.
