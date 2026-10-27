import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13fk-ncl-fourfen-p74-crossphoto.py"
mod=importlib.util.spec_from_file_location("v13fk",p);v=importlib.util.module_from_spec(mod);mod.loader.exec_module(v)
class Test13FK(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=v.load(v.P);cls.f=v.load(v.F);cls.en=v.load(v.EN);cls.s=v.load(v.S);cls.l=v.load(v.L)
 def test_valid(self):self.assertTrue(v.check(self.e,self.f,self.en,self.s,self.l))
 def reject(self,fn):
  q=copy.deepcopy(self.e);fn(q)
  with self.assertRaises(AssertionError):v.check(q,self.f,self.en,self.s,self.l)
 def test_forged_day7(self):self.reject(lambda q:q["fresh_native_photo_ROIs"][0].update(read_original_fourfen="四分五四九五"))
 def test_forged_nlc_day9(self):self.reject(lambda q:q["fresh_native_photo_ROIs"][2].update(read_original_fourfen="四分五八二〇"))
 def test_forged_day9_match(self):self.reject(lambda q:q["fresh_native_photo_ROIs"][2].update(matches_NIKH_same_day_literal=True))
 def test_wrong_pixel_sha(self):self.reject(lambda q:q["fresh_native_photo_ROIs"][3].update(original_lane_RGB_SHA256="0"*64))
 def test_false_physical_book(self):self.reject(lambda q:q["comparison"].update(same_ancient_physical_book_authenticated=True))
 def test_no_D5_winner(self):self.reject(lambda q:q["comparison"].update(historic_D5_numeric_winner=5172))
 def test_no_d5_original_erasure(self):self.reject(lambda q:q["comparison"].update(NLC_day5_vs_NIKH_day5_opposed_source_photo_glyphs=["四分五一七二","四分五一七二"]))
 def test_registry_no_inflation(self):self.reject(lambda q:q["impact"].update(source_registry_delta=1))
if __name__=="__main__":unittest.main()
