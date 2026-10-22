#!/usr/bin/env python3
"""13DA: 1909 printed source RGB D15-17 LONG and CUMULATIVE; no OCR or emendation."""
import json
from decimal import Decimal
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13DA-NLC416-1909-V52-D15-D17-THREE-COLUMN-RGB-AND-ERRATUM-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def check(e,s,l):
 assert e["schema"]=="TIANWEN-13DA-NLC416-1909-D15-D17-THREE-COLUMN-NATIVE-RGB-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 p=e["source"]
 assert (p["source_bytes"],p["pdf_pages"],p["pdf_page"],p["printed_page"])==(38410680,755,143,"百三十六")
 assert p["sha256_original_pdf"]=="b4bd5c557c7ba44bac1fc881e6c2e8784c9d56a8d2629f17b5255a1ec6bd9e97"
 assert p["original_embedded_rgb_sha256"]=="30fd1c9c1601d871d1739a8691e90183960ca19ce3e2f225fd1573ddb8e110b4"
 assert p["original_embedded_rgb_dimensions"]==[1486,2162]
 assert (p["workflow_run"],p["artifact_id"],p["ocr_used"])==(39804643623,12436942290,False)
 expected=[[15,"LONG","四百三十四八二四九","434.8249",[653,1080,700,1715],"1e4d1283e6416bd193db6a7cdd1a3b08b6631d8e0f87cfa1b86996d512bf9cf3"],[16,"LONG","四百二十九六〇七三","429.6073",[471,1080,519,1715],"0ccd02398cbee0dc860b329b382ab428135b442ea7c6ea57a3589e7121740258"],[17,"LONG","四百二十四三七一一","424.3711",[287,1080,335,1715],"e90b93bae924e38110eec5d7720f24690f32d68021446759c9cc6403819042fd"],[15,"CUMULATIVE","七千一百三十五八三七五","7135.8375",[601,1080,652,1715],"5fef490650aa57d2bb5cf354f69654569590f23bcb106ce466c6073e2c278d2b"],[16,"CUMULATIVE","七千五百七十〇六六二四","7570.6624",[420,1080,470,1715],"8af1d80f309d4aba861a40327788698485b1fd18ec89d7fb6809d9eb4420d37d"],[17,"CUMULATIVE","八千〇〇〇二六九七","8000.2697",[236,1080,286,1715],"b28074c4e039f7bbe6b0b5a33400024742b0a6d722b36c12e0f80be77e2a8dea"]]
 got=[[x["day"],x["field"],x["literal"],x["value"],x["bbox"],x["rgb_sha256"]] for x in e["source_native_lanes"]]
 assert got==expected
 assert len(e["source_native_group_rois"])==3
 for x in e["source_native_lanes"]+e["source_native_group_rois"]:
  x0,y0,x1,y1=x["bbox"]
  assert 0<=x0<x1<=1486 and 0<=y0<y1<=2162
  assert len(x["rgb_sha256"])==64
 long={x["day"]:Decimal(x["value"]) for x in e["source_native_lanes"] if x["field"]=="LONG"}
 cum={x["day"]:Decimal(x["value"]) for x in e["source_native_lanes"] if x["field"]=="CUMULATIVE"}
 short={x["day"]:Decimal(x["value"]) for x in e["source_short_prior_13cz"]}
 a=e["arithmetic"]
 assert cum[16]-cum[15]==long[15]==Decimal(a["cum16_minus_cum15"])
 assert cum[17]-cum[16]==long[16]==Decimal(a["cum17_minus_cum16"])
 assert long[15]-long[16]==short[15]==Decimal(a["long15_minus_long16"])
 assert long[16]-long[17]==Decimal(a["long16_minus_long17"])==Decimal(a["derived_short16_candidate_only"])
 assert long[16]-long[17]-short[16]==Decimal(a["discrepancy"])==Decimal("0.1000")
 assert short[16]==Decimal(a["printed_short16"])==Decimal("5.1362")
 assert a["emend_original_text"] is False and a["equals_printed_short16"] is False
 err=e["forward_only_erratum"]
 assert err["previous_manifest_lane_label"]=="candidate_long"
 assert err["previous_data_qualified_not_deleted"] and "cumulative" in err["correction"]
 c=e["comparison"];imp=e["impact"]
 assert c["later_print_not_new_independent_early_original"] and c["stemmatic_independence"]=="UNDETERMINED"
 assert (imp["matrix_rows"],imp["matrix_audited"],imp["registered_sources"],imp["genealogy_nodes"],imp["genealogy_edges"],imp["unresolved_risks"])==(222,222,754,252,238,11)
 assert (imp["new_early_independent_witnesses"],imp["new_graph_nodes"],imp["new_graph_edges"],imp["algorithm_reopens"])==(0,0,0,0)
 assert imp["deterministic_chart"]=="CLOSED"
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13DA ") for x in s["historical_audit"]["current_focus"])
 i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert i["status"]=="OPEN" and E in i["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13DA-NLC416-LONG-CUMULATIVE-ERRATUM" for x in i["history"])
 assert any(x.get("id")=="OMISSIONS-13DA-NLC416-LONG-CUMULATIVE-20261022" for x in l["checkpoint_log"])
 assert sum(x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for x in l["issues"])==11
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L))
 print("TIANWEN_13DA_NLC416_1909_THREE_COLUMN_NATIVE_RGB=PASS")
