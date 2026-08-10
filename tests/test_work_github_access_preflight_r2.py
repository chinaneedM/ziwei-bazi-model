import hashlib
import os
import secrets
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = PROJECT_ROOT / "scripts/bootstrap-work-env.sh"
ROUTING_CONTRACT = PROJECT_ROOT / "docs/WORK-GITHUB-ACCESS-R2.md"
CREDENTIAL_GUARD = PROJECT_ROOT / "scripts/check-no-github-credentials.py"


class WorkGitHubAccessPreflightR2Tests(unittest.TestCase):
    def _fake_gh(self, path: Path) -> None:
        path.write_text(
            """#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == "auth" && "${2:-}" == "status" ]]; then
  if [[ -n "${GH_TOKEN:-${GITHUB_TOKEN:-}}" ]]; then
    exit 0
  fi
  exit "${FAKE_GH_AUTH_EXIT:-1}"
fi
echo "fake gh"
""",
            encoding="utf-8",
        )
        path.chmod(0o755)

    def _run(self, *args: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        clean_env = os.environ.copy()
        clean_env.pop("GH_TOKEN", None)
        clean_env.pop("GITHUB_TOKEN", None)
        clean_env.update(env)
        return subprocess.run(
            [str(BOOTSTRAP), *args],
            cwd=PROJECT_ROOT,
            env=clean_env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_system_gh_present_binary_ready_auth_unavailable(self):
        with tempfile.TemporaryDirectory() as temporary:
            bin_dir = Path(temporary) / "bin"
            bin_dir.mkdir()
            fake_gh = bin_dir / "gh"
            self._fake_gh(fake_gh)
            result = self._run(
                "--check",
                env={"PATH": f"{bin_dir}:/usr/bin:/bin", "FAKE_GH_AUTH_EXIT": "1"},
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"GH_BINARY_READY path={fake_gh}", result.stdout)
        self.assertIn("GH_AUTH_UNAVAILABLE", result.stdout)
        self.assertNotIn("GH_AUTH_READY", result.stdout)

    def test_system_gh_absent_pinned_sha_bootstrap_succeeds(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            payload_root = root / "payload" / "gh_2.96.0_linux_amd64" / "bin"
            payload_root.mkdir(parents=True)
            self._fake_gh(payload_root / "gh")
            archive = root / "fixture.tar.gz"
            with tarfile.open(archive, "w:gz") as bundle:
                bundle.add(payload_root.parent, arcname="gh_2.96.0_linux_amd64")

            shim_dir = root / "shim"
            shim_dir.mkdir()
            (shim_dir / "curl").write_text(
                """#!/usr/bin/env bash
set -euo pipefail
output=""
while [[ $# -gt 0 ]]; do
  if [[ "$1" == "--output" ]]; then output="$2"; shift 2; else shift; fi
done
cp "$FIXTURE_GH_ARCHIVE" "$output"
""",
                encoding="utf-8",
            )
            (shim_dir / "sha256sum").write_text(
                """#!/usr/bin/env bash
set -euo pipefail
read -r expected path
expected="${expected%  }"
[[ "$expected" == "83d5c2ccad5498f58bf6368acb1ab32588cf43ab3a4b1c301bf36328b1c8bd60" ]]
actual="$(/usr/bin/sha256sum "$path" | /usr/bin/cut -d ' ' -f 1)"
[[ "$actual" == "$FIXTURE_GH_SHA256" ]]
echo "$path: OK"
""",
                encoding="utf-8",
            )
            (shim_dir / "curl").chmod(0o755)
            (shim_dir / "sha256sum").chmod(0o755)
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            install_root = root / "install"
            result = self._run(
                "--check",
                env={
                    "PATH": f"{shim_dir}:/usr/bin:/bin",
                    "FORTUNE_WORK_GH_FORCE_BOOTSTRAP": "1",
                    "FORTUNE_WORK_GH_INSTALL_ROOT": str(install_root),
                    "FIXTURE_GH_ARCHIVE": str(archive),
                    "FIXTURE_GH_SHA256": digest,
                },
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("gh_2.96.0_linux_amd64/bin/gh", result.stdout)
        self.assertIn("GH_BINARY_READY", result.stdout)
        self.assertIn("GH_AUTH_UNAVAILABLE", result.stdout)

    def test_env_backed_auth_is_detected_without_output_or_persistence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fake_gh = root / "gh"
            self._fake_gh(fake_gh)
            synthetic_value = "fixture-" + secrets.token_hex(24)
            result = self._run(
                "--check",
                env={"PATH": f"{root}:/usr/bin:/bin", "GH_TOKEN": synthetic_value},
            )
            persisted = [
                path
                for path in root.rglob("*")
                if path.is_file() and path != fake_gh
            ]
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("GH_AUTH_READY", result.stdout)
        self.assertNotIn(synthetic_value, result.stdout + result.stderr)
        self.assertEqual(persisted, [])

    def test_require_auth_fails_only_auth_capability(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._fake_gh(root / "gh")
            result = self._run(
                "--require-gh-auth",
                env={"PATH": f"{root}:/usr/bin:/bin", "FAKE_GH_AUTH_EXIT": "1"},
            )
        self.assertEqual(result.returncode, 3)
        self.assertIn("GH_BINARY_READY", result.stdout)
        self.assertIn("GH_AUTH_UNAVAILABLE", result.stdout)
        self.assertIn("authenticated gh capability is unavailable", result.stderr)

    def test_connector_supported_check_does_not_false_fail_without_gh_auth(self):
        contract = ROUTING_CONTRACT.read_text(encoding="utf-8")
        self.assertIn("Connector-first routing", contract)
        self.assertIn("exact-head CI", contract)
        self.assertIn("GH_AUTH_UNAVAILABLE` is not a WORK failure", contract)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._fake_gh(root / "gh")
            result = self._run(
                "--check",
                env={"PATH": f"{root}:/usr/bin:/bin", "FAKE_GH_AUTH_EXIT": "1"},
            )
        self.assertEqual(result.returncode, 0)

    def test_no_github_credential_artifact(self):
        result = subprocess.run(
            ["python", str(CREDENTIAL_GUARD)],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.strip(), "GITHUB_CREDENTIAL_PERSISTENCE=NO")


if __name__ == "__main__":
    unittest.main()
