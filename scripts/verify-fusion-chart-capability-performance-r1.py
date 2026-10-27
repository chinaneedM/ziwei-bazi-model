#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-CAPABILITY-MATRIX-R1.json"
OVERVIEW = ROOT / "docs" / "FUSION-CHART-CAPABILITY-PERFORMANCE-ACCEPTANCE-R1.md"
PERFORMANCE = ROOT / "docs" / "FUSION-CHART-PERFORMANCE-BASELINE-R1.md"
DEFECTS = ROOT / "docs" / "FUSION-CHART-DEFECT-REPORT-R1.md"
README = ROOT / "README.md"

EVIDENCE_SOURCE_SHA = "0b20a9cf6e058f096582e09b72142077399e1ac3"
EVIDENCE_WORKFLOW_RUN_ID = 33867682199
CATEGORIES = {
    "IMPLEMENTATION_DEFECT",
    "EXPECTED_PROFILE_DIFFERENCE",
    "DISPUTED_CANDIDATE",
    "REFERENCE_DIFFERENCE",
    "TEST_ORACLE_DEFECT",
    "UNRESOLVED",
}
REQUIRED_CAPABILITIES = {
    "CAP-TIME-CIVIL-TZDB",
    "CAP-TIME-TRUE-SOLAR",
    "CAP-CALENDAR-LUNAR-LEAP",
    "CAP-SOLAR-TERM-LICHUN",
    "CAP-BAZI-LATE-ZI",
    "CAP-BAZI-NATAL",
    "CAP-BAZI-DAYUN",
    "CAP-ZIWEI-NATAL",
    "CAP-ZIWEI-DAXIAN-XIAOXIAN",
    "CAP-COMBINED-LINEAGE-MANIFEST",
    "CAP-TARGET-FLOW",
    "CAP-FUSION-R2",
    "CAP-DETERMINISTIC-RANDOM-REPLAY",
    "CAP-REFERENCE-DIFFERENTIAL",
    "CAP-SOURCE-PERFORMANCE",
    "CAP-WINDOWS-PACKAGED-PERFORMANCE",
    "CAP-SOAK-RESOURCE-STABILITY",
}


def require_text(path: Path, needle: str) -> None:
    text = path.read_text(encoding="utf-8")
    if needle not in text:
        raise SystemExit(f"{path.relative_to(ROOT)} missing {needle!r}")


