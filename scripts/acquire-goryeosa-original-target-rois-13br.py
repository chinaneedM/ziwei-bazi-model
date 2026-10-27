#!/usr/bin/env python3
"""13BR strictly pinned historical source-image crop acquisition. No OCR or historical glyph inference."""
import argparse,hashlib,io,json,re,urllib.parse,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC="docs/research/TIANWEN-13BR-GORYEOSA-WASEDA-D16-NAJ-D18-D19-BOUNDED-SOURCE-ACQUISITION-R1.json"
MAX_PDF=90_000_000
MAX_MANIFEST=1_000_000
MAX_JPEG=12_000_000
def load_spec():return json.loads((ROOT/SPEC).read_text(encoding="utf-8"))
def sha(raw):return hashlib.sha256(raw).hexdigest()
def allowed_url(url,host):
 p=urllib.parse.urlsplit(url)
 return p.scheme=="https" and p.netloc==host and not p.query and not p.fragment and not p.username and not p.password
def fetch(url,cap,host):
 if not allowed_url(url,host):raise ValueError("unapproved URL")
 req=urllib.request.Request(url,headers={"User-Agent":"Tianwen13BRSourceAcquisition/1.0","Accept":"*/*"})
 with urllib.request.urlopen(req,timeout=100) as response:
  if response.status!=200 or not allowed_url(response.geturl(),host):raise ValueError("unexpected status/redirect")
  length=response.headers.get("Content-Length")
  if length and int(length)>cap:raise ValueError("oversize Content-Length")
  content=response.read(cap+1)
 if len(content)>cap:raise ValueError("download exceeds hard cap")
 return content
def naj_original_url(manifest,canvas=18):
 j=json.loads(manifest)
 sequences=j.get("sequences",[])
 if len(sequences)!=1 or len(sequences[0].get("canvases",[]))!=36:raise ValueError("unexpected NAJ canvas geometry")
 c=sequences[0]["canvases"][canvas-1]
 imgs=c.get("images",[])
 if len(imgs)!=1:raise ValueError("unbounded NAJ image annotation")
 url=imgs[0].get("resource",{}).get("@id","")
 p=urllib.parse.urlsplit(url)
 if not allowed_url(url,"www.digital.archives.go.jp") or not re.fullmatch(r"/api/content/item/da12/C[0-9]+/iiif/M[0-9]+_[0-9]+[.]jp2/full/max/0/native[.]jpg",p.path):
  raise ValueError("non-provider-issued NAJ image")
 return url
def validate_spec(e):
 assert e["schema"]=="TIANWEN-13BR-EXACT-SOURCE-SHA-BOUNDED-ORIGINAL-CANDIDATE-ROI-ACQUISITION-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["no_ocr"] is True
 assert e["d16_original_numeric_claim"]==e["naj_d18_d19_heading_claim"]=="NOT_REVIEWED"
 assert e["source_copy_vote_increment"]==0
 assert len(e["sources"])==2 and [s["id"] for s in e["sources"]]==["waseda","naj"]
 wa,na=e["sources"]
 assert wa["url"]=="https://archive.wul.waseda.ac.jp/kosho/ri06/ri06_02809/ri06_02809_0033/ri06_02809_0033.pdf"
 assert wa["pdf_sha256"]=="28ebfeb34191f45715bc449d27da61fe04fb05eb45e84dd00cf569699f46225f"
 assert wa["page_1based"]==23 and wa["xref"]==70 and wa["dimensions"]==[2592,1728]
 assert wa["image_sha256"]=="388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66"
 assert na["manifest"]=="https://www.digital.archives.go.jp/api/iiif/4898853/manifest.json"
 assert na["manifest_sha256"]=="3f38f52860bd06ca7f4b89cec65a32b8529fcb547ac098548120e8071fe370a1"
 assert na["canvas_1based"]==18 and na["dimensions"]==[3000,2215]
 assert na["image_sha256"]=="88cecf62c8cd0dd623199eb06e3044efbe61771c1ffe058b8e7a87cc2f8f88cc"
 assert len(wa["roi_plan"])==6 and len(na["roi_plan"])==4
 assert len({z["key"] for z in wa["roi_plan"]+na["roi_plan"]})==10
 for s in e["sources"]:
  w,h=s["dimensions"]
  for z in s["roi_plan"]:
   x1,y1,x2,y2=z["bbox"]
   assert 0<=x1<x2<=w and 0<=y1<y2<=h
   assert z["kind"] not in ("GLYPH_READ","SOURCE_POSITIVE")
 assert e["source_scope"]["issues_open_or_blocked"]==11
 assert e["source_scope"]["deterministic_product"]=="CLOSED"
 assert all(e["source_scope"][k]==0 for k in ("source_witnesses","registry_sources_added","matrix_rows_added","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens"))
 return True
