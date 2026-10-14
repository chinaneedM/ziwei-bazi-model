import gzip,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);return v
scan=load("marc12vw","scripts/probe-yehuobian-columbia-marc-12vw.py")
guard=load("scope12vw","scripts/verify-yehuobian-columbia-marc-scope-12vw.py")
MARC='http://www.loc.gov/MARC21/slim'
def rec(i,title,extras=""):
    return f'<record xmlns="{MARC}"><leader>00000nam a2200000 a 4500</leader><controlfield tag="001">{i}</controlfield><datafield tag="245" ind1="1" ind2="0"><subfield code="a">{title}</subfield></datafield>{extras}</record>'
class ColumbiaMARC(unittest.TestCase):
 def setUp(self):
    self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
    self.file=Path(self.temp.name)/"synthetic.xml.gz"
 def fixture(self,records):
    xml=f'<collection xmlns="{MARC}">'+''.join(records)+'</collection>'
    with gzip.open(self.file,'wb') as fh:fh.write(xml.encode())
 def test_synthetic_mixed_titles(self):
    self.fixture([rec("111","普通史书"),rec("222","萬曆野獲編",'<datafield xmlns="'+MARC+'" tag="852"><subfield code="h">FAKE TEST SHELFMARK</subfield></datafield>')])
    a=scan.report(self.file)
    self.assertEqual((a["record_count"],a["matched_title_records"],a["ancient_glyph_votes"]),(2,1,0))
    self.assertEqual(a["title_candidates"][0]["marc_001"],"222")
    self.assertFalse(a["whole_catalog_searched"])
 def test_romanization(self):
    self.assertTrue(scan.title_candidate(["Shen Te-fu: Wan li ye huo bian"]))
    self.assertTrue(scan.title_candidate(["Wan-li yeh huo pien"]))
 def test_simplified(self):self.assertTrue(scan.title_candidate(["万历野获编"]))
 def test_unrelated(self):self.assertFalse(scan.title_candidate(["Columbia history of print"]))
 def test_one_shard_nonhit_not_absence(self):
    self.fixture([rec("1","Unrelated book")]);x=scan.report(self.file)
    self.assertEqual(x["matched_title_records"],0);self.assertFalse(x["catalog_absence_inference_allowed"])
 def test_cap_matches_and_report_truncation(self):
    self.fixture([rec(str(i),"萬曆野獲編") for i in range(3)])
    x=scan.scan_gz(self.file,max_results=1)
    self.assertTrue(x["results_truncated"]);self.assertEqual(x["matched_title_records"],3)
 def test_corrupted_gzip_raises(self):
    self.file.write_bytes(b"not-gzip");self.assertRaises((OSError,EOFError),scan.scan_gz,self.file)
 def test_invalid_shard_number(self):
    with self.assertRaisesRegex(ValueError,"between 1 and 111"):scan.download_one(112,self.file)
 def test_source_schema(self):self.assertEqual(guard.verify()["new_ancient_glyph_votes"],0)
 def test_open_data_not_physical_original(self):
    rec0=json.loads((ROOT/guard.RECORD).read_text());s=json.loads((ROOT/guard.SHARD).read_text())
    m=json.loads((ROOT/guard.MANIFEST).read_text());st=json.loads((ROOT/guard.STATE).read_text())
    rec0["repository_gates"]["marc_catalogue_is_not_original_page_scan"]=False
    with self.assertRaisesRegex(ValueError,"marc_catalogue"):guard.validate(rec0,s,m,st)
if __name__=="__main__":unittest.main()
