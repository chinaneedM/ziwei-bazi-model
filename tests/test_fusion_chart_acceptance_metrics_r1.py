from __future__ import annotations

import unittest

from fortune_training.fusion_chart_acceptance.metrics import (
    percentile,
    summarize_latencies_ms,
)
from fortune_training.fusion_chart_acceptance.random_replay import (
    deterministic_random_cases,
)


class FusionChartAcceptanceMetricsR1Tests(unittest.TestCase):
    def test_percentiles_and_throughput_are_deterministic(self) -> None:
        summary = summarize_latencies_ms([1, 2, 3, 4, 5])
        self.assertEqual(5, summary.count)
        self.assertEqual(3.0, summary.p50_ms)
        self.assertEqual(4.8, summary.p95_ms)
        self.assertEqual(4.96, summary.p99_ms)
        self.assertEqual(1000.0 / 3.0, summary.throughput_per_second)
        self.assertEqual(2.0, percentile([1, 2, 3], 50))

    def test_random_case_generator_replays_exactly_for_seed(self) -> None:
        first = deterministic_random_cases(32, seed=20260904)
        second = deterministic_random_cases(32, seed=20260904)
        different = deterministic_random_cases(32, seed=20260905)
        self.assertEqual(first, second)
        self.assertNotEqual(first, different)
        self.assertTrue(all(row[0].year >= 1971 for row in first))
        self.assertTrue(all(row[0].year <= 2035 for row in first))

    def test_random_case_shards_are_exact_slices_of_global_sequence(self) -> None:
        full = deterministic_random_cases(40, seed=20260904)
        left = deterministic_random_cases(20, seed=20260904, start_index=0)
        right = deterministic_random_cases(20, seed=20260904, start_index=20)
        self.assertEqual(full, left + right)


if __name__ == "__main__":
    unittest.main()
