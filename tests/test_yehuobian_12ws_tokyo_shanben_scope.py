import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("ws",ROOT/"scripts/verify-yehuobian-12ws-tokyo-shanben-scope.py")
p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
class TokyoSourceFirstParty(unittest.TestCase):
 def setUp(self):
  self.r=p.json.loads((ROOT/p.R).read_text());self.s=p.json.loads((ROOT/p.S).read_text());self.code=(ROOT/p.P).read_text()
 def bad(self,msg):
  with self.assertRaisesRegex(ValueError,msg):p.validate(self.r,self.s,self.code)
 def test_live_gate(self):self.assertEqual(p.verify()["ancient_print_votes"],0)
 def test_query_echo_correct(self):
  self.code=self.code.replace("actual_index_result_count_from_visible_count","")
  self.bad("query-echo")
 def test_one_result_not_zero(self):
  self.r["source_capture"][2]["visible_result_count"]=1;self.bad("bounded 0-row")
 def test_absence_not_proved(self):
  self.r["inference"]["index_no_hit_does_not_prove_physical_holding_absence"]=False;self.bad("absence/paper")
 def test_catalog_item_not_swapped(self):
  self.r["catalog_items"][1]["copy_item"]="6403767830";self.bad("distinct catalog")
 def test_original_not_acquired(self):
  self.r["catalog_items"][0]["original_folio_image_obtained"]=True;self.bad("distinct catalog")
 def test_digests_must_match(self):
  self.r["source_capture"][0]["zip_sha256"]="a"*64;self.bad("original ZIP")
 def test_no_new_source_vote(self):
  self.r["inference"]["source_registry_additions"]=1;self.bad("scope frozen")
if __name__=="__main__":unittest.main()
