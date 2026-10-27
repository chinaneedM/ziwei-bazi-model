from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"docs"/"research"/"GORYEOSA-V52-KRDB-DIRECT-IMAGE-CONTROL-R1.json"

class GoryeosaV52KrdbDirectImageControlR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data=json.loads(PATH.read_text(encoding="utf-8"))
        cls.control=cls.data["controls"][0]

    def test_direct_control_is_exact_krdb_image_and_no_ocr(self) -> None:
        self.assertEqual(self.data["source_id"],"EXT-KRDB-GORYEOSA-V52-SHOUSHI-LICHENG")
        self.assertEqual(self.data["viewer_level_id"],"kr_052_0010_0010_0020")
        self.assertFalse(self.data["ocr_used"])
        self.assertFalse(self.data["original_image_committed_to_repository"])
        self.assertEqual(self.data["reproduction"]["workflow_run_id"],33971921953)
        self.assertEqual(self.data["reproduction"]["artifact_id"],9971177420)

    def test_l114_is_bound_by_printed_heading_and_direct_surface(self) -> None:
        self.assertEqual(self.data["page_localization"]["image_no"],1116)
        self.assertEqual(self.data["page_localization"]["printed_limit_headings"],["一百十四","一百十五","一百十六"])
        self.assertEqual(self.control["krdb_direct_image_surface"],"九日三四八九")
        self.assertEqual(self.control["krdb_o_transcription_surface"],"九日二四八九")
        self.assertEqual(self.control["finding"],"KRDB_O_TRANSCRIPTION_ERROR_CONFIRMED_BY_KRDB_OWN_UNDERLYING_SCAN")
        self.assertEqual(self.control["transmission_variant_effect"],"NONE_FOR_THE_2489_O_SURFACE")

    def test_page_mapping_and_authority_firewalls_are_preserved(self) -> None:
        self.assertEqual(self.data["page_mapping_correction"]["fixed_offset_as_evidence"],"FORBIDDEN")
        self.assertEqual(self.data["epistemic_boundaries"]["fixed_cross_copy_scan_offset_as_page_identity"],"FORBIDDEN")
        self.assertEqual(self.data["epistemic_boundaries"]["cadal_surface_alone_as_krdb_transcription_error_proof"],"FORBIDDEN")
        self.assertEqual(self.data["epistemic_boundaries"]["direct_l114_scan_as_other_control_glyph_proof"],"FORBIDDEN")
        self.assertEqual(self.data["epistemic_boundaries"]["algorithm_or_runtime_selection_effect"],"NONE")

if __name__=="__main__":
    unittest.main()
