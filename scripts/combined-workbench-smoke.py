#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from fortune_training.combined_chart_application.flow_fusion_local_app import (
    FLOW_FUSION_R2_LOCAL_RESOLVE_SCHEMA,
)
from fortune_training.combined_chart_application.flow_local_app import (
    FLOW_LOCAL_APP_RESOLVE_SCHEMA,
)
from fortune_training.combined_chart_application.interaction_local_app import (
    LOCAL_ZIWEI_INTERACTION_SCHEMA,
)
from fortune_training.combined_chart_application.local_app import (
    LOCAL_APP_HEALTH_SCHEMA,
    LOCAL_APP_RESOLVE_SCHEMA,
)
from fortune_training.combined_chart_application.shared_apply_local_app import (
    LOCAL_SHARED_ZIWEI_PROJECTION_SCHEMA,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    CombinedChartWorkbenchApplication,
)


RECEIPT_SCHEMA = "COMBINED-WORKBENCH-SMOKE-RECEIPT-R2"


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _base_payload() -> dict[str, object]:
    return {
        "birth_datetime": "1994-05-17T14:30:00",
        "birth_place": "Beijing",
        "latitude": 39.9042,
        "longitude": 116.4074,
        "timezone_id": "Asia/Shanghai",
        "sex": "MALE",
        "precision": "EXACT_SECOND",
        "uncertainty_seconds": 0,
        "ziwei_daxian_count": 12,
        "ziwei_daxian_frame_id": None,
        "ziwei_annual_year": 2025,
        "ziwei_minor_limit_age": None,
        "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
        "bazi_dayun_count": 12,
        "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
    }


def _target_payload() -> dict[str, object]:
    return {
        **_base_payload(),
        "target_datetime": "2026-06-01T12:00:00",
        "target_place": "Greenwich",
        "target_latitude": 51.4769,
        "target_longitude": 0.0,
        "target_timezone_id": "Etc/UTC",
        "target_precision": "EXACT_SECOND",
        "target_uncertainty_seconds": 0,
        "target_temporal_profile_id": (
            "BAZI-TARGET-TEMPORAL-COORDINATE-FOUNDATION-R1"
        ),
    }


def _require(condition: bool, diagnostic: str) -> None:
    if not condition:
        raise RuntimeError(diagnostic)


