#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import threading
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from fortune_training.combined_chart_application.bazi_branch_relation_local_app import (
    BAZI_BRANCH_RELATION_PRESENTATION_SCHEMA,
)
from fortune_training.combined_chart_application.bazi_hidden_exposure_local_app import (
    BAZI_HIDDEN_EXPOSURE_PRESENTATION_SCHEMA,
)
from fortune_training.combined_chart_application.bazi_stem_relation_local_app import (
    BAZI_STEM_RELATION_PRESENTATION_SCHEMA,
)
from fortune_training.combined_chart_application.local_app import (
    LOCAL_APP_HEALTH_SCHEMA,
    LOCAL_APP_RESOLVE_SCHEMA,
)
from fortune_training.combined_chart_application.nayin_local_app import (
    NAYIN_PRESENTATION_SCHEMA,
)
from fortune_training.combined_chart_application.palace_stem_topology_local_app import (
    LOCAL_ZIWEI_PALACE_STEM_TOPOLOGY_SCHEMA,
    LOCAL_ZIWEI_STAR_PROVENANCE_SCHEMA,
)
from fortune_training.combined_chart_application.product_shell_assets import (
    DESKTOP_PRODUCT_SHELL_SCHEMA,
)
from fortune_training.combined_chart_application.workbench_local_app import (
    build_workbench_server,
)
from fortune_training.combined_chart_application.ziwei_dignity_provenance_local_app import (
    LOCAL_ZIWEI_DIGNITY_PROVENANCE_SCHEMA,
)


RECEIPT_SCHEMA = "COMBINED-WORKBENCH-HTTP-SMOKE-RECEIPT-R1"


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


def _require(condition: bool, diagnostic: str) -> None:
    if not condition:
        raise RuntimeError(diagnostic)


def _require_sha256(value: object, diagnostic: str) -> None:
    _require(
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value.lower()),
        diagnostic,
    )


def _get(base_url: str, path: str) -> tuple[bytes, str]:
    with urlopen(f"{base_url}{path}", timeout=30) as response:
        body = response.read()
        content_type = response.headers.get("Content-Type", "")
        _require(response.status == 200, f"GET {path} returned HTTP {response.status}")
        _require(bool(body), f"GET {path} returned an empty body")
        return body, content_type


def _get_json(base_url: str, path: str) -> dict[str, Any]:
    body, content_type = _get(base_url, path)
    _require(
        content_type.split(";", 1)[0].strip().lower() == "application/json",
        f"GET {path} did not return application/json",
    )
    payload = json.loads(body.decode("utf-8"))
    _require(isinstance(payload, dict), f"GET {path} did not return a JSON object")
    return payload


