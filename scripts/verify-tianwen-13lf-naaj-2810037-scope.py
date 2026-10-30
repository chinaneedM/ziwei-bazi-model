#!/usr/bin/env python3
"""13LF 281-0037 manuscript locator: no inferred original witness or false historical winner."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13LF-NAJDA-2810037-CHAPTER-BINDING-AND-ORIGINAL-ACQUISITION-R1.json"
def load():
    return tuple(json.loads((ROOT/x).read_text(encoding="utf-8")) for x in (E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def check(e,s,l):
    assert e["schema"]=="TIANWEN-13LF-NAJDA-2810037-CHAPTER-BINDING-AND-ORIGINAL-ACQUISITION-R1" and e["issue_id"]=="TW-OPEN-0005"
    h=e["holding"];f=e["file_directory"];a=e["acquisition"];c=e["comparisons"];scope=e["scope"]
    assert h["reference_code"]=="281-0037" and h["physical_volumes"]==120 and h["prior_holder"]=="昌平坂学問所"
    assert not h["exact_impression_1739_proved"] and not h["same_printing_block_as_2810038_proved"]
    assert f["candidate_books_for_image_review"]==[10,11,12,13,14] and not f["exact_chapter_to_book_mapping_proved"] and f["candidate_books_are_not_asserted_to_contain_juan35"]
    assert not f["original_pdf_acquired_and_hash_verified_in_this_batch"] and not f["printed_numeral_read_from_2810037"]
    assert a["published_run_id"] is None and a["published_artifact_id"] is None and not a["original_folio_glyph_read"]
    assert c["direct_2810037_original_reading"] is None and c["independent_textual_recension_votes_new"]==0 and c["original_g893_six_historical_winners"]==0
    assert c["naaj_2810038_original_23897709"] and c["harvard_original_23897709"] and c["cadal_siku_original_28897709"]
    assert scope==dict(registry_root=647,registry_extensions=118,registry_total=765,matrix_rows=222,matrix_audited=222,graph_nodes=252,graph_edges=238,issues_open=11,chart_product="CLOSED",algorithm_reopens=0,registered_sources_added=0,genealogy_nodes_added=0,genealogy_edges_added=0)
    assert not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"]
    focus=s["historical_audit"]["current_focus"];binding=l["binding"]
    assert any(x.startswith("13LF ") for x in focus) and binding["source_focus_count"]==len(focus) and binding["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0]
    assert s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==binding["reviewed_state_version"]==l["checkpoint_log"][-1]["state_version"]
    issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
    assert issue["priority"]=="P0" and issue["status"]=="OPEN" and issue["next_action"].startswith(binding["latest_research_focus_prefix"]+" CURRENT ACTION:")
    assert E in issue["source_refs"] and E[:-5]+".md" in issue["source_refs"]
    assert any(x.get("revision_id")=="TW-OPEN-0005-13LF-NAJDA2810037-LOCATOR-20261030" for x in issue["history"])
    assert len(l["issues"])==11 and s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
    return {"status":"PASS","new_original_numeric_winners":0,"copy_2810037_chapter_binding":"PENDING"}
if __name__=="__main__":print(json.dumps(check(*load()),ensure_ascii=False))
