import base64, hashlib, importlib.util, io, json, subprocess, sys, tempfile, unittest
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("strict12xg", ROOT / "scripts/verify-yehuobian-original-folio-intake-12xg.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class OriginalLeafStrictIntake(unittest.TestCase):
    def setUp(self):
        self.png = io.BytesIO()
        Image.new("RGB", (16, 16), "white").save(self.png, format="PNG")
        self.raw = self.png.getvalue()
        self.receipt = {
          "physical_item_barcode": "6403767830",
          "catalog_detail": "9927", "ncid": "BC0492354X",
          "source_shelfmark": "大木;子部:雜家類:16-20",
          "juan": 20, "chapter": "改造漏刻", "provider": "TOKYO_IOC",
          "capture_channel": "INSTITUTION_FULFILLED_COPY",
          "custody_document": "SYNTHETIC FIXTURE FOR TEST ONLY: source not contacted",
          "original_leaf_ref": "SYNTHETIC PAGE 1",
          "source_image_url": "https://www.ioc.u-tokyo.ac.jp/~library/SYNTHETIC_TEST_FIXTURE.png",
          "capture_date": "2026-10-15",
          "research_use_authorization_ref": "SYNTHETIC TEST ONLY; NO REAL PERMISSION",
          "personal_identifying_data_included": False,
          "claims_ancient_glyph_votes": 0, "claims_independent_print_witnesses": 0,
          "format": "PNG", "image_bytes": len(self.raw),
          "image_sha256": hashlib.sha256(self.raw).hexdigest(),
          "human_glyph_review_completed": False, "print_plate_identity_adjudicated": False,
        }

    def bad(self, pattern):
        with self.assertRaisesRegex(ValueError, pattern):
            m.validate(self.receipt, self.raw)

    def test_ledger(self):
        self.assertEqual(m.verify()["strict_policy"]["new_historical_glyph_votes"], 0)
    def test_valid_synthetic_image_only_integrity_no_historical_votes(self):
        q = m.validate(self.receipt, self.raw)
        self.assertEqual(q["image"]["width"], 16)
        self.assertEqual(q["historical_glyph_votes_awarded"], 0)
        self.assertIs(q["authorization_verified_with_provider"], False)
    def test_looks_like_png_but_is_not_decodable(self):
        self.raw = b"\x89PNG\r\n\x1a\n" + b"not-real-pixel-data" * 5
        self.receipt["image_bytes"] = len(self.raw)
        self.receipt["image_sha256"] = hashlib.sha256(self.raw).hexdigest()
        self.bad("image cannot be fully decoded")
    def test_non_provider_domain(self):
        self.receipt["source_image_url"] = "https://example.org/source.png"
        self.bad("not official")
    def test_provider_name_suffix_attack(self):
        self.receipt["source_image_url"] = "https://ioc.u-tokyo.ac.jp.attacker.net/source.png"
        self.bad("not official")
    def test_userinfo_hostname_confusion(self):
        self.receipt["source_image_url"] = "https://www.ioc.u-tokyo.ac.jp@attacker.net/x.png"
        self.bad("not official")
    def test_userinfo_same_host(self):
        self.receipt["source_image_url"] = "https://foo@www.ioc.u-tokyo.ac.jp/x.png"
        self.bad("userinfo")
    def test_space_control(self):
        self.receipt["source_image_url"] += "\n"
        self.bad("control/space")
    def test_nonstandard_https_port(self):
        self.receipt["source_image_url"] = "https://www.ioc.u-tokyo.ac.jp:8080/x.png"
        self.bad("not official")
    def test_1959_modern_path_percent_encoding(self):
        self.receipt["source_image_url"] = "https://www.ioc.u-tokyo.ac.jp/ttsweb/hb_new/B/B17/%42%31%37%36%35%37%30%30-1,2_photo.html"
        self.bad("modern 1959")
    def test_pdf_not_single_image(self):
        self.raw = b"%PDF-1.7\n" + b"synthetic-pdf-not-a-real-page" * 4
        self.receipt["format"] = "PDF"
        self.receipt["image_bytes"] = len(self.raw)
        self.receipt["image_sha256"] = hashlib.sha256(self.raw).hexdigest()
        self.bad("PDF needs independent")
    def test_corrupted_pixel_decode(self):
        self.raw = self.raw[:45] + b"0123456"
        self.receipt["image_bytes"] = len(self.raw)
        self.receipt["image_sha256"] = hashlib.sha256(self.raw).hexdigest()
        self.bad("image cannot be fully decoded")
    def test_catalog_barcode_cross_copy(self):
        self.receipt["physical_item_barcode"] = "6403148395"
        self.bad("catalog item scope")
    def test_no_raw_authorization_is_not_claim(self):
        self.receipt["research_use_authorization_ref"] = ""
        self.bad("date and written scope")
    def test_two_distinct_print_plate_votes_still_forbidden(self):
        self.receipt["claims_independent_print_witnesses"] = 2
        self.bad("no automatic")
    def test_real_jpeg_file_decoder(self):
        out = io.BytesIO()
        Image.new("RGB", (24, 10), "white").save(out, "JPEG")
        self.raw = out.getvalue()
        self.receipt.update(format="JPEG", image_bytes=len(self.raw), image_sha256=hashlib.sha256(self.raw).hexdigest())
        self.assertEqual(m.validate(self.receipt, self.raw)["image"]["decoded_format"], "JPEG")
    def test_wrong_declared_image_type(self):
        # A falsely declared format is caught by the 12XD signature gate before Pillow.
        self.receipt["format"] = "JPEG"
        self.bad("file signature only")
        # Test the separate Pillow decoder against a real PNG mislabeled as JPEG.
        with self.assertRaisesRegex(ValueError, "image cannot be fully decoded"):
            m.decode_image(self.raw, "JPEG")
    def test_legacy_cli_routes_actual_receipts_through_strict(self):
        with tempfile.TemporaryDirectory() as d:
            image_path = Path(d) / "fake.png"
            image_path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"fake"*20)
            r = dict(self.receipt)
            raw = image_path.read_bytes()
            r["image_bytes"] = len(raw)
            r["image_sha256"] = hashlib.sha256(raw).hexdigest()
            receipt_path = Path(d) / "receipt.json"
            receipt_path.write_text(json.dumps(r), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts/verify-yehuobian-original-folio-intake-12xd.py"),
                 "--receipt-json", str(receipt_path), "--image-file", str(image_path)],
                text=True, capture_output=True, timeout=30, check=False,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("image cannot be fully decoded", proc.stderr)

if __name__ == "__main__":
    unittest.main()
