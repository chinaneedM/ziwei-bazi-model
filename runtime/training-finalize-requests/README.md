# Training-finalize requests

One immutable request finalizes a revealed group only after every question-unit evidence object is present under the same run root.

The request must use `GROUP-TRAINING-FINALIZE-REQUEST-V1`, bind the run-local training intake and evidence manifest, include its canonical `object_hash`, and preserve the original unit order. The finalizer evaluates and advances every unit serially and writes `training/training-finalize-receipt.json` only when all units complete. Post-reveal replays never count as blind accuracy, and finalization never promotes a knowledge, method, prompt, or model candidate.
# Training finalize requests

Place one immutable `GROUP-TRAINING-FINALIZE-REQUEST-V1` JSON object here only
after every question unit listed by the run's learning cycle has a hashed
`QUESTION-TRAINING-EVIDENCE-V2.1` object and the evidence manifest is complete.

The repository workflow performs a full manifest preflight before it writes any
evaluation, advances units serially, and commits a
`GROUP-TRAINING-FINALIZE-RECEIPT-V1` only when every declared unit closes.  A
DEV-GROUP-002 receipt must contain exactly five completed cases and 25 completed
question units.  Post-reveal replays remain training-fit evidence and never
become new blind-accuracy observations or a model-release promotion.
