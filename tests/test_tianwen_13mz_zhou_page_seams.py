"""13MZ: bounded table page/fold seams, not an independent calendar epoch."""
import json
import unittest
from decimal import Decimal
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "docs/research/TIANWEN-13MZ-ZHOU1569-P15-P16-D29-D30-D40-D41-SEAM-R1.json"
S = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
L = ROOT / "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
class Tianwen13MZSeams(unittest.TestCase):
    def test_independent_visual_anchor_coordinates_and_decimal_consistency(self):
        e=json.loads(E.read_text(encoding="utf-8"))
        rows=e["observed_bounded_normalized_anchors"]
        self.assertEqual([(r["day"],r["page"]) for r in rows],[(19,15),(29,15),(30,16),(40,16),(41,16),(51,16)])
        base=Decimal("4.9386"); step=Decimal("0.0186")
        for r in rows:
            self.assertEqual(Decimal(r["short"]),base+step*r["day"])
        self.assertEqual(Decimal(rows[2]["short"])-Decimal(rows[1]["short"]),step)
        self.assertEqual(Decimal(rows[4]["short"])-Decimal(rows[3]["short"]),step)
        self.assertFalse(e["source_local_arithmetic"]["all_intervening_rows_individually_glyph_verified"])
    def test_historical_source_and_copy_nonpromotion(self):
        e=json.loads(E.read_text(encoding="utf-8"))
        self.assertFalse(e["source"]["fresh_pdf_bytes_acquired"])
        self.assertFalse(e["source"]["native_glyph_pixel_collation"])
        self.assertEqual(e["source"]["physical_witness_count_added"],0)
        self.assertFalse(e["naaj_boundary"]["adjacent_record_is_target"])
        self.assertFalse(e["naaj_boundary"]["official_target_item_id_verified"])
        self.assertFalse(e["naaj_boundary"]["call_number_conflict_resolved"])
        self.assertFalse(e["no_promotion"]["g893_units_radix_epoch_bridge_proven"])
        self.assertEqual(e["no_promotion"]["new_historical_winners"],0)
        self.assertEqual(e["no_promotion"]["algorithm_reopens"],0)
        self.assertEqual(e["no_promotion"]["product"],"CLOSED")
    def test_live_handoff_guards(self):
        s=json.loads(S.read_text(encoding="utf-8"))
        l=json.loads(L.read_text(encoding="utf-8"))
        self.assertEqual(s["historical_audit"]["research_omission_guard"]["reviewed_state_version"],s["schema_version"])
        self.assertEqual(l["binding"]["reviewed_state_version"],s["schema_version"])
        self.assertEqual(l["binding"]["source_focus_count"],len(s["historical_audit"]["current_focus"]))
        self.assertEqual(l["binding"]["latest_research_focus_prefix"],s["historical_audit"]["current_focus"][-1].split(" ")[0])
        i=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
        self.assertEqual(i["priority"],"P0")
        self.assertEqual(i["status"],"OPEN")
        self.assertTrue(i["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:"))
        self.assertIn("docs/research/TIANWEN-13MZ-ZHOU1569-P15-P16-D29-D30-D40-D41-SEAM-R1.json",i["source_refs"])
if __name__=="__main__":unittest.main()
