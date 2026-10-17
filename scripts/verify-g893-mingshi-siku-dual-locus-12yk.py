#!/usr/bin/env python3
"""12YK: two independent arithmetic loci of modern received MingShi textual surfaces, zero physical witness votes."""
import json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YK-MINGSHI-V33-SIKU-RECEIVED-DUAL-LOCUS-ARITHMETIC-R1.json"
EXPECTED={
"MINGSHI_GENERAL_WIKISOURCE":("0.0186","4.9286"),
"MINGSHI_SIKU_WIKISOURCE":("0.0136","4.9386"),
"MINGSHI_DAZHISHI":("0.0186","4.9386"),
"DATONG_LIZHI_SHIDIAN":("0.0186","4.9386")
}
def need(v,msg):
 if not v:raise ValueError(msg)
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in [DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"])
def verify(d,ledger,state):
 need(d["schema"]=="TIANWEN-12YK-MINGSHI-V33-SIKU-RECEIVED-DUAL-LOCUS-ARITHMETIC-R1","schema")
 need(d["previous_batch"]=="docs/research/TIANWEN-12YJ-G893-HEADER-MINGSHI-PINGLI-RECEIVED-TEXT-ARITHMETIC-R1.json","12YJ parent")
 old=json.loads((ROOT/d["previous_batch"]).read_text(encoding="utf-8"))
 need(old["textual_calc"]["ming_shi_difference"]=="-0.0100" and old["textual_calc"]["correct_sum"]=="4.9386","unmodified 12YJ")
 need(d["scope"]=="FOUR_WEB_TEXT_PRESENTATIONS_NOT_FOUR_INDEPENDENT_EDITION_OR_PHYSICAL_WITNESSES","false independent voting")
 w=d["received_text_presentations"]
 need(len(w)==4 and [x["key"] for x in w]==list(EXPECTED),"four source-specific web text presentations")
 for item in w:
  allowed={
   "MINGSHI_GENERAL_WIKISOURCE":"RECEIVED_WEB_TRANSCRIPTION_NOT_PHYSICAL_PAGE",
   "MINGSHI_SIKU_WIKISOURCE":"RECEIVED_WEB_TRANSCRIPTION_WITH_UNVERIFIED_SIKU_EDITION_LABEL_NOT_PHYSICAL_PAGE",
   "MINGSHI_DAZHISHI":"RECEIVED_WEB_TRANSCRIPTION_NOT_VERIFIED_PHYSICAL_EDITION",
   "DATONG_LIZHI_SHIDIAN":"LATER_RECEIVED_EXEGETICAL_WEB_TRANSCRIPTION_NOT_PHYSICAL_PAGE"
  }
  need(item["url"].startswith("https://") and item["representation"]==allowed[item["key"]],"received only, no original upgrades")
  need((item["intermediate_decimal"],item["sum_decimal"])==EXPECTED[item["key"]],"source-local 2 locus glyph candidates")
  need(item["intermediate_glyph"].startswith("一秒") and item["sum_glyph"].startswith("四分") and "三十一" in item["multiplier_glyph"],"glyph confidence scope")
 m=d["mechanical_semantics"]
 def q(name):return Decimal(m[name])
 need(q("licha")*Decimal(m["factor"])==q("true_intermediate")==Decimal("0.0186"),"multiplication")
 need(q("base")+q("true_intermediate")==q("correct_total")==Decimal("4.9386"),"corrected sum")
 need(q("siku_reported_intermediate")==Decimal("0.0136") and q("general_reported_total")==Decimal("4.9286") and q("siku_reported_total")==Decimal("4.9386"),"variant inputs")
 need(q("general_reported_total")-q("correct_total")==q("delta_general_total")==Decimal("-0.0100"),"general discrepancy")
 need(q("siku_reported_intermediate")-q("true_intermediate")==q("delta_siku_intermediate")==Decimal("-0.0050"),"siku multiplication discrepancy")
 need(q("siku_reported_total")-(q("base")+q("siku_reported_intermediate"))==q("delta_siku_self_sum")==Decimal("0.0050"),"siku internal mismatch")
 need(q("siku_reported_total")-q("correct_total")==q("delta_siku_total_using_multiplied_correct")==Decimal("0.0000") and m["precision"]=="EXACT_DECIMAL_4","false arithmetic award")
 c=d["two_locus_controls"]
 need(len(c)==2 and c[0]["readings"]==[x["intermediate_decimal"] for x in w] and c[1]["readings"]==[x["sum_decimal"] for x in w] and c[0]["mismatch_siku"]=="-0.0050" and c[1]["general_vs_math"]=="-0.0100" and c[1]["siku_reported_minus_its_own_intermediate"]=="+0.0050","two-locus crosswalk")
 scan=d["scan_candidate"]
 need("upload.wikimedia.org" in scan["url"] and "36398055" in scan["fetch_attempt"] and all(scan[k] is False for k in ("actual_scanned_folio_read","physical_copy_date_verified","edition_impression_date_verified","scan_payload_hash_verified")) and scan["may_not_upgrade_grade"] is True and scan["claim_about_its_printed_glyphs"]=="UNVERIFIED_TARGET_PAGE","invented PDF original")
 q=d["crosswalk"]
 need(q["g893_source"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893" and q["g893_original_header_jpeg_page"]=="001a" and q["g893_daily_short_difference"]=="0.0186","G893 original source identity")
 need(q["mingshi_field_same_as_g893"]=="UNPROVEN" and q["native_g893_少_vs_received_微"]=="UNRESOLVED" and q["ming1569_independent_original_column"]=="NOT_BOUND","unsupported bridge")
 need(all(q[k]==0 for k in ("physical_witnesses_added","source_registry_additions","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens")),"imaginary witness")
 need(q["original_formal_targets"]=="5/6" and q["cross_witness_mechanical_final"]=="0/6" and q["open_research_issues"]==11,"premature closure")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 need(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"risk/source linkage")
 rows=issue["g893_12yk_dual_locus_received_comparison"]
 need(len(rows)==1 and rows[0]["evidence_doc"]==DOC and rows[0]["source_surfaces"]==4 and rows[0]["siku_intermediate"]=="0.0136" and rows[0]["siku_total"]=="4.9386" and rows[0]["web_pdf_original_folio_verified"] is False and rows[0]["physical_original_votes_added"]==0,"issue review mismatch")
 need(any(x.get("event")=="ISSUE_REVISION" and DOC in x.get("evidence_refs",[]) and "next_action" in x.get("changed_fields",[]) for x in issue["history"]), "append-only revision missing")
 need(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,625,0) and any(x.startswith("12YK ") for x in state["historical_audit"]["current_focus"]),"state sync")
 need(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"product closure")
 return {"status":"PASS","web_text_presentations":4,"received_loci":2,"siku_multiplication_delta":"-0.0050","mingshi_general_sum_delta":"-0.0100","physical_original_votes":0,"cross_witness_final":"0/6"}
if __name__=="__main__":
 print(json.dumps(verify(*load()),ensure_ascii=False))
