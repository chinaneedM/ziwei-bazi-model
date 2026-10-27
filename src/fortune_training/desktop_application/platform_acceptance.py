from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any, Protocol
from urllib.request import Request, urlopen

from fortune_training.combined_chart_application.local_app import (
    LOCAL_APP_HEALTH_SCHEMA,
    LOCAL_APP_RESOLVE_SCHEMA,
)
from fortune_training.combined_chart_application.product_shell_assets import (
    DESKTOP_PRODUCT_SHELL_SCHEMA,
)
from fortune_training.fusion_chart_acceptance.performance import benchmark_runtime

from .distribution import (
    DESKTOP_APPLICATION_ID,
    DESKTOP_APPLICATION_VERSION,
    DESKTOP_BUILD_METADATA_SCHEMA,
)


WINDOWS_BINARY_SMOKE_SCHEMA = "FORTUNE-CHART-WINDOWS-BINARY-SMOKE-R1"
WINDOWS_BINARY_READY_SCHEMA = "FORTUNE-CHART-WINDOWS-BINARY-READY-R1"
WINDOWS_BINARY_PERFORMANCE_SCHEMA = "FORTUNE-CHART-WINDOWS-BINARY-PERFORMANCE-R1"


class _DesktopServer(Protocol):
    server_address: tuple[object, ...]

    def serve_forever(self) -> None: ...
    def shutdown(self) -> None: ...
    def server_close(self) -> None: ...


def _require(condition: bool, diagnostic: str) -> None:
    if not condition:
        raise RuntimeError(diagnostic)


def _write_receipt(path: Path, payload: dict[str, object]) -> None:
    destination = Path(path).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _read_build_metadata(runtime_root: Path) -> dict[str, Any]:
    path = runtime_root / "desktop-build-metadata.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("packaged desktop build metadata is unreadable") from exc
    _require(isinstance(payload, dict), "packaged desktop build metadata must be an object")
    _require(payload.get("schema") == DESKTOP_BUILD_METADATA_SCHEMA, "build metadata schema mismatch")
    _require(payload.get("application_id") == DESKTOP_APPLICATION_ID, "application identity mismatch")
    _require(payload.get("application_version") == DESKTOP_APPLICATION_VERSION, "application version mismatch")
    source_commit = payload.get("source_commit")
    _require(
        isinstance(source_commit, str)
        and len(source_commit) == 40
        and all(character in "0123456789abcdef" for character in source_commit),
        "build metadata source commit is invalid",
    )
    return payload


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


def run_windows_binary_ready(
    server: _DesktopServer,
    *,
    runtime_root: Path,
) -> dict[str, object]:
    metadata = _read_build_metadata(runtime_root)
    host, port = server.server_address[:2]
    try:
        _require(host == "127.0.0.1", "binary ready server is not loopback-only")
        _require(isinstance(port, int) and port > 0, "binary ready server has no ephemeral port")
        return {
            "schema": WINDOWS_BINARY_READY_SCHEMA,
            "status": "PASS",
            "application_id": metadata["application_id"],
            "application_version": metadata["application_version"],
            "source_commit": metadata["source_commit"],
            "bind_policy": "LOOPBACK_ONLY",
            "server_ready": True,
        }
    finally:
        server.server_close()


def run_windows_binary_performance(
    *,
    runtime_root: Path,
    iterations: int = 5,
) -> dict[str, object]:
    metadata = _read_build_metadata(runtime_root)
    payload = benchmark_runtime(
        runtime_root,
        iterations=iterations,
        schema=WINDOWS_BINARY_PERFORMANCE_SCHEMA,
    )
    payload.update(
        {
            "application_id": metadata["application_id"],
            "application_version": metadata["application_version"],
            "source_commit": metadata["source_commit"],
            "runtime_kind": "PYINSTALLER_WINDOWS_PORTABLE_EXE",
        }
    )
    return payload


