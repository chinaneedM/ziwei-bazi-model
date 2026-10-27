# Historical Provenance Audit — Batch 12GF

## 1. Batch identity

- Batch: `BATCH-12-ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-NDL-2008-03-EXACT-CHILD-RECORD-AND-COPY-SURFACE-BOUNDARY-GF`
- Prior batch: `BATCH-12-ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-JAPAN-PHYSICAL-SERIAL-HOLDINGS-AND-COPY-ACTION-BOUNDARY-GE`
- Scope: exact National Diet Library issue-child identity for `中國典籍與文化 2008(3)`, the issue containing `《五石斋文史札记（二十八）》`, pp.121–129.
- This is an access/provenance-control batch only.

## 2. Exact target issue child record is now closed

GE established that the NDL paper-serial holding span under call number `Z21-AC41` / NDLBibID `a0000052718` covers 2008(03), but did not resolve the exact issue-child record.

A finite traversal of the NDL parent serial's own source-emitted child list was then performed using only four public pagination offsets: `0 / 20 / 40 / 60`. No child identifier was guessed.

At offset 40, NDL source-emits:

- `中國典籍與文化 2008(2) (通号 65) 2008` → `...-i25264749`;
- **`中國典籍與文化 2008(3) (通号 66) 2008` → `...-i25264793`;**
- `中國典籍與文化 2008(4) (通号 67) 2008` → `...-i25264816`.

Therefore:

`EXACT_2008_03_NDL_CHILD_RECORD=CLOSED_SOURCE_EMITTED_FIRST_PARTY`

Target URL:

`https://ndlsearch.ndl.go.jp/books/R100000002-Ia0000052718-i25264793`

This also closes the target issue as **通号66** at first-party NDL level.

## 3. Direct child-page control

Direct anonymous retrieval of the exact source-emitted child URL returns:

- HTTP 200;
- `text/html;charset=utf-8`;
- SHA-256 `b8678d1bab127f7ee45ef5851aa8d16fc2a03cc1d5a606e18baad9abc8823e29`;
- 201873 bytes;
- title: `中國典籍與文化 2008(3) (通号 66) 2008 | NDLサーチ | 国立国会図書館`;
- call number: `Z21-AC41`;
- NDL bibliographic ID: `a0000052718`.

The page also carries the CiNii identity `AA1225301X`.

## 4. Copy/access surface

The reviewed static child page source-emits generic NDL access-help links:

- `インターネットで資料を読む`;
- `資料のコピーを入手する`;
- `図書館で資料を読む`.

The static page does **not** directly source-emit target-specific confirmation that this exact issue can currently be remotely copied, that an article-location request is eligible, or that pp.121–129 are directly readable online.

No exact material-label/copy-item ID has yet been demonstrated.

Therefore:

- generic copy help ≠ target-specific remote-copy eligibility;
- exact issue child record ≠ exact article page;
- issue identity ≠ primary article text;
- call number/BibID ≠ material-label ID;
- generic application infrastructure ≠ requestable target item.

No login, remote-copy request, article-location investigation, ILL request, fee or purchase occurred.

## 5. Historical target status

The target article remains:

- PKU article ID `286663046`;
- `中国典籍与文化 2008(03)`;
- pp.121–129.

GF changes only issue-level physical provenance/access precision.

Still unresolved:

- whether 1950-01-29 is present in the directly reviewed article body;
- its exact journal page;
- primary journal wording;
- target-specific NDL copy eligibility;
- exact NDL material/item label;
- 2007 facsimile volume-5 exact page/leaf;
- direct handwriting.

No page number is inferred from date position.

## 6. Product / genealogy consequence

`NODES_ADDED=0`; `EDGES_ADDED=0`; `ACQUISITION_EDGE_AUTHORIZED=false`; `SAME_OBJECT_EDGE_AUTHORIZED=false`; `RUNTIME_RULE_CHANGE=false`; `ALGORITHM_REOPEN=false`; `CANDIDATE_COLLAPSE=false`.

Matrix row/audited/missing counts remain **198 / 166 / 10**. Provenance defects remain **14 / 14 repaired**. Chart algorithm defects remain **0**. `DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`.

## 7. Highest next gate

1. Inspect only source-emitted structured state/endpoints from exact child `i25264793` for a demonstrable material label or target-specific public request/copy state; no identifier guessing.
2. Continue public exact-page citation/fulltext discovery for the 2008 serial pp.121–129 and locate 1950-01-29 without interpolation.
3. Continue the 2007 facsimile volume-5 page/leaf route and directly collate handwriting if obtained.
4. If public routes remain insufficient, any authenticated NDL copy/article-location request remains an explicit user-account/external-action boundary.
5. Continue FV Jan-6, NLC [23]/[24], Ji Shuying chapter 9 and Gao Xizeng annotated-catalog routes in parallel.

Machine evidence: `docs/research/ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-NDL-2008-03-EXACT-CHILD-RECORD-AND-COPY-SURFACE-BOUNDARY-R1.json`.
