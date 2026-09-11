#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH_ID = "BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-AZ"
BATCH_DOC_REL = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-AZ.md"
EVIDENCE_REL = "docs/research/ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-R1.json"
SOURCE_ID = "EXT-ZIWEI-ZHANGGUO-WEIFANG-1594-LOCATOR"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def update_registry() -> None:
    path = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    existing = {s.get("source_id") for s in data.get("sources", [])}
    if SOURCE_ID not in existing:
        data["sources"].append({
            "source_id": SOURCE_ID,
            "title": "《新編評註通玄先生張果星宗大全》十卷（濰坊市圖書館／山東古籍平台線索）",
            "historical_period": "LOCATOR CLAIMS 明萬曆二十二年(1594); FIRST-PARTY SHANDONG OBJECT NOT YET BOUND",
            "edition": "multi-index locator claim: 明萬曆二十二年(1594)唐謙刻本",
            "provider": "Shandong Ancient Books / Weifang Library locator ecosystem; first-party object response unavailable in reviewed runners",
            "url": "https://guji.sdlib.com/front/#/bookInfo?resId=151613020240003",
            "source_role": "SECONDARY_MULTI_INDEX_LOCATOR_PENDING_FIRST_PARTY_SHANDONG_OBJECT_BINDING",
            "resource_id": "151613020240003",
            "holding_claim": "濰坊市圖書館藏",
            "extent_claim": "十卷",
            "official_catalog_metadata_directly_bound": False,
            "official_shandong_object_bytes_obtained": False,
            "target_leaf_obtained": False,
            "direct_glyph_authority": False,
            "whole_holding_text_negative_authorized": False,
            "resource_gone_claim_authorized": False,
            "independent_target_text_witness_increment": 0,
            "independent_hai_glyph_witness_increment": 0,
            "batch_id": BATCH_ID,
            "research_artifact": EVIDENCE_REL,
            "quality_notes": "High-value 1594 locator only. Initial Linux acquisition and a Linux/macOS/Windows cross-egress probe all timed out on reviewed Shandong official/API/front and old object-host routes. No first-party bytes were obtained; reachability failure is not bibliographic/textual absence and supplies zero glyph votes."
        })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_state() -> None:
    path = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("schema_version") not in {"1.58.0", "1.59.0"}:
        raise SystemExit(f"unexpected state schema version: {state.get('schema_version')}")
    state["schema_version"] = "1.59.0"
    audit = state["historical_audit"]
    if BATCH_ID not in audit["completed_batches"]:
        if audit["completed_batches"][-1] != "BATCH-12-ZIWEI-ZHANGGUO-JANGSEOGAK-1594-PUBLIC-ACCESS-BOUNDARY-AY":
            raise SystemExit("unexpected completed batch tail before AZ")
        audit["completed_batches"].append(BATCH_ID)
    audit["latest_batch_doc"] = BATCH_DOC_REL
    additions = [
        "Batch 12AZ retains Shandong/Weifang resource 151613020240003 as a high-value locator for 新編評註通玄先生張果星宗大全 十卷, described by convergent discovery surfaces as 濰坊市圖書館藏 / 明萬曆二十二年(1594)唐謙刻本; because no first-party Shandong catalog/API response was obtained, the edition/holding claim remains locator-scoped and is not promoted to direct physical-witness authority.",
        "AZ initial run 34596426615 / artifact 10262594953 obtained no official API response or PDF bytes. Cross-egress run 34597728895 repeated the official API/front and one old object-host sample on Linux westus3, macOS westus and Windows eastus; every reviewed route timed out, with artifacts 10263155974 / 10263650215 / 10263550354 respectively.",
        "The AZ result is an execution-environment/public-route reachability boundary only: official Shandong object bytes and target leaf remain unobtained; no whole-holding negative, no resource-gone/no-digitization inference and no text/Hai-glyph vote are authorized. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with no runtime winner, candidate collapse or algorithm reopen.",
        "Next high-value gate is a reachable first-party binding for Weifang resource 151613020240003 followed by no-OCR target-leaf collation; parallel early-copy research may pursue the SOAS/NCL union-catalog lead while strictly separating genuine early copies from later reprints."
    ]
    focus = audit["current_focus"]
    for item in additions:
        if item not in focus:
            focus.append(item)
    inv = state["invariants"]
    if inv.get("confirmed_chart_algorithm_defect_count") != 0 or inv.get("algorithm_reopen_count") != 0 or inv.get("candidate_collapse_count") != 0:
        raise SystemExit("algorithm invariants changed unexpectedly")
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_verifier() -> None:
    path = ROOT / "scripts/verify-project-continuity-state-r1.py"
    text = path.read_text(encoding="utf-8")
    if "ZIWEI_ZHANGGUO_AZ_EVIDENCE" in text:
        return

    text = replace_once(
        text,
        'ZIWEI_ZHANGGUO_AY_EVIDENCE = ROOT / "docs/research/ZIWEI-ZHANGGUO-JANGSEOGAK-PUBLIC-ACCESS-BOUNDARY-R1.json"\n',
        'ZIWEI_ZHANGGUO_AY_EVIDENCE = ROOT / "docs/research/ZIWEI-ZHANGGUO-JANGSEOGAK-PUBLIC-ACCESS-BOUNDARY-R1.json"\n'
        'ZIWEI_ZHANGGUO_AZ_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-AZ.md"\n'
        'ZIWEI_ZHANGGUO_AZ_EVIDENCE = ROOT / "docs/research/ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-R1.json"\n',
        "AZ constants",
    )
    text = replace_once(
        text,
        '    "BATCH-12-ZIWEI-ZHANGGUO-JANGSEOGAK-1594-PUBLIC-ACCESS-BOUNDARY-AY",\n]\nLATEST_BATCH_ID',
        '    "BATCH-12-ZIWEI-ZHANGGUO-JANGSEOGAK-1594-PUBLIC-ACCESS-BOUNDARY-AY",\n'
        '    "BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-AZ",\n]\nLATEST_BATCH_ID',
        "supplemental batch tail",
    )
    text = replace_once(
        text,
        'LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-JANGSEOGAK-1594-PUBLIC-ACCESS-BOUNDARY-AY.md"',
        'LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-AZ.md"',
        "latest batch doc",
    )
    text = replace_once(
        text,
        'def main() -> int:\n    for path in (ZIWEI_ZHANGGUO_AY_BATCH, ZIWEI_ZHANGGUO_AY_EVIDENCE):',
        'def main() -> int:\n    for path in (ZIWEI_ZHANGGUO_AZ_BATCH, ZIWEI_ZHANGGUO_AZ_EVIDENCE):\n'
        '        if not path.is_file():\n'
        '            fail(f"Batch 12AZ continuity artifact missing: {path.relative_to(ROOT)}")\n\n'
        '    for path in (ZIWEI_ZHANGGUO_AY_BATCH, ZIWEI_ZHANGGUO_AY_EVIDENCE):',
        "AZ artifact existence gate",
    )
    text = replace_once(
        text,
        '    ziwei_zhangguo_ay_evidence = json.loads(ZIWEI_ZHANGGUO_AY_EVIDENCE.read_text(encoding="utf-8"))\n',
        '    ziwei_zhangguo_ay_evidence = json.loads(ZIWEI_ZHANGGUO_AY_EVIDENCE.read_text(encoding="utf-8"))\n'
        '    ziwei_zhangguo_az_evidence = json.loads(ZIWEI_ZHANGGUO_AZ_EVIDENCE.read_text(encoding="utf-8"))\n',
        "AZ evidence load",
    )

    anchor = '''    # Provenance/access-only batches can advance without changing any Matrix row.\n'''
    checks = '''    # Batch 12AZ Weifang/Shandong 1594 locator and cross-egress access boundary.\n    if ziwei_zhangguo_az_evidence.get("batch_id") != "BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-AZ":\n        fail("Batch 12AZ evidence identity mismatch")\n    locator12az = ziwei_zhangguo_az_evidence.get("locator_claim", {})\n    if locator12az.get("resource_id") != "151613020240003" or locator12az.get("edition_claim") != "明萬曆二十二年(1594)唐謙刻本" or locator12az.get("holding_claim") != "濰坊市圖書館藏":\n        fail("Batch 12AZ Weifang locator binding regressed")\n    if locator12az.get("official_catalog_metadata_directly_bound") is not False or locator12az.get("physical_copy_identity_directly_bound") is not False:\n        fail("Batch 12AZ locator-to-primary authority firewall regressed")\n    initial12az = ziwei_zhangguo_az_evidence.get("initial_linux_probe", {})\n    if initial12az.get("workflow_run_id") != 34596426615 or initial12az.get("artifact_id") != 10262594953 or initial12az.get("downloaded_pdf_samples") != 0 or initial12az.get("rendered_pages") != 0:\n        fail("Batch 12AZ initial acquisition boundary regressed")\n    egress12az = ziwei_zhangguo_az_evidence.get("cross_egress_probe", {})\n    if egress12az.get("workflow_run_id") != 34597728895 or egress12az.get("routes_tested_per_runner") != 5:\n        fail("Batch 12AZ cross-egress provenance regressed")\n    runners12az = {r.get("os"): r for r in egress12az.get("runners", ())}\n    expected12az = {\n        "Linux": (103257322652, 10263155974),\n        "macOS": (103257322513, 10263650215),\n        "Windows": (103257322572, 10263550354),\n    }\n    for os_name, (job_id, artifact_id) in expected12az.items():\n        runner = runners12az.get(os_name, {})\n        if runner.get("job_id") != job_id or runner.get("artifact_id") != artifact_id or runner.get("all_reviewed_routes_timed_out") is not True:\n            fail(f"Batch 12AZ cross-egress runner binding regressed for {os_name}")\n    adj12az = ziwei_zhangguo_az_evidence.get("adjudication", {})\n    if adj12az.get("official_shandong_object_bytes_obtained") is not False or adj12az.get("target_leaf_obtained") is not False or adj12az.get("direct_glyph_collation_authorized") is not False:\n        fail("Batch 12AZ byte/glyph authority firewall regressed")\n    if adj12az.get("whole_holding_text_negative_authorized") is not False or adj12az.get("no_digitization_claim_authorized") is not False or adj12az.get("resource_gone_claim_authorized") is not False:\n        fail("Batch 12AZ access-vs-absence firewall regressed")\n    if adj12az.get("same_edition_text_stability_vote_increment") != 0 or adj12az.get("independent_target_text_witness_increment") != 0 or adj12az.get("independent_hai_glyph_witness_increment") != 0:\n        fail("Batch 12AZ witness accounting regressed")\n    effect12az = ziwei_zhangguo_az_evidence.get("project_consequence", {})\n    if effect12az.get("audit_status") != "MISSING_FROM_PRODUCT" or effect12az.get("runtime_winner_selected") is not False or effect12az.get("candidate_collapsed") is not False or effect12az.get("algorithm_reopen") is not False:\n        fail("Batch 12AZ HPA/algorithm firewall regressed")\n    src12az = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-ZIWEI-ZHANGGUO-WEIFANG-1594-LOCATOR"), None)\n    if not src12az or src12az.get("source_role") != "SECONDARY_MULTI_INDEX_LOCATOR_PENDING_FIRST_PARTY_SHANDONG_OBJECT_BINDING":\n        fail("Batch 12AZ registry locator authority scope regressed")\n    if src12az.get("official_catalog_metadata_directly_bound") is not False or src12az.get("target_leaf_obtained") is not False or src12az.get("whole_holding_text_negative_authorized") is not False:\n        fail("Batch 12AZ registry access/authority firewall regressed")\n    if src12az.get("independent_target_text_witness_increment") != 0 or src12az.get("independent_hai_glyph_witness_increment") != 0:\n        fail("Batch 12AZ registry witness accounting regressed")\n\n'''
    text = replace_once(text, anchor, checks + anchor, "AZ semantic checks")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    update_registry()
    update_state()
    update_verifier()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
