from __future__ import annotations

import json
import unittest
from decimal import Decimal, ROUND_CEILING, ROUND_DOWN, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "research" / "MING-DATONG-1569-FIXED-POINT-PRECISION-AUDIT-R1.json"
DAY_RATE = ROOT / "docs" / "research" / "MING-DATONG-1569-CHIJI-DAY-RATE-COLUMN-R1.json"
LUNAR_FULL = ROOT / "docs" / "research" / "MING-DATONG-1569-CHIJI-FULL-NUMERIC-RECONSTRUCTION-R1.json"
CHIJI_PRIMARY = ROOT / "docs" / "research" / "MING-DATONG-1569-LUNAR-CHIJI-PRIMARY-COLLATION-LEDGER-R1.json"
XINGDU_PRIMARY = ROOT / "docs" / "research" / "MING-DATONG-1569-LUNAR-XINGDU-PRIMARY-COLLATION-LEDGER-R1.json"
SOLAR_FULL = ROOT / "docs" / "research" / "MING-DATONG-1569-YINGSUO-FULL-NUMERIC-RECONSTRUCTION-R1.json"
SOLAR_PRIMARY = ROOT / "docs" / "research" / "MING-DATONG-1569-SOLAR-PRIMARY-COLLATION-LEDGER-R1.json"

