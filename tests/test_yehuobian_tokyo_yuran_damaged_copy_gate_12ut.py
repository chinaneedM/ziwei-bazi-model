#!/usr/bin/env python3
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("gate12ut", ROOT / "scripts/verify-yehuobian-tokyo-yuran-damaged-copy-gate-12ut.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

class CopyConditionGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / mod.DATA).read_text(encoding="utf-8"))
        cls.registry = json.loads((ROOT / mod.REGISTRY).read_text(encoding="utf-8"))
        cls.base = json.loads((ROOT / mod.BASE).read_text(encoding="utf-8"))
        cls.extra = json.loads((ROOT / mod.EXTRA).read_text(encoding="utf-8"))
    def check(self, data, registry=None, base=None, extra=None):
        return mod.validate(data, registry or self.registry, base or self.base, extra or self.extra)
    def test_real_records_pass(self):
        self.assertEqual(self.check(self.data)["original_juan20_glyph_votes"], 0)
    def test_chapter19_lacuna_cannot_be_chapter20_absence(self):
        d = copy.deepcopy(self.data)
        d["physical_copy"]["volume20_target_folio_absence_proven"] = True
        with self.assertRaises(ValueError): self.check(d)
    def test_catalogued_unavailable_cannot_be_actionable_without_new_source(self):
        d = copy.deepcopy(self.data)
        d["institutional_access"]["access_priority"] = "ACTIONABLE"
        with self.assertRaises(ValueError): self.check(d)
    def test_general_copy_guidance_is_not_item_permission(self):
        d = copy.deepcopy(self.data)
        d["institutional_access"]["individualized_permission_granted"] = True
        with self.assertRaises(ValueError): self.check(d)
    def test_catalogue_cannot_supply_historical_glyph(self):
        d = copy.deepcopy(self.data)
        d["physical_copy"]["four_locus_readings"]["GONGJIN"] = "宮禁"
        with self.assertRaises(ValueError): self.check(d)
    def test_1827_1869_comparator_not_conflated(self):
        d = copy.deepcopy(self.data)
        d["priority_comparators"][1]["item"] = "6403767830"
        with self.assertRaises(ValueError): self.check(d)
    def test_inaccessible_item_not_queued_as_original(self):
        b = copy.deepcopy(self.base)
        b["candidates"][0]["id"] = "TOKYO_YURAN_1827_6411758714"
        with self.assertRaises(ValueError): self.check(self.data, base=b)
    def test_metadata_registry_id_must_match(self):
        d = copy.deepcopy(self.data)
        d["physical_copy"]["registry_id"] = "EXT-NONEXISTENT"
        with self.assertRaises(ValueError): self.check(d)

if __name__ == "__main__":
    unittest.main()
