#!/usr/bin/env python3
"""12VD: protect referent identity when near quotation occurs in a different Jingzhiju entry."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12VD-JINGZHIJU-DAOYUAN-HOMOPHRASE-CONTROL-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
PREV="docs/research/MING-DATONG-YEHUOBIAN-12VC-JINGZHIJU-QUOTE-LOCATOR-BOUNDARY-R1.json"
def validate(r,st,p):
 if r.get("schema")!="TIANWEN-12VD-JINGZHIJU-DAOYUAN-NEAR-PHRASE-REFERENT-CONTROL-R1" or r.get("status")!="NEAR_PHRASE_IN_UNRELATED_ENTRY_DOES_NOT_RESOLVE_PANG1959_QUOTATION":raise ValueError("schema/status")
 q=r.get("passages",[])
 if len(q)!=3 or [x.get("role") for x in q]!=["CLAIMED_1959_SCHOLARLY_QUOTE","SHEN_DEFU_RECEIVED_ENTRY","DAOYUAN_NEAR_PHRASE"]:raise ValueError("passages")
 if q[0].get("wording")!="惜其书未刊行于世" or q[0].get("url")!=p["prior_registered_secondary"]["url"]:raise ValueError("1959 context")
 if q[1].get("url")!=p["locator_probe"][0]["url"] or q[1].get("contains_claimed_1959_quote") is not False:raise ValueError("Shen comparison")
 if q[2].get("wording")!="惜其書未刊行" or q[2].get("referent")!="道源所注李義山詩三卷" or q[2].get("not_referring_to")!="沈德符《萬曆野獲編》":raise ValueError("Dao Yuan referent")
 if q[0].get("exact_original_folio") is not None or q[0].get("full_article_read") is not False or q[1].get("original_print_leaf_seen") is not False or q[2].get("original_print_leaf_seen") is not False:raise ValueError("physical/page overclaim")
 c=r.get("collated_differences",{})
 if c.get("claimed_1959_tail")!="于世" or c.get("daoyuan_received_tail") is not None or c.get("exact_wording_match") is not False or c.get("near_phrase_match") is not True or any(c.get(k) is not False for k in ("referent_identity","source_to_source_copying_proved","misquotation_proved")):raise ValueError("false equivalence")
 guards=r.get("controls",{})
 if len(guards)!=10 or any(x is not True for x in guards.values()):raise ValueError("gate bypass")
 a=r.get("accounting",{})
 for k,v in (("root_sources",647),("extension_sources",43),("total_sources",690),("genealogy_nodes",252),("genealogy_edges",238),("formal_completed_batches",487),("formal_latest","12QD"),("product","CLOSED")):
  if a.get(k)!=v:raise ValueError("historical snapshot "+k)
 for k in ("new_registered_sources","new_original_images","new_glyph_votes","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"):
  if a.get(k)!=0:raise ValueError("unsupported increment "+k)
 h=st["historical_audit"]
 if st["invariants"]["algorithm_reopen_count"]!=0 or h["external_source_registry_total_unique_count"]<690 or h["row_count"]!=222 or h["audited_row_count"]!=222:raise ValueError("live state")
 if tuple(map(int,st["schema_version"].split(".")))<(1,560,0) or not any(s.startswith("12VD ") for s in h["current_focus"]):raise ValueError("handoff")
 return {"status":"PASS","new_glyph_votes":0,"misquote_proved":False,"referent_transfer_proved":False}
def verify(root=ROOT):
 def read(p):return json.loads((root/p).read_text(encoding="utf-8"))
 return validate(read(REC),read(STATE),read(PREV))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,sort_keys=True))
