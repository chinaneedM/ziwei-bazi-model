from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "research" / "MING-DATONG-1569-CROSS-EDITION-VARIANT-LEDGER-R1.json"


class MingDatong1569CrossEditionVariantLedgerR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data=json.loads(LEDGER.read_text(encoding="utf-8"))
        cls.variants={v["id"]:v for v in cls.data["numeric_variant_controls"]}

    def test_primary_ming_layer_is_closed_and_never_overwritten(self) -> None:
        primary=self.data["primary_reference"]
        self.assertEqual(primary["solar_primary_collation"],"185_OF_185_DIRECT_ZERO_VARIANTS_ZERO_AMBIGUOUS")
        self.assertEqual(primary["lunar_chiji_primary_collation"],"169_OF_169_DIRECT_ZERO_VARIANTS_ZERO_AMBIGUOUS")
        self.assertEqual(primary["lunar_xingdu_primary_collation"],"169_OF_169_DIRECT_ZERO_VARIANTS_ZERO_AMBIGUOUS")
        self.assertFalse(self.data["primary_ming_numeric_layer_changed_by_cross_witness_variants"])
        self.assertEqual(self.data["epistemic_firewalls"]["cross_regional_source_as_ming_edition_authority"],"FORBIDDEN")

    def test_structural_variants_do_not_collapse_terminology_or_schema(self) -> None:
        ids={v["id"] for v in self.data["structural_variants"]}
        self.assertEqual(ids,{"VAR-STRUCT-SOLAR-001","VAR-STRUCT-LUNAR-001"})
        self.assertEqual(
            self.data["structural_variants"][0]["philological_disposition"],
            "TERMINOLOGY_AND_TABLE_SCHEMA_VARIANT; DO_NOT_DECLARE 消息分 AND 日差加一秒... FULLY_IDENTICAL_WITHOUT_EXPLICIT_BRIDGE",
        )
        self.assertEqual(self.data["epistemic_firewalls"]["similar_numeric_series_as_automatic_term_equivalence"],"FORBIDDEN")

    def test_limit_124_live_goryeosa_value_is_10821_not_previous_project_00821(self) -> None:
        v=self.variants["VAR-NUM-LUNAR-L124-JI-XINGDU"]
        self.assertEqual(v["ming_1569_primary"],"1.0281")
        self.assertEqual(v["krdb_goryeosa_current_transcript"],"1.0821")
        self.assertEqual(v["wikisource_goryeosa_current_transcript"],"1.0821")
        self.assertEqual(v["krdb_r_original_image_entry_reading_layer"],"1.0821")
        self.assertFalse(v["propagate_to_ming_primary"])

    def test_db_specific_limit_114_error_is_distinguished_from_shared_variant(self) -> None:
        v=self.variants["VAR-NUM-LUNAR-L114-DAYRATE"]
        self.assertEqual(v["ming_1569_primary"],"9日3489")
        self.assertEqual(v["wikisource_goryeosa_current_transcript"],"9日3489")
        self.assertEqual(v["krdb_goryeosa_current_transcript"],"9日2489")
        self.assertEqual(v["krdb_r_original_image_entry_reading_layer"],"9日3489")
        self.assertEqual(v["classification"],"KRDB_O_VIEW_TRANSCRIPTION_LAYER_ERROR_STRONGLY_INDICATED")

    def test_limit_8_and_solar_day16_are_not_silently_normalized(self) -> None:
        l8=self.variants["VAR-NUM-LUNAR-L8-LOSSGAIN"]
        self.assertEqual(l8["ming_1569_primary"],"10.561775")
        self.assertEqual(l8["wikisource_goryeosa_current_transcript"],"10.5601775")
        self.assertEqual(l8["krdb_r_original_image_entry_reading_layer"],"10.5601775")
        s16=self.variants["VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE"]
        self.assertEqual(s16["ming_1569_primary"],"5.2362")
        self.assertEqual(s16["krdb_goryeosa_current_transcript"],"5.1362")
        self.assertEqual(s16["krdb_r_original_image_entry_reading_layer"],"5.1362")
        self.assertEqual(s16["wikisource_goryeosa_value"],"5.1362")
        self.assertEqual(s16["classification"],"SHARED_CROSS_REGIONAL_RECEIVED_OR_DIGITAL_VARIANT")

    def test_ledger_remains_open_until_image_and_exhaustive_comparison_complete(self) -> None:
        self.assertFalse(self.data["exhaustive_cross_witness_row_comparison_complete"])
        self.assertFalse(self.data["image_level_variant_cause_adjudication_complete"])
        self.assertEqual(self.data["current_variant_count"],4)
        self.assertEqual(self.data["epistemic_firewalls"]["digital_transcript_difference_as_manuscript_variant_without_image"],"FORBIDDEN")
        self.assertEqual(self.data["epistemic_firewalls"]["krdb_r_reading_layer_as_direct_original_image_glyph"],"FORBIDDEN")
        self.assertTrue(self.data["reading_layer_comparison_complete_for_current_controls"])
        self.assertEqual(self.data["current_classification_summary"]["shared_cross_regional_received_or_digital_variant_count"],3)
        self.assertEqual(self.data["current_classification_summary"]["krdb_o_view_transcription_layer_error_strongly_indicated_count"],1)
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["general_calendar_arithmetic_certified"])


if __name__=="__main__":
    unittest.main()
