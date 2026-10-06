from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

def run(root: Path) -> dict:
    fixture=json.loads((root/"docs/research/MING-DATONG-D1-56-CONJUNCTION-VALIDATION-R1.json").read_text(encoding="utf-8"))
    geo=json.loads((root/"docs/research/MING-DATONG-QISHUO-GEOGRAPHIC-CRITICAL-CASES-R1.json").read_text(encoding="utf-8"))
    delta_min=Decimal(str(geo["modern_comparison_coordinates"]["local_apparent_solar_time_delta_minutes"]))
    delta_day=delta_min/Decimal("1440")
    counts={"no_shift":0,"plus_delta":0,"minus_delta":0}
    plus_cross=minus_cross=0
    nearest=None
    for row in fixture["rows"]:
        v=Decimal(str(row["d1_day_index"]))
        lo=Decimal(str(row["lower_day_index"]))
        hi=Decimal(str(row["upper_day_index"]))
        def inside(x: Decimal) -> bool: return lo <= x <= hi
        counts["no_shift"] += int(inside(v))
        counts["plus_delta"] += int(inside(v+delta_day))
        counts["minus_delta"] += int(inside(v-delta_day))
        plus_cross += int(int(v+delta_day) != int(v))
        minus_cross += int(int(v-delta_day) != int(v))
        frac=v-int(v)
        dist=min(frac,Decimal("1")-frac)*Decimal("1440")
        if nearest is None or dist < nearest[0]:
            nearest=(dist,row)
    assert nearest is not None
    return {
        "delta_minutes":str(delta_min),
        "counts":counts,
        "plus_day_crossings":plus_cross,
        "minus_day_crossings":minus_cross,
        "nearest_boundary":{"minutes":str(nearest[0]),"year":nearest[1]["year"],"month":nearest[1]["month"],"display":nearest[1]["almanac_display"],"d1_day_index":nearest[1]["d1_day_index"]},
        "identifiability":"INTERNAL_SHARED_COORDINATE_CANNOT_IDENTIFY_ABSOLUTE_MERIDIAN",
    }

if __name__=="__main__":
    root=Path(__file__).resolve().parents[1]
    print(json.dumps(run(root),ensure_ascii=False,indent=2,sort_keys=True))
