#!/usr/bin/env python3
"""13DZ: positively locate original solar day28 without inventing source numeric glyphs."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13DZ-NCL03130-CORRECT-SOLAR-D28-ORIGINAL-P76-LOCATOR-R1.json";S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json";L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13DZ-NCL03130-CORRECT-SOLAR-D28-PAGE-LOCATOR-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["source"]["source_sha256"]=="3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e"
 assert e["source"]["physical_copy"]=="UNBOUND" and e["source"]["ocr_used"] is False
 ac=e["acquisition"]
 assert ac["workflow_run"]==39938606876 and ac["artifact_id"]==12494518841
 assert ac["job_conclusion"]=="success" and ac["source_pdf_sha_verified"] is True
 o=e["original_page_register"]
 assert [x["page"] for x in o]==list(range(73,81))
 assert [x["png_sha256"] for x in o]==["e4597c62fa1cd49eebc3372fcc30e8be273485736a2f7d2a903061f22ca47f52","a3f597f96f494a5ee9a6d582850f0642035d858bcbc587abc6fac11853018a14","059821b008f41c1cdf11bf0daab89de01b44dc5ffee1263e569decb567f76458","ce4eb8b044868fe48bb41fe5453b10fa7bbd949d8fdf2c8e31037f8b89f32fad","e854dde207c49fbb57d6d05a1f25fce51f2e3463585992ab657908dfcec0a12e","2962dd319b679c1a299b3eaa3e3664b0a905ab39f7c1586af41d9a7e5934398f","295c9e803f98d6e1a0546af10607069c17c7588e874f0bc0c78796fcda87b87c","b86b7bb0e6a105d3e194eea0f380d3c16edce81bdb60bde7d53a10b7c25a1ae0"]
 assert all(x["size"][0]==1305 for x in o)
 t=e["target_field"]
 assert (t["source_pdf_page"],t["table_original_heading"],t["table_type"],t["printed_day_heading"],t["ordinal_type"],t["day_number"])==(76,"大陽夏至前後二象縮初盈末限","SOLAR_XIAZHI","二十八日","SOLAR_DAY",28)
 assert t["source_png_sha256"]==o[3]["png_sha256"]
 assert t["exact_xingdu_field_bbox"] is None
 assert t["original_xingdu_literal"] is None and t["original_xingdu_decimal"] is None
 assert t["manual_read_grade"]=="ORIGINAL_SOURCE_TABLE_AND_DAY_POSITIVELY_LOCATED_FIELD_GLYPHS_PENDING"
 c=e["cross_witness_firewall"]
 assert c["ncl_source_solar_D28_original_glyph"]=="PENDING_TARGET_COLUMN_READ"
 assert c["ncl_original_winner"] is None and c["uniform_day_offset_law"]=="UNPROVEN"
 assert c["p86_taiyin_limit28"]=="CORRECTED_13DX_NOT_SOLAR_TARGET"
 assert c["arithmetic_emendation_0_964549"]=="NOT_ATTESTED_AS_ORIGINAL"
 assert all(v==0 for k,v in e["impact"].items() if k!="chart")
 assert e["impact"]["chart"]=="CLOSED"
 assert e["ci_recovery"]["failed_run_id"]==39938609673
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(x.startswith("13DZ ") for x in s["historical_audit"]["current_focus"])
 assert any(x.startswith("13DX ") for x in s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert "docs/research/TIANWEN-13DZ-NCL03130-CORRECT-SOLAR-D28-ORIGINAL-P76-LOCATOR-R1.json" in issue["source_refs"]
 assert any(h.get("revision_id")=="TW-OPEN-0005-13DZ-CORRECT-SOLAR-P76" for h in issue["history"])
 assert issue["next_action"].startswith("13DZ CURRENT ACTION")
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L))
 print("13DZ_PASS")
