#!/usr/bin/env python3
"""13BE historical original D16/17 long-lane evidence, positive source and negative lineage checks."""
from decimal import Decimal
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PC="docs/research/TIANWEN-13BE-GORYEOSA-D16-ORIGINAL-LONG-LANE-DUAL-COPY-COLLATION-R1.json"
PBD="docs/research/TIANWEN-13BD-GORYEOSA-D16-D17-ORIGINAL-MULTICOLUMN-IMAGE-PROBE-R1.json"
PBA="docs/research/TIANWEN-13BA-NAJDA-GORYEOSA51-WINTER-SOLAR-D16-DIRECT-GLYPH-R1.json"
PAB="docs/research/TIANWEN-13AB-WASEDA-NLC-GORYEOSA-WORK52-D15-D17-ORIGINAL-THREE-DAY-COVARIANT-R1.json"
PYZ="docs/research/TIANWEN-12YZ-GORYEOSA-D14-D20-INTRATABLE-THREE-COLUMN-RECEIVED-ARITHMETIC-R1.json"
MD=PC.replace(".json",".md")
def load(p):return json.loads((ROOT/p).read_text(encoding="utf8"))
def check(e,bd,ba,ab,yz,ledger,state):
    assert e["schema"]=="TIANWEN-13BE-SOURCE-ORIGINAL-D16-D17-TWO-COPY-LONG-SHORT-AND-ADJACENT-CUMULATIVE-GLYPH-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    c=e["source_capture"]
    assert c["source_batch"]=="13BD" and c["action_run_id"]==39421117170 and c["artifact_id"]==12263559032
    assert c["artifact_digest_sha256"]=="2b8fb5d5141d12b26949e1f4253806d31f3e548af9e04ac40e667093dc6c0f59"
    assert c["verified_image_count"]==2
    s=e["source_original_image_reviews"]
    assert len(s)==2
    assert s[0]["original_image_sha256"]==bd["sources"][0]["existing_JPEG_sha256"]==ba["source_glyph_loci"][1]["jpeg_sha256"]
    assert s[1]["original_image_sha256"]==bd["sources"][1]["embedded_JPEG_sha256"]==ab["source_waseda"]["jpeg_bytes_sha256"]
    assert s[0]["original_image_size"]==bd["sources"][0]["expected_dimensions"]==[3000,2215]
    assert s[1]["original_image_size"]==bd["sources"][1]["expected_dimensions"]==[2592,1728]
    expected={
      "NAJ-282-0006-PHYSICAL51":[([595,870,810,1775],"cd3ba5537f873e49edccb93aecc6cb992074246bcedc0115ef35a6e43d69d24e"),([432,870,635,1775],"191b6827563e4e5347dfbb2d1af16eaee630dfb10e302a312235dde9c7444ba5")],
      "WASEDA-RI06-02809-BOOK33":[([1390,700,1615,1470],"c7b9d0df4e9e959b790165abba9fda4e3849bb8aea11293e134e9a74d769a9ca"),([996,700,1210,1470],"17613b0de4fa7e7291cdffb0662ae7db69b988d39c80d457d7c0f3d007c44e69")]
    }
    assert [x["holding"] for x in s]==list(expected)
    for item in s:
        assert [r["day"] for r in item["day_rois"]]==[16,17]
        for i,row in enumerate(item["day_rois"]):
            assert (row["bbox"],row["rgb_pixel_sha256"])==expected[item["holding"]][i]
            assert row["short_original"]==(["五分一三六二","五分二五四八"][i])
            assert row["long_original"]==(["四百二十九六〇七三","四百二十四三七一一"][i])
            assert row["adjacent_cumulative_original"]==(["七千一百三十五八三七五","七千五百七十〇六六二四"][i])
    assert e["original_glyph_review_method"].startswith("MANUAL_DIRECT_NATIVE_RGB")
    v=e["roman_decimal_bridge"]
    assert (v["day16_short"],v["day16_long"],v["day17_long"],v["long_d16_minus_d17"],v["short_d16_minus_implied"])==("5.1362","429.6073","424.3711","5.2362","-0.1000")
    assert Decimal(v["day16_long"])-Decimal(v["day17_long"])==Decimal(v["long_d16_minus_d17"])
    assert Decimal(v["day16_short"])-Decimal(v["long_d16_minus_d17"])==Decimal(v["short_d16_minus_implied"])
    assert v["intrinsic_historical_original_long_lane_positive"] is True and v["not_proof_ancient_archetype_or_emendation"] is True
    z=e["adjacent_cumulative_scope"]
    assert z["printed_day16_decimal"]=="7135.8375" and z["printed_day17_decimal"]=="7570.6624"
    assert z["modern_digital_transcription_day16_cumulative"]==yz["modern_received_rows"][2]["cumulative"]=="7570.6624"
    assert z["modern_digital_transcription_day17_cumulative"]==yz["modern_received_rows"][3]["cumulative"]=="8000.2697"
    assert z["physical_layout_vs_received_row_index"]=="DAY_INDEX_RELATIONSHIP_NOT_ADJUDICATED"
    assert z["can_use_cumulative_for_direct_same_day_arithmetic"] is False
    f=e["evidence_grading"]
    assert f["ancestral_winner"]=="UNRESOLVED" and f["cross_work_mechanical_identity"]=="UNPROVEN"
    for k in ("two_images_proven_textually_independent","impression_date_and_common_exemplar_bound"):assert f[k] is False
    for k in ("this_batch_new_physical_witnesses_acquired","this_batch_new_image_objects_acquired","independent_stemmatic_votes_counted","registry_sources_added","genealogy_nodes_added","genealogy_edges_added","matrix_rows_added","algorithm_reopen_count"):assert f[k]==0
    assert f["chart_product"]=="CLOSED"
    issue=next(z for z in ledger["issues"] if z["id"]=="TW-OPEN-0005")
    assert issue["priority"]=="P0" and issue["status"]=="OPEN" and issue["source_refs"][-2:]==[MD,PC]
    assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert state["historical_audit"]["current_focus"][-1].startswith("13BE ")
    assert ledger["binding"]["latest_research_focus_prefix"]=="13BE"
    assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
    assert ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
    assert len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==11
    return True
if __name__=="__main__":
    assert check(load(PC),load(PBD),load(PBA),load(PAB),load(PYZ),load("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"),load("docs/PROJECT-CURRENT-STATE-R1.json"))
    print("13BE bounded original long lane and cumulative row index quarantine PASS")
