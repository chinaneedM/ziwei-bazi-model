#!/usr/bin/env python3
"""Recheck all locally extracted 12QK f6..9 images/contacts without OCR.

Usage: python scripts/verify-yehuobian-nlc-old20-atlas-boundaries-12qn.py --artifact-root /path/to/extracted
The root must contain nlc-fasc6/, nlc-fasc7/, nlc-fasc8/, nlc-fasc9/.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/research/MING-DATONG-YEHUOBIAN-12QN-NLC411999003250-VOL11-17-BOUNDARY-FOLIOS-R1.json"
CAPTURE = REPO / "docs/research/MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def verify(extract_root: Path, evidence: dict, capture: dict) -> dict:
    result = {"pass": True, "files": [], "pages_verified": 0, "contacts_verified": 0}
    assert evidence["one_holding_id"] == "NLC-411999003250"
    assert evidence["counting"]["full_454_page_transcription"] is False
    assert evidence["counting"]["full_old20_target_search_completed"] is False
    assert evidence["counting"]["original_1447_louke_target_folio_found"] is False
    assert evidence["new_independent_physical_copy_count"] == 0
    observed = {(x["fascicle"], x["pdf_page"]): x for x in (evidence["original_volume_heading_checks"] + evidence["adjacent_and_terminal_page_checks"])}
    assert len(observed) == len(evidence["original_volume_heading_checks"])+len(evidence["adjacent_and_terminal_page_checks"])
    for row in evidence["source_capture_checks"]:
        n = row["fascicle"]
        root = extract_root / ("nlc-fasc" + str(n))
        status = json.loads((root / "status.json").read_text(encoding="utf-8"))
        source = capture["sources"][n - 1]
        if not (status["status"] == "ALL_SOURCE_PAGES_CAPTURED_MANUAL_TARGET_SEARCH_PENDING"
                and status["source_pdf_sha256"] == source["source_pdf_sha256"] == row["source_pdf_sha256"]
                and status["observed_pages"] == source["source_pdf_pages"] == row["source_pdf_pages"]
                and len(status["image_pages"]) == row["source_page_images_verified_against_original_status_json"]
                and len(status["contact_sheets"]) == row["contact_sheets_verified_against_original_status_json"]):
            raise ValueError("SOURCE_IDENTITY_SCOPE_MISMATCH: " + str(n))
        for p in status["image_pages"]:
            pn = p["page"]
            actual = sha256_file(root / "images" / ("page-" + format(pn, "03d") + ".jpg"))
            if actual != p["sha256"]:
                raise ValueError("PAGE_IMAGE_SHA_MISMATCH: " + str((n, pn)))
            checked = observed.get((n, pn))
            if checked is not None and checked["jpeg_sha256"] != actual:
                raise ValueError("OBSERVED_PAGE_SHA_MISMATCH: " + str((n, pn)))
            result["pages_verified"] += 1
        for c in status["contact_sheets"]:
            if sha256_file(root / "contacts" / c["filename"]) != c["sha256"]:
                raise ValueError("CONTACT_SHA_MISMATCH: " + str((n, c["filename"])))
            result["contacts_verified"] += 1
        result["files"].append({"fascicle": n, "status": "HASHES_MATCH"})
    if result["pages_verified"] != 454 or result["contacts_verified"] != 58:
        raise ValueError("COVERAGE_MISMATCH")
    if len(evidence["original_volume_heading_checks"]) != 7:
        raise ValueError("ORIGINAL_VOLUME_HEADING_COVERAGE_MISMATCH")
    return result

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.artifact_root, json.loads(EVIDENCE.read_text(encoding="utf-8")),
                    json.loads(CAPTURE.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
