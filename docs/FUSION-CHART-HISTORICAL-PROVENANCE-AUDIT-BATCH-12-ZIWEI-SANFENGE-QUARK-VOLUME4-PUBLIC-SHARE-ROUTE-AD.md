# Fusion Chart Historical Provenance Audit R1 — Batch 12AD

## Sanfenge provider index → exact article → Quark public-share route for Fullbook volume four

Status: **PROVIDER-SIDE FILE/ARTICLE/SHARE BINDING CLOSED / PUBLIC SHARE SPA SHELL REACHED / PDF BYTES NOT OBSERVED / EDITION IDENTITY UNRESOLVED / ZERO TEXTUAL OR HAI-GLYPH VOTES / NO ALGORITHM EFFECT**

## 1. Scope

Batch 12AD continues `HPA-ZDATE-006` after Batch 12AC. It does not reopen deterministic chart algorithms. Its purpose is to determine whether recently surfaced standalone `紫薇斗数全书卷4.pdf` resources provide a reproducible route to the target late-Zi leaf.

The evidentiary firewall is strict:

```text
filename/index identity != edition identity
public cloud-share URL != observed file bytes
observed file bytes != physical-edition provenance
physical-edition provenance != target-glyph observation
```

## 2. Sanfenge provider-side binding

The provider page `https://www.sanfenge.com/col.jsp?id=112&m485pageno=2` returns gzip-compressed HTML. Earlier probes that treated the compressed body as text are superseded. Gzip-aware run `34312000287` directly decoded the provider response as UTF-8 and observed the relevant records in the site's own page data.

```text
article 212163
紫薇术紫薇斗数全书卷4.pdf
https://www.sanfenge.com/h-nd-212163.html
source-emitted share: https://pan.quark.cn/s/6956a639be12

article 212173
紫薇术《紫微斗数全书》四卷.pdf
https://www.sanfenge.com/h-nd-212173.html
source-emitted share: https://pan.quark.cn/s/9f7f6a4e7730
```

The first route is especially relevant because the provider explicitly labels it `卷4.pdf`. This closes the provider-side chain from filename to article identity to exact public-share URL. It does **not** identify the underlying historical edition.

Provider response controls:

```text
raw bytes = 97,735
raw SHA-256 = 670bd6dc088e978afb5cc3665e419b0fcec91fa29809c56c3d51c8213b25487a
decoded bytes = 1,362,516
decoded SHA-256 = 26a0e7e7b52ad1043e8286410e90a974d9b4292f73ce70b06201a9157a71fac6
```

## 3. Quark public-share boundary

Run `34312186561` fetched only the exact share URLs emitted by Sanfenge. Both returned HTTP 200 public share shells. The initial HTML contains generic Quark cloud-drive UI metadata, but neither expected filename nor PDF bytes are present in that initial response.

```text
PUBLIC_SHARE_SURFACE=REACHED
PUBLIC_FILENAME_IN_INITIAL_QUARK_HTML=NOT_OBSERVED
DIRECT_PDF_BYTES=NOT_OBSERVED
LOGIN_ATTEMPTED=NO
CLOUD_SAVE_ATTEMPTED=NO
HIDDEN_API_GUESSING=NO
ACCESS_CONTROL_BYPASS=NO
```

This is a current public-access boundary, not evidence that the shared files are absent or invalid.

## 4. Provenance adjudication

The Sanfenge route is useful as an acquisition locator because the provider itself binds the filenames, exact article IDs and exact public-share URLs. It is **not** promoted to historical textual authority because the underlying file bytes, internal title page, imprint and target leaf remain unobserved.

No inference is allowed from the generic filename to any known Fullbook lineage such as 南陽堂、敦化堂、繼述堂、經述堂、經綸堂、文誠堂 or another witness.

## 5. HPA-ZDATE-006 after Batch 12AD

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
WITHIN_FULLBOOK_HAI_GLYPH_STABILITY=UNRESOLVED
BATCH_12AD_TEXTUAL_WITNESS_INCREMENT=0
BATCH_12AD_HAI_GLYPH_WITNESS_INCREMENT=0
NEW_CANDIDATE_FAMILY=NO
CANDIDATE_SELECTION=NO
ALGORITHM_REOPEN=NO
CANDIDATE_COLLAPSE=0
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT_ROWS=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
```

The deterministic fusion-chart product remains CLOSED.

## 6. Next evidence gate

The next high-value gate remains a directly readable `《論人生時要審的確》` leaf from a physically bound Fullbook edition whose edition/imprint can be independently established. The new Sanfenge/Quark route remains worth revisiting only through normal public share/viewer behavior if it later exposes the file itself; no login, transfer-to-cloud, hidden API guessing or bypass is authorized.

## 7. Machine evidence

Primary machine artifact:

`docs/research/ZIWEI-SANFENGE-QUARK-VOLUME4-PUBLIC-SHARE-ROUTE-R1.json`

## 8. Closure execution binding

Batch 12AD state synchronization was executed by fail-closed workflow run `34312602674`. Before committing, that workflow passed the Fusion Chart Historical Provenance Audit R1 machine gate, the Project Continuity State R1 machine gate, and the focused `test_fusion_chart_historical_provenance_audit_matrix_r1.py` suite. It then produced closure commit `0281adda29690e7f8bf5d9dee343f2098e85ba8b` (tree `16991d5755ffd1b07007eb8570e1b0bf11153b75`). This binding records execution provenance only; it adds no textual evidence, no witness vote, and no algorithm effect.
