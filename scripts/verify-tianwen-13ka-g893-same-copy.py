#!/usr/bin/env python3
"""Validate scoped original evidence; optionally replay real source RGB pixels."""
import argparse
import hashlib
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = "docs/research/TIANWEN-13KA-G893-SAME-COPY-THREE-ROW-ORIGINAL-COLLATION-R1.json"
RECEIPT = "docs/research/TIANWEN-13JZ-G893-EXACT-PAGE-ACQUISITION-RECEIPT-R1.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load():
    return json.loads((ROOT / E).read_text())


def verify(e, original_dir=None):
    require(e["schema"] == "TIANWEN-13KA-G893-SAME-COPY-THREE-ROW-ORIGINAL-COLLATION-R1", "schema")
    require(e["book_code"] == "GK00893_00" and e["physical_copy_count"] == 1, "same physical source")
    a = e["acquisition"]
    require((a["run_id"], a["artifact_id"], a["artifact_zip_bytes"], a["artifact_zip_sha256"]) ==
            (40783073316, 12857907515, 449550, "a3e619a2a67f5590ae4f9b95665105d91bd0fa54a9382465e66db8cf534311ef"), "archive binding")
    require(a["zip_crc_pass"] is True and a["exact_previous_jpeg_hashes_matched"] == 4, "recovery grade")
    require(a["old_204_page_zip_recovered"] is False and a["old_204_page_integrity_replayed"] is False, "not entire archive")
    # Reuse the intake's fixed upstream-document mapping rather than treating this
    # new research record as the authority for its own original page hashes.
    import importlib.util
    spec = importlib.util.spec_from_file_location("intake", ROOT / "scripts/acquire-tianwen-13jz-g893-exact-pages.py")
    intake = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(intake)
    expected = intake.targets()
    pages = {p["page_id"]: p for p in e["pages"]}
    require(len(e["pages"]) == len(pages) == 4 and set(pages) == set(expected), "four exact pages")
    receipt_raw = (ROOT / RECEIPT).read_bytes()
    require(hashlib.sha256(receipt_raw).hexdigest() == a["receipt_sha256"], "immutable acquisition receipt")
    receipt = json.loads(receipt_raw)
    for page, p in pages.items():
        require(p["sha256"] == expected[page]["sha256"] and p["url"] == expected[page]["url"], "upstream source mismatch")
        require(p["size_px"] == [1150, 2000], "source dimensions")
        source = next(r for r in receipt["pages"] if r["page_id"] == page)
        require(source["sha256"] == p["sha256"] and source["rgb_sha256"] == p["rgb_sha256"], "acquisition receipt")
    regions = {r["id"]: r for r in e["regions"]}
    require(len(e["regions"]) == len(regions) == 20, "twenty distinct ROIs")
    for r in regions.values():
        require(r["page_id"] in pages, "ROI page")
        box = r["rect_px"]
        require(len(box) == 4 and all(type(n) is int for n in box), "integer ROI")
        x0, y0, x1, y1 = box
        require(0 <= x0 < x1 <= 1150 and 0 <= y0 < y1 <= 2000, "bounded ROI")
        require(x1-x0 >= 40 and y1-y0 >= 100, "not stripe ROI")
        require(len(r["rgb_pixel_sha256"]) == 64 and set(r["rgb_pixel_sha256"]) <= set("0123456789abcdef"), "ROI SHA")
    facts = {
        8: ("019b", ["七", "八", "九"], ["益一十〇分六三三五七五", "益一十〇分五六一七七五", "益一十〇分四八八〇二五"], ["10.633575", "10.561775", "10.488025"], "損益分"),
        124: ("035b", ["一百二十三", "一百二十四", "一百二十五"], ["一度〇二九五", "一度〇二八一", "一度〇二六七"], ["1.0295", "1.0281", "1.0267"], "疾曆限行度"),
        132: ("036b", ["一百三十一", "一百三十二", "一百三十三"], ["損七分七五九六七五", "損七分八八六〇七五", "損八分〇一〇五二五"], ["7.759675", "7.886075", "8.010525"], "損益分")}
    require(len(e["cases"]) == 3 and {c["target"] for c in e["cases"]} == set(facts), "three cases")
    for c in e["cases"]:
        target = c["target"]
        page, headings, literals, values, label = facts[target]
        require(c["page_id"] == page and c["field_label"] == label, "field identity")
        header = regions[c["header_roi"]]
        require(header["page_id"] == "018b" and header["original_literal"] == label, "complete field header")
        require([r["limit"] for r in c["rows"]] == [target-1, target, target+1], "contiguous three rows")
        for row, heading, literal, value in zip(c["rows"], headings, literals, values):
            require((row["heading_literal"], row["field_literal"], row["displayed_magnitude_decimal_candidate"]) == (heading, literal, value), "original literal/value")
            require(row["sign_glyph"] == (literal[0] if literal[0] in "損益" else None), "sign retained separately")
            for key, text, role in [("heading_roi", heading, "HEADING"), ("value_roi", literal, "VALUE")]:
                r = regions[row[key]]
                require(r["page_id"] == page and r["original_literal"] == text and r["role"] == f'L{row["limit"]}_{role}', "separate original lanes")
        x, y, z = map(Decimal, values)
        require(list(map(Decimal, c["first_differences"])) == [y-x, z-y] and Decimal(c["second_difference"]) == z-2*y+x, "exact differences")
        require(c["arithmetic_scope"].startswith("THREE_G893_ORIGINAL_SAME_COPY_ROWS_ONLY"), "same-copy scope")
    errata = e["forward_only_roi_semantic_errata"]
    require(len(errata) == 2 and {r["prior_role"] for r in errata} == {"L124_DAY_HEADING", "ORIGINAL_TABLE_FIELD_HEADER"}, "both semantic errata")
    for r in errata:
        raw = (ROOT / r["prior_doc"]).read_bytes()
        require(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == r["prior_doc_git_blob_sha"], "immutable old record")
        old = json.loads(raw)
        prior = next(p for p in old["original_rgb_pixel_regions"]["regions"] if p["role"] == r["prior_role"])
        require(prior["rect_px"] == r["prior_rect_px"] and prior["rgb_pixel_sha256"] == r["prior_rgb_pixel_sha256"], "historic ROI preserved")
        require(r["pixel_hash_replayed"] is True and r["semantic_sufficiency"] == "INVALID_AS_CLAIMED_COMPLETE_HEADING_EVIDENCE", "pixel identity is not semantic sufficiency")
        require(r["prior_full_page_glyph_reading_retracted"] is False and r["prior_field_numeric_roi_retracted"] is False, "no unsupported retraction")
        require(all(k in regions for k in r["replacement_roi_ids"]), "new replacement evidence")
    b = e["boundaries"]
    require(all(type(b[k]) is int and b[k] == 0 for k in ("new_physical_witnesses", "new_source_registry_entries", "genealogy_nodes_added", "genealogy_edges_added", "cross_witness_numeric_winners", "algorithm_reopens")), "no witness/winner promotion")
    require(b["unit_equivalence_to_ming_or_goryeosa"] is None and b["exact_impression_year"] is None, "units/date unproved")
    require(all(b[k] is False for k in ("received_goryeosa_literals_changed", "prior_13jy_mixed_witness_grade_rewritten", "full_five_row_same_copy_comparison_completed", "risk_closed")) and b["product"] == "CLOSED", "scope firewall")
    if original_dir is not None:
        from PIL import Image
        originals = {}
        for page, p in pages.items():
            path = Path(original_dir) / (page + ".jpg")
            require(hashlib.sha256(path.read_bytes()).hexdigest() == p["sha256"], "original JPEG replay")
            rgb = Image.open(path).convert("RGB")
            require(list(rgb.size) == p["size_px"] and hashlib.sha256(rgb.tobytes()).hexdigest() == p["rgb_sha256"], "native RGB replay")
            originals[page] = rgb
        for r in regions.values():
            require(hashlib.sha256(originals[r["page_id"]].crop(r["rect_px"]).tobytes()).hexdigest() == r["rgb_pixel_sha256"], "ROI pixel replay")
        for r in errata:
            require(hashlib.sha256(originals[r["prior_page_id"]].crop(r["prior_rect_px"]).tobytes()).hexdigest() == r["prior_rgb_pixel_sha256"], "old ROI pixel replay")
    return {"status": "PASS", "same_copy_rows": 9, "new_original_rois": 20,
            "semantic_roi_errata": 2, "source_pixels_replayed": original_dir is not None, "winners": 0}


