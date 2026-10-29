#!/usr/bin/env python3
"""Evidence-scoped G893 five-row check; optional exact original-image pixel replay."""
from __future__ import annotations
import argparse
import hashlib
import json
from decimal import Decimal
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = "docs/research/TIANWEN-13KC-G893-SAME-COPY-FIVE-ROW-ORIGINAL-COLLATION-R1.json"
UPSTREAM = "docs/research/TIANWEN-13KA-G893-SAME-COPY-THREE-ROW-ORIGINAL-COLLATION-R1.json"
ACQ_SCRIPT = "scripts/acquire-tianwen-13kb-g893-neighbor-pages.py"
EXPECTED = {
    6: ("019b","六","益一十〇分七〇三四二五","10.703425","益"),
    10: ("020a","十","益一十〇分四一二三二五","10.412325","益"),
    122: ("035a","一百二十二","一度〇三〇九","1.0309",None),
    126: ("035b","一百二十六","一度〇二五三","1.0253",None),
    130: ("036a","一百三十","損七分六三一三二五","7.631325","損"),
    134: ("037a","一百三十四","損八分一三三〇二五","8.133025","損"),
}
EXPECTED_PAGES = {
    "020a":"b3044190bdc7181c870a2077cfaa52b55533925b98b30ba2e079c05444d3f31b",
    "035a":"efbad3841aac3bc9f2c755a584464f1e6902930b3fb75550b961659fe84fa544",
    "036a":"6406455df8be50f4081e1bdb8c2ed85c754d7d5d54039643e7d77ec7a0816d40",
    "037a":"97051fbf7c707c660d09b9db38cf815c69041f992ec11534154d93cd1a45469e",
}
EXPECTED_NEIGHBOR_ROW_IDS = [(6,7,8,9,10),(122,123,124,125,126),(130,131,132,133,134)]


def require(p, message):
    if not p:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def github_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()


