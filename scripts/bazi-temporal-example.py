#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    bazi_foundation_v1_profile,
)
from fortune_training.bazi_temporal import (
    BaziSex,
    BaziTemporalEngine,
    BaziTemporalRequest,
    bazi_temporal_v1_continuous_profile,
)
from fortune_training.calendar_foundation import BirthInput


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    chart_engine = BaziChartFoundation.from_repository(ROOT)
    chart_profile = bazi_foundation_v1_profile(chart_engine.time_calendar.policy_registry)
    chart_resolution = chart_engine.resolve_typed(
        BaziChartRequest(
            birth=BirthInput(
                reported_local_datetime=datetime(2025, 2, 7, 10, 10),
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            profile=chart_profile,
        )
    )
    if len(chart_resolution.candidates) != 1:
        raise SystemExit(f"expected one natal candidate, got {chart_resolution.status}")

    temporal = BaziTemporalEngine().resolve(
        BaziTemporalRequest(
            candidate=chart_resolution.candidates[0],
            sex=BaziSex.MALE,
            profile=bazi_temporal_v1_continuous_profile(),
            dayun_count=8,
        )
    )
    print(json.dumps(temporal, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
