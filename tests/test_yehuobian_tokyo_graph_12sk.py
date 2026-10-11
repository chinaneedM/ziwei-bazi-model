import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CatalogGraph12SK(unittest.TestCase):
    def test_catalog_nodes_edges_and_scope(self):
        g=json.loads((ROOT/'docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json').read_text())
        s=json.loads((ROOT/'docs/PROJECT-CURRENT-STATE-R1.json').read_text())
        z=json.loads((ROOT/'docs/research/MING-DATONG-YEHUOBIAN-12SK-TOKYO-1827-1869-CATALOG-GRAPH-BACKFILL-R1.json').read_text())
        n={x['node_id']:x for x in g['nodes']}
        e={x['edge_id']:x for x in g['edges']}
        self.assertEqual(len(g['nodes']),z['graph_change']['new_nodes'])
        self.assertEqual(len(g['edges']),z['graph_change']['new_edges'])
        self.assertEqual(n['PHYSICAL-COPY-YEHUOBIAN-TOKYO-OKI-BC0492354X-V20']['item'],'6403767830')
        self.assertEqual(n['PHYSICAL-COPY-YEHUOBIAN-TOKYO-KURAISHI-BB23196128-V19V20']['item'],'6403148395')
        self.assertNotEqual(n['PHYSICAL-COPY-YEHUOBIAN-TOKYO-OKI-BC0492354X-V20']['collection'],n['PHYSICAL-COPY-YEHUOBIAN-TOKYO-KURAISHI-BB23196128-V19V20']['collection'])
        for x in ('TG-E0234','TG-E0235'):
            self.assertEqual(e[x]['relation'],'PHYSICAL_COPY_OF_EDITION')
            self.assertEqual(e[x]['evidence_class'],'DIRECT_BIBLIOGRAPHIC_BINDING')
        self.assertTrue(all(not n[x]['target_page_collated'] for x in ('PHYSICAL-COPY-YEHUOBIAN-TOKYO-OKI-BC0492354X-V20','PHYSICAL-COPY-YEHUOBIAN-TOKYO-KURAISHI-BB23196128-V19V20')))
        self.assertEqual(z['boundaries']['source_page_glyph_votes_added'],0)
        self.assertFalse(z['boundaries']['shared_printing_plates_proven'])
        a=s['historical_audit']
        self.assertEqual((a['row_count'],a['audited_row_count']),(222,222))
        self.assertEqual((a['external_source_registry_root_count'],a['external_source_registry_extension_count'],a['external_source_registry_total_unique_count']),(647,8,655))
        self.assertTrue(a['latest_batch_doc'].endswith('-QD.md'))
        self.assertEqual(s['invariants']['algorithm_reopen_count'],0)
if __name__=='__main__': unittest.main()
