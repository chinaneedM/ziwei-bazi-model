#!/usr/bin/env python3
"""Bounded official NCL bibliographic CSV probe: no item or glyph is presumed."""
import csv, hashlib, io, json, os, re, urllib.request, urllib.error
from pathlib import Path
URL="https://rbook.ncl.edu.tw/NCLSearch/rbook.csv"
DEST=Path(os.environ.get("TIANWEN_13GI_OUTPUT","/tmp/tianwen-13gi-catalog-result.json"))
MAX_BYTES=80_000_000
def is_exact_book_number(value):
 return "".join(value.split()) in ("03130","20803130")
def main():
 result={"schema":"TIANWEN-13GI-NCL-OFFICIAL-CSV-PROBE-RESULT-R1","url":URL,"status":"ACCESS_OR_PARSE_INCOMPLETE","status_detail":None,"http_status":None,"source_bytes_sha256":None,"source_size":None,"decoding":None,"headers":[],"rows_checked":None,"candidate_rows":[],"exact_book_number_rows":[],"negative_absence_certified":False,"item_folio_or_glyph_certified":False}
 try:
  req=urllib.request.Request(URL,headers={"User-Agent":"TianwenHistoricalSourceAudit/1.0 (public bibliography only)","Accept":"text/csv,text/plain,*/*"})
  with urllib.request.urlopen(req,timeout=90) as resp:
   result["http_status"]=resp.status
   raw=resp.read(MAX_BYTES+1)
  result["source_size"]=len(raw)
  if len(raw)>MAX_BYTES:
   raise ValueError("CSV_EXCEEDS_BOUNDED_80MB_DOWNLOAD")
  result["source_bytes_sha256"]=hashlib.sha256(raw).hexdigest()
  parsed=None
  for enc in ("utf-8-sig","utf-16","cp950","big5"):
   try:
    text=raw.decode(enc)
    if "<html" in text[:150].lower() or not ("," in text[:12000] or "\t" in text[:12000]):
     continue
    parsed=(enc,text)
    break
   except UnicodeError:pass
  if parsed is None:raise ValueError("NO_CONFIDENT_CSV_DECODE_OR_HTML_RESPONSE")
  enc,text=parsed
  result["decoding"]=enc
  # The provider may use a tab-delimited text export despite CSV extension.
  dialect=csv.excel_tab if text[:10000].count("\t")>text[:10000].count(",") else csv.excel
  rows=csv.reader(io.StringIO(text),dialect=dialect)
  header=next(rows)
  result["headers"]=header[:80]
  col_names=[str(x).replace(" ","").replace("\ufeff","") for x in header]
  index=[i for i,h in enumerate(col_names) if any(x in h for x in ("書號","索書號","正題名","題名","版本","作者"))]
  result["core_column_indices"]=index
  exact_indices=[i for i,h in enumerate(col_names) if "索書號" in h or h=="書號"]
  result["book_number_columns"]=exact_indices
  count=0
  for row in rows:
   count+=1
   if count>400000:raise ValueError("CSV_EXCEEDS_400000_ROWS")
   if not row:continue
   joined=" ".join(row)
   # Fuzzy match is a lead, never stronger than an exact recognized book-number column.
   exact=any(i<len(row) and is_exact_book_number(row[i]) for i in exact_indices)
   candidate=bool(re.search(r"(?<![0-9])0?3130(?![0-9])",joined))
   if exact or candidate:
    values={header[i]:row[i][:300] for i in index if i<len(row)}
    obj={"csv_row_1based":count+1,"bibliographic_fields":values,"exact_book_number_column":exact}
    if exact and len(result["exact_book_number_rows"])<20:result["exact_book_number_rows"].append(obj)
    if candidate and len(result["candidate_rows"])<20:result["candidate_rows"].append(obj)
  result["rows_checked"]=count
  result["status"]="CSV_RETRIEVED_PARSED_REPORT_ONLY"
  result["status_detail"]="Exact matches require original row, column, SHA and firstparty detail follow-up; absence here is not historic nonexistence."
 except Exception as exc:
  result["status_detail"]=str(type(exc).__name__)+": "+str(exc)[:500]
 DEST.parent.mkdir(parents=True,exist_ok=True)
 DEST.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,ensure_ascii=False,sort_keys=True))
if __name__=="__main__":main()
