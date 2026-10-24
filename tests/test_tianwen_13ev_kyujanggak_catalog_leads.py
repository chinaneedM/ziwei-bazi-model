import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-tianwen-13ev-kyujanggak-catalog-leads.py"
s=importlib.util.spec_from_file_location("v13ev",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Test13EV(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=m.load(m.P);cls.sh=m.load(m.S);cls.ma=m.load(m.M);cls.c=m.load(m.C);cls.l=m.load(m.L)
 def good(self,x=None,sh=None):return m.check(self.a if x is None else x,self.sh if sh is None else sh,self.ma,self.c,self.l)
 def bad(self,f):
  z=copy.deepcopy(self.a);f(z)
  with self.assertRaises(AssertionError):self.good(z)
 def test_valid(self):self.assertTrue(self.good())
 def test_false_original_glyph(self):self.bad(lambda x:x["catalog_objects"][0].update(exact_d5_glyph="五"))
 def test_false_1613_date_for_3269(self):self.bad(lambda x:x["catalog_objects"][2].update(catalog_impression_date="1613"))
 def test_two_editions_fiction(self):self.bad(lambda x:x["catalog_objects"][1].update(same_edition_group="1613_OTHER_EDITION"))
 def test_mislabel_work52_as_book52(self):self.bad(lambda x:x["next_original_folio_targets"][1].update(exact_book_number=52))
 def test_attach_unverified_krdb_image(self):self.bad(lambda x:x["official_db"].update(actual_image_viewer_target_folio_retrieved=True))
 def test_fake_krdb_snu_copy_link(self):self.bad(lambda x:x["official_db"].update(exact_catalog_object_link="GK03539_00"))
 def test_fake_ancient_witness(self):self.bad(lambda x:x["impact"].update(registered_original_glyph_witnesses_added=3))
 def test_fictitious_g893_reopen(self):self.bad(lambda x:x["barriers"].update(other_early_g893_six_targets="CLOSED"))
 def test_algorithm_reopen(self):self.bad(lambda x:x["impact"].update(algorithm_reopens=1))
 def test_source_becomes_glyph_authority(self):
  z=copy.deepcopy(self.sh);z["sources"][0]["physical_glyph_authority"]=True
  with self.assertRaises(AssertionError):self.good(sh=z)
if __name__=="__main__":unittest.main()
