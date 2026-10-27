#!/usr/bin/env python3
"""13HQ: keep two adjacent NDL1909 printed images and separate seasonal controls source-scoped."""
import argparse,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13HQ-NDL991069-CANVAS72-73-WINTER-SURPLUS-DEFICIT-CONTEXT-R1.json"
def check(e,*,ledger=None):
 assert e["schema"]=="TIANWEN-13HQ-NDL991069-CANVAS72-73-WINTER-SURPLUS-DEFICIT-CONTEXT-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["source"]["print_year"]==1909
 assert e["source"]["canvas72"]["sha256"]=="295a3a839914f51a33c19f6e7cea6c113413d9bcb3c2423c60589bb51bdf5c86"
 assert e["source"]["canvas73"]["sha256"]=="c5fc1b3aeff9aedb84bc36fff02fad2a865e7c86c9fd1e624f7f18a548f945bb"
 assert e["source"]["canvas72"]["dimensions"]==[1600,1248]
 assert e["source"]["canvas73"]["dimensions"]==[3773,2943]
 assert e["source"]["atlas"]["zip_sha256"]=="f0776fc9d679ac72c481241edb08010be889413ad15f8b36c8d25427726de69d"
 assert e["source"]["canvas73"]["artifact_zip_sha256"]=="5fa5a8d197238794d16ed5c3e37e33fe5d74b4838d4d51da27195548c42935e9"
 assert e["contextual_reading"]["heading_original_1909_surface"]=="太陽冬至前後二氣盈初縮末限"  # Historical misread, superseded by 13HT, do not overwrite immutable JSON
 assert e["contextual_reading"]["companion_caption"]=="授時曆立成"
 assert [x["visible_day_range"] for x in e["contextual_reading"]["table_day_continuity"]]==["初日..五日","六日..十一日","十二日..十七日"]
 assert e["contextual_reading"]["printed_D14_first_local_field"]=="五分一九九〇"
 assert e["contextual_reading"]["printed_D16_first_local_field"]=="五分一三六二"
 assert e["contextual_reading"]["exact_ancient_unit"] is None
 assert e["contextual_reading"]["ancient_numerical_winner"] is None
 assert e["contextual_reading"]["independent_earlier_original_solar_table_identity"] is None
 assert e["scope_firewall"]["printed_winter_surplus_deficit_context_does_not_equal_nikh_summer_d14"]
 assert e["scope_firewall"]["NIKH_photo4_summer_D14"]=="四分六六三〇"
 assert e["scope_firewall"]["NCL03130_original_D14_full"] is None
 assert e["scope_firewall"]["NCL03130_old_vs_Guangxu_copy_stratum"] is None
 assert e["scope_firewall"]["G893_original_six"]==e["scope_firewall"]["D5_original_zero_vs_five"]=="OPEN"
 assert e["scope_firewall"]["legacy_13EI"]=="RETRACTED"
 assert all(e["scope_firewall"][k]==0 for k in ("physical_witness_added","new_source_registry_entries","new_graph_nodes","new_graph_edges","algorithm_reopens","candidate_collapses"))
 assert e["counts"]=={"matrix":[222,222],"registered_sources":761,"genealogy":[252,238],"open_issues":11,"chart":"CLOSED"}
 assert e["transmission_impact"]=="NONE"
 rows=e["image_regions"]
 assert [x["id"] for x in rows]==["72-table-heading-and-winter-two-qi","72-day-initial-to-five","73-day-six-to-eleven","73-day-twelve-to-seventeen"]
 assert [x["rgb_sha256"] for x in rows]==[
  "7ff63b695d1009c1677640cd3bc7cc909ead58428666d7a9700d6237940a1bf9",
  "d9c6f1888910c15cd36bc0881b8557b1f24af364e1194f8192e7ce55e5d845a4",
  "32a7c551e85fbbb8d12bc38f656ad94b2888031a4dcfde2f12f0038e2d486bfa",
  "d9109e7d2e1d7c801a46973416eb821cbb4566c88bc88ef544087cb202b30b2e"]
 for j,x in enumerate(rows):
  w,h=([1600,1248] if j<2 else [3773,2943])
  a,b,c,d=x["bbox_xyxy"]
  assert 0<=a<c<=w and 0<=b<d<=h
 s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
 l=ledger if ledger is not None else json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,s["schema_version"].split("."))) >= (1,871,0)
 assert any(x.startswith("13HQ ") for x in s["historical_audit"]["current_focus"])
 assert any(x.startswith("13HQ ") for x in s["historical_audit"]["current_focus"])
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 # Historical action transitions live in append-only history; next_action may advance.
 for tag in ('13HQ', '13HP'):
     assert any(
         h.get("event")=="ISSUE_REVISION"
         and h.get("revision_id", "").startswith("TW-OPEN-0005-"+tag+"-")
         and "next_action" in h.get("changed_fields", [])
         and (tag!="13HQ" or str(E.relative_to(ROOT)) in h.get("evidence_refs", []))
         for h in i["history"]
     ), tag
 assert i["priority"]=="P0" and i["status"]=="OPEN"
 assert any(h.get("revision_id","").startswith("TW-OPEN-0005-13HQ-") for h in i["history"])
 assert str(E.relative_to(ROOT)) in i["source_refs"]
 return True
def replay(e,p72,p73):
 from io import BytesIO
 from PIL import Image
 for path,src,key in ((p72,e["source"]["canvas72"],"canvas-072.jpg"),(p73,e["source"]["canvas73"],"canvas-073-full-provider.jpg")):
  bb=Path(path).read_bytes()
  expected_zip=e["source"]["atlas"]["zip_sha256"] if key=="canvas-072.jpg" else src["artifact_zip_sha256"]
  assert hashlib.sha256(bb).hexdigest()==expected_zip
  with zipfile.ZipFile(BytesIO(bb)) as z:
   img=z.read(key)
  assert hashlib.sha256(img).hexdigest()==src["sha256"]
  with Image.open(BytesIO(img)) as x:
   rgb=x.convert("RGB")
   assert list(rgb.size)==src["dimensions"]
   for y in e["image_regions"]:
    if y["source_member"]!=key: continue
    assert hashlib.sha256(rgb.crop(tuple(y["bbox_xyxy"])).tobytes()).hexdigest()==y["rgb_sha256"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--atlas-zip");p.add_argument("--full-zip");args=p.parse_args()
 e=json.loads(E.read_text(encoding="utf8"))
 check(e)
 if args.atlas_zip and args.full_zip:
  assert replay(e,args.atlas_zip,args.full_zip)
 print("TIANWEN_13HQ_NDL991069_ADJACENT_WINTER_TEXT_SCOPE_PASS")
