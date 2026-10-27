import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-kyu-copy-gate-12zc.py"
s=importlib.util.spec_from_file_location("tw12zc",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class GoryeosaCopyScope(unittest.TestCase):
 def setUp(self):self.x=list(v.load())
 def bad(self):
  with self.assertRaises(ValueError):v.verify(*self.x)
 def copy(self,key):return next(x for x in self.x[0]["copies"] if x["key"]==key)
 def test_valid(self):self.assertEqual(v.verify(*self.x)["target_physical_originals_new"],0)
 def test_1613_same_edition(self):self.copy("GK03579_00")["same_edition_as"]="INDEPENDENT_1451_BRANCH";self.bad()
 def test_no_1451_copy(self):self.copy("GK03269_00")["copy_edition_date"]=1451;self.bad()
 def test_7157_supplement_scope(self):self.copy("SHELFMARK_奎7157")["catalog_replaced_work_volumes"]=[52];self.bad()
 def test_7157_no_auto_page_proof(self):self.copy("SHELFMARK_奎7157")["nonlisted_partial_glyph_repairs_excluded_by_catalog"]=True;self.bad()
 def test_5553_supplements(self):self.copy("GK05553_00")["known_replaced_fascicles"]=[8,26];self.bad()
 def test_3269_29_supplements(self):self.copy("GK03269_00")["known_replaced_fascicle_count"]=28;self.bad()
 def test_2015_replica_cannot_vote(self):self.copy("GD00009_00")["target_volume_in_work_range"]=True;self.bad()
 def test_no_phantom_original(self):self.x[0]["closure"]["new_physical_page_images_acquired"]=True;self.bad()
 def test_unreached_target_page(self):self.copy("GK03539_00")["target_volume_scan_bound"]=True;self.bad()
 def test_cadal_not_same_kyu(self):self.x[0]["existing_real_image_boundary"]["cadal_copy_proven_same_as_any_kyudb_copy"]=True;self.bad()
 def test_future_foci(self):
  self.x[2]["historical_audit"]["current_focus"].append("12ZD future")
  self.x[3]["binding"]["source_focus_count"]+=1
  self.x[3]["binding"]["latest_research_focus_prefix"]="12ZD"
  self.assertEqual(v.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