class MingDatong1569FixedPointPrecisionAuditR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit=json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.day=json.loads(DAY_RATE.read_text(encoding="utf-8"))
        cls.lunar=json.loads(LUNAR_FULL.read_text(encoding="utf-8"))
        cls.chiji=json.loads(CHIJI_PRIMARY.read_text(encoding="utf-8"))
        cls.xing=json.loads(XINGDU_PRIMARY.read_text(encoding="utf-8"))
        cls.solar=json.loads(SOLAR_FULL.read_text(encoding="utf-8"))
        cls.solar_primary=json.loads(SOLAR_PRIMARY.read_text(encoding="utf-8"))
        cls.lr={r["limit"]:r for r in cls.lunar["rows"]}
        cls.cr={r["limit"]:r for r in cls.chiji["rows"]}
        cls.xr={r["limit"]:r for r in cls.xing["rows"]}
        cls.rules={r["rule_id"]:r for r in cls.audit["table_generation_precision_rules"]}

    def test_scope_and_firewalls(self) -> None:
        self.assertEqual(self.audit["adjudication"]["single_global_rounding_rule"],"REJECTED_BY_PRIMARY_TABLE_EVIDENCE")
        self.assertEqual(self.audit["adjudication"]["table_generation_precision_map"],"CLOSED_FOR_1569_PRIMARY_TABLES")
        self.assertEqual(self.audit["adjudication"]["dynamic_interpolation_and_d1_conjunction_precision"],"OPEN_BEYOND_THE_1596_DATONG_WORKED_EXAMPLE")
        self.assertFalse(self.audit["runtime_selection_authorized"])
        self.assertFalse(self.audit["general_calendar_arithmetic_certified"])

    def test_day_rate_floor_168_of_168(self) -> None:
        half=primary=0
        for r in self.day["rows"]:
            raw=Decimal(r["limit"])*Decimal("820.08")
            target=r["printed_total_day_rate_source_units"]
            self.assertEqual(int(raw.to_integral_value(rounding=ROUND_DOWN)),target)
            half += int(int(raw.to_integral_value(rounding=ROUND_HALF_UP))==target)
            self.assertEqual(self.cr[r["limit"]]["primary_reading"]["day_rate_total_source_units"],target)
            primary+=1
        self.assertEqual((primary,half),(168,90))
        self.assertEqual(self.rules["PREC-DAY-RATE-FLOOR"]["discriminating_against_half_up_count"],78)

    def test_loss_gain_shortcut_truncate_168_of_168(self) -> None:
        q=Decimal("0.0001"); half=primary=0
        for n in range(168):
            r=self.lr[n]
            raw=Decimal(r["loss_gain_source_fen"])*Decimal("100")/Decimal("820")
            target=Decimal(r["loss_gain_shortcut_source_seconds"])
            self.assertEqual(raw.quantize(q,rounding=ROUND_DOWN),target)
            half += int(raw.quantize(q,rounding=ROUND_HALF_UP)==target)
            self.assertEqual(Decimal(self.cr[n]["primary_reading"]["loss_gain_shortcut_source_seconds"]),target)
            primary+=1
        self.assertEqual((primary,half),(168,92))
        self.assertEqual(self.rules["PREC-LOSS-GAIN-SHORTCUT-TRUNCATE"]["discriminating_against_half_up_count"],76)

    def test_line_speed_ceiling_334_generic_cells_plus_two_overrides(self) -> None:
        mean=Decimal("1.09623750"); q=Decimal("0.0001")
        ce=down=half=generic=primary=0
        for n in range(168):
            r=self.lr[n]; adj=Decimal(r["loss_gain_degree"])
            raws={"chi":mean-adj,"ji":mean+adj} if n<=83 else {"chi":mean+adj,"ji":mean-adj}
            for kind,raw in raws.items():
                target=Decimal(r[f"{kind}_xingdu_degree"])
                self.assertEqual(Decimal(self.xr[n]["primary_reading"][f"{kind}_xingdu_degree"]),target)
                primary+=1
                if (n,kind) in {(82,"chi"),(85,"ji")}:
                    continue
                generic+=1
                ce += int(raw.quantize(q,rounding=ROUND_CEILING)==target)
                down += int(raw.quantize(q,rounding=ROUND_DOWN)==target)
                half += int(raw.quantize(q,rounding=ROUND_HALF_UP)==target)
        self.assertEqual((generic,ce,down,half,primary),(334,334,0,154,336))
        self.assertEqual(self.lr[82]["chi_xingdu_degree"],"1.0960")
        self.assertEqual(self.lr[85]["ji_xingdu_degree"],"1.0960")
        self.assertEqual(self.rules["PREC-LINE-SPEED-CEILING"]["discriminating_against_half_up_count"],180)

    def test_xingdu_shortcut_truncate_336_of_336(self) -> None:
        q=Decimal("0.0000001"); half=primary=0
        for n in range(168):
            r=self.lr[n]
            for kind in ("ji","chi"):
                speed_int=int(Decimal(r[f"{kind}_xingdu_degree"])*Decimal("10000"))
                raw=Decimal("820")/Decimal(speed_int)
                target=Decimal(r[f"{kind}_xingdu_shortcut_source_ratio"])
                self.assertEqual(raw.quantize(q,rounding=ROUND_DOWN),target)
                half += int(raw.quantize(q,rounding=ROUND_HALF_UP)==target)
                self.assertEqual(Decimal(self.xr[n]["primary_reading"][f"{kind}_xingdu_shortcut_source_ratio"]),target)
                primary+=1
        self.assertEqual((primary,half),(336,158))
        self.assertEqual(self.rules["PREC-XINGDU-SHORTCUT-TRUNCATE"]["discriminating_against_half_up_count"],178)

    def test_exact_fixed_point_relations_match_primary(self) -> None:
        sf={}
        for fam in self.solar["families"]:
            for r in fam["rows"]:
                sf[(fam["family_id"],r["day_index"])]=r
        counts={"accumulated":[0,0],"add":[0,0],"message":[0,0]}
        fmap={"accumulated":"accumulated_source_table_units","add":"add_source_table_units","message":"message_source_table_units"}
        for p in self.solar_primary["rows"]:
            r=sf[(p["family_id"],p["day_index"])]; pr=p["primary_reading"]
            for label,field in fmap.items():
                if r.get(field) is None or pr.get(field) is None: continue
                counts[label][0]+=1
                self.assertEqual(Decimal(r[field]),Decimal(pr[field]))
                counts[label][1]+=1
        self.assertEqual(counts,{"accumulated":[183,183],"add":[183,183],"message":[181,181]})
        acc=loss=0
        for n,r in self.lr.items():
            pr=self.cr[n]["primary_reading"]
            if r["accumulated_chiji_degree"] is not None and pr["accumulated_chiji_degree"] is not None:
                self.assertEqual(Decimal(r["accumulated_chiji_degree"]),Decimal(pr["accumulated_chiji_degree"])); acc+=1
            if r["loss_gain_source_fen"] is not None and pr["loss_gain_source_fen"] is not None:
                self.assertEqual(Decimal(r["loss_gain_source_fen"]),Decimal(pr["loss_gain_source_fen"])); loss+=1
        self.assertEqual((acc,loss),(167,168))

    def test_later_mei_wending_exegesis_explains_but_does_not_override_primary_precision(self) -> None:
        controls={x["control_id"]:x for x in self.audit["later_explanatory_precision_controls"]}
        c=controls["MEI-WENDING-DATONG-LIZHI-V4-LINE-SPEED-PRECISION"]
        self.assertEqual(c["source_id"],"EXT-WIKISOURCE-DATONG-LIZHI-V4")
        self.assertEqual(c["authority_role"],"LATER_EXPLANATORY_WITNESS_NOT_1569_PRIMARY_AUTHORITY")
        self.assertIn("秒以下有零數不拘多少俱收為秒",c["received_wording"])
        self.assertIn("布立成法：秒以下數不用",c["received_wording"])
        self.assertFalse(c["use_to_override_primary"])
        self.assertFalse(c["runtime_authority"])

    def test_dynamic_controls_remain_scoped(self) -> None:
        c={x["control_id"]:x for x in self.audit["dynamic_worked_precision_controls"]}
        self.assertEqual(c["DATONG-1596-V49-LOCAL-TRUNCATION"]["printed_add_correction_source_units"],"1526.64")
        self.assertEqual(c["DATONG-1596-V49-LOCAL-TRUNCATION"]["generalization_status"],"LOCAL_DATONG_WORKED_EXAMPLE_ONLY")
        self.assertFalse(c["SHOUSHI-1605-V50-PRECISION-WIDTH-CONTROL"]["datong_authority"])
        self.assertEqual(self.audit["epistemic_firewalls"]["table_generation_precision_as_dynamic_interpolation_precision"],"FORBIDDEN")

if __name__=="__main__":
    unittest.main()
