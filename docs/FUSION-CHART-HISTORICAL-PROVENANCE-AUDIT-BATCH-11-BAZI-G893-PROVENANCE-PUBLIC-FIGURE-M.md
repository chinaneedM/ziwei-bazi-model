# Fusion Chart Historical Provenance & School Audit R1

## Batch 11M - Kyujanggak G893 Copy-Date Boundary & Public Opening-Figure Control

Status: **COMPLETE FOR COPY-DATE CONFLICT ADJUDICATION AND PUBLIC NON-TARGET OPENING-PAGE LOCALIZATION; SIX TARGET FOLIOS REMAIN OPEN**

Batch ID: `BATCH-11-BAZI-G893-PROVENANCE-PUBLIC-FIGURE-M`

This batch does not read or infer any of the six pending G893 target numeric
controls. It closes two provenance prerequisites that materially affect how the
early Korean witness may be weighted and searched:

1. the surviving G893 copy's exact printing year is **not source-closed**;
2. a public scholarly reproduction now directly exposes the physical object's
   opening solar-table page outside the institution's blocked renderer path.

The machine-readable evidence ledger is
`docs/research/KYUJANGGAK-G893-PROVENANCE-AND-PUBLIC-FIGURE-CONTROL-R1.json`.

## 1. Provider copy identity remains the controlling baseline

The live Kyujanggak catalog for `GK00893_00 / 奎貴893` states:

- title: `授時曆立成`;
- type: `甲寅字`;
- date: `15世紀 前半 (世宗 年間:1418-1450)`;
- extent: `1冊(102張)`;
- original digital images are available.

The provider does **not** state one exact printing year for the surviving copy.

Therefore the project copy-level date remains:

`G893_EXACT_SURVIVING_COPY_PRINT_YEAR = UNRESOLVED_WITHIN_1418_1450_PROVIDER_RANGE`

## 2. 1434 versus 1444 must be preserved, not silently normalized

Three high-quality secondary/bibliographic layers disagree:

- KOSTMA's print-history table lists `授時曆立成` under 1434 among
  first-cast `甲寅字` printing;
- Li Liang 2018 states that the extant Kyujanggak Shoushi licheng was
  reprinted in 1434;
- Li Liang's later chapter on sunrise/sunset tables identifies Kyujanggak
  collection no. 893 as printed in 1444.

None of those statements has yet been rebound in this project to a
copy-specific G893 colophon or an exact-year statement from the live provider
record.

The correct disposition is therefore:

`PRESERVE_1434_AND_1444_AS_CONFLICTING_SECONDARY_REPORTS`

and:

`DO_NOT_USE_1434_OR_1444_AS_A_NUMERIC_VARIANT_TIE_BREAKER`

This is particularly important because G893 is being used to investigate
transmission history between the Goryeosa received tradition and later Ming /
Japanese witnesses. An unclosed ten-year copy-date claim must not be converted
into false chronological precision.

## 3. Public object-level reproduction is now directly bound

Li Liang 2023, Figure 1, publicly reproduces the Kyujanggak Shoushi-licheng
object. The reviewable figure directly shows:

- cover title `授時曆`;
- `授時曆立成卷上`;
- `嘉儀大夫太史令臣王恂奉敕撰`;
- `太陽冬至前後二象盈初縮末限`;
- solar columns `初日` through `八日`.

This is stronger than catalog prose alone because it is object-level image
evidence for the opening solar table, visible through a public scholarly
reproduction outside the institutional renderer.

It is nevertheless a **secondary reproduction of a non-target page**.

The figure does not visibly contain D16, and it contains none of the lunar
L8/L101/L114/L124/L132 targets. Consequently:

`PUBLIC_OPENING_FIGURE_TARGET_VALUE_EFFECT = NONE`

No Goryeosa, Ming 1569, Ogawa 1673, or calculated value may be pre-populated
into G893 from this figure.

## 4. Search-space effect

Before this batch, the project had only textual-volume localization and
provider thumbnail filenames. The new figure directly establishes that the
opening solar table in this physical tradition begins with an `初日–八日`
block under the target table-family heading.

This narrows the next solar search to a **later page of the same printed table**
that must visibly contain `十六日`. It does not authorize a fixed folio
offset, a guessed filename, or the assumption that the provider thumbnail
`004b` is identical to the scholarly figure.

The lunar search remains unchanged: each control must be bound by the printed
table title, limit number, and field identity.

## 5. Image-access topology boundary

The live catalog currently exposes two real thumbnail image filenames:

- `GK00893_00IH_0001_000a.jpg`;
- `GK00893_00IH_0001_004b.jpg`.

The project's existing public adapter evidence documents Kyujanggak
`rendererImg.do` page discovery and `ImageServlet.do` full-image delivery.
GitHub-hosted Ubuntu TLS paths remain environment-blocked.

Batch 11M adds no claim that the public scholarly Figure 1 maps to either
thumbnail token, and no claim that a filename sequence can be used as folio
proof.

## 6. Six target controls remain fail-closed

All remain `PENDING_DIRECT_TARGET_PAGE`:

1. `VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE`;
2. `VAR-NUM-LUNAR-L8-LOSSGAIN`;
3. `NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING`;
4. `VAR-NUM-LUNAR-L114-DAYRATE`;
5. `VAR-NUM-LUNAR-L124-JI-XINGDU`;
6. `VAR-NUM-LUNAR-L132-LOSSGAIN`.

No G893 numeric target value is added in this batch.

## 7. Runtime consequence

None.

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

## 8. Next work

1. search for another public reproduction or mirror that visibly contains
   solar day 16;
2. bind lunar target pages by printed limit headings and field identity;
3. use the documented renderer/ImageServlet route only from a network path that
   actually reaches Kyujanggak, rather than repeating equivalent hosted-runner
   TLS failures;
4. keep exact surviving-copy year unresolved until copy-specific primary or
   provider evidence closes 1434 versus 1444;
5. only after direct G893 target glyph readings, return to transmission-stage
   causality for D16/L8/L124/L132 and the L101 positional bridge.
