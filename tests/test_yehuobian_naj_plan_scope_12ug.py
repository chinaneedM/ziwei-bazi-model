"""A dated digitization plan cannot supply an edition, target glyph or completion."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = "docs/research/MING-DATONG-YEHUOBIAN-12UG-NAJ3080212-DIGITIZATION-PLAN-AND-TARGET-ACCESS-R1.json"
SHARD = "docs/research/MING-DATONG-YEHUOBIAN-12UG-NAJ-DIGITIZATION-PLAN-SOURCE-SHARD-R1.json"

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class NajPlanScope12UG(unittest.TestCase):
    def test_no_plan_or_index_promotion_to_glyph(self):
        e = read(EVIDENCE)
        plan = e["official_plan"]
        self.assertEqual(plan["catalog_or_plan_shelfmark"], "308-0212")
        self.assertEqual(plan["pages"], 91)
        self.assertEqual(plan["pdf_sha256"], "42041ac392c208ac039b19b48ebc8501e0528ef5f2f102640bd3def143366e54")
        self.assertEqual({p["pdf_page"] for p in plan["manual_visual_review"]}, {1, 21, 91})
        self.assertFalse(plan["plan_is_completion_report"])
        self.assertFalse(plan["2026_public_access_proven"])
        self.assertEqual(plan["ancient_edition_or_impression"], "UNBOUND")
        self.assertTrue(all(v is None for v in e["four_locus_readings"].values()))
        self.assertFalse(e["gates"]["source_bound_original_target_leaf_seen"])
        self.assertEqual(e["gates"]["new_independent_ancient_glyph_votes"], 0)
        source = read(SHARD)["sources"][0]
        self.assertEqual(source["evidence"], EVIDENCE)
        self.assertEqual(source["verification_status"], "BIBLIOGRAPHIC_METADATA_ONLY")
        self.assertFalse(source["physical_glyph_authority"])

    def test_current_counts_are_derived_while_prior_snapshots_survive(self):
        path = ROOT / "scripts/verify-historical-source-registry-extensions-r1.py"
        spec = importlib.util.spec_from_file_location("registry_12ug", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        verified = module.verify(ROOT)
        state = read("docs/PROJECT-CURRENT-STATE-R1.json")
        self.assertEqual(verified["combined_source_count"], state["historical_audit"]["external_source_registry_total_unique_count"])
        self.assertEqual(verified["extension_source_count"], state["historical_audit"]["external_source_registry_extension_count"])
        self.assertEqual(read(EVIDENCE)["accounting"]["unique_sources_after"], 679)
        self.assertEqual(read("docs/research/MING-DATONG-YEHUOBIAN-12UD-XUXIU1174-FOUR-LOCI-SEAM-CORRECTION-R1.json")["invariants"]["source_registry_total"], 678)
        self.assertTrue(any(t.startswith("12UG ") for t in state["historical_audit"]["current_focus"]))

if __name__ == "__main__":
    unittest.main()
