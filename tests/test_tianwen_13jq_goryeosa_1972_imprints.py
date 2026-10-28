import copy
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/verify-tianwen-13jq-goryeosa-1972-imprints.py"
SPEC = importlib.util.spec_from_file_location("tw_13jq", SCRIPT)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

class TestGoryeosa1972ImprintFirewall(unittest.TestCase):
    def setUp(self):
        self.x = list(mod.load())

    def reject(self):
        with self.assertRaises(AssertionError):
            mod.check(*self.x)

    def test_valid(self):
        self.assertEqual(mod.check(*self.x)["status"], "PASS")

    def test_no_same_1972_imprint_merge(self):
        self.x[0]["adjudication"]["three_volume_asia_and_four_volume_yonsei_must_not_be_merged"] = False
        self.reject()

    def test_no_original_claim_from_catalog(self):
        self.x[0]["catalog_records"][1]["original_folio_examined"] = True
        self.reject()

    def test_no_gk5554_folio_attestation(self):
        self.x[0]["catalog_records"][1]["copy_gk5553_or_gk5554_bound"] = True
        self.reject()

    def test_no_historic_value_promotion(self):
        self.x[0]["adjudication"]["g893_six_target_original_numeric_decisions"] = 1
        self.reject()

    def test_no_ancient_fascicle_fiction(self):
        self.x[0]["adjudication"]["prior_13io_physical_volume29_binding"] = "VERIFIED"
        self.reject()

    def test_prior_state_compatible(self):
        self.x[1]["historical_audit"]["current_focus"].append("13JR later evidence")
        self.x[2]["binding"]["source_focus_count"] += 1
        self.x[2]["binding"]["latest_research_focus_prefix"] = "13JR"
        self.assertEqual(mod.check(*self.x)["status"], "PASS")

    def test_prior_revision_not_deleted(self):
        issue = next(i for i in self.x[2]["issues"] if i["id"] == "TW-OPEN-0005")
        issue["history"] = [rev for rev in issue["history"]
                            if rev.get("revision_id") != "TW-OPEN-0005-13JQ-1972-BIBLIOGRAPHIC-IMPRINT-COLLISION-20261028"]
        self.reject()

    def test_prior_revision_duplicate_rejected(self):
        issue = next(i for i in self.x[2]["issues"] if i["id"] == "TW-OPEN-0005")
        prior = next(rev for rev in issue["history"]
                     if rev.get("revision_id") == "TW-OPEN-0005-13JQ-1972-BIBLIOGRAPHIC-IMPRINT-COLLISION-20261028")
        issue["history"].append(copy.deepcopy(prior))
        self.reject()

    def test_prior_revision_forward_order(self):
        issue = next(i for i in self.x[2]["issues"] if i["id"] == "TW-OPEN-0005")
        prior = next(rev for rev in issue["history"]
                     if rev.get("revision_id") == "TW-OPEN-0005-13JQ-1972-BIBLIOGRAPHIC-IMPRINT-COLLISION-20261028")
        issue["history"].remove(prior)
        issue["history"].append(prior)
        self.reject()

    def test_prefix_drift_rejected(self):
        self.x[2]["binding"]["latest_research_focus_prefix"] = "BAD"
        self.reject()

if __name__ == "__main__":
    unittest.main()
