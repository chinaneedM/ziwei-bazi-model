#!/usr/bin/env python3
"""13BU source boundary and provider original folio acquisition gate."""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BU-GORYEOSA-WASEDA-D16-FOLIO-SEAM-AND-PRECEDING-SOURCE-R1.json"
MD="docs/research/TIANWEN-13BU-GORYEOSA-WASEDA-D16-FOLIO-SEAM-AND-PRECEDING-SOURCE-R1.md"
BS="docs/research/TIANWEN-13BS-GORYEOSA-WASEDA-D16-NAJ-D18-D19-SOURCE-NATIVE-GLYPH-COLLATION-R1.json"
BT="docs/research/TIANWEN-13BT-GORYEOSA-NAJ-C18-D18-D19-DIRECT-CUMULATIVE-AND-PRINTED-HEADING-GEOMETRY-R1.json"
BQ="docs/research/TIANWEN-13BQ-GORYEOSA-NUMERIC-PARALLELS-HEADING-GRADE-AND-LEGACY-ATTRIBUTION-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
ROIS=[["D16_TERMINAL_RULE_AND_LONG",[1360,330,1464,1470],"7f3a509a962408fd1192d6b475b7880e8c1cb06365d40b258c0f79eeb50f5245","BOUNDED_ORIGINAL_RIGHT_FOLIO_LEFTMOST_DAY16_RULE_AND_LONG_CONTEXT"],["D16_LONG_SHORT_WIDE",[1404,675,1520,1430],"bddcbc0d93f0a9893ae6d45be4c47618b578d357580b7672308b2f1ba282ee68","CONTEXT_NOT_AN_ISOLATED_CUMULATIVE_FIELD"],["PHYSICAL_FOLIO_GUTTER",[1170,330,1390,1490],"ce994ed0071a440f72439ec62591e25ea143b0de829d0c502fd3c987e03563e4","SOURCE_FOLIO_GUTTER_AND_SPACING"],["D17_SIDE_OUTER_NUMERIC_CANDIDATE",[1102,680,1164,1420],"34e91aab7aeee92d90513343f0d31383814cbcd5654d5fddb9d7a722f5e9c210","PREVIOUS_CUMULATIVE_CANDIDATE_NOT_REBOUND_TO_DAY16"],["LEFT_FOLIO_D17_CONTEXT",[965,345,1170,1450],"f4ce4be0e4a45955684663870905d9cc00072ad8acacf4d77e12433b94c8a9de","DAY17_CONTEXT_FOR_TABLE_READING_NOT_NEW_DAY16_FACT"]]
def load(p):return json.loads((R/p).read_text(encoding="utf8"))
def replay_original(e,image):
 from PIL import Image
 raw=Path(image).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==e["source"]["known_embedded_jpeg_sha256"]
 with Image.open(image) as im:
  rgb=im.convert("RGB")
  assert list(rgb.size)==e["source"]["image_dimensions"]
  for z in e["prior_p23_original_rgb_guard_rois"]:
   assert hashlib.sha256(rgb.crop(tuple(z["bbox"])).tobytes()).hexdigest()==z["rgb_sha256"]
 return True
