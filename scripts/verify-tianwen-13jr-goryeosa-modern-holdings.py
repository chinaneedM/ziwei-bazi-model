#!/usr/bin/env python3
"""13JR: never upgrade catalog-level 1972/1983 bibliographies to ancient physical/glyph proof."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
P = "docs/research/TIANWEN-13JR-GORYEOSA-1972-DUAL-SERIES-1983-REPRINT-HOLDINGS-ACCESS-GATE-R1.json"
def load():
    return tuple(json.loads((ROOT / p).read_text(encoding="utf-8")) for p in (P, "docs/PROJECT-CURRENT-STATE-R1.json", "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def verify(proof, state, ledger):
    assert proof["schema"] == "TIANWEN-13JR-GORYEOSA-1972-DUAL-SERIES-1983-REPRINT-HOLDINGS-ACCESS-GATE-R1"
    assert proof["issue_id"] == "TW-OPEN-0005"
    rows = proof["catalogs"]
    assert len(rows) == 5 and len({r["id"] for r in rows}) == 5
    b,c,d,h,t = rows
    assert b["ncid"] == "BA63617326" and b["series"] == "韓國學古典씨리즈" and b["extent"] == "3冊; 21cm"
    assert b["selected_physical_holdings"][1]["item_id"] == "005132003069258"
    assert c["ncid"] == "BB04922175" and c["series"] == "古典大學講讀教材; 7"
    assert c["year_label"] == "1972.9" and c["extent"] == "3冊; 22cm" and c["catalog_note"] == "刊行辞: 李 昌(1983年2月)"
    assert [r["item_id"] for r in c["selected_physical_holdings"]] == ["5065076","5065077","5065078"]
    assert d["ncid"] == "BA6602288X" and d["year_label"] == "1983.4" and d["edition_statement"] == "再版"
    assert d["catalog_note"] == "1972年初版"
    assert len(d["selected_physical_holdings"]) == 3 and d["selected_physical_holdings"][1]["item_id"] == "00014464994"
    assert len(h["modern_observations"]) == 3 and all(x["result_detail_access"] == "PUBLIC_WEB_DETAIL_RETURNED_PAGE_NOT_FOUND" for x in h["modern_observations"])
    assert t["ncid"] == "BA73763630" and t["publisher"] == "文史哲出版社" and t["place"] == "臺北"
    assert all(not q["original_colophon_seen"] and not q["ancient_gk5554_folio_bound"] for q in rows)
    a = proof["bibliographic_adjudication"]
    for name in ("riss_1972_yonsei_four_volumes_preserved_from_13jq", "two_1972_asia_cinii_ncid_are_distinct_catalog_entries", "chuo_1983_second_edition_catalog_not_1972_first_print_physical_proof", "chuo_first_1972_note_does_not_certify_1972_copy_original_pages", "hanbat_search_listing_is_not_direct_copy_colophon", "hanbat_detail_404_does_not_prove_book_absent", "taiwan_1972_is_separate_publisher_and_publication_place"):
        assert a[name] is True, name
    for name in ("two_asia_1972_catalog_entries_are_proven_distinct_textual_editions", "bb04922175_1972_9_plus_1983_2_preface_is_sufficient_to_identify_each_1972_physical_impression", "asian_1972_original_folio_or_work_juan52_retrieved", "modern_catalog_entry_is_independent_ancient_witness"):
        assert a[name] is False, name
    assert a["khs_manuscript_ordinals_8_12_26_vs_snu_8_26_29"] == "OPEN"
    assert a["old_13io_physical_book29"] == "RETRACTED_UNBOUND"
    assert a["deterministic_product"] == "CLOSED"
    assert all(a[k] == 0 for k in ("g893_six_numeric_targets_closed_this_batch", "new_independent_ancient_physical_witness_votes", "new_1972_full_page_originals", "genealogy_nodes_edges_added", "historical_source_registry_additions", "algorithm_reopens"))
    f = state["historical_audit"]["current_focus"]
    assert any(x.startswith("13JQ ") for x in f) and any(x.startswith("13JR ") for x in f)
    assert state["schema_version"] == ledger["binding"]["reviewed_state_version"] == state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert ledger["binding"]["source_focus_count"] == len(f)
    assert ledger["binding"]["latest_research_focus_prefix"] == f[-1].split(" ",1)[0]
    issue = next(x for x in ledger["issues"] if x["id"] == "TW-OPEN-0005")
    assert issue["status"] == "OPEN" and issue["priority"] == "P0"
    assert P in issue["source_refs"] and P.replace(".json", ".md") in issue["source_refs"]
    assert issue["history"][-1]["revision_id"].startswith("TW-OPEN-0005-13JR")
    assert ledger["checkpoint_log"][-1]["state_version"] == state["schema_version"]
    assert set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"]) == {x["id"] for x in ledger["issues"]}
    return {"status":"PASS", "catalog_records":5, "original_folio_new":0, "ancient_physical_votes":0}
if __name__ == "__main__":
    print(json.dumps(verify(*load()), ensure_ascii=False))
