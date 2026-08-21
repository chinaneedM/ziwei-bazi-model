from __future__ import annotations

from dataclasses import dataclass

from fortune_training.util import object_sha256
from fortune_training.bazi_chart.registries import SEXAGENARY_CYCLE
from fortune_training.ziwei_chart.registries import NAYIN_PAIRS as RELEASED_ZIWEI_NAYIN_PAIRS


NAYIN_REGISTRY_ID = "BAZI-NAYIN-REGISTRY-R1"
NAYIN_REGISTRY_VERSION = "1.0.0"
NAYIN_ANNOTATION_PROFILE_ID = "BAZI-NAYIN-ANNOTATION-R1"
NAYIN_ANNOTATION_PROFILE_VERSION = "1.0.0"
NAYIN_ALGORITHM_ID = "BAZI-NAYIN-ANNOTATION-R1"
NAYIN_ALGORITHM_VERSION = "1.0.0"
NAYIN_SOURCE_REFS = ("S01:ZZZA-PR-010", "S01:ZZZA-PR-011")
NAYIN_REGISTRY_ORIGIN = "fortune_training.ziwei_chart.registries.NAYIN_PAIRS"

# Pins the exact released Git registry consumed by Ziwei Five-Element Bureau at
# Issue #343 creation. A change to that upstream registry must be reviewed and
# versioned rather than silently changing the Bazi annotation contract.
RELEASED_ZIWEI_NAYIN_PAIRS_SHA256 = "662e834dfb9ed85eb6a36596b1f088628200c26d7ee10f1f2815c497352198d2"


@dataclass(frozen=True)
class NayinRegistryEntry:
    pair_index: int
    semantic_id: str
    display_name: str
    element: str
    sexagenary_indexes: tuple[int, int]
    ganzhi: tuple[str, str]
    source_refs: tuple[str, ...] = NAYIN_SOURCE_REFS


def released_registry_hash() -> str:
    return object_sha256([list(row) for row in RELEASED_ZIWEI_NAYIN_PAIRS])


def validate_released_registry() -> None:
    if len(RELEASED_ZIWEI_NAYIN_PAIRS) != 30:
        raise ValueError("released Nayin registry must contain exactly 30 pairs")
    if len(SEXAGENARY_CYCLE) != 60:
        raise ValueError("Bazi sexagenary registry must contain exactly 60 identities")
    actual_hash = released_registry_hash()
    if actual_hash != RELEASED_ZIWEI_NAYIN_PAIRS_SHA256:
        raise ValueError(
            "released Ziwei Nayin registry drifted from BAZI-NAYIN-REGISTRY-R1: "
            f"{actual_hash}"
        )


validate_released_registry()

NAYIN_REGISTRY = tuple(
    NayinRegistryEntry(
        pair_index=pair_index,
        semantic_id=f"NAYIN:PAIR:{pair_index:02d}",
        display_name=display_name,
        element=element,
        sexagenary_indexes=(pair_index * 2, pair_index * 2 + 1),
        ganzhi=(SEXAGENARY_CYCLE[pair_index * 2], SEXAGENARY_CYCLE[pair_index * 2 + 1]),
    )
    for pair_index, (display_name, element) in enumerate(RELEASED_ZIWEI_NAYIN_PAIRS)
)


def entry_for_sexagenary_index(index: int) -> NayinRegistryEntry:
    if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < 60:
        raise ValueError(f"sexagenary index must be an integer in [0, 59], got {index!r}")
    return NAYIN_REGISTRY[index // 2]


def entry_for_ganzhi(ganzhi: str) -> NayinRegistryEntry:
    try:
        index = SEXAGENARY_CYCLE.index(ganzhi)
    except ValueError as exc:
        raise ValueError(f"invalid sexagenary identity: {ganzhi!r}") from exc
    return entry_for_sexagenary_index(index)
