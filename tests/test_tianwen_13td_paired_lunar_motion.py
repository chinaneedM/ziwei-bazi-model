import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'docs/research/TIANWEN-13TD-G893-PAIRED-LUNAR-MOTION-MEAN-AND-CARRY-CANDIDATES-R1.json'


class PairedLunarMotion(unittest.TestCase):
    def setUp(self):
        self.e = json.loads(PATH.read_text())
        self.rows = self.e['original_rows']

    def test_selected_original_motion_pairs_match_preexisting_ming_table(self):
        ming = json.loads((ROOT / 'docs/research/MING-DATONG-1569-CHIJI-FULL-NUMERIC-RECONSTRUCTION-R1.json').read_text())
        lookup = {r['limit']: r for r in ming['rows']}
        self.assertEqual([r['limit'] for r in self.rows], list(range(122,127)))
        for row in self.rows:
            m = lookup[row['limit']]
            self.assertEqual(F(m['ji_xingdu_degree'])*10000, row['ji_scaled_1e4_degree'])
            self.assertEqual(F(m['chi_xingdu_degree'])*10000, row['chi_scaled_1e4_degree'])
            self.assertEqual(F(m['loss_gain_degree'])*10**8, row['loss_gain_magnitude_scaled_1e8_degree'])
        self.assertEqual(self.rows[-1]['chi_continues_on_page'], '036a')

    def test_exact_models_keep_original_13kd_counterexample(self):
        for model in self.e['exact_candidate_models']:
            mean = F(model['mean_degree'])
            predicted = []
            count = 0
            for row in self.rows:
                q = F(row['loss_gain_magnitude_scaled_1e8_degree'],10**8)
                out = []
                for value in (mean-q,mean+q):
                    if model['rounder']=='CEIL': out.append((value.numerator*10000+value.denominator-1)//value.denominator)
                    else: out.append((2*value.numerator*10000+value.denominator)//(2*value.denominator))
                predicted.append([row['limit'],*out])
                count += sum(a==b for a,b in zip(out,[row['ji_scaled_1e4_degree'],row['chi_scaled_1e4_degree']]))
            self.assertEqual(predicted,model['predicted_limit_ji_chi'])
            self.assertEqual(count,model['matches_out_of_10'])
        old = next(m for m in self.e['exact_candidate_models'] if m['name']=='LEGACY_ROUNDED_MEAN_NEAREST')
        self.assertEqual(old['predicted_limit_ji_chi'][0],[122,10310,11616])
        self.assertEqual(self.rows[0]['ji_scaled_1e4_degree'],10309)

    def test_two_disjoint_mean_intervals_prevent_unique_carry_claim(self):
        lows={False:[],True:[]};highs={False:[],True:[]}
        for row in self.rows:
            q=F(row['loss_gain_magnitude_scaled_1e8_degree'],10**8)
            for y,shift in [(row['ji_scaled_1e4_degree'],q),(row['chi_scaled_1e4_degree'],-q)]:
                lows[False].append(F(y-1,10000)+shift);highs[False].append(F(y,10000)+shift)
                lows[True].append(F(2*y-1,20000)+shift);highs[True].append(F(2*y+1,20000)+shift)
        c=(max(lows[False]),min(highs[False]));n=(max(lows[True]),min(highs[True]))
        self.assertEqual(c,tuple(F(x) for x in self.e['identifiability']['ceil_mean_interval_open_lower_closed_upper']))
        self.assertEqual(n,tuple(F(x) for x in self.e['identifiability']['nearest_mean_interval_closed_lower_open_upper']))
        self.assertLess(c[0],F('1.0962375'));self.assertLessEqual(F('1.0962375'),c[1])
        self.assertLessEqual(n[0],F('1.09628'));self.assertLess(F('1.09628'),n[1])
        self.assertLess(c[1],n[0])
        self.assertFalse(self.e['identifiability']['constructed_nearest_is_historical_source'])
        self.assertEqual(self.e['adjudication']['g893_six_historical_finals'],'0/6')
