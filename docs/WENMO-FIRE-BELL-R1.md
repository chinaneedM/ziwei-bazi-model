# WENMO FIRE / BELL R1

Status: external compatibility reconstruction, not canonical-source authority.

## Scope

This note closes the Wenmo-default Fire/Bell discriminator matrix after an external fixture was supplied for the previously missing `巳酉丑` year-branch trine class.

The reconstruction belongs only to `WENMO_DEFAULT_CORE_AUX_R1`. It does **not** overwrite the divergent strict QS witness family and does not modify `sources/canonical/`.

## Reconstructed generator

At Zi hour, select the starting branches by birth-year trine class:

| Year-branch trine | Fire start | Bell start | External discriminator |
|---|---:|---:|---|
| 寅午戌 | 丑 | 卯 | WENMO-CHARTDIFF-004: 戌年子时 -> 火丑 / 铃卯 |
| 申子辰 | 寅 | 戌 | WENMO-CHARTDIFF-002/003: 子年午时 -> 火申 / 铃辰 |
| 巳酉丑 | 卯 | 戌 | WENMO-CHARTDIFF-006: 巳年午时 -> 火酉 / 铃辰 |
| 亥卯未 | 酉 | 戌 | WENMO-CHARTDIFF-005: 未年午时 -> 火卯 / 铃辰 |

Then advance **both** Fire and Bell one Z12 address per birth-hour index, with Zi = 0, Chou = 1, ..., Hai = 11.

Formally, for a selected trine-class start pair `(F0, B0)` and hour index `h`:

- `Fire = F0 + h (mod 12)`
- `Bell = B0 + h (mod 12)`

## Why CHARTDIFF-005 is still usable here

The 1991 fixture is not a valid end-to-end time oracle because Wenmo's displayed true-solar time behaves as fixed UTC+8 while the engine preserves historical China DST. However, the external chart itself explicitly declares an 午-hour chart and directly displays 火卯 / 铃辰. That observation is sufficient to discriminate the Wenmo Fire/Bell rule family for the `亥卯未` class without redefining the physical Time/Calendar layer.

## New discriminator: WENMO-CHARTDIFF-006

Input:

- male
- Beijing, longitude 116.400E
- civil time: 2001-12-15 12:00
- Wenmo true-solar display: 11:50
- lunar label: 辛巳年冬月初一日午时
- Life / Body: 午 / 午
- Five-Element Bureau: 金四局, Life palace 甲午
- Fire / Bell: 酉 / 辰

This fixture also closes the current Wenmo operational comparison scope at 28 generated placements: fourteen main stars plus fourteen auxiliary placements including Fire/Bell.

## Release boundary

- External compatibility fixture: yes.
- Wenmo operational Profile generator: yes.
- Canonical source claim: no.
- Strict QS Fire/Bell replacement: no.
- `sources/canonical/` modification: no.
- `model-learning/` modification: no.
