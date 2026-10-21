#!/usr/bin/env python3
"""13BT: exact NAJ canvas18 same-folio day-heading/cumulative tight lane evidence."""
import argparse,hashlib,json
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BT-GORYEOSA-NAJ-C18-D18-D19-DIRECT-CUMULATIVE-AND-PRINTED-HEADING-GEOMETRY-R1.json"
MD="docs/research/TIANWEN-13BT-GORYEOSA-NAJ-C18-D18-D19-DIRECT-CUMULATIVE-AND-PRINTED-HEADING-GEOMETRY-R1.md"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
BS="docs/research/TIANWEN-13BS-GORYEOSA-WASEDA-D16-NAJ-D18-D19-SOURCE-NATIVE-GLYPH-COLLATION-R1.json"
BG="docs/research/TIANWEN-13BG-GORYEOSA-NAJ-ADJACENT-FOLIOS-CUMULATIVE-D17-D19-R1.json"
BQ="docs/research/TIANWEN-13BQ-GORYEOSA-NUMERIC-PARALLELS-HEADING-GRADE-AND-LEGACY-ATTRIBUTION-R1.json"
BR="docs/research/TIANWEN-13BR-GORYEOSA-WASEDA-D16-NAJ-D18-D19-BOUNDED-SOURCE-ACQUISITION-R1.json"
EXPECTED=[[18,"十八日",[2350,520,2465,815],"09a8f78fe2446bad31a689db2e339cc1a508de357c125bd39c92dd9e249cc257","八千〇〇〇二六九七","8000.2697",[2490,827,2552,1760],"433e8d3aab7170282c8bb94dd6e42acc7e1aa6cdb1d09738bd485e7a107ca20b"],[19,"十九日",[2185,520,2310,815],"691553c623bc1bbf344066a6feffae5b576e5d352e2623506f851b7cf0b5ca1d","八千四百二十四六四〇八","8424.6408",[2318,827,2378,1760],"d7316b09caa6210f7075176551064a2ac6ce5e86e5d21726983d0a15d17a4884"]]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def replay(e,original):
 from PIL import Image
 b=Path(original).read_bytes();src=e["firstparty_source"]
 assert hashlib.sha256(b).hexdigest()==src["jpeg_sha256"]
 with Image.open(original) as im:
  rgb=im.convert("RGB");assert list(rgb.size)==src["dimensions"]
  for row in e["paired_original_field_columns"]:
   for a,h in (("heading_bbox","heading_sha256"),("cumulative_bbox","cumulative_sha256")):
    assert hashlib.sha256(rgb.crop(tuple(row[a])).tobytes()).hexdigest()==row[h]
 return True
