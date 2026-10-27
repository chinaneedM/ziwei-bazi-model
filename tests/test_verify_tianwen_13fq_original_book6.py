import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('original13fq',ROOT/'scripts/verify-tianwen-13fq-original-book6.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class OriginalBook6(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=json.loads((ROOT/v.E).read_text())
 def reject(self,change):
  e=copy.deepcopy(self.e);change(e)
  with self.assertRaises(AssertionError):v.check(e)
 def test_original_payloads_and_pixel_rois(self):self.assertTrue(v.check(self.e))
 def test_reject_wrong_catalog(self):self.reject(lambda e:e['original_binding'].update(catalog='GK03467_02'))
 def test_reject_wrong_work(self):self.reject(lambda e:e['original_binding'].update(work_juan=53))
 def test_reject_pixel_substitution(self):self.reject(lambda e:e['glyph_rois'][1].update(rgb_sha256='0'*64))
 def test_reject_provider_payload_substitution(self):self.reject(lambda e:e['snapshots'][0].update(sha256='0'*64))
 def test_reject_d5_winner(self):self.reject(lambda e:e['bounded_glyph_reading'].update(D5_historical_winner='五一七二'))
 def test_reject_six_edition_votes(self):self.reject(lambda e:e['boundaries'].update(six_downloads_are_six_independent_editions=True))
 def test_reject_unit_inference(self):self.reject(lambda e:e['boundaries'].update(fourfen_to_chudu_historical_units='PROVEN'))
if __name__=='__main__':unittest.main()
