#!/usr/bin/env python3
"""13BM two physical original source images, cumulative day-header rebinding gate."""
import argparse,hashlib,json
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BM-GORYEOSA-WASEDA-P23-P24-DAY-HEADER-CUMULATIVE-FORWARD-ERRATUM-R1.json"
BJ="docs/research/TIANWEN-13BJ-GORYEOSA-WASEDA-P23-D18-D20-DIRECT-CUMULATIVE-AND-LONG-R1.json"
BK="docs/research/TIANWEN-13BK-GORYEOSA-NAJ-CANVAS18-D19-LONG-D20-D21-CUMULATIVE-R1.json"
YZ="docs/research/TIANWEN-12YZ-GORYEOSA-D14-D20-INTRATABLE-THREE-COLUMN-RECEIVED-ARITHMETIC-R1.json"
MD="docs/research/TIANWEN-13BM-GORYEOSA-WASEDA-P23-P24-DAY-HEADER-CUMULATIVE-FORWARD-ERRATUM-R1.md"
EXPECTED=[
("P23_D19_HEADING",23,19,"DAY_HEADING","十九日",None,[668,369,789,715],"1b369a17db7ca8438286ffc65e5eb88748fd8376b6329d950cea52fcd2942c5d"),
("P23_D19_CUM",23,19,"CUMULATIVE","八千八百四十三七五七一","8843.7571",[601,690,686,1400],"c84bbc7355dbf1ea3d46aefa7302cfc7587549e5a39a0e126a5427485f39a93a"),
("P23_D20_HEADING",23,20,"DAY_HEADING","二十日",None,[480,355,585,650],"419f8c26d10a6a1c29bc11498ccfa9702e8c4f10ad6b62eda72eaf72d383cb69"),
("P23_D20_CUM",23,20,"CUMULATIVE","九千二百五十七六〇〇〇","9257.6000",[455,690,527,1430],"c9a07620bceb80c7134930f9c888f8a94f8cd82a292202bf99cbee92dad6f236"),
("P24_D21_HEADING",24,21,"DAY_HEADING","二十一日",None,[2075,360,2150,610],"0f3016a057c2a1873ee4ef2a3a6dae6831c822bffcb6b32dfd11d53c4de60ff0"),
("P24_D21_CUM",24,21,"CUMULATIVE","九千六百六十六一五〇九","9666.1509",[2015,685,2080,1430],"54ac0b33b4075fc98f9875cbbfd5491bf1d95ff044e460e67ce4cd5c6b0f729c")]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def actual_original_replay(e,p23,p24):
 from PIL import Image
 for row,path in zip(e["source"]["pages"],(p23,p24)):
  raw=Path(path).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==row["jpeg_sha256"]
  with Image.open(path) as im:
   rgb=im.convert("RGB")
   assert list(rgb.size)==row["dimensions"]==[2592,1728]
   for roi in e["source_native_rgb_rois"]:
    if roi["pdf_page_1based"]==row["pdf_page_1based"]:
     assert hashlib.sha256(rgb.crop(roi["bbox"]).tobytes()).hexdigest()==roi["rgb_sha256"]
 return True
