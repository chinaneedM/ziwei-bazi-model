#!/usr/bin/env python3
"""13BB bounded cross-holding original glyph comparison; no vote-count inference."""
import json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PA="docs/research/TIANWEN-13AB-WASEDA-NLC-GORYEOSA-WORK52-D15-D17-ORIGINAL-THREE-DAY-COVARIANT-R1.json"
PB="docs/research/TIANWEN-13BA-NAJDA-GORYEOSA51-WINTER-SOLAR-D16-DIRECT-GLYPH-R1.json"
PC="docs/research/TIANWEN-13BB-GORYEOSA-SOLAR-D16-MULTIHOLDING-EVIDENCE-FIREWALL-R1.json"
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def check(c,a,b):
    assert c["schema"]=="TIANWEN-13BB-D16-MULTIHOLDING-ORIGINAL-GLYPH-SCOPE-AND-STEMMATIC-FIREWALL-R1"
    assert c["issue_id"]=="TW-OPEN-0005" and c["prior_primary_records"]==[PA,PB]
    rows=c["controls"]
    assert len(rows)==4 and len(set(r["id"] for r in rows))==4
    assert [r["short_d16"] for r in rows]==["五分一三六二"]*3+["五分二三六二"]
    assert all(r["short_d15"]=="五分二一七六" and r["short_d17"]=="五分二五四八" for r in rows)
    assert all(r["actual_copy_edition_or_ancestor_bound"] is False for r in rows)
    assert a["source_waseda"]["jpeg_bytes_sha256"]==rows[1]["source_file_sha256"]
    assert a["source_nlc"]["decoded_grayscale_pixel_sha256"]==rows[2]["source_file_sha256"]
    assert a["source_nlc"]["firstparty_nlc_item_crosswalk_verified"] is False
    assert [(x["day"],x["glyph"]) for x in a["collation"]]==[(15,"五分二一七六"),(16,"五分一三六二"),(17,"五分二五四八")]
    assert b["source_glyph_loci"][1]["jpeg_sha256"]==rows[0]["source_file_sha256"]
    assert [(x["day"],x["reading"]) for x in b["source_glyph_loci"][1]["original_rgb_roi"]]==[(15,"五分二一七六"),(16,"五分一三六二"),(17,"五分二五四八")]
    assert b["source_glyph_loci"][1]["original_rgb_roi"][1]["rgb_pixel_sha256"]=="70e262c702cf2d01c0779fb8b245c8733c65e803290a8b6fd46df4de825afb38"
    assert "授時曆立成" in rows[3]["work"] and rows[3]["source_file_sha256"] is None
    assert c["same_numeric_triple_does_not_prove_independent_plate_or_copy"] is True
    assert c["cross_work_same_locus_does_not_prove_same_original_table"] is True
    assert c["historical_earliest_one_or_two"]=="UNRESOLVED" and c["independent_stemmatic_votes"]=="NOT_COUNTED"
    v=c["local_arithmetic"]
    assert (Decimal(v["d15"])+Decimal(v["d17"]))/2==Decimal(v["midpoint"])==Decimal(v["d16_two"])
    assert Decimal(v["d16_one"])+Decimal("0.1000")==Decimal(v["d16_two"])
    assert c["mechanical_final_original_numeric_verdicts"]==0 and c["algorithm_reopens"]==0 and c["chart_product"]=="CLOSED"
    return True
if __name__=="__main__":
    assert check(load(PC),load(PA),load(PB))
    print("13BB multi-holding original glyph scope and no stemmatic votes PASS")
