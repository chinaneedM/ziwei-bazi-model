#!/usr/bin/env python3
"""12VH: received work parallels must not be promoted to source-bound original plate votes."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/MING-DATONG-YEHUOBIAN-12VH-YUJIDENG-RECEIVED-PARALLEL-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
def validate(d,s):
    if d.get("schema")!="TIANWEN-12VH-YUJIDENG-RECEIVED-ADMINISTRATIVE-CONTROL-R1" or d.get("status")!="RECEIVED_PARALLEL_NO_ORIGINAL_LEAF_PROMOTION":raise ValueError("scope")
    ww=d.get("witnesses",[])
    if [w.get("id") for w in ww]!=["MING_SHILU","YU_JIDENG","YEHUOBIAN","SHANGHAI_12QC"]:raise ValueError("witness identity")
    vv=[("辰初一刻","戌初一刻","宮禁",None),("辰初一刻","戌初一刻",None,None),("辰初二刻","戌初二刻","官禁","官漏"),("辰初一刻","戌初一刻","宮禁","宮漏")]
    for w,v in zip(ww,vv):
        if tuple(w.get(k) for k in ("winter","summer","gongjin","clock"))!=v:raise ValueError("four loci")
    if [x.get("grade") for x in ww]!=["RECEIVED_TEXT"]*3+["PRIOR_DIRECT_PAGE_NOT_RECHECKED"]:raise ValueError("new original claim")
    if ww[1]["url"]!="https://ctext.org/wiki.pl?chapter=349188&if=gb":raise ValueError("Yu locator")
    firewall=d.get("nonpromotion",{})
    if len(firewall)!=7 or not all(v is True for v in firewall.values()):raise ValueError("unsupported relationship")
    c=d.get("accounting",{})
    snapshot={"matrix_rows":222,"audited_rows":222,"metadata_repairs":45,"formal_batches":487,"latest_formal":"12QD","root_sources":647,"extension_sources":43,"union_sources":690,"graph_nodes":252,"graph_edges":238,"product":"CLOSED"}
    for k,v in snapshot.items():
        if c.get(k)!=v:raise ValueError("historical snapshot "+k)
    for k in ("new_original_pages","new_glyph_votes","new_source_rows","new_graph_edges","algorithm_reopens"):
        if c.get(k)!=0:raise ValueError("unearned promotion "+k)
    impact=d.get("transmission_impact",{})
    for k in ("nodes_added","edges_supported","edges_revised"):
        if impact.get(k)!=[]:raise ValueError("genealogy edge")
    h=s.get("historical_audit",{})
    if tuple(map(int,s.get("schema_version","0.0.0").split(".")))<(1,564,0):raise ValueError("handoff version")
    if not any(x.startswith("12VH ") for x in h.get("current_focus",[])):raise ValueError("handoff focus")
    if h.get("row_count")!=222 or h.get("audited_row_count")!=222 or h.get("external_source_registry_total_unique_count",0)<690:raise ValueError("state counters")
    if s.get("invariants",{}).get("algorithm_reopen_count")!=0:raise ValueError("algorithm invariant")
    return {"status":"PASS","new_glyph_votes":0,"original_1827_1869_pages":0}
if __name__=="__main__":
    root=ROOT
    print(json.dumps(validate(json.loads((root/DOC).read_text()),json.loads((root/STATE).read_text())),ensure_ascii=False,sort_keys=True))
