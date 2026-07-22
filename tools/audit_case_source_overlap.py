#!/usr/bin/env python3
"""Audit exact case-question overlap with frozen canonical source text.

The source library contains teaching cases as well as general doctrine.  A
question that already appears in those sources is not a clean blind example,
even when the separate answer vault is empty.  This scanner uses a small
Aho-Corasick automaton so the complete S00-S19 corpus is read only once.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path
from typing import Any


MIN_PATTERN_LENGTH = 8
NEARBY_LINE_WINDOW = 20


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def object_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_automaton(patterns: list[str]) -> tuple[list[dict[str, int]], list[int], list[list[int]]]:
    transitions: list[dict[str, int]] = [{}]
    failures = [0]
    outputs: list[list[int]] = [[]]
    for pattern_id, pattern in enumerate(patterns):
        state = 0
        for character in pattern:
            next_state = transitions[state].get(character)
            if next_state is None:
                next_state = len(transitions)
                transitions[state][character] = next_state
                transitions.append({})
                failures.append(0)
                outputs.append([])
            state = next_state
        outputs[state].append(pattern_id)

    queue: collections.deque[int] = collections.deque(transitions[0].values())
    while queue:
        state = queue.popleft()
        for character, next_state in transitions[state].items():
            queue.append(next_state)
            failure = failures[state]
            while failure and character not in transitions[failure]:
                failure = failures[failure]
            failures[next_state] = transitions[failure].get(character, 0)
            outputs[next_state].extend(outputs[failures[next_state]])
    return transitions, failures, outputs


def scan_line(
    line: str,
    transitions: list[dict[str, int]],
    failures: list[int],
    outputs: list[list[int]],
) -> set[int]:
    found: set[int] = set()
    state = 0
    for character in line:
        while state and character not in transitions[state]:
            state = failures[state]
        state = transitions[state].get(character, 0)
        found.update(outputs[state])
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("case-bank/source-overlap-audit.json"),
    )
    args = parser.parse_args()
    root = args.repo.resolve()

    metadata_by_pattern: dict[str, list[dict[str, str | None]]] = collections.defaultdict(list)
    for case_path in sorted((root / "case-bank" / "cases").glob("CASE-*.json")):
        case = json.loads(case_path.read_text(encoding="utf-8"))
        for question in case["questions"]["parsed"]:
            stem = normalize(question["stem"])
            if len(stem) >= MIN_PATTERN_LENGTH:
                metadata_by_pattern[stem].append(
                    {
                        "case_id": case["case_id"],
                        "question_id": question["question_id"],
                        "kind": "STEM",
                        "option_id": None,
                    }
                )
            for option in question["options"]:
                text = normalize(option["text"])
                if len(text) >= MIN_PATTERN_LENGTH:
                    metadata_by_pattern[text].append(
                        {
                            "case_id": case["case_id"],
                            "question_id": question["question_id"],
                            "kind": "OPTION",
                            "option_id": option["option_id"],
                        }
                    )

    patterns = sorted(metadata_by_pattern)
    transitions, failures, outputs = build_automaton(patterns)
    matches: list[dict[str, Any]] = []
    for source_path in sorted((root / "sources" / "canonical").glob("S*.txt")):
        source_id = source_path.name[:3]
        with source_path.open(encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                line = normalize(raw_line)
                if len(line) < MIN_PATTERN_LENGTH:
                    continue
                for pattern_id in scan_line(line, transitions, failures, outputs):
                    pattern = patterns[pattern_id]
                    for metadata in metadata_by_pattern[pattern]:
                        matches.append(
                            {
                                **metadata,
                                "source_id": source_id,
                                "source_path": source_path.relative_to(root).as_posix(),
                                "line": line_number,
                                "matched_text": pattern,
                            }
                        )

    by_question_source: dict[tuple[str, str, str], list[dict[str, Any]]] = collections.defaultdict(list)
    for match in matches:
        by_question_source[(match["case_id"], match["question_id"], match["source_id"])].append(match)

    risk_rows: list[dict[str, Any]] = []
    for (case_id, question_id, source_id), rows in sorted(by_question_source.items()):
        stem_lines = [row["line"] for row in rows if row["kind"] == "STEM"]
        option_rows = [row for row in rows if row["kind"] == "OPTION"]
        nearby_options: list[str] = []
        if stem_lines:
            nearby_options = sorted(
                {
                    row["option_id"]
                    for row in option_rows
                    if any(abs(row["line"] - stem_line) <= NEARBY_LINE_WINDOW for stem_line in stem_lines)
                }
            )
        option_cluster: list[str] = []
        for anchor in option_rows:
            cluster = sorted(
                {
                    row["option_id"]
                    for row in option_rows
                    if abs(row["line"] - anchor["line"]) <= NEARBY_LINE_WINDOW
                }
            )
            if len(cluster) > len(option_cluster):
                option_cluster = cluster
        if not stem_lines and len(option_cluster) < 2:
            continue
        risk_rows.append(
            {
                "case_id": case_id,
                "question_id": question_id,
                "source_id": source_id,
                "stem_lines": sorted(set(stem_lines)),
                "nearby_option_ids": nearby_options,
                "option_cluster_ids": option_cluster,
                "risk": "HIGH" if len(option_cluster) >= 2 or len(nearby_options) >= 2 else "REVIEW_REQUIRED",
            }
        )

    exact_stem_questions = sorted(
        {
            (row["case_id"], row["question_id"])
            for row in risk_rows
            if row["stem_lines"]
        }
    )
    high_risk_questions = sorted(
        {(row["case_id"], row["question_id"]) for row in risk_rows if row["risk"] == "HIGH"}
    )
    source_exposed_case_ids = sorted({case_id for case_id, _ in high_risk_questions})
    development_path = root / "case-bank" / "partitions" / "development.json"
    development = json.loads(development_path.read_text(encoding="utf-8"))
    development_cases = set(development["case_order"])
    uncontained = sorted(set(source_exposed_case_ids) - development_cases)
    if not uncontained:
        development["source_exposed_case_ids"] = source_exposed_case_ids
        development["first_blind_schedule"] = [
            case_id
            for case_id in development["first_blind_schedule"]
            if case_id not in source_exposed_case_ids
        ]
        write_json(development_path, development)
    report = {
        "schema": "CASE-SOURCE-OVERLAP-AUDIT-V1",
        "case_bank_manifest_sha256": object_sha256(
            json.loads((root / "case-bank" / "manifest.json").read_text(encoding="utf-8"))
        ),
        "canonical_source_manifest_sha256": object_sha256(
            json.loads((root / "sources" / "canonical-manifest.json").read_text(encoding="utf-8"))
        ),
        "scope": "EXACT_NORMALIZED_TEXT_ONLY",
        "minimum_pattern_length": MIN_PATTERN_LENGTH,
        "nearby_line_window": NEARBY_LINE_WINDOW,
        "pattern_count": len(patterns),
        "raw_match_count": len(matches),
        "exact_stem_question_count": len(exact_stem_questions),
        "exact_stem_case_ids": sorted({case_id for case_id, _ in exact_stem_questions}),
        "high_risk_question_count": len(high_risk_questions),
        "high_risk_case_ids": sorted({case_id for case_id, _ in high_risk_questions}),
        "source_exposed_case_ids": source_exposed_case_ids,
        "uncontained_high_risk_case_ids": uncontained,
        "question_source_findings": risk_rows,
        "option_only_matches": [
            {
                "case_id": row["case_id"],
                "question_id": row["question_id"],
                "option_id": row["option_id"],
                "source_id": row["source_id"],
                "line": row["line"],
                "matched_text": row["matched_text"],
            }
            for row in matches
            if row["kind"] == "OPTION"
        ],
        "interpretation": (
            "HIGH means an exact question stem and at least two exact options occur within the configured "
            "line window in one canonical source; REVIEW_REQUIRED means the exact stem occurs without that "
            "full nearby option pattern. Two or more nearby options from one question are also HIGH even "
            "without an exact stem. HIGH cases are development references, excluded from first-blind schedules. "
            "Exact overlap is a leakage screen, not proof that an answer is present."
        ),
    }
    output = args.output if args.output.is_absolute() else root / args.output
    write_json(output, report)
    print(json.dumps({key: report[key] for key in (
        "pattern_count",
        "raw_match_count",
        "exact_stem_question_count",
        "high_risk_question_count",
        "high_risk_case_ids",
    )}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
