from __future__ import annotations
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify-historical-source-registry-extensions-r1.py"
spec = importlib.util.spec_from_file_location("source_extensions_gate_r1", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

class ExtensionRegistryGateR1Test(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "docs/research").mkdir(parents=True)
        self.base = self.root / gate.BASE
        self.manifest = self.root / gate.MANIFEST
        self.shard = self.root / "docs/research/a.json"
        self.base.write_text(json.dumps({"schema": "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1", "sources": [{"source_id": "ORIGINAL"}]}), encoding="utf-8")
        self.row = {
            "source_id": "NEW", "title": "Witness", "provider": "website", "url": "https://example.org/x",
            "historical_period": "MODERN_TRANSCRIPT", "source_role": "RECEIVED_TEXT_ONLY",
            "quality_notes": "No physical witness", "physical_glyph_authority": False,
            "access_date": "2026-10-10", "evidence": "docs/research/a.json",
            "verification_status": "RECEIVED_TEXT_VERIFIED"}
        self.set_data()

    def set_data(self):
        self.shard.write_text(json.dumps({"schema": "SHARD-R1", "sources": [self.row]}, ensure_ascii=False), encoding="utf-8")
        self.manifest.write_text(json.dumps({
            "schema": "FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1",
            "root_registry": gate.BASE.as_posix(),
            "root_registry_blob_sha": gate.git_blob_sha(self.base.read_bytes()),
            "root_source_count": 1, "extension_source_count": 1, "combined_source_count": 2,
            "shards": [{"path": "docs/research/a.json", "schema": "SHARD-R1", "blob_sha": gate.git_blob_sha(self.shard.read_bytes()), "source_count": 1}]
        }), encoding="utf-8")

    def test_success(self):
        self.assertEqual(gate.verify(self.root)["combined_source_count"], 2)

    def test_duplicate_fails_closed(self):
        self.row["source_id"] = "ORIGINAL"
        self.set_data()
        with self.assertRaisesRegex(ValueError, "duplicate source id"):
            gate.verify(self.root)

    def test_claim_of_physical_glyph_fails_closed(self):
        self.row["physical_glyph_authority"] = True
        self.set_data()
        with self.assertRaisesRegex(ValueError, "physical glyph authority"):
            gate.verify(self.root)

    def test_unreviewed_source_status_fails_closed(self):
        self.row["verification_status"] = "HISTORICALLY_SUPPORTED"
        self.set_data()
        with self.assertRaisesRegex(ValueError, "verification status"):
            gate.verify(self.root)

    def test_scoped_direct_image_requires_matching_digests_and_unbound_edition(self):
        evidence = self.root / "docs/research/evidence.json"
        sha, page_sha = "a"*64, "b"*64
        evidence.write_text(json.dumps({"witness": {"source_url": "https://example.org/scan",
            "source_sha256": sha, "edition_impression_date_bound": False,
            "physical_copy_catalog_identity_bound": False,
            "manually_collated_pages": [{"page": 121, "sha256": page_sha}]}}), encoding="utf-8")
        self.row.update({"physical_glyph_authority": True,
            "verification_status": "DIRECT_SOURCE_IMAGE_GLYPH_COLLATED_EDITION_UNBOUND",
            "evidence": "docs/research/evidence.json",
            "direct_image_attestation": {"source_url": "https://example.org/scan",
                "source_sha256": sha, "page_sha256": {"121": page_sha}}})
        self.set_data()
        self.assertEqual(gate.verify(self.root)["extension_source_count"], 1)
        evidence.write_text(evidence.read_text().replace(page_sha, "c"*64), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "page hashes"):
            gate.verify(self.root)

    def test_direct_image_claim_without_attestation_fails(self):
        self.row.update({"physical_glyph_authority": True,
                         "verification_status": "DIRECT_SOURCE_IMAGE_GLYPH_COLLATED_EDITION_UNBOUND"})
        self.set_data()
        with self.assertRaisesRegex(ValueError, "page-level attestation"):
            gate.verify(self.root)

    def test_source_tampering_fails(self):
        self.shard.write_text(self.shard.read_text() + " ", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "shard hash mismatch"):
            gate.verify(self.root)

    def test_root_registry_drift_fails(self):
        self.base.write_text(self.base.read_text() + " ", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "root registry changed"):
            gate.verify(self.root)

if __name__ == "__main__":
    unittest.main()