def run_windows_binary_smoke(
    server: _DesktopServer,
    *,
    runtime_root: Path,
) -> dict[str, object]:
    """Exercise the emitted executable's packaged runtime over loopback HTTP."""

    metadata = _read_build_metadata(runtime_root)
    host, port = server.server_address[:2]
    _require(host == "127.0.0.1", "binary smoke server is not loopback-only")
    _require(isinstance(port, int) and port > 0, "binary smoke server has no ephemeral port")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://{host}:{port}"
    try:
        with urlopen(f"{base_url}/health", timeout=30) as response:
            health = json.loads(response.read().decode("utf-8"))
        _require(health.get("schema") == LOCAL_APP_HEALTH_SCHEMA, "binary health schema mismatch")
        _require(health.get("status") == "ok", "binary health status mismatch")
        _require(health.get("bind_policy") == "LOOPBACK_ONLY", "binary bind policy mismatch")

        with urlopen(f"{base_url}/", timeout=30) as response:
            index_content_type = response.headers.get("Content-Type", "")
            index_text = response.read().decode("utf-8")
        _require(
            index_content_type.split(";", 1)[0].strip().lower() == "text/html",
            "binary product shell index content type mismatch",
        )
        index_marker = (
            f'name="fortune-chart-product-shell" content="{DESKTOP_PRODUCT_SHELL_SCHEMA}"'
        )
        _require(index_marker in index_text, "binary product shell index marker is missing")

        with urlopen(f"{base_url}/product-shell.css", timeout=30) as response:
            product_css_type = response.headers.get("Content-Type", "")
            product_css = response.read().decode("utf-8")
        _require(
            product_css_type.split(";", 1)[0].strip().lower() == "text/css",
            "binary product shell CSS content type mismatch",
        )
        _require(".product-workspace" in product_css, "binary product shell CSS marker is missing")

        with urlopen(f"{base_url}/product-shell.js", timeout=30) as response:
            product_js_type = response.headers.get("Content-Type", "")
            product_js = response.read().decode("utf-8")
        _require(
            product_js_type.split(";", 1)[0].strip().lower() == "application/javascript",
            "binary product shell JavaScript content type mismatch",
        )
        _require(
            "fortune-chart-product-shell" in product_js,
            "binary product shell JavaScript marker is missing",
        )

        body = json.dumps(_base_payload(), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        request = Request(
            f"{base_url}/api/resolve",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=120) as response:
            resolved = json.loads(response.read().decode("utf-8"))
        _require(resolved.get("schema") == LOCAL_APP_RESOLVE_SCHEMA, "binary resolve schema mismatch")
        combined = resolved.get("combined_resolution")
        _require(isinstance(combined, dict), "binary resolve omitted combined resolution")
        _require(combined.get("integrity", {}).get("status") == "PASS", "binary resolve integrity failed")
        manifest_hash = combined.get("manifest_hash")
        _require(isinstance(manifest_hash, str) and len(manifest_hash) == 64, "binary manifest hash is invalid")

        return {
            "schema": WINDOWS_BINARY_SMOKE_SCHEMA,
            "status": "PASS",
            "application_id": metadata["application_id"],
            "application_version": metadata["application_version"],
            "source_commit": metadata["source_commit"],
            "bind_policy": "LOOPBACK_ONLY",
            "health_schema": health["schema"],
            "resolve_schema": resolved["schema"],
            "combined_manifest_hash": manifest_hash,
            "desktop_product_shell_schema": DESKTOP_PRODUCT_SHELL_SCHEMA,
            "desktop_product_shell_asset_count": 3,
        }
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        _require(not thread.is_alive(), "binary smoke server did not stop cleanly")


def write_windows_binary_ready_receipt(
    path: Path,
    *,
    server: _DesktopServer,
    runtime_root: Path,
) -> None:
    _write_receipt(path, run_windows_binary_ready(server, runtime_root=runtime_root))


def write_windows_binary_performance_receipt(
    path: Path,
    *,
    runtime_root: Path,
    iterations: int = 5,
) -> None:
    _write_receipt(
        path,
        run_windows_binary_performance(
            runtime_root=runtime_root,
            iterations=iterations,
        ),
    )


def write_windows_binary_smoke_receipt(
    path: Path,
    *,
    server: _DesktopServer,
    runtime_root: Path,
) -> None:
    _write_receipt(path, run_windows_binary_smoke(server, runtime_root=runtime_root))
