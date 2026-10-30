#!/usr/bin/env python3
"""13LV manifest-only book relationship; prevent fabricated volume1 or juan35."""
import json
from pathlib import Path
# Archived action terms come from preserved revisions, never from stale live next_action.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13LV-BSB-MINGSHI-ORIGINAL-MANIFEST-OPAC-AND-RELATIONS-ROUTE-R1.json"
def load():return tuple(json.loads((ROOT/p).read_text(encoding="utf8")) for p in [E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"])
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13LV-BSB-MINGSHI-ORIGINAL-MANIFEST-OPAC-AND-RELATIONS-ROUTE-R1" and e["issue_id"]=="TW-OPEN-0005"
 d=e["direct_first_party_links"];a=e["metadata_acquisition"];c=e["counts"]
 assert d["opac"]=="https://opacplus.bsb-muenchen.de/title/BV039968895"
 assert d["details"]=="https://mdz-nbn-resolving.de/details:bsb11166692"
 assert d["source_manifest_provided_explicit_sibling_volume1_identifier"] is False
 assert d["source_manifest_provided_juan35_original_leaf_identifier"] is False
 assert e["source_identifiers"]["exact_1739_physical_print_date_proven"] is False
 assert a["zip_sha256"]=="dcd8385c7a648216da9cdb5813adc143ac237ceb637a33ac8524109e02ce0547"
 assert a["zip_bytes"]==2070 and a["permanent_archive"]["library_file_id"]=="libfile_191afe87a5608191860186892d2ae899"
 for name in ["new_target_original_juan35_glyph","sibling_first_volume_verified","source_page_juan35_absence_proven","original_1739_print_copy_verified"]:
  assert e["adjudication"][name] is False
 assert e["follow_up_first_party_probe"]["opac_access_status"]=="UNRUN"
 assert e["adjudication"]["algorithm_reopens"]==e["adjudication"]["historical_numeric_winners_added"]==0
 assert e["adjudication"]["chart"]=="CLOSED"
 assert e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 assert c==dict(sources=765,matrix_rows=222,matrix_audited=222,genealogy_nodes=252,genealogy_edges=238,open_issues=11,g893_six_numeric_winners=0,product="CLOSED")
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,963,0)
 assert any(x.startswith("13LV ") for x in s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert len(s["historical_audit"]["current_focus"])==l["binding"]["source_focus_count"]
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and "13LV CURRENT ACTION:" in historical_action_view(issue)
 assert "13LT CURRENT ACTION:" in historical_action_view(issue) and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13LV-BSB-MANIFEST-OPAC-20261030" for x in issue["history"])
 return {"status":"PASS","official_opac_route":True,"source_glyphs_juan35":0,"numeric_winners":0}
if __name__=="__main__":print(json.dumps(check(*load()),ensure_ascii=False))
