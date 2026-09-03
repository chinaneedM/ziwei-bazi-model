from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-PARITY-MATRIX-R1.json"
ACCEPTANCE_PATH = ROOT / "docs" / "FUSION-CHART-PRODUCT-R1-FINAL-ACCEPTANCE-20260904.md"
CLOSURE_PATH = ROOT / "docs" / "FUSION-CHART-FIELD-CLOSURE-AUDIT-R1.md"
README_PATH = ROOT / "README.md"
CI_PATH = ROOT / ".github" / "workflows" / "ci.yml"
WINDOWS_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "windows-portable.yml"

CLOSED_MARKER = "DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED"
WINDOWS_PENDING_MARKER = "WINDOWS_BINARY_PLATFORM_ACCEPTANCE=PENDING_PLATFORM_ACCEPTANCE"
SELF_DIRECTION_MARKER = "ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED"
NO_WINNER_MARKER = "DISPUTED_CANDIDATE_POLICY=NO_WINNER"


def require_text(path: Path, needle: str) -> str:
    text = path.read_text(encoding="utf-8")
    if needle not in text:
        raise SystemExit(f"{path.relative_to(ROOT)}: missing required marker {needle!r}")
    return text


def main() -> int:
    payload = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    fields = payload.get("fields")
    if not isinstance(fields, list):
        raise SystemExit("field parity matrix fields must be a list")

    rows = {
        row.get("field_id"): row
        for row in fields
        if isinstance(row, dict) and isinstance(row.get("field_id"), str)
    }
    if len(rows) != len(fields):
        raise SystemExit("field parity matrix contains invalid or duplicate field_id rows")

    released_hidden = [
        field_id
        for field_id, row in rows.items()
        if row.get("status") == "ALREADY_RELEASED_NOT_YET_VISIBLE"
    ]
    if released_hidden:
        raise SystemExit(
            "released deterministic fields remain hidden: " + ", ".join(sorted(released_hidden))
        )

    self_direction = rows.get("ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION")
    if self_direction is None or self_direction.get("status") != "NOT_YET_FORMALIZED":
        raise SystemExit("Ziwei self/inward transformation direction boundary was changed")

    disputed = [
        field_id
        for field_id, row in rows.items()
        if row.get("status") == "DISPUTED_CANDIDATE_ONLY"
    ]
    if not disputed:
        raise SystemExit("expected disputed candidate rows are missing from the field matrix")

    for path in (ACCEPTANCE_PATH, CLOSURE_PATH, README_PATH):
        require_text(path, CLOSED_MARKER)
        require_text(path, WINDOWS_PENDING_MARKER)
        require_text(path, SELF_DIRECTION_MARKER)
    require_text(ACCEPTANCE_PATH, NO_WINNER_MARKER)
    require_text(CLOSURE_PATH, NO_WINNER_MARKER)

    required_paths = (
        "scripts/build-windows-portable.ps1",
        "scripts/fortune_chart_desktop.py",
        "scripts/fortune_chart_updater.py",
        "src/fortune_training/desktop_application/distribution.py",
        "src/fortune_training/desktop_application/launcher.py",
        "src/fortune_training/desktop_application/updates.py",
        "src/fortune_training/desktop_application/updater.py",
        "tests/test_windows_portable_desktop_launcher_r1.py",
        "tests/test_windows_verified_auto_update_r1.py",
        "tests/test_windows_stable_release_promotion_branch_r1.py",
        "tests/test_windows_stable_release_promotion_push_control_r3.py",
        "tests/test_windows_stable_release_promotion_pr_control_r4.py",
        "tests/test_combined_workbench_real_machine_calibration_r1.py",
        "tests/test_real_machine_calibration_regression_closure_r1.py",
        "docs/COMBINED-WORKBENCH-REAL-MACHINE-CALIBRATION-R1.md",
        ".github/workflows/windows-portable.yml",
    )
    missing = [relative for relative in required_paths if not (ROOT / relative).is_file()]
    if missing:
        raise SystemExit("R1 product closure evidence is missing: " + ", ".join(missing))

    ci = require_text(CI_PATH, "python scripts/verify-fusion-chart-product-r1.py")
    for step in (
        "Fusion Chart Product R1 machine gate",
        "Focused desktop acceptance tests",
        "Verify",
        "Full unittest",
        "Workbench smoke",
        "Workbench HTTP smoke",
    ):
        if step not in ci:
            raise SystemExit(f"ci.yml: missing required R1 gate step {step!r}")

    windows_workflow = require_text(
        WINDOWS_WORKFLOW_PATH,
        "python scripts/verify-fusion-chart-product-r1.py",
    )
    for contract in (
        "runs-on: windows-latest",
        "./scripts/build-windows-portable.ps1 -SourceCommit",
        "FortuneChart-windows-x64.zip",
        "fortune-chart-update.json",
    ):
        if contract not in windows_workflow:
            raise SystemExit(f"windows-portable.yml: missing release contract {contract!r}")

    receipt = {
        "schema": "FUSION-CHART-PRODUCT-R1-MACHINE-GATE",
        "status": "PASS",
        "deterministic_product": "CLOSED",
        "windows_binary_platform_acceptance": "PENDING_PLATFORM_ACCEPTANCE",
        "released_not_yet_visible_count": len(released_hidden),
        "disputed_candidate_count": len(disputed),
        "self_inward_transformation_direction": "NOT_YET_FORMALIZED",
        "disputed_candidate_policy": "NO_WINNER",
    }
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
