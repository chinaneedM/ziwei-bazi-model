from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import FortuneError, atomic_write_json, read_json, sha256_file, slug, utc_now

FIELD_STATES = {"VERIFIED", "READABLE_UNCONFIRMED", "AMBIGUOUS", "MISSING", "CONFLICT"}
CRITICAL_FIELDS = {"solar_term_pillars", "start_luck_age", "handover_time", "major_luck_cycles"}


def freeze_transcription(case_id: str, image_path: str | Path, transcription_json: str | Path,
                         output_path: str | Path, method: str = "HUMAN_VERIFIED_ENTRY",
                         method_version: str = "1") -> dict[str, Any]:
    source = read_json(transcription_json)
    versions = source.get("versions", [])
    if not versions:
        raise FortuneError("at least one transcription version is required", status="INPUT_QUARANTINE")
    for version in versions:
        fields = version.get("fields", {})
        for name, field in fields.items():
            if field.get("state") not in FIELD_STATES:
                raise FortuneError(f"invalid state for {name}", status="INPUT_QUARANTINE")
        critical_bad = [name for name in CRITICAL_FIELDS if fields.get(name, {}).get("state") in {None, "AMBIGUOUS", "MISSING", "CONFLICT"}]
        version["status"] = "INPUT_QUARANTINE" if critical_bad else version.get("status", "VALID")
        version["critical_unresolved"] = critical_bad
    if all(v["status"] == "INPUT_QUARANTINE" for v in versions):
        overall = "INPUT_QUARANTINE"
    elif len(versions) > 1:
        overall = "LEGAL_PARALLEL_VERSIONS"
    else:
        overall = "VALID"
    result = {
        "schema": "BAZI-FROZEN-TRANSCRIPTION-V1", "case_id": case_id,
        "object_id": f"BAZI-{slug(case_id)}-{sha256_file(image_path)[:12]}",
        "image_sha256": sha256_file(image_path), "method": method, "method_version": method_version,
        "versions": versions, "overall_status": overall, "frozen_at": utc_now(),
    }
    atomic_write_json(output_path, result)
    Path(output_path).chmod(0o444)
    return result

