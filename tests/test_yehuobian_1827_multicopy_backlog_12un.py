"""12UN: two already registered but missing from the six-candidate image intake plan."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
S=ROOT / "scripts/verify-yehuobian-1827-multicopy-backlog-r1.py"
spec=importlib.util.spec_from_file_location("backlog12un",S)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
load=lambda path:json.loads((ROOT/path).read_text(encoding="utf-8"))
P="docs/research/MING-DATONG-YEHUOBIAN-12UN-ADDITIONAL-1827-PHYSICAL-COPY-BACKLOG-R1.json"
B="docs/research/MING-DATONG-YEHUOBIAN-12UK-ORIGINAL-LEAF-INTAKE-QUEUE-R1.json"
C="docs/research/MING-DATONG-YEHUOBIAN-12UF-SOURCE-READING-CONTROL-AND-IMPRESSION-GATES-R1.json"
R="docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"

class MultiCopy12UN(unittest.TestCase):
    def setUp(self):
        self.d,self.b,self.c,self.r=(load(x) for x in [P,B,C,R])
    def check(self):
        return mod.validate(self.d,self.b,self.c,self.r)
    def test_composite_queue_eight_objects_zero_votes_and_zero_new_sources(self):
        self.assertEqual(self.check(),dict(status="PASS",old_candidates=6,incremental_candidates=2,total_pending_objects=8,new_external_sources=0,ancient_glyph_votes=0))
    def test_previously_registered_sources_not_readded(self):
        self.d["new_external_source_count"]=2
        with self.assertRaisesRegex(ValueError,"count mismatch"):self.check()
    def test_cannot_merge_kyoto_physical_accessions(self):
        self.d["candidates"][0]["object_identifier"]=self.b["candidates"][0]["object_identifier"]
        with self.assertRaisesRegex(ValueError,"binding"):self.check()
    def test_catalog_without_image_cannot_claim_four_locus_reading(self):
        self.d["candidates"][0]["four_locus_readings"]["GONGJIN"]="宮禁"
        with self.assertRaisesRegex(ValueError,"characters"):self.check()
    def test_catalog_not_proof_of_first_impression(self):
        self.d["candidates"][1]["verified_unrepaired_1827_original"]=True
        with self.assertRaisesRegex(ValueError,"unverified"):self.check()
    def test_20_volume_chronology_not_thematic30(self):
        self.d["candidates"][0]["historical_volume_arrangement"]="CHRONOLOGICAL_20"
        with self.assertRaisesRegex(ValueError,"old chronological"):self.check()
    def test_lower_priority_inaccessible_copy_not_new_witness(self):
        self.d["prior_known_but_not_queued"]["new_source"]=True
        with self.assertRaisesRegex(ValueError,"lower-priority"):self.check()
    def test_no_new_algorithm_or_prediction(self):
        self.d["algorithm_reopen_authorized"]=True
        with self.assertRaisesRegex(ValueError,"algorithm reopen"):self.check()
        st=load("docs/PROJECT-CURRENT-STATE-R1.json")
        self.assertTrue(any(x.startswith("12UN ") for x in st["historical_audit"]["current_focus"]))
        self.assertEqual(self.d["accounting"]["total_sources"],687)
        self.assertEqual(self.d["accounting"]["root_sources"]+self.d["accounting"]["extension_sources"],687)
        self.assertGreaterEqual(st["historical_audit"]["external_source_registry_total_unique_count"],self.d["accounting"]["total_sources"])
        self.assertEqual(st["invariants"]["algorithm_reopen_count"],0)
        self.assertEqual(st["invariants"]["deterministic_fusion_chart_product_r1"],"CLOSED")

if __name__=="__main__":
    unittest.main()
