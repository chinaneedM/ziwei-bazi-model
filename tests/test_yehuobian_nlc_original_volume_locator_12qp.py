"""Cross-bound 12QO source page intervals, no unproven negative manuscript claims."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "scripts/yehuobian_nlc_original_volume_locator_12qp.py"
spec = importlib.util.spec_from_file_location("nlc_locator_12qp", P)
loc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loc)


class Test12QPSourceBoundLocator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources, cls.spans = loc.load_index()

    def test_complete_1030_page_navigation_with_two_prelim_pages(self):
        self.assertEqual(loc.coverage(self.sources, self.spans), {
            "source_pages": 1030, "unassigned_prelim": 2,
            "one_candidate": 1020, "two_leaf_shared": 8,
            "volume_page_incidence": 1036, "invalid_coverage": 0,
        })
        self.assertEqual([x["original_volume"] for x in self.spans], list(range(1, 21)))

    def test_eight_mixed_original_volume_boundary_spreads(self):
        cases = [(1,35,1,2),(1,88,3,4),(3,83,6,7),(4,35,8,9),
                 (7,68,13,14),(9,84,16,17),(10,81,18,19),(10,137,19,20)]
        for fasc,page,right,left in cases:
            with self.subTest(fasc=fasc,page=page):
                row = loc.locate_page(self.sources,self.spans,fasc,page)
                self.assertEqual(row["original_volume_candidates"],[right,left])
                self.assertEqual(row["page_scope"],"TWO_LEAF_CROSS_VOLUME_BOUNDARY")
                self.assertEqual((row["right_leaf_candidate_volume"],row["left_leaf_candidate_volume"]),(right,left))
                self.assertFalse(row["can_assert_target_absence"])

    def test_opening_and_nonexclusive_page_and_prelims(self):
        self.assertEqual(loc.locate_page(self.sources,self.spans,1,1)["original_volume_candidates"],[])
        self.assertEqual(loc.locate_page(self.sources,self.spans,1,2)["page_scope"],"PRELIM_OR_UNASSIGNED_OUTSIDE_INDEXED_VOLUME_OPENINGS")
        self.assertEqual(loc.locate_page(self.sources,self.spans,1,3)["original_volume_candidates"],[1])
        self.assertEqual(loc.locate_page(self.sources,self.spans,7,48)["original_volume_candidates"],[13])
        self.assertEqual(loc.locate_page(self.sources,self.spans,7,67)["original_volume_candidates"],[13])
        self.assertEqual(loc.locate_page(self.sources,self.spans,7,69)["original_volume_candidates"],[14])
        self.assertEqual(loc.locate_page(self.sources,self.spans,10,145)["original_volume_candidates"],[20])
        self.assertEqual(loc.locate_page(self.sources,self.spans,10,145)["page_scope"],"END_COLOPHON_CONTEXT_NOT_CERTIFIED_VOLUME_TEXT")
        self.assertEqual(loc.locate_volume(self.spans,14)["end_pdf_page_inclusive"],110)
        self.assertFalse(loc.locate_volume(self.spans,14)["interior_pages_textually_collated"])

    def test_negative_attestation_and_out_of_range_fail_closed(self):
        for f,p in [(0,1),(11,1),(10,146),(1,0)]:
            with self.subTest(f=f,p=p),self.assertRaises(ValueError):
                loc.locate_page(self.sources,self.spans,f,p)
        with self.assertRaises(ValueError):
            loc.locate_volume(self.spans,21)


if __name__ == "__main__":
    unittest.main()
