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

gh_version="2.96.0"
archive_name="gh_${gh_version}_linux_amd64.tar.gz"
archive_sha256="83d5c2ccad5498f58bf6368acb1ab32588cf43ab3a4b1c301bf36328b1c8bd60"
install_root="${FORTUNE_WORK_GH_INSTALL_ROOT:-${TMPDIR:-/tmp}/fortune-gh}"
archive_path="$install_root/$archive_name"
extracted_root="$install_root/gh_${gh_version}_linux_amd64"

if [[ "${FORTUNE_WORK_GH_FORCE_BOOTSTRAP:-0}" != "1" ]] && command -v gh >/dev/null; then
  gh_bin="$(command -v gh)"
elif [[ -x "$extracted_root/bin/gh" ]]; then
  gh_bin="$extracted_root/bin/gh"
else
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

probe_gh_auth() {
  if GH_PROMPT_DISABLED=1 "$gh_bin" auth status --hostname github.com \
    >/dev/null 2>&1; then
    echo "GH_AUTH_READY"
    return 0
  fi
  echo "GH_AUTH_UNAVAILABLE"
  return 1
}

case "${1:-}" in
  --check)
    echo "GH_BINARY_READY path=$gh_bin"
    # Auth is a separate capability. A missing session must not fail a
    # connector-supported WORK operation or this general environment check.
    probe_gh_auth || true
    exit 0
    ;;
  --require-gh-auth)
    echo "GH_BINARY_READY path=$gh_bin"
    if ! probe_gh_auth; then
      echo "ERROR: authenticated gh capability is unavailable" >&2
      exit 3
    fi
    exit 0
    ;;
esac

if [[ "$#" -gt 0 ]]; then
  PATH="$(dirname "$gh_bin"):$PATH" exec "$@"
fi

echo "$gh_bin"
