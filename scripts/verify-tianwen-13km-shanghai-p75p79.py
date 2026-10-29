#!/usr/bin/env python3
"""13KM native original P75/79 image-locus positive; no cross-edition winner."""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KM-SHANGHAI-HUANG-P75-P79-DIRECT-ORIGINAL-LIMIT-PRECISION-POLARITY-R1.json"
SOURCE="c524693e7bad502d222a1444d688cc7d63ca4a4037d7d4e08cee4aa94f9adbae"
EXPECT=[
 (75,[1161,969],"d0598899732f5a76c89eb43454d912d3242832e88d9ffc64fd557db661cb5f69",[110,110,440,770],"51cf3da6a6790fb9b6988d7ab30e8c40a152e61d0ae95747b08b602b97882725",["中限一百六十八","初限八十四","周限三百三十六"]),
 (79,[1160,1028],"4dc6c52c353bc28ec8f059030e68f6689952944c64651e1fcb92f13dede8c4de",[785,125,1130,920],"2f57048dbcbeec29c7334cd183b182f172f73c145327aaf25dd68b643f44cdab",["大衍","益加損減"]),
 (79,[1160,1028],"4dc6c52c353bc28ec8f059030e68f6689952944c64651e1fcb92f13dede8c4de",[688,120,935,1005],"7eeac699644fc666e1ee496628408a1dd5e7aa038588d66d2eb6f5be10a705b5",["定立成術","五秒八十一微五十纖"])]
def chk(p,msg):
 if not p:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(e,state,ledger,pdf=None):
 chk(e["schema"]=="TIANWEN-13KM-SHANGHAI-HUANG-P75-P79-DIRECT-ORIGINAL-LIMIT-PRECISION-POLARITY-R1","schema")
 s=e["source"];k=e["interpretation_boundaries"];arr=e["positive_original_image_regions"]
 chk(s["pdf_sha256"]==SOURCE and s["pdf_pages"]==97 and s["pdf_bytes"]==14376480 and s["source_acquisition_artifact_id"]==12890397318,"source")
 chk(s["identified_physical_copy"] is False and s["original_impression_year_proven"] is False,"edition")
 chk(len(arr)==3,"three bounded source ROIs")
 for item,(pn,dim,full,rect,h,glyphs) in zip(arr,EXPECT):
  chk(item["pdf_page"]==pn and item["page_rgb_size"]==dim and item["page_rgb_sha256"]==full and item["rect_px"]==rect and item["rect_rgb_sha256"]==h and item["positive_glyphs"]==glyphs,"original source reading")
 chk(k["gain_loss_glyph_present_in_one_dayanscope_section"] is True and k["huang_source_50xian_full_precision_glyph_positive"] is True and k["source_P75_168_limits_positive"] is True and k["one_digital_object_only"] is True,"scoped positives")
 for x in ["huang_received_益加損減_same_step_as_dayanscope_proven","ancient_cross_version_copying_error_proven","source_167_reverse_index_original_glyph_positive","zero_based_167_and_168_period_semantics_proven","physical_manuscript_or_1923_identity_proven","issue_closed"]:
  chk(k[x] is False,"no false historical promotion:"+x)
 for x in ["new_independent_witnesses","new_source_registry_entries","graph_nodes_delta","graph_edges_delta","g893_six_cross_witness_numeric_winners","chart_algorithm_reopens"]:
  chk(k[x]==0,"no false source/algorithm award:"+x)
 chk(k["chart_product"]=="CLOSED","product")
 h=state["historical_audit"];b=ledger["binding"]
 chk(state["schema_version"]==b["reviewed_state_version"]==h["research_omission_guard"]["reviewed_state_version"],"handoff version")
 chk(b["source_focus_count"]==len(h["current_focus"]) and h["current_focus"][-1].startswith(b["latest_research_focus_prefix"]+" "),"focus")
 chk(h["external_source_registry_total_unique_count"]==765 and state["invariants"]["algorithm_reopen_count"]==0 and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","registry/product")
 issue=next(v for v in ledger["issues"] if v["id"]=="TW-OPEN-0005")
 chk(issue["priority"]=="P0" and issue["status"]=="OPEN" and E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"],"open issue references")
 chk(any(v.get("revision_id")=="TW-OPEN-0005-13KM-P75P79-GLYPHS-20261029" and E in v.get("evidence_refs",[]) for v in issue["history"]),"forward source event")
 chk(len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],"risk checkpoint")
 if pdf is not None:
  import fitz
  from PIL import Image
  raw=Path(pdf).read_bytes()
  chk(sha(raw)==SOURCE and len(raw)==14376480,"source PDF bytes")
  doc=fitz.open(stream=raw,filetype="pdf")
  chk(len(doc)==97,"source pages")
  for item in arr:
   pn=item["pdf_page"];pix=doc[pn-1].get_pixmap(matrix=fitz.Matrix(1.25,1.25),colorspace=fitz.csRGB,alpha=False)
   img=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
   chk(list(img.size)==item["page_rgb_size"] and sha(img.tobytes())==item["page_rgb_sha256"],"page source bytes")
   chk(sha(img.crop(item["rect_px"]).tobytes())==item["rect_rgb_sha256"],"ROI source bytes")
  doc.close()
 return {"status":"PASS","direct_original_positive_regions":3,"pdf_pages":[75,79],"source_registry_delta":0,"cross_edition_winners":0,"pdf_replayed":bool(pdf)}
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in [E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"])
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--pdf",type=Path)
 args=parser.parse_args()
 print(json.dumps(verify(*load(),pdf=args.pdf),ensure_ascii=False))
