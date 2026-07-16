# Fortune answer vault

This private repository initiates reverse grading. The runtime repository has no vault credential and no vault checkout workflow. The owner manually dispatches `.github/workflows/grade-frozen-prediction.yml` only after a prediction has been frozen.

The repository secret `RUNTIME_REPO_TOKEN` must be a fine-grained token scoped only to `chinaneedM/ziwei-bazi-model`, with Contents read/write and Metadata read-only. Never store the token value in a file, issue, log, or commit.

Place answer objects under `answers/` using the template and Schema in this package. Do not add real answers until the workflow and repository-scope probes have been independently verified.
