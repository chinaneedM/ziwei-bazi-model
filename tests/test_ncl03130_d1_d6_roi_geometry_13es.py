import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts"/"verify-ncl03130-d1-d6-roi-geometry-13es.py"
spec=importlib.util.spec_from_file_location("v13es",p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Test13ES(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=m.read(m.E);cls.er=m.read(m.ER);cls.eq=m.read(m.EQ);cls.en=m.read(m.EN);cls.s=m.read(m.S);cls.l=m.read(m.L)
    def run_check(self,e=None,er=None):
        return m.check(self.e if e is None else e,self.er if er is None else er,self.eq,self.en,self.s,self.l)
    def corrupted(self,change):
        e=copy.deepcopy(self.e);change(e)
        with self.assertRaises(AssertionError):self.run_check(e=e)
    def test_metadata_pass(self):self.assertTrue(self.run_check())
    def test_bbox_x_overlap_corruption(self):self.corrupted(lambda e:e["per_day_pairs"][0].update(bbox_x_overlap_px=0))
    def test_bbox_area_corruption(self):self.corrupted(lambda e:e["per_day_pairs"][4].update(bbox_xy_intersection_pixels=0))
    def test_fake_ink_collision(self):self.corrupted(lambda e:e["per_day_pairs"][1].update(ink_intersection_proven=True))
    def test_fake_field_equivalence(self):self.corrupted(lambda e:e["per_day_pairs"][5].update(mechanical_field_equivalence_proven=True))
    def test_imputed_decimal(self):self.corrupted(lambda e:e["adjudication"]["complete_fourfen_historical_decimal_values"].__setitem__(2,"0.4848"))
    def test_false_full_row(self):self.corrupted(lambda e:e["adjudication"]["original_full_fourfen_rows_proven"].__setitem__(3,True))
    def test_fake_witness(self):self.corrupted(lambda e:e["shared_source"].update(independent_witnesses_added=1))
    def test_upstream_bbox_mutation(self):
        er=copy.deepcopy(self.er);er["rois"][0]["bbox"][0]+=1
        with self.assertRaises(AssertionError):self.run_check(er=er)
if __name__=="__main__":unittest.main()