def verify(e, original_dir=None):
    require(e["schema"]=="TIANWEN-13KC-G893-SAME-COPY-FIVE-ROW-ORIGINAL-COLLATION-R1", "schema")
    require(e["issue_id"]=="TW-OPEN-0005" and e["book_code"]=="GK00893_00" and e["physical_copy_count"]==1,"one copy only")
    require(e["upstream_three_row_evidence"]==UPSTREAM,"immutable 13KA upstream")
    require(e["acquisition"]["workflow_id"]==40788504692 and e["acquisition"]["artifact_id"]==12860796453, "four-page acquisition identity")
    require(e["acquisition"]["artifact_zip_sha256"]=="c4da23f3165404d25e582a12ee1f7d756ae949c81311bf22b5403736aa62c14b", "four-page archive SHA")
    require(e["acquisition"]["old_204_page_archive_recovered"] is False,"old full archive not recovered")
    require(e["acquisition"]["source_issued_only"] is True,"no synthetic historical URL")
    require(e["acquisition"]["all_four_images_valid_jpeg"] is True,"JPEG intake")
    require(e["acquisition"]["all_four_dimensions"]==[1150,2000],"source dimensions")
    import importlib.util
    spec=importlib.util.spec_from_file_location("g893intake", ROOT / ACQ_SCRIPT)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    require(set(module.TARGETS)==set(EXPECTED_PAGES),"source-issued exact page set drift")
    pages={p["page_id"]:p for p in e["newly_acquired_pages"]}
    require(len(e["newly_acquired_pages"])==len(pages)==4 and set(pages)==set(EXPECTED_PAGES),"four source pages")
    for page,record in pages.items():
        require(record["sha256"]==EXPECTED_PAGES[page] and record["size_px"]==[1150,2000],"original JPEG identity")
        module.validate_url(page, record["source_issued_url"])
        require(len(record["rgb_sha256"])==64,"RGB SHA")
    upstream=json.loads((ROOT/UPSTREAM).read_text(encoding="utf-8"))
    require(upstream["book_code"]=="GK00893_00" and upstream["physical_copy_count"]==1 and len(upstream["cases"])==3,"13KA copy and original lanes")
    old={r["limit"]:(r["displayed_magnitude_decimal_candidate"],r["field_literal"],r["heading_literal"]) for case in upstream["cases"] for r in case["rows"]}
    original_pages={x["page_id"]:x for x in upstream["pages"]}
    full_sources={**original_pages,**pages}
    perimeter={r["limit"]:r for r in e["perimeter_original_rows"]}
    require(len(e["perimeter_original_rows"])==len(perimeter)==len(EXPECTED),"six perimeter rows")
    for lim,expected in EXPECTED.items():
        r=perimeter[lim]
        require((r["page_id"],r["heading_original_literal"],r["original_field_literal"],r["displayed_magnitude_decimal_candidate"],r["sign_glyph"])==expected,"original glyph/value " + str(lim))
        require(r["review_method"]=="DIRECT_HUMAN_VISUAL_SOURCE_JPEG_NO_OCR","no OCR substitution")
        require(r["header_provenance"]==UPSTREAM,"header semantic gate")
        for key,sha_key in (("heading_rect_px","heading_native_rgb_sha256"),("value_rect_px","value_native_rgb_sha256")):
            rect=r[key]
            require(len(rect)==4 and all(type(i) is int for i in rect) and
                    0<=rect[0]<rect[2]<=1150 and 0<=rect[1]<rect[3]<=2000,"invalid native ROI")
            require(rect[2]-rect[0]>=40 and rect[3]-rect[1]>=100,"trivial pixel ROI")
            require(len(r[sha_key])==64 and all(c in "0123456789abcdef" for c in r[sha_key]),"bad native pixel hash")
        require(r["page_id"] in full_sources,"ROI not source-bound")
    windows=e["five_row_same_copy_windows"]
    require(len(windows)==3 and [x["target"] for x in windows]==[8,124,132],"three windows and targets")
    for w,limits in zip(windows,EXPECTED_NEIGHBOR_ROW_IDS):
        require(tuple(w["limit_sequence"])==limits and len(w["same_copy_display_magnitude"])==5,"exact five-row source sequence")
        values=[]
        for lim,actual in zip(limits,w["same_copy_display_magnitude"]):
            val=perimeter[lim]["displayed_magnitude_decimal_candidate"] if lim in perimeter else old[lim][0]
            require(actual==val,"borrowed mixed-witness value or old central lane changed")
            values.append(Decimal(val))
        first=[values[i+1]-values[i] for i in range(4)]
        second=[first[i+1]-first[i] for i in range(3)]
        require(list(map(Decimal,w["first_differences"]))==first,"first differences")
        require(list(map(Decimal,w["second_differences"]))==second,"second differences")
        require(w["sign"]==perimeter[limits[0]]["sign_glyph"]==perimeter[limits[-1]]["sign_glyph"],"sign scope")
        require(set(w["source_pages"])=={(perimeter[lim]["page_id"] if lim in perimeter else next(c["page_id"] for c in upstream["cases"] if any(r["limit"]==lim for r in c["rows"]))) for lim in limits},"all same-copy source pages")
    b=e["boundaries"]
    require(all(type(b[k]) is int and b[k]==0 for k in ("new_independent_historical_physical_witnesses","new_source_registry_entries","new_genealogy_nodes","new_genealogy_edges","cross_witness_numeric_winners","algorithm_reopens")),"historical winner or algorithm falsely promoted")
    require(b["unit_equivalence_to_ming_or_goryeosa"] is None and b["exact_impression_year"] is None,"units/date incorrectly awarded")
    require(b["historical_causal_typology_of_received_variants"]=="UNRESOLVED","transmission error inferred")
    require(b["product"]=="CLOSED" and b["risk_closed"] is False and
            b["observed_goryeosa_original_literature_unmodified"] is True,"product / received-text firewall")
    replayed=0
    if original_dir is not None:
        for page,entry in full_sources.items():
            p=Path(original_dir)/(page+".jpg")
            raw=p.read_bytes()
            require(sha256(raw)==entry["sha256"],"original file hash "+page)
            with Image.open(p) as im:
                require(im.format=="JPEG" and im.size==(1150,2000),"source image shape "+page)
                rgb=im.convert("RGB")
            require(sha256(rgb.tobytes())==entry["rgb_sha256"],"original pixels "+page)
            for r in perimeter.values():
                if r["page_id"]!=page:continue
                for rect_key,hash_key in (("heading_rect_px","heading_native_rgb_sha256"),("value_rect_px","value_native_rgb_sha256")):
                    require(sha256(rgb.crop(r[rect_key]).tobytes())==r[hash_key],"visual ROI native pixels "+str(r["limit"]))
                    replayed+=1
    return {"status":"PASS","source_copy_count":1,"same_copy_rows":15,"new_perimeter_rows":6,
            "new_original_rois":12,"new_original_pixel_rois_replayed":replayed,"cross_witness_winners":0}


def handoff():
    s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf-8"))
    l=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf-8"))
    h=s["historical_audit"]
    require(s["schema_version"]==l["binding"]["reviewed_state_version"]==h["research_omission_guard"]["reviewed_state_version"],"state/ledger grade")
    require(l["binding"]["source_focus_count"]==len(h["current_focus"]) and
            h["current_focus"][-1].startswith(l["binding"]["latest_research_focus_prefix"]+" "),"state focus")
    issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
    require(issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:") and any(x.get("revision_id")=="TW-OPEN-0005-13KC-FIVE-ROW-20261029" for x in issue["history"]),"forward-only research action contract")
    require({EVIDENCE,EVIDENCE.replace(".json",".md")}.issubset(issue["source_refs"]),"source evidence anchored")
    require(any(r.get("revision_id")=="TW-OPEN-0005-13KC-FIVE-ROW-20261029" for r in issue["history"]),"forward-only history")
    require(s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0,"product invariant")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-dir",type=Path)
    a=p.parse_args()
    handoff()
    rec=json.loads((ROOT/EVIDENCE).read_text(encoding="utf-8"))
    print(json.dumps(verify(rec,a.original_dir),ensure_ascii=False))
