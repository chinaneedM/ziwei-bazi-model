#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from fortune_training.calendar_foundation import BirthInput, TimeCalendarFoundation


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    engine = TimeCalendarFoundation.from_repository(root)
    result = engine.resolve(
        BirthInput(
            reported_local_datetime=datetime(2000, 12, 26, 1, 40),
            birth_place="Kashgar",
            latitude=39.4704,
            longitude=75.9898,
            timezone_id="Asia/Shanghai",
        )
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
