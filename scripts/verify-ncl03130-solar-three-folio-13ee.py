#!/usr/bin/env python3
"""13EE exactly SHA-bind three same digital source printed-day and same-column controls."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EE-NCL03130-SOLAR-SAME-COLUMN-THREE-FOLIO-R1.json";S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
ED="docs/research/TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1.json"
DZ="docs/research/TIANWEN-13DZ-NCL03130-CORRECT-SOLAR-D28-ORIGINAL-P76-LOCATOR-R1.json"
def read(p):return json.loads((ROOT/p).read_text(encoding="utf8"))
def check(e,s,l,ed,dz):
 assert e["schema"]=="TIANWEN-13EE-NCL03130-SOLAR-SAME-COLUMN-THREE-FOLIO-R1" and e["issue_id"]=="TW-OPEN-0005"
 assert e["evidence_type"]=="SINGLE_DIGITAL_COPY_THREE_SEQUENTIAL_PAGE_LAYOUT_CONTROLS_NOT_THREE_WITNESSES"
 assert e["source"]["pdf_sha256"]==ed["source"]["pdf_sha256"]==dz["source"]["source_sha256"]
 assert e["source"]["archive_run"]==ed["source"]["archive"]["workflow_run"] and e["source"]["archive_artifact_id"]==ed["source"]["archive"]["artifact_id"]
 assert e["source"]["ocr_used"] is False and e["source"]["firstparty_item_identity"]==e["source"]["qing_vs_1905_hand"]=="UNBOUND"
 pages=e["pages"];assert len(pages)==3
 assert [(p["pdf_page"],p["source_printed_day"],p["printed_heading"]) for p in pages]==[(75,19,"十九日"),(76,30,"三十日"),(77,41,"四十一日")]
 source_pages={p["page"]:p for p in dz["original_page_register"]}
 assert all(p["png_sha256"]==source_pages[p["pdf_page"]]["png_sha256"] and p["rgb_sha256"]==source_pages[p["pdf_page"]]["rgb_sha256"] and p["size"]==source_pages[p["pdf_page"]]["size"] for p in pages)
 names=("day_heading","narrow_original_column","bounded_column_tail","adjacent_column_panel")
 bboxes=([561,165,602,291],[590,418,615,830],[590,706,615,830],[553,418,649,830])
 hashes=[
 ("c5b78cb7d76e5988b369987f5104f2abaa4ec0a13a74541ba9901c8808f36b22","8f886d0625d18891f08a5f1e2d3f0b98ee7bf6bbc957e2db3a4b45e7bbcb8950","362a4d8ff9e3de807f83db9dd01ca8a7f16581802d3ed5dc48da62775fcc5e30","d321c5c45d5cd13112f7a073c2458affcce8fbd226992f0b77d600f81a116b76"),
 ("2e18e2334cde0d4a94531053e04b3971ac585c2c2d322bca2e0c917c3d31bbe7","bc91212e7b7a6a98f67913788e0051c3eabfd5af46982aa26f90a3339cf0efd4","e4be7390aed463b167271a74aecd3d98046a2b9b5e0b204360411805d5337c6a","2908bd99867f113858322eb8cef07403b9ae7b6e7550b2a0c9002fdd80b32a87"),
 ("d2a63648cc7b8d545fb419e183511804ae2882fe27d188311fb772060a3ecef0","7f33c597134ce8f65f870f4c1b9acbb4ec8293e1bf939e4720b920e7c2f08120","a9b6daa174e40a5ef584427da733c0cf5bbdf64e0f0530a07324e844dfbd2e18","39fba34ac10c27091a83e735b8cb21c17e5b01fa9d76f243172750c44f8b85e6")]
 for page,expected_hashes in zip(pages,hashes):
  assert tuple(page["rois"])==names
  assert [(page["rois"][k]["bbox"],page["rois"][k]["rgb_sha256"]) for k in names]==list(zip(bboxes,expected_hashes))
 assert pages[1]["rois"]["narrow_original_column"]["rgb_sha256"]==ed["native_rois"][2]["rgb_sha256"]
 assert pages[1]["rois"]["bounded_column_tail"]["rgb_sha256"]==ed["native_rois"][3]["rgb_sha256"]
 obs=e["observation"]
 assert obs["day_heading_values"]==["十九日","三十日","四十一日"] and obs["all_three_are_same_shot_coordinate_roi"] is True
 assert obs["visible_column_endings_unequal"] is True and obs["neighbor_panel_has_distinct_printed_vertical_columns"] is True
 assert obs["d30_existing_literal"]==ed["finding"]["d30_visible_glyph_group"]=="初度九十六二〇三"
 assert obs["d30_tail_same_narrow_field_no_additional_character"] is True and obs["numeric_d30"] is None
 assert obs["meaning_of_d30_shortness"]=="UNRESOLVED" and obs["full_technical_same_field_equivalence_across_folios"]=="NOT_ADJUDICATED"
 assert obs["global_day_offset"]=="UNPROVEN" and obs["full_page_line_by_line_review"] is False and obs["full_folio_numerical_transcription"] is False
 imp=e["impact"];assert (imp["new_source_p75_p77_native_layout_controls"],imp["three_archived_source_pages_replayed"],imp["issues_open"],imp["product"])==(2,3,11,"CLOSED")
 assert all(imp[k]==0 for k in ("new_physical_copies","new_independent_votes","new_original_d30_numeric_adjudications","matrix_rows_added","source_registry_additions","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens","issues_closed"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"]) and l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(f.startswith("13EE NCL03130 THREE-FOLIO") for f in s["historical_audit"]["current_focus"])
 issue=next(q for q in l["issues"] if q["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN" and issue["next_action"].startswith("13EE CURRENT ACTION")
 assert "p73" in issue["next_action"] and "numeric" in issue["next_action"] and E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"]
 h=issue["history"][-1];assert h["revision_id"]=="TW-OPEN-0005-13EE-THREE-FOLIO-LANE-CONTROL-20261023"
 assert h["previous_next_action"].startswith("13ED CURRENT ACTION")
 assert set(h["changed_fields"])=={"source_refs","next_action"} and set([E,E.replace(".json",".md"),ED]).issubset(set(h["evidence_refs"]))
 assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay(e,source_dir):
 from PIL import Image
 root=Path(source_dir)
 for page in e["pages"]:
  f=root/f'original-p{page["pdf_page"]:03d}.png'
  raw=f.read_bytes();assert hashlib.sha256(raw).hexdigest()==page["png_sha256"],f.name
  with Image.open(f) as im:rgb=im.convert("RGB")
  assert list(rgb.size)==page["size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==page["rgb_sha256"],f.name
  for name,q in page["rois"].items():
   x0,y0,x1,y1=q["bbox"];assert 0<=x0<x1<=rgb.width and 0<=y0<y1<=rgb.height
   assert hashlib.sha256(rgb.crop(q["bbox"]).tobytes()).hexdigest()==q["rgb_sha256"],name
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--source-dir");args=ap.parse_args()
 e=read(E);assert check(e,read(S),read(L),read(ED),read(DZ))
 if args.source_dir:assert replay(e,args.source_dir)
 print("13EE_PASS SAME_SOURCE_THREE_FOLIOS_HEADINGS_19_30_41 D30_NUMERIC_OPEN")
