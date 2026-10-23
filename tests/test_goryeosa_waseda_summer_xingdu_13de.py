import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-goryeosa-waseda-summer-xingdu-13de.py"
spec=importlib.util.spec_from_file_location("t13de",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13DE(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.load(m.E);cls.s=m.load(m.S);cls.l=m.load(m.L)
 def go(self,e=None,l=None):return m.check(self.e if e is None else e,self.s,self.l if l is None else l)
 def bad(self,fn):
  e=copy.deepcopy(self.e);fn(e)
  with self.assertRaises(AssertionError):self.go(e=e)
 def test_positive(self):self.assertTrue(self.go())
 def test_false_reading(self):self.bad(lambda e:e["source_native_loci"][1].update(xingdu_literal="初度九十六四五四九"))
 def test_false_day_relabel(self):self.bad(lambda e:e["source_native_loci"][1].update(waseda_printed_day=28))
 def test_false_waseda_jpeg(self):self.bad(lambda e:e["holding"]["source_jpegs"][1].update(sha256="0"*64))
 def test_false_original_roi(self):self.bad(lambda e:e["source_native_loci"][1].update(xingdu_rgb_sha256="0"*64))
 def test_false_witness_vote(self):self.bad(lambda e:e["adjudication"].update(new_stemmatic_votes=1))
 def test_false_ancestor_winner(self):self.bad(lambda e:e["adjudication"].update(early_archetype_winner="PROVEN"))
 def test_global_law_invented(self):self.bad(lambda e:e["cross_original_locus_comparison"].update(scope="PROVEN_TABLE_LAW"))
 def test_a_source_original_is_not_candidate(self):self.bad(lambda e:e["arithmetic_scope"].update(earlier_source_candidate_0_964549_attested=True))
 def test_later_research_focus_keeps_13de_valid(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["schema_version"]="NEXT_REVISION"
  s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]="NEXT_REVISION"
  s["historical_audit"]["current_focus"].append("13DF UNRESOLVED_FUTURE_TEST")
  l["binding"]["reviewed_state_version"]="NEXT_REVISION"
  l["binding"]["latest_research_focus_prefix"]="13DF"
  l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  l["checkpoint_log"].append({"state_version":"NEXT_REVISION","reviewed_issue_ids":[x["id"] for x in l["issues"]]})
  self.assertTrue(m.check(self.e,s,l))
 def test_13de_focus_cannot_be_lost(self):
  s=copy.deepcopy(self.s);l=copy.deepcopy(self.l)
  s["historical_audit"]["current_focus"]=[x for x in s["historical_audit"]["current_focus"] if not x.startswith("13DE ")]
  l["binding"]["source_focus_count"]=len(s["historical_audit"]["current_focus"])
  l["binding"]["latest_research_focus_prefix"]=s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
  with self.assertRaises(AssertionError):m.check(self.e,s,l)
 def test_missed_ledger(self):
  l=copy.deepcopy(self.l);l["binding"]["source_focus_count"]-=1
  with self.assertRaises(AssertionError):self.go(l=l)
if __name__=="__main__":unittest.main()
