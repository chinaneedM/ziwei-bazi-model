from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .end_to_end import PREBLIND_STATUS, validate_staged_clean_start
from .util import FortuneError, atomic_write_json, read_json, sha256_file, utc_now


def _require(condition: bool, message: str, status: str) -> None:
    if not condition:
        raise FortuneError(message, status=status)


def _read_active_pointer(path: Path, schema: str, id_field: str, path_field: str) -> tuple[dict[str, Any], Path]:
    _require(path.is_file(), f"active pointer missing: {path}", "ACTIVE_RELEASE_POINTER_MISSING")
    pointer = read_json(path)
    _require(pointer.get("schema") == schema, f"active pointer schema invalid: {path}", "ACTIVE_RELEASE_POINTER_INVALID")
    _require(pointer.get("formal_release") == "YES", f"active pointer is not formal: {path}", "ACTIVE_RELEASE_POINTER_INVALID")
    release_path = Path(str(pointer.get(path_field, "")))
    _require(release_path.is_file(), f"active release missing: {release_path}", "ACTIVE_RELEASE_OBJECT_MISSING")
    release = read_json(release_path)
    _require(release.get(id_field) == pointer.get(id_field), f"active release identity mismatch: {path}", "ACTIVE_RELEASE_POINTER_INVALID")
    _require(release.get("object_hash") == pointer.get(path_field.replace("_path", "_object_hash")), f"active release hash mismatch: {path}", "ACTIVE_RELEASE_POINTER_INVALID")
    return pointer, release_path


def build_runtime_packet_request(
    clean_start_path: str | Path,
    output_path: str | Path,
    *,
    knowledge_pointer_path: str | Path = "knowledge/active-release.json",
    method_pointer_path: str | Path = "method/active-release.json",
    model_pointer_path: str | Path = "model/active-release.json",
) -> dict[str, Any]:
    clean_path = Path(clean_start_path)
    validation = validate_staged_clean_start(clean_path)
    clean = read_json(clean_path)
    _require(clean.get("status") == PREBLIND_STATUS, "clean start is not PREBLIND", "CLEAN_START_STAGE_INVALID")
    _require(clean.get("answer_data_available") is False, "answer data available", "ANSWER_ISOLATION_FAILED")

    knowledge_pointer, knowledge_release_path = _read_active_pointer(
        Path(knowledge_pointer_path),
        "FORTUNE-ACTIVE-KNOWLEDGE-RELEASE-POINTER-V1",
        "knowledge_release_id",
        "manifest_path",
    )
    method_pointer, method_release_path = _read_active_pointer(
        Path(method_pointer_path),
        "FORTUNE-ACTIVE-METHOD-RELEASE-POINTER-V1",
        "method_release_id",
        "method_release_path",
    )
    model_pointer, model_release_path = _read_active_pointer(
        Path(model_pointer_path),
        "FORTUNE-ACTIVE-MODEL-RELEASE-POINTER-V1",
        "model_release_id",
        "model_release_path",
    )

    bindings = dict(clean.get("active_runtime_binding") or {})
    expected = {
        "knowledge_release_id": knowledge_pointer["knowledge_release_id"],
        "method_release_id": method_pointer["method_release_id"],
        "model_release_id": model_pointer["model_release_id"],
        "main_prompt_runtime_id": method_pointer["main_prompt_runtime_id"],
    }
    for field, value in expected.items():
        _require(bindings.get(field) == value, f"clean-start binding mismatch: {field}", "RUNTIME_BINDING_MISMATCH")

    result = {
        "schema": "GROUP-RUNTIME-PACKET-REQUEST-V2",
        "status": "REQUESTED",
        "group_id": clean["group_id"],
        "group_run_id": clean["group_run_id"],
        "clean_start_path": str(clean_path),
        "clean_start_sha256": sha256_file(clean_path),
        "clean_start_validation_object_hash": validation["object_hash"],
        "knowledge_manifest_path": str(knowledge_release_path),
        "knowledge_manifest_sha256": sha256_file(knowledge_release_path),
        "method_release_path": str(method_release_path),
        "method_release_sha256": sha256_file(method_release_path),
        "model_release_path": str(model_release_path),
        "model_release_sha256": sha256_file(model_release_path),
        "output_root": str(clean_path.parent),
        "bindings": {
            **expected,
            "learning_policy_id": bindings.get("learning_policy_id"),
        },
        "repository_search_used": False,
        "answer_data_available": False,
        "created_at": utc_now(),
    }
    target = atomic_write_json(output_path, result)
    return {**result, "request_path": str(target), "request_sha256": sha256_file(target)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="create-runtime-packet-request")
    parser.add_argument("--clean-start", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        result = build_runtime_packet_request(args.clean_start, args.output)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except FortuneError as exc:
        print(json.dumps({"status": exc.status, "error": str(exc)}, ensure_ascii=False), file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
