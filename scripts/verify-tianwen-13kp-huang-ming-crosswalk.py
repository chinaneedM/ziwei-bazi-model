#!/usr/bin/env python3
"""13KP two direct original images and conditional index-alignment firewall."""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KP-HUANG-MING-83-84-167-168-DIRECT-ORIGINAL-CROSSWALK-R1.json"
def fail(p,msg):
 if not p:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def verify(e,state,ledger,huang_pdf=None,ming_pdf=None):
 fail(e["schema"]=="TIANWEN-13KP-HUANG-MING-DIRECT-ORIGINAL-CROSSWALK-R1","schema")
 h=e["sources"]["huang"];m=e["sources"]["ming"]
 fail(h["source_pdf_sha256"]=="c524693e7bad502d222a1444d688cc7d63ca4a4037d7d4e08cee4aa94f9adbae" and h["page_1_based"]==80,"Huang source")
 fail(m["source_pdf_sha256"]=="dde1bfd5d3cf15954ddc6dbf1c020971806038bbc7f737b9053d5643e5c7c264" and m["source_pdf_bytes"]==46883051 and m["pdf_pages"]==52 and m["page_1_based"]==11,"Ming source")
 fail(h["roi_xyxy"]==[605,165,915,944] and h["roi_rgb_sha256"]=="920bfa8ab658e9782bb3526474d24a4ff44e36114d137c11a214107f3a429c5a","Huang 167 source")
 fail(m["page_size_rgb"]==[2070,1786] and m["page_rgb_sha256"]=="55afb1634fb5558e4db1a7de7c1b6b180e6b35094fddc39ea3c1cd615820de7e","Ming original page")
 fail(m["roi_xyxy"]==[1075,260,1805,1710] and m["roi_rgb_sha256"]=="48c692ba9202e12303e472e81e3e53f4653f538eac9b4106c0e9cb0fe131f67f","Ming original ROI")
 fail(h["original_glyphs"]==["在八十三限已下者不減為初限","已上者置一百六十七限以所得限減之餘為末限"],"Huang exact reading")
 fail(m["original_glyphs"]==["凡求遲疾皆以入曆日乘十二限二十分","以在八十四限已下為初","已上轉減一百六十八限餘為末"],"Ming exact reading")
 fail(h["original_page_positive"] is True and m["original_page_positive"] is True,"original positive")
 a=e["counterfactual"];fail(a["domain_h"]==[0,167] and a["domain_m"]==[1,168] and a["mapping"]=="m=h+1" and a["huang_initial_guard"]=="h<=83" and a["ming_initial_guard"]=="m<=84" and a["huang_terminal_rule"]=="167-h" and a["ming_terminal_rule"]=="168-m","conditional indexing")
 fail(a["initial_cardinality"]==84 and a["terminal_cardinality"]==84 and a["synthetic_index_test_not_historical_limit_tables"] is True,"conditional model is not history")
 samples=[]
 for i in range(168):
  j=i+1;hval=i if i<=83 else 167-i;mval=j if j<=84 else 168-j
  sample={"huang_h":i,"ming_m":j,"region":"INITIAL" if i<=83 else "TERMINAL","huang_scoped_value":hval,"ming_scoped_value":mval,"ming_minus_huang":mval-hval}
  if i in [0,1,82,83,84,85,166,167]:samples.append(sample)
  fail((mval-hval)==(1 if i<=83 else 0),"piecewise difference")
 fail(a["samples"]==samples,"eight explicit boundary samples")
 b=e["mathematical_boundaries"]
 fail(all(b[k] is True for k in ("first_partition_alignment_under_shift","terminal_mirror_values_equal_under_shift")),"proven only two relations")
 fail(all(b[k] is False for k in ("initial_branch_values_equal_under_shift","source_已上_ambiguity_at_boundary_explicitly_resolved","historically_adopted_index_base_proven","historical_full_formula_equivalence_proven")),"unproven full mechanism")
 fail(b["initial_branch_delta_ming_minus_huang"]==1 and b["terminal_branch_delta_ming_minus_huang"]==0,"nonidentity")
 c=e["source_boundaries"]
 fail(c["new_source_registry_entries"]==0 and c["new_graph_nodes"]==0 and c["new_graph_edges"]==0 and c["verified_g893_six_variant_winners"]==0 and c["algorithm_reopens"]==0 and c["open_risks"]==11 and c["product"]=="CLOSED","do not invent original award")
 for k in ("verified_exact_independent_physical_impressions","huang_next_day_vs_ming_next_limit_equivalence_proven","physical_shanghai_item_authenticated","ming_source_specific_impression_date_authenticated"):fail(c[k] is False,k)
 astate=state["historical_audit"];binding=ledger["binding"]
 fail(state["schema_version"]==astate["research_omission_guard"]["reviewed_state_version"]==binding["reviewed_state_version"],"version")
 fail(len(astate["current_focus"])==binding["source_focus_count"] and astate["current_focus"][-1].startswith(binding["latest_research_focus_prefix"]+" "),"focus")
 fail(astate["external_source_registry_total_unique_count"]==765 and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"stable product")
 issue=next(k for k in ledger["issues"] if k["id"]==e["issue_id"])
 fail(issue["priority"]=="P0" and issue["status"]=="OPEN" and E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"],"issue")
 fail(any(x.get("revision_id")=="TW-OPEN-0005-13KP-HUANG-MING-INDEX-20261029" and E in x.get("evidence_refs",[]) for x in issue["history"]),"append-only revision")
 fail(len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],"risk review")
 if huang_pdf or ming_pdf:
  import fitz
  from PIL import Image
  for p,src in ((huang_pdf,h),(ming_pdf,m)):
   if not p:continue
   raw=Path(p).read_bytes();fail(digest(raw)==src["source_pdf_sha256"],"source PDF bytes")
   d=fitz.open(stream=raw,filetype="pdf");page=d[src["page_1_based"]-1]
   factor=1.25 if src is h else 1.15
   pix=page.get_pixmap(matrix=fitz.Matrix(factor,factor),colorspace=fitz.csRGB,alpha=False)
   image=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
   fail(list(image.size)==src["page_size_rgb"] and digest(image.tobytes())==src["page_rgb_sha256"],"RGB page")
   fail(digest(image.crop(src["roi_xyxy"]).tobytes())==src["roi_rgb_sha256"],"RGB source ROI")
   d.close()
 return {"status":"PASS","original_source_regions":2,"conditional_points_checked":168,"initial_difference":1,"terminal_difference":0,"winners":0,"algorithm_reopens":0,"pixels_replayed":bool(huang_pdf or ming_pdf)}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--huang-pdf",type=Path);p.add_argument("--ming-pdf",type=Path);args=p.parse_args()
 print(json.dumps(verify(*load(),huang_pdf=args.huang_pdf,ming_pdf=args.ming_pdf),ensure_ascii=False))
