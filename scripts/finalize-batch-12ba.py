#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH_ID = "BATCH-12-ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-BA"
BATCH_DOC_REL = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-BA.md"
EVIDENCE_REL = "docs/research/ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-R1.json"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def update_registry() -> None:
    path = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    existing = {s.get("source_id") for s in data.get("sources", [])}
    additions = [
        {
            "source_id": "EXT-ZIWEI-ZHANGGUO-NCL-SOAS-MIRR0000375",
            "title": "《新編評註通玄先生張果星宗大全》SOAS holding union-catalog record",
            "provider": "National Central Library, Taiwan - Chinese Rare Books Union Catalog",
            "url": "https://rbook.ncl.edu.tw/NCLSearch/Search/SearchDetail?HasImage=&SourceID=0&item=4d49327ec5a14df4b31deae023849cfafDk3MTI30.WuivSY2RngP1AoCQSj60_woTSo6UZDy90JPEkgtURzU_&page=81174&sourceWhereString=&whereString=IChOVUxMSUYoRGF0ZV9DcmVhdGVkLCAnICcpIGlzIE5VTEwgYW5kIE5VTExJRihEb2N1bWVudF9ZZWFyLCAnICcpIGlzIE5VTEwgKSA1.uQrV5XxqrHh4fOCXMwOuuzssvPVRwJbumFyT4mFEUCA_",
            "source_role": "UNION_CATALOG_METADATA_ROUTE_ORIGINAL_PUBLICATION_DATE_NOT_PHYSICAL_IMPRESSION_AUTHORITY",
            "registration_number": "mirr0000375",
            "catalog_date": "明萬曆癸巳[1593]",
            "critical_date_note": "原刊行年據韋環序",
            "date_semantics": "ORIGINAL_PUBLICATION_YEAR_INFERRED_FROM_PREFACE_NOT_DIRECT_PHYSICAL_IMPRESSION_DATE",
            "holding_institution": "英國倫敦大學亞非學院圖書館",
            "quantity": "1 v.",
            "physical_impression_1593_proven": False,
            "target_leaf_obtained": False,
            "independent_early_physical_witness_increment": 0,
            "independent_target_text_witness_increment": 0,
            "independent_hai_glyph_witness_increment": 0,
            "batch_id": BATCH_ID,
            "research_artifact": EVIDENCE_REL,
            "quality_notes": "Official NCL union-catalog metadata. Its own note says the original publication year is inferred from the Wei Huan preface; the 1593 field therefore cannot be promoted to the impression date of the extant SOAS object."
        },
        {
            "source_id": "EXT-ZIWEI-ZHANGGUO-SOAS-MORRISON-RM65",
            "title": "Morrison manuscript catalogue no.65 《張果老星宗》",
            "provider": "Morrison Collection / Andrew C. West edited transcription of SOAS MS 80823",
            "url": "https://www.babelstone.co.uk/Morrison/Collection/MS80823.html",
            "source_role": "EARLY_COLLECTION_INVENTORY_AND_CURRENT_CALLMARK_BRIDGE_ROUTE_NOT_PRINT_DATE_AUTHORITY",
            "morrison_catalog_number": 65,
            "catalogued_extent": "5 vols.",
            "current_callmark_bridge": "RM c.41.c.1",
            "bridge_source_url": "https://www.babelstone.co.uk/Morrison/Collection/Numbers.html",
            "bridge_status": "DIRECTLY_ATTESTED_ON_CATALOG_NUMBER_INDEX",
            "independent_physical_witness_increment": 0,
            "batch_id": BATCH_ID,
            "research_artifact": EVIDENCE_REL,
            "quality_notes": "Morrison's 1824 manuscript catalogue records no.65 as 張果老星宗 / 5 vols. The catalogue-number index directly maps RM 65 to RM c.41.c.1; this is an inventory/callmark bridge, not a separate physical witness."
        },
        {
            "source_id": "EXT-ZIWEI-ZHANGGUO-SOAS-MORRISON-RM-C41-C1",
            "title": "《張果星宗命格大全》 / RM c.41.c.1",
            "provider": "Morrison Collection / nineteenth-century UCL shelfmark inventory and 1998 SOAS catalogue description",
            "url": "https://www.babelstone.co.uk/Morrison/Collection/MS58685.html",
            "alternate_url": "https://www.babelstone.co.uk/Morrison/Collection/Description.html",
            "source_role": "LATER_1797_REPRINT_PHYSICAL_LINEAGE_CONTROL_NOT_EARLY_1593_WITNESS",
            "ucl_shelfmark": "L.g.9",
            "current_soas_callmark": "RM c.41.c.1",
            "inventory_date": "1797",
            "bound_item_count": 1,
            "edition_description": "1797 reprint of circa 1593 edition",
            "physical_copy_classification": "QING_DYNASTY_REPRINT_OF_MING_EDITION",
            "genuine_1593_physical_impression": False,
            "target_leaf_obtained": False,
            "whole_book_text_negative_authorized": False,
            "independent_early_physical_witness_increment": 0,
            "later_reprint_physical_lineage_control_increment": 1,
            "independent_target_text_witness_increment": 0,
            "independent_hai_glyph_witness_increment": 0,
            "batch_id": BATCH_ID,
            "research_artifact": EVIDENCE_REL,
            "quality_notes": "UCL shelfmark inventory binds L.g.9 / 張果星宗命格大全 / 1797 / one bound item to RM c.41.c.1. The Morrison Collection description classifies the title as a 1797 Qing reprint of a circa-1593 edition. No target leaf has been collated."
        }
    ]
    for source in additions:
        if source["source_id"] not in existing:
            data["sources"].append(source)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_state() -> None:
    path = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("schema_version") not in {"1.59.0", "1.60.0"}:
        raise SystemExit(f"unexpected state schema version: {state.get('schema_version')}")
    state["schema_version"] = "1.60.0"
    audit = state["historical_audit"]
    if BATCH_ID not in audit["completed_batches"]:
        if audit["completed_batches"][-1] != "BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-AZ":
            raise SystemExit("unexpected completed batch tail before BA")
        audit["completed_batches"].append(BATCH_ID)
    audit["latest_batch_doc"] = BATCH_DOC_REL
    additions = [
        "Batch 12BA separates NCL/SOAS date semantics from physical-impression dating: NCL union record mirr0000375 gives 明萬曆癸巳[1593] but explicitly notes 原刊行年據韋環序, so 1593 is an original-publication-year inference from the preface and is not direct proof that the extant SOAS object was printed in 1593.",
        "Morrison's 1824 manuscript catalogue records 張果老星宗 as RM no.65 / 5 vols.; the Morrison catalogue-number index directly maps RM 65 to current callmark RM c.41.c.1. The nineteenth-century UCL shelfmark inventory then binds L.g.9 / 張果星宗命格大全 / 1797 / one bound item to RM c.41.c.1.",
        "The Morrison Collection edition description classifies 新編評註通玄先生張果星宗大全 as a 1797 reprint of a circa-1593 edition. Therefore RM c.41.c.1 is a later Qing reprint lineage control, not an independent genuine 1593 physical witness. NCL mirr0000375 -> RM c.41.c.1 is high-confidence but not formally closed because the reviewed NCL record exposes no RM callmark/number crosswalk.",
        "Batch 12BA adds zero early physical-witness, target-text and Hai-glyph votes; NCL and Morrison may not be double-counted. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with no runtime winner, candidate collapse or algorithm reopen. Next gate is first-party SOAS item/image binding or another genuinely independent 1593/1594 physical target leaf."
    ]
    for item in additions:
        if item not in audit["current_focus"]:
            audit["current_focus"].append(item)
    inv = state["invariants"]
    if inv.get("confirmed_chart_algorithm_defect_count") != 0 or inv.get("algorithm_reopen_count") != 0 or inv.get("candidate_collapse_count") != 0:
        raise SystemExit("algorithm invariants changed unexpectedly")
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_verifier() -> None:
    path = ROOT / "scripts/verify-project-continuity-state-r1.py"
    text = path.read_text(encoding="utf-8")
    if "ZIWEI_ZHANGGUO_BA_EVIDENCE" in text:
        return
    text = replace_once(
        text,
        'ZIWEI_ZHANGGUO_AZ_EVIDENCE = ROOT / "docs/research/ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-R1.json"\n',
        'ZIWEI_ZHANGGUO_AZ_EVIDENCE = ROOT / "docs/research/ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-R1.json"\n'
        'ZIWEI_ZHANGGUO_BA_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-BA.md"\n'
        'ZIWEI_ZHANGGUO_BA_EVIDENCE = ROOT / "docs/research/ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-R1.json"\n',
        "BA constants",
    )
    text = replace_once(
        text,
        '    "BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-AZ",\n]\nLATEST_BATCH_ID',
        '    "BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-AZ",\n'
        '    "BATCH-12-ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-BA",\n]\nLATEST_BATCH_ID',
        "BA supplemental batch tail",
    )
    text = replace_once(
        text,
        'LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-WEIFANG-1594-PUBLIC-ROUTE-ACCESS-BOUNDARY-AZ.md"',
        'LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-BA.md"',
        "BA latest batch doc",
    )
    text = replace_once(
        text,
        'def main() -> int:\n    for path in (ZIWEI_ZHANGGUO_AZ_BATCH, ZIWEI_ZHANGGUO_AZ_EVIDENCE):',
        'def main() -> int:\n    for path in (ZIWEI_ZHANGGUO_BA_BATCH, ZIWEI_ZHANGGUO_BA_EVIDENCE):\n'
        '        if not path.is_file():\n'
        '            fail(f"Batch 12BA continuity artifact missing: {path.relative_to(ROOT)}")\n\n'
        '    for path in (ZIWEI_ZHANGGUO_AZ_BATCH, ZIWEI_ZHANGGUO_AZ_EVIDENCE):',
        "BA artifact existence gate",
    )
    text = replace_once(
        text,
        '    ziwei_zhangguo_az_evidence = json.loads(ZIWEI_ZHANGGUO_AZ_EVIDENCE.read_text(encoding="utf-8"))\n',
        '    ziwei_zhangguo_az_evidence = json.loads(ZIWEI_ZHANGGUO_AZ_EVIDENCE.read_text(encoding="utf-8"))\n'
        '    ziwei_zhangguo_ba_evidence = json.loads(ZIWEI_ZHANGGUO_BA_EVIDENCE.read_text(encoding="utf-8"))\n',
        "BA evidence load",
    )
    anchor = '    # Provenance/access-only batches can advance without changing any Matrix row.\n'
    checks = '''    # Batch 12BA SOAS/NCL/Morrison 1593-vs-1797 provenance reconciliation.\n    if ziwei_zhangguo_ba_evidence.get("batch_id") != "BATCH-12-ZIWEI-ZHANGGUO-SOAS-NCL-MORRISON-1593-1797-PROVENANCE-RECONCILIATION-BA":\n        fail("Batch 12BA evidence identity mismatch")\n    ncl12ba = ziwei_zhangguo_ba_evidence.get("ncl_union_catalog_record", {})\n    if ncl12ba.get("registration_number") != "mirr0000375" or ncl12ba.get("catalog_date") != "明萬曆癸巳[1593]" or ncl12ba.get("critical_date_note") != "原刊行年據韋環序":\n        fail("Batch 12BA NCL record/date-note binding regressed")\n    if ncl12ba.get("date_semantics") != "ORIGINAL_PUBLICATION_YEAR_INFERRED_FROM_WEI_HUAN_PREFACE_NOT_DIRECT_PHYSICAL_IMPRESSION_DATE" or ncl12ba.get("physical_impression_1593_proven") is not False:\n        fail("Batch 12BA NCL date-semantics firewall regressed")\n    bridge12ba = ziwei_zhangguo_ba_evidence.get("rm_number_to_current_callmark_bridge", {})\n    if bridge12ba.get("rm_number") != 65 or bridge12ba.get("identification") != "RM c.41.c.1 [65]" or bridge12ba.get("bridge_status") != "DIRECTLY_ATTESTED_ON_CATALOG_NUMBER_INDEX":\n        fail("Batch 12BA Morrison RM65 callmark bridge regressed")\n    ucl12ba = ziwei_zhangguo_ba_evidence.get("ucl_shelfmark_inventory", {})\n    if ucl12ba.get("ucl_shelfmark") != "L.g.9" or ucl12ba.get("date") != "1797" or ucl12ba.get("bound_item_count") != 1 or ucl12ba.get("current_soas_callmark") != "RM c.41.c.1":\n        fail("Batch 12BA UCL 1797 physical-lineage binding regressed")\n    desc12ba = ziwei_zhangguo_ba_evidence.get("morrison_collection_edition_description", {})\n    if desc12ba.get("edition_description") != "1797 reprint of circa 1593 edition" or desc12ba.get("physical_copy_classification") != "QING_DYNASTY_REPRINT_OF_MING_EDITION" or desc12ba.get("genuine_1593_impression_claimed") is not False:\n        fail("Batch 12BA Morrison edition classification regressed")\n    identity12ba = ziwei_zhangguo_ba_evidence.get("identity_reconciliation", {})\n    if identity12ba.get("morrison_rm65_to_rm_c41c1") != "RESOLVED_BY_DIRECT_CATALOG_NUMBER_INDEX" or identity12ba.get("rm_c41c1_physical_date") != "1797_REPRINT":\n        fail("Batch 12BA Morrison physical identity/date reconciliation regressed")\n    if identity12ba.get("ncl_mirr0000375_to_rm_c41c1_exact_object_identity") != "HIGH_CONFIDENCE_BUT_NOT_FORMALLY_CLOSED":\n        fail("Batch 12BA NCL-to-Morrison identity confidence scope regressed")\n    if identity12ba.get("early_physical_witness_count_increment") != 0 or identity12ba.get("independent_target_text_witness_increment") != 0 or identity12ba.get("independent_hai_glyph_witness_increment") != 0:\n        fail("Batch 12BA witness accounting regressed")\n    adj12ba = ziwei_zhangguo_ba_evidence.get("philological_and_bibliographic_adjudication", {})\n    if adj12ba.get("ncl_1593_may_be_used_as_original_edition_date_locator") is not True or adj12ba.get("ncl_1593_may_be_used_as_extant_soas_impression_date") is not False:\n        fail("Batch 12BA original-vs-impression-date firewall regressed")\n    if adj12ba.get("morrison_rm_c41c1_may_be_called_genuine_1593_physical_copy") is not False or adj12ba.get("double_count_ncl_and_morrison_as_two_physical_witnesses") is not False or adj12ba.get("preventive_scope_adjudication_not_project_provenance_defect_repair") is not True:\n        fail("Batch 12BA physical-witness/dedup/provenance-defect firewall regressed")\n    effect12ba = ziwei_zhangguo_ba_evidence.get("project_consequence", {})\n    if effect12ba.get("audit_status") != "MISSING_FROM_PRODUCT" or effect12ba.get("runtime_winner_selected") is not False or effect12ba.get("candidate_collapsed") is not False or effect12ba.get("algorithm_reopen") is not False or effect12ba.get("provenance_defect_count_change") is not False:\n        fail("Batch 12BA HPA/algorithm/accounting firewall regressed")\n    registry12ba = {s.get("source_id"): s for s in registry.get("sources", ())}\n    ncl_reg12ba = registry12ba.get("EXT-ZIWEI-ZHANGGUO-NCL-SOAS-MIRR0000375")\n    mor_reg12ba = registry12ba.get("EXT-ZIWEI-ZHANGGUO-SOAS-MORRISON-RM-C41-C1")\n    if not ncl_reg12ba or ncl_reg12ba.get("physical_impression_1593_proven") is not False or ncl_reg12ba.get("independent_early_physical_witness_increment") != 0:\n        fail("Batch 12BA NCL registry date/witness firewall regressed")\n    if not mor_reg12ba or mor_reg12ba.get("inventory_date") != "1797" or mor_reg12ba.get("genuine_1593_physical_impression") is not False or mor_reg12ba.get("independent_early_physical_witness_increment") != 0:\n        fail("Batch 12BA Morrison registry physical-date firewall regressed")\n\n'''
    text = replace_once(text, anchor, checks + anchor, "BA semantic checks")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    update_registry()
    update_state()
    update_verifier()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
