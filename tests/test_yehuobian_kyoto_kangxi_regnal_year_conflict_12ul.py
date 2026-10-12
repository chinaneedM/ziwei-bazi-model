"""12UL: Kyoto catalog Kangxi regnal mismatch is not original-print evidence."""
import json,importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/MING-DATONG-YEHUOBIAN-12UL-KYOTO-KANGXI-PREFACE-DATE-CONFLICT-R1.json"
S="docs/research/MING-DATONG-YEHUOBIAN-12UL-ERA-CONCORDANCE-SOURCE-SHARD-R1.json"
QF="docs/research/MING-DATONG-YEHUOBIAN-12QF-CADAL-FIRST-PREFACE-DIRECT-DATES-R1.json"
def read(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
class KyotoDateConflict12UL(unittest.TestCase):
 def test_regnal_year_mismatch_and_physical_copy_boundary(self):
  x=read(E); c=x["catalog"]; k=x["calendar_authority"]
  self.assertEqual(c["ncid"],"BB18578034")
  self.assertIn("康熙30年[1700]",c["verbatim_catalog_annotation"])
  self.assertEqual(k["regnal_30_year"],1691);self.assertEqual(k["regnal_39_year"],1700)
  self.assertEqual(c["same_line_regnal_30_correct_gregorian"],k["regnal_30_year"])
  self.assertEqual(c["gregorian_1700_correct_kangxi_regnal"],39)
  self.assertTrue(c["internal_conflict_proven"])
  self.assertEqual(c["exact_cause_of_catalog_mismatch"],"UNRESOLVED")
  self.assertFalse(c["original_kyoto_frontmatter_page_image_read"])
  self.assertFalse(c["physical_copy_1827_unrepaired_first_impression_proven"])
 def test_existing_cadal_image_hash_and_earlier_layers(self):
  x=read(E); qf=read(QF)["witness"]; w=x["prior_source_image"]
  self.assertEqual(qf["source_sha256"],w["source_binary_sha256"])
  p=next(p for p in qf["manually_collated_pages"] if p["page"]==10)
  self.assertEqual(p["sha256"],w["page_image_sha256"])
  self.assertEqual(p["reading"],w["manually_read"])
  self.assertEqual(w["semantic_year"],1700)
  self.assertFalse(qf["physical_copy_catalog_identity_bound"])
  self.assertFalse(qf["edition_impression_date_bound"])
  self.assertEqual(w["exact_kyoto_catalog_physical_copy_match"],"NOT_PROVEN")
  self.assertEqual({z["year"] for z in read(QF)["four_separate_date_layers"]},{1606,1700,1827,1869})
 def test_registry_counts_are_current_not_old_snapshot(self):
  spec=importlib.util.spec_from_file_location("reg",ROOT/"scripts/verify-historical-source-registry-extensions-r1.py")
  m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  v=m.verify(ROOT); state=read("docs/PROJECT-CURRENT-STATE-R1.json")
  self.assertEqual(v["combined_source_count"],state["historical_audit"]["external_source_registry_total_unique_count"])
  self.assertEqual(v["extension_source_count"],state["historical_audit"]["external_source_registry_extension_count"])
  self.assertGreaterEqual(v["combined_source_count"],read(E)["accounting"]["total_sources_after"])
  self.assertTrue(any(s.startswith("12UL ") for s in state["historical_audit"]["current_focus"]))
  sources=read(S)["sources"];self.assertEqual(len(sources),1)
  self.assertTrue(all(s["verification_status"]=="BIBLIOGRAPHIC_METADATA_ONLY" and not s["physical_glyph_authority"] for s in sources))
  self.assertFalse(read(E)["disposition"]["do_not_rewrite_institution_catalog"] is False)
  self.assertEqual(read(E)["disposition"]["new_glyph_votes"],0)
  self.assertEqual(state["invariants"]["algorithm_reopen_count"],0)
if __name__=="__main__":unittest.main()
