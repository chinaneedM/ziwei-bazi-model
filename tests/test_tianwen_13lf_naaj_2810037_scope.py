import copy,importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/verify-tianwen-13lf-naaj-2810037-scope.py"
spec=importlib.util.spec_from_file_location("tw13lf",p);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class LocatorScope(unittest.TestCase):
    def setUp(self):self.args=copy.deepcopy(list(v.load()))
    def bad(self):
        with self.assertRaises(AssertionError):v.check(*self.args)
    def test_base(self):self.assertEqual(v.check(*self.args)["status"],"PASS")
    def test_no_invented_original(self):self.args[0]["file_directory"]["printed_numeral_read_from_2810037"]=True;self.bad()
    def test_no_unproved_chapter(self):self.args[0]["file_directory"]["exact_chapter_to_book_mapping_proved"]=True;self.bad()
    def test_no_1739_date(self):self.args[0]["holding"]["exact_impression_1739_proved"]=True;self.bad()
    def test_no_stemma_vote(self):self.args[0]["comparisons"]["independent_textual_recension_votes_new"]=1;self.bad()
    def test_future_focus_compatible(self):
        self.args[1]["historical_audit"]["current_focus"].append("13LG next leaf original proof")
        self.args[2]["binding"]["source_focus_count"]+=1
        self.args[2]["binding"]["latest_research_focus_prefix"]="13LG"
        next(x for x in self.args[2]["issues"] if x["id"]=="TW-OPEN-0005")["next_action"]="13LG CURRENT ACTION: staged"
        self.assertEqual(v.check(*self.args)["status"],"PASS")
if __name__=="__main__":unittest.main()
