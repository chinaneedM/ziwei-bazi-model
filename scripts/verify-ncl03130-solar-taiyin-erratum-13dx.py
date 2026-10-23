#!/usr/bin/env python3
"""13DX: ensure same-source lunar limit number is never mis-voted as solar XingDu."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13DX-NCL03130-SOLAR-TAIYIN-TABLE-CATEGORY-FORWARD-ERRATUM-R1.json"; S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"; L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13DX-NCL03130-SOLAR-TAIYIN-CATEGORY-ERRATUM-R1"
 assert e["correction_type"]=="FORWARD_ONLY_SOURCE_TABLE_IDENTITY_ERRATUM"
 assert e["previous_batches_retained_immutable"]==["13DT","13DU","13DV","13DW"]
 assert e["source_object"]["source_sha256"]=="3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
 assert e["source_object"]["physical_copy_identity"]=="UNBOUND" and e["source_object"]["ocr_used"] is False
 pages=e["acquired_original_evidence"]
 assert [p["page"] for p in pages]==list(range(81,91))
 assert [p["source_png_sha256"] for p in pages]==["92d45bc726e35087173d25ff5ea75885f6a1c8757890d57f3a1d71936ce7dcbe","4b8efc11d9ce84e9025f8115533cafb4a6a33e2653e33f548b1d85c9487c6ed7","713d7dddf8f26030eaca40b3552f598acdc580cfbf291da059461a6d7bec83c0","abfabdaba9c64c845b0f8e4fba078de3e36a93cedfa8ff2da09a98619753917a","09512931027d1677e34af8fc5244493f936837d39f6047d1ced87e7a7bcef8c7","9107be92e0381fb596ffec33f2e7fbcffda2adc0f17bca4da303ffec6032693c","efdd635b305c05b0340bdc17d5e5cb90882c367e324de422df84ec3b33c30710","071baa8520fcbcf78bd85cff3065e77943c53ae1ec01cba0c49dbd74077e01db","410ea3c121c7d63e5df9c97c501a5da3a571b2b76244e2a59bfe0f767de66261","c9bdb2601d2b453d2e5474b144a638cc7bce955eb92b11baae63f816c038e4f7"]
 assert pages[1]["observed"].startswith("SOURCE_ORIGINAL_READS_太陰限數遲疾度")
 assert [p["observed"] for p in pages[2:]]==[
   "TAIYIN_LIMIT_SEQUENCE_RESTART_1_TO_8","TAIYIN_LIMIT_9_TO_15","TAIYIN_LIMIT_16_TO_22",
   "TAIYIN_LIMIT_23_TO_30","TAIYIN_LIMIT_31_TO_37","TAIYIN_LIMIT_38_TO_44",
   "TAIYIN_LIMIT_45_TO_52","TAIYIN_LIMIT_53_TO_59"]
 r=e["p86_source_native_limit28"]
 assert r["ordinal_type"]=="TAIYIN_LIMIT_NUMBER" and r["table_title"]=="太陰限數遲疾度"
 assert (r["printed_ordinal"],r["field_name"],r["source_original_literal"],r["source_value"])==("二十八","遲疾曆日率","二日二九六二","2.2962")
 assert r["source_roi"]["png_sha256"]=="5428823bed7f7b25fce08fae873583cdd3ae01b4717ac5a396cb81da86f30167"
 assert r["source_roi"]["rgb_sha256"]=="4aa02c6a50b2cc9a6e9259396b9a2af1f5989fb3561adf2638f3f5194c44f2a1"
 assert e["received_text_comparator"]["evidence_class"]=="MODERN_RECEIVED_TRANSCRIPTION_NOT_AN_ADDITIONAL_PHYSICAL_COPY"
 assert e["received_text_comparator"]["dayrate"]==r["source_original_literal"]
 a=e["adjudication"]
 assert a["p86_prior_solar_D28_target"]=="REJECTED_AS_WRONG_TABLE"
 assert a["p86_correct_object"]=="TAIYIN_LIMIT_28"
 assert a["solar_summer_xingdu_D28_in_NCL"]=="NOT_FOUND_YET_IN_CORRECT_TABLE" and a["solar_D28_numeric"]=="UNREAD"
 assert a["solar_D28_0_994549_physical_vote"]=="NOT_ADMITTED_FROM_P86"
 assert a["arithmetic_0_964549_physical_vote"]=="NOT_ATTESTED"
 assert all(a[k]==0 for k in ("new_source_registry_entries","new_genealogy_nodes","new_genealogy_edges","algorithm_reopen_count","research_issues_closed"))
 assert a["chart"]=="CLOSED"
 q=e["next_page_search"]
 assert q["requested_pages"]==[73,74,75,76,77,78,79,80]
 assert q["p76_is_confirmed_solar_D28"] is False and q["no_ocr"] is True
 assert q["source_original_target_xingdu"]=="PENDING_DIRECT_CORRECT_TABLE_PAGE"
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13DX ") for x in s["historical_audit"]["current_focus"])
 assert any(x.startswith("13DW ") for x in s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert "docs/research/TIANWEN-13DX-NCL03130-SOLAR-TAIYIN-TABLE-CATEGORY-FORWARD-ERRATUM-R1.json" in issue["source_refs"]
 assert any(h.get("revision_id")=="TW-OPEN-0005-13DX-SOLAR-TAIYIN-ERRATUM" for h in issue["history"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L))
 print("13DX_PASS")
