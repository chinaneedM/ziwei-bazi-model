#!/usr/bin/env python3
"""13T forward-only correction: decoded source pixels, not versioned extracted PNG bytes."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13T-NLC-GORYEOSA-CROSS-RUNTIME-PIXEL-DIGEST-CORRECTION-R1.json"
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def check(d):
 assert d["schema"]=="TIANWEN-13T-NLC-GORYEOSA-CROSS-RUNTIME-PIXEL-SHA-ERRATUM-R1"
 assert d["failed_workflow"]["run_id"]==39203880339 and d["failed_workflow"]["not_evidence_of_changed_underlying_pdf"] is True
 assert d["correction_technique"].startswith("use fitz.Pixmap")
 assert d["source_pdf_sha256"]=="2b9e51cc5f44a4d92d3cb4a63318605f78cc8ffb118853036655b65ed279a689"
 assert [x["pdf_page_1based"] for x in d["page_checks"]]==[2,16,17]
 assert [x["xref"] for x in d["page_checks"]]==[13,111,118]
 assert [x["decoded_grayscale_pixels_sha256"] for x in d["page_checks"]]==[
  "92da44e6c7b015d42f7e1a7768610f0cb65c0c153b2b4c0f1ed1c3a158d115b4",
  "d99f7233a4203f634b58f25ae7f9d554aeaf363108e48c71a12f32e04d310832",
  "fd8f9871e00f1f3b53882173c39d81e964ed81b517adb587652ceef0dbb018b7"]
 assert all(x["pixel_dimensions"]==[4296,3607] and x["pixel_channels"]=="GRAYSCALE_L" for x in d["page_checks"])
 assert d["safety"]["old_13r_13s_snapshot_overwritten"] is False and d["safety"]["original_13r_crop_sha_historic_retained"] is True
 assert all(d["safety"][k]==0 for k in ("new_original_glyph_votes","independent_physical_numeric_votes","algorithm_reopens","external_sources_added","transmission_edges_added"))
 assert d["safety"]["firstparty_nlc_catalog_linkage_proven"] is False and d["safety"]["open_research_issues"]==11 and d["safety"]["product_r1"]=="CLOSED"
 old=load(d["previous_evidence"]);assert old["serialization_contract"]["reference_stack"]=="PyMuPDF 1.26.7 / Pillow 12.3.0"
 code=(R/"scripts/replay-goryeosa-nlc-source-pixels-13s.py").read_text(encoding="utf-8")
 assert "fitz.Pixmap(doc,xref)" in code and "Image.frombytes" in code
 assert 'h(grayscale)==item["decoded_grayscale_pixels_sha256"]' in code
 assert 'h(raw)==rec["rgb_pixels_sha256"]' in code
 assert 'h(img["image"])==rec["expected_encoded_png_sha256"]' not in code
 state=load("docs/PROJECT-CURRENT-STATE-R1.json")
 ledger=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert tuple(map(int,state["schema_version"].split(".")))>=(1,679,0)
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"] and E[:-5]+".md" in issue["source_refs"]
 assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in ledger["issues"]}
 return True
if __name__=="__main__":print(json.dumps({"status":"PASS","source_pixel_checks":len(load(E)["page_checks"])}))
