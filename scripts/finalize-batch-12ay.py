#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH_ID = "BATCH-12-ZIWEI-ZHANGGUO-JANGSEOGAK-1594-PUBLIC-ACCESS-BOUNDARY-AY"
BATCH_DOC_REL = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-JANGSEOGAK-1594-PUBLIC-ACCESS-BOUNDARY-AY.md"
EVIDENCE_REL = "docs/research/ZIWEI-ZHANGGUO-JANGSEOGAK-PUBLIC-ACCESS-BOUNDARY-R1.json"

BATCH_DOC = r'''# Fusion Chart Historical Provenance Audit R1 — Batch 12AY

## 《张果星宗大全》藏书阁万历二十二年本公开访问边界审计

Status: **JANGSEOGAK 1594 HOLDING CATALOG IDENTITY CONFIRMED / SECOND UNDATED HOLDING CONFIRMED / ADJACENT MF-PDF CONTROL VERIFIED / 15 OBJECT-SPECIFIC TARGET PDF ROUTES RETURN 404 HTML / TARGET LEAF NOT OBTAINED / ACCESS FAILURE IS NOT TEXTUAL ABSENCE / ZERO TEXT OR HAI-GLYPH VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Why this batch exists

Batch 12AW established a direct 1594 physical witness for the Zhangguo passage and Batch 12AX showed that a later Hirayama recension differs at the reviewed boundary. The highest-value next question was therefore whether an independent 1594 holding could provide a second physical target-leaf collation.

Jangseogak exposes two catalog records for 《新編評註通玄先生張果星宗大全》. AY binds those holdings and then tests the public image/MF-PDF topology without converting an access failure into a textual negative.

## 2. Jangseogak holdings

### 2.1 Dated 1594 holding

```text
data_id=LIB_169178
display_call_number=PC9A-20
detail_call_number=C9A-20
mf_number=MF16/1453-1454
title=新編評註通玄先生張果星宗大全
catalog_date=萬曆22(1594)
edition_type=中國木板本
extent=10卷10冊:圖, 四周雙邊, 上黑魚尾;25.7 × 15.5cm
```

Official public record:

```text
https://jsg.aks.ac.kr/dir/view?dataId=LIB_169178
```

The public directory exposes bibliography / electronic-library / XML linkage, but no image link and no MF-PDF link for this object.

### 2.2 Second undated holding

```text
data_id=LIB_169177
display_call_number=PC9A-20A
detail_call_number=C9A-20A
mf_number=MF35/8437
title=新編評註通玄先生張果星宗大全
catalog_date=[刊年未詳]
edition_type=中國木板本
extent=10卷5冊:圖, 四周雙邊, 上黑魚尾;25.3 × 15.4cm
```

Official public record:

```text
https://jsg.aks.ac.kr/dir/view?dataId=LIB_169177
```

This holding is a separate access/recension control. Its unresolved catalog date must not be promoted to 1594 or to an early witness by inference.

## 3. Public-route positive control

The same Jangseogak directory visibly distinguishes items with digitized/MF-PDF access. Adjacent record `PC9A-23 / LIB_169174`, 《紫微斗數補遺》, exposes an MF-PDF link whose first book is a real public PDF:

```text
https://jsg.aks.ac.kr/data/serviceFiles/pdf/PC9A-23_001.pdf
```

This proves that the route pattern

```text
/data/serviceFiles/pdf/{display_call_number}_{book}.pdf
```

is genuine for at least a Jangseogak object that advertises MF-PDF access. It does **not** prove that every Jangseogak holding is digitized or publicly downloadable.

## 4. Object-specific target probe

GitHub Actions run and artifact:

```text
workflow_run_id=34593669934
artifact_id=10260891530
artifact_digest=sha256:10d7ee063b017464143f05dc9740903b40090ce65d782b1576c81fa9675b27fc
```

Routes tested:

```text
PC9A-20_001.pdf ... PC9A-20_010.pdf
PC9A-20A_001.pdf ... PC9A-20A_005.pdf
```

All 15 responses were:

```text
HTTP 404
Content-Type: text/html
response_bytes=1259
prefix_hex=3c21444f43545950  # <!DOCTYP
PDF magic=false
```

No live target PDF route and no rendered target book were obtained.

## 5. Scope discipline

The result authorizes only the following statement:

```text
THE_REVIEWED_PUBLIC_JANGSEOGAK_IMAGE_MF_PDF_ROUTE_DOES_NOT_EXPOSE_THE_TARGET_BOOK_BYTES
```

It does **not** authorize any of these statements:

```text
TARGET_PASSAGE_ABSENT=false_to_claim
WHOLE_HOLDING_NEGATIVE=false_to_claim
NO_INTERNAL_DIGITIZATION=false_to_claim
NO_REPRODUCTION_POSSIBLE=false_to_claim
```

Catalog identity and access topology are evidence; failure to retrieve target bytes is not text criticism.

## 6. Philological and witness accounting

Because no target leaf was obtained, AY performs no glyph adjudication and supplies no same-edition stability vote.

```text
PUBLIC_TARGET_LEAF_OBTAINED=false
DIRECT_GLYPH_COLLATION_AUTHORIZED=false
WHOLE_HOLDING_TEXT_NEGATIVE_AUTHORIZED=false
SAME_EDITION_TEXT_STABILITY_VOTE_INCREMENT=0
INDEPENDENT_TARGET_TEXT_WITNESS_INCREMENT=0
INDEPENDENT_HAI_GLYPH_WITNESS_INCREMENT=0
```

The 1594 AW physical leaf remains the controlling positive witness for its own wording. AY neither strengthens nor weakens the missing mechanical bridge `upper/night Zi -> Hai branch`.

## 7. Effect on HPA-ZDATE-006

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
NEW_CANDIDATE_FAMILY=false
RUNTIME_WINNER_SELECTED=false
CANDIDATE_COLLAPSED=false
ALGORITHM_REOPEN=false
```

No current runtime behavior changes are authorized.

## 8. Accounting

```text
ROW_COUNT=198
AUDITED_ROW_COUNT=166
MISSING_FROM_PRODUCT=10
IDENTIFIED_MISSING_CANDIDATE_FAMILIES=14
CONFIRMED_PROVENANCE_DEFECTS=11
REPAIRED_PROVENANCE_DEFECTS=11
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
```

No Historical Audit Matrix count changes are authorized.

## 9. External-action boundary

Jangseogak's public pages expose an institutional image-use/contact route. Requesting target-page imaging or reproduction is an external institutional action.

```text
REQUEST_SUBMITTED=false
USER_AUTHORIZATION_REQUIRED=true
```

No request is submitted in this batch. A future request may be made only with explicit user authorization and whatever request identity/contact data the institution requires.

## 10. Durable artifact

```text
docs/research/ZIWEI-ZHANGGUO-JANGSEOGAK-PUBLIC-ACCESS-BOUNDARY-R1.json
```

## 11. Next gate

1. Seek another publicly readable 1594, same-edition, or clearly near-edition physical witness and directly collate the target leaf.
2. Keep the Jangseogak institutional request route available but dormant until explicit authorization.
3. Continue searching for an independent historical witness that explicitly supplies the missing `upper/night Zi -> Hai branch` bridge; do not infer it from day-stem/day-date ownership language alone.
'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def append_registry_sources(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    existing = {s.get("source_id") for s in data.get("sources", [])}
    sources = [
        {
            "source_id": "EXT-ZIWEI-ZHANGGUO-JANGSEOGAK-1594",
            "title": "《新編評註通玄先生張果星宗大全》",
            "historical_period": "明",
            "edition": "中國木板本 / 萬曆22(1594) / 10卷10冊",
            "provider": "Jangseogak Archives, Academy of Korean Studies",
            "url": "https://jsg.aks.ac.kr/dir/view?dataId=LIB_169178",
            "source_role": "INDEPENDENT_INSTITUTIONAL_1594_HOLDING_ACCESS_CONTROL_TARGET_LEAF_NOT_OBTAINED",
            "display_call_number": "PC9A-20",
            "detail_call_number": "C9A-20",
            "mf_number": "MF16/1453-1454",
            "public_image_link_exposed": False,
            "public_mf_pdf_link_exposed": False,
            "target_leaf_obtained": False,
            "whole_holding_text_negative_authorized": False,
            "independent_target_text_witness_increment": 0,
            "independent_hai_glyph_witness_increment": 0,
            "batch_id": BATCH_ID,
            "research_artifact": EVIDENCE_REL,
            "quality_notes": "Catalog identity is directly bound at the official Jangseogak record. Object-specific public PDF-pattern probes returned 404 HTML for all tested books; this is an access boundary only, not target-text absence and not a glyph vote."
        },
        {
            "source_id": "EXT-ZIWEI-ZHANGGUO-JANGSEOGAK-UNDATED-20A",
            "title": "《新編評註通玄先生張果星宗大全》",
            "historical_period": "刊年未詳",
            "edition": "中國木板本 / [刊年未詳] / 10卷5冊",
            "provider": "Jangseogak Archives, Academy of Korean Studies",
            "url": "https://jsg.aks.ac.kr/dir/view?dataId=LIB_169177",
            "source_role": "UNDATED_RECENSION_HOLDING_ACCESS_CONTROL_TARGET_LEAF_NOT_OBTAINED",
            "display_call_number": "PC9A-20A",
            "detail_call_number": "C9A-20A",
            "mf_number": "MF35/8437",
            "public_image_link_exposed": False,
            "public_mf_pdf_link_exposed": False,
            "target_leaf_obtained": False,
            "whole_holding_text_negative_authorized": False,
            "independent_target_text_witness_increment": 0,
            "independent_hai_glyph_witness_increment": 0,
            "batch_id": BATCH_ID,
            "research_artifact": EVIDENCE_REL,
            "quality_notes": "Official catalog identity is confirmed but the date remains unresolved. Do not promote this holding to 1594/early-witness status. The reviewed public route exposes no target bytes and adds zero textual/glyph votes."
        },
    ]
    missing = [s for s in sources if s["source_id"] not in existing]
    if not missing:
        return
    tail = "\n  ]\n}\n"
    if not text.endswith(tail):
        raise SystemExit("source registry tail shape changed")
    rendered = []
    for src in missing:
        block = json.dumps(src, ensure_ascii=False, indent=2)
        rendered.append("\n".join("    " + line for line in block.splitlines()))
    text = text[:-len(tail)] + ",\n" + ",\n".join(rendered) + tail
    json.loads(text)
    path.write_text(text, encoding="utf-8")


def update_state(path: Path) -> None:
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("schema_version") not in {"1.57.0", "1.58.0"}:
        raise SystemExit(f"unexpected state schema version: {state.get('schema_version')}")
    state["schema_version"] = "1.58.0"
    audit = state["historical_audit"]
    if BATCH_ID not in audit["completed_batches"]:
        if audit["completed_batches"][-1] != "BATCH-12-ZIWEI-ZHANGGUO-HIRAYAMA-GUANGXU7-RECENSION-COLLATION-AX":
            raise SystemExit("unexpected prior completed batch tail")
        audit["completed_batches"].append(BATCH_ID)
    audit["latest_batch_doc"] = BATCH_DOC_REL
    additions = [
        "Batch 12AY directly binds Jangseogak LIB_169178 / PC9A-20 / C9A-20 / MF16/1453-1454 as a 中國木板本 10卷10冊 cataloged 萬曆22(1594) holding of 新編評註通玄先生張果星宗大全; LIB_169177 / PC9A-20A / C9A-20A / MF35/8437 is separately bound as a 10卷5冊 [刊年未詳] holding and must not be promoted to 1594 by inference.",
        "Jangseogak adjacent control PC9A-23 / LIB_169174 exposes a real serviceFiles/pdf MF-PDF route, but the two Zhangguo directory records expose no image/MF-PDF link. Workflow 34593669934 / artifact 10260891530 tested PC9A-20 books 1-10 and PC9A-20A books 1-5; all 15 routes returned HTTP 404 text/html with no PDF magic.",
        "Batch 12AY is therefore an object-specific public access boundary only: no target leaf bytes were obtained, no whole-holding textual negative is authorized, and no same-edition text-stability, target-text or Hai-glyph vote is added. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with no runtime winner, candidate collapse or algorithm reopen.",
        "A formal Jangseogak image/reproduction request remains an explicit external-action boundary requiring user authorization and any required identity/contact details; no request has been submitted. Next high-value gate is another publicly readable 1594/same-edition/near-edition physical target leaf or an independent historical witness explicitly supplying the missing upper/night-Zi -> Hai mechanical bridge."
    ]
    focus = audit["current_focus"]
    for item in additions:
        if item not in focus:
            focus.append(item)
    inv = state["invariants"]
    if inv.get("confirmed_chart_algorithm_defect_count") != 0 or inv.get("algorithm_reopen_count") != 0 or inv.get("candidate_collapse_count") != 0:
        raise SystemExit("algorithm invariants changed unexpectedly")
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_verifier(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "ZIWEI_ZHANGGUO_AY_EVIDENCE" in text:
        return

    text = replace_once(
        text,
        'ZIWEI_ZHANGGUO_AX_EVIDENCE = ROOT / "docs/research/ZIWEI-ZHANGGUO-HIRAYAMA-GUANGXU7-RECENSION-COLLATION-R1.json"\n',
        'ZIWEI_ZHANGGUO_AX_EVIDENCE = ROOT / "docs/research/ZIWEI-ZHANGGUO-HIRAYAMA-GUANGXU7-RECENSION-COLLATION-R1.json"\n'
        'ZIWEI_ZHANGGUO_AY_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-JANGSEOGAK-1594-PUBLIC-ACCESS-BOUNDARY-AY.md"\n'
        'ZIWEI_ZHANGGUO_AY_EVIDENCE = ROOT / "docs/research/ZIWEI-ZHANGGUO-JANGSEOGAK-PUBLIC-ACCESS-BOUNDARY-R1.json"\n',
        "AY constants",
    )
    text = replace_once(
        text,
        '    "BATCH-12-ZIWEI-ZHANGGUO-HIRAYAMA-GUANGXU7-RECENSION-COLLATION-AX",\n]\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\nLATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-HIRAYAMA-GUANGXU7-RECENSION-COLLATION-AX.md"\n',
        '    "BATCH-12-ZIWEI-ZHANGGUO-HIRAYAMA-GUANGXU7-RECENSION-COLLATION-AX",\n'
        f'    "{BATCH_ID}",\n'
        ']\nLATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]\n'
        f'LATEST_BATCH_DOC = "{BATCH_DOC_REL}"\n',
        "AY supplemental batch ledger",
    )
    text = replace_once(
        text,
        'def main() -> int:\n    for path in (ZIWEI_ZHANGGUO_AX_BATCH, ZIWEI_ZHANGGUO_AX_EVIDENCE):\n',
        'def main() -> int:\n    for path in (ZIWEI_ZHANGGUO_AY_BATCH, ZIWEI_ZHANGGUO_AY_EVIDENCE):\n'
        '        if not path.is_file():\n'
        '            fail(f"Batch 12AY continuity artifact missing: {path.relative_to(ROOT)}")\n\n'
        '    for path in (ZIWEI_ZHANGGUO_AX_BATCH, ZIWEI_ZHANGGUO_AX_EVIDENCE):\n',
        "AY artifact existence",
    )
    text = replace_once(
        text,
        '    ziwei_zhangguo_ax_evidence = json.loads(ZIWEI_ZHANGGUO_AX_EVIDENCE.read_text(encoding="utf-8"))\n',
        '    ziwei_zhangguo_ax_evidence = json.loads(ZIWEI_ZHANGGUO_AX_EVIDENCE.read_text(encoding="utf-8"))\n'
        '    ziwei_zhangguo_ay_evidence = json.loads(ZIWEI_ZHANGGUO_AY_EVIDENCE.read_text(encoding="utf-8"))\n',
        "AY evidence load",
    )

    anchor = '''    if not src_registry12ax or src_registry12ax.get("whole_volume_negative_authorized") is not False:\n        fail("Batch 12AX registry scope firewall regressed")\n\n'''
    block = anchor + '''    # Batch 12AY Jangseogak 1594 public-access boundary.\n    if ziwei_zhangguo_ay_evidence.get("batch_id") != "BATCH-12-ZIWEI-ZHANGGUO-JANGSEOGAK-1594-PUBLIC-ACCESS-BOUNDARY-AY":\n        fail("Batch 12AY evidence identity mismatch")\n    holdings12ay = {h.get("source_id"): h for h in ziwei_zhangguo_ay_evidence.get("holdings", ())}\n    dated12ay = holdings12ay.get("EXT-ZIWEI-ZHANGGUO-JANGSEOGAK-1594", {})\n    undated12ay = holdings12ay.get("EXT-ZIWEI-ZHANGGUO-JANGSEOGAK-UNDATED-20A", {})\n    if dated12ay.get("data_id") != "LIB_169178" or dated12ay.get("display_call_number") != "PC9A-20" or dated12ay.get("catalog_date") != "萬曆22(1594)":\n        fail("Batch 12AY dated Jangseogak holding binding regressed")\n    if undated12ay.get("data_id") != "LIB_169177" or undated12ay.get("display_call_number") != "PC9A-20A" or undated12ay.get("catalog_date") != "[刊年未詳]":\n        fail("Batch 12AY undated Jangseogak holding scope regressed")\n    route12ay = ziwei_zhangguo_ay_evidence.get("object_specific_route_probe", {})\n    if route12ay.get("workflow_run_id") != 34593669934 or route12ay.get("artifact_id") != 10260891530:\n        fail("Batch 12AY route-probe provenance regressed")\n    if route12ay.get("result") != "ALL_TESTED_ROUTES_HTTP_404_TEXT_HTML_NO_PDF_MAGIC" or route12ay.get("live_pdf_routes") != [] or route12ay.get("rendered_target_books") != []:\n        fail("Batch 12AY public-route boundary regressed")\n    adjudication12ay = ziwei_zhangguo_ay_evidence.get("adjudication", {})\n    if adjudication12ay.get("public_target_leaf_obtained") is not False or adjudication12ay.get("direct_glyph_collation_authorized") is not False or adjudication12ay.get("whole_holding_text_negative_authorized") is not False:\n        fail("Batch 12AY access-vs-text firewall regressed")\n    if adjudication12ay.get("same_edition_text_stability_vote_increment") != 0 or adjudication12ay.get("independent_target_text_witness_increment") != 0 or adjudication12ay.get("independent_hai_glyph_witness_increment") != 0:\n        fail("Batch 12AY witness accounting regressed")\n    effect12ay = ziwei_zhangguo_ay_evidence.get("project_consequence", {})\n    if effect12ay.get("audit_status") != "MISSING_FROM_PRODUCT" or effect12ay.get("new_candidate_family") is not False or effect12ay.get("runtime_winner_selected") is not False or effect12ay.get("candidate_collapsed") is not False or effect12ay.get("algorithm_reopen") is not False:\n        fail("Batch 12AY HPA/algorithm firewall regressed")\n    ext12ay = ziwei_zhangguo_ay_evidence.get("external_action_boundary", {})\n    if ext12ay.get("request_submitted") is not False or ext12ay.get("authorization_required_before_submission") is not True:\n        fail("Batch 12AY institutional-request authorization boundary regressed")\n    registry12ay = {s.get("source_id"): s for s in registry.get("sources", ())}\n    for source_id in ("EXT-ZIWEI-ZHANGGUO-JANGSEOGAK-1594", "EXT-ZIWEI-ZHANGGUO-JANGSEOGAK-UNDATED-20A"):\n        source = registry12ay.get(source_id)\n        if not source or source.get("target_leaf_obtained") is not False or source.get("whole_holding_text_negative_authorized") is not False:\n            fail(f"Batch 12AY registry scope firewall regressed for {source_id}")\n        if source.get("independent_target_text_witness_increment") != 0 or source.get("independent_hai_glyph_witness_increment") != 0:\n            fail(f"Batch 12AY registry vote accounting regressed for {source_id}")\n\n'''
    text = replace_once(text, anchor, block, "AY semantic firewall")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    evidence = ROOT / EVIDENCE_REL
    if not evidence.is_file():
        raise SystemExit(f"missing AY evidence: {EVIDENCE_REL}")
    evidence_data = json.loads(evidence.read_text(encoding="utf-8"))
    if evidence_data.get("batch_id") != BATCH_ID:
        raise SystemExit("AY evidence batch identity mismatch")

    batch_doc = ROOT / BATCH_DOC_REL
    batch_doc.write_text(BATCH_DOC, encoding="utf-8")
    append_registry_sources(ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
    update_state(ROOT / "docs/PROJECT-CURRENT-STATE-R1.json")
    update_verifier(ROOT / "scripts/verify-project-continuity-state-r1.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
