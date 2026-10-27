from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Mapping, Protocol

from fortune_training.util import object_sha256


HISTORICAL_CALENDAR_ADAPTER_CONTRACT_ID = "HISTORICAL-CHINESE-CALENDAR-ADAPTER-CONTRACT-R1"
HISTORICAL_CALENDAR_ADAPTER_CONTRACT_VERSION = "1.0.0"
MODERN_CHINESE_CALENDAR_ENGINE_ID = "MODERN-CHINESE-CALENDAR-ASTRONOMICAL-V1"

MING_DATONG_CONTEXT_ID = "MING-DATONG-CALENDAR-CONTEXT-R1"
QING_SHIXIAN_1645_CONTEXT_ID = "QING-SHIXIAN-1645-CALENDAR-CONTEXT-R1"

CONTRACT_SELECTION_STATUS = "PRESERVED_NOT_SELECTED"
CONTRACT_IMPLEMENTATION_STATUS = "CONTRACT_ONLY_NO_CERTIFIED_CALENDAR_ARITHMETIC"
FAIL_CLOSED_STATUS = "UNRESOLVED_NO_CERTIFIED_HISTORICAL_CALENDAR_ADAPTER"


class HistoricalCalendarOperation(str, Enum):
    MAP_CIVIL_DATE_TO_HISTORICAL_LUNISOLAR = "MAP_CIVIL_DATE_TO_HISTORICAL_LUNISOLAR"
    REALIZE_DAYUN_HANDOVER = "REALIZE_DAYUN_HANDOVER"
    ADD_CALENDAR_YEARS = "ADD_CALENDAR_YEARS"


@dataclass(frozen=True)
class HistoricalCalendarRegimeDescriptor:
    regime_id: str
    display_name: str
    historical_scope: str
    computational_context: str
    implementation_status: str
    source_refs: tuple[str, ...]
    prohibited_fallback_algorithm_ids: tuple[str, ...]
    notes: tuple[str, ...]


@dataclass(frozen=True)
class HistoricalCalendarResolution:
    status: str
    regime_id: str
    operation: str
    value: Mapping[str, object] | None
    source_refs: tuple[str, ...]
    diagnostics: tuple[str, ...]


class HistoricalCalendarAdapter(Protocol):
    regime_id: str

    def resolve(
        self,
        *,
        operation: HistoricalCalendarOperation,
        payload: Mapping[str, object],
    ) -> HistoricalCalendarResolution:
        ...


_REGIMES = {
    MING_DATONG_CONTEXT_ID: HistoricalCalendarRegimeDescriptor(
        regime_id=MING_DATONG_CONTEXT_ID,
        display_name="Ming Datong calendar context",
        historical_scope=(
            "MING_OFFICIAL_CALENDAR_CONTEXT_RELEVANT_TO_THE_1578_SANMING_TONGHUI_WITNESS;"
            " CONTEXT_IDENTIFIED_BUT_EXACT_EDITION_SCOPED_ARITHMETIC_NOT_IMPLEMENTED"
        ),
        computational_context=(
            "MINGSHI_RECORDS_DATONG_AS_SHOUSHI_DERIVED; THIS DESCRIPTOR_DOES_NOT_ASSERT"
            " A_COMPLETE_RECONSTRUCTION_OF_MONTH_STARTS_LEAP_MONTHS_OR_CLOCK_REALIZATION"
        ),
        implementation_status=CONTRACT_IMPLEMENTATION_STATUS,
        source_refs=(
            "EXT-CTEXT-MINGSHI-DATONG-CALENDAR",
            "EXT-CTEXT-SANMING-V2-DAYUN",
        ),
        prohibited_fallback_algorithm_ids=(MODERN_CHINESE_CALENDAR_ENGINE_ID,),
        notes=(
            "Primary research target for the Ming Dayun calendarization family; not an algorithm winner.",
            "Small-month/leap-month wording does not by itself specify every historical calendar arithmetic detail.",
        ),
    ),
    QING_SHIXIAN_1645_CONTEXT_ID: HistoricalCalendarRegimeDescriptor(
        regime_id=QING_SHIXIAN_1645_CONTEXT_ID,
        display_name="Qing Shixian calendar context from 1645",
        historical_scope=(
            "POST_1645_QING_CALENDAR_CONTEXT; DISTINCT_FROM_THE_1578_MING_SOURCE_CONTEXT"
        ),
        computational_context=(
            "REGISTERED_AS_A_REGIME_BOUNDARY_WITNESS_SO_POST_1645_RULES_CANNOT_BE"
            " SILENTLY_BACK_PROJECTED_INTO_MING_DAYUN_EXAMPLES"
        ),
        implementation_status=CONTRACT_IMPLEMENTATION_STATUS,
        source_refs=("EXT-LOC-XINLI-XIAOHUO-SHIXIAN-1645",),
        prohibited_fallback_algorithm_ids=(MODERN_CHINESE_CALENDAR_ENGINE_ID,),
        notes=(
            "Chronological contrast only in R1; no Shixian arithmetic is implemented here.",
            "Must never become the default calendar for a Ming witness merely because it is historical.",
        ),
    ),
}


