# Manual installation and readback

1. Upload this package to the root of the existing private repository `chinaneedM/fortune-answer-vault` without adding real answers.
2. Confirm the Actions secret is named `RUNTIME_REPO_TOKEN`. Do not disclose its value.
3. Confirm the token is scoped only to `chinaneedM/ziwei-bazi-model`, with Contents read/write and Metadata read-only.
4. Commit the files and enable Actions. Do not add branch protection, ruleset, or environment-protection PASS claims on the current GitHub Free private-repository plan.
5. Read back every installed file and compare it with `initialization-manifest.json`.
6. Run a token-scope probe from this repository: runtime repository must return 200; answer vault must return 403/404 for `RUNTIME_REPO_TOKEN`.
7. Record the workflow commit SHA, workflow byte SHA256, repository visibility, and probe HTTP statuses in a topology receipt.
8. Do not mark the topology installed until the runtime side reads that receipt and all install gates pass.
