import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs/research/TIANWEN-13TF-KYOTO-ORIGINAL-LUNAR-MEAN-PERIOD-AND-LIMIT-SCALE-FIREWALL-R1.json'


class LunarOperandScales(unittest.TestCase):
    def test_same_original_periods_and_nominal_limit_are_distinct(self):
        e = json.loads(DOC.read_text())
        p = e['original_quantities']
        self.assertEqual(F(p['turn_period_day']), 2 * F(p['half_turn_day']))
        self.assertEqual(p['cycle_limits'], 2 * p['middle_limit'])
        self.assertEqual(p['middle_limit'], 2 * p['initial_limit'])
        daily = F(p['daily_lunar_mean_degree'])
        self.assertEqual(daily * F(820, 10000), F(87699, 80000))
        self.assertNotEqual(F(p['turn_period_day']) / p['cycle_limits'], F(820, 10000))

    def test_replacing_only_the_mean_operand_changes_original_pair_replay(self):
        e = json.loads(DOC.read_text())
        prior = json.loads((ROOT / e['paired_original_reference']).read_text())
        daily = F(e['original_quantities']['daily_lunar_mean_degree'])
        for candidate in e['conditional_replays']:
            mean = daily * F(candidate['day_fraction'])
            self.assertEqual(mean, F(candidate['mean_rational']))
            actual = {'CEIL': 0, 'HALF_UP': 0}
            for row in prior['original_rows']:
                q = F(row['loss_gain_magnitude_scaled_1e8_degree'], 10**8)
                for value, original in zip((mean-q, mean+q),
                        (row['ji_scaled_1e4_degree'], row['chi_scaled_1e4_degree'])):
                    x = value * 10000
                    actual['CEIL'] += -(-x.numerator // x.denominator) == original
                    actual['HALF_UP'] += (2*x.numerator+x.denominator)//(2*x.denominator) == original
            self.assertEqual(actual, candidate['matches_out_of_10'])

    def test_uniform_period_is_outside_prior_original_day_rate_window(self):
        # The window is recomputed from original L6..9 and L112..115,
        # independently of the lunar motion columns and their rounder.
        anchors = [(6, 4920), (7, 5740), (8, 6560), (9, 7380),
                   (112, 91848), (113, 92669), (114, 93489), (115, 94309)]
        low = max(F(y, n) for n, y in anchors)
        high = min(F(y+1, n) for n, y in anchors)
        e = json.loads(DOC.read_text())
        p = e['original_quantities']
        full = F(p['turn_period_day']) * 10000 / p['cycle_limits']
        self.assertLess(low, F('820.08'))
        self.assertLess(F('820.08'), high)
        self.assertLess(full, low)
        self.assertEqual(e['adjudication']['g893_historical_six_finals'], '0/6')
        self.assertFalse(e['adjudication']['g893_native_mean_or_quantizer_proven'])
