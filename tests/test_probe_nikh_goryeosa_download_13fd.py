import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'scripts'/'probe-nikh-goryeosa-download-13fd.py'
s=importlib.util.spec_from_file_location('tianwen13fd',p)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)
C='proxyFile : "/common/imageProxy.do?";proxyParam : "filePath=";serverContext : "";imgFileRootDir : ""'
J="saveOri : function() { this.cfg.imgFileList[this.cfg.imgFileViewPage] + '&mode=download'; }"
V='var imgArr = ["kr/052/kr_052_1055.jpg"];viewer.addFile(imgArr)'
class SourceEmittedDownloadGate(unittest.TestCase):
    def test_exact_public_js_contract(self):
        self.assertEqual(m.save_url(C,J,V),m.BASE+'/common/imageProxy.do?filePath=/kr/052/kr_052_1055.jpg&mode=download')
    def test_reject_without_download_mode(self):
        self.assertIsNone(m.save_url(C,J.replace('download','thumb'),V))
    def test_reject_without_source_file(self):
        self.assertIsNone(m.save_url(C,J,V.replace('1055','9999')))
    def test_reject_without_source_config(self):
        self.assertIsNone(m.save_url(C.replace('serverContext : ""','serverContext : "/secret"'),J,V))
    def test_image_magic_not_transcription(self):
        self.assertEqual(m.image_format(b'<!doctype html>'),'NON_IMAGE_OR_UNKNOWN')
        self.assertEqual(m.image_format(b'\xff\xd8\xffanything'),'JPEG')
if __name__=='__main__':
    unittest.main()