def run_smoke(repository_root: Path) -> dict[str, Any]:
    """Exercise released combined-workbench application boundaries without writes."""

    app = CombinedChartWorkbenchApplication(repository_root)

    health = app.health()
    _require(health.get("schema") == LOCAL_APP_HEALTH_SCHEMA, "health schema mismatch")
    _require(health.get("status") == "ok", "health status is not ok")
    _require(
        health.get("bind_policy") == "LOOPBACK_ONLY",
        "health bind policy is not loopback-only",
    )
    _require(
        health.get("location_lookup_network_access") is False,
        "location lookup unexpectedly requires network access",
    )

    base_payload = _base_payload()
    base = app.resolve_payload(base_payload)
    _require(
        base.get("schema") == LOCAL_APP_RESOLVE_SCHEMA,
        "base resolve schema mismatch",
    )
    combined = base["combined_resolution"]
    _require(
        combined["integrity"]["status"] == "PASS",
        "base combined integrity did not PASS",
    )
    _require(
        combined["ziwei_bundle"] is not None,
        "base combined resolution has no Ziwei bundle",
    )
    _require(
        combined["bazi_bundle"] is not None,
        "base combined resolution has no Bazi bundle",
    )
    _require(base.get("ziwei_svg"), "base combined resolution produced no Ziwei SVG")

    ziwei_temporal_state = combined["ziwei_bundle"]["temporal_state"]
    daxian_rows = ziwei_temporal_state["daxian_frames"]
    _require(
        isinstance(daxian_rows, list) and len(daxian_rows) == base_payload["ziwei_daxian_count"],
        "released Ziwei Daxian sequence count mismatch",
    )
    daxian_frame_ids: set[str] = set()
    daxian_indexes: set[int] = set()
    for row in daxian_rows:
        _require(isinstance(row.get("frame_id"), str) and bool(row["frame_id"]), "Daxian frame_id missing")
        _require(isinstance(row.get("index"), int), "Daxian index missing")
        _require(isinstance(row.get("nominal_age_start"), int), "Daxian nominal_age_start missing")
        _require(isinstance(row.get("nominal_age_end"), int), "Daxian nominal_age_end missing")
        _require(isinstance(row.get("absolute_year_start"), int), "Daxian absolute_year_start missing")
        _require(isinstance(row.get("absolute_year_end"), int), "Daxian absolute_year_end missing")
        _require(
            isinstance(row.get("active_address"), dict)
            and isinstance(row["active_address"].get("index"), int)
            and isinstance(row["active_address"].get("branch"), str)
            and bool(row["active_address"]["branch"]),
            "Daxian active_address identity missing",
        )
        _require(
            isinstance(row.get("active_palace_ganzhi"), str) and bool(row["active_palace_ganzhi"]),
            "Daxian active_palace_ganzhi missing",
        )
        _require(row["nominal_age_start"] <= row["nominal_age_end"], "Daxian nominal age range is invalid")
        _require(row["absolute_year_start"] <= row["absolute_year_end"], "Daxian absolute year range is invalid")
        _require(row["frame_id"] not in daxian_frame_ids, "released Daxian frame_id is duplicated")
        _require(row["index"] not in daxian_indexes, "released Daxian index is duplicated")
        daxian_frame_ids.add(row["frame_id"])
        daxian_indexes.add(row["index"])

    zi_year_doujun_rows = [
        row
        for row in ziwei_temporal_state["annual_frames"]
        if row["year_branch"] == "子"
    ]
    _require(zi_year_doujun_rows, "base Ziwei bundle produced no 子-year AnnualFrame")
    zi_year_doujun_identities = {
        (row["doujun_address"]["index"], row["doujun_address"]["branch"])
        for row in zi_year_doujun_rows
    }
    _require(
        len(zi_year_doujun_identities) == 1,
        "released 子-year Doujun address identity is inconsistent",
    )
    zi_year_doujun_branch = next(iter(zi_year_doujun_identities))[1]
    _require(
        zi_year_doujun_branch == "辰",
        "1994 Beijing compatibility fixture 子年斗君 is not 辰",
    )

    manifest_hash = combined["manifest_hash"]
    ziwei_bundle_hash = combined["ziwei_bundle"]["bundle_hash"]
    bazi_bundle_hash = combined["bazi_bundle"]["bundle_hash"]

    interaction_payload = {
        **base_payload,
        "ziwei_origin_designation_id": "LIFE",
    }
    interaction = app.resolve_ziwei_interaction_payload(interaction_payload)
    _require(
        interaction.get("schema") == LOCAL_ZIWEI_INTERACTION_SCHEMA,
        "Ziwei interaction schema mismatch",
    )
    _require(
        interaction["source_combined_manifest_hash"] == manifest_hash,
        "Ziwei interaction manifest binding mismatch",
    )
    _require(
        interaction["source_ziwei_bundle_hash"] == ziwei_bundle_hash,
        "Ziwei interaction bundle binding mismatch",
    )
    _require(
        interaction["interaction"]["integrity"]["status"] == "PASS",
        "Ziwei interaction integrity did not PASS",
    )
    _require(
        len(interaction["interaction"]["relative_roles"]) == 12,
        "Ziwei interaction did not expose 12 relative roles",
    )
    _require(
        len(interaction["interaction"]["sanfang_sizheng_frame"]["members"]) == 4,
        "Ziwei interaction did not expose four Sanfang/Sizheng members",
    )

    target_payload = _target_payload()
    flow = app.resolve_flow_payload(target_payload)
    _require(
        flow.get("schema") == FLOW_LOCAL_APP_RESOLVE_SCHEMA,
        "Bazi target-flow local schema mismatch",
    )
    combined_flow = flow["combined_target_flow_resolution"]
    _require(
        combined_flow["integrity"]["status"] == "PASS",
        "combined target-flow integrity did not PASS",
    )
    _require(
        combined_flow["base_combined_manifest_hash"] == manifest_hash,
        "target-flow base manifest binding mismatch",
    )
    _require(
        combined_flow["ziwei_bundle_hash"] == ziwei_bundle_hash,
        "target-flow Ziwei bundle binding mismatch",
    )
    _require(
        combined_flow["bazi_base_bundle_hash"] == bazi_bundle_hash,
        "target-flow Bazi base bundle binding mismatch",
    )
    _require(
        flow["bazi_target_flow_bundle"]["integrity"]["status"] == "PASS",
        "Bazi target-flow bundle integrity did not PASS",
    )
    _require(
        len(flow["bazi_target_flow_bundle"]["candidates"]) >= 1,
        "Bazi target-flow produced no candidates",
    )

    projection = app.resolve_shared_ziwei_projection_payload(target_payload)
    _require(
        projection.get("schema") == LOCAL_SHARED_ZIWEI_PROJECTION_SCHEMA,
        "shared projection local schema mismatch",
    )
    _require(
        projection["source_combined_manifest_hash"] == manifest_hash,
        "shared projection manifest binding mismatch",
    )
    _require(
        projection["source_ziwei_bundle_hash"] == ziwei_bundle_hash,
        "shared projection Ziwei bundle binding mismatch",
    )
    _require(
        projection["projection"]["integrity"]["status"] == "PASS",
        "shared projection integrity did not PASS",
    )
    _require(
        len(projection["projection"]["candidates"]) >= 1,
        "shared projection produced no candidates",
    )
    _require(
        projection["target_coordinate_fact_hash"]
        == combined_flow["target_coordinate_fact_hash"],
        "shared projection and Bazi flow disagree on target-coordinate FactHash",
    )
    _require(
        projection["target_coordinate_computation_hash"]
        == combined_flow["target_coordinate_computation_hash"],
        "shared projection and Bazi flow disagree on target-coordinate ComputationHash",
    )

    fusion = app.resolve_flow_fusion_r2_payload(target_payload)
    _require(
        fusion.get("schema") == FLOW_FUSION_R2_LOCAL_RESOLVE_SCHEMA,
        "fusion R2 local schema mismatch",
    )
    fusion_r2 = fusion["combined_target_flow_fusion_r2"]
    _require(
        fusion_r2["integrity"]["status"] == "PASS",
        "combined target-flow fusion R2 integrity did not PASS",
    )
    _require(
        fusion_r2["base_combined_manifest_hash"] == manifest_hash,
        "fusion R2 base manifest binding mismatch",
    )
    _require(
        fusion_r2["r1_target_flow_bundle_hash"] == combined_flow["bundle_hash"],
        "fusion R2 did not bind the released R1 target-flow bundle",
    )
    _require(
        fusion_r2["target_coordinate_fact_hash"]
        == combined_flow["target_coordinate_fact_hash"]
        == projection["target_coordinate_fact_hash"],
        "fusion R2 target-coordinate FactHash diverged across sidecars",
    )
    _require(
        fusion_r2["target_coordinate_computation_hash"]
        == combined_flow["target_coordinate_computation_hash"]
        == projection["target_coordinate_computation_hash"],
        "fusion R2 target-coordinate ComputationHash diverged across sidecars",
    )
    _require(
        fusion_r2["bazi_target_flow_bundle_hash"]
        == flow["bazi_target_flow_bundle"]["bundle_hash"],
        "fusion R2 Bazi target-flow binding mismatch",
    )
    _require(
        fusion_r2["ziwei_selector_fact_hash"]
        == projection["projection"]["hashes"]["fact_hash"],
        "fusion R2 Ziwei selector FactHash mismatch",
    )
    _require(
        fusion_r2["ziwei_selector_computation_hash"]
        == projection["projection"]["hashes"]["computation_hash"],
        "fusion R2 Ziwei selector ComputationHash mismatch",
    )
    _require(
        fusion["target_coordinate_resolution"]["integrity"]["status"] == "PASS",
        "fusion R2 target-coordinate integrity did not PASS",
    )
    _require(
        fusion["ziwei_selector_projection"]["integrity"]["status"] == "PASS",
        "fusion R2 Ziwei selector integrity did not PASS",
    )
    _require(
        fusion["bazi_target_flow_bundle"]["integrity"]["status"] == "PASS",
        "fusion R2 Bazi target-flow integrity did not PASS",
    )

    return {
        "schema": RECEIPT_SCHEMA,
        "status": "PASS",
        "health_schema": health["schema"],
        "bind_policy": health["bind_policy"],
        "combined_manifest_hash": manifest_hash,
        "ziwei_bundle_hash": ziwei_bundle_hash,
        "bazi_bundle_hash": bazi_bundle_hash,
        "ziwei_daxian_sequence_count": len(daxian_rows),
        "zi_year_doujun_branch": zi_year_doujun_branch,
        "ziwei_interaction_bundle_hash": interaction["interaction"]["bundle_hash"],
        "bazi_target_flow_bundle_hash": combined_flow["bazi_target_flow_bundle_hash"],
        "target_coordinate_fact_hash": combined_flow["target_coordinate_fact_hash"],
        "shared_projection_fact_hash": projection["projection"]["hashes"]["fact_hash"],
        "fusion_r2_bundle_hash": fusion_r2["bundle_hash"],
        "bazi_target_flow_candidate_count": len(
            flow["bazi_target_flow_bundle"]["candidates"]
        ),
        "shared_projection_candidate_count": len(
            projection["projection"]["candidates"]
        ),
        "fusion_r2_ziwei_selector_candidate_count": fusion_r2[
            "ziwei_selector_candidate_count"
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run a deterministic, read-only smoke check of the released "
            "combined chart workbench"
        )
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=_repository_root(),
        help="repository root containing config/time-calendar-policies.json",
    )
    args = parser.parse_args(argv)

    try:
        receipt = run_smoke(args.repository_root.resolve())
    except Exception as exc:  # deliberate command-level fail-closed boundary
        print(
            json.dumps(
                {
                    "schema": RECEIPT_SCHEMA,
                    "status": "FAIL",
                    "diagnostic": f"{type(exc).__name__}: {exc}",
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1

    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
