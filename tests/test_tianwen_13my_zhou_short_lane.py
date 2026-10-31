"""13MY: source-local bounded Zhou daily short lane; not an absolute calendrical adapter."""
import json
import unittest
from decimal import Decimal
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "docs/research/TIANWEN-13MY-ZHOU1569-D0-D18-BOUNDED-SHORT-LANE-R1.json"

class Tianwen13MYShortLane(unittest.TestCase):
    def test_source_local_nineteen_daily_rows(self):
        d = json.loads(PATH.read_text(encoding="utf-8"))
        rows = d["rows"]
        self.assertEqual([r["day"] for r in rows], list(range(19)))
        self.assertEqual([r["pdf_page_1based"] for r in rows], [14]*8+[15]*11)
        expected = [Decimal("4.9386") + i*Decimal("0.0186") for i in range(19)]
        observed = [Decimal(r["short_normalized"]) for r in rows]
        self.assertEqual(observed, expected)
        self.assertEqual(observed[8]-observed[7], Decimal("0.0186"))
        self.assertEqual(observed[15], Decimal("5.2176"))
        self.assertEqual(observed[16], Decimal("5.2362"))

    def test_cannot_promote_original_identity(self):
        d = json.loads(PATH.read_text(encoding="utf-8"))
        self.assertFalse(d["source"]["fresh_pdf_bytes_acquired"])
        self.assertFalse(d["source"]["fresh_pdf_sha256_computed"])
        self.assertFalse(d["source_local_replay"]["g893_same_unit_radix_epoch_bridge_proven"])
        self.assertFalse(d["national_archives_catalog_boundary"]["same_physical_copy_proven"])
        self.assertEqual(d["no_promotion"]["new_six_original_historical_winners"], 0)
        self.assertEqual(d["no_promotion"]["new_registered_source_count"], 0)
        self.assertEqual(d["no_promotion"]["algorithm_reopen_count"], 0)
        self.assertEqual(d["no_promotion"]["deterministic_chart_product"], "CLOSED")

if __name__ == "__main__":
    unittest.main()
