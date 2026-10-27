#!/usr/bin/env python3
"""13CE: source-original D15-D17 separate photographic-leaf geometries."""
import argparse,hashlib,io,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CE-GORYEOSA-ORIGINAL-FOLIO-SEAM-TOPOLOGY-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
DIGESTS=["2ad07b5351f330881b5c8a62d1cada1219d63f214f073269f113441ebd7131f2","90a5f72f18650e0ab269d7599475d031b1de7c6fe39ab4dd2323dd8694b5ce83","7df92391d0232d9b4080a46fc6f1724b37b6d96d0ef74c64e10ac4659ce241ce","a5dbe77e45ea8fe2f123dfc84f53ca5fd599ddad266b5ecd42b83def49ebe292","4574fc5f683f716090d261ad492422225065207f61aa444fcfadd18be7d079aa","7cae726e95e37ea2f6a1f700edd2346ba5222111f21059b7cbe3bddeb2c352fd"]
BOXES=[[750,490,855,820],[590,490,710,820],[420,490,535,820],[1575,350,1680,600],[1400,350,1525,600],[1010,350,1125,600]]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13CE-SOURCE-ORIGINAL-D15-D17-TWO-PHYSICAL-LEAF-TOPOLOGIES-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and "NO_OCR" in e["evidence_grade"]
 rr=e["original_headings"]
 assert [x["rgb_sha256"] for x in rr]==DIGESTS
 assert [x["bbox"] for x in rr]==BOXES
 assert [(x["source"],x["day"],x["literal"],x["leaf"]) for x in rr]==[(n,d,{15:"十五日",16:"十六日",17:"十七日"}[d],leaf) for n,days in (("NAJ",[(15,"LEFT"),(16,"LEFT"),(17,"LEFT")]),("WASEDA",[(15,"RIGHT"),(16,"RIGHT"),(17,"LEFT")])) for d,leaf in days]
 assert all(e["source_local_geometry"].values())
 u=e["unresolved"]
 assert u["NAJ_D17_adjacent_7570_source_technical_C"]=="UNBOUND"
 assert u["WASEDA_D16_independent_yingsuoji"]=="UNBOUND"
 assert u["historical_global_day_shift"]=="UNPROVEN"
 assert u["physical_copy_stemma"]=="UNRESOLVED"
 t=e["new_evidence_scope"]
 assert all(v==0 for k,v in t.items() if k.startswith("new_") and k not in ("new_d15_tight_header_locations",) and type(v) is int)
 assert t["new_d15_tight_header_locations"]==2 and t["previously_known_d16_d17_headings_rebound"]==4
 assert t["product"]=="CLOSED" and t["open_issues"]==11 and t["algorithm_reopens"]==0
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert any(x.startswith("13CE ") for x in s["historical_audit"]["current_focus"])
 assert s["historical_audit"]["external_source_registry_total_unique_count"]==s["historical_audit"]["external_source_registry_root_count"]+s["historical_audit"]["external_source_registry_extension_count"]
 assert l["binding"]["reviewed_state_version"]==s["schema_version"] and l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(x.get("revision_id")=="TW-OPEN-0005-FOLIO-13CE" for x in next(q for q in l["issues"] if q["id"]=="TW-OPEN-0005")["history"])
 assert any(x["id"]=="OMISSIONS-13CE-FOLIO-20261021" for x in l["checkpoint_log"])
 return True
def replay(e,archives):
 from PIL import Image
 for source,path in archives:
  d=e["sources"][source];data=Path(path).read_bytes()
  assert hashlib.sha256(data).hexdigest()==d["archive_zip_sha256"]
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   assert z.testzip() is None
   raw=z.read(d["source_image"])
  assert hashlib.sha256(raw).hexdigest()==d["source_sha256"]
  im=Image.open(io.BytesIO(raw)).convert("RGB")
  assert list(im.size)==d["dimensions"]
  for q in e["original_headings"]:
   if q["source"]==source: assert hashlib.sha256(im.crop(tuple(q["bbox"])).tobytes()).hexdigest()==q["rgb_sha256"]
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--naj-zip");p.add_argument("--waseda-zip");a=p.parse_args()
 e,s,l=load(E),load(S),load(L);check(e,s,l)
 if bool(a.naj_zip)!=bool(a.waseda_zip):p.error("paired firstparty archive ZIPs required")
 if a.naj_zip:replay(e,[("NAJ",a.naj_zip),("WASEDA",a.waseda_zip)])
 print("TIANWEN_13CE_FOLIO_TOPOLOGY=PASS")