def acquire(source,out):
 import fitz
 from PIL import Image,ImageDraw
 if source["id"]=="waseda":
  raw=fetch(source["url"],MAX_PDF,"archive.wul.waseda.ac.jp")
  if not raw.startswith(b"%PDF-") or sha(raw)!=source["pdf_sha256"]:raise ValueError("Waseda PDF SHA/type mismatch")
  with fitz.open(stream=raw,filetype="pdf") as d:
   if d.page_count<source["page_1based"]:raise ValueError("Waseda PDF page missing")
   p=d.load_page(source["page_1based"]-1)
   if source["xref"] not in [z[0] for z in p.get_images(full=True)]:raise ValueError("image xref missing on source page")
   obj=d.extract_image(source["xref"])
   if obj["ext"].lower() not in ("jpeg","jpg"):raise ValueError("unexpected Waseda image type")
   original=obj["image"]
  locator={"pdf_page_1based":source["page_1based"],"xref":source["xref"],"pdf_sha256":sha(raw)}
 else:
  raw=fetch(source["manifest"],MAX_MANIFEST,"www.digital.archives.go.jp")
  if sha(raw)!=source["manifest_sha256"]:raise ValueError("NAJ manifest SHA drift")
  imgurl=naj_original_url(raw,source["canvas_1based"])
  original=fetch(imgurl,MAX_JPEG,"www.digital.archives.go.jp")
  locator={"manifest_sha256":sha(raw),"manifest_canvas_1based":source["canvas_1based"],"image_url":imgurl}
 if len(original)>MAX_JPEG or not original.startswith(bytes.fromhex("ffd8ff")) or sha(original)!=source["image_sha256"]:
  raise ValueError("source original JPEG type/SHA mismatch")
 with Image.open(io.BytesIO(original)) as im:
  rgb=im.convert("RGB");rgb.load()
 if list(rgb.size)!=source["dimensions"]:raise ValueError("source original pixel dimension drift")
 (out/"original-source.jpg").write_bytes(original)
 rows=[]
 for z in source["roi_plan"]:
  box=z["bbox"];crop=rgb.crop(tuple(box))
  filename=z["key"]+".png"
  crop.save(out/filename,format="PNG")
  data=(out/filename).read_bytes()
  rows.append({"key":z["key"],"bbox":box,"kind":z["kind"],"image_file":filename,"image_png_sha256":sha(data),"original_rgb_crop_sha256":sha(crop.tobytes()),"original_dimensions":list(crop.size),"direct_glyph_read":"NOT_REVIEWED"})
 # Context image preserves headings and neighboring columns without silently converting to glyph readings.
 preview=rgb.copy();preview.thumbnail((1700,1700),Image.Resampling.LANCZOS)
 preview.save(out/"original-overview.jpg",quality=88)
 return {"source_image_sha256":sha(original),"image_dimensions":source["dimensions"],"source_locator":locator,"roi_count":len(rows),"rois":rows}
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--source",choices=["waseda","naj"],required=True)
 parser.add_argument("--out",default=None)
 args=parser.parse_args()
 e=load_spec();validate_spec(e)
 source=next(z for z in e["sources"] if z["id"]==args.source)
 out=Path(args.out or ("goryeosa-13br-original-"+args.source))
 out.mkdir(parents=True,exist_ok=True)
 receipt={"schema":"TIANWEN-13BR-ORIGINAL-CANDIDATE-ROI-RECEIPT","source_id":args.source,"source_spec":SPEC,
          "source_witnesses_added":0,"no_ocr":True,"research_glyph_state":"CANDIDATE_ROI_NOT_READ",
          "result":"PENDING","error":None}
 try:
  result=acquire(source,out)
  receipt.update(result);receipt["result"]="ORIGINAL_SHA_VERIFIED_CANDIDATE_ROIS_SAVED"
 except Exception as ex:
  receipt["result"]="SOURCE_ACCESS_OR_INTEGRITY_FAILURE"
  receipt["error"]=type(ex).__name__+": "+str(ex)[:600]
 (out/"receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({k:receipt.get(k) for k in ("schema","source_id","result","error","roi_count","research_glyph_state")},ensure_ascii=False))
 if receipt["result"]!="ORIGINAL_SHA_VERIFIED_CANDIDATE_ROIS_SAVED":raise SystemExit(1)
if __name__=="__main__":main()
