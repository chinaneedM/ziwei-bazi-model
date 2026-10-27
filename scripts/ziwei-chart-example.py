#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, PolicyRegistry, TimeCalendarFoundation
from fortune_training.ziwei_chart import (
    Sex,
    ZiweiChartFoundation,
    ZiweiChartRequest,
    build_production_ziwei_profile,
)


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    registry = PolicyRegistry.from_file(ROOT / "config" / "time-calendar-policies.json")
    profile = build_production_ziwei_profile(registry)
    engine = ZiweiChartFoundation(TimeCalendarFoundation(registry))
    result = engine.resolve(
        ZiweiChartRequest(
            birth=BirthInput(
                reported_local_datetime=datetime(1994, 5, 17, 14, 30),
                birth_place="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone_id="Asia/Shanghai",
            ),
            sex=Sex.MALE,
            profile=profile,
        )
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
