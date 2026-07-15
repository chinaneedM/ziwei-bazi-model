#!/usr/bin/env bash
set -euo pipefail
owner="${1:?usage: create-repositories.sh OWNER}"

echo "Repository creation is owner-controlled for GitHub Free private repositories."
echo "Expected existing runtime: ${owner}/ziwei-bazi-model"
echo "Expected existing vault:   ${owner}/fortune-answer-vault"
echo "This script does not create repositories, tokens, secrets, protections, rulesets, or environments."
exit 2