def check(e,bj,bk,yz,ledger,state):
 assert e["schema"]=="TIANWEN-13BM-WASEDA-ORIGINAL-CUMULATIVE-DAY-HEADER-CROSS-FOLIO-ERRATUM-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["date"]=="2026-10-21"
 assert e["grade"]=="TWO_SHA_VERIFIED_SOURCE_NATIVE_JPEGS_MANUAL_RGB_ROI_LITERAL_AND_DAY_HEADING_COLLATION_NO_OCR"
 s=e["source"]
 assert s["physical_holding"]==bj["source"]["holding"]=="WASEDA-RI06-02809-BOOK33"
 assert s["source_pdf_sha256"]==bj["source"]["pdf_sha256"]
 assert s["pages"]==[
 {"pdf_page_1based":23,"xref":70,"jpeg_sha256":"388f3d5dd9e9861f8ce90c304b154edaeaee98614bb12cd3468f957dcde6fc66","dimensions":[2592,1728],"source_artifact":12263559032},
 {"pdf_page_1based":24,"xref":73,"jpeg_sha256":"913368872d9a7589abf88a4ae9b8d87ca4b836cc27c0d66d21b8ba82022e1574","dimensions":[2592,1728],"source_artifact":12322497620}]
 assert len(e["source_native_rgb_rois"])==len(EXPECTED)==6
 for actual,expected in zip(e["source_native_rgb_rois"],EXPECTED):
  assert (actual["key"],actual["pdf_page_1based"],actual["printed_day"],actual["field"],actual["literal"],actual["decimal"],actual["bbox"],actual["rgb_sha256"])==expected
 rows={z["key"]:z for z in e["source_native_rgb_rois"]}
 numbers={day:Decimal(rows[key]["decimal"]) for day,key in [(19,"P23_D19_CUM"),(20,"P23_D20_CUM"),(21,"P24_D21_CUM")]}
 assert numbers=={19:Decimal("8843.7571"),20:Decimal("9257.6000"),21:Decimal("9666.1509")}
 assert e["arithmetic"]["original_waseda_printed_day20_cumulative"]==str(numbers[20])
 assert e["arithmetic"]["original_waseda_printed_day21_cumulative"]==str(numbers[21])
 assert numbers[21]-numbers[20]==Decimal(e["arithmetic"]["exact_decimal_difference"])==Decimal("408.5509")
 assert e["arithmetic"]["received_korean_d20_long"]==next(x["long"] for x in yz["modern_received_rows"] if x["day"]==20)=="408.5509"
 assert e["arithmetic"]["original_waseda_d20_long_native_roi"]=="NOT_YET_DIRECTLY_COLLATED"
 assert e["arithmetic"]["global_waseda_cumulative_index_law"]=="NOT_ADJUDICATED"
 correction=e["correction"]
 old=next(z for z in bj["source_native_rgb_regions"] if z["id"]=="D20_CUMULATIVE")
 assert correction["prior_evidence"]==BJ and correction["legacy_source_roi_key"]==old["id"]
 assert correction["legacy_source_roi_exact_sha"]==old["original_rgb_pixel_sha256"]==rows["P23_D19_CUM"]["rgb_sha256"]
 assert old["original_rgb_roi_bbox"]==rows["P23_D19_CUM"]["bbox"]
 assert correction["legacy_labelled_printed_day"]==old["layout_day"]==20
 assert correction["source_original_corrected_printed_day"]==19
 assert correction["legacy_numeric_value_unchanged"]==old["decimal_value"]==str(numbers[19])
 assert correction["old_machine_evidence_preserved_forward_only"] is True
 assert correction["historical_original_bytes_or_numeric_digits_changed"] is False
 assert correction["previous_cumulative_D18_D19_D20_column_day_assignment"]=="SUPERSEDED_PENDING_EXPLICIT_CROSS_FOLIO_DAY_HEADER_REBIND"
 cross=e["cross_holding_local"]
 assert cross["naj_book51_source"]==BK
 assert cross["naj_printed_day20_cumulative"]==next(z["decimal"] for z in bk["original_native_rois"] if z["key"]=="D20_CUM")==str(numbers[19])
 assert cross["naj_printed_day21_cumulative"]==next(z["decimal"] for z in bk["original_native_rois"] if z["key"]=="D21_CUM")==str(numbers[20])
 assert cross["waseda_printed_day19_cumulative"]==str(numbers[19])
 assert cross["waseda_printed_day20_cumulative"]==str(numbers[20])
 assert cross["observation"]=="SAME_PAIR_ON_DIFFERENT_PRINTED_DAY_LABELS_SOURCE_LOCAL_ONLY"
 assert cross["independent_stemmatic_votes_added"]==0
 assert all(cross[k] is False for k in ("shared_exemplar_proven","whole_table_shift_law_proven","numerical_winner_selected"))
 assert all(e["negative_controls"].values())
 assert not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"]
 counts=e["scope_counters"]
 assert counts["original_images_reused"]==2 and counts["native_rgb_rois_newly_collated"]==4 and counts["heading_rois_independently_rechecked"]==2
 assert counts["open_issues"]==11 and counts["product"]=="CLOSED"
 for k in ("new_physical_witnesses","independent_numerical_votes","source_registry_added","matrix_rows_added","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens"):assert counts[k]==0
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["source_refs"].count(MD)==issue["source_refs"].count(P)==1 and issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 h=next(x for x in issue["history"] if x.get("revision_id")=="TW-OPEN-0005-WASEDA-DAY-HEADER-13BM")
 assert h["event"]=="ISSUE_REVISION" and set(h["changed_fields"])=={"evidence_boundary","missing_evidence","next_action"}
 assert h["previous_next_action"].startswith("13BL CURRENT ACTION")
 assert {P,MD,BJ,BK,YZ}.issubset(set(h["evidence_refs"]))
 assert "[13BM 2026-10-21 WASEDA NATIVE HEADER-LANE FORWARD ERRATUM]" in issue["evidence_boundary"]
 assert "[13BM 2026-10-21 REMAINING GLOBAL HEADER AND LONG LANE]" in issue["missing_evidence"]
 later=any(z.get("event")=="ISSUE_REVISION" and "next_action" in z.get("changed_fields",[])
           for z in issue["history"][issue["history"].index(h)+1:])
 prefix=ledger["binding"]["latest_research_focus_prefix"]
 assert issue["next_action"].startswith("13BM CURRENT ACTION") or (
  later and prefix!="13BM" and (issue["next_action"].startswith(prefix+" CURRENT ACTION") or issue["next_action"].startswith(next((z["revision_id"].split("-")[3]+" CURRENT ACTION" for z in reversed(issue["history"]) if "next_action" in z.get("changed_fields",[]) and len(z.get("revision_id","").split("-"))>3 and z["revision_id"].split("-")[3].startswith("13")),"__NO_RECORDED_ACTION__"))))
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert any(z.startswith("13BM ") for z in state["historical_audit"]["current_focus"])
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert prefix==state["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
 assert set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in ledger["issues"]}
 assert (ROOT/MD).is_file()
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser()
 ap.add_argument("--waseda-p23")
 ap.add_argument("--waseda-p24")
 a=ap.parse_args()
 e=load(P)
 assert check(e,load(BJ),load(BK),load(YZ),load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"),load("docs/PROJECT-CURRENT-STATE-R1.json"))
 if a.waseda_p23 or a.waseda_p24:
  assert a.waseda_p23 and a.waseda_p24
  assert actual_original_replay(e,a.waseda_p23,a.waseda_p24)
 print("13BM Waseda P23/P24 direct day header and cumulative forward erratum PASS")
