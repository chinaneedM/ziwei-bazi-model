import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('color13if', ROOT / 'scripts/verify-tianwen-13if-color-coverage.py')
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class ColorCoverageTest(unittest.TestCase):
    def test_native_source_bytes_and_scope(self):
        self.assertTrue(M.check(M.load()))

    def test_selected_twenty_cannot_be_reported_as_acquired_twenty(self):
        data = copy.deepcopy(M.load())
        data['source_contract']['decoded_initial_color_images'] = 20
        with self.assertRaises(AssertionError):
            M.check(data, False)

    def test_navigation_cannot_prove_leaf_loss_or_complete_negative(self):
        for section, key in [('adjudication', 'physical_leaf_loss_proven'), ('adjudication', 'transport_failure_is_nonexistence_proof'), ('navigation_transition', 'all_104_pages_linewise_collated')]:
            with self.subTest(key=key):
                data = copy.deepcopy(M.load())
                data[section][key] = True
                with self.assertRaises(AssertionError):
                    M.check(data, False)

    def test_type_label_cannot_supply_exact_impression_date(self):
        data = copy.deepcopy(M.load())
        data['catalog_scope']['exact_impression_year'] = 1455
        with self.assertRaises(AssertionError):
            M.check(data, False)

    def test_wrong_source_image_hash_rejected(self):
        data = copy.deepcopy(M.load())
        data['images'][1]['jpeg_sha256'] = '0' * 64
        with self.assertRaises(AssertionError):
            M.check(data, False)


if __name__ == '__main__':
    unittest.main()
