import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-nikh-goryeosa-target-retry-13ff.py"
s=importlib.util.spec_from_file_location("retry13ff",p)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)
class Test13FF(unittest.TestCase):
 def setUp(self):self.urls=[m.m.BASE+"/common/imageProxy.do?filePath=/kr/052/kr_052_%04d.jpg&mode=download"%k for k in range(1055,1078)]
 def test_positive_exact_publisher_positions(self):
  self.assertEqual([z[0] for z in m.retry_plan(self.urls)],[3,4])
 def test_no_other_modern_name(self):
  z=self.urls.copy();z[2]=z[2].replace("1057","9999")
  self.assertEqual(m.retry_plan(z),[])
 def test_no_non_publisher(self):
  z=self.urls.copy();z[3]=z[3].replace("db.history.go.kr","evil.invalid")
  self.assertEqual(m.retry_plan(z),[])
 def test_no_enumerated_24th(self):
  self.assertEqual(m.retry_plan(self.urls+self.urls[:1]),[])
if __name__=="__main__":unittest.main()
