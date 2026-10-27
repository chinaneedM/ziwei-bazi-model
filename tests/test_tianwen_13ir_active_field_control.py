import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "v13ir", ROOT / "scripts" / "verify-tianwen-13ir-active-field-control.py"
)
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)

class Evidence(unittest.TestCase):
    def test_current_active_controls(self):
        self.assertTrue(verifier.check(verifier.load()))

    def test_solar_d30_remains_null(self):
        record = copy.deepcopy(verifier.load())
        record["source_controls"][0]["value"] = 13
        with self.assertRaises(AssertionError):
            verifier.check(record, with_state=False)

    def test_preserve_13ei_retraction(self):
        record = copy.deepcopy(verifier.load())
        record["source_controls"][2]["status"] = "RESOLVED"
        with self.assertRaises(AssertionError):
            verifier.check(record, with_state=False)

    def test_no_new_historic_source(self):
        record = copy.deepcopy(verifier.load())
        record["file_policy"]["source_images_added"] = 1
        with self.assertRaises(AssertionError):
            verifier.check(record, with_state=False)

if __name__ == "__main__":
    unittest.main()
