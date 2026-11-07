import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'docs/research/TIANWEN-13TC-G893-LUNAR-DAYRATE-ORIGINAL-QUANTIZATION-WINDOW-R1.json'
DIGITS = dict(zip('〇一二三四五六七八九', '0123456789'))


class LunarDayrateQuantization(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(PATH.read_text())
        self.rows = self.data['original_rows']

    def test_literal_day_field_matches_independent_ming_rows(self):
        ming = json.loads((ROOT / 'docs/research/MING-DATONG-1569-CHIJI-DAY-RATE-COLUMN-R1.json').read_text())
        lookup = {r['limit']: r['printed_total_day_rate_source_units'] for r in ming['rows']}
        self.assertEqual([r['limit'] for r in self.rows], [6, 7, 8, 9, 112, 113, 114, 115])
        for row in self.rows:
            day, tail = row['literal_dayrate'].split('日')
            self.assertEqual(len(tail), 4)
            value = int(''.join(DIGITS[x] for x in day)) * 10000 + int(''.join(DIGITS[x] for x in tail))
            self.assertEqual(value, row['normalized_1e4_day_integer'])
            self.assertEqual(value, lookup[row['limit']])

    def test_constant_step_families_are_discriminated_without_unique_slope(self):
        points = [(r['limit'], r['normalized_1e4_day_integer']) for r in self.rows]
        lo = max(F(y, n) for n, y in points)
        hi = min(F(y + 1, n) for n, y in points)
        cert = self.data['constant_step_identifiability']
        self.assertEqual([lo, hi], [F(x) for x in cert['floor_slope_interval_inclusive_lower_exclusive_upper']])
        self.assertLess(lo, F(82008, 100))
        self.assertLess(F(82008, 100), hi)
        nearest_lo = max(F(2*y - 1, 2*n) for n, y in points)
        nearest_hi = min(F(2*y + 1, 2*n) for n, y in points)
        self.assertGreater(nearest_lo, nearest_hi)
        for name, denominator, numerator, nearest in [('FLOOR_82008_OVER_100',100,82008,False), ('HALF_UP_82008_OVER_100',100,82008,True), ('FLOOR_137773_OVER_168',168,137773,False), ('HALF_UP_137773_OVER_168',168,137773,True), ('FLOOR_STEP_820',1,820,False)]:
            predicted = [(2*n*numerator+denominator)//(2*denominator) if nearest else n*numerator//denominator for n, _ in points]
            expected = [r['predicted'] for r in self.data['exact_models'][name]['rows']]
            self.assertEqual(predicted, expected)
            self.assertEqual(sum(v == y for v, (_, y) in zip(predicted, points)), self.data['exact_models'][name]['match_count'])
        self.assertEqual(self.data['exact_models']['FLOOR_82008_OVER_100']['match_count'], 8)
        self.assertFalse(cert['unique_slope_identified'])

    def test_phase_counterexample_prevents_general_rounding_claim(self):
        # Nearest with a -1/2 input phase is observationally the same floor model.
        for row in self.rows:
            phased = F(row['limit']*82008,100) - F(1,2)
            nearest = (2*phased.numerator+phased.denominator)//(2*phased.denominator)
            self.assertEqual(nearest, row['normalized_1e4_day_integer'])
        self.assertEqual(self.data['adjudication']['g893_six_historical_finals'], '0/6')
        self.assertEqual(self.data['adjudication']['algorithm_reopens'], 0)
