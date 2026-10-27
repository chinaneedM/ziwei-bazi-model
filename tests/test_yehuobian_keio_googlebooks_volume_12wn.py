import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("wn",ROOT/"scripts/probe-yehuobian-12wn-keio-googlebooks-volume-metadata.py")
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class MockResponse:
 def __init__(self,url,payload):
  self.url=url;self.payload=payload
 def __enter__(self):return self
 def __exit__(self,*args):return None
 def geturl(self):return self.url
 def read(self,num):return self.payload[:num]
class ProviderVolume(unittest.TestCase):
 def obj(self):return {"id":p.ID,"kind":"books#volume","volumeInfo":{"title":"野獲編 : 30巻補遺4巻","publisher":"姚氏扶荔山房","publishedDate":"1827","pageCount":300},"accessInfo":{"country":"JP","viewability":"NO_PAGES","pdf":{"isAvailable":False}}}
 def open_with(self,obj):
  raw=json.dumps(obj).encode()
  return lambda req,timeout:MockResponse(req.full_url,raw)
 def test_explicit_provider_id(self):
  o,b=p.read_public_metadata(self.open_with(self.obj()))
  self.assertEqual(o["id"],p.ID)
 def test_never_confirm_original_juan20_from_catalog_date(self):
  d=p.classify(self.obj())
  self.assertFalse(d["source_juan20_folio_identified"])
  self.assertFalse(d["original_1827_unrepaired_print_proven"])
  self.assertEqual(d["new_independent_ancient_original_folio_votes"],0)
 def test_1869_not_automatically_comparator(self):
  self.assertFalse(p.classify(self.obj())["1869_print_comparator_proven"])
 def test_error_on_wrong_work(self):
  obj=self.obj();obj["volumeInfo"]["title"]="一代名著"
  with self.assertRaisesRegex(ValueError,"title"):p.classify(obj)
 def test_error_on_wrong_volume_id(self):
  obj=self.obj();obj["id"]="ALTERED"
  with self.assertRaisesRegex(ValueError,"nonmatching"):p.read_public_metadata(self.open_with(obj))
 def test_error_on_wrong_resource_type(self):
  obj=self.obj();obj["kind"]="books#bookshelf"
  with self.assertRaisesRegex(ValueError,"nonmatching"):p.read_public_metadata(self.open_with(obj))
 def test_forbid_unapproved_redirect(self):
  for url in ("http://www.googleapis.com/books/v1/volumes/"+p.ID,"https://attacker.example/books/v1/volumes/"+p.ID,"https://www.googleapis.com/books/v1/volumes/OTHER"):
   with self.assertRaisesRegex(ValueError,"unapproved"):p.check_url(url)
 def test_pdf_availability_not_paper_identity(self):
  obj=self.obj();obj["accessInfo"]["viewability"]="ALL_PAGES";obj["accessInfo"]["pdf"]["isAvailable"]=True
  d=p.classify(obj)
  self.assertFalse(d["source_printed_page_images_examined"])
  self.assertFalse(d["original_1827_unrepaired_print_proven"])
 def test_api_response_has_bound(self):self.assertLess(p.MAX_BYTES,1_000_000)
 def test_strict_title_requires_exact_work(self):
  obj=self.obj();obj["volumeInfo"]["title"]="朱子语类"
  with self.assertRaisesRegex(ValueError,"title"):p.classify(obj)
if __name__=="__main__":unittest.main()
