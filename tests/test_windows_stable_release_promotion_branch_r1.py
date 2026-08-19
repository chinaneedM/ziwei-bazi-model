from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class WindowsStableReleasePromotionBranchR1Tests(unittest.TestCase):
    def test_release_workflow_accepts_only_versioned_tag_or_promotion_branch(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "windows-portable.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("branches:", workflow)
        self.assertIn('"release/fortune-chart-v*"', workflow)
        self.assertIn("tags:", workflow)
        self.assertIn('"fortune-chart-v*"', workflow)
        self.assertIn("refs/heads/release/fortune-chart-v", workflow)
        self.assertIn("refs/tags/fortune-chart-v", workflow)
        self.assertIn("release ref/version mismatch", workflow)
        self.assertIn("malformed release ref", workflow)

    def test_promotion_branch_creates_exact_immutable_tag_from_manifest_commit(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "windows-portable.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("PROMOTION_BRANCH", workflow)
        self.assertIn("PREEXISTING_TAG", workflow)
        self.assertIn("Substring('release/'.Length)", workflow)
        self.assertIn('--verify-tag', workflow)
        self.assertIn('--target "$($manifest.source_commit)"', workflow)
        self.assertIn("immutable FortuneChart release already exists", workflow)
        self.assertIn("release manifest source commit mismatch", workflow)

    def test_stable_pointer_remains_manifest_only_and_fail_closed(self) -> None:
        workflow = (REPO_ROOT / ".github" / "workflows" / "windows-portable.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("fortune-chart-stable", workflow)
        self.assertIn("fortune-chart-update.json", workflow)
        self.assertIn("gh release upload fortune-chart-stable", workflow)
        self.assertIn("--clobber", workflow)
        self.assertIn("stable update manifest publication failed", workflow)
        self.assertNotIn("FortuneChart-windows-x64.zip' `\n            --clobber", workflow)


class WindowsStableReleasePromotionControlR2Tests(unittest.TestCase):
    def _workflow(self) -> str:
        return (REPO_ROOT / ".github" / "workflows" / "windows-stable-promote.yml").read_text(
            encoding="utf-8"
        )

    def test_comment_control_is_owner_issue_and_closed_regex_gated(self) -> None:
        workflow = self._workflow()
        self.assertIn("issue_comment:", workflow)
        self.assertIn("github.event.issue.number == 330", workflow)
        self.assertIn("github.event.comment.user.login == github.repository_owner", workflow)
        self.assertIn("github.event.comment.user.login == 'chinaneedM'", workflow)
        self.assertIn("^/fortune-chart-promote ([0-9]+\\.[0-9]+\\.[0-9]+) ([0-9a-f]{40})\\s*$", workflow)
        self.assertIn("malformed FortuneChart promotion command", workflow)

    def test_comment_control_requires_exact_current_main_and_version(self) -> None:
        workflow = self._workflow()
        self.assertIn("git fetch origin main --depth=1", workflow)
        self.assertIn("git rev-parse FETCH_HEAD", workflow)
        self.assertIn("promotion source is not exact current main", workflow)
        self.assertIn("DESKTOP_APPLICATION_VERSION", workflow)
        self.assertIn("promotion version/main mismatch", workflow)
        self.assertIn("promotion tag/version mismatch", workflow)

    def test_comment_control_reuses_verified_build_and_payload_gates(self) -> None:
        workflow = self._workflow()
        self.assertIn("test_windows_portable_desktop_launcher_r1.py", workflow)
        self.assertIn("test_windows_verified_auto_update_r1.py", workflow)
        self.assertIn("test_windows_stable_release_promotion_branch_r1.py", workflow)
        self.assertIn("build-windows-portable.ps1", workflow)
        self.assertIn("promotion manifest source commit mismatch", workflow)
        self.assertIn("promotion manifest immutable asset URL mismatch", workflow)
        self.assertIn("promotion release ZIP SHA-256 mismatch", workflow)
        self.assertIn("promotion release ZIP size mismatch", workflow)

    def test_comment_control_publishes_immutable_release_before_manifest_only_pointer(self) -> None:
        workflow = self._workflow()
        immutable = workflow.index('gh release create "$env:RELEASE_TAG"')
        stable_upload = workflow.index("gh release upload fortune-chart-stable")
        self.assertLess(immutable, stable_upload)
        self.assertIn("immutable FortuneChart release already exists", workflow)
        self.assertIn('--target "$env:SOURCE_COMMIT"', workflow)
        self.assertIn("stable update manifest publication failed", workflow)
        self.assertNotIn("FortuneChart-windows-x64.zip' `\n            --clobber", workflow)


if __name__ == "__main__":
    unittest.main()
