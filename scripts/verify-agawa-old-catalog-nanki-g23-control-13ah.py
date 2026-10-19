#!/usr/bin/env python3
"""Fail-closed validation of G23 provenance controls and early Agawa bibliography."""
import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AH-AGAWA-OLD-CATALOG-AND-G23-NANKI-CONTROL-R1.json"
S="docs/research/TIANWEN-13AH-AGAWA-OLD-CATALOG-G23-NANKI-SOURCE-SHARD-R1.json"
M="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
def load(path):return json.loads((P/path).read_text(encoding="utf-8"))
def verify():
 e=load(E);s=load(S);m=load(M)
 assert e["schema"]=="TIANWEN-13AH-AGAWA-EARLY-CATALOG-KYUSHU-HOLDING-AND-G23-NANKI-PREFIX-COUNTEREXAMPLE-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 k=e["early_agawa_bibliography"];assert k["ncid"]=="BA63404722" and k["compiler"]=="古關吉雄" and k["extent"]=="96丁"
 assert k["date_prior_to_1998_proven"] is False and k["original_catalog_folios_acquired"] is False
 ky=e["kyushu_firstparty"];assert ky["call_number"]=="石崎文庫/029-ア-1/1" and ky["individual_registration"]=="003132003022182"
 assert ky["same_item_as_CiNii_record"] is True and ky["digitized_fulltext_claim"] is False
 tok=e["utokyo_g23_nanki_control"]
 assert tok["call_number"]=="G23:236" and tok["firstparty_collection"]=="南葵文庫"
 assert "南葵文庫" in tok["physical_stamps_listed"] and tok["stamp_described_by_firstparty_catalog"]
 assert tok["stamp_observed_directly_from_original_image"] is False
 assert tok["prefix_G23_exclusive_Agawa"] is False and tok["prefix_G23_exclusive_Nanki"] is False
 assert tok["prefix_proves_either_target_ownership"] is False
 target=e["target_work52_items"];assert len(target)==2
 assert {x["call_number"] for x in target}=={"G23:12","G23:194"}
 assert all(x["Nanki_provenance"]=="UNVERIFIED" and x["Agawa_provenance"]=="UNVERIFIED" and x["day16_original_value"] is None for x in target)
 c=e["comparison"];assert c["Koseki_CiNii_and_Kyushu_same_physical_holding"] and c["G23_Nanki_counterexample_is_different_book"]
 assert c["new_historical_numeric_votes"]==c["raw_Goryeosa_original_images_acquired"]==c["algorithm_reopens"]==0
 assert c["open_omissions"]==11 and c["product"]=="CLOSED"
 assert len(s["sources"])==3 and len({x["source_id"] for x in s["sources"]})==3
 assert all(x["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and x["physical_glyph_authority"] is False for x in s["sources"])
 assert m["root_source_count"]==647 and m["extension_source_count"]>=99 and m["combined_source_count"]>=746
 assert any(x["path"]==S and x["schema"]==s["schema"] and x["source_count"]==3 for x in m["shards"])
 st=load("docs/PROJECT-CURRENT-STATE-R1.json");le=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert tuple(map(int,st["schema_version"].split(".")))>=(1,693,0)
 assert st["schema_version"]==le["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert le["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert le["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert st["historical_audit"]["external_source_registry_total_unique_count"]==m["combined_source_count"]
 assert any(x.startswith("13AH ") for x in st["historical_audit"]["current_focus"])
 issue=next(x for x in le["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and all(x in issue["source_refs"] for x in (E,"docs/research/TIANWEN-13AH-AGAWA-OLD-CATALOG-AND-G23-NANKI-CONTROL-R1.md",S))
 assert any(x["event"]=="G23_NANKI_FIRSTPARTY_COUNTEREXAMPLE_AND_KYUSHU_OLDER_AGAWA_LIST" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13AH-G23-NANKI-AND-KYUSHU-AGAWA-LIST-20261019" for x in le["checkpoint_log"])
 assert len(le["issues"])>=11 and le["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 return True
if __name__=="__main__":
 assert verify()
 print("TIANWEN_13AH_G23_NANKI_COUNTEREXAMPLE_AND_AGAWA_CATALOG_PASS")
