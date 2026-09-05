#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import urllib.request
from pathlib import Path

from PIL import Image

MANIFEST_URL = "https://catalog.lib.kyushu-u.ac.jp/image/manifest/1/820/6631038.json"
UA = "Mozilla/5.0 (compatible; ziwei-bazi-model historical-research-probe/1.0)"
TARGETS = {
    40: {
        "table_identity": "SOLAR_YINGSUO_CONTEXT",
        "controls": ["STRUCT-SOLAR-YINGSUO-TABLE-OPENING"],
        "binding": "PRINTED_SOLAR_TABLE_OPENING_AND_SCHEMA_CONTEXT; STRUCTURE_ONLY",
        "purpose": "FIELD_CONTEXT_ONLY_NOT_A_TARGET_NUMERIC_READING",
    },
    41: {
        "table_identity": "SOLAR_YINGSUO_CONTEXT",
        "controls": ["VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE"],
        "binding": "PRINTED_SOLAR_TABLE_CONTINUATION_CONTAINS_DAY_16; TEST_FIELD_PRESENCE_NOT_VALUE_INFERENCE",
    },
    50: {
        "controls": ["STRUCT-LUNAR-CHIJI-TABLE-HEADER"],
        "binding": "PRINTED_TITLE_TAIYIN_CHIJI_LICHENG_AND_FIELDS_LIMIT_DAYRATE_LOSSGAIN_ACCUMULATED",
        "purpose": "FIELD_CONTEXT_ONLY_NOT_A_TARGET_NUMERIC_READING",
    },
    51: {
        "controls": ["VAR-NUM-LUNAR-L8-LOSSGAIN"],
        "binding": "SAME_TAIYIN_CHIJI_TABLE_CONTINUATION; PRINTED_LIMITS_6_TO_25_INCLUDE_L8",
    },
    55: {
        "controls": ["NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING"],
        "binding": "SAME_TAIYIN_CHIJI_TABLE_CONTINUATION; PRINTED_LIMITS_86_TO_105_INCLUDE_L101",
    },
    56: {
        "controls": ["VAR-NUM-LUNAR-L114-DAYRATE"],
        "binding": "SAME_TAIYIN_CHIJI_TABLE_CONTINUATION; PRINTED_LIMITS_106_TO_125_INCLUDE_L114",
    },
    57: {
        "table_identity": "LUNAR_CHIJI",
        "controls": ["VAR-NUM-LUNAR-L132-LOSSGAIN"],
        "binding": "SAME_TAIYIN_CHIJI_TABLE_CONTINUATION; PRINTED_LIMITS_126_TO_145_INCLUDE_L132",
    },
    68: {
        "table_identity": "LUNAR_LIMIT_XINGDU",
        "controls": ["STRUCT-LUNAR-LIMIT-XINGDU-TABLE-HEADER"],
        "binding": "PRINTED_HEADER_READS_CHIJI_XIAN_XINGDU; THIS_IS_A_DISTINCT_TABLE_FAMILY_FROM_TAIYIN_CHIJI",
        "purpose": "FIELD_CONTEXT_ONLY_NOT_A_TARGET_NUMERIC_READING",
    },
    70: {
        "table_identity": "LUNAR_LIMIT_XINGDU",
        "controls": ["VAR-NUM-LUNAR-L124-JI-XINGDU"],
        "binding": "SAME_CHIJI_XIAN_XINGDU_TABLE; PRINTED_LOWER_BAND_LIMITS_INCLUDE_118_TO_137; L124_MUST_BE_READ_FROM_JI_XINGDU_FIELD",
    },
}
REJECTED_PRIOR_BINDING = {
    "canvases": [68, 69, 70],
    "reason": "THESE_CANVASES_BELONG_TO_THE_DISTINCT_CHIJI_XIAN_XINGDU_TABLE; THE_PRIOR L8/L101/L114/L132 CHIJI_BINDINGS_ARE_REJECTED_BECAUSE_SHARED_LIMIT_NUMBERING_DOES_NOT_ESTABLISH_FIELD_IDENTITY",
    "scope": "REJECT_PRIOR_CROSS_TABLE_CHIJI_BINDINGS_ONLY; CANVAS_68_REMAINS_STRUCTURAL_XINGDU_EVIDENCE_AND_CANVAS_70_IS_A_VALID_LOCATOR_FOR_L124_JI_XINGDU",
    "target_value_authorized": False,
}


def fetch(url: str, timeout: int = 90) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json,image/*,*/*;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def body_for_canvas(canvas: dict) -> dict:
    pages = canvas.get("items") or []
    if not pages:
        raise ValueError("canvas annotation page missing")
    annotations = (pages[0] or {}).get("items") or []
    if not annotations:
        raise ValueError("canvas annotation missing")
    return (annotations[0] or {}).get("body") or {}


def native_url(body: dict) -> str:
    body_id = body.get("id") or body.get("@id")
    if body_id:
        return body_id
    service = body.get("service") or []
    if isinstance(service, dict):
        service = [service]
    if service:
        sid = (service[0] or {}).get("id") or (service[0] or {}).get("@id")
        if sid:
            return sid.rstrip("/") + "/full/max/0/default.jpg"
    raise ValueError("image body/service id missing")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="artifacts/kyushu-ogawa-target-pages")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    raw_manifest = fetch(MANIFEST_URL)
    manifest = json.loads(raw_manifest.decode("utf-8"))
    canvases = manifest.get("items") or []
    if manifest.get("type") != "Manifest" or not canvases:
        raise SystemExit("Kyushu IIIF Presentation 3 manifest expected")

    records = []
    for index, target in TARGETS.items():
        canvas = canvases[index]
        body = body_for_canvas(canvas)
        url = native_url(body)
        rec = {
            "canvas_index": index,
            "canvas_id": canvas.get("id"),
            "canvas_label": canvas.get("label"),
            "table_identity": target.get("table_identity", "LUNAR_CHIJI"),
            "controls": target["controls"],
            "printed_binding": target["binding"],
            "purpose": target.get("purpose", "TARGET_PAGE_LOCALIZATION_ONLY"),
            "url": url,
            "ocr_used": False,
            "target_values_authorized_by_fetch": False,
        }
        try:
            body_bytes = fetch(url)
            im = Image.open(io.BytesIO(body_bytes)).convert("RGB")
            path = out / f"canvas-{index:03d}.jpg"
            im.save(path, quality=95)
            rec.update({"status": "OK", "file": path.name, "size": [im.width, im.height], "bytes": len(body_bytes)})
        except Exception as exc:
            rec.update({"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
        records.append(rec)

    result = {
        "schema": "KYUSHU-OGAWA-1673-TARGET-PAGES-R1",
        "manifest_url": MANIFEST_URL,
        "title": manifest.get("label"),
        "viewing_direction": manifest.get("viewingDirection"),
        "ocr_used": False,
        "cross_copy_page_offset_used": False,
        "localization_basis": "DIRECT_CONTACT_SHEET_INSPECTION_OF_PRINTED_TABLE_TITLE_FIELD_HEADERS_AND_LIMIT_HEADINGS_IN_THIS_KYUSHU_COPY",
        "binding_invariant": "TABLE_IDENTITY_AND_FIELD_IDENTITY_MUST_MATCH_CONTROL_BEFORE_ANY_TARGET_READING",
        "cross_table_field_substitution_allowed": False,
        "target_values_authorized_by_fetch": False,
        "rejected_prior_binding": REJECTED_PRIOR_BINDING,
        "pages": records,
    }
    (out / "target-page-map.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if all(x.get("status") == "OK" for x in records) else 2


if __name__ == "__main__":
    raise SystemExit(main())
