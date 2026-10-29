#!/usr/bin/env python3
"""13KK: exact original P71 title seam; never awards uncollated lunar mechanism."""
import argparse, hashlib, io, json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KK-HUANG-DATONG-V3-SHOUSHI-V4-ORIGINAL-SEAM-P71-R1.json"
SOURCE="c524693e7bad502d222a1444d688cc7d63ca4a4037d7d4e08cee4aa94f9adbae"
EXPECTED={
 "P71-RIGHT-PREVIOUS-WORK-TERMINUS":("大統曆故卷三終",[685,200,770,490],"e6a0758fb67eb7f603c357bb9539c87db8f6135911722eff474fd3d846cea0ee"),
 "P71-LEFT-NEW-WORK-HEADING":("授時曆故卷四／月離曆",[510,165,575,605],"248b5b6af0e28b499bc61f959ede1c71c93d0c2c194ce07bfc0c59d58d912a73")}
def chk(cond,msg):
 if not cond: raise ValueError(msg)
def dig(b):return hashlib.sha256(b).hexdigest()
def verify(e,state,ledger,pdf=None):
 chk(e["schema"]=="TIANWEN-13KK-HUANG-DATONG-V3-SHOUSHI-V4-ORIGINAL-SEAM-P71-R1","schema")
 d=e["source_identity"];v=e["direct_visual_collation"];s=e["revised_source_scope"]
 chk(e["issue_id"]=="TW-OPEN-0005" and d["source_pdf_sha256"]==SOURCE and d["source_pdf_pages"]==97 and d["source_pdf_bytes"]==14376480 and d["acquisition_artifact_id"]==12890397318,"source identity")
 chk(not d["original_physical_copy_identity_bound"] and not d["ancient_edition_impression_bound"],"edition boundary")
 chk(v["pdf_page_1_based"]==71 and v["zero_based_index"]==70 and v["page_rgb_size_px"]==[1160,1028] and v["page_rgb_sha256"]=="c8b5be0c976d966240403c3d357e9453cd22c69a36c772ef7da0cdad4807160d","page original")
 reviews=v["pixel_roi_reviews"]
 chk(len(reviews)==2 and {x["id"] for x in reviews}==set(EXPECTED),"two original title ROIs")
 for x in reviews:
  literal,rect,h=EXPECTED[x["id"]]
  chk(x["literal"]==literal and x["rect_px"]==rect and x["roi_rgb_sha256"]==h and x["scope"]=="DIRECT_SOURCE_GLYPH_POSITIVE_ONLY","glyph ROI")
 chk(s["volume_four_start_page_mapped"]==71 and s["two_different_adjacent_work_labels_attested"],"volume4 title")
 for k in ("source_compilation_or_rebinding_mechanism_proven","g893_source_algorithm_units_proven","huang_益加損減_original_glyph_proven","huang_五秒八十一微五十纖_original_glyph_proven","huang_一百六十七限_original_glyph_proven","printed_1923_Jiayetang_copy_identity_proven","issue_closed"):
  chk(s[k] is False,"no false promotion: "+k)
 for k in ("new_independent_physical_witnesses","new_source_registry_entries","new_genealogy_nodes","new_genealogy_edges","numeric_variant_winners","algorithm_reopens"):
  chk(s[k]==0,"no unearned award: "+k)
 chk(s["product"]=="CLOSED" and s["previous_13KI_immutable_coverage_snapshot_unchanged"] and s["no_false_absence_in_unevaluated_pages"],"evidence firewall")
 h=state["historical_audit"];b=ledger["binding"]
 chk(state["schema_version"]==b["reviewed_state_version"]==h["research_omission_guard"]["reviewed_state_version"],"handoff version")
 chk(len(h["current_focus"])==b["source_focus_count"] and h["current_focus"][-1].startswith(b["latest_research_focus_prefix"]+" "),"latest focus")
 chk(h["external_source_registry_total_unique_count"]>=765 and h["external_source_registry_total_unique_count"]==h["external_source_registry_root_count"]+h["external_source_registry_extension_count"],"source totals")
 chk(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"algorithm state")
 issue=next(y for y in ledger["issues"] if y["id"]=="TW-OPEN-0005")
 chk(issue["status"]=="OPEN" and issue["priority"]=="P0","P0 open")
 chk(E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"],"source refs")
 chk(any(y.get("revision_id")=="TW-OPEN-0005-13KK-ORIGINAL-P71-SEAM-20261029" for y in issue["history"]),"forward revision")
 chk(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["issues"])==11,"omission review")
 if pdf is not None:
  import fitz
  from PIL import Image
  raw=Path(pdf).read_bytes()
  chk(dig(raw)==SOURCE and len(raw)==14376480,"source PDF SHA")
  doc=fitz.open(stream=raw,filetype="pdf")
  chk(len(doc)==97,"source pages")
  pix=doc[70].get_pixmap(matrix=fitz.Matrix(1.25,1.25),colorspace=fitz.csRGB,alpha=False)
  img=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
  chk(list(img.size)==v["page_rgb_size_px"] and dig(img.tobytes())==v["page_rgb_sha256"],"page native RGB")
  for x in reviews:
   chk(dig(img.crop(x["rect_px"]).tobytes())==x["roi_rgb_sha256"],"original ROI replay")
  doc.close()
 return {"status":"PASS","direct_original_seam_page":71,"direct_glyph_regions":2,"source_registry_delta":0,"lunar_polarity_winners":0,"pdf_replayed":bool(pdf)}
def load():
 return tuple(json.loads((R/q).read_text(encoding="utf-8")) for q in (E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--pdf",type=Path);args=a.parse_args()
 print(json.dumps(verify(*load(),pdf=args.pdf),ensure_ascii=False))
