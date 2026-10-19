import importlib.util, unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-utokyo-goryeosa-marginalia-13ak.py"
spec=importlib.util.spec_from_file_location("g13ak",p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class TestGoryeosaVolumeAnnotations(unittest.TestCase):
 def test_integrity(self):self.assertTrue(mod.verify())
 def test_volume_52_unproven(self):
  e=mod.load(mod.E)
  self.assertFalse(any(x["work_volume"]==52 for x in e["printed_copy"]["explicit_copy_annotations"]))
  self.assertFalse(e["printed_copy"]["one_collection_level_mark_implies_volume52_ownership"])
 def test_institution_not_proven_provenance(self):
  a=mod.load(mod.E)["academy_reference"]
  self.assertTrue(a["name_match_to_ink_annotation"])
  self.assertFalse(a["specific_UTokyo_copy_from_this_institution_proven"])
  self.assertFalse(a["foundation_year_independent_earliest_date_of_this_printed_copy"])
 def test_ink_not_imprint(self):
  e=mod.load(mod.E);self.assertFalse(e["printed_copy"]["handwritten_marks_equivalent_to_printer_colophon"])
  self.assertEqual(e["non_promotions"]["cross_print_independent_numeric_votes_added"],0)
if __name__=="__main__":unittest.main()
