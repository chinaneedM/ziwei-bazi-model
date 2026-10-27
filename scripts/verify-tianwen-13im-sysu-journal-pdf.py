#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH="docs/research/TIANWEN-13IM-SYSU-2020-JOURNAL-ORIGINAL-PDF-FOOTNOTE-AND-GK5553-ROUTE-R1.json"
def read(path=PATH): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(x,with_state=True):
    assert x["schema"]=="TIANWEN-13IM-SYSU-2020-JOURNAL-ORIGINAL-PDF-FOOTNOTE-AND-GK5553-ROUTE-R1"
    assert x["issue_id"]=="TW-OPEN-0005"
    a=x["journal_original"]
    assert a["article_publication_year"]==2020 and a["journal"]=="史学史研究"
    assert (a["web_pdf_view_pages"],a["observed_printed_page_start"],a["observed_printed_page_footnote"],a["observed_printed_page_end"])==(12,93,100,104)
    assert (a["page0_index"],a["page100_index"],a["page104_index"])==(0,7,11)
    assert a["direct_url"].startswith("https://sir.sysu.edu.cn/sites/default/files/2026-07/")
    assert a["source_web_pdf_viewer"]=="DIRECT_WEB_OPEN_CONTENT_TYPE_APPLICATION_PDF_12_PAGES"
    assert a["original_journal_direct_page_recovered"] is True
    for k in ("binary_downloaded_to_project","visual_page_100_chinese_glyphs_exhaustive","journal_original_page_is_historical_goryeosa_copy"):
        assert a[k] is False
    assert a["raw_pdf_bytes_sha256"] is None and a["hosted_pdf_file_byte_hash_not_yet_verified"] is True
    b=x["original_footnote"]
    assert (b["printed_page"],b["footnote_number"])==(100,6)
    assert b["facsimile_base"]=="奎5554" and b["excluded_alternate_holding"]=="奎5553"
    assert b["supplement_from_woodblock_volume_numbers"]==[19,20,21,31,73,74,77,78,79,81,82,83]
    assert b["alternate_eulhae_eligible_but_not_used"]==[31,77,78,79,81,82]
    c=x["scope_boundaries"]
    assert len(c["separate_objects"])==3
    for k in ("gk3467_book6_original_physical_leaves_between_folio2_and_folio10_recovered","gk3467_original_winter_table_heading_recovered","gk3467_original_d1_to_d7_recovered","g893_six_original_target_values_adjudicated","source_original_article_footnote_can_close_ancient_copy_quire","original_pdf_cjk_glyph_pixels_all_verified"):
        assert c[k] is False
    assert c["physical_copy_missing_leaf_count"] is None
    assert c["new_independent_ancient_source_witnesses"]==c["new_genealogy_edges"]==c["algorithm_reopen_count"]==0
    assert x["invariants"]=={"matrix":[222,222],"registry":761,"graph":[252,238],"issues":11,"deterministic_chart_product":"CLOSED","algorithm_reopens":0,"candidate_collapses":0}
    if with_state:
        s=read("docs/PROJECT-CURRENT-STATE-R1.json")
        l=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
        assert s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==l["binding"]["reviewed_state_version"]
        assert tuple(map(int,s["schema_version"].split("."))) >= (1,892,0)
        assert any(z.startswith("13IM ") for z in s["historical_audit"]["current_focus"])
        issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
        assert issue["status"]=="OPEN" and PATH in issue["source_refs"]
        assert any(z.get("new_action_prefix")=="13IM" for z in issue["history"])
    return True
if __name__=="__main__":
    assert check(read())
    print("TIANWEN_13IM_SYSU_ORIGINAL_PDF_PAGE_AND_FOOTNOTE_FIREWALL_PASS")
