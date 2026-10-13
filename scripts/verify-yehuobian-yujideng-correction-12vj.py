#!/usr/bin/env python3
"""12VJ: enforce correction from inferred Peng attribution to Yu's unassigned paragraph."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/MING-DATONG-YEHUOBIAN-12VJ-YUJIDENG-NO-ATTRIBUTION-FORWARD-CORRECTION-R1.json"
VH="docs/research/MING-DATONG-YEHUOBIAN-12VH-YUJIDENG-RECEIVED-PARALLEL-R1.json"
VI="docs/research/MING-DATONG-YEHUOBIAN-12VI-NCL-YUJIDENG-TWO-COPIES-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
def validate(doc,prior,previous,state):
    if doc.get("schema")!="TIANWEN-12VJ-ATTRIBUTION-SCOPE-FORWARD-CORRECTION-R1" or doc.get("status")!="EARLIER_YU_CHAPTER11_PENG_DEQING_ATTRIBUTION_WITHDRAWN_NOT_GLYPHS":raise ValueError("not a forward-only correction")
    revisions=doc.get("supersedes_assertion_scopes",[])
    if len(revisions)!=2 or revisions[0].get("file")!=VH or revisions[0].get("old_claim")!="卷十一彭德清奏摘要" or revisions[0].get("corrected_claim")!="卷十一独立南京、北京北极出地及二至日出入记述；目标段未明确署彭德清":raise ValueError("old attribution not scoped")
    if not all(x.get("historical_file_unchanged") is True for x in revisions):raise ValueError("historical forward-only policy")
    old=next((w for w in prior.get("witnesses",[]) if w.get("id")=="YU_JIDENG"),None)
    if old is None or old.get("locus")!="卷十一彭德清奏摘要" or old.get("winter")!="辰初一刻" or old.get("summer")!="戌初一刻":raise ValueError("immutable prior snapshot")
    if previous.get("schema")!="TIANWEN-12VI-NCL-YUJIDENG-MING-COPY-ACCESS-GATE-R1" or {x.get("catalog_id") for x in previous.get("catalog_records",[])}!={"02253","02254"}:raise ValueError("old copy register")
    e=doc.get("scoped_evidence",[])
    expected={"YU_CTEXT_349188","YU_WIKISOURCE_CH11","MING_SHILU_160","YEHUOBIAN_CTEXT","YU_SHIDIAN_CADAL_LABEL"}
    if len(e)!=5 or {x.get("witness_id") for x in e}!=expected:raise ValueError("correction witnesses")
    refs={x["witness_id"]:x for x in e}
    for w in ("YU_CTEXT_349188","YU_WIKISOURCE_CH11"):
        x=refs[w]
        if x.get("attributed_to_peng_in_target_paragraph") is not False or (x.get("winter"),x.get("summer"))!=("辰初一刻","戌初一刻") or x.get("direct_physical_leaf_reviewed") is not False:raise ValueError("Yu is not explicit Peng memorial")
    if refs["YU_CTEXT_349188"].get("preceding_subject")!="正統十二年馬愉卒追贈兩官" or refs["YU_CTEXT_349188"].get("followup_subject")!="郭璡為福建參議時年二十四":raise ValueError("exact section boundary")
    for w,reading in (("MING_SHILU_160",("辰初一刻","戌初一刻")),("YEHUOBIAN_CTEXT",("辰初二刻","戌初二刻"))):
        x=refs[w]
        if x.get("attributed_to_peng_in_target_paragraph") is not True or (x.get("winter"),x.get("summer"))!=reading or x.get("direct_physical_leaf_reviewed") is not False:raise ValueError("separate explicit Peng attribution")
    if refs["MING_SHILU_160"].get("explicit_attribution")!="欽天監監正彭德清言":raise ValueError("Shilu attribution")
    sd=refs["YU_SHIDIAN_CADAL_LABEL"]
    if sd.get("source_label")!="CADAL02047821" or any(sd.get(k) is not False for k in ("physical_edition_verified","scan_to_ncl_02253_or_02254_verified","original_juan11_leaf_downloaded")):raise ValueError("Shidian source link is not physical image")
    fw=doc.get("philology_and_provenance_firewalls",{})
    if len(fw)!=10 or any(v is not True for v in fw.values()):raise ValueError("same phrase is not descent")
    target=doc.get("target_status",{})
    for k in ("original_1827_yehuobian_juan20_target_folio","original_1869_yehuobian_juan20_target_folio","yu_juan11_original_print_leaf","original_file_sha256","page_sha256"):
        if target.get(k) is not None:raise ValueError("unearned original source")
    if target.get("attribution_of_juan11_pair_to_peng")!="NOT_STATED_IN_TARGET_PARAGRAPH" or target.get("transmission_from_shilu_to_yu")!="UNPROVEN":raise ValueError("unearned textual genealogy")
    counts=doc.get("accounting",{})
    historical={"matrix_rows":222,"audited_rows":222,"metadata_repairs":45,"formal_batches":487,"latest_formal":"12QD","root_sources":647,"extension_sources":43,"total_sources":690,"graph_nodes":252,"graph_edges":238,"product":"CLOSED"}
    for k,v in historical.items():
        if counts.get(k)!=v:raise ValueError("snapshot "+k)
    for k in ("new_registered_sources","new_graph_nodes","new_graph_edges","new_original_target_images","new_independent_original_glyph_votes","new_algorithm_reopens"):
        if counts.get(k)!=0:raise ValueError("unearned promotion "+k)
    ti=doc.get("transmission_impact",{})
    if any(ti.get(k) for k in ("nodes_added","edges_supported","edges_revised")):raise ValueError("false genealogy")
    h=state.get("historical_audit",{})
    if tuple(map(int,state.get("schema_version","0.0.0").split(".")))<(1,566,0) or not any(x.startswith("12VJ ") for x in h.get("current_focus",[])):raise ValueError("handoff correction missing")
    if (h.get("row_count"),h.get("audited_row_count"))!=(222,222) or h.get("external_source_registry_total_unique_count",0)<690 or state["invariants"]["algorithm_reopen_count"]!=0:raise ValueError("live state invariant")
    return {"status":"PASS","corrected_attribution_claims":1,"original_glyph_votes":0,"new_source_rows":0}
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
if __name__=="__main__":
    print(json.dumps(validate(read(DOC),read(VH),read(VI),read(STATE)),ensure_ascii=False,sort_keys=True))
