#!/usr/bin/env python3
import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("verify12ux",ROOT/"scripts/verify-yehuobian-npm-jinxiang-12ux.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
class NPMJinxiangCopyBinding(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.v=[load(p) for p in (m.RECORD,m.SHARD,m.MANIFEST,m.GRAPH,m.STATE)]
 def check(self,values=None):return m.validate(*(self.v if values is None else values))
 def bad(self,i,path,new):
  c=copy.deepcopy(self.v);a=c[i]
  for k in path[:-1]:a=a[k]
  a[path[-1]]=new
  with self.assertRaises(ValueError):self.check(c)
 def test_baseline(self):self.assertEqual(self.check()["new_target_glyph_votes"],0)
 def test_16_not_20_books(self):self.bad(0,["object","individual_book_count"],20)
 def test_exhibited_part_not_juan20(self):self.bad(0,["object","item_displayed_in_2023"],"故觀003520")
 def test_no_certain_print_year(self):self.bad(0,["object","precise_impression_year"],1827)
 def test_unknown_plates(self):self.bad(0,["object","edition_printing_block_identity"],"1827")
 def test_1869_not_same_plate(self):self.bad(0,["print_lineage_firewall","same_plate_as_tokyo_or_kyoto_unproven"],False)
 def test_no_current_access_permission(self):self.bad(0,["legacy_copy_note","current_2026_permission"],"DENIED")
 def test_2009_note_not_current_denial(self):self.bad(0,["print_lineage_firewall","2009_copy_restriction_is_not_current_access_denial"],False)
 def test_museum_image_not_page(self):self.bad(0,["print_lineage_firewall","museum_cover_photo_not_four_target_page_glyphs"],False)
 def test_zero_original_target(self):self.bad(0,["scope_outcome","new_original_juan20_pages"],1)
 def test_zero_glyph_vote(self):self.bad(0,["scope_outcome","new_historical_target_glyph_votes"],1)
 def test_zero_outreach(self):self.bad(0,["scope_outcome","institutional_contact_sent"],1)
 def test_no_source_upgrade(self):self.bad(1,["sources",0,"physical_glyph_authority"],True)
 def test_manifest_counts(self):self.bad(2,["combined_source_count"],self.v[2]["combined_source_count"]+1)
 def test_graph_relation_not_1827(self):
  e=next(i for i,x in enumerate(self.v[3]["edges"]) if x.get("edge_id")=="TG-E0238")
  self.bad(3,["edges",e,"to"],"EDITION-YEHUOBIAN-1827-FULISHANFANG-30V")
 def test_graph_node_unread(self):self.bad(3,["nodes",251,"target_page_collated"],True)
 def test_state_count(self):self.bad(4,["historical_audit","external_source_registry_extension_count"],40)
 def test_past_owner_not_physical_seal(self):self.bad(0,["print_lineage_firewall","yuan_past_owner_narrative_not_physically_seal_proven"],False)
if __name__=="__main__":unittest.main()
