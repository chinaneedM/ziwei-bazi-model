import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("mod12vq",ROOT/"scripts/verify-yehuobian-modern-edition-12vq.py")
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class ModernBoundary(unittest.TestCase):
 def setUp(self):
  self.r=json.loads((ROOT/v.RECORD).read_text());self.s=json.loads((ROOT/v.SHARD).read_text());self.m=json.loads((ROOT/v.MANIFEST).read_text());self.st=json.loads((ROOT/v.STATE).read_text())
 def bad(self,msg):
  with self.assertRaisesRegex(ValueError,msg):v.validate(self.r,self.s,self.m,self.st)
 def test_initial_evidence(self):self.assertEqual(v.verify()["ancient_target_votes"],0)
 def test_no_1997_source_facsimile_promotion(self):self.r["critical_scope"]["modern_1997_facsimile_status"]="PROVEN";self.bad("1997 format")
 def test_no_1959_physical_look_through(self):self.r["critical_scope"]["modern_1959_typeset_status"]="INSPECTED";self.bad("1959 format")
 def test_2011_syllabus_not_2014(self):self.r["source_readings"][1]["visible_section"]="2014-2015";self.bad("old syllabus")
 def test_two_printed_modern_objects_distinct(self):self.r["source_readings"][1]["asserted_object"]=self.r["source_readings"][0]["asserted_object"];self.bad("two books")
 def test_no_paper_original_image(self):self.r["source_readings"][0]["original_1827_source_image_attested"]=True;self.bad("physical source")
 def test_no_ancient_glyph_vote(self):self.r["accounting"]["new_glyph_votes"]=1;self.bad("no ancient")
 def test_false_contradiction(self):self.r["critical_scope"]["different_modern_items_not_logical_direct_contradiction"]=False;self.bad("false logical")
 def test_registered_source_glyph_not_authorized(self):self.s["sources"][0]["physical_glyph_authority"]=True;self.bad("source register")
 def test_forward_source_growth(self):
  self.m["combined_source_count"]+=1;self.m["extension_source_count"]+=1;self.st["historical_audit"]["external_source_registry_total_unique_count"]+=1
  self.assertEqual(v.validate(self.r,self.s,self.m,self.st)["status"],"PASS")
 def test_count_regression(self):self.m["combined_source_count"]=696;self.bad("must not regress")
if __name__=="__main__":unittest.main()
