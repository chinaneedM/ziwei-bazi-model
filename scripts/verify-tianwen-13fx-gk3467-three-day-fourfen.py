#!/usr/bin/env python3
"""13FX original three-day Fourfen lane with forward-only 13FR correction; optional source PDF pixel hashes."""
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EV=ROOT/"docs/research/TIANWEN-13FX-GK3467-P17-THREE-DAY-FOURFEN-SOURCE-FIELD-ERRATUM-R1.json"
FR=ROOT/"docs/research/TIANWEN-13FR-GK3467-BOOK6-D16-D30-DIRECT-FIELD-COLLATION-R1.json"
FW=ROOT/"docs/research/TIANWEN-13FW-GORYEOSA-D30-RECEIVED-FOURFEN-ARITHMETIC-CONFLICT-R1.json"
FV=ROOT/"docs/research/TIANWEN-13FV-NLC-D30-GUTTER-DAY-HEADER-GEOMETRY-R1.json"
STATE=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
LEDGER=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
DIGITS=dict(zip("〇一二三四五六七八九","0123456789"))
EXPECTED=[(29,"九〇六〇",9060,[2128,670,2192,1370]),(30,"九二二二",9222,[1899,670,1964,1260]),(31,"九三八四",9384,[1655,670,1722,1370])]
def sha(x): return hashlib.sha256(x).hexdigest()
def read(p): return json.loads(p.read_text("utf-8"))
def check(e, fr, fw, fv, state, ledger, pdf=None):
    assert e["schema"]=="TIANWEN-13FX-GK3467-P17-THREE-DAY-FOURFEN-SOURCE-FIELD-ERRATUM-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    src=e["source"]
    assert (src["source_catalog"],src["digital_volume"],src["physical_book"],src["work_juan"],src["pdf_page_one_based"])==("GK03467_04","0001",6,52,17)
    assert (src["pdf_sha256"],src["source_embedded_png_sha256"],src["source_original_rgb_sha256"])==("b75009805dae9ccc22797c005bd5f32c7870a192945b503f6b3af3fbf14e1386","375acd8814bca370bc9d83402f6ca6f77368efbadddef646bac0632faf5db585","7bb9428f748f61875bf0ca1470b3bd8ada29ee8e0c79a5b8621f27c6d2467238")
    assert src["source_image_native_wh"]==[2432,2064] and src["source_embedded_xref"]==48
    assert src["new_ancient_physical_witnesses"]==0 and src["physical_copy_vs_nlc_nikh_independence"] is None
    rows=e["original_fourfen_rows"]
    assert len(rows)==3
    assert e["source_native_numeric_neighbor_differences"]==[162,162]
    for r,(day,digits,num,box) in zip(rows,EXPECTED):
        assert (r["day"],r["field"],r["digits"],r["numeric"],r["roi_xyxy"])==(day,"四分",digits,num,box)
        assert int("".join(DIGITS[c] for c in digits))==num
        assert all(len(r[k])==64 for k in ("roi_rgb_sha256","roi_png_sha256"))
    assert [r["numeric"] for r in rows]==[9060,9222,9384]
    assert [b["numeric"]-a["numeric"] for a,b in zip(rows,rows[1:])]==[162,162]
    assert rows[0]["roi_xyxy"][0]>rows[1]["roi_xyxy"][2]>rows[2]["roi_xyxy"][2]
    assert [x["numeric"] for x in fw["received_table"]["rows"] if x["day"] in (29,30,31)]==[9060,9222,9384]
    old=e["forward_only_erratum"]
    assert fr["readings"][1]["numeric_glyph_literal"]==old["earlier_day30_literal"]=="九二二一四三"
    assert old["earlier_broad_roi_xyxy"]==fr["readings"][1]["roi_xyxy"]
    assert old["earlier_record_bytes_preserved"] and old["revised_original_fourfen_source_specific_day30"]=="九二二二"
    assert old["cause_of_earlier_six_glyph_report"].startswith("NOT_PROVEN")
    assert fw["adjudication"]["source_original_erratum_authorized"] is False # historical pre-correction snapshot
    assert fv["geometry"]["day30_complete_fourfen_original_digits"] is None
    assert e["limits"]["nlc_p76_day30_fourfen_original_digits"] is None
    assert e["limits"]["historical_day30_winner"] is None
    assert e["limits"]["g893_six_direct_controls"]=="OPEN"
    assert e["limits"]["product"]=="CLOSED"
    assert all(e["limits"][x]==0 for x in ("new_source_registry_records","new_graph_nodes","new_graph_edges","matrix_rows_changed","algorithm_reopens","candidate_collapses","risk_issues_closed"))
    assert not e["transmission_impact"]["edges_supported"]
    assert state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
    assert any(x.startswith("13FX ") for x in state["historical_audit"]["current_focus"]), "13FX evidence must remain append-only replayable"
    assert ledger["binding"]["reviewed_state_version"]==state["schema_version"]
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    assert issue["status"]=="OPEN" and str(EV.relative_to(ROOT)) in issue["source_refs"]
    if pdf is not None:
        from PIL import Image
        from io import BytesIO
        import fitz
        binary=Path(pdf).read_bytes()
        assert sha(binary)==src["pdf_sha256"]
        d=fitz.open(stream=binary,filetype="pdf")
        assert len(d)==src["pdf_pages"]
        images=d[16].get_images(full=True)
        assert len(images)==1 and images[0][0]==48
        emb=d.extract_image(48)
        assert emb["ext"]=="png" and sha(emb["image"])==src["source_embedded_png_sha256"]
        image=Image.open(BytesIO(emb["image"])).convert("RGB")
        assert image.size==tuple(src["source_image_native_wh"]) and sha(image.tobytes())==src["source_original_rgb_sha256"]
        for r in rows:
            roi=image.crop(tuple(r["roi_xyxy"]))
            assert sha(roi.tobytes())==r["roi_rgb_sha256"]
            dest=BytesIO();roi.save(dest,format="PNG")
            assert sha(dest.getvalue())==r["roi_png_sha256"]
    return True
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--pdf",default=None)
    args=ap.parse_args()
    assert check(read(EV),read(FR),read(FW),read(FV),read(STATE),read(LEDGER),args.pdf)
    print("13FX_PASS_SOURCE_BOUND_FOURFEN_29_30_31_FORWARD_ONLY_ERRATUM_NO_HISTORICAL_WINNER")
