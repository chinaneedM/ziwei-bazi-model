# Fusion Chart Historical Provenance & School Audit R1

## Batch 11Q - Kyujanggak G893 Hosted-Access Boundary & Mirror Discovery Routes

Status: **COMPLETE FOR GITHUB-HOSTED ACCESS EXHAUSTION AND MIRROR-ROUTE DISCOVERY; SIX TARGET FOLIOS REMAIN OPEN**

Batch ID: `BATCH-11-BAZI-G893-ACCESS-MIRROR-ROUTES-Q`

Machine-readable evidence:

- `docs/research/KYUJANGGAK-G893-IMAGE-ACCESS-TOPOLOGY-R1.json`
- `docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json`

This batch does not read, infer or pre-populate any of the six pending G893
numeric controls. It closes the execution-environment boundary around the
official Kyujanggak renderer and records two independent routes for future
page acquisition without converting locator evidence into textual evidence.

## 1. G893 object identity and target state are unchanged

The controlling institutional object remains:

- title: `授時曆立成`;
- catalog identifier: `奎貴893`;
- `BOOK_CD=GK00893_00`;
- `ITEM_CD=SIC`;
- provider date: first half of the fifteenth century / Sejong 1418-1450;
- physical extent: one book, 102 leaves.

The surviving copy's exact print year remains unresolved because the provider
does not select one exact year while high-quality secondary reports conflict
between 1434 and 1444.

All six controls remain `PENDING_DIRECT_TARGET_PAGE`:

1. `VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE`;
2. `VAR-NUM-LUNAR-L8-LOSSGAIN`;
3. `NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING`;
4. `VAR-NUM-LUNAR-L114-DAYRATE`;
5. `VAR-NUM-LUNAR-L124-JI-XINGDU`;
6. `VAR-NUM-LUNAR-L132-LOSSGAIN`.

## 2. Equivalent GitHub-hosted access routes are now exhausted

The project has directly tested the G893 renderer from all three available
GitHub-hosted OS families with read-only transports:

| Runner family | Workflow / job | Transport | Result |
| --- | --- | --- | --- |
| Ubuntu | `33962192868` | requests / urllib3 | TLS connection reset |
| Ubuntu | `33962291588` | curl_cffi Chrome impersonation | TLS connection reset |
| macOS | `34027558494 / 101471139340` | curl_cffi Chrome impersonation | curl 35 receive reset |
| Windows | `34027558494 / 101471139387` | curl_cffi Chrome impersonation | curl 35 receive reset |

The macOS and Windows diagnostic artifacts are `9987542932` and
`9987546688`. They contain only the attempt/error records; no page manifest,
page image or target glyph was returned. OCR was not used.

Therefore:

```text
GITHUB_HOSTED_G893_EQUIVALENT_TRANSPORTS=EXHAUSTED
NETWORK_FAILURE_AS_SOURCE_EVIDENCE=FORBIDDEN
NETWORK_FAILURE_AS_FOLIO_OR_GLYPH_EVIDENCE=FORBIDDEN
```

Equivalent GitHub-hosted retries must not be repeated merely by changing runner
OS or HTTP/TLS client.

## 3. The Kyujanggak renderer is not globally unavailable

A separate public technical witness records a 2026-08-26 Wikimedia Commons
upload sourced from the same Kyujanggak `rendererImg.do` family for another
institutional object, `GK17375_00 / 奎17375`.

This establishes only that a non-GitHub network path has successfully acquired
pages from the renderer family. It does **not** prove that the same path will
reach G893 and supplies no G893 folio, page identity or glyph.

Therefore:

```text
OTHER_OBJECT_RENDERER_SUCCESS_AS_G893_ACCESS_PROOF=FORBIDDEN
OTHER_OBJECT_RENDERER_SUCCESS_AS_G893_TARGET_EVIDENCE=FORBIDDEN
```

## 4. Legacy DVD04 route is a locator lead, not an edition witness

A 2015 third-party catalog for an offline package titled
`奎章閣漢文文獻珍藏` reports 64 works across five DVDs, predominantly PDF/DJVU,
and lists `授時曆立成` under DVD04.

The underlying file has not been retrieved in this project. Its relation to
`GK00893_00 / 奎貴893`, completeness, image fidelity and authorization have
not been independently established.

Accordingly the route is retained only as a discovery lead:

```text
LEGACY_DVD04_FILE_RETRIEVED=FALSE
LEGACY_DVD04_G893_IDENTITY_BOUND=FALSE
LEGACY_DVD04_TARGET_FOLIO_EFFECT=NONE
LEGACY_DVD04_TARGET_GLYPH_EFFECT=NONE
```

Only an authorized or publicly reviewable copy whose visible object metadata
can be bound to the G893 object may advance this route.

## 5. G893 and Kang Bo's derived licheng remain separate works

The project's existing Li Liang 2023 separation is now independently
corroborated by Yu Gyung Ro's 1997 Sejong-period astronomical-book list, which
lists `授時曆立成` and Kang Bo's `授時曆捷法立成` as separate books.

This strengthens work-identity separation only. It does not authorize the
derived work as a substitute for G893 and does not transfer any row value.

```text
KANG_BO_JIEFA_LICHENG_AS_G893_SUBSTITUTE=FORBIDDEN
```

## 6. Runtime and audit-count consequence

None.

This batch adds access/provenance evidence and search topology, not a newly
audited chart rule family. Matrix row and audit counts therefore remain
unchanged.

```text
HISTORICAL_PROVENANCE_ROW_COUNT=197
AUDITED_ROW_COUNT=165
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

## 7. Next work

1. locate an authorized or publicly reviewable copy of the legacy DVD04
   `授時曆立成` file and bind it to `GK00893_00` by visible object metadata
   before using any page;
2. continue searching public scholarly reproductions and mirrors for later
   G893 solar pages and the lunar table;
3. use the official renderer/ImageServlet protocol only from a genuinely
   non-GitHub-hosted browser/network path rather than repeating equivalent
   hosted-runner probes;
4. bind solar D16 only from a page that visibly contains `十六日` and the
   correct target field schema;
5. bind L8/L101/L114/L124/L132 only from printed table headings, limit numbers
   and mechanically mapped fields, then read glyphs directly without
   pre-population from Goryeosa, Ming, Ogawa, G894, Sillok or Kang Bo;
6. continue Sillok solar D16 continuation-image research independently.
