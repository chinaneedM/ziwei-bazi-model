#!/usr/bin/env python3
"""12VE source-scoped Chinese philology: printing is not completion nor Shiguan submission."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12VE-THREE-PREDICATES-OF-SHENZHEN-PARATEXT-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
def validate(r,st):
 if r.get("schema")!="TIANWEN-12VE-SHENZHEN-PARATEXT-SEMANTIC-DISTINCTION-R1" or r.get("status")!="RECEIVED_TEXT_ONLY_ORIGINAL_PHYSICAL_LEAVES_UNVERIFIED": raise ValueError("schema/status")
 w=r.get("witnesses",[])
 if len(w)!=3 or any(v.get("physical_source_leaf_seen") is not False for v in w[:2]) or w[2].get("full_article_seen") is not False: raise ValueError("witness authority")
 t=r.get("predicates",[])
 if [p.get("key") for p in t]!=["NOT_PRINTED","NOT_PRESENTED_TO_SHIGUAN","NOT_FINISHED"]: raise ValueError("concepts")
 if [p.get("wording") for p in t]!=["惜未梓","以上史館，惜其有志而未逮也","惜其未就也"]: raise ValueError("wording")
 if any(p.get("physical_leaf_seen") is not False for p in t): raise ValueError("no physical folios")
 for p in t:
  if any(k not in ["NOT_PRINTED","NOT_PRESENTED_TO_SHIGUAN","NOT_FINISHED","NEVER_PRINTED_IN_ANY_DYNASTY"] for k in p["forbidden_equivalences"]): raise ValueError("unknown semantics")
 a=r.get("reported_transmission",{})
 if a.get("qian_phrase")!=t[1]["wording"] or a.get("zhu_shizong_phrase")!=t[2]["wording"]: raise ValueError("reported wording")
 if a.get("pang1959_claimed_jingzhiju_quote")!="惜其书未刊行于世": raise ValueError("Pang claim")
 for k in ("shizong_and_jingzhiju_same_passage_proven","qian_and_zhu_exact_historical_printed_pages_seen","pang1959_full_article_seen","pang1959_misquotation_proven","zhu_shizong_clause_is_pang_jingzhiju_quote_proven"):
  if a.get(k) is not False: raise ValueError("false bridge "+k)
 f=r.get("firewalls",{})
 if len(f)!=11 or not all(v is True for v in f.values()): raise ValueError("scope firewall")
 c=r.get("accounting",{})
 for k,v in (("matrix_rows",222),("audited_rows",222),("provenance_repairs",45),("source_root",647),("source_extensions",43),("source_total",690),("graph_nodes",252),("graph_edges",238),("formal_batches",487),("latest_formal","12QD"),("product_r1","CLOSED")):
  if c.get(k)!=v: raise ValueError("snapshot "+k)
 for k in ("new_original_target_images","new_ancient_glyph_votes","new_source_registry_rows","new_graph_nodes","new_graph_edges","new_algorithm_reopens"):
  if c.get(k)!=0: raise ValueError("unsupported claim "+k)
 h=st["historical_audit"]
 if tuple(map(int,st["schema_version"].split(".")))<(1,561,0) or not any(s.startswith("12VE ") for s in h["current_focus"]): raise ValueError("handoff")
 if h["external_source_registry_total_unique_count"]<690 or h["row_count"]!=222 or st["invariants"]["algorithm_reopen_count"]!=0: raise ValueError("state")
 return {"status":"PASS","predicates":3,"original_glyph_votes":0}
def verify(root=ROOT):
 return validate(json.loads((root/REC).read_text(encoding="utf-8")),json.loads((root/STATE).read_text(encoding="utf-8")))
if __name__=="__main__": print(json.dumps(verify(),ensure_ascii=False,sort_keys=True))
