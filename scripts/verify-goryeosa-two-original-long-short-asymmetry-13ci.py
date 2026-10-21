#!/usr/bin/env python3
"""13CI: first-party original D16-D18 two-copy long/short negative-control."""
import argparse, hashlib, io, json, zipfile
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CI-GORYEOSA-D16-D18-TWO-ORIGINAL-LONG-SHORT-ASYMMETRY-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
KEYS=[["NAJ17",16,"LONG"],["NAJ17",16,"SHORT"],["NAJ17",17,"LONG"],["NAJ17",17,"SHORT"],["NAJ18",18,"LONG"],["W23",16,"LONG"],["W23",16,"SHORT"],["W23",17,"LONG"],["W23",17,"SHORT"],["W23",18,"LONG"]]
DIGESTS=["11078a97de2fdad111372f4e4e9bd7a89c21d166742a59b74686e537506e76a7","da64b48ce26b2bf127bad6c1866e9934c19c7d030e9aa46701a8a5f15980530d","1726510e8bee586529972678b2c39f1c7756800f1d6f271c6976af4cbdaa2b1f","a2dbae06ed5747da9e93a66dc55173a150b33bd3e495bb3d25341dbc0b8f561b","ffa1d5bf1b98c058c9d730f3eeb2c776b9a5a76a3cc76c040c5896b226eb5b36","72008b56d7ea8ebde8804d0648f3e7934c0e98838a45b0cc1ca25a5c0f4fba5d","78648fd810f726f4cb42eb50bf9dfd95841bc5d20dd73196b165994f0f66e443","b4c061d08bf03b4d1909b529628427103ea16220a801b24a6d277c6854e90739","8e33787e6c5cc15259acf1ea3c802e9c0c52282eda1cde016b7adfe98dc0450d","d4c555e6445f5c7de9c5e15ad697bbdbf7accc1469b979af22ace692124c2772"]
SOURCE_SHA={"NAJ17":"8362e8a2b8ddf5f36408d4450a81ebad2d9548b32f49dbe37e01493592b7c3e9","NAJ18":"88cecf62c8cd0dd623199eb06e3044efbe61771c1ffe058b8e7a87cc2f8f88cc","W23":"388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66"}
PRIOR={"atlas13CH":{"path":"docs/research/TIANWEN-13CH-GORYEOSA-TWO-HOLDING-D01-D20-ORIGINAL-HEADING-ATLAS-R1.json","sha":"597ce1e7cd72acf54a82f4c662f34848b353a81c"},"D16_17_13BE":{"path":"docs/research/TIANWEN-13BE-GORYEOSA-D16-ORIGINAL-LONG-LANE-DUAL-COPY-COLLATION-R1.json","sha":"603b63097bc24c8ef958b22f4b1999e85fa3d908"},"W_d16_13BS":{"path":"docs/research/TIANWEN-13BS-GORYEOSA-WASEDA-D16-NAJ-D18-D19-SOURCE-NATIVE-GLYPH-COLLATION-R1.json","sha":"77379611cc58fcd6d516e50e29e6cb25dc8d1775"},"W_d18_13BO":{"path":"docs/research/TIANWEN-13BO-GORYEOSA-WASEDA-P23-D17-D18-ORIGINAL-HEADER-CUMULATIVE-LONG-R1.json","sha":"e4115ce8d121c976bd9866b2307bb7662e09fc4d"}}

def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def prior_sha(e):
 assert e["prior_source_git_blobs"]==PRIOR
 out={}
 for key,v in PRIOR.items():
  data=(ROOT/v["path"]).read_bytes()
  blob=b"blob "+str(len(data)).encode("ascii")+bytes([0])+data
  assert hashlib.sha1(blob).hexdigest()==v["sha"],key
  out[key]=json.loads(data)
 return out

