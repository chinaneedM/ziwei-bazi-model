import importlib.util,json,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'scripts/probe-tianwen-13jk-snu-gk5553-neighbor-controls.py'
sp=importlib.util.spec_from_file_location('jk',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class SourceGated(unittest.TestCase):
 def test_six_volume_controls(self):
  self.assertEqual(m.TARGET_VOL_TOKENS,('0008','0026','0011','0013','0025','0027'))
 def test_empty_source_list_blocks(self):
  self.assertEqual(m.source_listed_targets(m.parse_vols(b'{}')),[])
 def test_only_firstparty_listed(self):
  a=json.dumps({'volList':[{'BOOK_CD':m.BOOK,'ITEM_CD':'GJB','VOL_NO':'0008'},{'BOOK_CD':m.BOOK,'ITEM_CD':'GJB','VOL_NO':'0026'}]}).encode()
  self.assertEqual(m.source_listed_targets(m.parse_vols(a)),['0008','0026'])
 def test_wrong_book_blocks(self):
  a=json.dumps({'volList':[{'BOOK_CD':'GK05554_00','ITEM_CD':'GJB','VOL_NO':'0008'}]}).encode()
  self.assertEqual(m.source_listed_targets(m.parse_vols(a)),[])
 def test_book_identity_gate(self):
  self.assertFalse(m.summarize_catalog(b'Not firstparty GK05553_00')['exact_post_control'])
  self.assertTrue(m.summarize_catalog(b"GK05553_00 fn_mfPdfPopShow('GK05553_00')")['exact_post_control'])
 def test_no_physical_proof_from_digital_text(self):
  a=m.analyze_viewer(b"fn_originalImg('GJB','GK05553_00','0008','001a')",'0008')
  self.assertFalse(a['physical_book_ordinal_verified']);self.assertFalse(a['original_printed_juan_verified'])
if __name__=='__main__':unittest.main()
