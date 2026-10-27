import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"probe-nikh-goryeosa-source-atlas-13fe.py"
spec=importlib.util.spec_from_file_location("probe13fe",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
C='proxyFile : "/common/imageProxy.do?";proxyParam : "filePath=";serverContext : "";imgFileRootDir : ""'
J="saveOri : function() { this.cfg.imgFileList[this.cfg.imgFileViewPage] + '&mode=download'; }"
def page(vals):
 return 'var imgArr = ['+','.join('"'+v+'"' for v in vals)+'];viewer.addFile(imgArr);'+''.join('<img data-src="/common/imageProxy.do?mode=thumb&filePath=/'+v+'">' for v in vals)
class Test13FE(unittest.TestCase):
 def setUp(self):self.items=["kr/052/kr_052_%04d.jpg"%n for n in range(1055,1078)]
 def test_first_party_exact_23(self):
  self.assertEqual(m.source_emitted_array(page(self.items)),self.items)
  a=m.permitted_download_urls(page(self.items),C,J)
  self.assertEqual(len(a),23);self.assertEqual(a[0],m.BASE+"/common/imageProxy.do?filePath=/kr/052/kr_052_1055.jpg&mode=download")
 def test_thumb_mismatch_fail(self):self.assertEqual(m.source_emitted_array(page(self.items).replace("1056.jpg","9999.jpg",1)),[])
 def test_extra_file_fail(self):self.assertEqual(m.source_emitted_array(page(self.items+["kr/052/kr_052_1078.jpg"])),[])
 def test_path_escape_fail(self):self.assertEqual(m.source_emitted_array(page(self.items[:-1]+["../../private.jpg"])),[])
 def test_no_download_without_first_party_js(self):self.assertEqual(m.permitted_download_urls(page(self.items),C,J.replace("download","full")),[])
 def test_no_download_without_source_config(self):self.assertEqual(m.permitted_download_urls(page(self.items),C.replace("serverContext : \"\"","serverContext : x"),J),[])
if __name__=="__main__":unittest.main()
