#!/usr/bin/env python3
"""13AF exact acquired PDF digests, separate 史部/子部, preserve forward correction."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13AF-UTOKYO-HANSEKI1995-DIRECT-PDF-SHA-AND-SHIBU-HOMOGRAPH-ERRATUM-R1.json"
def load(x):return json.loads((P/x).read_text(encoding="utf-8"))
def verify():
 e=load(E);assert e["schema"]=="TIANWEN-13AF-UTOKYO-HANSEKI1995-EXACT-SOURCE-PDF-ACQUISITION-AND-FORWARD-ERRATUM-R1"
 assert e["issue"]=="TW-OPEN-0005"
 ac=e["acquisition"];assert ac["run_id"]==39256688817 and ac["artifact_id"]==12188365046 and ac["run_conclusion"]=="success" and ac["local_original_byte_sha256_rechecked"]
 p=e["pdfs"];assert len(p)==3 and len({x["filename"] for x in p})==3
 assert [(x["filename"],x["pdf_pages"]) for x in p]==[("kansekimokuroku_11_shibu.pdf",152),("kansekimokuroku_12_shibu.pdf",187),("kansekimokuroku_90_errata_1.pdf",74)]
 assert p[0]["part"]=="史部" and p[0]["section"]=="正史類" and p[0]["printed_page_start"]==100
 assert p[1]["part"]=="子部" and p[1]["section"]=="諸子合刻類" and p[1]["printed_page_start"]==252
 assert all(re.fullmatch("[0-9a-f]{64}",q["sha256"]) and re.fullmatch("[0-9a-f]{64}",q["firstpage_native_rgb_sha256"]) and q["original_byte_count"]>1000000 for q in p)
 old=e["correction"];assert old["status"]=="ERRATUM_REVISED_FORWARD_ONLY" and old["prior_record_preserved_without_silent_rewrite"]
 prev=load(old["prior_evidence"]);assert len(prev["source"]["repository_section_files"])==3
 assert prev["source"]["repository_section_files"][1]["part"]=="SHIBU_12"
 assert "two History-section fascicle" in old["previous_claim"] and "12_shibu.pdf is the Philosophers-section" in old["corrected_claim"]
 sc=e["scope"]
 for x in ["historical_goryeosa_work52_original_image_acquired","physical_UTokyo_G2312_work52_folio","physical_UTokyo_G23194_work52_folio","whole_History_catalog_negative_search_proven","whole_152page_catalog_linewise_review_complete"]:
  assert sc[x] is False
 assert sc["original_D16_glyph"]==sc["original_D18_cumulative"]=="UNREAD"
 assert sc["direct_Historical_Goryeosa_numeric_votes_added"]==0 and sc["algorithm_reopens"]==0
 assert sc["remaining_open_issues"]==11 and sc["product"]=="CLOSED"
 st=load("docs/PROJECT-CURRENT-STATE-R1.json");le=load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
 assert st["schema_version"]==le["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert tuple(map(int,st["schema_version"].split(".")))>=(1,691,0)
 assert any(x.startswith("13AF ") for x in st["historical_audit"]["current_focus"])
 assert le["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert le["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
 assert st["historical_audit"]["external_source_registry_total_unique_count"]>=739
 assert st["historical_audit"]["external_source_registry_total_unique_count"]==load("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")["combined_source_count"]
 i=next(x for x in le["issues"] if x["id"]=="TW-OPEN-0005")
 assert i["status"]=="OPEN" and all(x in i["source_refs"] for x in [E,"docs/research/TIANWEN-13AF-UTOKYO-HANSEKI1995-DIRECT-PDF-SHA-AND-SHIBU-HOMOGRAPH-ERRATUM-R1.md"])
 assert any(x["event"]=="FORWARD_ONLY_ERRATUM_13AE_SHIBU_ROMANIZED_CLASSIFICATION" for x in i["history"])
 assert len(le["issues"])==11 and le["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 return True
if __name__=="__main__":
 assert verify()
 print("TIANWEN_13AF_UTOKYO_CATALOG_ORIGINAL_SHA_AND_SHIBU_ERRATUM_PASS")
