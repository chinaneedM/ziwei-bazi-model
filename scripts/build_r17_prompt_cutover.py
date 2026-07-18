#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

R17_RUNTIME_ID = "MP-PROFESSIONAL-REASONING-20260718-R17"
R16_RELEASE_ID = "KNOWLEDGE-R16"
R17_RELEASE_ID = "KNOWLEDGE-R17-PROMPT-CUTOVER-CANDIDATE"
LIBRARIES = tuple(f"S{i:02d}" for i in range(20))


class CutoverError(RuntimeError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def object_hash(value: dict[str, Any]) -> str:
    body = dict(value)
    body.pop("object_hash", None)
    return hashlib.sha256(canonical_bytes(body)).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise CutoverError(f"JSON object required: {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = dict(value)
    body["object_hash"] = object_hash(body)
    path.write_text(
        json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def prompt_metrics(data: bytes) -> dict[str, Any]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CutoverError("prompt export is not valid UTF-8") from exc
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"
    return {
        "sha256_raw_bytes": sha256_bytes(data),
        "size_bytes": len(data),
        "sha256_utf8_lf_trailing_lf": sha256_bytes(normalized.encode("utf-8")),
        "normalized_size_bytes": len(normalized.encode("utf-8")),
        "visible_nonwhitespace_codepoints": sum(1 for char in text if not char.isspace()),
        "bom": data.startswith(b"\xef\xbb\xbf"),
        "lf_count": text.count("\n"),
        "crlf_count": text.count("\r\n"),
        "leading_whitespace_codepoints": len(text) - len(text.lstrip()),
        "trailing_whitespace_codepoints": len(text) - len(text.rstrip()),
        "runtime_id_present": R17_RUNTIME_ID in text,
    }


def build_prompt_snapshot(args: argparse.Namespace) -> int:
    source = Path(args.input)
    raw = source.read_bytes()
    metrics = prompt_metrics(raw)
    expected_normalized = args.expected_normalized_sha256
    normalized_match = expected_normalized is None or metrics["sha256_utf8_lf_trailing_lf"] == expected_normalized
    status = "PASS" if metrics["runtime_id_present"] and normalized_match else "REVIEW_REQUIRED"
    target_text = Path(args.output_text)
    target_receipt = Path(args.output_receipt)
    if target_text.exists() or target_receipt.exists():
        raise CutoverError("snapshot target already exists; create a new immutable version")
    target_text.parent.mkdir(parents=True, exist_ok=True)
    target_text.write_bytes(raw)
    receipt = {
        "schema": "MAIN-PROMPT-AUDIT-SNAPSHOT-V1",
        "runtime_id": R17_RUNTIME_ID,
        "authority_statement": "AUDIT_COPY_ONLY_NOT_RUNTIME_AUTHORITY",
        "capture_method": "OPERATOR_EXPORTED_ACTIVE_PROJECT_CUSTOM_INSTRUCTIONS",
        "snapshot_path": target_text.as_posix(),
        "snapshot_sha256": metrics["sha256_raw_bytes"],
        "snapshot_bytes": metrics["size_bytes"],
        "candidate_normalized_sha256": expected_normalized,
        "candidate_normalized_match": normalized_match,
        "actual": metrics,
        "checks": {
            "utf8": True,
            "runtime_id": metrics["runtime_id_present"],
            "candidate_normalized_match": normalized_match,
            "snapshot_copy_hash": sha256_file(target_text) == metrics["sha256_raw_bytes"],
        },
        "status": status,
        "formal_release": "NO",
        "score_eligibility": "PROHIBITED_PENDING_S19_MODEL_AND_SHADOW_VALIDATION",
    }
    write_json(target_receipt, receipt)
    print(json.dumps(receipt | {"object_hash": object_hash(receipt)}, ensure_ascii=False, indent=2))
    return 0 if status == "PASS" else 2


def validate_base(base_dir: Path, manifest: dict[str, Any]) -> None:
    if manifest.get("knowledge_release_id") != R16_RELEASE_ID:
        raise CutoverError("R16 base manifest required")
    rows = manifest.get("source_files")
    if not isinstance(rows, list) or [row.get("library_id") for row in rows] != list(LIBRARIES):
        raise CutoverError("base manifest must contain ordered S00-S19 rows")
    for row in rows:
        path = base_dir / row["canonical_filename"]
        if not path.is_file():
            raise CutoverError(f"missing base library: {path}")
        if sha256_file(path) != row["sha256_raw_file_bytes"]:
            raise CutoverError(f"base hash mismatch: {row['library_id']}")
        if path.stat().st_size != row["file_size_bytes"]:
            raise CutoverError(f"base size mismatch: {row['library_id']}")


def r17_s19_overlay(prompt: dict[str, Any]) -> bytes:
    actual = prompt["actual"]
    lines = [
        "# R17半自动化仓库运行与提示词—方法解耦唯一活动控制根",
        "",
        "```text",
        "CURRENT_ACTIVE_CONTROL_ROOT=THIS_SECTION",
        "CURRENT_ACTIVE_CONTROL_ROOT_PRECEDENCE=ABSOLUTE_HIGHEST_WITHIN_S19",
        "LIBRARY_ID=S19",
        "PATCH_ID=R17-REPOSITORY-BOUND-SEMI-AUTOMATION-CUTOVER-20260718-R1",
        "PATCH_SCOPE=PROMPT_BINDING_STATE_AUTHORITY_GROUP_POLICY_AND_REPOSITORY_RUNTIME_CUTOVER_ONLY",
        "BASE_ASTROLOGICAL_KNOWLEDGE_CHANGE_PERMISSION=NO",
        "CORRECT_ANSWER_AS_RULE_PERMISSION=NO",
        "CASE_SPECIFIC_DIRECTION_RULE_PERMISSION=NO",
        f"EXPECTED_MAIN_PROMPT_RUNTIME_ID={R17_RUNTIME_ID}",
        f"EXPECTED_MAIN_PROMPT_SHA256_RAW_BYTES={prompt['snapshot_sha256']}",
        f"EXPECTED_MAIN_PROMPT_SIZE_BYTES={prompt['snapshot_bytes']}",
        f"EXPECTED_MAIN_PROMPT_VISIBLE_CHARACTER_COUNT={actual['visible_nonwhitespace_codepoints']}",
        "EXPECTED_MAIN_PROMPT_VISIBLE_CHARACTER_COUNT_METHOD=UNICODE_NON_WHITESPACE_CODEPOINT_COUNT",
        "EXECUTION_ARCHITECTURE=USER_INITIATED_REPOSITORY_BOUND_SEMI_AUTOMATION",
        "BACKGROUND_MODEL_EXECUTION_PERMISSION=NO",
        "GITHUB_AUTONOMOUS_CHATGPT_WAKE_PERMISSION=NO",
        "REPOSITORY_STATE_AUTHORITY=YES",
        "SYSTEM_MANAGED_STATE_CAPSULE_RUNTIME_AUTHORITY=NO",
        "FIXED_TEN_CASE_BLOCK_RUNTIME_AUTHORITY=NO",
        "FIXED_CASE_COUNT_OR_QUESTION_COUNT_PERMISSION=NO",
        "GROUP_SIZE_ORDER_UNIT_THRESHOLD_AND_REGRESSION_SCOPE_AUTHORITY=GROUP_MANIFEST|RUN_CONTRACT|LEARNING_POLICY",
        "PROJECT_UPLOADED_S00_S19_RUNTIME_SOURCE_PERMISSION=NO",
        "PROJECT_UPLOAD_OR_MODEL_MEMORY_FALLBACK_PERMISSION=NO",
        "SOURCE_PACKET_BEFORE_REASONING_REQUIRED=YES",
        "METHOD_PACKET_BEFORE_REASONING_REQUIRED=YES",
        "CAUSAL_USE_PASS_REQUIRED_FOR_SCORE=YES",
        "AUTOMATION_RUNTIME_INSTALL_STATUS=INTERFACES_INSTALLED_R17_CUTOVER_SHADOW_VALIDATION_PENDING",
        "FORMAL_RELEASE=NO",
        "LOWER_CONFLICTING_PROMPT_ID_PROMPT_HASH_STATE_CAPSULE_FIXED_BLOCK_GROUP_SIZE_BACKGROUND_EXECUTION_AND_FALLBACK_RULES=HISTORICAL_AUDIT_ONLY",
        "LOWER_SOURCE_TEXT_KNOWLEDGE_CONDITIONS_NEGATIONS_EXCEPTIONS_ALTERNATIVES_AND_RECOVERY=ACTIVE_BY_DIRECT_REFERENCE",
        "```",
        "",
        "本节只迁移运行绑定和状态权威，不改变任何紫微、八字或现实语义知识。R16完整文件继续保留在下文作为历史父版本；与本节冲突的旧提示词ID、固定十案块、跨对话状态胶囊、后台执行、项目文件回退和旧安装状态不得重新取得运行权限。",
        "",
        "BEGIN_S19_RETAINED_R16_COMPLETE_FILE",
        "",
    ]
    return ("\n".join(lines)).encode("utf-8")


def build_knowledge_candidate(args: argparse.Namespace) -> int:
    base_dir = Path(args.base_dir)
    base_manifest_path = Path(args.base_manifest)
    output_dir = Path(args.output_dir)
    prompt_receipt_path = Path(args.prompt_receipt)

    if output_dir.exists():
        raise CutoverError("candidate directory already exists")
    if "knowledge/candidates/" not in output_dir.as_posix().replace("\\", "/"):
        raise CutoverError("output must be under knowledge/candidates")

    manifest = read_json(base_manifest_path)
    validate_base(base_dir, manifest)
    prompt = read_json(prompt_receipt_path)
    if prompt.get("schema") != "MAIN-PROMPT-AUDIT-SNAPSHOT-V1" or prompt.get("status") != "PASS":
        raise CutoverError("exact R17 prompt snapshot PASS required")
    if prompt.get("runtime_id") != R17_RUNTIME_ID:
        raise CutoverError("prompt runtime ID mismatch")
    snapshot_path = Path(prompt.get("snapshot_path", ""))
    if not snapshot_path.is_file() or sha256_file(snapshot_path) != prompt.get("snapshot_sha256"):
        raise CutoverError("prompt snapshot readback failed")

    temp_parent = output_dir.parent
    temp_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".r17-cutover.", dir=temp_parent) as temp_name:
        staged = Path(temp_name) / output_dir.name
        staged.mkdir()
        for row in manifest["source_files"]:
            shutil.copy2(base_dir / row["canonical_filename"], staged / row["canonical_filename"])

        s19_filename = next(row["canonical_filename"] for row in manifest["source_files"] if row["library_id"] == "S19")
        s19_path = staged / s19_filename
        original_s19 = s19_path.read_bytes()
        s19_path.write_bytes(r17_s19_overlay(prompt) + original_s19)

        source_rows = []
        for library_id in LIBRARIES:
            matches = list(staged.glob(f"{library_id}_*.txt"))
            if len(matches) != 1:
                raise CutoverError(f"candidate library set invalid: {library_id}")
            path = matches[0]
            source_rows.append({
                "library_id": library_id,
                "canonical_filename": path.name,
                "repository_relative_path": f"{output_dir.as_posix()}/{path.name}",
                "sha256_raw_file_bytes": sha256_file(path),
                "file_size_bytes": path.stat().st_size,
            })

        candidate_manifest = {
            "schema": "FORTUNE-KNOWLEDGE-RELEASE-MANIFEST-V1",
            "knowledge_release_id": args.release_id,
            "release_kind": "CANDIDATE",
            "parent_release_id": manifest["knowledge_release_id"],
            "repository_full_name": args.repository,
            "repository_commit_sha": args.source_content_commit,
            "source_root": output_dir.as_posix(),
            "source_authority": "GITHUB_REPOSITORY",
            "source_file_count": 20,
            "source_files": source_rows,
            "s19_binding_sha256": manifest["s19_binding_sha256"],
            "prompt_runtime_id": R17_RUNTIME_ID,
            "prompt_snapshot_sha256": prompt["snapshot_sha256"],
            "prompt_snapshot_receipt_sha256": sha256_file(prompt_receipt_path),
            "changed_library_ids": ["S19"],
            "unchanged_library_ids": list(LIBRARIES[:-1]),
            "immutability": "NO_IN_PLACE_MUTATION",
            "promotion_status": "BLOCKED_PENDING_FULL_READBACK_CONTAMINATION_SHADOW_CAUSAL_AND_APPROVAL",
            "score_eligibility": "BLOCKED_PENDING_CAUSAL_SHADOW_VALIDATION",
            "formal_release": "NO",
        }
        write_json(staged / "release-manifest.json", candidate_manifest)
        receipt = {
            "schema": "R17-PROMPT-S19-CUTOVER-BUILD-RECEIPT-V1",
            "status": "PASS_CANDIDATE_BUILT_NOT_PROMOTED",
            "base_manifest_sha256": sha256_file(base_manifest_path),
            "prompt_snapshot_receipt_sha256": sha256_file(prompt_receipt_path),
            "knowledge_release_id": args.release_id,
            "changed_library_ids": ["S19"],
            "s19_candidate_sha256": source_rows[-1]["sha256_raw_file_bytes"],
            "source_file_count": len(source_rows),
            "formal_release": "NO",
            "score_eligibility": "PROHIBITED",
        }
        write_json(staged / "cutover-build-receipt.json", receipt)
        staged.replace(output_dir)

    print(json.dumps(read_json(output_dir / "cutover-build-receipt.json"), ensure_ascii=False, indent=2))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Build the R17 prompt/S19 cutover without mutating R16.")
    sub = root.add_subparsers(dest="command", required=True)

    snapshot = sub.add_parser("snapshot")
    snapshot.add_argument("--input", required=True)
    snapshot.add_argument("--output-text", required=True)
    snapshot.add_argument("--output-receipt", required=True)
    snapshot.add_argument("--expected-normalized-sha256")
    snapshot.set_defaults(handler=build_prompt_snapshot)

    candidate = sub.add_parser("knowledge-candidate")
    candidate.add_argument("--base-dir", required=True)
    candidate.add_argument("--base-manifest", required=True)
    candidate.add_argument("--prompt-receipt", required=True)
    candidate.add_argument("--output-dir", required=True)
    candidate.add_argument("--source-content-commit", required=True)
    candidate.add_argument("--repository", default="chinaneedM/ziwei-bazi-model")
    candidate.add_argument("--release-id", default=R17_RELEASE_ID)
    candidate.set_defaults(handler=build_knowledge_candidate)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except (CutoverError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
