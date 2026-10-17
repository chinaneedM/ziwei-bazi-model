#!/usr/bin/env python3
"""12YJ: source-scoped G893 header vs later received textual arithmetic; no physical vote."""
import argparse,hashlib,io,json,zipfile
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YJ-G893-HEADER-MINGSHI-PINGLI-RECEIVED-TEXT-ARITHMETIC-R1.json"
def require(c,m):
 if not c:raise ValueError(m)
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def verify(d,ledger,state):
 require(d["schema"]=="TIANWEN-12YJ-G893-HEADER-RECEIVED-TEXT-UNIT-BOUNDARY-R1","schema")
 o=d["source_original"]; require(o["id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893" and o["provider_copy"]=="GK00893_00","source identity")
 require(o["archive_sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107" and o["archive_bytes"]==33525981 and o["crc"]=="PASS" and o["reverified_original_jpeg_sha_count"]==204,"archive proof")
 require(o["page"]=="001a" and o["page_sha256"]=="8b07513ca8aad42ae167a93f22c39f14850c8cd1c345db9ce98c1e0e769226a5" and o["original_rgb_roi"]=={"rect":[480,580,720,1380],"sha256":"6416400c1805f41b5dc56e3ff6cc6f11b057ff6eb266bb3c8934ad8dcf7b853f"},"original source ROI")
 require(o["visible_terms"]==["盈縮積","盈縮加分","日差加一秒八十六少"] and o["last_graphic_少_vs_微"]=="UNRESOLVED_SOURCE_GLYPH_VS_RECEIVED_TEXT_NORMALIZATION" and o["column_header_to_numeric_lane_unit"]=="UNPROVEN" and o["second_as_modern_time_second"]=="FORBIDDEN_INFERENCE" and o["new_original_pages"]==0,"header unit forbidden bridge")
 rows=d["received_witnesses"];require(len(rows)==4,"four received texts")
 require([x["work"] for x in rows]==["明史","大統歷志","授時曆故","古今律歷考"],"received witness identity")
 expected=["4.9286","4.9386","4.9386","4.9386"]
 require([x["received_total"] for x in rows]==expected and [x["consistent"] for x in rows]==[False,True,True,True],"received variant")
 require(all(x["coefficient"]=="0.0186" and x["url"].startswith("https://") and "RECEIVED" in x["read_grade"] for x in rows),"received scope or URL")
 a=d["textual_calc"];base=Decimal(a["input_twice_pingcha"]);step=Decimal(a["added_licha"]);correct=base+step;received=Decimal(a["ming_shi_received_sum"])
 require((str(base),str(step),str(correct),str(received),str(received-correct))==("4.9200","0.0186",a["correct_sum"],"4.9286",a["ming_shi_difference"]) and a["ming_shi_difference"]=="-0.0100","received arithmetic mismatch")
 require(Decimal(a["mei_wending_solar_dividend"])/Decimal(a["mei_wending_days"])==Decimal(a["mei_wending_quotient"])==step and a["other_three_received_sum"]==a["correct_sum"],"second received method check")
 require(a["interpretation"]=="RECEIVED_ARITHMETIC_INTERNAL_CONSISTENCY_NOT_PROOF_OF_G893_IDENTICAL_FIELD","no transitive unit award")
 p=d["source_local_check"];prior=json.loads((ROOT/p["prior_doc"]).read_text(encoding="utf-8"))
 require(prior["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893" and p["short_first_difference"]==prior["exact_arithmetic"]["short_first_differences"][0]=="0.0186" and p["supported_observed_span"]=="D14-D30","source-local exact stage")
 require(p["same_original_physical_copies"]==1 and p["identical_historical_units"]==p["cross_edition_D16_final"]=="UNPROVEN","false identity")
 w=d["evidence_weight"]
 require(all(w[k]==0 for k in ("new_historical_independent_physical_copies","new_source_registry_entries","new_genealogy_nodes","new_genealogy_edges","new_chart_algorithm_reopens")),"false research votes")
 require(w["original_six_primary_fields"]=="5/6" and w["independent_cross_witness_mechanical_final"]=="0/6" and w["open_research_issues"]==11 and w["manuscript_header_glyph_override"]=="FORBIDDEN" and w["generic_calendar_algorithm_authorization"]=="FORBIDDEN","unsupported historical closure")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 require(issue["status"]=="OPEN" and DOC in issue["source_refs"] and DOC.replace(".json",".md") in issue["source_refs"],"open source review")
 q=issue["g893_12yj_received_arithmetic_text_reviews"]
 require(len(q)==1 and q[0]["evidence_doc"]==DOC and q[0]["received_readings"]==expected and q[0]["internal_discrepancy"]=="-0.0100" and q[0]["unit_bridge"]=="UNPROVEN" and q[0]["external_original_votes_added"]==0,"risk append")
 require(any(z.get("event")=="G893_12YJ_RECEIVED_TEXT_ARITHMETIC_CONFLICT_APPEND" and DOC in z.get("evidence_refs",[]) for z in issue["history"]),"forward-only history")
 require(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,624,0),"handoff sync")
 require(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0 and any(x.startswith("12YJ ") for x in state["historical_audit"]["current_focus"]),"algorithm protected")
 return {"status":"PASS","received_texts":4,"internal_mingshi_discrepancy":"-0.0100","physically_independent_source_votes":0,"G893_target":"5/6","cross_witness_final":"0/6"}
def replay_original(path,d):
 from PIL import Image
 b=Path(path).read_bytes();o=d["source_original"]
 require(len(b)==o["archive_bytes"] and hashlib.sha256(b).hexdigest()==o["archive_sha256"],"ZIP original")
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  require(z.testzip() is None,"CRC")
  report=json.loads(z.read("report.json"));require(report["book_cd"]=="GK00893_00" and len(report["physical_pages"])==204,"source object")
  src=None
  for q in report["physical_pages"]:
   raw=z.read("physical/"+q["page"]+".jpg")
   require(len(raw)==q["bytes"] and hashlib.sha256(raw).hexdigest()==q["sha256"],"204 original JPEG SHA")
   if q["page"]=="001a":src=raw
  require(hashlib.sha256(src).hexdigest()==o["page_sha256"],"001a SHA")
  rgb=Image.open(io.BytesIO(src)).convert("RGB")
  require(hashlib.sha256(rgb.crop(tuple(o["original_rgb_roi"]["rect"])).tobytes()).hexdigest()==o["original_rgb_roi"]["sha256"],"native source ROI")
 return {"status":"PASS","source_original_page_sha_count":204,"original_header_pixel_sha":"MATCH"}
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--archive");args=parser.parse_args()
 d,*other=load();print(json.dumps(verify(d,*other),ensure_ascii=False))
 if args.archive:print(json.dumps(replay_original(args.archive,d),ensure_ascii=False))
