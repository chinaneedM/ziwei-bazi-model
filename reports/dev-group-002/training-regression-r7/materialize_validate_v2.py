#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import materialize_validate as v1

BAZI_SHARED_PARENT_IDS = {
    "VERIFIED_ABSTENTION_HIGH_RISK_TASKS",
    "BAZI_ROLE_TO_REALITY_CHAIN",
}


def patch_objects(repo_root: Path, objects: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    source_spec = v1.read_json(repo_root / v1.INPUTS["r2_source_spec"])
    excerpt_index = {entry["excerpt_id"]: entry for entry in source_spec["entries"]}

    source_registry = dict(objects["source-registry.json"])
    rows = list(source_registry["rows"])
    existing = {row["call_id"] for row in rows}
    for parent_id in sorted(BAZI_SHARED_PARENT_IDS):
        if parent_id in existing:
            continue
        entry = excerpt_index.get(parent_id)
        if entry is None:
            raise ValueError(f"missing Bazi shared parent excerpt: {parent_id}")
        rows.append(
            {
                "call_id": parent_id,
                "library": entry["library_id"],
                "purpose": entry["purpose"],
                "required_text": None,
                "required_text_sha256": entry["excerpt_sha256"],
                "capability_ceiling": "GENERIC_BAZI_CAPABILITY_BOUNDARY_ONLY",
                "applicability": "FULL_PARENT_SEGMENT_MATERIALIZED_IN_R2",
                "parent_artifact": v1.INPUTS["r2_source_spec"],
                "canonical_path": entry["canonical_path"],
                "line_start": entry["line_start"],
                "line_end": entry["line_end"],
            }
        )
    source_registry["rows"] = rows
    source_registry["row_count"] = len(rows)
    source_registry = v1.with_hash(source_registry)

    bindings = dict(objects["track-option-parent-bindings.json"])
    bindings["parent_source_registry_sha256"] = source_registry["canonical_sha256"]
    bindings = v1.with_hash(bindings)

    adjudication = dict(objects["pairwise-adjudication.json"])
    adjudication["parent_bindings_sha256"] = bindings["canonical_sha256"]
    adjudication = v1.with_hash(adjudication)

    manifest = dict(objects["manifest.json"])
    manifest["artifacts"] = dict(manifest["artifacts"])
    manifest["artifacts"]["source_registry"] = dict(manifest["artifacts"]["source_registry"])
    manifest["artifacts"]["source_registry"]["canonical_sha256"] = source_registry["canonical_sha256"]
    manifest["artifacts"]["source_registry"]["row_count"] = source_registry["row_count"]
    manifest["artifacts"]["parent_bindings"] = dict(manifest["artifacts"]["parent_bindings"])
    manifest["artifacts"]["parent_bindings"]["canonical_sha256"] = bindings["canonical_sha256"]
    manifest["artifacts"]["adjudication"] = dict(manifest["artifacts"]["adjudication"])
    manifest["artifacts"]["adjudication"]["canonical_sha256"] = adjudication["canonical_sha256"]
    manifest = v1.with_hash(manifest)

    patched = dict(objects)
    patched["source-registry.json"] = source_registry
    patched["track-option-parent-bindings.json"] = bindings
    patched["pairwise-adjudication.json"] = adjudication
    patched["manifest.json"] = manifest
    return patched


def materialize(repo_root: Path) -> None:
    output_dir = repo_root / v1.ROUND_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    objects = patch_objects(repo_root, v1.build_objects(repo_root))
    for filename, obj in objects.items():
        v1.write_json(output_dir / filename, obj)

    stats = objects["manifest.json"]["statistics"]
    summary = f"""# DEV-GROUP-002 R7：DEV-EXAMPLE-001逐选项来源父链重建

R7完整保留R1—R6，仅对仓库中具有真实来源调用正文的DEV-EXAMPLE-001进行逐轨、逐选项重建。20条紫微选项行已绑定本轨来源父对象；八字仍缺S11—S15独立父对象，因此不能密封或融合。

本轮从来源方向重建了{stats['evidence_reconstructed_pairwise_rows']}组成对理由，另有{stats['low_information_forced_pairwise_rows_in_processed_case']}组因方向同距继续低信息强制决胜。Q3中创业选项受到“均不宜自行经商”的直接反证，不能再排在无直接反证的“不用工作”选项之前，因此全排序由`DBCA`修正为`DBAC`。该变化只涉及第三、第四位，TOP1和TOP2不变。

全组`TRAINING_REGRESSION_SCORE`仍为TOP1 {stats['top1_hits']}/25、TOP2 {stats['top2_coverage']}/25。正式有效题、本地机器密封和S03融合仍全部为0；S00—S19和基础命理知识未修改。

R7验证器V2同时修复两项纯接口错误：登记八字共享能力边界父对象，并按实际对象重算有效紫微方向行为5条。其余四案没有保存可重放的来源调用正文，下一轮必须先恢复DEV-EXAMPLE-002的真实调用体；若不能恢复，应失败关闭而不是按计数或旧排序猜测方向。
"""
    (output_dir / "summary.md").write_text(summary, encoding="utf-8")


def validate(repo_root: Path) -> dict[str, Any]:
    result = v1.validate(repo_root)
    expected_v1_interface_error = "unexpected effective Ziwei option count"
    errors = [error for error in result.get("errors", []) if error != expected_v1_interface_error]

    bindings = v1.read_json(repo_root / v1.ROUND_DIR / "track-option-parent-bindings.json")
    source_registry = v1.read_json(repo_root / v1.ROUND_DIR / "source-registry.json")
    registry_ids = {row["call_id"] for row in source_registry["rows"]}
    effective_ziwei = [
        row for row in bindings["track_rows"]
        if row["track_id"] == "ZIWEI" and row["effective"]
    ]
    if len(effective_ziwei) != 5:
        errors.append("V2 effective Ziwei option count")
    if not BAZI_SHARED_PARENT_IDS.issubset(registry_ids):
        errors.append("V2 Bazi shared parent registration")

    result["schema"] = "DEV-GROUP-002-R7-VALIDATION-V2"
    result["errors"] = errors
    result["error_count"] = len(errors)
    result["status"] = "PASS" if not errors else "FAIL"
    result["effective_ziwei_option_rows"] = len(effective_ziwei)
    result["bazi_shared_parent_ids_registered"] = sorted(BAZI_SHARED_PARENT_IDS)
    result["validator_interface_fix"] = "PASS" if not errors else "FAIL"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    if not args.write and not args.validate:
        parser.error("select --write and/or --validate")
    if args.write:
        materialize(repo_root)
    if args.validate:
        result = validate(repo_root)
        output_dir = repo_root / v1.ROUND_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        v1.write_json(output_dir / "validation.json", result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0 if result["status"] == "PASS" else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
