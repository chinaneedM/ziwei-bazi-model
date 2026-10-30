#!/usr/bin/env python3
"""13EN source-original bounded 四分 prefixes, hash gates, no complete-field invention."""
import argparse,hashlib,json
from pathlib import Path
try:
    from scripts._tianwen_historical_action_r1 import historical_action_view
except ModuleNotFoundError:
    from _tianwen_historical_action_r1 import historical_action_view
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13EN-NCL03130-P74-FOURFEN-D4-D6-BOUNDED-PREFIX-R1.json"
EL="docs/research/TIANWEN-13EL-NCL03130-P74-D6-CHUDU-LONG-AND-D4-D6-CONTROLS-R1.json";EM="docs/research/TIANWEN-13EM-NCL03130-P74-D4-D6-RIGHT-NEIGHBOR-LONG-STRIPS-R1.json";EI="docs/research/TIANWEN-13EI-NCL03130-D4-MISATTRIBUTED-CHUDU-ROI-ERRATUM-R1.json";ED="docs/research/TIANWEN-13ED-NCL03130-SOLAR-D30-EXTENDED-ORIGINAL-STRIP-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EXPECTED=json.loads(r'''[["D4_FOURFEN_PREFIX",[919,406,945,625],"29b89c50739b3ffcc0a89dbc8f5a7bf3543758bd51948d9dea95b2f53f23948f","四分五〇一"],["D5_FOURFEN_PREFIX",[829,405,855,671],"6e2b5a5a686c559ba9722920a0a10e74dfc82c3717f553f51fefb26cce0b3525","四分〇一七二"],["D6_FOURFEN_PREFIX",[736,405,765,677],"f35f5d2955dfc2d9f5c3ce0255564886276418d51d85613abe89355d56af159b","四分五三三四"],["D4_FOURFEN_EXTENDED",[916,398,950,830],"a9c1b24f653b219a79c4d0c139406e916db642a3a71ab11842b5d13cd288b74c",null],["D5_FOURFEN_EXTENDED",[820,398,859,830],"29fd276aa4c6e7b4cf6010f42c1fcc4827c2142848344bea0d1392ab74cd4b78",null],["D6_FOURFEN_EXTENDED",[730,398,766,830],"73dc4f0f3345c8fce2deb492d5627b147094381c134c5d3ac80da67b60f6aad0",null],["D4_FOURFEN_TAIL",[919,625,945,830],"bca5f29f3850bc8b2136ed4bfbb2cf609df4dd0cd550d06e9cdcf039e6016c6c",null],["D5_FOURFEN_TAIL",[829,671,855,830],"6bf028ccc8cd7def073ea150fef43888f8a2de4f3612775d6ce6f7e5f7169c67",null],["D6_FOURFEN_TAIL",[736,677,765,830],"8f982e84a2a1d85f5e22f53097114f218943b88a1b41c72e1b1e94f178937235",null],["D4_CHUDU_CONTROL",[943,411,970,771],"a82d6f37825b16f1c1250604f8021cbf165b2ce26d0913928a19be720eb0375c","初度九十五二八五一"],["D5_CHUDU_CONTROL",[849,411,876,771],"3005a769650dbb37c5213ab977a1f196b88c9a2bca6f02e0d7e75b1747e2dc79","初度九十五三三〇〇"],["D6_CHUDU_CONTROL",[759,411,785,771],"0867d3c79f288e3b83c6d3cf682628b0be4f3ddac6d0d4102cfddae6e9dd66f9","初度九十五三七五〇"],["D4_RIGHT_CONTROL",[974,405,1002,815],"41232f81b4144b32ae41fb0ea92bd09cb281dfa74b7ab4b866ebbc10601c0ef4","一千四百四十一二二七一"],["D5_RIGHT_CONTROL",[879,405,909,815],"f0074f8777cf218a6c480af88f2ea59275707288e0e0c869f82b1bc180f11ca3","一千九百一十二七〇七二"],["D6_RIGHT_CONTROL",[785,405,819,815],"ace3950cfc60b0624009a49c18be48423976d1ec22b9ef3f3d685272e481213b","一千三百七十九七一二五"],["D4_DAYTITLE_CONTROL",[885,150,951,300],"dac2d4865d428da1a875428c6542a24b5192ac05b0bcb49799d6ed625b23bb38","四日"],["D5_DAYTITLE_CONTROL",[796,150,880,300],"fbe99140e3d22c09ae796069a60ebd31d76c832be6db3736b923b068694455ea","五日"],["D6_DAYTITLE_CONTROL",[704,150,792,300],"149d70bd1d383d5396258a3af68f2c9c1758f5c6a45579abeee3e5cd4c5b6b4b","六日"],["THREE_DAY_GROUP_CONTEXT",[704,380,1005,831],"9af97c249b7853b5d03032b02c921d7f5054e29c103ced9dde712f12b59903c8",null]]''')
def read(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(e,el,em,ei,ed,state,ledger):
 assert e["schema"]=="TIANWEN-13EN-NCL03130-P74-FOURFEN-D4-D6-BOUNDED-PREFIX-R1" and e["issue_id"]=="TW-OPEN-0005"
 src=e["source"]
 assert src["pdf_page"]==em["source"]["original_pdf_page"]==el["source"]["pdf_page"]==74
 assert src["pdf_sha256"]==em["source"]["pdf_sha256"]==el["source"]["pdf_sha256"]==ed["source"]["pdf_sha256"]
 assert src["png_sha256"]==em["source"]["png_sha256"]==el["source"]["png_sha256"]
 assert src["rgb_sha256"]==em["source"]["rgb_sha256"]==el["source"]["rgb_sha256"]
 assert src["image_size"]==em["source"]["size"]==[1305,873]
 assert src["artifact_id"]==em["source"]["artifact_id"]==el["source"]["artifact_id"] and src["original_archive_run"]==em["source"]["archived_run"]
 assert src["ocr_used"] is False and src["physical_copy_id"]==src["qing_vs_1905_hand"]=="UNBOUND" and src["independent_original_witnesses_added"]==0
 assert len(e["rois"])==len(EXPECTED)==19
 assert [[r["name"],r["bbox"],r["rgb_sha256"],r["visible_prefix"]] for r in e["rois"]]==EXPECTED
 assert all(r["grade"]==("SOURCE_NATIVE_BOUNDED_DIRECT_VISIBLE_PREFIX_ONLY" if r["name"].endswith("_PREFIX") else "SOURCE_NATIVE_RGB_SHA_CONTROL_NO_EXTRA_READING") for r in e["rois"])
 assert all(0<=r["bbox"][0]<r["bbox"][2]<=1305 and 0<=r["bbox"][1]<r["bbox"][3]<=873 for r in e["rois"])
 assert [r["rgb_sha256"] for r in e["rois"][9:12]]==[em["rois"][12]["rgb_sha256"],em["rois"][13]["rgb_sha256"],em["rois"][14]["rgb_sha256"]]
 assert [r["rgb_sha256"] for r in e["rois"][12:15]]==[em["rois"][0]["rgb_sha256"],em["rois"][1]["rgb_sha256"],em["rois"][2]["rgb_sha256"]]
 assert e["rois"][17]["rgb_sha256"]==el["rois"][0]["rgb_sha256"]
 f=e["findings"]
 assert [f["fourfen_d4_clear_prefix"],f["fourfen_d5_clear_prefix"],f["fourfen_d6_clear_prefix"]]==[r["visible_prefix"] for r in e["rois"][:3]]==["四分五〇一","四分〇一七二","四分五三三四"]
 assert f["fourfen_prefix_is_complete_column"]==[False]*3 and f["fourfen_below_prefix"]=="UNREAD_OR_AMBIGUOUS_NOT_NEGATIVE_ABSENCE_PROOF"
 assert f["d4_d5_d6_fourfen_exact_decimals"]==[None]*3 and f["d4_d5_d6_fourfen_full_row"] is None
 assert f["chudu_originals"]==[r["visible_prefix"] for r in e["rois"][9:12]]==em["findings"]["source_original_chudu_control_strings"]
 assert f["right_originals"]==[r["visible_prefix"] for r in e["rois"][12:15]]==em["findings"]["right_neighbor_visible_strings"]
 assert f["p73_technical_heading_lane_assignment"]=="UNPROVEN" and f["columns_not_concatenated"] is True
 assert f["day30_original"]==ed["finding"]["d30_visible_glyph_group"]=="初度九十六二〇三" and f["day30_historical_decimal"] is None and f["day30_missing_character_proved"] is False
 assert f["legacy_13ei_erratum_preserved"] is True and ei["replacement"]["normalized_pair_geometry"]=="RETRACTED_NOT_ADMISSIBLE"
 assert f["source_folio_qualifies_as_independent_witness_count"]==0 and f["source_units_and_decimal_precision"]=="UNBOUND"
 i=e["impact"];assert i["deterministic_product"]=="CLOSED" and i["issues_open_or_blocked"]==11
 assert all(i[k]==0 for k in ("matrix_rows_changed","external_registry_sources_added","genealogy_nodes_added","genealogy_edges_added","algorithm_reopens","issues_closed"))
 assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert any(r.startswith("13EN SOURCE ORIGINAL NCL03130") for r in state["historical_audit"]["current_focus"])
 assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 q=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 assert q["priority"]=="P0" and q["status"]=="OPEN" and historical_action_view(q).startswith(ledger["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION")
 assert {E,E.replace(".json",".md")}.issubset(set(q["source_refs"]))
 h=next(z for z in q["history"] if z.get("revision_id")=="TW-OPEN-0005-13EN-FOURFEN-BOUNDED-PREFIX-20261024")
 assert h["previous_next_action"].startswith("13EM CURRENT ACTION") and set(h["changed_fields"])=={"source_refs","next_action"}
 assert len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
 return True
def replay(e,source_dir):
 from PIL import Image
 f=Path(source_dir)/"original-p074.png"
 assert hashlib.sha256(f.read_bytes()).hexdigest()==e["source"]["png_sha256"]
 with Image.open(f) as im:rgb=im.convert("RGB")
 assert list(rgb.size)==e["source"]["image_size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==e["source"]["rgb_sha256"]
 for r in e["rois"]:
  assert hashlib.sha256(rgb.crop(tuple(r["bbox"])).tobytes()).hexdigest()==r["rgb_sha256"],r["name"]
 return True
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--source-dir");x=p.parse_args()
 e=read(E);assert check(e,read(EL),read(EM),read(EI),read(ED),read(S),read(L))
 if x.source_dir: assert replay(e,x.source_dir)
 print("13EN_PASS BOUNDED_FOURFEN_PREFIXES_NUMERIC_UNRESOLVED")
