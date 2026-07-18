# Ziwei-Bazi Public Runner Bootstrap

This directory is the installation source for the public, stateless GitHub Actions executor.

## Fixed repository roles

- Private authority repository: `chinaneedM/ziwei-bazi-model`
- Public compute repository: `chinaneedM/ziwei-bazi-public-runner`
- Public repository role: execute allowlisted deterministic tasks only
- Private repository role: sole authority for cases, knowledge, methods, state, generated objects and hashes

The public repository must never contain case bodies, source-library bodies, answers, reveals, predictions, diagnosis text or generated private runtime objects.

## Required public repository setup

Create `chinaneedM/ziwei-bazi-public-runner` as a **public** repository and initialize it with a README so that the `main` branch exists.

Create one fine-grained personal access token:

- Resource owner: `chinaneedM`
- Repository access: only `ziwei-bazi-model`
- Repository permissions:
  - Contents: Read and write
  - Metadata: Read

Add it to the public repository as an Actions repository secret named exactly:

`PRIVATE_REPO_TOKEN`

Do not place the token in a file, issue, pull request, commit, variable or workflow input.

## Installed workflow

Copy `.github/workflows/private-repo-task.yml` from this bootstrap directory into the public repository at the same path.

The workflow:

1. runs only for same-repository pull requests;
2. requires exactly one changed file under `requests/*.json`;
3. accepts only an allowlisted task and fixed private repository;
4. checks the private request file against a frozen SHA-256;
5. builds answer-free runtime packets in the private checkout;
6. prints only IDs, hashes, counts and status;
7. uploads no private artifact;
8. stages and pushes only the bound private output root.

Fork pull requests fail the job-level same-repository condition and receive no repository secret.

## Current migration target

- Group run: `GROUP-RUN-20260718T180018Z-1F09939E2A6A`
- Private request: `runtime/runtime-packet-requests/GROUP-RUN-20260718T180018Z-1F09939E2A6A.json`
- Task: `BUILD_RUNTIME_PACKETS`

After the public repository and secret exist, the current ChatGPT session can install the workflow, create a request branch, open the same-repository request PR, observe the free public Actions run, and validate the private writeback.
