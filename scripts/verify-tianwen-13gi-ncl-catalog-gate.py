#!/usr/bin/env python3
"""13GI: potential NCL first-party CSV route does not establish exact physical folio."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13GI-NCL-OPEN-DATA-CATALOG-CSV-GATE-R1.json"; S=R/"docs/PROJECT-CURRENT-STATE-R1.json"; L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13GI-NCL-OPEN-DATA-CATALOG-CSV-GATE-R1"
 assert e["grade"]=="OFFICIAL_METADATA_DATASET_LOCATOR_AND_REPRODUCIBLE_RETRIEVAL_PROBE_NOT_ITEM_CROSSWALK"
 assert e["sources"][0]["official_catalog_dataset"]=="https://data.gov.tw/dataset/6839"
 assert e["sources"][0]["official_file"]=="https://rbook.ncl.edu.tw/NCLSearch/rbook.csv"
 assert e["sources"][0]["target_record_retrieved"] is False
 r=e["retrieval"];assert r["github_actions_probe"]=="PENDING" and r["target_record_observed"] is None
 assert r["dataset_snapshot_sha256"] is None and r["total_records"] is None and r["matching_row_count"] is None
 t=e["targets"]
 assert t["mirror_call_number"]=="208 03130" and t["mirror_segment"]=="NCL-03130_09"
 for k in ("catalog_03130_record_verification","exact_physical_copy_identifier","source_original_folios","d9","d14","d30"):assert t[k] is None
 assert t["later_1909_d30_only"]=="四分九二二二"
 g=e["historical_guards"];assert g["old_d9_d14_d30"]==[None,None,None] and g["historic_fourfen_unit"] is None
 assert g["legacy_13ei"]=="RETRACTED" and g["g893_six"]=="OPEN"
 assert (g["verified_chart_algorithm_defect"],g["algorithm_reopens"],g["candidate_collapses"])==(0,0,0)
 assert e["counts"]=={"matrix_rows":222,"matrix_audited":222,"registry_sources":761,"genealogy_nodes":252,"genealogy_edges":238,"risks_open_or_blocked":11,"product":"CLOSED","new_sources":0,"new_physical_witnesses":0,"new_glyphs":0}
 assert not e["transmission_impact"]["edges_supported"]
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,838,0)
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ")[0]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert "docs/research/TIANWEN-13GI-NCL-OPEN-DATA-CATALOG-CSV-GATE-R1.json" in issue["source_refs"] and "docs/research/TIANWEN-13GI-NCL-OPEN-DATA-CATALOG-CSV-GATE-R1.md" in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13GI-OFFICIAL-CSV-GATE-20261025" for x in issue["history"])
 assert any(x.get("id")=="OMISSIONS-13GI-NCL-CSV-GATE-20261025" for x in l["checkpoint_log"])
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L));print("13GI_PASS_METADATA_PROBE_WITH_NO_UNVERIFIED_ITEM_OR_GLYPH")
