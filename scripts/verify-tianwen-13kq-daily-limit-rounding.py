#!/usr/bin/env python3
"""13KQ original 820 unit arithmetic and conditional rounding, never select index base."""
import argparse,hashlib,json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KQ-HUANG-MING-820-DAILY-LIMIT-ROUNDING-R1.json"
def require(p,m):
 if not p:raise ValueError(m)
def hashbytes(b):return hashlib.sha256(b).hexdigest()
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def verify(e,state,ledger,huang_pdf=None,ming_pdf=None):
 require(e["schema"]=="TIANWEN-13KQ-HUANG-MING-820-DAILY-LIMIT-ROUNDING-R1","schema")
 source=e["sources"];h=source["huang_p75"];m=source["ming_p12"]
 require(h["pdf_sha256"]=="c524693e7bad502d222a1444d688cc7d63ca4a4037d7d4e08cee4aa94f9adbae" and m["pdf_sha256"]=="dde1bfd5d3cf15954ddc6dbf1c020971806038bbc7f737b9053d5643e5c7c264","source originals")
 require(h["pdf_page"]==75 and h["page_size_rgb"]==[1161,969] and h["page_rgb_sha256"]=="d0598899732f5a76c89eb43454d912d3242832e88d9ffc64fd557db661cb5f69","huang page")
 require(h["roi_xyxy"]==[735,105,1140,910] and h["roi_rgb_sha256"]=="09b9ceff44a4beee73ca0e3c0fd465ca4887e99934443831294ede26d5f9c104","huang ROI")
 require(m["pdf_page"]==12 and m["page_size_rgb"]==[2070,1804] and m["page_rgb_sha256"]=="9e2efc909ef20b1d8682a30474e33d438bcaa6c91914c5116791e2394c9967ef","ming page")
 require(m["roi_xyxy"]==[1090,245,1520,1690] and m["roi_rgb_sha256"]=="26bf9a667db927fe2cae6124427c41a4ad95c9a593cd820eec5db216f666280a","ming ROI")
 require(h["positive_phrases"]==["日法萬分以八百二十分為一限","一日得十二限餘一百六十分今就整為二十分"],"huang text")
 require(m["positive_phrases"]==["以八百二十分為一限日率","累加八百二十分為每限日率"],"ming text")
 require(h["physical_impression_authenticated"] is False and m["physical_impression_authenticated"] is False,"physical evidence gate")
 x=e["exact_arithmetic"]
 require(x["daily_base_units"]==10000 and x["limit_base_units"]==820 and x["whole_limits"]==12 and x["remaining_units"]==160,"original units")
 require(10000==12*820+160,"one day exact decomposition")
 actual=Fraction(10000,820);approx=Fraction(61,5);diff=approx-actual
 require(actual==Fraction(500,41) and diff==Fraction(1,205) and 820*diff==4,"exact rational diagnostics")
 require(x["exact_fractional_limit"]=="8/41" and x["rounded_fractional_limit"]=="1/5" and x["exact_daily_limits"]=="500/41" and x["approximated_daily_limits"]=="61/5" and x["approximation_surplus_limits_per_day"]=="1/205" and x["approximation_surplus_base_units_per_day"]==4,"recorded quantities")
 require(x["hundredth_interpretation"]=="CONDITIONAL_DECIMAL_INTERPRETATION_OF_二十分","historic interpretation not forced")
 expected=[{"days":n,"delta_limit_fraction":str(n)+"/205","delta_time_units_fraction":str(n*4)+"/1"} for n in (1,7,14,27)]
 require(x["controls"]==expected,"all rational controls")
 require(28*diff < 1 and "threshold" in x["interval_warning"],"sub-limit error not sufficient to rule out branch crossing")
 b=e["negative_boundaries"]
 for k in ("full_huang_ming_time_to_limit_equivalence_proven","integer_83_84_boundary_reconciled","historic_index_base_selected","rounding_was_the_only_source_of_one_limit_offset","new_physical_source_or_impression_proven"):require(b[k] is False,"no historical overclaim "+k)
 require(b["same_limit_unit_proven_for_both_direct_image_phrases"] is True and b["ming_source_origin_12limit20fraction_original_positive_from_13kp"] is True,"source positives")
 require(b["historical_g893_six_numeric_winners"]==0 and b["chart_algorithm_reopens"]==0 and b["chart_product"]=="CLOSED","no chart change")
 require(e["registry"]=={"source_total":765,"matrix_rows":222,"graph_nodes":252,"graph_edges":238,"open_issues":11},"ledger count")
 a=state["historical_audit"];review=ledger["binding"]
 require(state["schema_version"]==a["research_omission_guard"]["reviewed_state_version"]==review["reviewed_state_version"],"version")
 require(len(a["current_focus"])==review["source_focus_count"] and a["current_focus"][-1].startswith(review["latest_research_focus_prefix"]+" "),"focus")
 require(a["external_source_registry_total_unique_count"]==765 and state["invariants"]["algorithm_reopen_count"]==0 and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","product")
 issue=next(i for i in ledger["issues"] if i["id"]==e["issue_id"])
 require(issue["priority"]=="P0" and issue["status"]=="OPEN" and E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"],"risk")
 require(any(i.get("revision_id")=="TW-OPEN-0005-13KQ-820-DAY-RATE-20261029" and E in i.get("evidence_refs",[]) for i in issue["history"]),"append-only event")
 require(len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],"checkpoint")
 if huang_pdf or ming_pdf:
  import fitz
  from PIL import Image
  for pdf,s in ((huang_pdf,h),(ming_pdf,m)):
   if not pdf:continue
   raw=Path(pdf).read_bytes();require(hashbytes(raw)==s["pdf_sha256"],"PDF hash")
   doc=fitz.open(stream=raw,filetype="pdf"); factor=1.25 if s is h else 1.15
   pix=doc[s["pdf_page"]-1].get_pixmap(matrix=fitz.Matrix(factor,factor),colorspace=fitz.csRGB,alpha=False)
   im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
   require(list(im.size)==s["page_size_rgb"] and hashbytes(im.tobytes())==s["page_rgb_sha256"],"page pixel hash")
   require(hashbytes(im.crop(s["roi_xyxy"]).tobytes())==s["roi_rgb_sha256"],"ROI pixel hash")
   doc.close()
 return {"status":"PASS","source_positive_regions":2,"exact_daily_rate":"500/41","approx_daily_rate":"61/5","error_per_day":"1/205","historic_winners":0,"algorithm_reopens":0,"pixels_replayed":bool(huang_pdf or ming_pdf)}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--huang-pdf",type=Path);p.add_argument("--ming-pdf",type=Path);a=p.parse_args()
 print(json.dumps(verify(*load(),huang_pdf=a.huang_pdf,ming_pdf=a.ming_pdf),ensure_ascii=False))
