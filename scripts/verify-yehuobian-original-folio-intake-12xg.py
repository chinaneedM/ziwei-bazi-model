#!/usr/bin/env python3
"""12XG: fail-closed provider-URL and *decoded* original-image integrity check.

This is a technical gate, NEVER proof of physical printed-copy identity,
historical glyph reading, publication permission or independent plate descent.
"""
import argparse
import importlib.util
import io
import json
import warnings
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "scripts/verify-yehuobian-original-folio-intake-12xd.py"
REC = "docs/research/MING-DATONG-YEHUOBIAN-12XG-STRICT-ORIGINAL-FOLIO-TECHNICAL-INTAKE-R1.json"
STATE = "docs/PROJECT-CURRENT-STATE-R1.json"
ALLOWED_HOSTS = frozenset({"ioc.u-tokyo.ac.jp", "www.ioc.u-tokyo.ac.jp"})
MAX_BYTES = 250 * 1024 * 1024
MAX_PIXELS = 80_000_000

def load_12xd():
    spec = importlib.util.spec_from_file_location("yehuobian_intake_12xd", OLD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def parse_official_link(value, record):
    require(isinstance(value, str) and value, "URL absent")
    require(not any(ord(c) < 33 or ord(c) == 127 for c in value), "URL contains control/space")
    require(len(value) <= 4096, "URL length")
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError as exc:
        raise ValueError("malformed provider URL") from exc
    require(parsed.scheme == "https" and hostname in ALLOWED_HOSTS and port in (None, 443), "provider URL not official Tokyo IOC host")
    require(parsed.username is None and parsed.password is None and parsed.fragment == "", "provider URL userinfo or fragment")
    # Check the decoded path against the known modern-1959 page, including encoded slash tricks.
    path = parsed.path
    for _ in range(4):
        unescaped = unquote(path)
        if unescaped == path:
            break
        path = unescaped
    forbidden = record["intake_contract"]["disallowed_modern_1959_image_path_substring"]
    require(forbidden.casefold() not in path.casefold(), "modern 1959 file forbidden as original")
    require(path.startswith("/") and not path.startswith("//"), "provider URL path")
    return hostname

def decode_image(image_bytes, label):
    require(isinstance(image_bytes, bytes) and len(image_bytes) >= 32, "no image bytes")
    require(len(image_bytes) <= MAX_BYTES, "oversize image rejected")
    require(label in ("PNG", "JPEG", "TIFF_LE", "TIFF_BE", "PDF"), "unsupported image declaration")
    # PDF is multipage or potentially embedded text. Page selection requires a different,
    # separately audited render/original-page extraction contract.
    require(label != "PDF", "PDF needs independent source-page mapping and rendering; not a single image")
    try:
        from PIL import Image
    except ImportError as exc:
        raise ValueError("Pillow decoder required for strict real-image intake") from exc
    Image.MAX_IMAGE_PIXELS = MAX_PIXELS
    expected = {"PNG": "PNG", "JPEG": "JPEG", "TIFF_LE": "TIFF", "TIFF_BE": "TIFF"}[label]
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        try:
            with Image.open(io.BytesIO(image_bytes)) as probe:
                require(probe.format == expected, "decoder format contradicts receipt")
                require(getattr(probe, "n_frames", 1) == 1, "multi-frame object requires explicit page binding")
                dims = probe.size
                require(all(isinstance(n, int) and n > 0 for n in dims), "invalid raster dimensions")
                require(dims[0] * dims[1] <= MAX_PIXELS, "image pixel limit")
                probe.verify()
            with Image.open(io.BytesIO(image_bytes)) as actual:
                actual.load()  # verify() checks container; load() checks pixel payload
                require(actual.size == dims and actual.format == expected, "decoded image changed on reload")
        except (OSError, SyntaxError, EOFError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
            # Do not catch our own meaningful input error only to erase context.
            raise ValueError("image cannot be fully decoded / format mismatch") from exc
    return {"decoder": "Pillow", "decoded_format": expected, "width": dims[0], "height": dims[1], "pixels": dims[0] * dims[1]}

def validate_ledger(doc, state):
    require(doc["schema"] == "TIANWEN-12XG-STRICT-IOC-ORIGINAL-FOLIO-INTAKE-GATE-R1", "12XG schema")
    require(doc["parent_intake"] == "scripts/verify-yehuobian-original-folio-intake-12xd.py", "parent intake")
    require(doc["domain_policy"]["allowed_exact_hosts"] == sorted(ALLOWED_HOSTS), "provider domains")
    require(doc["domain_policy"]["external_delivery_policy"] == "QUARANTINE_PENDING_INDEPENDENT_STAFF_COPY_BINDING", "external host cannot self-attest")
    require(doc["decoder_policy"]["recognized_formats"] == ["PNG", "JPEG", "TIFF_LE", "TIFF_BE"], "formats")
    require(doc["decoder_policy"]["pdf_policy"] == "BLOCK_PENDING_SEPARATE_SOURCE_PAGE_RENDER", "no PDF single-image promotion")
    require(doc["decoder_policy"]["real_decode_library"] == "Pillow", "pixel decoder required")
    require(doc["historical_glpyh_votes_awarded"] == 0 and doc["plate_independence_votes_awarded"] == 0, "no historical votes")
    inv = state["invariants"]
    h = state["historical_audit"]
    require(inv["deterministic_fusion_chart_product_r1"] == "CLOSED" and inv["algorithm_reopen_count"] == 0, "chart freeze")
    require(h["row_count"] == h["audited_row_count"] == 222 and h["repaired_provenance_metadata_defect_count"] == 45, "matrix state")
    require(h["external_source_registry_total_unique_count"] == 706 and len(h["completed_batches"]) == 487, "unchanged bibliography")
    return {"status": "PASS", "known_ancient_target_folios": 0, "new_historical_glyph_votes": 0}

def validate(receipt, image_bytes, base_record=None):
    old = load_12xd()
    record = base_record or old.read(old.REC)
    # First use legacy item-specific barcode, text, binary size/digest, and authorization
    # *field presence* checks. That authorization string is not externally verified here.
    old_status = old.check_receipt(receipt, image_bytes, record)
    require(old_status["historical_glyph_votes_awarded"] == 0, "no vote from baseline")
    host = parse_official_link(receipt["source_image_url"], record)
    image = decode_image(image_bytes, receipt["format"])
    return {
        "status": "TECHNICAL_BINARY_AND_URL_CONSISTENCY_ONLY_PENDING_INDEPENDENT_CUSTODY_AND_GLYPH_REVIEW",
        "physical_item_barcode": old_status["physical_item_barcode"],
        "image_sha256": old_status["image_sha256"],
        "provider_url_hostname": host,
        "image": image,
        "provider_has_issued_image_for_target": "NOT_INDEPENDENTLY_VERIFIED_BY_THIS_CHECK",
        "authorization_verified_with_provider": False,
        "ancient_printed_copy_identity_verified": False,
        "historical_glyph_votes_awarded": 0,
        "plate_independence_votes_awarded": 0,
    }

def verify():
    old = load_12xd()
    old_result = old.verify()
    document = json.loads((ROOT / REC).read_text(encoding="utf-8"))
    state = old.read(STATE)
    return {"baseline": old_result, "strict_policy": validate_ledger(document, state)}

if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--receipt-json")
    a.add_argument("--image-file")
    opt = a.parse_args()
    require(bool(opt.receipt_json) == bool(opt.image_file), "provide receipt and image together")
    result = verify()
    if opt.receipt_json:
        result["intake"] = validate(
            json.loads(Path(opt.receipt_json).read_text(encoding="utf-8")),
            Path(opt.image_file).read_bytes(),
        )
    print(json.dumps(result, ensure_ascii=False))
