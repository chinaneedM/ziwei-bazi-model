import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13JG-GK5554-VOL18-JUAN81-82-FIRSTPARTY-ORIGINAL-HEADINGS-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
class FirstpartyHeadings(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e=json.loads(E.read_text(encoding="utf-8"))
  cls.s=json.loads(S.read_text(encoding="utf-8"))
  cls.l=json.loads(L.read_text(encoding="utf-8"))
 def test_artifact_and_hash_chain(self):
  c=self.e["source_chain"]
  self.assertEqual((c["image_run"],c["image_artifact"]),(40639648199,12794394664))
  self.assertEqual(c["javascript_sha256"],"b2b4aaabf3da440b84b64f25768965a6c2c5500775b53e7634e98e4f59adf087")
  self.assertEqual(c["official_submit_endpoint"],"https://kyudb.snu.ac.kr/pf01/rendererImg.do")
 def test_two_distinct_firstparty_page_bindings(self):
  a=self.e["original_pages"]
  self.assertEqual([(p["page_id"],p["toc_work_juan"]) for p in a],[("048a",81),("085a",82)])
  self.assertEqual([p["captured_jpeg_bytes"] for p in a],[311454,324283])
  self.assertEqual([p["pixel_dimensions"] for p in a],[[1009,2000],[1006,2000]])
  self.assertTrue(all(p["printed_work_juan_heading_confirmed"] for p in a))
 def test_original_glyphs_and_rgb_rois_scoped(self):
  a=self.e["original_pages"]
  self.assertIn("高麗史八十一",a[0]["manual_original_heading_readings"])
  self.assertIn("高麗史八十二",a[1]["manual_original_heading_readings"])
  self.assertIn("宿衛",a[1]["manual_original_heading_readings"])
  for p in a:
   self.assertEqual(len(p["heading_rois"]),2)
   self.assertTrue(all(len(r["rgb_sha256"])==64 for r in p["heading_rois"]))
 def test_no_copy_count_inflation(self):
  f=self.e["scope_firewall"]
  self.assertTrue(f["two_pages_are_one_digital_book_and_not_two_independent_physical_witnesses"])
  self.assertIsNone(f["edition_impression_date"])
  self.assertEqual(f["gk5553_book29_81_83_claim"],"RETRACTED_UNBOUND")
  self.assertEqual(self.e["counts"]["independent_physical_copies_awarded"],0)
 def test_no_unrelated_adjudication(self):
  self.assertEqual(self.e["counts"]["chart_algorithms_reopened"],0)
  self.assertEqual(self.e["transmission_impact"]["edges_supported"],[])
  self.assertEqual(self.e["counts"]["source_registry_total"],763)
 def test_forward_only_state_sync(self):
  self.assertEqual(self.s["schema_version"],self.l["binding"]["reviewed_state_version"])
  self.assertEqual(self.s["historical_audit"]["research_omission_guard"]["reviewed_state_version"],self.s["schema_version"])
  self.assertEqual(len(self.s["historical_audit"]["current_focus"]),self.l["binding"]["source_focus_count"])
  self.assertTrue(any(x.startswith("13JG ") for x in self.s["historical_audit"]["current_focus"]))
  self.assertTrue(self.s["historical_audit"]["current_focus"][-1].startswith(self.l["binding"]["latest_research_focus_prefix"]+" "))
 def test_issue_stays_open_and_binds_record(self):
  issue=next(x for x in self.l["issues"] if x["id"]=="TW-OPEN-0005")
  self.assertEqual((issue["priority"],issue["status"]),("P0","OPEN"))
  self.assertIn(E.relative_to(R).as_posix(),issue["source_refs"])
  self.assertTrue(any(x.get("revision_id","").startswith("TW-OPEN-0005-13JG-") for x in issue["history"]))
  self.assertIn("13JG CURRENT ACTION:",issue["next_action"])
  self.assertEqual(self.l["checkpoint_log"][-1]["state_version"],self.s["schema_version"])
 def test_other_source_controls_stay_open(self):
  x=next(y for y in self.l["issues"] if y["id"]=="TW-OPEN-0005")
  for token in ("G893","GK3467","NLC03130 solar D30","NLC03130 summer D14","四分","初度","13EI","RETRACTED"):
   self.assertIn(token,x["next_action"])
if __name__=="__main__":unittest.main()
