import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-tianwen-13fh-snu-gk5553.py"
spec=importlib.util.spec_from_file_location("m13fh",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13FH(unittest.TestCase):
 def test_bounded_microfilm_explicit_only(self):
  s="M/F74-102-17-1, M/F74-102-17-3, M/F74-102-17-7"
  self.assertEqual(m.microfilm_literals(s),["M/F74-102-17-1","M/F74-102-17-3","M/F74-102-17-7"])
 def test_cannot_infer_juan52_from_microfilm_sequence(self):
  s="139卷 46冊 M/F74-102-17-3(奎 5553/v.17-24) 卷52"
  self.assertEqual(m.microfilm_literals(s),["M/F74-102-17-3"])
  self.assertNotIn("v.17-24",m.microfilm_literals(s))
 def test_no_false_early_glyph(self):
  self.assertNotIn("古",m.bounded_context("第8·26·29冊(合3冊)이 補寫本","卷52"))
 def test_text_extraction(self):
  h=m.Text();h.feed("<div>奎貴5553</div><span>乙亥字</span>")
  self.assertEqual(" ".join(h.parts),"奎貴5553 乙亥字")
if __name__=="__main__":unittest.main()