def check(e,st,ledger,prev):
 assert e["schema"]=="TIANWEN-13BU-WASEDA-D16-SOURCE-FOLIO-SEAM-AND-PRIOR-PAGES-RETRIEVAL-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["date"]=="2026-10-21"
 assert e["evidence_grade"]=="DIRECT_SHA_BOUND_SOURCE_IMAGE_GEOMETRY_NO_NEW_NUMERIC_GLYPH_DECISION"
 src=e["source"]
 assert src["holding"]=="WASEDA-RI06-02809-BOOK33"
 assert src["pdf_sha256"]=="28ebfeb34191f45715bc449d27da61fe04fb05eb45e84dd00cf569699f46225f"
 assert src["known_pdf_page_1based"]==23 and src["known_image_xref"]==70
 assert src["known_embedded_jpeg_sha256"]==prev["BS"]["source_images"][0]["jpeg_sha256"]
 assert src["image_dimensions"]==[2592,1728] and src["same_old_artifact_id"]==12340588249
 assert [(z["key"],z["bbox"],z["rgb_sha256"],z["role"]) for z in e["prior_p23_original_rgb_guard_rois"]]==[tuple(z) for z in ROIS]
 assert e["bounded_neighbor_pdf_pages_1based"]==[20,21,22]
 assert e["original_neighbor_page_image_readings"]=="NOT_YET_OBTAINED_OR_VISUALLY_REVIEWED"
 assert e["neighbor_source_jpeg_sha256"]=="PENDING_SOURCE_RUN"
 assert e["workflow"]==".github/workflows/probe-goryeosa-waseda-folio-seam-13bu.yml" and e["script"]=="scripts/probe-goryeosa-waseda-folio-seam-13bu.py"
 a=e["local_original_observation"]
 assert a["day16_heading"]=="十六日" and a["day16_long"]=="429.6073" and a["day16_short"]=="5.1362"
 assert a["d16_same_heading_isolated_cumulative"]=="UNBOUND"
 assert a["d17_side_outer_numeric_candidate_value"]=="NOT_ADJUDICATED"
 assert a["whole_table_index_rule"]=="UNPROVEN" and a["d16_archetype_one_vs_two"]=="UNRESOLVED"
 assert e["source_dependencies"]=={"prior_d16_source_original":BS,"prior_naj_field_geometry":BT,"prior_bq_field_day_grade":BQ}
 assert prev["BT"]["comparison"]["uniform_all_field_day_shift_proven"] is False
 fw=e["scope"]
 assert all(fw[k]==0 for k in ("new_physical_witnesses","new_source_registry_entries","independent_stemmatic_votes","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"))
 assert fw["research_risks_open_or_blocked"]==len(ledger["issues"])==11 and fw["chart_r1"]=="CLOSED"
 assert e["transmission_impact"]["nodes_added"]==e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 issue=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["source_refs"].count(MD)==issue["source_refs"].count(P)==1
 assert issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 rev=next(z for z in issue["history"] if z.get("revision_id")=="TW-OPEN-0005-WASEDA-D16-FOLIO-SEAM-13BU")
 assert rev["previous_next_action"].startswith("13BT CURRENT ACTION")
 assert {MD,P,BS,BT,BQ}.issubset(set(rev["evidence_refs"]))
 later=any("next_action" in v.get("changed_fields",[]) for v in issue["history"][issue["history"].index(rev)+1:])
 prefix=ledger["binding"]["latest_research_focus_prefix"]
 assert issue["next_action"].startswith("13BU CURRENT ACTION") or (later and prefix!="13BU" and (issue["next_action"].startswith(prefix+" CURRENT ACTION") or issue["next_action"].startswith(next((z["revision_id"].split("-")[3]+" CURRENT ACTION" for z in reversed(issue["history"]) if "next_action" in z.get("changed_fields",[]) and len(z.get("revision_id","").split("-"))>3 and z["revision_id"].split("-")[3].startswith("13")),"__NO_RECORDED_ACTION__"))))
 assert ledger["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert ledger["binding"]["reviewed_state_version"]==st["schema_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert any(x.startswith("13BU ") for x in st["historical_audit"]["current_focus"])
 assert prefix==st["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert ledger["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 assert set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in ledger["issues"]}
 assert (R/MD).is_file()
 return True
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("--source-p23");args=a.parse_args()
 e=load(P)
 assert check(e,load(S),load(L),{"BS":load(BS),"BT":load(BT),"BQ":load(BQ)})
 if args.source_p23:assert replay_original(e,args.source_p23)
 print("13BU original physical folio seam image hashes and bounded p20-p22 source gate PASS")
