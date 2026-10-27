from __future__ import annotations

import copy
import json
import threading
import unittest
import urllib.request
from pathlib import Path

import jsonschema

from fortune_training.combined_chart_application.interaction_assets import (
    INTERACTION_JS,
    interaction_index_html,
)
from fortune_training.combined_chart_application.interaction_local_app import (
    LOCAL_ZIWEI_INTERACTION_SCHEMA,
    InteractionLocalCombinedChartApplication,
    build_interaction_server,
)
from fortune_training.combined_chart_application.local_app import (
    INDEX_HTML,
    LocalCombinedAppRequestError,
)


ROOT = Path(__file__).resolve().parents[1]


class CombinedBrowserZiweiSanheInteractionSidecarR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = InteractionLocalCombinedChartApplication(ROOT)
        cls.wrapper_schema = json.loads(
            (
                ROOT
                / "schemas"
                / "combined-local-ziwei-sanhe-interaction-response-r1.schema.json"
            ).read_text(encoding="utf-8")
        )
        cls.controller_schema = json.loads(
            (
                ROOT / "schemas" / "ziwei-sanhe-interaction-controller-r1.schema.json"
            ).read_text(encoding="utf-8")
        )

    @staticmethod
    def base_payload(*, annual_year: int | None = 2001) -> dict[str, object]:
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
            "ziwei_daxian_frame_id": "DAXIAN:index=1",
            "ziwei_annual_year": annual_year,
            "ziwei_minor_limit_age": 8,
            "bazi_natal_profile_id": "BAZI-FOUNDATION-V1-R1",
            "bazi_temporal_profile_id": "BAZI-TEMPORAL-V1-CONTINUOUS-R1",
            "bazi_dayun_count": 12,
            "combined_profile_id": "ZIWEI-BAZI-COMBINED-LOCAL-SHELL-V1-R1",
        }

    @classmethod
    def interaction_payload(
        cls,
        origin: str = "LIFE",
        *,
        annual_year: int | None = 2001,
    ) -> dict[str, object]:
        return {
            **cls.base_payload(annual_year=annual_year),
            "ziwei_origin_designation_id": origin,
        }

    def test_sidecar_binds_exact_combined_ziwei_bundle_and_schemas(self) -> None:
        base = self.app.resolve_payload(self.base_payload())
        sidecar = self.app.resolve_ziwei_interaction_payload(
            self.interaction_payload()
        )

        self.assertEqual(LOCAL_ZIWEI_INTERACTION_SCHEMA, sidecar["schema"])
        jsonschema.Draft202012Validator(self.wrapper_schema).validate(sidecar)
        jsonschema.Draft202012Validator(self.controller_schema).validate(
            sidecar["interaction"]
        )

        combined = base["combined_resolution"]
        self.assertEqual(
            combined["manifest_hash"],
            sidecar["source_combined_manifest_hash"],
        )
        self.assertEqual(
            combined["ziwei_bundle"]["bundle_hash"],
            sidecar["source_ziwei_bundle_hash"],
        )
        self.assertEqual(
            combined["bazi_bundle"]["bundle_hash"],
            sidecar["source_bazi_bundle_hash"],
        )
        self.assertEqual(
            sidecar["source_ziwei_bundle_hash"],
            sidecar["interaction"]["source_application_bundle_hash"],
        )
        self.assertEqual("LIFE", sidecar["interaction"]["selected_origin_designation_id"])
        self.assertEqual("PASS", sidecar["interaction"]["integrity"]["status"])
        self.assertIn('<svg xmlns="http://www.w3.org/2000/svg"', sidecar["ziwei_svg"])
        self.assertIn('data-address-index="0"', sidecar["ziwei_svg"])

        injected = copy.deepcopy(sidecar)
        injected["prediction"] = "FORBIDDEN"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.wrapper_schema).validate(injected)

        nested = copy.deepcopy(sidecar["interaction"])
        nested["prediction"] = "FORBIDDEN"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(self.controller_schema).validate(nested)

    def test_all_twelve_origins_are_typed_and_resolve_exact_r5_members(self) -> None:
        first = self.app.resolve_ziwei_interaction_payload(self.interaction_payload())
        options = first["origin_options"]
        self.assertEqual(12, len(options))
        self.assertEqual(set(range(12)), {row["address_index"] for row in options})
        self.assertEqual(12, len({row["designation_id"] for row in options}))

        for option in options:
            with self.subTest(origin=option["designation_id"]):
                response = self.app.resolve_ziwei_interaction_payload(
                    self.interaction_payload(option["designation_id"])
                )
                interaction = response["interaction"]
                self.assertEqual(
                    option["designation_id"],
                    interaction["selected_origin_designation_id"],
                )
                self.assertEqual(
                    option["address_index"],
                    interaction["selected_origin_address"]["index"],
                )
                members = interaction["sanfang_sizheng_frame"]["members"]
                self.assertEqual([0, 4, 6, 8], [row["member_offset"] for row in members])
                self.assertEqual(
                    ["SELF", "TRINE_PLUS_4", "OPPOSITION", "TRINE_PLUS_8"],
                    [row["semantic_role"] for row in members],
                )
                self.assertEqual(
                    4,
                    len({row["target_raw_address"]["index"] for row in members}),
                )
                self.assertEqual(12, len(interaction["relative_roles"]))

    def test_unknown_origin_fails_closed_without_fallback(self) -> None:
        with self.assertRaises(LocalCombinedAppRequestError) as caught:
            self.app.resolve_ziwei_interaction_payload(
                self.interaction_payload("NOT-A-REAL-PALACE")
            )
        self.assertEqual(
            "SANHE_INTERACTION_R2_ORIGIN_NOT_UNIQUE",
            caught.exception.code,
        )
        self.assertEqual(422, caught.exception.status)

    def test_temporal_sidecar_changes_ziwei_identity_without_bazi_identity(self) -> None:
        year_2001 = self.app.resolve_ziwei_interaction_payload(
            self.interaction_payload(annual_year=2001)
        )
        year_2002 = self.app.resolve_ziwei_interaction_payload(
            self.interaction_payload(annual_year=2002)
        )

        self.assertNotEqual(
            year_2001["source_ziwei_bundle_hash"],
            year_2002["source_ziwei_bundle_hash"],
        )
        self.assertEqual(
            year_2001["source_bazi_bundle_hash"],
            year_2002["source_bazi_bundle_hash"],
        )
        self.assertEqual(2001, year_2001["interaction"]["selected_annual_year"])
        self.assertEqual(2002, year_2002["interaction"]["selected_annual_year"])
        self.assertEqual(
            year_2001["interaction"]["relative_roles"],
            year_2002["interaction"]["relative_roles"],
        )
        self.assertEqual(
            year_2001["interaction"]["sanfang_sizheng_frame"],
            year_2002["interaction"]["sanfang_sizheng_frame"],
        )

    def test_temporal_navigator_options_are_exactly_source_temporal_frames(self) -> None:
        response = self.app.resolve_ziwei_interaction_payload(self.interaction_payload())
        options = response["temporal_options"]
        interaction = response["interaction"]

        self.assertEqual(12, len(options["daxian"]))
        self.assertEqual(
            "DAXIAN:index=1",
            interaction["selected_daxian_frame_id"],
        )
        self.assertIn(
            interaction["selected_daxian_frame_id"],
            {row["frame_id"] for row in options["daxian"]},
        )
        self.assertIn(
            interaction["selected_annual_year"],
            {row["absolute_year"] for row in options["annual"]},
        )
        self.assertIn(
            interaction["selected_minor_limit_age"],
            {row["nominal_age"] for row in options["minor_limit"]},
        )

    def test_legacy_resolve_contract_remains_exactly_without_interaction_fields(self) -> None:
        response = self.app.resolve_payload(self.base_payload())
        self.assertEqual(
            {
                "schema",
                "location_selection",
                "combined_resolution",
                "combined_export",
                "ziwei_svg",
            },
            set(response),
        )
        self.assertNotIn("interaction", response)
        self.assertNotIn("origin_options", response)
        self.assertNotIn("temporal_options", response)

    def test_browser_assets_consume_typed_identity_without_geometry_or_bazi_view_mutation(self) -> None:
        html = interaction_index_html(INDEX_HTML)
        self.assertEqual(1, html.count('/interaction.css'))
        self.assertEqual(1, html.count('/interaction.js'))
        self.assertIn("/api/ziwei-interaction", INTERACTION_JS)
        self.assertIn("data-address-index", INTERACTION_JS)
        self.assertIn("row.designation_id", INTERACTION_JS)
        self.assertIn("member.target_raw_address.index", INTERACTION_JS)
        self.assertNotIn("clockwise_offset", INTERACTION_JS)
        self.assertNotIn("$('bazi-chart')", INTERACTION_JS)
        self.assertNotIn("renderBazi", INTERACTION_JS)
        self.assertNotIn("target_datetime", INTERACTION_JS)
        self.assertNotIn("target_longitude", INTERACTION_JS)
        self.assertIn('id="ziwei-month-nav"', INTERACTION_JS)
        self.assertIn("ziwei_lunar_month: optionalInt('ziwei-lunar-month')", INTERACTION_JS)
        self.assertIn("$('ziwei-lunar-month').value = monthNav.value", INTERACTION_JS)

    def test_real_loopback_server_exposes_additive_interaction_route(self) -> None:
        server = build_interaction_server(ROOT, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            host, port = server.server_address[:2]
            body = json.dumps(self.interaction_payload()).encode("utf-8")
            request = urllib.request.Request(
                f"http://{host}:{port}/api/ziwei-interaction",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=10) as response:
                self.assertEqual(200, response.status)
                payload = json.loads(response.read().decode("utf-8"))
            self.assertEqual(LOCAL_ZIWEI_INTERACTION_SCHEMA, payload["schema"])
            self.assertEqual("PASS", payload["interaction"]["integrity"]["status"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
