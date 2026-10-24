#!/usr/bin/env python3
"""13FL: preserve catalog/secondary GK05553 28-vs-29 repair-book tension."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
E = "docs/research/TIANWEN-13FL-GK05553-REPLACEMENT-BOOK-ORDINAL-28-29-SOURCE-SCOPE-R1.json"
P = "docs/research/TIANWEN-13FK-NCL-P74-D7D8D10-CROSS-PHOTO-FOURFEN-BOUNDED-COLLATION-R1.json"
S = "docs/PROJECT-CURRENT-STATE-R1.json"
L = "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):
    return json.loads((R / p).read_text(encoding="utf-8"))
def check(e, prior, s, ledger):
    assert e["schema"] == "TIANWEN-13FL-GK05553-REPLACEMENT-BOOK-ORDINAL-28-29-SOURCE-SCOPE-R1"
    assert e["issue_id"] == "TW-OPEN-0005"
    assert e["status"] == "FIRST_PARTY_CATALOG_VS_SECONDARY_SCHOLARLY_TEXT_ORDINAL_DISAGREEMENT_OPEN"
    a, b, d, t, i = (e[x] for x in (
        "first_party_catalog","secondary_scholarship","discrepancy",
        "relation_to_active_rule","impact"))
    assert a["book_id"] == "GK05553_00" and a["bibliographic_copy"] == "奎貴5553"
    assert a["url"] == "https://kyudb.snu.ac.kr/book/view.do?book_cd=GK05553_00"
    assert a["replacement_book_ordinals"] == [8,26,29]
    assert a["reported_original_script"] == "＜奎 5553＞은 第8·26·29冊(合3冊)이 補寫本"
    assert b["replacement_book_ordinals_from_republished_text"] == [8,26,28]
    assert b["journal"] == "《史学史研究》2020年第1期"
    assert b["original_article_pdf_direct_page_collation"] is False
    assert d["exact_ordinal_difference"] == [28,29] and d["agreed_ordinals"] == [8,26]
    assert d["cause"] is d["identity_of_historical_repair_book"] is d["which_is_transcription_or_book_number_error"] is None
    assert d["independent_original_photo_confirmation"] is False
    assert d["cannot_assign_volume_81_to_83_to_official_book29"] is True
    assert a["edition_impression_date"] is a["book52_exact_fascicle"] is None
    assert a["verified_target_leaf_photo"] is False
    assert t["work_juan_52_to_physical_book"] is t["NIKH_viewer_file_kr_052_1056_to_exact_physical_leaf"] is None
    assert t["NLC_D5_original"] == prior["comparison"]["NLC_day5_vs_NIKH_day5_opposed_source_photo_glyphs"][0] == "四分〇一七二"
    assert t["NIKH_D5_original"] == prior["comparison"]["NLC_day5_vs_NIKH_day5_opposed_source_photo_glyphs"][1] == "四分五一七二"
    assert t["NLC_D9_original"] is t["D5_numeric_winner"] is None
    assert t["G893_six_control_status"] == "OPEN" and t["thirteenth_batch_13EI_original_claim"] == "RETRACTED"
    assert not e["transmission_impact"]["nodes_added_or_strengthened"]
    assert not e["transmission_impact"]["edges_supported"]
    assert not e["transmission_impact"]["edges_revised"]
    assert not e["transmission_impact"]["edges_rejected_or_unproved"]
    assert i["external_source_registry_delta"] == i["new_independent_physical_witnesses"] == i["new_historical_target_glyphs"] == 0
    assert i["external_source_registry_total"] == 761 and i["matrix_rows"] == i["matrix_audited"] == 222
    assert i["genealogy_nodes"] == 252 and i["genealogy_edges"] == 238
    assert i["open_risks"] == len(ledger["issues"]) == 11
    assert i["product"] == "CLOSED" and i["algorithm_reopens"] == 0 and i["source_original_D5_winner"] is None
    assert s["schema_version"] == "1.812.0"
    assert ledger["binding"]["reviewed_state_version"] == s["schema_version"]
    assert s["historical_audit"]["research_omission_guard"]["reviewed_state_version"] == s["schema_version"]
    assert ledger["binding"]["source_focus_count"] == len(s["historical_audit"]["current_focus"])
    assert ledger["binding"]["latest_research_focus_prefix"] == "13FL"
    assert any(q.startswith("13FL ") for q in s["historical_audit"]["current_focus"])
    issue = next(q for q in ledger["issues"] if q["id"] == "TW-OPEN-0005")
    assert issue["priority"] == "P0" and issue["status"] == "OPEN"
    assert issue["next_action"].startswith("13FL CURRENT ACTION:")
    assert all(x in issue["next_action"] for x in ("D1 D2 D3 D4 D5 D6","G893","D30","NULL","13EI","四分","初度","GK03539_00","GK03579_00","GK03269_00","GK05554_00"))
    assert {E,E.replace(".json",".md")}.issubset(set(issue["source_refs"]))
    assert any(q.get("revision_id") == "TW-OPEN-0005-13FL-GK05553-REPAIR-BOOK-28-29-SOURCE-CONFLICT-20261024" for q in issue["history"])
    assert ledger["checkpoint_log"][-1]["state_version"] == s["schema_version"]
    assert ledger["checkpoint_log"][-1]["id"] == "OMISSIONS-13FL-GK05553-28-29-ORDINAL-CONFLICT-20261024"
    return True
if __name__ == "__main__":
    assert check(load(E),load(P),load(S),load(L))
    print("13FL_PASS_CATALOG29_SECONDARY28_UNRESOLVED_NO_D5_OR_D9_FORCED_WINNER")