def verify_handoff():
    state = json.loads((ROOT / "docs/PROJECT-CURRENT-STATE-R1.json").read_text())
    ledger = json.loads((ROOT / "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text())
    h = state["historical_audit"]
    binding = ledger["binding"]
    require(state["schema_version"] == binding["reviewed_state_version"] == h["research_omission_guard"]["reviewed_state_version"], "reviewed state")
    require(binding["source_focus_count"] == len(h["current_focus"]) and h["current_focus"][-1].startswith(binding["latest_research_focus_prefix"] + " "), "current focus")
    require(any(f.startswith("13KA ") for f in h["current_focus"]), "historic batch retained")
    issue = next(i for i in ledger["issues"] if i["id"] == "TW-OPEN-0005")
    require(issue["next_action"].startswith(binding["latest_research_focus_prefix"] + " CURRENT ACTION:"), "action prefix integration")
    require({E, E.replace(".json", ".md"), RECEIPT}.issubset(issue["source_refs"]), "issue evidence references")
    require(any(r.get("revision_id") == "TW-OPEN-0005-13KA-SAME-COPY-20261029" for r in issue["history"]), "forward-only revision")
    require(state["invariants"]["deterministic_fusion_chart_product_r1"] == "CLOSED", "product state")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--original-dir", type=Path)
    args = parser.parse_args()
    verify_handoff()
    print(json.dumps(verify(load(), args.original_dir)))
