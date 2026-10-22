import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-institutional-d18-tail-13ck.py"
spec=importlib.util.spec_from_file_location("goryeosa13ck",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Source13CK(unittest.TestCase):
 def setUp(self):
  self.e=m.load(m.E);self.s=m.load(m.S);self.l=m.load(m.L);self.reg=m.load(m.R);self.old=m.load(m.OLD)
 def check(self,e=None,s=None,l=None,reg=None,old=None):
  return m.check(self.e if e is None else e,self.s if s is None else s,self.l if l is None else l,self.reg if reg is None else reg,self.old if old is None else old)
 def test_pass(self):self.assertTrue(self.check())
 def test_fake_original_terminal_three(self):
  e=copy.deepcopy(self.e);e["previously_sha_bound_original"]["original_glyph_literal"]=m.KR
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_silent_electronic_text_emendation(self):
  e=copy.deepcopy(self.e);e["directly_observed_received_rows"][2]["institutional"]["yingsuoji"]=m.WK
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_wrong_column_label(self):
  e=copy.deepcopy(self.e);e["live_html_snapshot_boundaries"]["institutional_display_header_order"][3]="盈縮加分"
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_faked_live_html_digest(self):
  e=copy.deepcopy(self.e);e["live_html_snapshot_boundaries"]["sha256_of_live_html_download"]="0"*64
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_false_physical_copy_vote(self):
  e=copy.deepcopy(self.e);e["new_evidence_scope"]["independent_stemmatic_votes"]=1
  with self.assertRaises(AssertionError):self.check(e=e)
 def test_future_state_append(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l);s["schema_version"]="1.999.0";s["historical_audit"]["current_focus"].append("13ZZ future")
  s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="1.999.0"
  l["binding"]["reviewed_state_version"]="1.999.0";l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"]);l["binding"]["latest_research_focus_prefix"]="13ZZ"
  self.assertTrue(self.check(s=s,l=l))
if __name__=="__main__":unittest.main()