def main() -> int:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    if matrix.get("schema") != "FUSION-CHART-CAPABILITY-MATRIX-R1":
        raise SystemExit("capability matrix schema mismatch")
    if matrix.get("acceptance_state") != "ACCEPTED":
        raise SystemExit("capability/performance acceptance is not closed")
    if matrix.get("acceptance_execution_source_sha") != EVIDENCE_SOURCE_SHA:
        raise SystemExit("acceptance evidence source SHA mismatch")
    if matrix.get("acceptance_workflow_run_id") != EVIDENCE_WORKFLOW_RUN_ID:
        raise SystemExit("acceptance workflow run mismatch")
    if not re.fullmatch(r"[0-9a-f]{40}", matrix["acceptance_execution_source_sha"]):
        raise SystemExit("acceptance evidence SHA is malformed")
    if set(matrix.get("failure_taxonomy", ())) != CATEGORIES:
        raise SystemExit("failure taxonomy mismatch")
    if matrix.get("deterministic_product_state") != "CLOSED":
        raise SystemExit("deterministic product closure was reopened")
    if matrix.get("reference_implementation_authority") is not False:
        raise SystemExit("reference implementation was promoted to authority")
    if matrix.get("confirmed_implementation_defect_count") != 0:
        raise SystemExit("confirmed implementation defect count is nonzero")
    if matrix.get("algorithm_reopen_count") != 0:
        raise SystemExit("algorithm reopen count is nonzero")
    if matrix.get("unresolved_defect_count") != 0:
        raise SystemExit("unresolved defect count is nonzero")

    rows = matrix.get("capabilities", ())
    ids = {row.get("capability_id") for row in rows}
    missing = sorted(REQUIRED_CAPABILITIES - ids)
    if missing:
        raise SystemExit("capability matrix missing: " + ", ".join(missing))
    not_accepted = sorted(
        row.get("capability_id", "<missing>")
        for row in rows
        if row.get("capability_id") in REQUIRED_CAPABILITIES
        and row.get("status") != "ACCEPTED"
    )
    if not_accepted:
        raise SystemExit("capabilities not accepted: " + ", ".join(not_accepted))

    summary = matrix.get("acceptance_summary", {})
    expected_summary = {
        "focused_capability": "PASS",
        "source_performance": "PASS",
        "windows_packaged_performance": "PASS",
        "deterministic_replay_10000": "PASS",
        "deterministic_replay_100000": "SKIPPED_PERFORMANCE_BUDGET",
        "soak_resource_stability": "PASS",
        "deterministic_mismatch_count": 0,
        "invariant_failure_count": 0,
        "execution_error_count": 0,
    }
    for key, value in expected_summary.items():
        if summary.get(key) != value:
            raise SystemExit(f"acceptance summary mismatch for {key}")

    for path in (OVERVIEW, README):
        require_text(path, "DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED")
        require_text(path, "ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED")
        require_text(path, "FUSION_CHART_CAPABILITY_PERFORMANCE_ACCEPTANCE_R1=ACCEPTED")
    require_text(DEFECTS, "CONFIRMED_IMPLEMENTATION_DEFECT_COUNT=0")
    require_text(DEFECTS, "TEST_ORACLE_DEFECT_COUNT=3")
    require_text(DEFECTS, "UNRESOLVED_DEFECT_COUNT=0")
    require_text(DEFECTS, "ALGORITHM_REOPEN_COUNT=0")
    require_text(PERFORMANCE, "DETERMINISTIC_REPLAY_10000=PASS")
    require_text(PERFORMANCE, "DETERMINISTIC_REPLAY_100000=SKIPPED_PERFORMANCE_BUDGET")
    require_text(PERFORMANCE, "SOAK_RESOURCE_ACCEPTANCE_R1=PASS")
    require_text(PERFORMANCE, "DETERMINISTIC_REPLAY_MISMATCH_COUNT=0")
    require_text(PERFORMANCE, "DETERMINISTIC_REPLAY_INVARIANT_FAILURE_COUNT=0")
    require_text(PERFORMANCE, "DETERMINISTIC_REPLAY_EXECUTION_ERROR_COUNT=0")

    required_paths = (
        "src/fortune_training/fusion_chart_acceptance/harness.py",
        "src/fortune_training/fusion_chart_acceptance/invariants.py",
        "src/fortune_training/fusion_chart_acceptance/reference_diff.py",
        "src/fortune_training/fusion_chart_acceptance/random_replay.py",
        "src/fortune_training/fusion_chart_acceptance/performance.py",
        "tests/fixtures/fusion-chart-capability-golden-r1.json",
        "tests/test_fusion_chart_capability_acceptance_r1.py",
        "tests/test_fusion_chart_temporal_torture_r1.py",
        "tests/test_fusion_chart_reference_diff_framework_r1.py",
        "tests/test_fusion_chart_acceptance_metrics_r1.py",
        "scripts/fusion-chart-deterministic-replay.py",
        "scripts/fusion-chart-merge-replay.py",
        "scripts/fusion-chart-source-benchmark.py",
        "scripts/fusion-chart-soak.py",
        "scripts/fusion-chart-reference-diff.py",
        ".github/workflows/fusion-chart-capability-performance-r1.yml",
    )
    missing_paths = [path for path in required_paths if not (ROOT / path).is_file()]
    if missing_paths:
        raise SystemExit("acceptance infrastructure missing: " + ", ".join(missing_paths))

    print(json.dumps({
        "schema": "FUSION-CHART-CAPABILITY-PERFORMANCE-R1-MACHINE-GATE",
        "status": "PASS",
        "acceptance_state": "ACCEPTED",
        "acceptance_execution_source_sha": EVIDENCE_SOURCE_SHA,
        "acceptance_workflow_run_id": EVIDENCE_WORKFLOW_RUN_ID,
        "deterministic_product": "CLOSED",
        "reference_implementation_authority": False,
        "confirmed_implementation_defect_count": 0,
        "algorithm_reopen_count": 0,
        "failure_taxonomy": sorted(CATEGORIES),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
