import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('berlin12vm', ROOT/'scripts/verify-yehuobian-berlin-prior-samples-12vm.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class PriorSamples(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT/mod.RECORD).read_text())
        self.docs = [json.loads((ROOT/x['path']).read_text()) for x in self.record['prior_records']]

    def test_real_records_join(self):
        self.assertEqual(mod.verify(), {'historical_samples_reviewed':38, 'new_target_glyph_votes':0})

    def test_other_ppn_cannot_inherit_sample_nonhit(self):
        self.record['object']['ppn'] = 'PPN_OTHER'
        with self.assertRaisesRegex(ValueError, 'object identity'):
            mod.validate(self.record, *self.docs)

    def test_partial_or_duplicate_coverage_rejected(self):
        for replacement in [self.docs[2]['all_original_jpegs_source_sha256'][:-1], [self.docs[2]['all_original_jpegs_source_sha256'][0]]*38]:
            docs = copy.deepcopy(self.docs)
            docs[2]['all_original_jpegs_source_sha256'] = replacement
            with self.assertRaises(ValueError):
                mod.validate(self.record, *docs)

    def test_sample_nonhit_never_full_print_absence(self):
        self.record['historical_observation']['full_1827_juan20_negative_claim_allowed'] = True
        with self.assertRaisesRegex(ValueError, 'full print absence'):
            mod.validate(self.record, *self.docs)

    def test_archive_metadata_not_new_visual_review(self):
        self.record['current_session']['new_images_reviewed'] = 38
        with self.assertRaisesRegex(ValueError, 'new review'):
            mod.validate(self.record, *self.docs)

    def test_no_new_glyph_from_restored_sample_history(self):
        self.record['accounting']['new_target_glyph_votes'] = 1
        with self.assertRaisesRegex(ValueError, 'evidence promotion'):
            mod.validate(self.record, *self.docs)

if __name__ == '__main__':
    unittest.main()
