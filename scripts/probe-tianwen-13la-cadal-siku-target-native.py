#!/usr/bin/env python3
"""13LA: source-original CADAL06056956 selected native pages. Acquisition only; no historical glyph awards."""
from pathlib import Path
import hashlib, json, io, subprocess, urllib.request
from PIL import Image
URL="https://upload.wikimedia.org/wikipedia/commons/3/36/CADAL06056956_%E6%98%8E%E5%8F%B2%C2%B7%E5%8D%B7%E4%B8%89%E5%8D%81%E4%BA%94~%E5%8D%B7%E4%B8%89%E5%8D%81%E5%85%AD.djvu"
SHA1="45fc977d134b07689391907d6671eac3c0b7eedb"
SHA256="98a65bbecf7f07fc8b7dbf3307ae2e2ee8888d0b7c7d841161c944e2ea3b9759"
LENGTH=4528817
PAGES=(2,10,11,12,15,16,17)
OUT=Path("13la-target-native-output")
def require(p,s):
 if not p:raise ValueError(s)
def main():
 request=urllib.request.Request(URL,headers={"User-Agent":"TianwenHistoricalAudit/1.0 (research; +https://github.com/chinaneedM/ziwei-bazi-model)","Accept":"*/*"})
 with urllib.request.urlopen(request,timeout=120) as result: source=result.read()
 require(len(source)==LENGTH,"source size")
 require(hashlib.sha1(source).hexdigest()==SHA1,"source sha1")
 require(hashlib.sha256(source).hexdigest()==SHA256,"source sha256")
 OUT.mkdir(exist_ok=True)
 target=OUT/"original-source.djvu";target.write_bytes(source)
 n=subprocess.run(["djvused",str(target),"-e","n"],capture_output=True,text=True,check=True)
 require(int(n.stdout.strip())==126,"source page count")
 page_rows=[]
 for p in PAGES:
  decoded=subprocess.run(["ddjvu","-format=ppm",f"-page={p}","-scale=100",str(target),"-"],capture_output=True,check=True).stdout
  im=Image.open(io.BytesIO(decoded)).convert("RGB")
  require(600<=im.width<=2500 and 800<=im.height<=3500,"source-native size sanity")
  file=OUT/f"native-p{p:03d}.png";im.save(file,format="PNG")
  page_rows.append({"pdf_page_1based":None,"djvu_page_1based":p,"native_rgb_dimensions":[im.width,im.height],"rgb_sha256":hashlib.sha256(im.tobytes()).hexdigest(),"png_sha256":hashlib.sha256(file.read_bytes()).hexdigest(),"png_bytes":file.stat().st_size,"status":"SOURCE_NATIVE_BYTES_CAPTURED_NOT_YET_HISTORICAL_GLYPH_READ"})
 evidence={"source_file_sha256":SHA256,"source_file_sha1":SHA1,"source_bytes":LENGTH,"full_source_page_count":126,"pages":page_rows,"no_ocr":True,"new_physical_witness_votes":0,"new_historical_winners":0}
 (OUT/"source-native-receipt.json").write_text(json.dumps(evidence,indent=2,ensure_ascii=False),encoding="utf-8")
 print(json.dumps(evidence,ensure_ascii=False))
if __name__=="__main__":main()
