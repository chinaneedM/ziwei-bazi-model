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


if __name__ == "__main__":
    unittest.main()
