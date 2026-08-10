# Work GitHub Access Preflight R2

This contract governs GitHub tool routing in WORK. It changes tool selection,
not repository semantics or release gates.

## Capability states

Run:

```bash
./scripts/bootstrap-work-env.sh --check
```

The preflight always reports `GH_BINARY_READY` after locating a system `gh` or
installing the pinned, SHA-verified binary. It then reports exactly one auth
state:

- `GH_AUTH_READY`: `gh auth status --hostname github.com` succeeded.
- `GH_AUTH_UNAVAILABLE`: no usable non-interactive `gh` auth was detected.

The auth probe runs once with prompts disabled. Its output is suppressed so
credentials or credential-helper details cannot enter logs. Environment-provided
`GH_TOKEN` or `GITHUB_TOKEN` may be consumed by `gh` normally; the bootstrap
does not print, copy, or persist either value.

`--check` exits successfully in both auth states because binary readiness and
authenticated GitHub CLI capability are distinct. A genuinely gh-only action
may use `--require-gh-auth`; that flag fails only the missing authenticated-gh
capability and does not relax or replace any repository release gate.

## Connector-first routing

Use the first available capability that covers the requested operation:

1. Connected GitHub tools: repository metadata, files, Issues, PRs, comments,
   mergeability/merge operations, and workflow/run/status inspection.
2. Local `git`: checkout, branches, worktree/tree inspection, commits, and push.
3. Local `gh`: only a capability the connector does not cover materially,
   especially detailed GitHub Actions check, job, or log debugging.

Do not invoke `gh` merely to re-read connector-supported PR metadata, comments,
files, merge state, workflow status, create a comment, or merge. When the
connector covers the task, `GH_AUTH_UNAVAILABLE` is not a WORK failure.

For exact-head CI acceptance, verify both the run/check head SHA and terminal
successful conclusion through the connected workflow-status capability when it
is available. Local `gh` authentication is not mandatory solely to establish
that exact-head CI passed. If a failure needs detail beyond connector coverage,
probe the specific `gh` capability and fail that capability clearly if auth is
unavailable; never change the validation standard or repository semantics.
