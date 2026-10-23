import copy,importlib.util,unittest
from pathlib import Path
path=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-p74-d4-d5-triple-lane-13ej.py"
spec=importlib.util.spec_from_file_location("v13ej",path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13EJ(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.e=m.read(m.E);cls.s=m.read(m.S);cls.l=m.read(m.L);cls.ei=m.read(m.EI);cls.eg=m.read(m.EG);cls.ed=m.read(m.ED)
 def go(self,e=None,l=None):return m.check(self.e if e is None else e,self.s,self.l if l is None else l,self.ei,self.eg,self.ed)
 def reject(self,fn):
  x=copy.deepcopy(self.e);fn(x)
  with self.assertRaises(AssertionError):self.go(e=x)
 def test_original(self):self.assertTrue(self.go())
 def test_wrong_heading(self):self.reject(lambda e:e["rois"][1].update(visible="六日"))
 def test_wrong_d4_bbox(self):self.reject(lambda e:e["rois"][2].update(bbox=[922,406,944,526]))
 def test_fake_roi_hash(self):self.reject(lambda e:e["rois"][6].update(rgb_sha256="0"*64))
 def test_fake_d30_decimal(self):self.reject(lambda e:e["observations"].update(d30_exact_numeric="0.965038"))
 def test_fake_technical_bridge(self):self.reject(lambda e:e["observations"].update(technical_semantic_relation_p73="PROVEN"))
 def test_fake_copy(self):self.reject(lambda e:e["impact"].update(new_ancient_witnesses=1))
if __name__=="__main__":unittest.main()
