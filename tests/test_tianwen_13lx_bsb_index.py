"""13LX first-party index parser must not invent physical-volume identity."""
import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/probe-tianwen-13lx-bsb-mingshi-volume-index.py"
s=importlib.util.spec_from_file_location("bsb13lx",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class SourceTitleTests(unittest.TestCase):
 def test_eight_explicit_volumes(self):
  h="".join(f'<section><h4>Ming shi (明史); {n}</h4><a href="/view/bsb1234567{n}">Mehr Informationen zum Titel</a></section>' for n in range(1,9))
  cards=m.extract(h,"https://ostasien.digitale-sammlungen.de/discover/titles/M")
  self.assertEqual([x["number"] for x in cards],list(range(1,9)))
  self.assertEqual(cards[0]["provider_links"],["https://ostasien.digitale-sammlungen.de/view/bsb12345671"])
 def test_does_not_guess_from_volume_two(self):
  h='<section><h4>Ming shi (明史); 2</h4><a href="/view/bsb11166692">Detail</a></section>'
  self.assertEqual([x["number"] for x in m.extract(h,"https://ostasien.digitale-sammlungen.de")],[2])
 def test_offsite_link_rejected(self):
  h='<section><h4>Ming shi (明史); 1</h4><a href="https://evil.example/test">Detail</a></section>'
  self.assertEqual(m.extract(h,"https://ostasien.digitale-sammlungen.de")[0]["provider_links"],[])
 def test_other_ming_shi_forms_not_assumed_volume(self):
  self.assertEqual(m.extract('<p>Ming shi gao (明史藁)</p>','https://ostasien.digitale-sammlungen.de'),[])
if __name__=="__main__":unittest.main()
