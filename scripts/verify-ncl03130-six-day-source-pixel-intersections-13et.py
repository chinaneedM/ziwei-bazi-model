#!/usr/bin/env python3
"""13ET source-original RGB crop intersection replay; no glyph/number inference."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13ET-NCL03130-SIX-DAY-SOURCE-PIXEL-INTERSECTIONS-R1.json"
ES="docs/research/TIANWEN-13ES-NCL03130-D1-D6-ROI-OVERLAP-GEOMETRY-FIREWALL-R1.json"
EN="docs/research/TIANWEN-13EN-NCL03130-P74-FOURFEN-D4-D6-BOUNDED-PREFIX-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
EXPECTED=[[1,73,[274,405,287,745],"98d747a1f9b593038f67afb2c3c6d49d732c992743d6c512d9ffcd9fb389e8a8",[172,314,427]],[2,73,[194,405,204,710],"1570b4986e8243003e974eab3f3ee37cb0ec7deade42eae072578bbcc41c591d",[81,140,190]],[3,73,[112,405,118,709],"6d4eb8e02aca595f7effe85442d7e3086cf5427a10eeb294966e1b87d1ca6a97",[23,45,91]],[4,74,[943,411,945,625],"e463cb2a13bd1c6585dceeb39aecb1a37cd07a8bc1c4c67bcb4a946f8dded74d",[1,2,10]],[5,74,[849,411,855,671],"416a7cf14b7a2ae5b03843948b19fbe4b7c0b0249aac1bcbd6fa70954a1a2848",[56,93,406]],[6,74,[759,411,765,677],"4ca17c8cb3b26bf383d8c04898eb11756a969e933e362beff2db02e8cb7773bd",[134,216,634]]]
def read(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def intersect(a,b):
    return [max(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),min(a[3],b[3])]
def check(e,es,en,s,l):
    assert e["schema"]=="TIANWEN-13ET-NCL03130-SIX-DAY-SOURCE-PIXEL-INTERSECTIONS-R1" and e["issue_id"]=="TW-OPEN-0005"
    o=e["source"]
    assert o["pdf_sha256"]==es["shared_source"]["pdf_sha256"]
    assert o["archive_run"]==es["shared_source"]["archived_action_run"] and o["artifact_id"]==es["shared_source"]["archived_artifact_id"]
    assert [(z["pdf_page"],z["png_sha256"]) for z in o["original_pages"]]==[(73,es["shared_source"]["page73_png_sha256"]),(74,es["shared_source"]["page74_png_sha256"])]
    assert o["original_image_ocr_used"] is False and o["new_independent_original_witnesses"]==0
    assert o["physical_copy_identity"]==o["qing_vs_1905_source_hand"]=="UNBOUND"
    assert [z["path"] for z in e["upstream_records"]]==[ES,EN]
    assert len(e["intersection_source_pixel_samples"])==len(EXPECTED)==6
    for row,sample,b in zip(e["intersection_source_pixel_samples"],es["per_day_pairs"],EXPECTED):
        day,page,box,sha,counts=b
        assert row["day"]==sample["day"]==day and row["pdf_page"]==sample["pdf_page"]==page
        assert row["intersection_bbox"]==intersect(sample["fourfen_bbox"],sample["chudu_bbox"])==box
        assert row["pixels"]==sample["bbox_xy_intersection_pixels"]==(box[2]-box[0])*(box[3]-box[1])
        assert row["intersection_rgb_sha256"]==sha
        assert [row["dark_rgb_mean_lt_counts"][str(k)] for k in (90,130,160)]==counts
        assert row["pixel_thresholds_are_not_glyph_ink_identification"] is True and row["source_glyphs_newly_adjudicated"]==0
    tail=e["source_original_lower_fourfen_tail_scope"]
    assert tail["page"]==74 and tail["days"]==[4,5,6] and tail["earlier_predecessor"]==EN
    assert tail["manual_original_tail_reinspect"]=="BOUNDED_VISUAL_REVIEW_NO_COMPLETE_FIELD_ATTESTED"
    assert tail["complete_fourfen_tail_strings"]==[None]*3 and tail["not_negative_absence_proof"] is True
    for d,t in zip((4,5,6),tail["preceding_evidence"]):
        z=next(i for i in en["rois"] if i["name"]==f"D{d}_FOURFEN_TAIL")
        assert t==dict(day=d,roi_name=z["name"],bbox=z["bbox"],rgb_sha256=z["rgb_sha256"])
    f=e["findings"]
    assert f["overlap_tiles_with_rgb_mean_below_90"]==6
    assert f["overlap_dark_pixels_at_threshold_90"]==[r["dark_rgb_mean_lt_counts"]["90"] for r in e["intersection_source_pixel_samples"]]
    assert all(f[k] is True for k in ("dark_pixel_threshold_is_not_historical_ink_classifier","shared_crop_dark_pixels_do_not_prove_shared_glyph_ink","shared_crop_dark_pixels_do_not_prove_wrong_previous_transcription"))
    assert f["complete_original_historical_fourfen_numeric"]==[None]*6
    assert f["original_heading_to_daily_field_mapping"]=="UNPROVEN"
    assert f["solar_d30_numeric"] is None and f["winter_d16_numeric"] is None
    assert f["g893_six_primary_numerics"]=="OPEN" and f["thirteen_ei_erratum"]=="RETRACTED_NOT_ADMISSIBLE"
    assert f["new_source_glyph_readings"]==0
    i=e["impact"]
    assert all(i[k]==0 for k in ("matrix_rows_changed","registry_sources_added","genealogy_nodes_added","genealogy_edges_added","risks_closed","algorithm_reopens"))
    assert i["risks_open_or_blocked"]==11 and i["chart_product"]=="CLOSED"
    assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
    assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
    assert any(x.startswith("13ET ") for x in s["historical_audit"]["current_focus"])
    q=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
    assert q["priority"]=="P0" and q["status"]=="OPEN"
    assert q["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
    assert all(x in q["next_action"] for x in ("D1","D2","D3","D4","D5","D6","D30","四分","初度","NULL"))
    assert {E,E.replace(".json",".md")}.issubset(set(q["source_refs"]))
    v=next(x for x in q["history"] if x.get("revision_id")=="TW-OPEN-0005-13ET-ORIGINAL-PIXEL-20261024")
    assert v["previous_next_action"].startswith("13ES CURRENT ACTION:") and set(v["changed_fields"])=={"source_refs","next_action"}
    assert len(l["issues"])==11 and l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
    return True
def replay(e,source_dir):
    from PIL import Image
    pages={}
    for z in e["source"]["original_pages"]:
        p=Path(source_dir)/z["png_name"]
        assert hashlib.sha256(p.read_bytes()).hexdigest()==z["png_sha256"]
        with Image.open(p) as im:rgb=im.convert("RGB")
        assert list(rgb.size)==z["image_size"] and hashlib.sha256(rgb.tobytes()).hexdigest()==z["rgb_sha256"]
        pages[z["pdf_page"]]=rgb
    for z in e["intersection_source_pixel_samples"]:
        crop=pages[z["pdf_page"]].crop(tuple(z["intersection_bbox"]))
        assert hashlib.sha256(crop.tobytes()).hexdigest()==z["intersection_rgb_sha256"]
        pix=list(crop.getdata())
        assert len(pix)==z["pixels"]
        for t in (90,130,160):
            assert sum(1 for r,g,b in pix if (r+g+b)<3*t)==z["dark_rgb_mean_lt_counts"][str(t)]
    return True
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir")
    args=p.parse_args()
    e=read(E)
    assert check(e,read(ES),read(EN),read(S),read(L))
    if args.source_dir:assert replay(e,args.source_dir)
    print("13ET_PASS ORIGINAL_PIXEL_INTERSECTIONS_NO_GLYPH_OR_NUMERIC_INFERENCE")
