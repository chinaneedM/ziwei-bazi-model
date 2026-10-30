#!/usr/bin/env python3
"""Read BSB original verified IIIF metadata ONLY: no guessed sibling IDs, no OCR."""
import hashlib,json,urllib.request,urllib.parse,argparse
from pathlib import Path
MANIFEST="https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11166692/manifest"
EXPECTED="fb28be88c767636c6394926620c112e994f1b0b5d58cf896d4a5edc2919f047c"
def acquire():
 p=urllib.parse.urlsplit(MANIFEST)
 assert p.scheme=="https" and p.hostname=="api.digitale-sammlungen.de"
 req=urllib.request.Request(MANIFEST,headers={"User-Agent":"TIANWEN/13LU source-only metadata collation"})
 with urllib.request.urlopen(req,timeout=35) as r:
  raw=r.read(12000000)
 assert hashlib.sha256(raw).hexdigest()==EXPECTED
 return json.loads(raw.decode("utf8"))
def run(out):
 doc=acquire();sequences=doc.get("sequences",[])
 canvases=sequences[0].get("canvases",[]) if sequences else []
 assert len(canvases)==1880
 keys=["@id","@type","label","description","attribution","license","metadata","related","seeAlso","within","rendering","service","structures","navDate","thumbnail","otherContent","homepage"]
 raw={k:doc[k] for k in keys if k in doc}
 # Explicitly preserve the original labels/relations without autointerpreting HTML.
 # Do not list canvas services as sibling digital objects.
 result={"schema":"TIANWEN-13LU-BSB-SIBLING-RELATION-MANIFEST-ONLY","original_manifest_sha256":EXPECTED,"canvas_count":len(canvases),"fields":raw,
 "top_level_keys":list(doc.keys()),"first_canvas_keys":list(canvases[0].keys()),"last_canvas_keys":list(canvases[-1].keys()),
 "provider_sibling_volume1_id_verified":False,
 "provider_original_juan35_target_verified":False,
 "do_not_guess_numeric_bsb_neighbor":True,
 "no_ocr":True,"historical_witness_votes":0}
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 (out/"manifest-top-metadata.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
 print(json.dumps({"status":"PASS","top_level_keys":result["top_level_keys"],"relation_fields":[k for k in ("related","seeAlso","within","metadata","rendering","service") if k in raw],"metadata_size":len(json.dumps(raw,ensure_ascii=False))},ensure_ascii=False))
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);run(ap.parse_args().out)
