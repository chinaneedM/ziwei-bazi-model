import hashlib,importlib.util,io,socket,ssl,unittest,urllib.error
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'scripts/fetch-tianwen-13hb-photo4-source.py'
s=importlib.util.spec_from_file_location('transport13lk',p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Response(io.BytesIO):
 def geturl(self):return v.URL
class SourceTransport(unittest.TestCase):
 def setUp(self):self.source={'source_emitted_download_url':v.URL,'jpeg_bytes':3,'jpeg_sha256':hashlib.sha256(b'abc').hexdigest()};self.calls=0
 def fetch(self,seq):
  def op(*a,**k):
   self.calls+=1;x=seq.pop(0)
   if isinstance(x,Exception):raise x
   return Response(x)
  return v.fetch(self.source,opener=op,sleeper=lambda _:None)
 def test_timeout_then_hash_verified(self):
  data,events=self.fetch([urllib.error.URLError(socket.timeout('connect')),b'abc']);self.assertEqual(data,b'abc');self.assertEqual(len(events),2)
 def test_server_503_then_success(self):self.assertEqual(self.fetch([urllib.error.HTTPError(v.URL,503,'unavailable',{},None),b'abc'])[0],b'abc')
 def test_timeout_exhaustion_fails(self):
  with self.assertRaises(urllib.error.URLError):self.fetch([urllib.error.URLError(TimeoutError()) for _ in range(3)])
  self.assertEqual(self.calls,3)
 def test_403_is_not_retried(self):
  with self.assertRaises(urllib.error.HTTPError):self.fetch([urllib.error.HTTPError(v.URL,403,'forbidden',{},None),b'abc'])
  self.assertEqual(self.calls,1)
 def test_tls_failure_is_not_retried(self):
  with self.assertRaises(urllib.error.URLError):self.fetch([urllib.error.URLError(ssl.SSLCertVerificationError('certificate')),b'abc'])
  self.assertEqual(self.calls,1)
 def test_wrong_hash_is_not_retried(self):
  with self.assertRaises(AssertionError):self.fetch([b'abd',b'abc'])
  self.assertEqual(self.calls,1)
 def test_truncated_bytes_are_not_accepted(self):
  with self.assertRaises(AssertionError):self.fetch([b'ab'])
 def test_oversize_is_not_accepted(self):
  with self.assertRaises(AssertionError):self.fetch([b'abcd'])
 def test_no_alternate_source(self):
  self.source['source_emitted_download_url']='https://example.org/photo.jpg'
  with self.assertRaises(AssertionError):self.fetch([b'abc'])
  self.assertEqual(self.calls,0)
if __name__=='__main__':unittest.main()
