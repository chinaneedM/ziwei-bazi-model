import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('tianwen13ie', ROOT / 'scripts/verify-tianwen-13ie-gk3467-winter-source.py')
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class SourceEvidenceTest(unittest.TestCase):
    def test_actual_native_evidence(self):
        self.assertTrue(M.check(M.load()))

    def test_counterfactual_cannot_replace_original(self):
        data = copy.deepcopy(M.load())
        data['direct_rows'][1]['literal'] = '五分二三六二'
        data['direct_rows'][1]['local_integer'] = 52362
        with self.assertRaises(AssertionError):
            M.check(data, False)

    def test_day_heading_swap_rejected(self):
        data = copy.deepcopy(M.load())
        data['direct_rows'][1]['header_key'] = 'D15_HEADER'
        with self.assertRaises(AssertionError):
            M.check(data, False)

    def test_roi_cannot_move_to_adjacent_lane(self):
        data = copy.deepcopy(M.load())
        data['rois'][3]['bbox'][0] += 30
        with self.assertRaises(AssertionError):
            M.check(data, False)

    def test_unseen_title_and_physical_loss_not_certified(self):
        for section, key, value in [('field_identity', 'winter_table_title_on_inspected_pages', '大陽冬至前後二象盈初縮末限'), ('source_coverage', 'physical_leaf_loss_proven', True), ('source', 'physical_impression_year', 1455)]:
            with self.subTest(key=key):
                data = copy.deepcopy(M.load())
                data[section][key] = value
                with self.assertRaises(AssertionError):
                    M.check(data, False)


if __name__ == '__main__':
    unittest.main()
