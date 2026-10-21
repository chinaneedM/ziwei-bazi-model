#!/usr/bin/env python3
"""13BR bounded acquisition definition, source lineage, and no false evidence closure."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BR-GORYEOSA-WASEDA-D16-NAJ-D18-D19-BOUNDED-SOURCE-ACQUISITION-R1.json"
M="docs/research/TIANWEN-13BR-GORYEOSA-WASEDA-D16-NAJ-D18-D19-BOUNDED-SOURCE-ACQUISITION-R1.md"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(path):return json.loads((R/path).read_text(encoding="utf-8"))
def check(e,state,ledger):
 from importlib import util
 a=R/"scripts/acquire-goryeosa-original-target-rois-13br.py"
 spec=util.spec_from_file_location("goryeosa13br",a)
 mod=util.module_from_spec(spec);spec.loader.exec_module(mod)
 assert mod.validate_spec(e)
 assert e["requested_workflow"]==".github/workflows/acquire-goryeosa-original-target-rois-13br.yml"
 assert e["output_receipt_schema"]=="TIANWEN-13BR-ORIGINAL-CANDIDATE-ROI-RECEIPT"
 assert e["access_failure"]=="RECORD_AS_ENVIRONMENT_BOUNDARY_NOT_AS_ABSENCE"
 assert e["next_action"].startswith("Inspect archived SHA-verified ROI")
 assert e["transmission_impact"]["nodes_added"]==e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 assert (R/M).is_file()
 issue=next(v for v in ledger["issues"] if v["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["source_refs"].count(M)==issue["source_refs"].count(P)==1
 assert issue["source_refs"].index(P)==issue["source_refs"].index(M)+1
 rev=next(v for v in issue["history"] if v.get("revision_id")=="TW-OPEN-0005-EXACT-SOURCE-ROI-ACQUISITION-13BR")
 assert rev["previous_next_action"].startswith("13BQ CURRENT ACTION")
 assert {M,P,"docs/research/TIANWEN-13BO-GORYEOSA-WASEDA-P23-D17-D18-ORIGINAL-HEADER-CUMULATIVE-LONG-R1.json","docs/research/TIANWEN-13BK-GORYEOSA-NAJ-CANVAS18-D19-LONG-D20-D21-CUMULATIVE-R1.json"}.issubset(set(rev["evidence_refs"]))
 later=any("next_action" in z.get("changed_fields",[]) for z in issue["history"][issue["history"].index(rev)+1:])
 prefix=ledger["binding"]["latest_research_focus_prefix"]
 assert issue["next_action"].startswith("13BR CURRENT ACTION") or (later and prefix!="13BR" and issue["next_action"].startswith(prefix+" CURRENT ACTION"))
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert any(z.startswith("13BR ") for z in state["historical_audit"]["current_focus"])
 assert prefix==state["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
 assert set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in ledger["issues"]}
 return True
if __name__=="__main__":
 assert check(load(P),load(S),load(L))
 print("13BR strict original-image acquisition definition and forward-only state PASS")
