#!/usr/bin/env python3
"""12WW source-emitted Tokyo university catalog form JavaScript, no user queries or images."""
import argparse,hashlib,json,re,urllib.parse,urllib.request,urllib.error
from pathlib import Path
SCRIPT_URL="https://kanseki.ioc.u-tokyo.ac.jp/user/js/script.js"
LIMIT=240_000
UA="Tianwen/12WW public first-party JS from officially emitted HTML src, no scraping"
def guard(url=SCRIPT_URL):
 if url!=SCRIPT_URL:raise ValueError("not the original form's own JavaScript src")
 return True
def inspect(body):
 if len(body)>LIMIT:raise ValueError("JS too large")
 text=body.decode("utf-8",errors="replace")
 functions=re.findall(r"function\s+([A-Za-z_$][\w$]*)\s*\(",text)
 target="qadv_ck"
 pos=text.find("function "+target)
 return {
  "schema":"TIANWEN-12WW-TOKYO-KANSEKI-PROVIDER-SCRIPT-FORM-POST-GATE-R1",
  "original_url":SCRIPT_URL,
  "source_bytes":len(body),"source_sha256":hashlib.sha256(body).hexdigest(),
  "provider_function_names":functions[:180],
  "contains_advanced_form_validator":target in functions,
  "qadv_ck_source_excerpt":text[pos:pos+4500] if pos>=0 else None,
  "qadv_ck_excerpt_not_entire_call_graph":True,
  "query_original_juan20_not_executed":True,
  "no_1827_1869_page_images":True,"no_independent_historical_print_vote":True,"ocr":False
 }
def run(output_dir):
 guard();o=Path(output_dir);o.mkdir(parents=True,exist_ok=True)
 try:
  req=urllib.request.Request(SCRIPT_URL,headers={"User-Agent":UA,"Accept":"application/javascript,text/javascript,*/*"})
  with urllib.request.urlopen(req,timeout=35) as r:
   u=urllib.parse.urlparse(r.geturl())
   if u.scheme!="https" or u.hostname!="kanseki.ioc.u-tokyo.ac.jp":raise ValueError("source script host change")
   body=r.read(LIMIT+1)
  s=inspect(body)
  (o/"source-script.js").write_bytes(body)
  (o/"receipt.json").write_text(json.dumps(s,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  print(json.dumps({"status":"SOURCE_SCRIPT_ACQUIRED","sha":s["source_sha256"],"functions":len(s["provider_function_names"]),"validator_found":s["contains_advanced_form_validator"],"original_page_votes":0}))
 except Exception as e:
  (o/"access-error.json").write_text(json.dumps({"status":"SOURCE_JS_ACCESS_BOUNDARY","error":type(e).__name__,"http":getattr(e,"code",None),"votes":0}))
  raise
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--output-dir",default="12ww-tokyo-kanseki-script-output");n=a.parse_args()
 run(n.output_dir)