def _post_json(base_url: str, path: str, payload: dict[str, object]) -> dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    request = Request(
        f"{base_url}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=90) as response:
        response_body = response.read()
        content_type = response.headers.get("Content-Type", "")
        _require(response.status == 200, f"POST {path} returned HTTP {response.status}")
        _require(
            content_type.split(";", 1)[0].strip().lower() == "application/json",
            f"POST {path} did not return application/json",
        )
        result = json.loads(response_body.decode("utf-8"))
        _require(isinstance(result, dict), f"POST {path} did not return a JSON object")
        return result


def _require_profile_identity(profile: object, label: str) -> dict[str, Any]:
    _require(isinstance(profile, dict), f"{label} resolved profile is missing")
    assert isinstance(profile, dict)
    _require(
        isinstance(profile.get("profile_id"), str) and bool(profile["profile_id"]),
        f"{label} resolved profile_id is missing",
    )
    _require(
        isinstance(profile.get("profile_version"), str) and bool(profile["profile_version"]),
        f"{label} resolved profile_version is missing",
    )
    return profile


def _require_source_binding(
    result: dict[str, Any],
    *,
    schema: str,
    manifest_hash: str,
    bundle_key: str,
    bundle_hash: str,
    label: str,
) -> None:
    _require(result.get("schema") == schema, f"{label} schema mismatch")
    _require(
        result.get("source_combined_manifest_hash") == manifest_hash,
        f"{label} manifest binding mismatch",
    )
    _require(result.get(bundle_key) == bundle_hash, f"{label} bundle binding mismatch")


def run_http_smoke(repository_root: Path) -> dict[str, Any]:
    """Exercise released Workbench resources and sidecars through loopback HTTP."""

    server = build_workbench_server(repository_root, port=0)
    host, port = server.server_address[:2]
    _require(host == "127.0.0.1", "workbench server is not bound to loopback")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://{host}:{port}"

    try:
        health = _get_json(base_url, "/health")
        _require(health.get("schema") == LOCAL_APP_HEALTH_SCHEMA, "HTTP health schema mismatch")
        _require(health.get("status") == "ok", "HTTP health status is not ok")
        _require(health.get("bind_policy") == "LOOPBACK_ONLY", "HTTP health bind policy mismatch")

        index_body, index_content_type = _get(base_url, "/")
        _require(
            index_content_type.split(";", 1)[0].strip().lower() == "text/html",
            "Workbench index did not return text/html",
        )
        index_text = index_body.decode("utf-8")
        for marker in (
            f'name="fortune-chart-product-shell" content="{DESKTOP_PRODUCT_SHELL_SCHEMA}"',
            "resolved-profile-lineage-panel",
            "ziwei-dignity-provenance",
            "ziwei-palace-stem-topology",
            "bazi-hidden-exposure",
            "bazi-stem-relations",
            "bazi-branch-relations",
            "nayin",
        ):
            _require(marker in index_text, f"Workbench index is missing {marker}")

        asset_paths = (
            "/product-shell.css",
            "/product-shell.js",
            "/resolved-profile-lineage.css",
            "/resolved-profile-lineage.js",
            "/ziwei-dignity-provenance.css",
            "/ziwei-dignity-provenance.js",
            "/ziwei-palace-stem-topology.css",
            "/ziwei-palace-stem-topology.js",
            "/ziwei-basic-info.css",
            "/ziwei-basic-info.js",
            "/bazi-hidden-exposure.css",
            "/bazi-hidden-exposure.js",
            "/bazi-stem-relations.css",
            "/bazi-stem-relations.js",
            "/bazi-branch-relations.css",
            "/bazi-branch-relations.js",
            "/bazi-pillar-metadata.css",
            "/bazi-pillar-metadata.js",
            "/nayin.css",
            "/nayin.js",
        )
        for path in asset_paths:
            _get(base_url, path)

        product_css, product_css_type = _get(base_url, "/product-shell.css")
        _require(
            product_css_type.split(";", 1)[0].strip().lower() == "text/css",
            "Product shell CSS content type mismatch",
        )
        _require(b".product-workspace" in product_css, "Product shell CSS marker is missing")
        product_js, product_js_type = _get(base_url, "/product-shell.js")
        _require(
            product_js_type.split(";", 1)[0].strip().lower() == "application/javascript",
            "Product shell JavaScript content type mismatch",
        )
        _require(
            b"fortune-chart-product-shell" in product_js,
            "Product shell JavaScript marker is missing",
        )

        base_payload = _base_payload()
        base = _post_json(base_url, "/api/resolve", base_payload)
        _require(base.get("schema") == LOCAL_APP_RESOLVE_SCHEMA, "HTTP resolve schema mismatch")
        combined = base.get("combined_resolution")
        _require(isinstance(combined, dict), "HTTP resolve has no combined_resolution")
        assert isinstance(combined, dict)
        _require(
            combined.get("integrity", {}).get("status") == "PASS",
            "HTTP combined integrity did not PASS",
        )
        manifest_hash = combined.get("manifest_hash")
        _require_sha256(manifest_hash, "HTTP combined manifest hash is invalid")
        assert isinstance(manifest_hash, str)
        ziwei_bundle = combined.get("ziwei_bundle")
        bazi_bundle = combined.get("bazi_bundle")
        _require(isinstance(ziwei_bundle, dict), "HTTP resolve has no Ziwei bundle")
        _require(isinstance(bazi_bundle, dict), "HTTP resolve has no Bazi bundle")
        assert isinstance(ziwei_bundle, dict)
        assert isinstance(bazi_bundle, dict)
        ziwei_bundle_hash = ziwei_bundle.get("bundle_hash")
        bazi_bundle_hash = bazi_bundle.get("bundle_hash")
        _require_sha256(ziwei_bundle_hash, "HTTP Ziwei bundle hash is invalid")
        _require_sha256(bazi_bundle_hash, "HTTP Bazi bundle hash is invalid")
        assert isinstance(ziwei_bundle_hash, str)
        assert isinstance(bazi_bundle_hash, str)

        combined_profile = _require_profile_identity(combined.get("combined_profile"), "combined")
        ziwei_profile = _require_profile_identity(
            combined.get("ziwei_calculation_profile"), "Ziwei calculation"
        )
        _require_profile_identity(combined.get("ziwei_application_profile"), "Ziwei application")
        _require_profile_identity(combined.get("ziwei_presentation_profile"), "Ziwei presentation")
        bazi_natal_profile = _require_profile_identity(combined.get("bazi_natal_profile"), "Bazi natal")
        bazi_temporal_profile = _require_profile_identity(
            combined.get("bazi_temporal_profile"), "Bazi temporal"
        )
        _require_profile_identity(combined.get("bazi_application_profile"), "Bazi application")
        for profile, id_key, version_key, label in (
            (combined_profile, "algorithm_id", "algorithm_version", "combined algorithm"),
            (ziwei_profile, "natal_structure_algorithm_id", "natal_structure_algorithm_version", "Ziwei natal algorithm"),
            (ziwei_profile, "dignity_rule_set_id", "dignity_rule_set_version", "Ziwei dignity rules"),
            (bazi_natal_profile, "hidden_stem_rule_set_id", "hidden_stem_rule_set_version", "Bazi hidden-stem rules"),
            (bazi_natal_profile, "natal_algorithm_id", "natal_algorithm_version", "Bazi natal algorithm"),
            (bazi_temporal_profile, "direction_rule_set_id", "direction_rule_set_version", "Bazi direction rules"),
            (bazi_temporal_profile, "algorithm_id", "algorithm_version", "Bazi temporal algorithm"),
        ):
            _require(
                isinstance(profile.get(id_key), str)
                and bool(profile[id_key])
                and isinstance(profile.get(version_key), str)
                and bool(profile[version_key]),
                f"{label} lineage is missing",
            )

        ziwei_sidecars = (
            (
                "/api/ziwei-palace-stem-topology",
                LOCAL_ZIWEI_PALACE_STEM_TOPOLOGY_SCHEMA,
                "ziwei_palace_stem_transformation_topology",
                "Ziwei palace-stem topology",
            ),
            (
                "/api/ziwei-star-provenance",
                LOCAL_ZIWEI_STAR_PROVENANCE_SCHEMA,
                "ziwei_star_placement_provenance",
                "Ziwei star provenance",
            ),
            (
                "/api/ziwei-dignity-provenance",
                LOCAL_ZIWEI_DIGNITY_PROVENANCE_SCHEMA,
                "ziwei_dignity_annotation_provenance",
                "Ziwei dignity provenance",
            ),
        )
        for path, schema, payload_key, label in ziwei_sidecars:
            result = _post_json(base_url, path, base_payload)
            _require_source_binding(
                result,
                schema=schema,
                manifest_hash=manifest_hash,
                bundle_key="source_ziwei_bundle_hash",
                bundle_hash=ziwei_bundle_hash,
                label=label,
            )
            payload_value = result.get(payload_key)
            _require(isinstance(payload_value, dict), f"{label} payload is missing")
            _require(
                payload_value.get("source_application_bundle_hash") == ziwei_bundle_hash,
                f"{label} source application bundle binding mismatch",
            )

        bazi_sidecars = (
            (
                "/api/bazi-hidden-exposure-presentation",
                BAZI_HIDDEN_EXPOSURE_PRESENTATION_SCHEMA,
                "Bazi hidden exposure",
            ),
            (
                "/api/bazi-stem-relations-presentation",
                BAZI_STEM_RELATION_PRESENTATION_SCHEMA,
                "Bazi stem relations",
            ),
            (
                "/api/bazi-branch-relations-presentation",
                BAZI_BRANCH_RELATION_PRESENTATION_SCHEMA,
                "Bazi branch relations",
            ),
            (
                "/api/bazi-nayin-presentation",
                NAYIN_PRESENTATION_SCHEMA,
                "Bazi Nayin",
            ),
        )
        for path, schema, label in bazi_sidecars:
            result = _post_json(base_url, path, base_payload)
            _require_source_binding(
                result,
                schema=schema,
                manifest_hash=manifest_hash,
                bundle_key="source_bazi_bundle_hash",
                bundle_hash=bazi_bundle_hash,
                label=label,
            )
            candidates = result.get("candidates")
            _require(isinstance(candidates, list) and bool(candidates), f"{label} candidates are missing")
            for candidate in candidates:
                _require(isinstance(candidate, dict), f"{label} candidate is not an object")
                _require_sha256(
                    candidate.get("source_natal_fact_hash"),
                    f"{label} source natal fact hash is invalid",
                )
                _require_sha256(
                    candidate.get("source_natal_computation_hash"),
                    f"{label} source natal computation hash is invalid",
                )

        return {
            "schema": RECEIPT_SCHEMA,
            "status": "PASS",
            "source_combined_manifest_hash": manifest_hash,
            "source_ziwei_bundle_hash": ziwei_bundle_hash,
            "source_bazi_bundle_hash": bazi_bundle_hash,
            "http_asset_count": len(asset_paths) + 1,
            "http_sidecar_count": len(ziwei_sidecars) + len(bazi_sidecars),
            "desktop_product_shell_schema": DESKTOP_PRODUCT_SHELL_SCHEMA,
            "desktop_product_shell_asset_count": 3,
        }
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        _require(not thread.is_alive(), "workbench HTTP server did not stop cleanly")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Smoke released combined Workbench surfaces through loopback HTTP"
    )
    parser.add_argument("--repository-root", type=Path, default=_repository_root())
    args = parser.parse_args(argv)
    receipt = run_http_smoke(args.repository_root.resolve())
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
