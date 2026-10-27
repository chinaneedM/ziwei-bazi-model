#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from fortune_training.bazi_chart import (
    BaziChartFoundation,
    BaziChartRequest,
    build_production_bazi_profile,
)
from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
    profile = build_production_bazi_profile(registry)
    engine = BaziChartFoundation(TimeCalendarFoundation(registry))
    result = engine.resolve(
        BaziChartRequest(
            birth=BirthInput(
                reported_local_datetime=datetime(1990, 6, 15, 12, 0),
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            profile=profile,
        )
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
