import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'scripts/verify-tianwen-13ll-naaj-zero-controls.py'
s=importlib.util.spec_from_file_location('tw13ll',p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class PositionedGlyphEvidence(unittest.TestCase):
 def setUp(self):self.d=copy.deepcopy(list(v.load()))
 def bad(self):
  with self.assertRaises(AssertionError):v.check(*self.d)
 def test_source_bound(self):self.assertEqual(v.check(*self.d)['paired_glyphs'],4)
 def test_fake_same_plate(self):self.d[0]['interpretation']['same_woodblock_proven']=True;self.bad()
 def test_fake_date(self):self.d[0]['interpretation']['exact_impression_year_proven']=True;self.bad()
 def test_fake_wrong_symbol(self):self.d[0]['interpretation']['wrong_jbig2_symbol_substitution_proven']=True;self.bad()
 def test_count_components_as_damage(self):self.d[0]['interpretation']['component_count_is_not_historical_break_count']=False;self.bad()
 def test_fake_new_recension(self):self.d[0]['interpretation']['new_independent_recensions']=2;self.bad()
 def test_fake_new_constant(self):self.d[0]['interpretation']['second_control_decimal_value_inferred']=True;self.bad()
 def test_rewrite_capture_grade(self):self.d[1]['human_reading']='COLLATED';self.bad()
 def test_collapse_source_positions(self):self.d[0]['direct_visual_reviews'][1]['glyph_xyxy']=self.d[0]['direct_visual_reviews'][0]['glyph_xyxy'];self.bad()
 def test_fake_rgb(self):self.d[0]['direct_visual_reviews'][0]['color_glyph_rgb_sha256']='0'*64;self.bad()
 def test_erase_transport_failure(self):self.d[5]['failed_run_id']=0;self.bad()
 def test_transport_relaxation(self):self.d[5]['retry_policy']['source_hash_gate_unchanged']=False;self.bad()
 def test_forward_focus(self):
  self.d[3]['historical_audit']['current_focus'].append('13LM future');self.d[4]['binding']['source_focus_count']+=1;self.d[4]['binding']['latest_research_focus_prefix']='13LM'
  i=next(i for i in self.d[4]['issues'] if i['id']=='TW-OPEN-0005');i['next_action']='13LM CURRENT ACTION: future\n'+i['next_action']
  self.assertEqual(v.check(*self.d)['status'],'PASS')
if __name__=='__main__':unittest.main()
