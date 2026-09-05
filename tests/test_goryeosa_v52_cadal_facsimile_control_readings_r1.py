from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"docs"/"research"/"GORYEOSA-V52-CADAL-FACSIMILE-CONTROL-READINGS-R1.json"

class GoryeosaV52CadalFacsimileControlReadingsR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data=json.loads(PATH.read_text(encoding="utf-8"))
        cls.controls={x["control_id"]:x for x in cls.data["controls"]}

    def test_probe_is_no_ocr_and_bound_to_exact_public_facsimile(self) -> None:
        self.assertEqual(self.data["source_id"],"EXT-COMMONS-CADAL-GORYEOSA-V52-FACSIMILE")
        self.assertEqual(self.data["source_internal_identity"],"高麗史卷五十二·志第六·曆三")
        self.assertEqual(self.data["page_count"],151)
        self.assertEqual(self.data["djvu_embedded_text_pages"],0)
        self.assertFalse(self.data["ocr_used"])
        self.assertEqual(self.data["reproduction"]["workflow_run_id"],33968138492)
        self.assertEqual(self.data["reproduction"]["artifact_id"],9970086664)

    def test_current_variant_surfaces_and_pages_are_directly_bound(self) -> None:
        expected={
            "VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE":(39,"五分一三六二"),
            "VAR-NUM-LUNAR-L8-LOSSGAIN":(81,"一十〇分五六〇一七七五"),
            "NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING":(112,"五度二十四八一一二五"),
            "VAR-NUM-LUNAR-L114-DAYRATE":(117,"九日三四八九"),
            "VAR-NUM-LUNAR-L124-JI-XINGDU":(120,"一度〇八二一"),
            "VAR-NUM-LUNAR-L132-LOSSGAIN":(123,"七分八八六七五"),
        }
        for cid,(page,surface) in expected.items():
            self.assertEqual(self.controls[cid]["scan_page"],page)
            self.assertEqual(self.controls[cid]["direct_surface"],surface)

    def test_same_copy_symmetric_zero_controls_are_preserved(self) -> None:
        self.assertEqual(self.controls["SYM-LUNAR-L35-LOSSGAIN-ZERO"]["scan_page"],90)
        self.assertEqual(self.controls["SYM-LUNAR-L35-LOSSGAIN-ZERO"]["direct_surface"],"七分八八六〇七五")
        self.assertEqual(self.controls["SYM-LUNAR-L67-CHIJI-DEGREE-ZERO"]["scan_page"],101)
        self.assertEqual(self.controls["SYM-LUNAR-L67-CHIJI-DEGREE-ZERO"]["direct_surface"],"五度二十〇四八一一二五")
        self.assertEqual(self.controls["NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING"]["normalized_value"],"5.20481125")
        self.assertEqual(self.controls["VAR-NUM-LUNAR-L132-LOSSGAIN"]["normalized_value"],"NOT_FORCED")

    def test_epistemic_boundaries_block_overclaim(self) -> None:
        b=self.data["epistemic_boundaries"]
        self.assertEqual(b["cadal_copy_as_15c_goryeosa_original"],"FORBIDDEN")
        self.assertEqual(b["cadal_copy_as_g893_equivalent"],"FORBIDDEN")
        self.assertEqual(b["l114_as_proven_krdb_transcription_error_before_krdb_scan"],"FORBIDDEN")
        self.assertEqual(b["direct_page_reading_as_transmission_cause_adjudication"],"FORBIDDEN")
        self.assertEqual(b["algorithm_or_runtime_selection_effect"],"NONE")

if __name__=="__main__":
    unittest.main()
