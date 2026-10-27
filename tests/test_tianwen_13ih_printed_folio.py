import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('folio13ih', ROOT / 'scripts/verify-tianwen-13ih-printed-folio.py')
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class PrintedFolioTest(unittest.TestCase):
    def test_source_pixels_and_current_ledger(self):
        self.assertTrue(M.check(M.load()))

    def reject(self, edit):
        d = copy.deepcopy(M.load())
        edit(d)
        with self.assertRaises(AssertionError):
            M.check(d, False)

    def test_model_residual_cannot_be_physical_leaf_count(self):
        self.reject(lambda d: d['adjudication'].update(physical_missing_leaf_count=6))

    def test_capture_stage_cannot_be_invented(self):
        for key in ('physical_leaf_loss_proven', 'microfilm_omission_proven', 'digital_omission_proven'):
            with self.subTest(key=key):
                self.reject(lambda d: d['adjudication'].update({key: True}))

    def test_unread_numerals_cannot_be_interpolated(self):
        self.reject(lambda d: d['comparison'].update(p4_left_and_p5_right_folio_numerals=[9, 9]))

    def test_provider_page_number_is_not_original_leaf_number(self):
        self.reject(lambda d: d['direct_folio_readings'][0].update(printed_number=4))

    def test_source_roi_pixel_change_is_detected(self):
        self.reject(lambda d: d['rois'][0].update(rgb_sha256='0' * 64))

    def test_crop_cannot_move_into_adjacent_numeric_column(self):
        self.reject(lambda d: d['rois'][1]['bbox'].__setitem__(0, 2100))

    def test_source_original_cannot_be_replaced_with_other_copy(self):
        self.reject(lambda d: d['native_pages'][0].update(sha256='0' * 64))

    def test_folio_discontinuity_does_not_supply_missing_title(self):
        self.reject(lambda d: d['adjudication'].update(table_title_or_initial_day_leaf_recovered=True))


if __name__ == '__main__':
    unittest.main()
