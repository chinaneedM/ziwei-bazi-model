# Historical Provenance Audit — Batch 12GE

## 1. Batch identity

- Batch: `BATCH-12-ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-JAPAN-PHYSICAL-SERIAL-HOLDINGS-AND-COPY-ACTION-BOUNDARY-GE`
- Prior batch: `BATCH-12-ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-PKU-TITLE-PHRASE-INDEX-NONMATCH-BOUNDARY-GD`
- Scope: physical-journal access routes for `《中国典籍与文化》2008(03)`, especially the target serial article `《五石斋文史札记（二十八）》`, pp.121–129.
- This is an access/provenance-control batch only. It does not reopen deterministic chart algorithms.

## 2. Why this route is now higher value

Batch 12GD correctly demonstrated that current PKU title-scoped phrase nonmatches are index behavior only and cannot be promoted to negative collation of the article body.

The next useful step is therefore not more phrase-index probing. It is to identify direct physical holdings of the target issue that can support lawful inspection or copying of the actual pp.121–129.

## 3. National Diet Library first-party serial holding

The National Diet Library first-party record for `中國典籍與文化` is:

- NDL call number: `Z21-AC41`;
- NDLBibID: `a0000052718`;
- carrier: paper;
- holdings: `1994年1期 总8期` through `2018年4期 总107期`.

This listed holding span covers `2008(03)`.

That closes a direct **physical serial holding route**, but not yet the exact child-record/material identifier for `2008(03)`.

Therefore:

- `TARGET_ISSUE_WITHIN_NDL_HOLDING_SPAN=true`;
- `EXACT_2008_03_CHILD_RECORD_ID=UNRESOLVED`;
- `EXACT_2008_03_MATERIAL_LABEL_ID=UNRESOLVED`;
- `PP121_129_DIRECTLY_REVIEWED=false`.

## 4. CiNii union-catalog controls

CiNii record `AA1225301X` / ISSN `10043241` independently exposes several Japanese university holdings whose stated ranges include 2008:

- 学習院大学 図書館 — `123/2//P` — 2008 included;
- 京都大学 人文科学研究所 図書室 — `222.005||C/62` — 2008 included;
- 拓殖大学 八王子図書館 — 2007–2024 span includes 2008;
- 東京大学 東洋文化研究所 図書室 — `CZZ:296` — 2008 included;
- 佛教大学 附属図書館 — 1993–2009 span includes 2008;
- 早稲田大学 図書館（中央図書館） — 1992–2025 span includes 2008.

A useful negative holding control is also visible:

- 奈良大学 図書館 lists `2008(1-2)`, not `2008(3)`; it is therefore not counted as a target-issue route.

These holdings are access locators only. No target article page has been inspected through them.

## 5. Copy / ILL action boundary

NDL's official help documents that some NDL-tagged materials can be obtained by **paid remote copy** without visiting the library, and that registered individual users can use an **article-location investigation** service.

The exact target issue's eligibility has **not** been checked through an authenticated cart.

The Gakushuin OPAC surface for NCID `AA1225301X` also exposes user-service controls for:

- InterLibrary Copy Request;
- InterLibrary Loan Request;
- Login.

Those controls demonstrate an actionable service surface, not user eligibility or target-issue copy eligibility.

No account login, ILL request, remote-copy request, article-location investigation, purchase or fee was performed.

## 6. Authority firewall

The following equivalences are explicitly forbidden:

- series holding span ≠ target page review;
- union-catalog holding ≠ article-text authority;
- copy-service availability ≠ target-issue eligibility;
- physical holding ≠ exact issue-item identity;
- target issue in a stated range ≠ exact material-label ID;
- article pp.121–129 ≠ exact 1950-01-29 page;
- no account action ≠ service unavailable.

## 7. Target status

After Batch 12GE:

- article range remains **121–129**;
- `1950-01-29 exact journal page = UNRESOLVED`;
- `1950-01-29 primary journal text = NOT_REVIEWED`;
- `1950-01-29 exact 2007 facsimile page = UNRESOLVED`;
- direct physical 2008-issue access routes are expanded to NDL plus multiple Japanese university holdings;
- exact NDL child record/material ID remains unresolved.

No target `3482/3483` transaction route is selected.

## 8. Product / genealogy consequence

`NODES_ADDED=0`; `EDGES_ADDED=0`; `ACQUISITION_EDGE_AUTHORIZED=false`; `SAME_OBJECT_EDGE_AUTHORIZED=false`; `RUNTIME_RULE_CHANGE=false`; `ALGORITHM_REOPEN=false`; `CANDIDATE_COLLAPSE=false`.

Matrix row/audited/missing counts remain **198 / 166 / 10**. Provenance defects remain **14 / 14 repaired**. Chart algorithm defects remain **0**. `DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`.

## 9. Highest next gate

1. Resolve the exact NDL child record/material identifier for `中國典籍與文化 2008(3)` without guessing identifiers.
2. Determine exact target-issue remote-copy or article-location-investigation eligibility only from source-emitted service state.
3. Continue public searches for an exact 1950-01-29 serial page/citation before any account-based request.
4. If a lawful copy/page object is obtained, directly collate pp.121–129 and bind 1950-01-29 to its exact page and punctuation-independent wording.
5. Continue the 2007 facsimile volume-5 page/leaf route, plus FV Jan-6, NLC [23]/[24], Ji Shuying chapter 9 and Gao Xizeng annotated-catalog routes in parallel.

Machine evidence: `docs/research/ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-JAPAN-PHYSICAL-SERIAL-HOLDINGS-COPY-ACTION-BOUNDARY-R1.json`.
