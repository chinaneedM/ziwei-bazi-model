import json
import unittest
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/research/TIANWEN-13TB-ZHOU1569-SAME-COPY-SOLAR-INTERPOLATION-ENDPOINT-GATE-R1.json'


class ZhouSameCopyInterpolation(unittest.TestCase):
    def test_original_endpoint_inputs_and_exact_replay(self):
        evidence = json.loads(EVIDENCE.read_text())
        old = json.loads((ROOT / 'docs/research/MING-DATONG-1569-YINGSUO-FULL-NUMERIC-RECONSTRUCTION-R1.json').read_text())
        for family, row in zip(old['families'], evidence['exact_replay']['rows']):
            source_row = next(x for x in family['rows'] if x['day_index'] == row['n'])
            self.assertEqual(Decimal(source_row['accumulated_source_table_units']), Decimal(row['normalized_C_fen']))
            self.assertEqual(Decimal(source_row['add_source_table_units']), Decimal(row['normalized_M_fen']))
            self.assertEqual(Decimal(family['exact_initial_limit_cutoff']['normalized_days']), Decimal(row['n']) + Decimal(row['fraction_numerator_over_million']) / 10**6)
            support = next(x for x in family['rows'] if x['day_index'] == row['n'] + 1)
            self.assertEqual(Decimal(support['accumulated_source_table_units']) - Decimal(row['normalized_C_fen']), Decimal(row['normalized_M_fen']))
            numerator = row['C_scaled_1e8'] * 10**6 + row['fraction_numerator_over_million'] * row['M_scaled_1e8']
            self.assertEqual(numerator, row['interpolated_correction_numerator_over_1e14'])
            self.assertEqual(Decimal(numerator) / 10**14, Decimal(row['interpolated_degree_correction']))

    def test_g893_mapping_fails_both_final_rounders(self):
        e = json.loads(EVIDENCE.read_text())
        prose = json.loads((ROOT / 'docs/research/TIANWEN-13SK-G893-ORIGINAL-SOLAR-POST-TABLE-TOTALS-R1.json').read_text())
        for row in e['exact_replay']['rows']:
            observed = next(x['total_microdegrees'] for x in prose['post_table_original_totals'] if x['season'] == row['season'] and x['start'] == '初日')
            total = Decimal(row['comparison_integer_baseline']) + row['comparison_sign'] * Decimal(row['interpolated_degree_correction'])
            self.assertEqual(total, Decimal(row['hypothetical_G893_full_degree']))
            self.assertEqual(observed - total * 10**6, Decimal(row['prose_minus_model_microdegree']))
            for rounding in (ROUND_DOWN, ROUND_HALF_UP):
                self.assertNotEqual(total.quantize(Decimal('.000001'), rounding=rounding), Decimal(observed) / 10**6)
        self.assertEqual(e['adjudication']['historical_finals'], '0/6')
        self.assertEqual(e['adjudication']['algorithm_reopens'], 0)
