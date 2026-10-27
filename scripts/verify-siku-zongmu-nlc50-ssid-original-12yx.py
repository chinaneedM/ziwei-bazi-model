#!/usr/bin/env python3
"""12YX source-byte bound parallel original-title variants are evidence, not edition genealogy."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YX-SIKU-ZONGMU-NLC50-SSID106-DUAL-ORIGINAL-RUBRIC-GLYPH-COLLATION-R1.json"
def read():
 return [json.loads((R/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json")]
def check(d,l,s):
 def req(x,msg):
  if not x: raise ValueError(msg)
 req(d["schema"]=="TIANWEN-12YX-SIKU-ZONGMU-SAME-WORK-TWO-SCANS-DIRECT-PRINTED-TITLE-REVIEW-R1","schema")
 a=d["source_acquisition"]
 req(a["job_run_id"]==39035535094 and a["artifact_id"]==12102300310 and a["artifact_retention_days"]==20,"run source binding")
 req(a["original_byte_hashes_self_calculated"] is True and len(a["scans"])==2,"source files")
 src={x["source_id"]:x for x in a["scans"]}
 req(set(src)=={"SSID-11564461","NLC892-001945406-317607"},"source identities")
 req((src["SSID-11564461"]["bytes"],src["SSID-11564461"]["pages"],src["SSID-11564461"]["sha256"])==(8724887,101,"1ad6be6b74970ba6f56f6f4a298dc9e85d3e80d41907975ce599cc7952f2611b"),"SSID source")
 req((src["NLC892-001945406-317607"]["bytes"],src["NLC892-001945406-317607"]["pages"],src["NLC892-001945406-317607"]["sha256"])==(65706664,103,"85cb8f8e072dea9e077988783c2276730a6477de22a318cf683c87f5ba803c6e"),"NLC source")
 req(src["SSID-11564461"]["historical_impression_date"]=="UNVERIFIED" and src["NLC892-001945406-317607"]["historical_impression_date"]=="EXACT_DATE_UNVERIFIED","no pseudo-printing year")
 reads=d["direct_original_glyphs"]
 req([(x["source_id"],x["viewer_page"],x["pdf_index"]) for x in reads]==[("SSID-11564461",87,86),("SSID-11564461",89,88),("NLC892-001945406-317607",93,92),("NLC892-001945406-317607",94,93)],"exact folio binding")
 req([x["exact_printed"] for x in reads]==["大統歷志八卷附錄一卷","十七目一目定為一卷以便循覽焉","大統書志十七卷","以所立十七目一目定為一卷以便循覽焉"],"literal printed sources")
 req([x["page_RGB_sha256"] for x in reads]==["3975a380bd37ccd7e53d5cb5c63f915477b7d91fb478594b0837650b5c9343b6","dc77ed24662d7b0ccf25aaada1c38b60dbe4a3208af8476caff9516a74b55be9","8c3963f39e8df021ffd0deb3de3bbc64e8e40e252b346262c0c6d88adad44654","bcfc5036d0994af2fedc160fce911d1e9ab84083c17cd2de56b3ac2fbda5da19"],"render image SHA")
 req(all(x["ocr_used"] is False for x in reads),"no OCR")
 t=d["title_variant"]
 req(t["printed_title_glyph_divergence"]==["歷","書"] and t["printed_volume_count_divergence"]==["八卷附錄一卷","十七卷"],"variant identity")
 req(t["independently_certified_distinct_historical_physical_impressions"] is False and t["editorial_winner_or_scribal_error_proven"] is False and t["genealogical_copy_direction"]=="UNPROVEN","no forged stemma verdict")
 im=d["evidence_impact"]
 req(im["scanned_document_files_fully_sha256_bound"]==2 and im["direct_original_catalog_page_render_loci_reviewed"]==4 and im["newly_verified_original_printed_rubric_locus"]==1,"bounded evidence")
 req(all(im[x]==0 for x in ("source_registry_additions","additional_independent_ancient_historical_print_votes","genealogy_nodes_added","genealogy_edges_added","new_G893_original_numeric_decisions","algorithm_reopen_count")),"false mechanical or source vote")
 req(im["G893_source_six_original_fields"]=="5/6" and im["G893_cross_source_final"]=="0/6" and im["research_issues_open"]==11 and im["chart_R1"]=="CLOSED","product freeze")
 issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
 req(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"issue original evidence")
 req(issue["mei_12yx_dual_original_zongmu_title_reviews"][0]["nlc_printed_title"]=="大統書志十七卷" and issue["mei_12yx_dual_original_zongmu_title_reviews"][0]["source_sha256_nlc"]==src["NLC892-001945406-317607"]["sha256"],"source cross-binding")
 req(l["binding"]["reviewed_state_version"]==s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"handoff drift")
 req(l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"]) and any(x.startswith("12YX ") for x in s["historical_audit"]["current_focus"]) and l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ")[0],"append-only focus")
 req(l["checkpoint_log"][-1]["state_version"]==s["schema_version"],"checkpoint")
 return {"result":"PASS","different_printed_original_titles":2,"source_sha256_originals":2,"printed_folio_loci":4,"new_independent_historical_impression_votes":0,"open_issues":11}
if __name__=="__main__":print(json.dumps(check(*read()),ensure_ascii=False))
