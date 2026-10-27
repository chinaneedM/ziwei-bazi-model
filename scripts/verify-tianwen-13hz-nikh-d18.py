#!/usr/bin/env python3
"""13HZ: two-sided first-party modern edited table check; no original glyph promotion."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13HZ-NIKH-WINTER-D18-TWO-SIDED-R1.json"
def check(e,with_state=True):
 assert e["schema"]=="TIANWEN-13HZ-NIKH-WINTER-D18-TWO-SIDED-R1" and e["issue_id"]=="TW-OPEN-0005"
 assert e["source"]["item_id"]=="kr_052_0010_0010_0020_0010"
 assert e["source"]["grade"]=="OFFICIAL_MODERN_EDITED_TEXT_NOT_PHYSICAL_ORIGINAL"
 p,q,z=e["D17"],e["D18"],e["D19"];a=e["arithmetic"]
 assert (p["A"],p["B"],p["C"])==("五分二五四八","四百二十四三七一一","八千〇〇〇二六九七")
 assert (q["A"],q["B"],q["C"])==("五分二七三四","四百一十九一一六三","八千四百二十四六四〇八三")
 assert (z["B"],z["C"])==("四百一十三八四二九","八千八百四十三七五七一")
 assert (p["A_int"],p["B_int"],p["C_int"])==(52548,4243711,80002697)
 assert (q["A_int"],q["B_int"],q["C_int"])==(52734,4191163,None)
 assert (z["B_int"],z["C_int"])==(4138429,88437571)
 assert p["B_int"]-q["B_int"]==a["A17_from_B"]==p["A_int"]
 assert q["B_int"]-z["B_int"]==a["A18_from_B"]==q["A_int"]
 assert p["C_int"]+p["B_int"]==a["left_C18"]==84246408
 assert z["C_int"]-q["B_int"]==a["right_C18"]==84246408
 assert q["C_digit_stream"]=="842464083" and a["nine_digit_modern_string_preserved"]
 assert a["original_C18_print_glyph"] is None
 assert e["secondary"]["D18_C"]=="八千四百二十四六四〇八"
 assert e["secondary"]["grade"]=="MODERN_RECEIVED_TEXT_NOT_PHYSICAL_ORIGINAL"
 src=e["prior"];raw=(ROOT/src["erratum"]).read_bytes()
 assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==src["erratum_git_blob"]
 assert src["erratum_git_blob"]=="1b35143cfe1b65171a32a9e9119863c23b718add"
 j=json.loads(raw);assert j["earlier_assertion"]["previous_D17_D18_cumulative_equality_claim"]=="RETRACTED_IN_13HY"
 photo=json.loads((ROOT/src["D16_photographs"]).read_text(encoding="utf8"))
 assert all(x["rows"][1]["literal"]==src["physical_D16"]=="五分一三六二" for x in photo["holdings"])
 assert src["D16_counterfactual_only"]=="五分二三六二"
 assert src["old_13HX_accumulation_retraction_retained"]
 f=e["firewall"]
 assert all(f[k] is True for k in ("modern_text_not_original","no_ancient_unit_identity","no_new_source","no_new_witness","no_lineage_promotion"))
 assert f["new_original_folio"] is False and f["NCL03130_summer_D14"] is None
 assert f["G893_six"]==f["D5_zero_five"]=="OPEN" and f["thirteen_EI"]=="RETRACTED"
 assert f["algorithm_reopens"]==f["candidate_collapses"]==0
 assert e["counts"]=={"matrix":[222,222],"sources":761,"genealogy":[252,238],"issues":11,"product":"CLOSED"}
 assert e["transmission_impact"]=="NONE"
 if with_state:
  st=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
  ld=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
  assert st["schema_version"]==ld["binding"]["reviewed_state_version"]==st["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
  assert tuple(map(int,st["schema_version"].split("."))) >= (1,879,0)
  assert any(x.startswith("13HZ ") for x in st["historical_audit"]["current_focus"])
  assert ld["binding"]["latest_research_focus_prefix"]==st["historical_audit"]["current_focus"][-1].split(" ")[0]
  assert ld["binding"]["source_focus_count"]==len(st["historical_audit"]["current_focus"])
  issue=next(i for i in ld["issues"] if i["id"]=="TW-OPEN-0005")
  assert issue["priority"]=="P0" and issue["status"]=="OPEN"
  assert all(any(h.get("revision_id","").startswith("TW-OPEN-0005-" + tag + "-") and "next_action" in h.get("changed_fields",[]) for h in issue["history"]) for tag in ("13HZ","13HY"))
  assert any(x.get("revision_id","").startswith("TW-OPEN-0005-13HZ-") for x in issue["history"])
  assert str(E.relative_to(ROOT)) in issue["source_refs"]
  assert ld["checkpoint_log"][-1]["state_version"]==st["schema_version"]
 return True
if __name__=="__main__":
 assert check(json.loads(E.read_text(encoding="utf8")))
 print("TIANWEN_13HZ_NIKH_D18_TWO_SIDED_SCOPE_PASS")
