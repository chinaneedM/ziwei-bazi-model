# Runtime view materialization

`TRAINING-CASE-BUNDLE-V2` remains the canonical immutable case object. For CHAT/WORK connector compatibility, the runtime-view materializer creates deterministic sidecars under:

`training-data/<GROUP_ID>/runtime-views/<CASE_ID>/`

Each view contains:

- `ziwei.txt` — normalized LF text, one physical line per chart line;
- `questions.txt` — original question text with normalized LF;
- `questions-parsed.json` — structured answer-free questions;
- `bazi-transcription.json` — verified mechanical transcription;
- `manifest.json` — source case SHA-256 and per-file SHA-256/byte counts.

The tool fails closed when an answer payload or answer reference is visible, and refuses to overwrite an existing view. Views are transport artifacts only and have zero astrological contribution.
