#!/usr/bin/env python3
"""Build a non-authoritative structural inventory of frozen S00-S19.

The output contains hashes, counts, active-prefix headings and method-term
locations.  It intentionally does not copy source paragraphs or create new
astrological claims.  Curated knowledge cards are maintained separately.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SOURCE_LAYER = re.compile(r'"SOURCE_LAYER"\s*:\s*"([^"]+)"')
BEGIN_RETAINED = re.compile(r"^BEGIN_[A-Z0-9_]*(?:RETAINED|COMPLETE_FILE|PAYLOAD)")
METHOD_TERMS = {
    "CLASSICAL_QUANSHU": ("紫微斗数全书", "全书格局"),
    "ZHONGZHOU": ("中州派", "王亭之", "六十星系"),
    "FLYING_STAR_LIANG": ("梁若瑜", "飞星派", "自化", "禄忌线"),
    "HELUO_FANGWAI": ("河洛", "方外人", "气数位", "天地人三盘"),
    "ONE_HUNDRED_FORTY_FOUR": ("一四四诀", "144诀", "BODY_PALACE", "USE_PALACE"),
    "BAZI_CLASSICS": ("滴天髓", "渊海子平", "子平真诠", "神峰通考", "穷通宝鉴", "三命通会"),
    "BAZI_STRUCTURE_METHODS": ("月令", "格局", "扶抑", "调候", "通关", "病药", "从化"),
    "BAZI_AUXILIARY_SIGNALS": ("神煞", "伏吟", "反吟", "十恶大败"),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def inventory_source(root: Path, manifest_row: dict[str, Any]) -> dict[str, Any]:
    path = root / manifest_row["path"]
    size = path.stat().st_size
    digest = sha256_file(path)
    if size != manifest_row["bytes"] or digest != manifest_row["sha256"]:
        raise ValueError(f"canonical source integrity mismatch: {manifest_row['source_id']}")

    line_count = 0
    heading_count = 0
    json_record_count = 0
    case_example_record_count = 0
    retained_marker_count = 0
    source_layers: Counter[str] = Counter()
    method_counts: Counter[str] = Counter()
    method_first_lines: dict[str, int] = {}
    active_prefix_headings: list[dict[str, Any]] = []
    inside_active_prefix = True

    with path.open(encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line_count = line_number
            line = raw_line.rstrip("\r\n")
            if BEGIN_RETAINED.match(line):
                retained_marker_count += 1
                inside_active_prefix = False
            heading = HEADING.match(line)
            if heading:
                heading_count += 1
                if inside_active_prefix:
                    active_prefix_headings.append({
                        "level": len(heading.group(1)),
                        "line": line_number,
                        "title": heading.group(2),
                    })
            stripped = line.lstrip()
            if stripped.startswith("{") and stripped.endswith("}"):
                try:
                    value = json.loads(stripped)
                except json.JSONDecodeError:
                    value = None
                if isinstance(value, dict):
                    json_record_count += 1
                    if any(key in value for key in ("CASE_ID", "case_id", "case_role", "prediction_contribution_permission")):
                        case_example_record_count += 1
            layer = SOURCE_LAYER.search(line)
            if layer:
                source_layers[layer.group(1)] += 1
            for family, terms in METHOD_TERMS.items():
                hits = sum(line.count(term) for term in terms)
                if hits:
                    method_counts[family] += hits
                    method_first_lines.setdefault(family, line_number)

    return {
        "source_id": manifest_row["source_id"],
        "path": manifest_row["path"],
        "bytes": size,
        "sha256": digest,
        "runtime_role": manifest_row["runtime_role"],
        "line_count": line_count,
        "heading_count": heading_count,
        "json_record_line_count": json_record_count,
        "case_example_record_line_count": case_example_record_count,
        "retained_payload_marker_count": retained_marker_count,
        "source_layer_record_counts": dict(sorted(source_layers.items())),
        "method_term_occurrences": dict(sorted(method_counts.items())),
        "method_term_first_line": dict(sorted(method_first_lines.items())),
        "active_prefix_headings": active_prefix_headings,
        "curation_status": "STRUCTURALLY_INVENTORIED_NOT_FULLY_CURATED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("knowledge-workbench/source-inventory.json"),
    )
    args = parser.parse_args()
    root = args.repo.resolve()
    manifest_path = root / "sources" / "canonical-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    sources = [inventory_source(root, row) for row in manifest["sources"]]
    result = {
        "schema": "FORTUNE-KNOWLEDGE-SOURCE-INVENTORY-V1",
        "authority": "DERIVED_INDEX_ONLY",
        "canonical_manifest_path": "sources/canonical-manifest.json",
        "canonical_manifest_sha256": sha256_file(manifest_path),
        "source_count": len(sources),
        "total_bytes": sum(row["bytes"] for row in sources),
        "total_lines": sum(row["line_count"] for row in sources),
        "method_term_families": METHOD_TERMS,
        "sources": sources,
        "limitations": [
            "Term occurrence counts are navigation signals, not evidence weights.",
            "Active-prefix headings describe runtime boundaries but do not replace retained source text.",
            "Example records remain zero-contribution until independently evaluated under the training policy.",
        ],
    }
    output = args.output if args.output.is_absolute() else root / args.output
    write_json(output, result)
    print(json.dumps({
        "source_count": result["source_count"],
        "total_bytes": result["total_bytes"],
        "total_lines": result["total_lines"],
        "output": output.relative_to(root).as_posix(),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
