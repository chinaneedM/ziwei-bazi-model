#!/usr/bin/env python3
"""13KO source P79/P80 glyph page, edition, and index firewall with optional byte/pixel replay."""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KO-HUANG-P79-P80-ORIGINAL-NEXTDAY-REVERSE167-R1.json"
SRC="c524693e7bad502d222a1444d688cc7d63ca4a4037d7d4e08cee4aa94f9adbae"
P79="4dc6c52c353bc28ec8f059030e68f6689952944c64651e1fcb92f13dede8c4de"
P80="37443f9e73d134cb331c8ecc142d0b1e473f6c8c3fc15123fb9b7ee87e8fea07"
ROWS=[
(79,[1160,1028],P79,[88,170,255,938],"e905b2501b5b54570e84fdb3782a674868945818d1f99e7f2bd41dc00fb223a4",["置損益分以其日平合立差益加","損減之即為次日損益分"],"NEXT_DAY_GAIN_LOSS"),
(79,[1160,1028],P79,[22,170,118,932],"017332a64ce6111122050c17ca64f2c7bcb44af5b0a490f0a806f6a7458b42e0",["以益分積之損分減之便為其下遲疾度"],"SUBSEQUENT_MOON_DEGREE"),
(80,[1161,969],P80,[605,165,915,944],"920bfa8ab658e9782bb3526474d24a4ff44e36114d137c11a214107f3a429c5a",["求損益分術曰置所得限在八十三限已下者不減為初限","已上者置一百六十七限以所得限減之餘為末限"],"SPLIT_83_AND_REVERSE_167")]
def chk(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load():
 return tuple(json.loads((R/p).read_text(encoding="utf-8")) for p in (E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def verify(e,state,ledger,pdf=None):
 chk(e["schema"]=="TIANWEN-13KO-HUANG-ORIGINAL-P79-P80-R1","schema")
 s=e["source"]
 chk(s["pdf_sha256"]==SRC and s["pdf_pages"]==97 and s["pdf_bytes"]==14376480 and s["artifact_id"]==12890397318,"source")
 chk(s["zip_sha256"]=="1328eaca52cf8c692edf397ee76aedad90c8d63bbea1b8bba8ae48772ddd835d","zip identity")
 chk(s["physical_copy_or_impression_authenticated"] is False,"physical copy")
 chk(len(e["original_regions"])==3,"three original ROIs")
 for rec,(pn,dim,full,rect,digest,glyphs,scope) in zip(e['original_regions'],ROWS):
  chk(rec["page"]==pn and rec["size"]==dim and rec["full"]==full,"page identity")
  chk(rec["rect"]==rect and rec["rgb_sha256"]==digest and rec["original"]==glyphs and rec["scope"]==scope,"native glyph region")
 for k in ('next_day_add_gain_subtract_loss','separate_degree_integrator','reversal_167','limit_83_branch','preexisting_limit_168_at_p75'):
  chk(e["original_positives"][k] is True,"direct positive "+k)
 for k in ('physical_edition_identity','zero_based_or_one_based_historic_index','complete_83_84_limit_semantics','huang_ming_same_mechanical_step','ancient_copying_error','independent_second_witness'):
  chk(e["unproven"][k] is True,"preserve unresolved "+k)
 c=e["preserved"]
 chk(c=={"registry_total":765,"matrix_rows":222,"graph_nodes":252,"graph_edges":238,"open_risks":11,"g893_six_historic_numeric_winners":0,"algorithm_reopens":0,"product":"CLOSED"},"no algorithm/source promotion")
 chk(e["ci_recovery"]["fix"].startswith("Change negative test mutation"),"CI fixture")
 a=state["historical_audit"];b=ledger["binding"]
 chk(state["schema_version"]==a["research_omission_guard"]["reviewed_state_version"]==b["reviewed_state_version"],"state version")
 chk(len(a["current_focus"])==b["source_focus_count"] and a["current_focus"][-1].startswith(b["latest_research_focus_prefix"]+" "),"focus")
 chk(a["external_source_registry_total_unique_count"]==765 and state["invariants"]["algorithm_reopen_count"]==0 and state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","invariants")
 issue=next(i for i in ledger["issues"] if i["id"]=="TW-OPEN-0005")
 chk(issue["priority"]=="P0" and issue["status"]=="OPEN" and E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"],"open issue references")
 chk(any(x.get("revision_id")=="TW-OPEN-0005-13KO-HUANG-ORIGINAL-20261029" and E in x.get("evidence_refs",[]) for x in issue["history"]),"append-only issue event")
 chk(len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],"checkpoint")
 if pdf is not None:
  import fitz
  from PIL import Image
  raw=Path(pdf).read_bytes();chk(len(raw)==14376480 and sha(raw)==SRC,"source bytes")
  doc=fitz.open(stream=raw,filetype="pdf");chk(len(doc)==97,"page count")
  for rec in e["original_regions"]:
   pix=doc[rec["page"]-1].get_pixmap(matrix=fitz.Matrix(1.25,1.25),colorspace=fitz.csRGB,alpha=False)
   im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
   chk(list(im.size)==rec["size"] and sha(im.tobytes())==rec["full"],"source RGB")
   chk(sha(im.crop(rec["rect"]).tobytes())==rec["rgb_sha256"],"original ROI RGB")
  doc.close()
 return {"status":"PASS","page_originals":[79,80],"roi_count":3,"original_167":True,"source_independent_physical_witnesses":0,"pdf_replayed":bool(pdf)}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--pdf",type=Path);args=p.parse_args()
 print(json.dumps(verify(*load(),pdf=args.pdf),ensure_ascii=False))
