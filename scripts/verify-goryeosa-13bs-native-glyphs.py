#!/usr/bin/env python3
"""13BS manually visually reviewed original-image SHA-bound ROI gate."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BS-GORYEOSA-WASEDA-D16-NAJ-D18-D19-SOURCE-NATIVE-GLYPH-COLLATION-R1.json"
MD="docs/research/TIANWEN-13BS-GORYEOSA-WASEDA-D16-NAJ-D18-D19-SOURCE-NATIVE-GLYPH-COLLATION-R1.md"
BR="docs/research/TIANWEN-13BR-GORYEOSA-WASEDA-D16-NAJ-D18-D19-BOUNDED-SOURCE-ACQUISITION-R1.json"
BQ="docs/research/TIANWEN-13BQ-GORYEOSA-NUMERIC-PARALLELS-HEADING-GRADE-AND-LEGACY-ATTRIBUTION-R1.json"
BG="docs/research/TIANWEN-13BG-GORYEOSA-NAJ-ADJACENT-FOLIOS-CUMULATIVE-D17-D19-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
REQUIRED=[
("W_D16_DAY","十六日",16,[1392,352,1535,670],"a1e38d946ae6dd7e16d0e652887489d983227cc605adf7a047874bfe8033d85b"),
("W_D16_LONG","四百二十九六〇七三",16,[1415,680,1462,1410],"72008b56d7ea8ebde8804d0648f3e7934c0e98838a45b0cc1ca25a5c0f4fba5d"),
("W_D16_SHORT","五分一三六二",16,[1462,680,1512,1410],"78648fd810f726f4cb42eb50bf9dfd95841bc5d20dd73196b165994f0f66e443"),
("N_D18_DAY","十八日",18,[2350,520,2465,815],"09a8f78fe2446bad31a689db2e339cc1a508de357c125bd39c92dd9e249cc257"),
("N_D19_DAY","十九日",19,[2185,520,2310,815],"691553c623bc1bbf344066a6feffae5b576e5d352e2623506f851b7cf0b5ca1d")]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def replay(e,wa,na):
 from PIL import Image
 for s,path in zip(e["source_images"],(wa,na)):
  orig=Path(path).read_bytes()
  assert hashlib.sha256(orig).hexdigest()==s["jpeg_sha256"]
  with Image.open(path) as im:
   rgb=im.convert("RGB")
   assert list(rgb.size)==s["dimensions"]
   for r in e["original_rgb_rois"]:
    if r["source"]==s["holding"]:
     assert hashlib.sha256(rgb.crop(r["bbox"]).tobytes()).hexdigest()==r["rgb_sha256"]
 return True
def check(e,br,bq,bg,l,s):
 assert e["schema"]=="TIANWEN-13BS-FIRSTPARTY-TWO-COPY-ORIGINAL-ISOLATED-GLYPHS-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["grade"]=="DIRECT_HUMAN_VISUAL_NO_OCR_ORIGINAL_SOURCE_RGB_SHA_BOUND"
 assert [(r["key"],r["literal"],r["printed_day"],r["bbox"],r["rgb_sha256"]) for r in e["original_rgb_rois"]]==REQUIRED
 assert [x["artifact_id"] for x in e["source_images"]]==[12340588249,12340553228]
 assert [x["run_id"] for x in e["source_images"]]==[39588454662,39588454662]
 assert [x["jpeg_sha256"] for x in e["source_images"]]==[br["sources"][0]["image_sha256"],br["sources"][1]["image_sha256"]]
 assert [x["artifact_zip_sha256"] for x in e["source_images"]]==["41863a3d931122d53cce3bcdd59af1828eb41cc7efbab53b32ec738273a9306c","f39ac9b4dd815133ea2cad55088ff33963783e22d960b19c03729230b80eaced"]
 assert bg["source_canvases"][2]["source_jpeg_sha256"]==e["source_images"][1]["jpeg_sha256"]
 assert bq["subfinding"]["naj_apparent_layout_without_individual_day_header_pairs"]==2  # preserved old snapshot
 assert e["upgraded_scope"]["WASEDA_D16_CUMULATIVE"]=="NOT_YET_BOUND"
 assert e["upgraded_scope"]["NAJ_D18_D19_HEADING_TO_CUMULATIVE_FIELD"]=="NOT_YET_REBOUND"
 assert e["upgraded_scope"]["D16_ANCESTRAL_ONE_VS_TWO"]=="UNRESOLVED"
 assert e["upgraded_scope"]["WHOLE_TABLE_INDEX"]=="UNRESOLVED"
 assert all(e["firewall"][k]==0 for k in ("new_original_source_objects","new_physical_witnesses","new_independent_stemma_votes","new_source_registry_entries","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"))
 assert e["firewall"]["open_research_risks"]==len(l["issues"])==11
 assert e["firewall"]["deterministic_product"]==s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 assert e["transmission_impact"]["nodes_added"]==e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert i["status"]=="OPEN" and i["priority"]=="P0"
 assert i["source_refs"].count(MD)==i["source_refs"].count(P)==1 and i["source_refs"].index(P)==i["source_refs"].index(MD)+1
 h=next(x for x in i["history"] if x.get("revision_id")=="TW-OPEN-0005-NATIVE-D16-D18-D19-13BS")
 assert h["previous_next_action"].startswith("13BR CURRENT ACTION")
 assert {P,MD,BR,BG,BQ}.issubset(set(h["evidence_refs"]))
 later=any("next_action" in z.get("changed_fields",[]) for z in i["history"][i["history"].index(h)+1:])
 prefix=l["binding"]["latest_research_focus_prefix"]
 assert i["next_action"].startswith("13BS CURRENT ACTION") or (later and prefix!="13BS" and i["next_action"].startswith(prefix+" CURRENT ACTION"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(z.startswith("13BS ") for z in s["historical_audit"]["current_focus"])
 assert prefix==s["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in l["issues"]}
 assert (ROOT/MD).is_file()
 return True
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--waseda-jpeg");a.add_argument("--naj-jpeg");args=a.parse_args()
 e=load(P);assert check(e,load(BR),load(BQ),load(BG),load(L),load(S))
 if args.waseda_jpeg or args.naj_jpeg:
  assert args.waseda_jpeg and args.naj_jpeg and replay(e,args.waseda_jpeg,args.naj_jpeg)
 print("13BS original Waseda D16 / NAJ D18-D19 direct glyph source ROI gate PASS")
