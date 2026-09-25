# Historical Provenance Audit — Batch 12GG

## 1. Batch identity

- Batch: `BATCH-12-ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-NDL-REMOTE-COPY-FRONTEND-CONTRACT-STATIC-BOUNDARY-GG`
- Prior batch: `BATCH-12-ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-NDL-2008-03-EXACT-CHILD-RECORD-AND-COPY-SURFACE-BOUNDARY-GF`
- Scope: source-emitted NDL frontend request/copy contracts and anonymous exact-child request state.
- This is an access-control batch only.

## 2. What the frontend proves

The exact target child remains:

`https://ndlsearch.ndl.go.jp/books/R100000002-Ia0000052718-i25264793`

The source-emitted entry module `/_nuxt/QlNHqkx-.js` and its finite first-level imports were statically inspected without executing request APIs.

The code directly demonstrates that NDL Search has global request flows including:

- `/request/cart`;
- `/request/rcopy/agree`;
- `/request/rcopy/input`;
- `/request/rcopy/confirm`;
- `/request/rcopy/docs`;
- `/request/rcopy/fee`;
- `/request/rcopy/complete`;
- `/api/cart`;
- `/api/request`;
- `/api/request/without-cart`;
- `/copy/remote`;
- `/help/remotecopy`.

This closes **global remote-copy frontend existence**, not target eligibility.

## 3. Request-object contract

The static `rcopy` store builds requests from previously populated `requestItemFromTml / requestItemFromKsk / requestItemFromIlcl` entries.

The request creation path expects target-specific fields including:

- `cartItemId`;
- `rcopyPartItemId`;
- `risItemId / itemId`;
- `bibId`;
- `maximumFee`;
- `rcopyPatronNote`.

For `i25264793`, none of those target-specific request objects was obtained.

## 4. Anonymous state must not be misread as denial

The exact child page's anonymous initial state contains:

- `checkedCartItems=[]`;
- `requestCount=0`;
- `requestItemFromTml=[]`;
- `requestItemFromKsk=[]`;
- `requestItemFromIlcl=[]`.

Those values are default anonymous/client state. They are **not** an eligibility decision and are not evidence that copying is forbidden.

Similarly, the target bibliographic record being `PUBLIC` means its public metadata page is exposed; it does not mean a copy request is authorized.

## 5. Static-probe control

Research run `36098813291`:

- artifact: `10848705735`;
- artifact digest: `sha256:459e0abc6ba0f66200a78d99f6d20339cf0fd506387570b07b65d333ad1100a9`;
- entry module SHA-256: `095c1b4e55d21b0378d8e2b70516d77d1b022ee4d779d6071fdfa17b7eda0575`;
- entry module bytes: `3488867`;
- 75 source-emitted modules were read;
- no request/copy API was executed;
- no login occurred;
- no request was submitted.

## 6. Access firewall

The following are forbidden equivalences:

- global remote-copy routes ≠ target issue eligibility;
- public bibliographic metadata ≠ copy permission;
- empty anonymous request store ≠ copy denial;
- request schema ≠ target request object;
- discovering `/api/cart` or `/api/request` ≠ authorization to execute them.

No login, copy request, article-location investigation, ILL request, fee or purchase occurred.

## 7. Stop rule

Generic NDL frontend-route archaeology is now **deprioritized**.

The global request architecture is sufficiently established. Without a source-emitted target-specific request/material object, further enumeration of generic frontend routes has low historical value.

Research priority returns to the actual historical target:

1. exact 1950-01-29 page/text in `《五石斋文史札记（二十八）》`, pp.121–129;
2. exact 2007 facsimile volume-5 page/leaf and handwriting.

## 8. Product / genealogy consequence

`NODES_ADDED=0`; `EDGES_ADDED=0`; `ACQUISITION_EDGE_AUTHORIZED=false`; `SAME_OBJECT_EDGE_AUTHORIZED=false`; `RUNTIME_RULE_CHANGE=false`; `ALGORITHM_REOPEN=false`; `CANDIDATE_COLLAPSE=false`.

Matrix row/audited/missing counts remain **198 / 166 / 10**. Provenance defects remain **14 / 14 repaired**. Chart algorithm defects remain **0**. `DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`.

Machine evidence: `docs/research/ZIWEI-DENG-ZHICHENG-WUSHIZHAI28-NDL-REMOTE-COPY-FRONTEND-CONTRACT-STATIC-BOUNDARY-R1.json`.
