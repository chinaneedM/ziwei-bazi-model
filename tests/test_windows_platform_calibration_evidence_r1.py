from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "WINDOWS-PLATFORM-CALIBRATION-0.2.4-TO-0.2.5-20260904.md"
ACCEPTANCE = ROOT / "docs" / "WINDOWS-BINARY-PLATFORM-ACCEPTANCE-R1.md"
README = ROOT / "README.md"


class WindowsPlatformCalibrationEvidenceR1Tests(unittest.TestCase):
    def test_two_version_release_evidence_is_exact_and_closed(self) -> None:
        text = EVIDENCE.read_text(encoding="utf-8")
        for expected in (
            "AUTOMATED_TWO_VERSION_UPDATE_CALIBRATION=ACCEPTED",
            "MANUAL_WINDOWS_BROWSER_ACCEPTANCE=PENDING",
            "WINDOWS_BINARY_PLATFORM_ACCEPTANCE=PENDING_PLATFORM_ACCEPTANCE",
            "7c20668b4ad301fc549beb4cd183d3ae69efbae7",
            "2b6b836879700a2ff8f20d75c7d7af76dc867b1a",
            "d26321a0aa0956e6056852548a9cad5a0721432fc5270d1dfe65c3f1a47fc6df",
            "be3a2ec32c16d5ef8774287048483b75b6f3bab68699e8f39c77bd4aa31f8d0e",
            "ce05f47623291ab2d07fb94750fd79e5884aa8718d5dfd1e13666ffb627ab7ce",
            "33850578562",
            "33851789847",
            "activation_complete_tree_replacement=true",
            "rollback_complete_old_tree_restored=true",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_overall_windows_acceptance_remains_manual_browser_pending(self) -> None:
        acceptance = ACCEPTANCE.read_text(encoding="utf-8")
        self.assertIn("AUTOMATED_TWO_VERSION_UPDATE_CALIBRATION=ACCEPTED", acceptance)
        self.assertIn("MANUAL_WINDOWS_BROWSER_ACCEPTANCE=PENDING", acceptance)
        self.assertIn("WINDOWS_BINARY_PLATFORM_ACCEPTANCE=PENDING_PLATFORM_ACCEPTANCE", acceptance)
        self.assertNotIn("WINDOWS_BINARY_PLATFORM_ACCEPTANCE=ACCEPTED", acceptance)

        readme = README.read_text(encoding="utf-8")
        self.assertIn("AUTOMATED_TWO_VERSION_UPDATE_CALIBRATION=ACCEPTED", readme)
        self.assertIn("MANUAL_WINDOWS_BROWSER_ACCEPTANCE=PENDING", readme)
        self.assertIn("DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED", readme)


if __name__ == "__main__":
    unittest.main()
