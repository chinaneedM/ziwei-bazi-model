#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
required_paths=(
  .github
  case-bank
  chat-input
  config
  docs
  examples
  knowledge-workbench
  model-learning
  scripts
  sources/canonical
  src
  tests
  training
)

if [[ "$(git -C "$repo_root" config --bool core.sparseCheckout || true)" == "true" ]]; then
  git -C "$repo_root" sparse-checkout add "${required_paths[@]}"
fi

for relative_path in "${required_paths[@]}"; do
  if [[ ! -e "$repo_root/$relative_path" ]]; then
    echo "ERROR: required checkout path is missing: $relative_path" >&2
    exit 2
  fi
done

if command -v gh >/dev/null; then
  gh_bin="$(command -v gh)"
elif [[ -x "/tmp/fortune-gh/gh_2.96.0_linux_amd64/bin/gh" ]]; then
  gh_bin="/tmp/fortune-gh/gh_2.96.0_linux_amd64/bin/gh"
else
  gh_version="2.96.0"
  archive_name="gh_${gh_version}_linux_amd64.tar.gz"
  archive_sha256="83d5c2ccad5498f58bf6368acb1ab32588cf43ab3a4b1c301bf36328b1c8bd60"
  install_root="${TMPDIR:-/tmp}/fortune-gh"
  archive_path="$install_root/$archive_name"
  extracted_root="$install_root/gh_${gh_version}_linux_amd64"
  mkdir -p "$install_root"
  curl --fail --location --retry 3 \
    "https://github.com/cli/cli/releases/download/v${gh_version}/${archive_name}" \
    --output "$archive_path"
  printf '%s  %s\n' "$archive_sha256" "$archive_path" | sha256sum --check -
  tar --no-same-owner -xzf "$archive_path" -C "$install_root"
  gh_bin="$extracted_root/bin/gh"
fi

if [[ ! -x "$gh_bin" ]]; then
  echo "ERROR: gh bootstrap did not produce an executable" >&2
  exit 2
fi

if [[ "${1:-}" == "--check" ]]; then
  echo "Work environment is ready: $gh_bin"
  exit 0
fi

if [[ "$#" -gt 0 ]]; then
  PATH="$(dirname "$gh_bin"):$PATH" exec "$@"
fi

echo "$gh_bin"
