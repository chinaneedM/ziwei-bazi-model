"""13MS stage guards: physical-source identity and field equivalence cannot be fabricated."""
import copy,importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("acquire13ms",ROOT/"scripts/acquire-tianwen-13ms-zhou-original-atlas.py")
v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
class AtlasGate(unittest.TestCase):
 def source(self):
  return {"schema":"TIANWEN-13MS-ZHOU1569-ORIGINAL-PAGE-ATLAS-R1",
          "source":{"sha256":v.EXPECTED,"pdf_pages":45,"new_historical_source_count":0,"new_physical_witness_count":0,"ocr":False},
          "limits":{"cross_source_same_field_verified":False,"column_unit_radix_epoch_complete":False,
          "historical_six_winners":0,"algorithm_reopens":0,"physical_impression_identified":False},
          "roi_records":[{"name":n,"page":p,"box":list(b)} for n,p,b in v.ROIS]}
 def test_expected_coordinate_layout(self):self.assertTrue(v.gate(self.source()))
 def test_unproven_field_promotion_rejected(self):
  a=self.source();a["limits"]["cross_source_same_field_verified"]=True
  with self.assertRaises(AssertionError):v.gate(a)
 def test_unproven_impression_rejected(self):
  a=self.source();a["limits"]["physical_impression_identified"]=True
  with self.assertRaises(AssertionError):v.gate(a)
 def test_not_new_witness(self):
  a=self.source();a["source"]["new_physical_witness_count"]=1
  with self.assertRaises(AssertionError):v.gate(a)
 def test_original_roi_coordinates_cannot_drift(self):
  a=self.source();a["roi_records"][3]["box"][0]+=1
  with self.assertRaises(AssertionError):v.gate(a)
if __name__=="__main__":unittest.main()
