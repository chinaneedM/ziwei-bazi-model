#!/usr/bin/env python3
"""13IY: guard modern firstparty government/SNU discord without ancient-folio promotion."""
import json
from pathlib import Path
# Backward-looking assertions use append-only history, never overwrite live next_action.
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
R=Path(__file__).resolve().parents[1]
D="docs/research/TIANWEN-13IY-KHS-2114-1-DIRECT-KOREAN-DESIGNATION-COPY-SCOPE-R1.json"
S="docs/research/TIANWEN-13IY-KHS-2114-1-2114-2-OFFICIAL-DESCRIPTION-SOURCE-SHARD-R1.json"
def get(path):return json.loads((R/path).read_text(encoding="utf-8"))
def check(d=None,state=None,ledger=None,manifest=None):
 d=get(D) if d is None else d
 a=d["firstparty_2114_1"];b=d["separate_firstparty_2114_2"];c=d["snu_firstparty_metadata"];j=d["adjudication"]
 assert d["schema"]=="TIANWEN-13IY-KHS-2114-1-DIRECT-KOREAN-DESIGNATION-COPY-SCOPE-R1"
 assert d["issue_id"]=="TW-OPEN-0005"
 assert a["api_url"]=="https://www.khs.go.kr/cha/SearchKindOpenapiDt.do?ccbaKdcd=12&ccbaAsno=0021140000100&ccbaCtcd=11"
 assert a["source_discovered_official_page"]=="https://www.heritage.go.kr/heri/cul/culSelectDetail.do?ccbaCpno=1121121140100"
 assert (a["run_id"],a["job_id"],a["artifact_id"])==(40631928662,122630058347,12791554120)
 assert a["response_http"]==200 and a["raw_bytes"]==6398
 assert a["raw_sha256"]=="711ba17ffa8f09f091c04eea1de8a89ee1fd43ad35e8cd81318ccb4e2bfbec80"
 assert a["korean_description_length"]==2149 and a["description_sha256"]=="6b0f04d2186d9d191438c16630dcca378827241a566249def7e55d208dfbbf8b"
 assert a["identity_title_description_verified"] is True
 assert a["manuscript_replacement_book_ordinals"]==[8,12,26]
 assert a["manuscript_juan_ranges"]==[[19,21],[31,33],[73,74]]
 assert all(x in a["official_exact_korean_passage"] for x in ("권19∼권21(8책)","권31∼권33(12책)","권73∼권74(26책)"))
 assert a["designated_print_scope"]=={"books":43,"juan":131}
 assert a["total_catalog_set"]=={"books":46,"juan":139}
 assert a["whole_work_book_16_to_30_juan_span"]==[47,85]
 assert a["ancient_physical_target_folio"] is None and a["impression_year_exact_for_present_copy"] is None
 assert a["physical_rebindings_noted_by_government"] is True
 assert b["api_url"]=="https://www.khs.go.kr/cha/SearchKindOpenapiDt.do?ccbaKdcd=12&ccbaAsno=0021140000200&ccbaCtcd=11"
 assert b["raw_bytes"]==5414 and b["description_length"]==1759
 assert b["raw_sha256"]=="c8a7de9c9f0ff5a64674153e7dd2048b3e6bb7e6193e0f9f9d18d7fc9106a5b9"
 assert b["gk5554_book_range"]==[17,18] and b["gk5554_juan_span"]==[79,80,81,82]
 assert b["gk5553_comparator_designated_books"]==43 and b["gk5553_comparator_designated_juan"]==131
 assert b["original_physical_target_folio"] is None
 assert c["official_url"]=="https://kyudb.snu.ac.kr/book/view.do?book_cd=GK05553_00"
 assert c["catalog_total_books"]==46 and c["manuscript_replacements_listed"]==[8,26,29]
 assert c["book29_original_juan_title"] is None and c["physical_book29_juan81_83"]=="RETRACTED_UNBOUND"
 assert j["government_8_12_26_now_direct_firstparty_text"] is True and j["secondary_2021_8_12_26_not_an_independent_witness"] is True
 assert j["preferred_book_sequence"] is None and j["source_catalog_scope_not_original_leaf"] is True
 assert j["snu_8_26_29_not_retracted_without_original_edition_binding"] is True
 assert j["gk5553_all_46_missing_81_82_unproved"] is True
 assert j["gk5553_book29_to_juan81_83"]=="RETRACTED_UNBOUND"
 assert j["gk5554_individual_17_or_18_to_81_82"] is None
 assert d["impact"]=={"matrix":[222,222],"genealogy_nodes":252,"genealogy_edges":238,"open_issue_count":11,"chart":"CLOSED","algorithm_reopens":0,"independent_new_ancient_pages":0,"historical_numeric_winners":0,"genealogy_edges_added":0}
 assert d["transmission_impact"]["edges_supported"]==[]
 assert all(v is None for k,v in d["original_ancient_targets"].items() if k!="erroneous_13ei")
 assert d["original_ancient_targets"]["erroneous_13ei"]=="RETRACTED"
 state=get("docs/PROJECT-CURRENT-STATE-R1.json") if state is None else state
 ledger=get("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json") if ledger is None else ledger
 manifest=get("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json") if manifest is None else manifest
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,state["schema_version"].split(".")))>=(1,904,0)
 assert manifest["root_source_count"]==647 and manifest["extension_source_count"]>=116
 assert manifest["combined_source_count"]==manifest["root_source_count"]+manifest["extension_source_count"]>=763
 assert state["historical_audit"]["external_source_registry_extension_count"]==manifest["extension_source_count"]
 assert state["historical_audit"]["external_source_registry_total_unique_count"]==manifest["combined_source_count"]
 assert len(state["historical_audit"]["current_focus"])==ledger["binding"]["source_focus_count"]
 assert any(x.startswith("13IY ") for x in state["historical_audit"]["current_focus"])
 assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x["path"]==S and x["blob_sha"]=="1c99ec83c879efe0242a2672bde2f07d94b8c5a0" and x["source_count"]==2 for x in manifest["shards"])
 shard=get(S);assert len(shard["sources"])==2
 assert all(x["physical_glyph_authority"] is False and x["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" for x in shard["sources"])
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert D in issue["source_refs"] and S in issue["source_refs"]
 assert historical_action_view(issue).startswith(ledger["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert any(x.get("revision_id","").startswith("TW-OPEN-0005-13IY-") and x.get("previous_next_action","").startswith("13IX CURRENT ACTION:") for x in issue["history"])
 assert all(z in historical_action_view(issue) for z in ("GK03539_00","GK03579_00","GK03269_00","D1-D6","四分","初度","G893","NLC03130 solar D30","NLC03130 summer D14","NULL","13EI","RETRACTED"))
 assert any(x.get("revision_id","").startswith("TW-OPEN-0005-13IY-") and D in x.get("evidence_refs",[]) for x in issue["history"])
 assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
 return True
if __name__=="__main__":
 assert check()
 print("TIANWEN_13IY_DIRECT_FIRSTPARTY_MANUSCRIPT_BOOK_SCOPE_DIFFERENCE_PASS")
