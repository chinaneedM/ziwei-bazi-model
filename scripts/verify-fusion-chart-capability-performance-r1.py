#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "FUSION-CHART-CAPABILITY-MATRIX-R1.json"
OVERVIEW = ROOT / "docs" / "FUSION-CHART-CAPABILITY-PERFORMANCE-ACCEPTANCE-R1.md"
PERFORMANCE = ROOT / "docs" / "FUSION-CHART-PERFORMANCE-BASELINE-R1.md"
DEFECTS = ROOT / "docs" / "FUSION-CHART-DEFECT-REPORT-R1.md"
README = ROOT / "README.md"

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
    if set(matrix.get("failure_taxonomy", ())) != CATEGORIES:
        raise SystemExit("failure taxonomy mismatch")
    if matrix.get("deterministic_product_state") != "CLOSED":
        raise SystemExit("deterministic product closure was reopened")
    if matrix.get("reference_implementation_authority") is not False:
        raise SystemExit("reference implementation was promoted to authority")
    ids = {row.get("capability_id") for row in matrix.get("capabilities", ())}
    missing = sorted(REQUIRED_CAPABILITIES - ids)
    if missing:
        raise SystemExit("capability matrix missing: " + ", ".join(missing))

    for path in (OVERVIEW, README):
        require_text(path, "DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED")
        require_text(path, "ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED")
        require_text(path, "FUSION_CHART_CAPABILITY_PERFORMANCE_ACCEPTANCE_R1=IN_PROGRESS")
    require_text(DEFECTS, "CONFIRMED_IMPLEMENTATION_DEFECT_COUNT=0")
    require_text(DEFECTS, "ALGORITHM_REOPEN_COUNT=0")
    require_text(PERFORMANCE, "DETERMINISTIC_REPLAY_10000=RUNNING")

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
        "scripts/fusion-chart-deterministic-replay.py",
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
        "acceptance_state": "IN_PROGRESS",
        "deterministic_product": "CLOSED",
        "reference_implementation_authority": False,
        "failure_taxonomy": sorted(CATEGORIES),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
