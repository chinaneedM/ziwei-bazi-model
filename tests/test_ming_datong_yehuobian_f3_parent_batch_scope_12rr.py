"""12RR: parent batch identity and stage state are different semantic fields.

The historical parent is 12QE, whereas the open stage is 12QE_OPEN.
Prevent an accidental 'parent_batch == stage' shortcut in F3 native evidence gates.
"""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATES = {
    "12RL": "verify_yehuobian_nlc_f3_p21_40_native_12rl.py",
    "12RM": "verify_yehuobian_nlc_f3_p41_60_native_12rm.py",
    "12RN": "verify_yehuobian_nlc_f3_mixed_juan7_12rn.py",
    "12RO": "verify_yehuobian_nlc_f3_p61_80_native_12ro.py",
    "12RP": "verify_yehuobian_nlc_f3_p85_104_native_12rp.py",
}

def load_gate(batch, script):
    spec = importlib.util.spec_from_file_location("parent_scope_" + batch.lower(), ROOT / "scripts" / script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class TestYehuobianF3ParentStageScope12RR(unittest.TestCase):
    def test_all_five_real_evidence_records_pass(self):
        for batch, script in GATES.items():
            with self.subTest(batch=batch):
                gate = load_gate(batch, script)
                self.assertEqual(gate.verify()["batch"], batch)

    def check_tamper(self, field, value):
        for batch, script in GATES.items():
            with self.subTest(batch=batch, field=field):
                gate = load_gate(batch, script)
                rec = copy.deepcopy(gate.read(gate.RECORD))
                self.assertEqual(rec["parent_open_batch"], "12QE")
                self.assertEqual(rec["stage"], "12QE_OPEN")
                rec[field] = value
                with tempfile.TemporaryDirectory() as folder:
                    path = Path(folder) / "mutated.json"
                    path.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "DRIFT"):
                        gate.verify(record_path=path)

    def test_wrong_parent_is_rejected(self):
        self.check_tamper("parent_open_batch", "12QE_OPEN")

    def test_closed_stage_is_rejected(self):
        self.check_tamper("stage", "12QE")

if __name__ == "__main__":
    unittest.main()
