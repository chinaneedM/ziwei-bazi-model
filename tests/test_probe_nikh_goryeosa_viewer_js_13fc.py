import importlib.util
import unittest
from pathlib import Path
f=Path(__file__).resolve().parents[1]/'scripts'/'probe-nikh-goryeosa-viewer-js-13fc.py'
s=importlib.util.spec_from_file_location('tianwen13fc',f)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)

class SourceEmittedViewerScripts(unittest.TestCase):
    def test_strictly_emitted(self):
        self.assertEqual(m.permitted_urls('<script src="/resources/imageViewer/js/html5_viewer.js?ver=2.0"></script>'), [m.BASE+'/resources/imageViewer/js/html5_viewer.js?ver=2.0'])
    def test_no_invented_full_image_mode(self):
        self.assertEqual(m.permitted_urls('<script src="/common/imageProxy.do?mode=full&filePath=/kr/052/kr_052_1055.jpg"></script>'), [])
    def test_no_rogue_origin_or_query(self):
        markup='<script src="https://evil.invalid/resources/imageViewer/js/html5_viewer.js?ver=2.0"></script><script src="/resources/imageViewer/js/html5_viewer.js?ver=1.0"></script>'
        self.assertEqual(m.permitted_urls(markup), [])
    def test_duplicate_scripts_do_not_count_independently(self):
        one='<script src="/resources/imageViewer/js/html5_viewer.config.js?ver=2.0"></script>'
        self.assertEqual(len(m.permitted_urls(one+one)), 1)
    def test_script_and_context_are_bounded(self):
        out=m.permitted_urls('<script src="/resources/imageViewer/js/html5_viewer.js?ver=2.0"></script>')
        self.assertEqual(len(out),1)
        self.assertLessEqual(len(m.contexts('imageProxy mode download '*100)),18)

if __name__ == '__main__':
    unittest.main()
