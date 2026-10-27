from __future__ import annotations

from datetime import date, datetime


HEAVENLY_STEMS = "甲乙丙丁戊己庚辛壬癸"
EARTHLY_BRANCHES = "子丑寅卯辰巳午未申酉戌亥"


def sexagenary_day_index(gregorian_date: date) -> int:
    """Return the sexagenary day index for a proleptic-Gregorian date."""

    # JDN 2451551 (2000-01-07, Gregorian) is 甲子.
    julian_day_number = gregorian_date.toordinal() + 1_721_425
    return (julian_day_number + 49) % 60


def sexagenary_pillar(index: int) -> str:
    return HEAVENLY_STEMS[index % 10] + EARTHLY_BRANCHES[index % 12]


def sexagenary_day_pillar(gregorian_date: date) -> str:
    return sexagenary_pillar(sexagenary_day_index(gregorian_date))


def double_hour_branch_index(local_datetime: datetime) -> int:
    if local_datetime.tzinfo is not None:
        raise ValueError("local_datetime must be a naive local clock reading")
    return ((local_datetime.hour + 1) // 2) % 12


def five_rats_hour_pillar(local_datetime: datetime, day_stem_source_date: date) -> str:
    """Return an hour Ganzhi from an explicit clock and day-stem source date.

    Calendar/day-boundary policy is intentionally outside this primitive.  A
    caller must choose the clock standard and the date supplying the day stem.
    """

    branch_index = double_hour_branch_index(local_datetime)
    day_stem_index = sexagenary_day_index(day_stem_source_date) % 10
    zi_hour_stem_index = (day_stem_index % 5) * 2
    hour_stem_index = (zi_hour_stem_index + branch_index) % 10
    return HEAVENLY_STEMS[hour_stem_index] + EARTHLY_BRANCHES[branch_index]
