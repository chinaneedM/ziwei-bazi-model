import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-solar-d4-d30-prefix-geometry-13eh.py"
spec=importlib.util.spec_from_file_location("v13eh",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13EH(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=m.read(m.E);cls.s=m.read(m.S);cls.l=m.read(m.L);cls.eg=m.read(m.EG);cls.ef=m.read(m.EF);cls.ed=m.read(m.ED)
 def go(self,e=None,l=None):
  return m.check(self.e if e is None else e,self.s,self.l if l is None else l,self.eg,self.ef,self.ed)
 def reject(self,edit):
  e=copy.deepcopy(self.e);edit(e)
  with self.assertRaises(AssertionError):self.go(e)
 def test_bound_original(self):self.assertTrue(self.go())
 def test_fake_day4_roi(self):self.reject(lambda e:e["pages"][1]["rois"][1].update(rgb_sha256="0"*64))
 def test_fake_day30_bbox(self):self.reject(lambda e:e["pages"][2]["rois"][1].update(bbox=[590,418,617,830]))
 def test_fake_day4_heading(self):self.reject(lambda e:e["pages"][1]["day_heading"].update(source_literal="五日"))
 def test_false_offset(self):self.reject(lambda e:e["relative_column_observation"]["day4"].update(offset_px=25))
 def test_fabricated_d30_number(self):self.reject(lambda e:e["open_questions"].update(day30_original_numeric_decimal="0.965038"))
 def test_fabricated_field_mapping(self):self.reject(lambda e:e["open_questions"].update(technical_name_to_full_numeric_lane_binding="PROVEN"))
 def test_fabricated_independent_copy(self):self.reject(lambda e:e["impact"].update(new_independent_physical_witnesses=1))
 def test_action_rollback(self):
  l=copy.deepcopy(self.l);x=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
  x["next_action"]=next(h for h in x["history"] if h.get("revision_id")=="TW-OPEN-0005-13EH-SAME-SOURCE-PREFIX-GEOMETRY-20261023")["previous_next_action"]
  with self.assertRaises(AssertionError):self.go(l=l)
if __name__=="__main__":unittest.main()
