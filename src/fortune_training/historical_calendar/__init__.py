"""Source/regime-scoped historical Chinese-calendar adapter contract."""

from .contract import (
    HISTORICAL_CALENDAR_ADAPTER_CONTRACT_ID,
    HISTORICAL_CALENDAR_ADAPTER_CONTRACT_VERSION,
    MING_DATONG_CONTEXT_ID,
    MODERN_CHINESE_CALENDAR_ENGINE_ID,
    QING_SHIXIAN_1645_CONTEXT_ID,
    FailClosedHistoricalCalendarAdapter,
    HistoricalCalendarAdapter,
    HistoricalCalendarOperation,
    HistoricalCalendarRegimeDescriptor,
    HistoricalCalendarResolution,
    get_historical_calendar_regime,
    historical_calendar_adapter_contract_hash,
    historical_calendar_adapter_contract_payload,
)

__all__ = [
    "HISTORICAL_CALENDAR_ADAPTER_CONTRACT_ID",
    "HISTORICAL_CALENDAR_ADAPTER_CONTRACT_VERSION",
    "MING_DATONG_CONTEXT_ID",
    "MODERN_CHINESE_CALENDAR_ENGINE_ID",
    "QING_SHIXIAN_1645_CONTEXT_ID",
    "FailClosedHistoricalCalendarAdapter",
    "HistoricalCalendarAdapter",
    "HistoricalCalendarOperation",
    "HistoricalCalendarRegimeDescriptor",
    "HistoricalCalendarResolution",
    "get_historical_calendar_regime",
    "historical_calendar_adapter_contract_hash",
    "historical_calendar_adapter_contract_payload",
]
