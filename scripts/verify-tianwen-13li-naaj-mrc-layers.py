#!/usr/bin/env python3
"""13LI source image-layer firewall: derived JBIG2 glyph mask != original physical block damage."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13LI-NAJDA2810037-2810038-PDF-MRC-DIGITAL-LAYER-FIREWALL-R1.json"
def load():return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (E,"docs/PROJECT-CURRENT-STATE-R1.json","docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"))
def check(e,s,l):
    assert e["schema"]=="TIANWEN-13LI-NAJDA2810037-2810038-PDF-MRC-DIGITAL-LAYER-FIREWALL-R1" and e["issue_id"]=="TW-OPEN-0005"
    a,b=e["source_originals"]
    assert a["holding"]=="281-0037" and a["book"]==10 and a["pdf_sha256"]=="8892b16c3b8e17f12211195cf7b58acfd5b7dc0d0aefca6623f653a04d4da93e"
    assert b["holding"]=="281-0038" and b["book"]==11 and b["pdf_sha256"]=="73322281149551c76f96008c1b9f3933e817543f7cb8710c92268ade9ca031eb"
    assert a["pdf_producer"]==b["pdf_producer"]=="LuraDocument.jpm v2.05"
    assert a["pdf_creation_metadata"].startswith("D:20160213") and b["pdf_creation_metadata"].startswith("D:20150116")
    assert a["metadata_is_not_print_date"] and b["metadata_is_not_print_date"]
    for x,width,height,maskhash,crop,crhash in ((a,6300,4450,"a18164299d54e38f808ba229f5efec591bcaf41919d7aaa044803d29784d081b",[3277,472,3566,3955],"f64e1fb09435a14216df6a57fa84065290f0270156b103c91c308dd88a5712cc"),(b,6200,4500,"5d1c5e28f13341ca74832dddc0c5754f9e6cc6958b34664ad55b5383f75a5193",[3383,499,3738,4044],"5dd68c5e361c29854bd6e023a7c5393851505543961ea0471dc42af44fd47481")):
        base,mask,foreground=x["layers"]
        assert [v["xref"] for v in x["layers"]]==[32,33,34]
        assert base["filter"]==foreground["filter"]=="JPXDecode" and base["width"]==foreground["width"] and base["height"]==foreground["height"]
        assert mask["role"]=="TEXT_MASK" and mask["filter"]=="JBIG2Decode" and mask["width"]==width and mask["height"]==height and mask["bits"]==1
        assert mask["decoded_pixmap_sha256"]==maskhash and foreground["smask_xref"]==33
        assert x["historic_numeric"]=="238977.09" and x["target_mask_crop_xyxy"]==crop and x["target_mask_crop_gray_sha256"]==crhash and x["target_mask_crop_rgb_not_applicable"]
    c=e["interpretation"];scope=e["counts"]
    for key in ("pdf_creation_dates_prove_ancient_printing","decoded_jbig2_mask_is_unprocessed_camera_original","lossy_symbol_substitution_proven_in_these_files","mask_6300x4450_equivalent_to_physical_optical_resolution_proven","derived_glyph_stroke_damage_sufficient_to_identify_woodblock","same_woodblocks_historically_proven"):
        assert c[key] is False,key
    assert c["lossy_symbol_substitution_possible_without_encoder_proof"] is True
    assert c["independent_historical_recensions_added"]==c["ancient_1739_impressions_proven"]==c["numeric_historical_winners_added"]==0
    assert c["competing_siku_original"]=="288977.09"
    assert scope==dict(root_sources=647,extension_sources=118,total_sources=765,matrix_rows=222,audited=222,graph_nodes=252,graph_edges=238,open_issues=11,historical_g893_winners=0,algorithm_reopens=0,product="CLOSED")
    assert e["replay_contract"]["script"]=="scripts/replay-tianwen-13li-naaj-mrc-layers.py" and e["replay_contract"]["no_ocr"]
    assert not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"]
    f=s["historical_audit"]["current_focus"];binding=l["binding"]
    assert any(x.startswith("13LI ") for x in f) and len(f)==binding["source_focus_count"] and f[-1].split(" ",1)[0]==binding["latest_research_focus_prefix"]
    assert s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]==binding["reviewed_state_version"]==l["checkpoint_log"][-1]["state_version"]
    issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
    assert issue["status"]=="OPEN" and issue["priority"]=="P0" and issue["next_action"].startswith(binding["latest_research_focus_prefix"]+" CURRENT ACTION:")
    assert "13LH CURRENT ACTION:" in issue["next_action"] and "13LG CURRENT ACTION:" in issue["next_action"] and "13JM CURRENT ACTION:" in issue["next_action"] and "RETRACTED" in issue["next_action"]
    assert E in issue["source_refs"] and E[:-5]+".md" in issue["source_refs"]
    assert any(x.get("revision_id")=="TW-OPEN-0005-13LI-MRC-LAYER-20261030" for x in issue["history"])
    assert len(l["issues"])==11 and s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
    return {"status":"PASS","mrc_composite_sources":2,"woodblock_identity_proven":False,"numbers_adjudicated":0}
if __name__=="__main__":print(json.dumps(check(*load()),ensure_ascii=False))
