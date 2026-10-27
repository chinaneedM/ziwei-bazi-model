#!/usr/bin/env python3
"""Replay the archived NCL CSV; catalog identity does not certify ancient glyphs."""
import argparse
import base64
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'docs/research/TIANWEN-13GK-NCL03130-ORIGINAL-CSV-BYTE-REPLAY-R1.json'
EXPECTED_SHA='d33512f060122a3ade8cdadd0c2195c3f1996983d83c3c0599e01e8a9c4a9c24'
FIELDS=['正題名','書號','索書號','作者','版本']
VALUES=['高麗史','03130','208 03130','鄭麟趾','清初葉舊鈔光緒間(1644-1735)錢塘丁氏補鈔本']

def load(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def digest(raw):return hashlib.sha256(raw).hexdigest()

def check(e,source=None):
 assert e['schema']=='TIANWEN-13GK-NCL03130-ORIGINAL-CSV-BYTE-REPLAY-R1'
 assert e['grade']=='DIRECT_FIRSTPARTY_CATALOG_CSV_BYTE_REPLAY_NOT_TARGET_FOLIO'
 s=e['source'];t=e['target_record']
 assert s['url']=='https://rbook.ncl.edu.tw/NCLSearch/rbook.csv'
 assert (s['sha256'],s['bytes'],s['encoding'],s['data_records'])==(EXPECTED_SHA,1937091,'cp950',28913)
 assert (t['logical_record_with_header'],t['physical_start_line'],t['physical_end_line'])==(3541,3633,3633)
 assert t['fields']==dict(zip(FIELDS,VALUES))
 fragments=[]
 for key,expected in (('raw_header',FIELDS),('raw_record',VALUES)):
  f=t[key];raw=base64.b64decode(f['cp950_base64'],validate=True)
  assert len(raw)==f['bytes'] and digest(raw)==f['sha256']
  assert list(csv.reader(io.StringIO(raw.decode('cp950'),newline=''),strict=True))==[expected]
  fragments.append(raw)
 report=load(ROOT/e['report']['path'])
 assert digest((ROOT/e['report']['path']).read_bytes())==e['report']['sha256']
 assert report['http_status']==200 and report['source_size']==s['bytes'] and report['source_bytes_sha256']==s['sha256']
 assert report['headers']==FIELDS and report['rows_checked']==s['data_records']
 assert report['exact_book_number_rows']==[{'csv_row_1based':3541,'bibliographic_fields':t['fields'],'exact_book_number_column':True}]
 assert report['negative_absence_certified'] is False and report['item_folio_or_glyph_certified'] is False
 assert all(e['independent_replay'][k] is True for k in ('full_csv_sha_recomputed','complete_csv_reparsed','exact_row_reproduced','raw_record_offset_reproduced'))
 assert all(v is None for v in e['unresolved'].values())
 assert e['historical_guards']=={'d5':'〇/五_UNRESOLVED','g893_six':'OPEN','legacy_13ei':'RETRACTED','algorithm_reopens':0,'candidate_collapses':0}
 assert e['counts']=={'matrix':[222,222],'sources':761,'graph':[252,238],'open_or_blocked':11,'new_physical_witnesses':0,'new_original_glyphs':0,'product':'CLOSED'}
 assert not e['transmission_impact']['edges_supported']
 if source is not None:
  assert len(source)==s['bytes'] and digest(source)==EXPECTED_SHA
  reader=csv.reader(io.StringIO(source.decode('cp950'),newline=''),strict=True)
  previous_line=0;matches=[];records=0;lines=source.splitlines(keepends=True)
  for logical,row in enumerate(reader,1):
   first,last=previous_line+1,reader.line_num;previous_line=last
   if logical==1:assert row==FIELDS;continue
   records+=1
   if not row:continue
   assert len(row)==5
   if ''.join(row[1].split()) in ('03130','20803130') or ''.join(row[2].split()) in ('03130','20803130'):
    matches.append((logical,first,last,row))
    assert b''.join(lines[first-1:last])==fragments[1]
  assert records==28913 and matches==[(3541,3633,3633,VALUES)]
  assert lines[0]==fragments[0]
 return True

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--source-csv',type=Path);args=parser.parse_args()
 check(load(E),args.source_csv.read_bytes() if args.source_csv else None)
 print('13GK_PASS_'+('FULL_CSV_BYTE_REPLAY' if args.source_csv else 'SEALED_ROW_AND_REPORT_SCOPE'))
