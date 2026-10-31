#!/usr/bin/env python3
"""13MP: fail-closed original archive replay. No archive -> metadata only."""
from pathlib import Path
from io import BytesIO
import argparse,hashlib,json,re,zipfile
from decimal import Decimal
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13MO-G893-ZHOU1569-PAIRED-LANE-SOURCE-COMPARISON-R1.json"
P=R/"docs/research/TIANWEN-13MP-G893-1569-ARCHIVE-PIXEL-REPLAY-AND-CROSSSOURCE-SCOPE-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
ZIP_SHA="1d8f10da7c27411bf38ad635494a1b9f4e700fb76cb37b2a7541c075a0ca9835"
FILE_SHA={
 "G893-001a.jpg":"8b07513ca8aad42ae167a93f22c39f14850c8cd1c345db9ce98c1e0e769226a5",
 "G893-002b.jpg":"f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55",
 "zhouxiang-1569-vol6-original.pdf":"4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c"}
def digest(b):return hashlib.sha256(b).hexdigest()
def check(e,p,s,l):
 assert e["schema"]=="TIANWEN-13MO-G893-ZHOU1569-PAIRED-LANE-SOURCE-COMPARISON-R1"
 assert p["schema"]=="TIANWEN-13MP-G893-1569-ARCHIVE-PIXEL-REPLAY-AND-CROSSSOURCE-SCOPE-R1"
 assert p["issue_id"]==e["issue_id"]=="TW-OPEN-0005"
 assert e["archive"]["zip_sha256"]==p["archived_original"]["zip_sha256"]==ZIP_SHA
 assert e["archive"]["new_physical_copy"] is False and e["archive"]["ocr"] is False
 assert p["archived_original"]["verified_no_ocr"] is True
 assert {x["filename"]:x["sha256"] for x in p["archived_original"]["source_files"]}==FILE_SHA
 assert e["g893"]["header_jpeg_sha256"]==FILE_SHA["G893-001a.jpg"]
 assert e["g893"]["jpeg_sha256"]==FILE_SHA["G893-002b.jpg"]
 assert e["zhou1569"]["pdf_sha256"]==FILE_SHA["zhouxiang-1569-vol6-original.pdf"]
 assert e["g893"]["header_minor_unit_glyph"]==p["source_field_scope"]["g893_source_original_001a_minor_glyph"]=="少"
 assert p["source_field_scope"]["zhou1569_other_column_field_identity_to_g893_long"]=="NOT_PROVEN"
 assert p["source_field_scope"]["zhou1569_other_column_normalized_values_claimed_equal_to_g893_long"] is False
 assert p["source_field_scope"]["zhou1569_p15_short_numeric_strings_match_g893"] is True
 assert p["source_field_scope"]["original_impression_independence_and_lineage"]=="UNRESOLVED"
 rows=e["paired_column_transcriptions"]
 assert [(v["day"],v["short"],v["long"]) for v in rows]==[(15,"5.2176","434.8249"),(16,"5.2362","429.6073"),(17,"5.2548","424.3711")]
 sh=[Decimal(v["short"]) for v in rows];lo=[Decimal(v["long"]) for v in rows]
 assert sh[1]-sh[0]==sh[2]-sh[1]==Decimal("0.0186")
 assert lo[0]-sh[0]==lo[1] and lo[1]-sh[1]==lo[2]
 assert len(e["g893"]["bounded_native_rgb_crops"])==3
 assert len(e["zhou1569"]["bounded_native_rgb_crops"])==2
 for c in e["g893"]["bounded_native_rgb_crops"]+e["zhou1569"]["bounded_native_rgb_crops"]:
  assert re.fullmatch(r"[0-9a-f]{64}",c["rgb_sha256"])
  x0,y0,x1,y1=c["box"];assert min(x0,y0)>=0 and x1>x0 and y1>y0
 assert p["archived_original"]["native_rgb_crop_count"]==5
 for k in ("historical_cross_original_six_winners","source_registry_delta","physical_copy_delta","matrix_delta","graph_node_delta","graph_edge_delta","algorithm_reopen"):
  assert p["invariants"][k]==0
 assert p["invariants"]["deterministic_product"]=="CLOSED"
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,978,0)
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 focus=s["historical_audit"]["current_focus"]
 assert any(x.startswith("13MP ") for x in focus) and any(x.startswith("13MO ") for x in focus)
 assert l["binding"]["source_focus_count"]==len(focus)
 assert l["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0]
 issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert str(P.relative_to(R)) in issue["source_refs"]
 assert any(x["revision_id"]=="TW-OPEN-0005-13MP-PIXEL-REPLAY-20261031" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13MP-G893-PIXEL-REPLAY-20261031" for x in l["checkpoint_log"])
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return {"status":"PASS","source_image_hash_replay":"NOT_EXECUTED_WITHOUT_ARCHIVE"}
def replay(e,source_archive):
 from PIL import Image
 import fitz
 raw=Path(source_archive).read_bytes()
 assert digest(raw)==ZIP_SHA,"Source archive SHA mismatch"
 with zipfile.ZipFile(BytesIO(raw)) as z:
  assert z.testzip() is None,"Source archive CRC failed"
  files={name:z.read(name) for name in FILE_SHA}
 assert {name:digest(content) for name,content in files.items()}==FILE_SHA
 def crop(image,c):
  x0,y0,x1,y1=c["box"]
  assert x1<=image.width and y1<=image.height
  assert digest(image.crop((x0,y0,x1,y1)).tobytes())==c["rgb_sha256"]
 images={n:Image.open(BytesIO(files[n])).convert("RGB") for n in ["G893-001a.jpg","G893-002b.jpg"]}
 assert all(im.size==(1150,2000) for im in images.values())
 for c in e["g893"]["bounded_native_rgb_crops"]:crop(images["G893-"+c["page"]+".jpg"],c)
 pdf=fitz.open(stream=files["zhouxiang-1569-vol6-original.pdf"],filetype="pdf")
 assert len(pdf)==45
 for c in e["zhou1569"]["bounded_native_rgb_crops"]:
  pix=pdf[c["page"]-1].get_pixmap(matrix=fitz.Matrix(2.5,2.5),colorspace=fitz.csRGB,alpha=False)
  im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
  assert im.size==(2105,1489)
  crop(im,c)
 return {"status":"PASS","source_image_hash_replay":"PASS","native_rgb_crops_verified":5,"source_files_verified":3,"new_physical_copy_votes":0,"historical_cross_original_six_winners":0}
if __name__=="__main__":
 ap=argparse.ArgumentParser()
 ap.add_argument("--source-archive",type=Path)
 args=ap.parse_args()
 data=[json.loads(f.read_text("utf-8")) for f in [E,P,S,L]]
 result=check(*data)
 if args.source_archive:result=replay(data[0],args.source_archive)
 print(json.dumps(result,ensure_ascii=False))
