from __future__ import annotations

import unittest

from fortune_training.historical_calendar import (
    HISTORICAL_CALENDAR_ADAPTER_CONTRACT_ID,
    MING_DATONG_CONTEXT_ID,
    MODERN_CHINESE_CALENDAR_ENGINE_ID,
    QING_SHIXIAN_1645_CONTEXT_ID,
    FailClosedHistoricalCalendarAdapter,
    HistoricalCalendarOperation,
    get_historical_calendar_regime,
    historical_calendar_adapter_contract_hash,
    historical_calendar_adapter_contract_payload,
)


class HistoricalCalendarAdapterContractR1Tests(unittest.TestCase):
    def test_ming_and_shixian_are_distinct_regime_contexts(self) -> None:
        ming = get_historical_calendar_regime(MING_DATONG_CONTEXT_ID)
        qing = get_historical_calendar_regime(QING_SHIXIAN_1645_CONTEXT_ID)
        self.assertNotEqual(ming.regime_id, qing.regime_id)
        self.assertIn("EXT-CTEXT-SANMING-V2-DAYUN", ming.source_refs)
        self.assertNotIn("EXT-CTEXT-SANMING-V2-DAYUN", qing.source_refs)
        self.assertIn(MODERN_CHINESE_CALENDAR_ENGINE_ID, ming.prohibited_fallback_algorithm_ids)
        self.assertIn(MODERN_CHINESE_CALENDAR_ENGINE_ID, qing.prohibited_fallback_algorithm_ids)

    def test_contract_is_unselected_and_contains_no_certified_arithmetic(self) -> None:
        payload = historical_calendar_adapter_contract_payload()
        self.assertEqual(payload["contract_id"], HISTORICAL_CALENDAR_ADAPTER_CONTRACT_ID)
        self.assertEqual(payload["selection_status"], "PRESERVED_NOT_SELECTED")
        self.assertEqual(payload["implementation_status"], "CONTRACT_ONLY_NO_CERTIFIED_CALENDAR_ARITHMETIC")
        self.assertIn("NO_MODERN_CHINESE_CALENDAR_AS_HISTORICAL_AUTHORITY", payload["global_prohibitions"])

    def test_fail_closed_adapter_never_falls_back_to_modern_calendar(self) -> None:
        adapter = FailClosedHistoricalCalendarAdapter(MING_DATONG_CONTEXT_ID)
        result = adapter.resolve(
            operation=HistoricalCalendarOperation.REALIZE_DAYUN_HANDOVER,
            payload={"birth": "source-scoped-placeholder"},
        )
        self.assertEqual(result.status, "UNRESOLVED_NO_CERTIFIED_HISTORICAL_CALENDAR_ADAPTER")
        self.assertIsNone(result.value)
        self.assertIn("MODERN_CHINESE_CALENDAR_FALLBACK_FORBIDDEN", result.diagnostics)
        self.assertIn("NO_IMPLICIT_GREGORIAN_OR_UTC_ANNIVERSARY_SUBSTITUTION", result.diagnostics)

    def test_contract_hash_is_deterministic(self) -> None:
        self.assertEqual(historical_calendar_adapter_contract_hash(), historical_calendar_adapter_contract_hash())


if __name__ == "__main__":
    unittest.main()
