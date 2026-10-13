#!/usr/bin/env python3
"""12VG: PKU 1869 secondary route cannot become a copy, glyph or plate vote."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/MING-DATONG-YEHUOBIAN-12VG-PKU-1869-SECONDARY-TO-FIRSTPARTY-ROUTE-R1.json"
PRIOR="docs/research/MING-DATONG-YEHUOBIAN-12UU-ORIGINAL-JUAN20-ACQUISITION-PACKET-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
LOCI={"GONGJIN","CLOCK_NOUN","BEIJING_WINTER_SUNRISE","BEIJING_SUMMER_SUNSET"}
def validate(data,prior,state):
 if data.get("schema")!="TIANWEN-12VG-PKU-1869-CROSSWALK-NONPROMOTION-GATE-R1" or data.get("status")!="PKU_1869_SECONDARY_HOLDING_LEAD_NOT_A_SOURCE_BOUND_PHYSICAL_COPY":raise ValueError("schema/scope")
 t=data.get("controlling_tokyo_1869",{})
 old={x["queue_id"]:x for x in prior["original_copy_candidates"]}
 ref=old["TOKYO_1869_6403148395"]
 if t.get("ncid")!="BB23196128" or t.get("physical_item")!="6403148395" or t.get("catalog")!=ref["source_catalog_url"] or t.get("physical_item") not in ref["source_issued_item_identifier"]:raise ValueError("Tokyo original item crosswalk")
 if t.get("source_issued_original_image_url") is not None or t.get("original_juan20_folio") is not None or t.get("first_party_glyph_votes")!=0 or t.get("earlier_preface_is_not_1827_edition_proof") is not True:raise ValueError("Tokyo unearned attestation")
 official=data.get("first_party_platform_evidence",[])
 if len(official)!=4 or {x.get("provider") for x in official}!={"Beijing University Library","祕籍琳琅","学苑汲古"} or any(x.get("item_1869_confirmed") is not False for x in official):raise ValueError("not item-specific first party")
 for x in official:
  if x.get("authority") not in ("FIRST_PARTY_DISCOVERY_GUIDANCE_NOT_ITEM_CATALOG","FIRST_PARTY_PLATFORM_DESCRIPTION_NOT_ITEM_CATALOG","FIRST_PARTY_LINKED_ITEM_SEARCH_ENTRANCE_ONLY","FIRST_PARTY_LINKED_MULTI_INSTITUTION_INDEX_ENTRANCE_ONLY"):raise ValueError("official platform evidence layer")
 p=data.get("candidate_1869",{})
 if p.get("secondary_source_url")!="https://www.guoxuedashi.com/shumu/gj-3053193xz.html" or p.get("claimed_holder")!="北京大學圖書館" or p.get("source_grade")!="UNVERIFIED_SECONDARY_BIBLIOGRAPHIC_HOLDING_LEAD":raise ValueError("secondary bibliographic status")
 for k in ("first_party_item_url","source_issued_shelfmark","first_party_physical_copy_identifier","first_party_edition_description","original_juan20_folio","source_issued_target_image_url","source_binary_sha256","target_page_sha256"):
  if p.get(k) is not None:raise ValueError("unearned item/impression/image: "+k)
 for k in ("confirmed_original_1869_revised_impression","independent_physical_copy_attested","has_direct_target_glyphs"):
  if p.get(k) is not False:raise ValueError("unverified copy: "+k)
 if p.get("independent_target_votes")!=0 or set(p.get("four_loci",{}))!=LOCI or any(x is not None for x in p["four_loci"].values()):raise ValueError("no original glyphs")
 steps=data.get("crosswalk_requirements",[])
 if [x.get("step") for x in steps]!=list("ABCDEF") or any(x.get("satisfied") is not False for x in steps):raise ValueError("requires six acquisition conditions")
 flags=data.get("source_identity_firewalls",{})
 if len(flags)!=12 or any(v is not True for v in flags.values()):raise ValueError("print state scope firewall")
 if data.get("controlling_prior_records",[])[:1]!=[PRIOR]:raise ValueError("prior queue")
 c=data.get("accounting",{})
 for k,v in (("matrix_rows",222),("audited_rows",222),("metadata_defects_repaired",45),("formal_batches",487),("latest_formal","12QD"),("root_sources",647),("extension_sources",43),("union_sources",690),("graph_nodes",252),("graph_edges",238),("product","CLOSED")):
  if c.get(k)!=v:raise ValueError("historical snapshot: "+k)
 for k in ("new_registry_rows","new_graph_nodes","new_graph_edges","new_original_target_images","new_independent_glyph_votes","algorithm_reopens"):
  if c.get(k)!=0:raise ValueError("unearned provenance promotion: "+k)
 h=state["historical_audit"]
 if tuple(map(int,state["schema_version"].split(".")))<(1,563,0) or not any(x.startswith("12VG ") for x in h["current_focus"]):raise ValueError("handoff not updated")
 if h["row_count"]!=222 or h["audited_row_count"]!=222 or h["external_source_registry_total_unique_count"]<690 or state["invariants"]["algorithm_reopen_count"]!=0:raise ValueError("current state regression")
 return {"status":"PASS","first_party_item_confirmed":False,"candidate_1869_glyph_votes":0,"six_unsatisfied_evidence_gates":6}
def verify(root=ROOT):
 def j(p):return json.loads((root/p).read_text(encoding="utf-8"))
 return validate(j(DOC),j(PRIOR),j(STATE))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,sort_keys=True))
