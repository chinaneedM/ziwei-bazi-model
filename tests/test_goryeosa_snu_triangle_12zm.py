import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-goryeosa-snu-triangle-12zm.py"
s=importlib.util.spec_from_file_location("tw12zm",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test(unittest.TestCase):
 def setUp(self):self.x=list(v.load())
 def bad(self):
  with self.assertRaises(ValueError):v.verify(*self.x)
 def test_ok(self):self.assertEqual(v.verify(*self.x)["status"],"PASS")
 def test_5553_v29_scope(self):self.x[0]["source"]["first_party_snu_guide"]["rows"][2]["work_volumes"]=[31,32,33];self.bad()
 def test_3467_not_5554_copy(self):self.x[0]["three_way_replay"]["eligible_vol52_separate_copy_route"]["source_copy"]="奎 5554";self.bad()
 def test_no_5554_d16(self):self.x[0]["boundaries"]["direct_5554_d16_glyph"]="123";self.bad()
 def test_no_heritage_primary_upgrade(self):self.x[0]["boundaries"]["full_firstparty_heritage_designation_text_read"]=True;self.bad()
 def test_no_oldbook_witness_vote(self):self.x[0]["boundaries"]["independent_old_original_page_votes_added"]=1;self.bad()
 def test_future_focus_allowed(self):
  self.x[2]["historical_audit"]["current_focus"].append("12ZN later")
  self.x[3]["binding"]["source_focus_count"]+=1
  self.x[3]["binding"]["latest_research_focus_prefix"]="12ZN"
  self.assertEqual(v.verify(*self.x)["status"],"PASS")
if __name__=="__main__":unittest.main()
