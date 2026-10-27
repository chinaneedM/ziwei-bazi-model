#!/usr/bin/env python3
"""12YY isolate NIKH modern received D16 anomaly without ancient-original claim."""
from decimal import Decimal
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YY-GORYEOSA-FIRSTPARTY-ONLINE-SOLAR-D16-RECEIVED-VARIANT-VS-G893-ORIGINAL-R1.json"
PREVIOUS="docs/research/TIANWEN-12YD-G893-D15-D17-DIRECT-SOLAR-PRINTED-FIVE-FEN-SEQUENCE-R1.json"
def read():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json",PREVIOUS))
def require(v,msg):
 if not v:raise ValueError(msg)
def verify(d,l,s,prior):
 require(d["schema"]=="TIANWEN-12YY-GORYEOSA-INSTITUTIONAL-RECEIVED-D16-LOCAL-NUMERAL-DIVERGENCE-R1","schema")
 src=d["sources"]
 require(src["goryeosa_institutional"]["url"]=="https://db.history.go.kr/goryeo/level.do?levelId=kr_052_0010_0010_0020_0010&types=o","official primary digital source")
 require(src["goryeosa_institutional"]["evidence_level"]=="RECEIVED_DIGITAL_TEXT_TRANSCRIPTION_NOT_MANUALLY_INSPECTED_HISTORICAL_PAPER_FOLIO","digital vs original")
 require(src["g893_original"]["original_print_source_record"]==PREVIOUS and src["g893_original"]["page_id"]=="002b" and src["g893_original"]["original_page_sha256"]=="f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55","G893 original locus")
 original=prior["original_reading_scope"]["source_bounded_candidate_vertical_lane"]
 require([x["original_short_glyph_string"] for x in original]==[x["g893_original"] for x in d["direct_reading"]["days"]],"older certified native source")
 days=d["direct_reading"]["days"]
 require([x["day"] for x in days]==[15,16,17],"ordered neighborhood")
 require([x["official_goryeosa"] for x in days]==["五分二一七六","五分一三六二","五分二五四八"],"first-party received glyphs")
 require(all(x["wikisource_goryeosa"]==x["official_goryeosa"] for x in days),"secondary received mirror")
 off=[Decimal(x["official_number"]) for x in days]
 ori=[Decimal(x["g893_candidate_number"]) for x in days]
 require([str(a) for a in ori]==["5.2176","5.2362","5.2548"] and [str(a) for a in off]==["5.2176","5.1362","5.2548"],"candidate decimals")
 a=d["decimal_adjacency"]
 require(str(ori[1]-ori[0])==a["source_g893_day15_to_day16"]=="0.0186" and str(ori[2]-ori[1])==a["source_g893_day16_to_day17"],"G893 recurrence")
 require(str(off[1]-off[0])==a["institution_day15_to_day16"]=="-0.0814" and str(off[2]-off[1])==a["institution_day16_to_day17"]=="0.1186","received anomaly")
 require(str(off[2]-2*off[1]+off[0])==a["institution_d16_second_difference"]=="0.2000","received second difference")
 require(str(off[1]-ori[1])==a["received_deviation_from_both_neighbors"]=="-0.1000","single digit divergence")
 require(d["direct_reading"]["glyph_position_difference"]["official"]=="一" and d["direct_reading"]["glyph_position_difference"]["g893"]=="二","cannot silently normalize literal")
 sc=d["scope_firewall"]
 require(all(sc[k] is False for k in ("institutional_digital_text_is_not_original_image","wikisource_and_institutional_text_are_two_independently_attested_ancient_prints","distinct_goryeosa_historical_paper_page_verified","G893_day16_complete_target_field_confirmed")) is False,"booleans sanity check")
 require(sc["institutional_digital_text_is_not_original_image"] is True and sc["wikisource_and_institutional_text_are_two_independently_attested_ancient_prints"] is False and sc["distinct_goryeosa_historical_paper_page_verified"] is False,"digital/physical gate")
 require(sc["historical_少_微_unit_mapping"]=="UNPROVEN" and sc["attribution_as_original_printing_or_ocr_error"]=="UNDETERMINED" and sc["historical_transmission_direction"]=="UNPROVEN","no unearned inference")
 require(all(sc[k]==0 for k in ("new_ancient_physical_source_votes","source_registry_new_entries","transmission_graph_nodes","transmission_graph_edges","runtime_algorithm_reopens")),"no counterfeit vote")
 require(sc["g893_principal_six"]=="5/6" and sc["g893_final_cross_source"]=="0/6" and sc["open_issues"]==11 and sc["product_R1"]=="CLOSED","unresolved unchanged")
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 require(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"research issue linkage")
 require(issue["g893_12yy_goryeosa_d16_modern_transcription_reviews"][0]["goryeosa_original_image_verified"] is False,"false paper-leaf claim")
 require(l["binding"]["reviewed_state_version"]==s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"state consistency")
 require(l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"]) and any(x.startswith("12YY ") for x in s["historical_audit"]["current_focus"]) and l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ")[0],"append-only batch compatibility")
 require(l["checkpoint_log"][-1]["state_version"]==s["schema_version"] and len(l["checkpoint_log"][-1]["reviewed_issue_ids"])==len(l["issues"]),"ledger all issues reviewed")
 return {"status":"PASS","discrepancy":"GORYEOSA_DIGITAL_5.1362_VS_G893_ORIGINAL_5.2362","gap":"0.1000","physical_copy_votes_added":0,"open_issues":11}
if __name__=="__main__":print(json.dumps(verify(*read()),ensure_ascii=False))
