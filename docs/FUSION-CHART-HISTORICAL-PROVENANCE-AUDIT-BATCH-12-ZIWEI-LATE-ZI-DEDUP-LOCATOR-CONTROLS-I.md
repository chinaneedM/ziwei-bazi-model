# Fusion Chart Historical Provenance Audit R1 — Batch 12I

## Late-Zi duplicate-lineage + locator-control closure

Status: **POST-12H PROBES ADJUDICATED / DUPLICATE PHYSICAL LINEAGE NOT DOUBLE-COUNTED / LOCATOR OBJECTS BOUND / NO INDEPENDENT TARGET PAGE / NO ALGORITHM REOPEN**

Batch 12I closes the committed work that appeared after Batch 12H. Its purpose is evidentiary hygiene: a second URL, index object or digitization route is not automatically a second physical witness.

## 1. Nanyangtang mirror vs National Archives Japan

The Batch 12A direct facsimile and the Batch 12H National Archives/Naikaku route share a strong chain of controls:

- the same seven-juan Fullbook identity and Nanyangtang publishing family;
- the same Japan Cabinet Library / 紅葉山文庫 provenance route;
- the exact National Archives call number `子０６０－０００１`, parent file `1078787` and known first-item `4468520` were already present in the Batch 12A acquisition artifact;
- public facsimile metadata identifies the Japan Cabinet Library copy and lists 卷五《論人生時要審的確》.

The physical-copy and digitization lineage are therefore **highly supported as the same copy/scan family**, although file-level identity is not closed until an official NAAJ JP2/page hash or the public facsimile binary is directly compared.

The counting rule is consequently:

```text
BATCH_12A_MIRROR_AS_HAI_WITNESS=1_DIRECT_PHYSICAL_COPY_LINEAGE
BATCH_12H_NAAJ_ROUTE_AS_SECOND_INDEPENDENT_HAI_WITNESS=NO
DUPLICATE_SCAN_LINEAGE_AS_CROSS_EDITION_CORROBORATION=FORBIDDEN
```

This correction is important: the Japan route strengthens provenance, but it does not yet establish cross-edition stability of the `亥時` glyph.

Machine control: `docs/research/ZIWEI-QUANSHU-NANYANGTANG-NAAJ-PHYSICAL-COPY-BRIDGE-R1.json`.

## 2. Zihai / Google Books locator controls

Three public-index probes were adjudicated.

The broad API discovery run `34134962705` / artifact `10023583175` returned no usable volume IDs; that result is not negative bibliographic proof.

Public object `hyotxQEACAAJ`, exposed in a Volume-4 search context, was probed in run `34135974564` / artifact `10023985930`. It does not close target-work presence or a target page.

More importantly, standalone Google Books object `kxdy0QEACAAJ` was directly retrieved in run `34136387337` / artifact `10024140134`. Its public bibliographic HTML is HTTP 200, 79,458 bytes, SHA-256 `b8da1b1fda8493c97dad0af82045a644b029a0ea786a8915664a7cb63015fa78`, and directly exposes the 2016 seven-juan `新鋟希夷陳先生紫微斗數全書` identity.

This closes the standalone bibliographic object. It does **not** close:

- which of the 15 `《子海珍本編·海外卷·日本：內閣文庫》` volumes contains the work;
- the target facsimile leaf/page;
- an independent physical witness.

The volume explicitly reports `searchable=false`; zero SearchWithinVolume results are therefore unusable as textual absence.

Machine control: `docs/research/ZIWEI-QUANSHU-ZIHAI-NAIKAKU-VOLUME-LOCATOR-R1.json`.

## 3. Wenguang comparison-book locator

Google Books volume `RISpDgAAQBAJ`, 潘國森《紫微斗數全書古訣辨正》, was probed in run `34137662618` / artifact `10024619096`.

The public index strengthens the edition map:

- `文光堂`: 10 indexed page hits;
- `敦化堂`: PA13 / PA14;
- `繼述堂`: PA13 / PA14.

But exact late-Zi controls `論人生時要審的確 / 上五刻 / 下五刻 / 子時有十刻 / 南陽堂` returned no useful target hit. The two `亥時` hits at PA43/PA53 are unrelated ordinary birth-hour examples.

Thus this source remains a **modern secondary edition locator**. It cannot supply the missing physical Wenguang target glyph.

Machine control: `docs/research/ZIWEI-WENGUANG-COMPARISON-BOOK-LATE-ZI-INDEX-LOCATOR-R1.json`.

## 4. Shidian target-page API control

Commit `afaab66575f89d6e34f4ded4c0150d3deb42fe76` added a public-only probe using IDs already exposed by the reviewed Shidian target surface:

- book `SDZJ0170`;
- volume `7330179081331277875`;
- middle page `7330179103183667235`;
- version `44`.

Workflow run `34138050721`, job `101793499709`, artifact `10024763004` succeeded.

The public middle-page HTML returned HTTP 200, 241,798 bytes, SHA-256 `e068c1b18ac7f4da92528270360d6442e089e4865bd30b389937a0ff627abb66`. The known volume/middle-page API controls each returned HTTP 200 and a 33-byte JSON response with SHA-256 `757892ec1b4b89c47dfa1d7df9b00af36f4d1f840d0dd0416ed6b82287997709`.

Crucially:

```text
RETURNED_IMAGE_URL_CANDIDATES=0
FETCHED_IMAGE_CANDIDATES=0
SAVED_IMAGES=0
TARGET_PHYSICAL_PAGE_DIRECTLY_OBSERVED=NO
```

No identifier enumeration, authentication bypass or token guessing was attempted. API reachability therefore adds no physical-glyph authority to the existing received transcription.

## 5. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
DIRECT_INDEPENDENT_HAI_GLYPH_WITNESS_COUNT_ADDED=0
HAI_GLYPH_STABILITY_ACROSS_PHYSICAL_EDITIONS=UNRESOLVED_PENDING_DIRECT_INDEPENDENT_PHYSICAL_TARGET_PAGES
RUNTIME_TIME_STANDARD_BINDING=UNRESOLVED
NEW_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
```

The best next evidence is **not another mirror of the same Naikaku copy**. Priority shifts to a directly readable target page from a genuinely independent physical route: Wenguangtang (敦化堂/繼述堂), Jingluntang, Wenchengtang/Guangyi, or Lianyuange Quanji. An official NAAJ JP2/page hash remains valuable for same-copy provenance closure, but cannot be counted as a second independent edition witness unless a distinct copy is established.

## 6. Accounting

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

Aggregate machine evidence: `docs/research/ZIWEI-LATE-ZI-DEDUP-LOCATOR-CONTROLS-R1.json`.

The deterministic fusion-chart product remains CLOSED.
