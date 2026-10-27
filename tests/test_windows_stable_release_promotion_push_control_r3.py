from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "windows-stable-promote-push.yml"


class WindowsStableReleasePromotionPushControlR3Tests(unittest.TestCase):
    def _workflow(self) -> str:
        return WORKFLOW_PATH.read_text(encoding="utf-8")

    def test_trigger_is_exact_control_branch_and_request_path(self) -> None:
        workflow = self._workflow()
        self.assertIn('"release-control/fortune-chart-stable"', workflow)
        self.assertIn('"release-control/fortune-chart-promotion-request.json"', workflow)
        self.assertIn("push:", workflow)
        self.assertNotIn("pull_request_target", workflow)

    def test_request_object_is_closed_and_validated(self) -> None:
        workflow = self._workflow()
        self.assertIn("FORTUNE-CHART-STABLE-PROMOTION-REQUEST-R1", workflow)
        self.assertIn("schema,source_commit,version", workflow)
        self.assertIn("promotion request fields are not closed", workflow)
        self.assertIn("promotion request schema mismatch", workflow)
        self.assertIn("^[0-9]+\\.[0-9]+\\.[0-9]+$", workflow)
        self.assertIn("^[0-9a-f]{40}$", workflow)

    def test_control_commit_is_not_used_as_product_source(self) -> None:
        workflow = self._workflow()
        control_checkout = workflow.index("Checkout control request commit")
        source_checkout = workflow.index("Checkout requested product source")
        main_gate = workflow.index("promotion source is not exact current main")
        self.assertLess(control_checkout, source_checkout)
        self.assertLess(source_checkout, main_gate)
        self.assertIn("ref: ${{ steps.resolve.outputs.source_commit }}", workflow)
        self.assertIn("git fetch origin main --depth=1", workflow)
        self.assertIn("git rev-parse FETCH_HEAD", workflow)

    def test_version_and_verified_payload_are_bound_to_requested_main(self) -> None:
        workflow = self._workflow()
        self.assertIn("DESKTOP_APPLICATION_VERSION", workflow)
        self.assertIn("promotion version/main mismatch", workflow)
        self.assertIn("build-windows-portable.ps1", workflow)
        self.assertIn('-SourceCommit "$env:SOURCE_COMMIT"', workflow)
        self.assertIn('-ReleaseTag "$env:RELEASE_TAG"', workflow)
        self.assertIn("promotion manifest source commit mismatch", workflow)
        self.assertIn("promotion manifest immutable asset URL mismatch", workflow)
        self.assertIn("promotion release ZIP SHA-256 mismatch", workflow)
        self.assertIn("promotion release ZIP size mismatch", workflow)

    def test_focused_windows_regressions_run_before_publication(self) -> None:
        workflow = self._workflow()
        tests = workflow.index("Run Windows portable/update focused tests")
        build = workflow.index("Build exact-main portable bundle and manifest")
        publish = workflow.index("Publish immutable release then stable manifest pointer")
        self.assertLess(tests, build)
        self.assertLess(build, publish)
        self.assertIn("test_windows_portable_desktop_launcher_r1.py", workflow)
        self.assertIn("test_windows_verified_auto_update_r1.py", workflow)
        self.assertIn("test_windows_stable_release_promotion_branch_r1.py", workflow)
        self.assertIn("test_windows_stable_release_promotion_push_control_r3.py", workflow)

    def test_immutable_release_precedes_manifest_only_stable_pointer(self) -> None:
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
