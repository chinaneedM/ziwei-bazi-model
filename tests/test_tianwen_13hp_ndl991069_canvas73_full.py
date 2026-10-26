import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "tianwen_13hp", ROOT / "scripts/probe-tianwen-13hp-ndl991069-canvas73-full.py"
)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

class Ndl1909FullSourceAcquisition(unittest.TestCase):
    def test_bounded_source_binding_no_guessed_endpoint(self):
        fake = {
            "@id": M.MANIFEST,
            "sequences": [{"canvases": [{"@id": "https://wrong.invalid"}]*395}],
        }
        with self.assertRaises(ValueError):
            M.source_canvas(fake)

    def test_source_coordinates_scale_not_numeric_guess(self):
        self.assertEqual(M.scaled_box((1020,590,1098,682), (4000,3120)), (2550,1475,2745,1705))
        self.assertEqual(M.scaled_box((866,589,939,680), (4000,3120)), (2165,1473,2348,1700))

    def test_box_bounds_reject_oversized_or_invalid(self):
        for dims in ((6000,4680),(800,624),(4000,0)):
            with self.assertRaises(ValueError): M.scaled_box((866,589,939,680), dims)
        with self.assertRaises(ValueError): M.scaled_box((866,589,1700,680), (4000,3120))

    def test_persisted_scope_is_non_decisive(self):
        self.assertEqual(M.EXPECTED_MANIFEST_SHA,
            "5ef67e4f84917ffd1eafee2b2da1d22f1aeb68f8d7f2ac441b7d398be19bf674")
        self.assertEqual(M.HEADINGS["day14"], (1020,590,1098,682))
        self.assertEqual(M.HEADINGS["day16"], (866,589,939,680))

if __name__ == "__main__":
    unittest.main()
