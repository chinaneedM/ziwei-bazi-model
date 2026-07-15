#!/usr/bin/env bash
set -euo pipefail

owner="${1:?usage: create-repositories.sh OWNER}"
command -v gh >/dev/null || { echo "gh CLI is required" >&2; exit 2; }
gh auth status >/dev/null

gh repo view "$owner/fortune-runtime" >/dev/null 2>&1 || gh repo create "$owner/fortune-runtime" --private --disable-issues --disable-wiki
gh repo view "$owner/fortune-answer-vault" >/dev/null 2>&1 || gh repo create "$owner/fortune-answer-vault" --private --disable-issues --disable-wiki

echo "Repositories created. Provision separate prediction and grader identities, then run fortune-v1 verify-topology."

