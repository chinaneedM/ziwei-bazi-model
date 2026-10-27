#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-12ZI-GORYEOSA-5554-FIRSTPARTY-PARATEXT-COUNT-AND-BOOK52-CLOSURE-GATE-R1.json"
PREV="docs/research/TIANWEN-12ZH-GORYEOSA-5554-98V105-ENUMERATION-AND-V52-BOOK-BOUNDARY-R1.json"
def load():
 return tuple(json.loads((ROOT/x).read_text(encoding="utf-8")) for x in (P,PREV,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def check(test,why):
 if not test:raise ValueError(why)
def verify(d,old,state,ledger):
 check(d["schema"]=="TIANWEN-12ZI-GORYEOSA-5554-PARATEXT-COUNT-AND-BOOK52-GATE-R1" and d["prior"]==PREV,"schema/prior")
 first=d["first_party_rechecks"];a=first["kyujanggak_overview"];b=first["kyujanggak_5554_item"];h=first["heritage_count"];r=d["bounded_received_enumerations"];m=d["constrained_model"]
 check("卷首1 목록2 137권 46책" in a["gk5553_literal"] and "32책" in a["gk5554_literal"] and a["v52_book_number_in_5554"] is None,"first party scope")
 check(b["item"]=="GK05554_00" and b["impression_year"]=="[刊年未詳]" and b["printed_v52_folio"] is None and b["crosspointed_mf_label"]=="奎 5553","scope and microfilm")
 check(h["declared_work_volume_count"]==98 and h["physical_books"]==32 and h["year_classification"]=="1482年","heritage")
 check(r["third_party_heritage_republication"]["source_type"].startswith("SECONDARY_") and r["secondary_scholarly_account"]["source_type"].startswith("SECONDARY_"),"source levels")
 x=old["received_enumerations"];check(r["third_party_heritage_republication"]["enumerated_numbered_work_volumes"]==x["republished_heritage"]["computed_distinct_numbered_work_volumes"]==95 and r["secondary_scholarly_account"]["enumerated_numbered_work_volumes"]==x["secondary_scholarly"]["computed_distinct_numbered_work_volumes"]==100,"forward old math")
 check(m["whole_work_ordinal_body_volumes"]==137 and m["whole_work_numbered_catalog_volumes"]==2 and m["whole_work_total_when_catalogs_included"]==139 and m["first_party_other_copy_gk5553_extra_preface_unit_count"]==1,"other-copy composition")
 check(m["last_batch_heritage_enumeration_gap"]==h["declared_work_volume_count"]-95==3 and m["last_batch_secondary_enumeration_gap"]==r["secondary_scholarly_account"]["published_total"]-100==5,"reported gaps")
 check(m["conditional_heritage_sum_if_both_catalog_and_preface_units_survive_5554"]==95+2+1==98,"conditional arithmetic")
 check(m["conditional_scholarly_sum_if_both_catalog_and_preface_units_survive_5554"]==100+2+1==103 and m["conditional_remaining_scholarly_gap_after_three_extras"]==105-103==2,"no fabricated full reconciliation")
 check(m["gk5554_catalog_and_preface_unit_actual_physical_survival"]=="NOT_PROVEN_IN_FIRST_PARTY_ITEM_SPECIFIC_COLLATION" and m["same_gk5553_counting_schema_applicable_to_gk5554"]=="UNVERIFIED" and m["counts_98_and_105_historically_adjudicated"] is False,"no illicit transfer")
 check(m["item_5554_v52_exact_physical_book"] is None and m["original_5554_v52_d16_glyph"] is None and m["original_5554_v52_d18_glyph"] is None,"no original invented")
 for k in ("new_original_pixel_hashes","new_stemmatic_physical_witnesses","new_source_registry_entries","new_transmission_edges","algorithm_reopens"):check(m[k]==0,k)
 check(m["g893_principal_original_controls"]=="5/6" and m["g893_cross_original_decisions"]=="0/6" and m["research_open_issues"]==11 and m["deterministic_fusion_chart_product"]=="CLOSED","invariants")
 issue=next(v for v in ledger["issues"] if v["id"]=="TW-OPEN-0005")
 check(issue["status"]=="OPEN" and P in issue["source_refs"] and P.replace(".json",".md") in issue["source_refs"],"issue refs")
 f=state["historical_audit"]["current_focus"]
 check(any(z.startswith("12ZI ") for z in f) and ledger["binding"]["latest_research_focus_prefix"]==f[-1].split(" ",1)[0] and ledger["binding"]["source_focus_count"]==len(f),"forward focus")
 check(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"],"state version")
 check(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])=={x["id"] for x in ledger["issues"]},"review checkpoints")
 return {"status":"PASS","source_layer":"CATALOG_COUNTS_ONLY","image_target":None,"unresolved_105_remaining_gap":2}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
