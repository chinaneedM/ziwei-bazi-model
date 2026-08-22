from __future__ import annotations

import json
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

from jsonschema import Draft202012Validator

from fortune_training.ziwei_application.local_app import (
    APP_JS,
    CSP,
    INDEX_HTML,
    LOCAL_APP_ERROR_SCHEMA,
    LOCAL_APP_HEALTH_SCHEMA,
    LOCAL_APP_RESOLVE_SCHEMA,
    MAX_REQUEST_BYTES,
    STYLE_CSS,
    build_server,
)


ROOT = Path(__file__).resolve().parents[1]


class ZiweiLocalAppV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = build_server(ROOT, port=0)
        cls.host, cls.port = cls.server.server_address[:2]
        cls.base_url = f"http://{cls.host}:{cls.port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.fixture = {
            "birth_datetime": "1994-05-17T14:30:00",
            "birth_place": "Beijing",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone_id": "Asia/Shanghai",
            "sex": "MALE",
            "daxian_frame_id": "DAXIAN:index=1",
            "annual_year": 2001,
            "lunar_month": 5,
            "minor_limit_age": 8,
        }

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    @classmethod
    def _get(cls, path: str):
        with urllib.request.urlopen(cls.base_url + path, timeout=30) as response:
            return response.status, dict(response.headers.items()), response.read()

    @classmethod
    def _post_raw(cls, body: bytes, *, content_type: str = "application/json"):
        request = urllib.request.Request(
            cls.base_url + "/api/resolve",
            data=body,
            headers={"Content-Type": content_type},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                return response.status, dict(response.headers.items()), response.read()
        except urllib.error.HTTPError as exc:
            return exc.code, dict(exc.headers.items()), exc.read()

    @classmethod
    def _post_json(cls, payload):
        return cls._post_raw(json.dumps(payload, ensure_ascii=False).encode("utf-8"))

    def test_server_binds_loopback_only(self) -> None:
        self.assertEqual("127.0.0.1", self.host)

    def test_health_endpoint_is_fixed_and_versioned(self) -> None:
        status, headers, body = self._get("/health")
        self.assertEqual(200, status)
        payload = json.loads(body)
        self.assertEqual(LOCAL_APP_HEALTH_SCHEMA, payload["schema"])
        self.assertEqual("ok", payload["status"])
        self.assertEqual("LOOPBACK_ONLY", payload["bind_policy"])
        self.assertEqual(CSP, headers["Content-Security-Policy"])
        self.assertEqual("nosniff", headers["X-Content-Type-Options"])

    def test_local_page_assets_are_self_contained(self) -> None:
        status, headers, body = self._get("/")
        self.assertEqual(200, status)
        html = body.decode("utf-8")
        self.assertIn("紫微排盘", html)
        self.assertIn('/style.css', html)
        self.assertIn('/app.js', html)
        self.assertEqual(CSP, headers["Content-Security-Policy"])
        joined = "\n".join((INDEX_HTML, STYLE_CSS, APP_JS)).lower()
        self.assertNotIn("https://", joined)
        self.assertNotIn("http://", joined)
        self.assertNotIn("<script>", INDEX_HTML.lower())

    def test_real_http_resolve_returns_application_export_and_svg(self) -> None:
        status, _, body = self._post_json(self.fixture)
        self.assertEqual(200, status, body.decode("utf-8", errors="replace"))
        payload = json.loads(body)
        self.assertEqual(LOCAL_APP_RESOLVE_SCHEMA, payload["schema"])
        export = payload["application_export"]
        artifact = payload["svg_artifact"]
        self.assertEqual(export["view_hash"], artifact["source_view_hash"])
        self.assertRegex(export["bundle_hash"], r"^[0-9a-f]{64}$")
        self.assertRegex(artifact["render_hash"], r"^[0-9a-f]{64}$")
        self.assertTrue(payload["svg"].startswith('<?xml version="1.0" encoding="UTF-8"?>'))
        self.assertIn("DAXIAN:index=1", payload["svg"])
        self.assertIn("ANNUAL:2001", payload["svg"])

    def test_response_validates_against_local_and_application_schemas(self) -> None:
        status, _, body = self._post_json(self.fixture)
        self.assertEqual(200, status)
        payload = json.loads(body)
        local_schema = json.loads(
            (ROOT / "schemas" / "ziwei-local-app-resolve-v1.schema.json").read_text(encoding="utf-8")
        )
        application_schema = json.loads(
            (ROOT / "schemas" / "ziwei-application-chart-export-v1.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(local_schema)
        Draft202012Validator.check_schema(application_schema)
        local_errors = list(Draft202012Validator(local_schema).iter_errors(payload))
        app_errors = list(Draft202012Validator(application_schema).iter_errors(payload["application_export"]))
        if local_errors:
            self.fail("local response schema failed: " + "; ".join(row.message for row in local_errors))
        if app_errors:
            self.fail("application export schema failed: " + "; ".join(row.message for row in app_errors))

    def test_same_http_request_is_deterministic(self) -> None:
        first_status, _, first_body = self._post_json(self.fixture)
        second_status, _, second_body = self._post_json(self.fixture)
        self.assertEqual(200, first_status)
        self.assertEqual(200, second_status)
        first = json.loads(first_body)
        second = json.loads(second_body)
        self.assertEqual(first["application_export"]["bundle_hash"], second["application_export"]["bundle_hash"])
        self.assertEqual(first["application_export"]["view_hash"], second["application_export"]["view_hash"])
        self.assertEqual(first["svg_artifact"]["render_hash"], second["svg_artifact"]["render_hash"])
        self.assertEqual(first["svg"], second["svg"])

    def test_invalid_sex_and_timezone_are_structured_4xx(self) -> None:
        bad_sex = dict(self.fixture, sex="UNKNOWN")
        status, _, body = self._post_json(bad_sex)
        payload = json.loads(body)
        self.assertEqual(400, status)
        self.assertEqual(LOCAL_APP_ERROR_SCHEMA, payload["schema"])
        self.assertEqual("LOCAL_APP_INVALID_INPUT", payload["error"]["code"])

        bad_zone = dict(self.fixture, timezone_id="Not/A_Real_Timezone")
        status, _, body = self._post_json(bad_zone)
        payload = json.loads(body)
        self.assertEqual(400, status)
        self.assertEqual("LOCAL_APP_INVALID_TIMEZONE", payload["error"]["code"])

    def test_invalid_datetime_and_numeric_input_are_structured_4xx(self) -> None:
        bad_datetime = dict(self.fixture, birth_datetime="not-a-date")
        status, _, body = self._post_json(bad_datetime)
        self.assertEqual(400, status)
        self.assertEqual("LOCAL_APP_INVALID_INPUT", json.loads(body)["error"]["code"])

        bad_number = dict(self.fixture, latitude="NaN")
        status, _, body = self._post_json(bad_number)
        self.assertEqual(400, status)
        self.assertEqual("LOCAL_APP_INVALID_INPUT", json.loads(body)["error"]["code"])

    def test_malformed_oversized_and_wrong_content_type_are_rejected(self) -> None:
        status, _, body = self._post_raw(b"{")
        self.assertEqual(400, status)
        self.assertEqual("LOCAL_APP_INVALID_JSON", json.loads(body)["error"]["code"])

        oversized = b"{" + b" " * (MAX_REQUEST_BYTES + 1)
        status, _, body = self._post_raw(oversized)
        self.assertEqual(413, status)
        self.assertEqual("LOCAL_APP_REQUEST_TOO_LARGE", json.loads(body)["error"]["code"])

        status, _, body = self._post_raw(b"{}", content_type="text/plain")
        self.assertEqual(415, status)
        self.assertEqual("LOCAL_APP_JSON_REQUIRED", json.loads(body)["error"]["code"])

    def test_user_supplied_html_is_not_reflected_into_svg(self) -> None:
        payload = dict(self.fixture, birth_place='<script>alert("x")</script>')
        status, _, body = self._post_json(payload)
        self.assertEqual(200, status)
        response = json.loads(body)
        self.assertNotIn('<script>alert("x")</script>', response["svg"])
        self.assertNotIn("<script", response["svg"].lower())


if __name__ == "__main__":
    unittest.main()
