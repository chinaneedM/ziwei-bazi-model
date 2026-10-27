from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlsplit

from fortune_training.bazi_application import BaziApplicationResolutionError
from fortune_training.calendar_foundation.models import json_value

from .flow_fusion_r2 import (
    CombinedTargetFlowFusionR2ResolutionError,
    CombinedTargetFlowFusionR2Service,
)
from .flow_models import CombinedTargetFlowRequest
from .flow_service import CombinedTargetFlowResolutionError
from .local_app import (
    MAX_REQUEST_BYTES,
    LocalCombinedAppRequestError,
)
from .service import CombinedApplicationResolutionError
from .shared_time_service import SharedZiweiSelectorProjectionError


FLOW_FUSION_R2_LOCAL_RESOLVE_SCHEMA = (
    "ZIWEI-BAZI-COMBINED-LOCAL-TARGET-FLOW-FUSION-R2"
)
FLOW_FUSION_R2_ENDPOINT = "/api/resolve-flow-fusion-r2"


class FlowFusionR2LocalMixin:
    """Read-only workbench adapter over the released target-flow fusion R2 contract."""

    def resolve_flow_fusion_r2_payload(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_INVALID_JSON",
                "request body must be a JSON object",
            )

        combined_request, location_selection = self._combined_request_from_payload(payload)
        target_input, target_profile = self._shared_target_input_from_payload(payload)
        request = CombinedTargetFlowRequest(
            combined_request=combined_request,
            target_input=target_input,
            target_coordinate_profile=target_profile,
        )

        try:
            (
                base,
                bazi_flow,
                r1_flow,
                target_resolution,
                ziwei_selector,
                fusion_r2,
            ) = CombinedTargetFlowFusionR2Service(self.flow_service).resolve_with_bundles(
                request
            )
        except CombinedTargetFlowFusionR2ResolutionError as exc:
            raise LocalCombinedAppRequestError(exc.code, exc.detail, status=422) from exc
        except CombinedTargetFlowResolutionError as exc:
            raise LocalCombinedAppRequestError(exc.code, exc.detail, status=422) from exc
        except SharedZiweiSelectorProjectionError as exc:
            raise LocalCombinedAppRequestError(exc.code, exc.detail, status=422) from exc
        except BaziApplicationResolutionError as exc:
            raise LocalCombinedAppRequestError(exc.code, exc.detail, status=422) from exc
        except CombinedApplicationResolutionError as exc:
            raise LocalCombinedAppRequestError(exc.code, exc.detail, status=422) from exc
        except ValueError as exc:
            raise LocalCombinedAppRequestError(
                "LOCAL_APP_FLOW_FUSION_R2_RESOLUTION_FAILED",
                str(exc),
                status=422,
            ) from exc

        return {
            "schema": FLOW_FUSION_R2_LOCAL_RESOLVE_SCHEMA,
            "location_selection": location_selection,
            "combined_resolution": json_value(base),
            "target_coordinate_resolution": json_value(target_resolution),
            "bazi_target_flow_bundle": json_value(bazi_flow),
            "combined_target_flow_resolution_r1": json_value(r1_flow),
            "ziwei_selector_projection": json_value(ziwei_selector),
            "combined_target_flow_fusion_r2": json_value(fusion_r2),
        }


class _FlowFusionR2HandlerMixin:
    application: FlowFusionR2LocalMixin

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path != FLOW_FUSION_R2_ENDPOINT:
            super().do_POST()
            return

        if (
            self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            != "application/json"
        ):
            self._error(
                LocalCombinedAppRequestError(
                    "LOCAL_APP_JSON_REQUIRED",
                    "Content-Type must be application/json",
                    status=415,
                )
            )
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._error(
                LocalCombinedAppRequestError(
                    "LOCAL_APP_INVALID_CONTENT_LENGTH",
                    "invalid Content-Length",
                )
            )
            return

        if length <= 0:
            self._error(
                LocalCombinedAppRequestError(
                    "LOCAL_APP_EMPTY_BODY",
                    "request body is required",
                )
            )
            return
        if length > MAX_REQUEST_BYTES:
            self._error(
                LocalCombinedAppRequestError(
                    "LOCAL_APP_REQUEST_TOO_LARGE",
                    "request body exceeds local limit",
                    status=413,
                )
            )
            return

        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._error(
                LocalCombinedAppRequestError(
                    "LOCAL_APP_INVALID_JSON",
                    "malformed UTF-8 JSON",
                )
            )
            return

        try:
            response = self.application.resolve_flow_fusion_r2_payload(payload)
        except LocalCombinedAppRequestError as exc:
            self._error(exc)
            return

        self._send_json(200, response)
