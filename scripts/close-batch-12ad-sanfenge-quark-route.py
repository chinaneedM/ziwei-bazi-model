#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH_ID = "BATCH-12-ZIWEI-SANFENGE-QUARK-VOLUME4-PUBLIC-SHARE-ROUTE-AD"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SANFENGE-QUARK-VOLUME4-PUBLIC-SHARE-ROUTE-AD.md"
EVIDENCE_PATH = "docs/research/ZIWEI-SANFENGE-QUARK-VOLUME4-PUBLIC-SHARE-ROUTE-R1.json"
SOURCE_ID = "EXT-SANFENGE-ZWDSQS-V4-QUARK-PUBLIC-SHARE"


def dump(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    evidence = {
        "schema": "ZIWEI-SANFENGE-QUARK-VOLUME4-PUBLIC-SHARE-ROUTE-R1",
        "batch_id": BATCH_ID,
        "access_date": "2026-09-09",
        "status": "PROVIDER_FILENAME_ARTICLE_AND_PUBLIC_SHARE_BINDING_CLOSED_CONTENT_BYTES_AND_EDITION_IDENTITY_UNRESOLVED",
        "sanfenge_provider_page": {
            "url": "https://www.sanfenge.com/col.jsp?id=112&m485pageno=2",
            "http_status": 200,
            "content_encoding": "gzip",
            "raw_bytes": 97735,
            "raw_sha256": "670bd6dc088e978afb5cc3665e419b0fcec91fa29809c56c3d51c8213b25487a",
            "decoded_bytes": 1362516,
            "decoded_sha256": "26a0e7e7b52ad1043e8286410e90a974d9b4292f73ce70b06201a9157a71fac6",
            "decode_encoding": "utf-8",
            "direct_provider_records": [
                {
                    "article_id": 212163,
                    "title": "紫薇术紫薇斗数全书卷4.pdf",
                    "article_url": "https://www.sanfenge.com/h-nd-212163.html",
                    "source_label": "网络",
                    "source_emitted_public_share": "https://pan.quark.cn/s/6956a639be12",
                },
                {
                    "article_id": 212173,
                    "title": "紫薇术《紫微斗数全书》四卷.pdf",
                    "article_url": "https://www.sanfenge.com/h-nd-212173.html",
                    "source_label": "网络",
                    "source_emitted_public_share": "https://pan.quark.cn/s/9f7f6a4e7730",
                },
            ],
            "research_run_id": 34312000287,
            "research_job_id": 102340404754,
            "artifact_id": 10088702331,
            "artifact_zip_sha256": "687fac22e4aec5955ad489d68d15755b92a8067863309fa541ec4d778ec9fe4e",
        },
        "quark_public_share_probe": {
            "research_run_id": 34312186561,
            "research_job_id": 102340947244,
            "artifact_id": 10088756117,
            "artifact_zip_sha256": "0746e94fd6bf55312d6609ed5f56dd928469533172a6c6c7902064e77651f082",
            "volume4_share": {
                "url": "https://pan.quark.cn/s/6956a639be12",
                "http_status": 200,
                "raw_bytes": 1358,
                "decoded_bytes": 2732,
                "expected_filename_observed_on_initial_html": False,
                "direct_pdf_bytes_observed": False,
            },
            "four_volume_share": {
                "url": "https://pan.quark.cn/s/9f7f6a4e7730",
                "http_status": 200,
                "raw_bytes": 1358,
                "decoded_bytes": 2732,
                "expected_filename_observed_on_initial_html": False,
                "direct_pdf_bytes_observed": False,
            },
            "public_surface_adjudication": "HTTP_200_QUARK_SHARE_SPA_SHELL_ONLY; FILE_LIST_CONTENT_NOT_PRESENT_IN_INITIAL_HTML; NO_LOGIN_CLOUD_SAVE_HIDDEN_API_GUESSING_OR_BYPASS_ATTEMPTED",
        },
        "adjudication": {
            "provider_filename_article_share_binding": "DIRECT_PROVIDER_SOURCE_CLOSED",
            "file_bytes_obtained": False,
            "internal_title_page_observed": False,
            "edition_or_imprint_identity": "UNRESOLVED",
            "late_zi_target_page_observed": False,
            "independent_textual_witness_increment": 0,
            "independent_hai_glyph_witness_increment": 0,
            "candidate_created": False,
            "candidate_selected": False,
            "algorithm_reopen_authorized": False,
            "algorithm_effect": "NONE",
            "next_gate": "DIRECTLY_READABLE_TARGET_LEAF_FROM_A_PHYSICALLY_BOUND_FULLBOOK_EDITION_WITH_KNOWN_EDITION_OR_IMPRINT",
        },
        "safety": {
            "authentication_attempted": False,
            "cloud_save_attempted": False,
            "purchase_attempted": False,
            "identifier_guessing_attempted": False,
            "hidden_api_guessing_attempted": False,
            "access_control_bypass_attempted": False,
        },
    }
    dump(ROOT / EVIDENCE_PATH, evidence)

    batch = """# Fusion Chart Historical Provenance Audit R1 — Batch 12AD

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
"""
    (ROOT / BATCH_DOC).write_text(batch, encoding="utf-8")

    state_path = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["schema_version"] = "1.41.0"
    audit = state["historical_audit"]
    if BATCH_ID not in audit["completed_batches"]:
        audit["completed_batches"].append(BATCH_ID)
    audit["latest_batch_doc"] = BATCH_DOC
    additions = [
        "Batch 12AD gzip-aware direct provider parsing binds Sanfenge article 212163 exactly to 紫薇术紫薇斗数全书卷4.pdf and source-emitted Quark share 6956a639be12; article 212173 binds 紫薇术《紫微斗数全书》四卷.pdf to share 9f7f6a4e7730.",
        "The exact Quark public-share URLs both return HTTP 200 initial SPA shells, but the expected filenames and PDF bytes are not present in the initial HTML. This is an access-surface boundary, not file-absence evidence; no login, cloud-save, hidden-API guessing or bypass occurred.",
        "The generic Fullbook filenames do not establish an edition, imprint or stemmatic lineage and MUST NOT be normalized to Nanyangtang, Dunhuatang, Jishutang, Jingshutang, Jingluntang, Wenchengtang or any other physical witness without internal title/imprint evidence.",
        "HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; Batch 12AD adds zero textual/Hai-glyph votes, changes no 198/166/10/14 accounting and authorizes no candidate creation/selection/collapse or algorithm reopen. Next gate remains a directly readable target leaf from a physically bound Fullbook edition.",
    ]
    for item in additions:
        if item not in audit["current_focus"]:
            audit["current_focus"].append(item)
    dump(state_path, state)

    matrix_path = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    row = next(r for r in matrix["rows"] if r.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12ad_sanfenge_quark_artifact"] = EVIDENCE_PATH
    row["sanfenge_volume4_article_id"] = 212163
    row["sanfenge_volume4_provider_title"] = "紫薇术紫薇斗数全书卷4.pdf"
    row["sanfenge_volume4_public_share"] = "https://pan.quark.cn/s/6956a639be12"
    row["sanfenge_four_volume_article_id"] = 212173
    row["sanfenge_four_volume_public_share"] = "https://pan.quark.cn/s/9f7f6a4e7730"
    row["sanfenge_provider_binding_status"] = "DIRECT_PROVIDER_FILENAME_ARTICLE_AND_SHARE_URL_BOUND"
    row["sanfenge_quark_public_surface_status"] = "HTTP_200_INITIAL_SPA_SHELL_NO_FILENAME_OR_PDF_BYTES_OBSERVED"
    row["sanfenge_edition_identity"] = "UNRESOLVED_DO_NOT_INFER_FROM_FILENAME"
    row["independent_hai_glyph_witness_count_added_batch_12ad"] = 0
    later = "Batch 12AD: Sanfenge provider source directly binds article 212163 / 紫薇术紫薇斗数全书卷4.pdf to Quark share 6956a639be12 and article 212173 / 紫薇术《紫微斗数全书》四卷.pdf to share 9f7f6a4e7730. Quark initial public HTML exposes only the SPA shell, not file bytes or edition identity; zero textual/Hai votes."
    if later not in row.get("later_witnesses", []):
        row.setdefault("later_witnesses", []).append(later)
    dump(matrix_path, matrix)

    registry_path = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if not any(s.get("source_id") == SOURCE_ID for s in registry["sources"]):
        registry["sources"].append({
            "source_id": SOURCE_ID,
            "title": "Sanfenge provider records for Fullbook volume-four/four-volume PDF shares",
            "historical_period": "MODERN DIGITAL RESOURCE INDEX FOR UNRESOLVED HISTORICAL FULLBOOK FILES",
            "provider": "Sanfenge / public Quark share routes",
            "url": "https://www.sanfenge.com/col.jsp?id=112&m485pageno=2",
            "source_role": "SECONDARY_PROVIDER_INDEX_AND_PUBLIC_SHARE_ACQUISITION_ROUTE_NOT_HISTORICAL_TEXT_AUTHORITY",
            "quality_notes": "Provider HTML directly binds article 212163 to 紫薇术紫薇斗数全书卷4.pdf and Quark share 6956a639be12, and article 212173 to 紫薇术《紫微斗数全书》四卷.pdf and share 9f7f6a4e7730. Initial Quark share HTML returns a generic SPA shell without filename/PDF bytes. Edition, imprint, target leaf and text remain unobserved; zero textual/Hai-glyph votes.",
            "article_ids": [212163, 212173],
            "public_share_urls": ["https://pan.quark.cn/s/6956a639be12", "https://pan.quark.cn/s/9f7f6a4e7730"],
            "direct_file_bytes_observed": False,
            "direct_target_page_observed": False,
            "independent_witness_increment": 0,
            "research_artifact": EVIDENCE_PATH,
        })
    dump(registry_path, registry)

    matrix_md_path = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md"
    matrix_md = matrix_md_path.read_text(encoding="utf-8")
    marker = "### Batch 12AD — Sanfenge/Quark Fullbook volume-four public-share route"
    if marker not in matrix_md:
        matrix_md += "\n\n" + marker + "\n\n- Sanfenge provider HTML directly binds `212163` → `紫薇术紫薇斗数全书卷4.pdf` → Quark `6956a639be12`, and `212173` → `紫薇术《紫微斗数全书》四卷.pdf` → Quark `9f7f6a4e7730`.\n- Both exact public Quark share URLs return HTTP 200 initial SPA shells, but no filename or PDF bytes are present in that initial HTML. This is an access boundary, not content absence.\n- Edition/imprint identity and the target late-Zi leaf remain unobserved; `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`, with zero new textual/Hai votes and no algorithm effect.\n"
        matrix_md_path.write_text(matrix_md, encoding="utf-8")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    summary = f"- **Batch 12AD (Sanfenge/Quark volume-four route):** Sanfenge provider source directly binds article `212163` to `紫薇术紫薇斗数全书卷4.pdf` and Quark share `6956a639be12`, plus article `212173` to the four-volume file and share `9f7f6a4e7730`. Both public Quark URLs return HTTP 200 initial SPA shells but expose no filename/PDF bytes there; edition/imprint and target leaf remain unobserved. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; 198/166/10/14 and all algorithm invariants remain unchanged. See `{BATCH_DOC}`.\n"
    if "Batch 12AD (Sanfenge/Quark volume-four route)" not in readme:
        readme_path.write_text(readme + "\n" + summary, encoding="utf-8")

    verifier_path = ROOT / "scripts/verify-project-continuity-state-r1.py"
    verifier = verifier_path.read_text(encoding="utf-8")
    anchor = 'ZIWEI_WENGUANG_PT165_RESPONSE_EVIDENCE = ROOT / "docs/research/ZIWEI-WENGUANG-PT165-PUBLIC-VIEWER-RESPONSE-CLOSURE-R1.json"\n'
    if "ZIWEI_SANFENGE_QUARK_BATCH" not in verifier:
        if anchor not in verifier:
            raise SystemExit("continuity constant anchor missing")
        verifier = verifier.replace(anchor, anchor + f'ZIWEI_SANFENGE_QUARK_BATCH = ROOT / "{BATCH_DOC}"\nZIWEI_SANFENGE_QUARK_EVIDENCE = ROOT / "{EVIDENCE_PATH}"\n', 1)

    batch_line = '    "BATCH-12-ZIWEI-WENGUANG-PT165-PUBLIC-VIEWER-RESPONSE-CLOSURE-AC",\n'
    if f'"{BATCH_ID}"' not in verifier:
        if batch_line not in verifier:
            raise SystemExit("continuity batch-list anchor missing")
        verifier = verifier.replace(batch_line, batch_line + f'    "{BATCH_ID}",\n', 1)

    old_latest = 'LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENGUANG-PT165-PUBLIC-VIEWER-RESPONSE-CLOSURE-AC.md"'
    verifier = verifier.replace(old_latest, f'LATEST_BATCH_DOC = "{BATCH_DOC}"', 1)

    load_anchor = '    ziwei_wenguang_pt165_response_evidence = json.loads(ZIWEI_WENGUANG_PT165_RESPONSE_EVIDENCE.read_text(encoding="utf-8"))\n'
    if "ziwei_sanfenge_quark_evidence =" not in verifier:
        if load_anchor not in verifier:
            raise SystemExit("continuity evidence-load anchor missing")
        verifier = verifier.replace(load_anchor, load_anchor + '    ziwei_sanfenge_quark_evidence = json.loads(ZIWEI_SANFENGE_QUARK_EVIDENCE.read_text(encoding="utf-8"))\n', 1)

    source_anchor = '        "EXT-KOREA-NLK-CNTS-00047996572-ZIWEIDOUSHUFANGSHU",\n'
    if f'"{SOURCE_ID}"' not in verifier:
        if source_anchor not in verifier:
            raise SystemExit("continuity source anchor missing")
        verifier = verifier.replace(source_anchor, source_anchor + f'        "{SOURCE_ID}",\n', 1)

    check_anchor = '    invariants = state.get("invariants", {})\n'
    if "Batch 12AD Sanfenge provider/share route" not in verifier:
        if check_anchor not in verifier:
            raise SystemExit("continuity check anchor missing")
        check = f'''    # Batch 12AD Sanfenge provider/share route: locator closure only, zero textual votes.\n    if not ZIWEI_SANFENGE_QUARK_BATCH.is_file() or not ZIWEI_SANFENGE_QUARK_EVIDENCE.is_file():\n        fail("Batch 12AD continuity artifacts missing")\n    if ziwei_sanfenge_quark_evidence.get("batch_id") != "{BATCH_ID}":\n        fail("Batch 12AD evidence identity mismatch")\n    p12ad = ziwei_sanfenge_quark_evidence.get("sanfenge_provider_page", {{}})\n    records12ad = {{r.get("article_id"): r for r in p12ad.get("direct_provider_records", ())}}\n    if records12ad.get(212163, {{}}).get("source_emitted_public_share") != "https://pan.quark.cn/s/6956a639be12":\n        fail("Batch 12AD volume-four provider/share binding regressed")\n    if records12ad.get(212173, {{}}).get("source_emitted_public_share") != "https://pan.quark.cn/s/9f7f6a4e7730":\n        fail("Batch 12AD four-volume provider/share binding regressed")\n    q12ad = ziwei_sanfenge_quark_evidence.get("quark_public_share_probe", {{}})\n    if q12ad.get("volume4_share", {{}}).get("direct_pdf_bytes_observed") is not False:\n        fail("Batch 12AD public-share byte boundary regressed")\n    a12ad = ziwei_sanfenge_quark_evidence.get("adjudication", {{}})\n    if a12ad.get("independent_textual_witness_increment") != 0 or a12ad.get("independent_hai_glyph_witness_increment") != 0 or a12ad.get("algorithm_reopen_authorized") is not False:\n        fail("Batch 12AD witness/algorithm firewall regressed")\n    row12ad = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)\n    if not row12ad or row12ad.get("sanfenge_volume4_article_id") != 212163 or row12ad.get("independent_hai_glyph_witness_count_added_batch_12ad") != 0:\n        fail("Batch 12AD Matrix binding regressed")\n\n'''
        verifier = verifier.replace(check_anchor, check + check_anchor, 1)

    verifier_path.write_text(verifier, encoding="utf-8")
    print(BATCH_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
