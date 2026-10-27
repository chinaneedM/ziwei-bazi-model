import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-six-day-source-pixel-intersections-13et.py"
spec=importlib.util.spec_from_file_location("v13et",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13ET(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=m.read(m.E);cls.es=m.read(m.ES);cls.en=m.read(m.EN);cls.s=m.read(m.S);cls.l=m.read(m.L)
    def check(self,e=None):
        return m.check(self.e if e is None else e,self.es,self.en,self.s,self.l)
    def bad(self,change):
        e=copy.deepcopy(self.e);change(e)
        with self.assertRaises(AssertionError):self.check(e)
    def test_metadata(self):self.assertTrue(self.check())
    def test_tampered_source_page(self):self.bad(lambda e:e["source"]["original_pages"][0].update(png_sha256="0"*64))
    def test_tampered_crop_sha(self):self.bad(lambda e:e["intersection_source_pixel_samples"][1].update(intersection_rgb_sha256="0"*64))
    def test_tampered_roi_bbox(self):self.bad(lambda e:e["intersection_source_pixel_samples"][2]["intersection_bbox"].__setitem__(0,99))
    def test_tampered_dark_count(self):self.bad(lambda e:e["intersection_source_pixel_samples"][3]["dark_rgb_mean_lt_counts"].update({"90":0}))
    def test_fake_ink_proof(self):self.bad(lambda e:e["findings"].update(shared_crop_dark_pixels_do_not_prove_shared_glyph_ink=False))
    def test_imputed_numeric(self):self.bad(lambda e:e["findings"]["complete_original_historical_fourfen_numeric"].__setitem__(0,"0.4524"))
    def test_false_tail_completion(self):self.bad(lambda e:e["source_original_lower_fourfen_tail_scope"]["complete_fourfen_tail_strings"].__setitem__(2,"一二"))
    def test_fake_independent_source(self):self.bad(lambda e:e["source"].update(new_independent_original_witnesses=1))
    def test_reopened_algorithm(self):self.bad(lambda e:e["impact"].update(algorithm_reopens=1))
if __name__=="__main__":unittest.main()