class FailClosedHistoricalCalendarAdapter:
    """Structured refusal until one regime has certified source-scoped arithmetic."""

    def __init__(self, regime_id: str) -> None:
        self.descriptor = get_historical_calendar_regime(regime_id)
        self.regime_id = self.descriptor.regime_id

    def resolve(
        self,
        *,
        operation: HistoricalCalendarOperation,
        payload: Mapping[str, object],
    ) -> HistoricalCalendarResolution:
        del payload
        return HistoricalCalendarResolution(
            status=FAIL_CLOSED_STATUS,
            regime_id=self.regime_id,
            operation=operation.value,
            value=None,
            source_refs=self.descriptor.source_refs,
            diagnostics=(
                "HISTORICAL_CALENDAR_ARITHMETIC_NOT_CERTIFIED",
                "MODERN_CHINESE_CALENDAR_FALLBACK_FORBIDDEN",
                "NO_IMPLICIT_GREGORIAN_OR_UTC_ANNIVERSARY_SUBSTITUTION",
            ),
        )


def get_historical_calendar_regime(regime_id: str) -> HistoricalCalendarRegimeDescriptor:
    try:
        return _REGIMES[regime_id]
    except KeyError as exc:
        raise ValueError(f"unsupported historical calendar regime context: {regime_id!r}") from exc


def historical_calendar_adapter_contract_payload() -> dict[str, object]:
    return {
        "schema": "HISTORICAL-CHINESE-CALENDAR-ADAPTER-CONTRACT-R1",
        "contract_id": HISTORICAL_CALENDAR_ADAPTER_CONTRACT_ID,
        "contract_version": HISTORICAL_CALENDAR_ADAPTER_CONTRACT_VERSION,
        "selection_status": CONTRACT_SELECTION_STATUS,
        "implementation_status": CONTRACT_IMPLEMENTATION_STATUS,
        "operations": tuple(operation.value for operation in HistoricalCalendarOperation),
        "regimes": tuple(asdict(_REGIMES[key]) for key in sorted(_REGIMES)),
        "global_prohibitions": (
            "NO_MODERN_CHINESE_CALENDAR_AS_HISTORICAL_AUTHORITY",
            "NO_CROSS_REGIME_BACK_PROJECTION",
            "NO_IMPLICIT_GREGORIAN_ANNIVERSARY_FOR_CLASSICAL_CANDIDATES",
            "NO_RUNTIME_WINNER_SELECTION_FROM_CHRONOLOGY_ALONE",
        ),
    }


def historical_calendar_adapter_contract_hash() -> str:
    return object_sha256(historical_calendar_adapter_contract_payload())


def validate_historical_calendar_adapter_contract() -> None:
    if set(_REGIMES) != {MING_DATONG_CONTEXT_ID, QING_SHIXIAN_1645_CONTEXT_ID}:
        raise ValueError("historical calendar R1 must preserve distinct Ming Datong and Qing Shixian contexts")
    if CONTRACT_SELECTION_STATUS != "PRESERVED_NOT_SELECTED":
        raise ValueError("historical calendar contract must not select a production winner")
    for descriptor in _REGIMES.values():
        if descriptor.implementation_status != CONTRACT_IMPLEMENTATION_STATUS:
            raise ValueError("historical calendar context was incorrectly upgraded to executable arithmetic")
        if MODERN_CHINESE_CALENDAR_ENGINE_ID not in descriptor.prohibited_fallback_algorithm_ids:
            raise ValueError("modern Chinese calendar fallback prohibition regressed")
    ming = _REGIMES[MING_DATONG_CONTEXT_ID]
    qing = _REGIMES[QING_SHIXIAN_1645_CONTEXT_ID]
    if "EXT-CTEXT-SANMING-V2-DAYUN" not in ming.source_refs:
        raise ValueError("Ming Dayun source lost its calendar-context research binding")
    if "EXT-CTEXT-SANMING-V2-DAYUN" in qing.source_refs:
        raise ValueError("post-1645 Shixian context must not absorb the 1578 Ming Dayun witness")


validate_historical_calendar_adapter_contract()
