import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("xf",ROOT/"scripts/verify-yehuobian-utokyo-digital-access-12xf.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class DigitalSurfaceScope(unittest.TestCase):
 def setUp(self):
  self.d=m.j(m.REC);self.w=m.j(m.WZ);self.x=m.j(m.XA);self.e=m.j(m.XE);self.s=m.j(m.STATE);self.mn=m.j(m.MAN)
 def bad(self,msg):
  with self.assertRaisesRegex(ValueError,msg):m.validate(self.d,self.w,self.x,self.e,self.s,self.mn)
 def snap(self,id):return next(x for x in self.d["source_snapshots"] if x["id"]==id)
 def test_live(self):self.assertEqual(m.verify()["target_original_folios"],0)
 def test_2009_temporality(self):self.snap("SHANBEN_FULLIMAGE")["date"]="2026-10";self.bad("dated image intro")
 def test_AB_count(self):self.snap("SHANBEN_FULLIMAGE")["A_full_global"]=999;self.bad("historical A/B")
 def test_AB_imputed_item(self):self.snap("SHANBEN_FULLIMAGE")["object_matches"]=["6403767830"];self.bad("historical A/B")
 def test_selected_result_not_global(self):self.snap("SHANBEN_SELECTED_LIST")["interpretation"]="NO_HOLDINGS";self.bad("no global negative")
 def test_title_zero_false(self):self.snap("SHANBEN_SELECTED_LIST")["title_hits_in_selected_search"]=1;self.bad("bounded historical search")
 def test_kuraishi_lectures_not_book(self):self.snap("KURAISHI_LECTURE")["interpretation"]="ORIGINAL_PRINT_IMAGE";self.bad("personal lectures false positive")
 def test_kuraishi_35_not_40(self):self.snap("KURAISHI_LECTURE")["digitized_notebooks"]=40;self.bad("lecture notebooks")
 def test_NIJL_not_original(self):self.snap("NIJL_PARTNER")["object_matches"]=["6403148395"];self.bad("NIJL no item match")
 def test_Oki_not_Kuraishi(self):self.d["original_items"][0]["barcode"]="6403148395";self.bad("original copy identifiers")
 def test_original_image_not_found(self):self.d["original_items"][1]["original_leaf_image_found"]=True;self.bad("no printed folio evidence")
 def test_no_artificial_glyph(self):self.d["historical_glyph_votes"]=1;self.bad("no fabricated evidence")
 def test_registry_not_added(self):self.d["invariants"]["extensions"]=60;self.bad("registry counts")
 def test_no_genealogy_edge(self):self.d["transmission_impact"]["edges_supported"]=["1827→1869"];self.bad("no transmission promoted")
if __name__=="__main__":unittest.main()
