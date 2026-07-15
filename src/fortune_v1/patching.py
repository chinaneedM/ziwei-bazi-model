from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .util import atomic_write_json, read_json, sha256_file, utc_now

CASE_ID_PATTERN = re.compile(r"\bCASE[-_A-Z0-9]{6,}\b", re.I)
ANSWER_VECTOR_PATTERN = re.compile(r"(?:答案|answer)[^\n]{0,20}\b[A-H](?:\s*[,，、/|-]?\s*[A-H]){1,}\b", re.I)
OPTION_MEMORY_PATTERN = re.compile(r"(?:这个|该|本)案例[^\n]{0,80}(?:优先|选择|选)[^\n]{0,20}[A-H]", re.I)
BARE_DIRECTION_PATTERN = re.compile(r"(?:总是|一律|必选|直接选|固定选)\s*[A-H]", re.I)
DATE_PATTERN = re.compile(r"\b(?:18|19|20)\d{2}[-/.年]\d{1,2}(?:[-/.月]\d{1,2}日?)?\b")
AMOUNT_IDENTITY_PATTERN = re.compile(r"(?:人民币|年收入|金额|局长|董事长|总经理|判刑|手术)[^\n]{0,30}")


def scan_patch(patch_path: str | Path, output_path: str | Path,
               case_fingerprint_path: str | Path | None = None) -> dict[str, Any]:
    path = Path(patch_path); text = path.read_text(encoding="utf-8")
    findings = []
    patterns = {
        "CASE_ID": CASE_ID_PATTERN, "ANSWER_VECTOR": ANSWER_VECTOR_PATTERN,
        "CASE_OPTION_MEMORY": OPTION_MEMORY_PATTERN, "BARE_DIRECTION_RULE": BARE_DIRECTION_PATTERN,
        "UNIQUE_DATE": DATE_PATTERN, "UNIQUE_AMOUNT_OR_IDENTITY": AMOUNT_IDENTITY_PATTERN,
    }
    for kind, pattern in patterns.items():
        for match in pattern.finditer(text):
            findings.append({"kind": kind, "offset": match.start(), "sha256": __import__("hashlib").sha256(match.group(0).encode()).hexdigest()})
    if case_fingerprint_path:
        fingerprint = read_json(case_fingerprint_path)
        for value in fingerprint.get("unique_literals", []):
            if isinstance(value, str) and len(value) >= 4 and value in text:
                findings.append({"kind": "CASE_UNIQUE_LITERAL", "offset": text.index(value), "literal_sha256": __import__("hashlib").sha256(value.encode()).hexdigest()})
        for long_text in fingerprint.get("unique_long_texts", []):
            if isinstance(long_text, str) and len(long_text) >= 16 and long_text in text:
                findings.append({"kind": "QUESTION_UNIQUE_LONG_TEXT", "offset": text.index(long_text), "literal_sha256": __import__("hashlib").sha256(long_text.encode()).hexdigest()})
    parent_chain_missing = False
    try:
        obj = json.loads(text)
        parent_chain_missing = not bool(obj.get("universal_parent_chain"))
    except json.JSONDecodeError:
        parent_chain_missing = not bool(re.search(r"(?:SOURCE_PARENT|universal_parent_chain|来源父链)", text, re.I))
    if parent_chain_missing:
        findings.append({"kind": "UNIVERSAL_SOURCE_PARENT_CHAIN_MISSING", "offset": None})
    result = {
        "schema": "PATCH-LEAK-SCAN-V1", "patch_path": str(path), "patch_sha256": sha256_file(path),
        "status": "PATCH_REJECTED_CASE_SPECIFIC" if findings else "PASS", "findings": findings, "scanned_at": utc_now(),
    }
    atomic_write_json(output_path, result)
    return result

