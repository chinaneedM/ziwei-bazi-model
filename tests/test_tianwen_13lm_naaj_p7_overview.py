"""13LM evidence scope mutation tests: no overview -> ancient plate promotion."""
import copy,importlib.util,unittest
from pathlib import Path
S=Path(__file__).resolve().parents[1]/'scripts/verify-tianwen-13lm-naaj-p7-overview.py'
spec=importlib.util.spec_from_file_location('verify_13lm',S)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class EvidenceGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.inputs=m.load()
    def test_original(self):
        self.assertEqual(m.check(*self.inputs)['status'],'PASS')
    def test_fake_native_colocation(self):
        e,s,l=copy.deepcopy(self.inputs)
        e['targets'][0]['native_color_acquisition']='ATTESTED'
        with self.assertRaises(AssertionError):m.check(e,s,l)
    def test_false_plate_adjudication(self):
        e,s,l=copy.deepcopy(self.inputs);e['adjudication']['plate_identity_or_impression_date_proven']=True
        with self.assertRaises(AssertionError):m.check(e,s,l)
    def test_wrong_source_canvas(self):
        e,s,l=copy.deepcopy(self.inputs);e['sources'][1]['source_canvas_pixels']=[3000,2177]
        with self.assertRaises(AssertionError):m.check(e,s,l)
    def test_loss_of_prior_issue(self):
        e,s,l=copy.deepcopy(self.inputs);l['issues'][4]['source_refs'].remove(m.NAME)
        with self.assertRaises(AssertionError):m.check(e,s,l)
    def test_false_historical_winner(self):
        e,s,l=copy.deepcopy(self.inputs);e['adjudication']['g893_six_winners']=1
        with self.assertRaises(AssertionError):m.check(e,s,l)
if __name__=='__main__':unittest.main()
