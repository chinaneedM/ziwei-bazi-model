#!/usr/bin/env python3
"""13BX firstparty Waseda p26/p27 D39-D56 bounded header-original replay."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BX-GORYEOSA-WASEDA-P26-P27-ORIGINAL-D39-D56-AND-EXTENDED-FOLIO-ATLAS-R1.json"
MD="docs/research/TIANWEN-13BX-GORYEOSA-WASEDA-P26-P27-ORIGINAL-D39-D56-AND-EXTENDED-FOLIO-ATLAS-R1.md"
BW="docs/research/TIANWEN-13BW-GORYEOSA-WASEDA-P24-P25-ORIGINAL-D21-D38-AND-P26-P27-BOUNDARY-R1.json"
BV="docs/research/TIANWEN-13BV-GORYEOSA-WASEDA-P21-P23-ORIGINAL-SOLAR-TABLE-TITLE-AND-FIRST-DAY-INDEX-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EXPECTED=[["P26_D39_DAY",26,39,"三十九日",[2035,345,2195,670],"00cd2a0ac1e828b07e9303ecd1d46e17b06737d6e3aca275f04b2079d6680045"],["P26_D47_DAY",26,47,"四十七日",[465,350,620,670],"e9e90512382a56437feab71f46052592882f14a92be9195a0f51199155e30f1d"],["P27_D48_DAY",27,48,"四十八日",[2040,345,2190,680],"cd25147733fc55af20298e0774a23656315cafc1a959ca5b3ef700e03e49f933"],["P27_D56_DAY",27,56,"五十六日",[465,350,620,680],"53519d9c27862bcb212f68880ec0949a8ef10ab6a746af79c0247ea16e934801"]]
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def replay(e,source26,source27):
 from PIL import Image
 for source,path in zip(e["source"]["images"],[source26,source27]):
  raw=Path(path).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==source["jpeg_sha256"]
  with Image.open(path) as im:
   rgb=im.convert("RGB")
   assert list(rgb.size)==source["dimensions"]
   for z in e["original_day_header_rois"]:
    if z["page"]==source["page"]:
     assert hashlib.sha256(rgb.crop(tuple(z["bbox"])).tobytes()).hexdigest()==z["pixel_sha256"]
 return True
def check(e,state,ledger,old):
 assert e["schema"]=="TIANWEN-13BX-WASEDA-ORIGINAL-D39-D56-HEADINGS-AND-P28-P44-ATLAS-R1"
 assert e["date"]=="2026-10-21" and e["issue_id"]=="TW-OPEN-0005"
 assert e["grade"]=="DIRECT_FIRSTPARTY_NATIVE_RGB_MANUAL_NO_OCR_TWO_PAGE_DAY_ENDPOINTS"
 src=e["source"]
 assert src["holding"]=="WASEDA-RI06-02809-BOOK33"
 assert src["pdf_sha256"]==old["BW"]["source"]["pdf_sha256"]==old["BV"]["source"]["pdf_sha256"]
 assert src["run_id"]==39600263596 and src["artifact_id"]==12345517803
 assert src["zip_sha256"]=="3bdfeb8635d237472d76cea12ee49aaac166e0a0f6a0b6ddd34a062a59d2cfca"
 assert [(z["page"],z["xref"],z["jpeg_sha256"],z["dimensions"]) for z in src["images"]]==[
 (26,79,"a87c09d1a0b0711d8b0165e04a4f31df0d9a2bf755589e9b91ff43602243bb62",[2592,1728]),
 (27,82,"bfe72c70715b152295d526b8921a0ca1821a38340c73d275343a694d015201a0",[2592,1728])]
 assert [(z["key"],z["page"],z["day"],z["literal"],z["bbox"],z["pixel_sha256"]) for z in e["original_day_header_rois"]]==[tuple(x) for x in EXPECTED]
 assert [z["day"] for z in e["original_day_header_rois"]]==[39,47,48,56]
 for z in e["original_day_header_rois"]:
  x1,y1,x2,y2=z["bbox"]
  assert 0<=x1<x2<=2592 and 0<=y1<y2<=1728
 f=e["extension_summary"]
 assert [f[x] for x in ("p26_first","p26_last","p27_first","p27_last")]==["三十九日","四十七日","四十八日","五十六日"]
 assert f["observed_day_endpoint_span"]=="初日至五十六日"
 assert f["historical_full_table_end"]=="UNBOUND_AFTER_D56"
 assert f["Waseda_D16_independent_cumulative"]=="UNBOUND"
 assert f["all_intermediate_days_individually_hashed"] is False
 assert f["JIRI_printed_day_heading_is_not_proven_numeric_field"] is True
 assert f["universal_day_offset_between_physical_holdings"]=="UNPROVEN"
 assert old["BW"]["findings"]["printed_table_end"]=="UNBOUND_AFTER_D38"
 assert old["BV"]["finding"]["original_initial_day_heading"]=="初日"
 atlas=e["requested_atlas"]
 assert [atlas["pages_first"],atlas["pages_last"],atlas["pages_count"]]==[28,44,17]
 assert atlas["pages_captured"]=="PENDING_SOURCE_WORKFLOW" and atlas["image_hashes"]=="PENDING_ARTIFACT"
 assert atlas["pdf_expected_sha256"]==src["pdf_sha256"]
 assert atlas["prior_p27_jpeg_expected_sha256"]==src["images"][1]["jpeg_sha256"]
 assert atlas["source_image_pixels_interpreted"] is False and atlas["ocr"] is False
 assert atlas["workflow"]==".github/workflows/acquire-goryeosa-waseda-p28-p44-original-13bx.yml" and atlas["script"]=="scripts/acquire-goryeosa-waseda-p28-p44-original-13bx.py"
 assert e["source_dependencies"]=={"previous_p24_p25_original":BW,"original_table_start":BV}
 fw=e["scope_firewall"]
 assert all(fw[k]==0 for k in ("new_historical_physical_witnesses","new_independent_stemmatic_votes","new_source_registry_entries","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"))
 assert fw["research_risks_open_or_blocked"]==len(ledger["issues"])==11 and fw["chart"]=="CLOSED"
 assert e["transmission_impact"]["nodes_added"]==e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 issue=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert issue["source_refs"].count(MD)==issue["source_refs"].count(P)==1
 assert issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 rev=next(z for z in issue["history"] if z.get("revision_id")=="TW-OPEN-0005-WASEDA-P26-P27-AND-BULK-13BX")
 assert rev["previous_next_action"].startswith("13BW CURRENT ACTION")
 assert {MD,P,BW,BV}.issubset(set(rev["evidence_refs"]))
 later=any("next_action" in z.get("changed_fields",[]) for z in issue["history"][issue["history"].index(rev)+1:])
 prefix=ledger["binding"]["latest_research_focus_prefix"]
 assert issue["next_action"].startswith("13BX CURRENT ACTION") or (later and prefix!="13BX" and issue["next_action"].startswith(prefix+" CURRENT ACTION"))
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert any(z.startswith("13BX ") for z in state["historical_audit"]["current_focus"])
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert prefix==state["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
 assert set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in ledger["issues"]}
 assert (ROOT/MD).is_file()
 return True
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--source-p26");parser.add_argument("--source-p27")
 args=parser.parse_args();e=load(P)
 assert check(e,load(S),load(L),{"BW":load(BW),"BV":load(BV)})
 if args.source_p26 or args.source_p27:
  assert args.source_p26 and args.source_p27
  assert replay(e,args.source_p26,args.source_p27)
 print("13BX original Waseda p26/p27 day39..56 header SHA and atlas safety PASS")
