import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13ld-naaj-mingshi-juan35-source-route.py"
s=importlib.util.spec_from_file_location("tw13ld",p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Route(unittest.TestCase):
 def setUp(self):self.a=copy.deepcopy(list(v.load()))
 def fails(self):
  with self.assertRaises(ValueError):v.verify(*self.a)
 def test_good(self):self.assertEqual(v.verify(*self.a)["exact_book_order"],"0011")
 def test_copy_conflation(self):self.a[0]["cross_holdings_control"]["same_holding_as_2810038_proven"]=True;self.fails()
 def test_fake_numeric(self):self.a[0]["scope"]["new_confirmed_original_numeric_winners"]=1;self.fails()
 def test_fake_download(self):self.a[0]["commons_source_route"]["original_pdf_bytes_acquired"]=True;self.fails()
 def test_wrong_juan(self):self.a[0]["original_catalog"]["target_book_order"]="0010";self.fails()
 def test_future_append(self):
  self.a[1]["historical_audit"]["current_focus"].append("13LE later successful source retrieval")
  self.a[2]["binding"]["source_focus_count"]+=1
  self.a[2]["binding"]["latest_research_focus_prefix"]="13LE"
  self.a[2]["issues"][4]["next_action"]="13LE CURRENT ACTION: later positive original"
  self.assertEqual(v.verify(*self.a)["status"],"PASS")
if __name__=="__main__":unittest.main()