def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CI-TWO-COPY-D16-D18-LONG-SHORT-LOCAL-ASYMMETRY-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and "NO_OCR" in e["grade"]
 assert list(e["sources"])==["NAJ17","NAJ18","W23"]
 assert {k:v["image_sha256"] for k,v in e["sources"].items()}==SOURCE_SHA
 a=e["rois"]
 assert len(a)==10
 assert [(x["source"],x["printed_day"],x["field"]) for x in a]==[tuple(k) for k in KEYS]
 assert [x["rgb_sha256"] for x in a]==DIGESTS
 assert len(set(x["rgb_sha256"] for x in a))==10
 assert e["sources"]["NAJ17"]["zip_sha256"]==e["sources"]["NAJ18"]["zip_sha256"]
 for x in a:
  w,h=e["sources"][x["source"]]["dimensions"];left,top,right,bottom=x["bbox"]
  assert 0<=left<right<=w and 0<=top<bottom<=h
  assert len(x["rgb_sha256"])==64
 expected={16:{"LONG":("429.6073","四百二十九六〇七三"),"SHORT":("5.1362","五分一三六二")},
           17:{"LONG":("424.3711","四百二十四三七一一"),"SHORT":("5.2548","五分二五四八")},
           18:{"LONG":("419.1163","四百一十九一一六三")}}
 for x in a:
  assert (x["decimal"],x["original"])==expected[x["printed_day"]][x["field"]]
 for day in (16,17,18):
  vals=[x["decimal"] for x in a if x["printed_day"]==day and x["field"]=="LONG"]
  assert len(vals)==2 and len(set(vals))==1
 for day in (16,17):
  vals=[x["decimal"] for x in a if x["printed_day"]==day and x["field"]=="SHORT"]
  assert len(vals)==2 and len(set(vals))==1
 a0=e["local_exact_arithmetic"]
 L16=Decimal(a0["original_D16_long"]);L17=Decimal(a0["original_D17_long"]);L18=Decimal(a0["original_D18_long"])
 S16=Decimal(a0["source_printed_D16_short"]);S17=Decimal(a0["source_printed_D17_short"])
 assert L16-L17==Decimal(a0["long_D16_minus_D17"])==Decimal("5.2362")
 assert L17-L18==Decimal(a0["long_D17_minus_D18"])==S17==Decimal("5.2548")
 assert L16-L17-S16==Decimal(a0["first_edge_minus_D16_printed_short"])==Decimal("0.1000")
 assert S16==Decimal("5.1362")
 assert a0["edge16_equals_printed_short16"] is False and a0["edge17_equals_printed_short17"] is True
 assert a0["not_a_unique_historical_typographical_error_diagnosis"] is True
 assert a0["cannot_emend_D16_original_from_subtraction"] is True
 assert a0["historical_mechanical_rule_generalization"]=="UNPROVEN"
 b=e["source_boundaries"]
 assert b["D16_short_original_in_both"]=="五分一三六二" and b["D17_short_original_in_both"]=="五分二五四八"
 assert b["W_D16_same_day_yingsuoji"]==b["NAJ_D17_same_day_yingsuoji"]=="UNBOUND"
 assert b["G893_Ming1569_unit_equivalence"]=="UNPROVEN"
 assert b["historical_D16_one_vs_two_ancestral_winner"]=="UNRESOLVED"
 t=e["new_evidence_scope"]
 assert t["previously_published_identical_tight_roi_signatures"]==4 and t["new_tight_rgb_roi_signatures"]==6
 assert t["reviewed_source_jpeg_objects"]==3 and t["open_issues"]==11 and t["product"]=="CLOSED"
 for k in ("new_provider_jpeg_objects","new_physical_historical_witnesses","new_registry_entries","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","new_independent_stemmatic_votes","algorithm_reopens"):assert t[k]==0
 z=s["historical_audit"]
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 assert z["row_count"]==z["audited_row_count"]==222 and z["external_source_registry_total_unique_count"]==754
 assert any(x.startswith("13CI ") for x in z["current_focus"])
 assert l["binding"]["reviewed_state_version"]==s["schema_version"] and l["binding"]["source_focus_count"]==len(z["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert any(r.get("revision_id")=="TW-OPEN-0005-D16-18-LONG-SHORT-13CI" for r in issue["history"])
 assert any(x["id"]=="OMISSIONS-13CI-D16D18-LONGSHORT-20261022" for x in l["checkpoint_log"])
 assert len([x for x in l["issues"] if x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS")])==11
 return True

def replay(e,naj_zip,waseda_zip):
 from PIL import Image
 archives={"NAJ17":naj_zip,"NAJ18":naj_zip,"W23":waseda_zip}
 for key in ("NAJ17","NAJ18","W23"):
  meta=e["sources"][key]
  data=Path(archives[key]).read_bytes()
  assert hashlib.sha256(data).hexdigest()==meta["zip_sha256"],key
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   assert z.testzip() is None
   src=z.read(meta["jpeg"])
  assert hashlib.sha256(src).hexdigest()==meta["image_sha256"],key
  im=Image.open(io.BytesIO(src)).convert("RGB")
  assert list(im.size)==meta["dimensions"]
  for r in e["rois"]:
   if r["source"]!=key:continue
   actual=hashlib.sha256(im.crop(tuple(r["bbox"])).tobytes()).hexdigest()
   assert actual==r["rgb_sha256"],(key,r["printed_day"],r["field"],actual)
 return True

if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--naj-zip");p.add_argument("--waseda-zip");q=p.parse_args()
 e=load(E)
 assert check(e,load(S),load(L))
 assert prior_sha(e)
 if bool(q.naj_zip)!=bool(q.waseda_zip):p.error("both exact source ZIPs required")
 if q.naj_zip:assert replay(e,q.naj_zip,q.waseda_zip)
 print("TIANWEN_13CI_ORIGINAL_D16_D18_LONG_SHORT=PASS")
