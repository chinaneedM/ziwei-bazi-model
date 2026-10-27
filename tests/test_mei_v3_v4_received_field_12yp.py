import unittest, importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-mei-v3-v4-received-field-12yp.py"
sp=importlib.util.spec_from_file_location("tianwen_12yp",p);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class TestReceivedFieldFirewall(unittest.TestCase):
 def setUp(self):self.x=list(v.read())
 def rejected(self):
  with self.assertRaises(ValueError):v.verify(*self.x)
 def test_clean(self):self.assertEqual(v.verify(*self.x)["received_numerical_roles"],6)
 def test_fake_original(self):self.x[0]["original_print_impact"]["mei_original_page_readings"]=1;self.rejected()
 def test_invalid_pingli(self):self.x[0]["controls"][3]["decimal"]="4.9286";self.rejected()
 def test_wrong_daily_diff(self):self.x[0]["controls"][4]["decimal"]="0.0185";self.rejected()
 def test_fake_1971_original(self):self.x[0]["source_presentations"][4]["original_17TH_18TH_print"]=True;self.rejected()
 def test_fake_ancestor(self):self.x[0]["rule_relationships"][0]["historical_shared_physical_copy_proven"]=True;self.rejected()
 def test_reopen_chart(self):self.x[0]["original_print_impact"]["new_algorithm_reopens"]=1;self.rejected()
 def test_close_issue(self):next(y for y in self.x[1]["issues"] if y["id"]=="TW-OPEN-0005")["status"]="RESOLVED";self.rejected()
 def test_old_version(self):self.x[2]["schema_version"]="1.629.0";self.rejected()
 def test_future_focus_allowed(self):self.x[2]["historical_audit"]["current_focus"].append("12YQ FUTURE");self.assertEqual(v.verify(*self.x)["status"],"PASS")
 def test_missing_focus_disallowed(self):self.x[2]["historical_audit"]["current_focus"]=[x for x in self.x[2]["historical_audit"]["current_focus"] if not x.startswith("12YP ")];self.rejected()
if __name__=="__main__":unittest.main()
