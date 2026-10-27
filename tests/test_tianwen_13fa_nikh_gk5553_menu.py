import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'scripts'/'verify-tianwen-13fa-nikh-gk5553-menu.py'
s=importlib.util.spec_from_file_location('v13fa',p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Test13FA(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.d=v.get(v.E);cls.s=v.get(v.SH);cls.m=v.get(v.M);cls.st=v.get(v.ST);cls.l=v.get(v.L)
 def good(self,d=None):return v.check(self.d if d is None else d,self.s,self.m,self.st,self.l)
 def bad(self,f):
  d=copy.deepcopy(self.d);f(d)
  with self.assertRaises(AssertionError):self.good(d)
 def test_valid(self):self.assertTrue(self.good())
 def test_fake_original_glyph(self):self.bad(lambda x:x['target_native_menu'].update(original_glyph_reading='五'))
 def test_fake_image_sha(self):self.bad(lambda x:x['target_native_menu'].update(original_image_bytes_sha256='0'*64))
 def test_fake_viewer_execution(self):self.bad(lambda x:x['target_native_menu'].update(onclick_executed=True))
 def test_false_ko21634_target_option(self):self.bad(lambda x:x['target_native_menu'].update(any_KO21634_menu_entry_proven_at_target=True))
 def test_wrong_physical_book(self):self.bad(lambda x:x['kyujanggak_catalog'].update(juan52_to_physical_book=52))
 def test_catalog_wrong_print_date(self):self.bad(lambda x:x['kyujanggak_catalog'].update(catalog_print_year=1455))
 def test_lose_manuscript_exception(self):self.bad(lambda x:x['kyujanggak_catalog'].update(notable_replacement_physical_books=[]))
 def test_fake_ancient_vote(self):self.bad(lambda x:x['impact'].update(new_historic_glyph_votes=1))
 def test_reopen_algorithm(self):self.bad(lambda x:x['impact'].update(algorithm_reopens=1))
 def test_current_gk5553_shelfmark_alias(self):
  q=copy.deepcopy(self.l);risk=next(x for x in q['issues'] if x['id']=='TW-OPEN-0005')
  self.assertIn('GK5553',risk['next_action'])
  risk['next_action']=risk['next_action'].replace('GK5553','GK05553_00')
  self.assertTrue(v.check(self.d,self.s,self.m,self.st,q))
 def test_unbound_gk5553_shelfmark_rejected(self):
  q=copy.deepcopy(self.l);risk=next(x for x in q['issues'] if x['id']=='TW-OPEN-0005')
  risk['next_action']=risk['next_action'].replace('GK05553_00','UNBOUND_COPY').replace('GK5553','UNBOUND_COPY')
  with self.assertRaises(AssertionError):v.check(self.d,self.s,self.m,self.st,q)
if __name__=='__main__':unittest.main()
