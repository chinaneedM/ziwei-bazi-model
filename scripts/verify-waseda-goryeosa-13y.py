#!/usr/bin/env python3
"""13Y source-anchored, no-OCR, exact Decimal collation. Optional PDF replay."""
import json,hashlib,argparse
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH='docs/research/TIANWEN-13Y-WASEDA-GORYEOSA-WORK52-D12-D20-SOLAR-LOCAL-FINITE-DIFFERENCE-R1.json'
PDF_SHA='28ebfeb34191f45715bc449d27da61fe04fb05eb45e84dd00cf569699f46225f'
JPEG_SHA='388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66'
EXPECTED=["5.1618","5.1804","5.1990","5.2176","5.1362","5.2548","5.2734","5.2920","5.3106"]
GLYPHS=["五分一六一八","五分一八〇四","五分一九九〇","五分二一七六","五分一三六二","五分二五四八","五分二七三四","五分二九二〇","五分三一〇六"]
ROI_SHA=['b1b41fff371665fb35bd006b0b4851eb2c7da810035ddfb75aabe072b69f862c','9dad04dce3c5de40fdbd165e13c7ae038cc7b3ab2d8a37c64fb90b93be3b8c0e']
def read():return json.loads((ROOT/PATH).read_text(encoding='utf-8'))
def check(d):
 assert d['schema']=='TIANWEN-13Y-WASEDA-WORK52-D12-D20-NATIVE-SOLAR-ORIGINAL-COLLATION-R1'
 s=d['source'];assert (s['pdf_sha256'],s['pdf_pages'],s['pdf_page_1_based'],s['native_embedded_jpeg_xref'],s['jpeg_sha256'])==(PDF_SHA,85,23,70,JPEG_SHA)
 assert s['native_dimensions']==[2592,1728]
 assert [x['day'] for x in d['original_short_day_series']]==list(range(12,21))
 assert [x['lexical_decimal'] for x in d['original_short_day_series']]==EXPECTED
 assert [x['original_glyph'] for x in d['original_short_day_series']]==GLYPHS
 assert [x['decoded_rgb_sha256'] for x in d['native_rgb_crops']]==ROI_SHA
 assert [x['xyxy'] for x in d['native_rgb_crops']]==[[1350,360,2270,1500],[375,360,1200,1500]]
 vs=[Decimal(x) for x in EXPECTED];ds=[vs[i+1]-vs[i] for i in range(8)]
 assert ds==[Decimal(x) for x in ('0.0186','0.0186','0.0186','-0.0814','0.1186','0.0186','0.0186','0.0186')]
 a=d['arithmetic'];assert a['exception_d15_to_d16']=='-0.0814' and a['exception_d16_to_d17']=='+0.1186'
 assert (vs[3]+vs[5])/2==Decimal(a['neighbor_midpoint_d16'])==Decimal('5.2362')
 assert Decimal(a['neighbor_midpoint_d16'])-vs[4]==Decimal(a['midpoint_minus_print'])==Decimal('0.1000')
 assert d['comparator']['waseda_d18_cumulative_folio'] is None and d['comparator']['ming1569_same_mechanical_column_proven'] is False
 r=d['restrictions'];assert r['single_original_pdf_source'] and r['no_ocr'] and r['not_proof_of_direct_copying']
 assert (r['physical_independent_vote_added'],r['registry_sources_added'],r['genealogy_edges_added'],r['algorithm_reopen'],r['open_research_issues'],r['deterministic_chart_product'])==(0,0,0,0,11,'CLOSED')
 return True
def verify_pdf(d,pdf_path):
 import fitz
 from PIL import Image
 from io import BytesIO
 p=Path(pdf_path);assert hashlib.sha256(p.read_bytes()).hexdigest()==PDF_SHA
 doc=fitz.open(str(p))
 try:
  assert len(doc)==85 and any(x[0]==70 for x in doc[22].get_images(full=True))
  b=doc.extract_image(70);assert b['ext']=='jpeg' and hashlib.sha256(b['image']).hexdigest()==JPEG_SHA
  rgb=Image.open(BytesIO(b['image'])).convert('RGB')
  for x in d['native_rgb_crops']:
   assert hashlib.sha256(rgb.crop(tuple(x['xyxy'])).tobytes()).hexdigest()==x['decoded_rgb_sha256']
 finally:doc.close()
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--source-pdf');a=parser.parse_args();e=read();check(e)
 if a.source_pdf:verify_pdf(e,a.source_pdf)
 print('TIANWEN_13Y_'+('SOURCE_REPLAY' if a.source_pdf else 'STATIC')+'_PASS')
