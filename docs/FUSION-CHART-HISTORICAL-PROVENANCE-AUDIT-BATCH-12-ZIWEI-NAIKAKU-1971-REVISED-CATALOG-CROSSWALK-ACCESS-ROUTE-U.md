# Fusion Chart Historical Provenance Audit R1 — Batch 12U

## Naikaku 1971 revised catalog crosswalk access route

Status: **OFFICIAL REVISED-CATALOG OBJECT + OCR/TRANSMISSION ROUTE BOUND / TARGET 15856 → 子060-0001 ENTRY NOT OBSERVED / NO NEGATIVE WHOLE-CATALOG CLAIM / ZERO RULE EFFECT / NO ALGORITHM REOPEN**

Batch 12U follows Batch 12T's high-confidence physical-lineage convergence and asks the narrower unresolved question: can the legacy label `漢 / 子六十 / 一五八五六 / 全二` be explicitly crosswalked to current National Archives call `子060-0001` by a first-party catalog source?

### 1. Official 1971 revised catalog object

The National Diet Library public record binds `内閣文庫漢籍分類目録 改訂` to:

- author/publisher: `内閣文庫`;
- publication year: `1971`;
- NDL call: `UP111-59`;
- NDL bibliographic ID: `000001237342`;
- persistent PID: `12282052`;
- DOI: `10.11501/12282052`;
- material: paper + digital, one volume, 27 cm.

This is the strongest currently located public acquisition route to the revised Naikaku Chinese-book catalog itself. It is a catalog-object/access witness, not yet a target-entry witness.

### 2. OCR and legitimate-access boundary

The NDL Minna Search record binds the same PID to an uncorrected plain-text OCR derivative made by the National Diet Library. The public metadata records digitization on 2022-03-22, public start on 2022-05-31, `image/jp2`, and library/individual transmission eligibility.

The reviewed unauthenticated surface does not expose the OCR body. No login, transmission entitlement, library request, remote-copy request, paid request, credential reuse, or access-control bypass was attempted.

Therefore:

```text
1971_REVISED_CATALOG_DIGITAL_OBJECT=BOUND
OCR_DERIVATIVE_EXISTS=YES
UNAUTHENTICATED_TARGET_ENTRY_TEXT=NOT_OBSERVED
ACCESS_BYPASS=NO
```

### 3. National Archives index-structure control

Hiroshi Tsuchiya of the National Archives of Japan states in the 2009 National Archives journal article on the Naikaku Chinese catalog that the 1971 revised `内閣文庫漢籍分類目録` contains a list of document names at its end, while modern National Archives digital search permits keyword lookup across names/authors.

This independently makes the 1971 revised catalog a plausible direct bridge source for the old-number question. The article does **not** quote the Ziwei target entry and does not state `15856 -> 子060-0001`.

### 4. Epistemic ceiling

No explicit old-registration migration line was observed on the reviewed public metadata/index surfaces. This is deliberately **not** a whole-catalog negative claim because the target OCR/page body remains behind legitimate access controls.

Batch 12T therefore remains controlling:

```text
BATCH12A_TO_NAJ_PHYSICAL_LINEAGE=HIGH_CONFIDENCE
LEGACY_REGISTRATION_15856_TO_CURRENT_CALL=UNRESOLVED
BATCH12A_AND_NAJ_AS_TWO_INDEPENDENT_TEXTUAL_WITNESSES=NO
```

### 5. Rule effect

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
DIRECT_INDEPENDENT_HAI_GLYPH_WITNESS_ADDED=0
NEW_CHART_RULE_CANDIDATE=NO
CANDIDATE_SELECTION=NO
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
```

The deterministic product remains CLOSED. The next decisive gate is the actual 1971 revised-catalog target entry (or another explicit first-party old-number crosswalk). In parallel, the independent direct `五凶神` physical-page search remains valid.

Machine evidence: `docs/research/ZIWEI-NAIKAKU-1971-REVISED-CATALOG-CROSSWALK-ACCESS-ROUTE-R1.json`.
