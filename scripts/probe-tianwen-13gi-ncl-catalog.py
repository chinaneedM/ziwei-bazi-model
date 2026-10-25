#!/usr/bin/env python3
"""Bounded official NCL bibliographic CSV probe: no item or glyph is presumed."""
import csv, hashlib, io, json, os, re, urllib.request, urllib.error
from pathlib import Path
URL="https://rbook.ncl.edu.tw/NCLSearch/rbook.csv"
DEST=Path(os.environ.get("TIANWEN_13GI_OUTPUT","/tmp/tianwen-13gi-catalog-result.json"))
MAX_BYTES=80_000_000
def is_exact_book_number(value):
 return "".join(value.split()) in ("03130","20803130")
def parse_csv(raw):
 """Parse only the advertised bibliographic schema; retain exact source fields."""
 if len(raw)>MAX_BYTES:raise ValueError("CSV_EXCEEDS_BOUNDED_80MB_DOWNLOAD")
 expected=["正題名","書號","索書號","作者","版本"]
 for enc in ("utf-8-sig","utf-16","cp950","big5"):
  try:
   decoded=raw.decode(enc)
  except UnicodeError:continue
  if "<html" in decoded[:1000].lower() or "<!doctype html" in decoded[:1000].lower():continue
  dialect=csv.excel_tab if decoded[:10000].count("\t")>decoded[:10000].count(",") else csv.excel
  rows=csv.reader(io.StringIO(decoded,newline=""),dialect=dialect,strict=True)
  try:header=next(rows)
  except (StopIteration,csv.Error):continue
  if [h.strip().lstrip("\ufeff") for h in header]!=expected:continue
  result={"decoding":enc,"headers":header,"core_column_indices":list(range(5)),"book_number_columns":[1,2],"candidate_rows":[],"exact_book_number_rows":[]}
  count=0
  for row in rows:
   count+=1
   if count>400000:raise ValueError("CSV_EXCEEDS_400000_ROWS")
   if not row:continue
   if len(row)!=5:raise ValueError("CSV_ROW_WIDTH_MISMATCH")
   exact=is_exact_book_number(row[1]) or is_exact_book_number(row[2])
   candidate=bool(re.search(r"(?<![0-9])0?3130(?![0-9])"," ".join(row)))
   if exact or candidate:
    obj={"csv_row_1based":count+1,"bibliographic_fields":dict(zip(header,row)),"exact_book_number_column":exact}
    for flag,key in ((exact,"exact_book_number_rows"),(candidate,"candidate_rows")):
     if flag:
      if len(result[key])>=20:raise ValueError("CSV_MATCH_REPORT_LIMIT_EXCEEDED")
      result[key].append(obj)
  result["rows_checked"]=count
  return result
 raise ValueError("NO_CONFIDENT_CSV_DECODE_OR_EXPECTED_HEADER")
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
  result.update(parse_csv(raw))
  # Public bibliography bytes are required to independently replay the report.
  source_path=DEST.with_name("tianwen-13gi-source.csv")
  source_path.parent.mkdir(parents=True,exist_ok=True)
  source_path.write_bytes(raw)
  result["source_archive_file"]=source_path.name
  result["status"]="CSV_RETRIEVED_PARSED_REPORT_ONLY"
  result["status_detail"]="Exact matches require original row, column, SHA and firstparty detail follow-up; absence here is not historic nonexistence."
 except Exception as exc:
  result["status_detail"]=str(type(exc).__name__)+": "+str(exc)[:500]
 DEST.parent.mkdir(parents=True,exist_ok=True)
 DEST.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,ensure_ascii=False,sort_keys=True))
if __name__=="__main__":main()