def check(e,s,l,prior):
 assert e["schema"]=="TIANWEN-13BT-NAJ-ORIGINAL-CANVAS18-INTRA-COLUMN-PRINTED-DAY-AND-CUMULATIVE-GEOMETRY-R1"
 assert e["date"]=="2026-10-21" and e["issue_id"]=="TW-OPEN-0005"
 assert e["grade"]=="DIRECT_SOURCE_NATIVE_ORIGINAL_RGB_TIGHT_CUMULATIVE_PLUS_INDEPENDENT_DAY_HEADING_NO_OCR"
 src=e["firstparty_source"]
 assert src["physical_holding"]=="NAJ-282-0006-PHYSICAL51"
 assert src["canvas_1based"]==18 and src["dimensions"]==[3000,2215]
 assert src["jpeg_sha256"]==prior["BS"]["source_images"][1]["jpeg_sha256"]==prior["BR"]["sources"][1]["image_sha256"]
 assert src["provider_manifest_sha256"]==prior["BR"]["sources"][1]["manifest_sha256"]
 assert src["run_id"]==39588454662 and src["artifact_id"]==12340553228
 assert src["artifact_zip_sha256"]=="f39ac9b4dd815133ea2cad55088ff33963783e22d960b19c03729230b80eaced"
 assert src["manual_review"]=="SOURCE_NATIVE_JPEG_RGB_NO_OCR"
 rows=e["paired_original_field_columns"]
 assert len(rows)==2 and [z["day"] for z in rows]==[18,19]
 assert [(z["day"],z["heading"],z["heading_bbox"],z["heading_sha256"],z["cumulative_literal"],z["cumulative_value"],z["cumulative_bbox"],z["cumulative_sha256"]) for z in rows]==[tuple(z) for z in EXPECTED]
 prevhead={z["printed_day"]:z for z in prior["BS"]["original_rgb_rois"] if z["field"]=="DAY_HEADING" and z["source"]==src["physical_holding"]}
 assert len(prevhead)==2
 oldnum={x["apparent_layout_day"]:x for x in prior["BG"]["source_canvases"][2]["new_day_slots"]}
 assert len(oldnum)==2
 for z in rows:
  day=z["day"]
  assert z["heading"]==prevhead[day]["literal"]
  assert z["heading_bbox"]==prevhead[day]["bbox"] and z["heading_sha256"]==prevhead[day]["rgb_sha256"]
  assert Decimal(z["cumulative_value"])==Decimal(oldnum[day]["decimal"])
  hx1,hy1,hx2,hy2=z["heading_bbox"];cx1,cy1,cx2,cy2=z["cumulative_bbox"]
  assert hy2<cy1 and 0<=hx1<hx2<=3000 and 0<=cx1<cx2<=3000
  assert 0<cx1-hx1<260 and 0<cx2-hx2<260
  assert 600<=cy2-cy1<=1000 and 30<=cx2-cx1<=80
 assert rows[0]["heading_bbox"][0]>rows[1]["heading_bbox"][0]
 assert rows[0]["cumulative_bbox"][0]>rows[1]["cumulative_bbox"][0]
 assert [z["value"] for z in prior["BQ"]["local_original_numeric_parallels"][:2]]==[z["cumulative_value"] for z in rows]
 assert all(z["naj"]["grade"]=="DIRECT_ORIGINAL_NUMERIC_APPARENT_LAYOUT_DAY_NO_INDIVIDUAL_DAY_HEADER" for z in prior["BQ"]["local_original_numeric_parallels"][:2])
 comp=e["comparison"]
 assert [comp["waseda_printed_day17_cumulative"],comp["waseda_printed_day18_cumulative"]]==[z["cumulative_value"] for z in rows]
 assert all(comp[k] is False for k in ("uniform_all_field_day_shift_proven","global_source_day_index_proven","independent_physical_copying_lineage_proven","ancient_D16_variant_ancestry_proven"))
 assert e["source_dependencies"]=={"previous_d18_d19_original_day_header":BS,"previous_broad_naj_numeric":BG,"prior_evidence_grade":BQ,"pixel_capture_definition":BR}
 fw=e["source_scope"]
 assert all(fw[k]==0 for k in ("new_original_jpeg_objects","new_physical_witnesses","new_independent_stemmatic_votes","new_registry_sources","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"))
 assert fw["research_risks_open_or_blocked"]==len(l["issues"])==11 and fw["product"]=="CLOSED"
 assert e["transmission_impact"]["nodes_added"]==e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["source_refs"].count(MD)==issue["source_refs"].count(P)==1
 assert issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 rev=next(z for z in issue["history"] if z.get("revision_id")=="TW-OPEN-0005-NAJ-HEADING-CUMULATIVE-GEOMETRY-13BT")
 assert rev["previous_next_action"].startswith("13BS CURRENT ACTION")
 assert {MD,P,BS,BG,BQ,BR}.issubset(set(rev["evidence_refs"]))
 later=any("next_action" in z.get("changed_fields",[]) for z in issue["history"][issue["history"].index(rev)+1:])
 prefix=l["binding"]["latest_research_focus_prefix"]
 assert issue["next_action"].startswith("13BT CURRENT ACTION") or (later and prefix!="13BT" and issue["next_action"].startswith(prefix+" CURRENT ACTION"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(x.startswith("13BT ") for x in s["historical_audit"]["current_focus"])
 assert prefix==s["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in l["issues"]}
 assert (ROOT/MD).is_file()
 return True
if __name__=="__main__":
 args=argparse.ArgumentParser();args.add_argument("--naj-original")
 a=args.parse_args();e=load(P)
 assert check(e,load(S),load(L),{"BS":load(BS),"BG":load(BG),"BQ":load(BQ),"BR":load(BR)})
 if a.naj_original: assert replay(e,a.naj_original)
 print("13BT NAJ original D18/D19 heading + cumulative field column geometry SHA PASS")
