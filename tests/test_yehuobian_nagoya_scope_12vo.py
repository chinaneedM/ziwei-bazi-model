import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('scope12vo',ROOT/'scripts/verify-yehuobian-nagoya-scope-12vo.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class ScholarshipScope(unittest.TestCase):
 def setUp(self):self.r=json.loads((ROOT/v.RECORD).read_text())
 def test_current_scope(self):self.assertEqual(v.validate(self.r)['new_ancient_target_glyph_votes'],0)
 def test_other_volume_not_target_collation(self):
  self.r['apparatus_scope']['inoue2021']['target_juan20_covered']=True
  with self.assertRaisesRegex(ValueError,'juan20'):v.validate(self.r)
 def test_unlisted_variant_not_agreement(self):
  self.r['apparatus_scope']['selection_policy']['unlisted_variant_proves_agreement']=True
  with self.assertRaisesRegex(ValueError,'equality'):v.validate(self.r)
 def test_scholar_labels_not_current_accessions(self):
  self.r['scholarly_copy_labels']['C_equals_IHP174009']='CONFIRMED'
  with self.assertRaisesRegex(ValueError,'identity'):v.validate(self.r)
if __name__=='__main__':unittest.main()
