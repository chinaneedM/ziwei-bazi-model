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
        self.assertEqual(v["krdb_r_korean_normalized_rendering"],"1.0821")
        self.assertFalse(v["propagate_to_ming_primary"])

    def test_limit_114_o_surface_divergence_is_not_promoted_to_proven_transcription_error(self) -> None:
        v=self.variants["VAR-NUM-LUNAR-L114-DAYRATE"]
        self.assertEqual(v["ming_1569_primary"],"9日3489")
        self.assertEqual(v["wikisource_goryeosa_current_transcript"],"9日3489")
        self.assertEqual(v["krdb_goryeosa_current_transcript"],"9日2489")
        self.assertEqual(v["krdb_r_korean_normalized_rendering"],"9日3489")
        self.assertEqual(v["classification"],"KRDB_O_TEXT_SURFACE_DIVERGENCE_R_NORMALIZATION_AND_WIKISOURCE_ALIGN_WITH_MING")

    def test_limit_8_and_solar_day16_are_not_silently_normalized(self) -> None:
        l8=self.variants["VAR-NUM-LUNAR-L8-LOSSGAIN"]
        self.assertEqual(l8["ming_1569_primary"],"10.561775")
        self.assertEqual(l8["wikisource_goryeosa_current_transcript"],"10.5601775")
        self.assertEqual(l8["krdb_r_korean_normalized_rendering"],"10.5601775")
        s16=self.variants["VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE"]
        self.assertEqual(s16["ming_1569_primary"],"5.2362")
        self.assertEqual(s16["krdb_goryeosa_current_transcript"],"5.1362")
        self.assertEqual(s16["krdb_r_korean_normalized_rendering"],"5.1362")
        self.assertEqual(s16["wikisource_goryeosa_value"],"5.1362")
        self.assertEqual(s16["classification"],"SHARED_CROSS_REGIONAL_RECEIVED_OR_DIGITAL_VARIANT")

    def test_limit_132_is_variant_but_not_force_normalized(self) -> None:
        v=self.variants["VAR-NUM-LUNAR-L132-LOSSGAIN"]
        self.assertEqual(v["ming_1569_primary_normalized"],"7.886075")
        self.assertEqual(v["krdb_o_exact_surface"],"七分八八六七五")
        self.assertEqual(v["krdb_r_korean_normalized_surface"],"7″88‴67''''5'''''")
        self.assertEqual(v["wikisource_exact_surface"],"七分八八六七五")
        self.assertEqual(v["symmetric_control_limit_35"]["krdb_o_exact_surface"],"七分八八六〇七五")
        self.assertEqual(v["symmetric_control_limit_35"]["ming_1569_primary_normalized"],"7.886075")
        self.assertEqual(v["normalized_cross_witness_value"],"NOT_FORCED_PENDING_PLACE_VALUE_AND_IMAGE_ADJUDICATION")
        self.assertEqual(v["classification"],"SHARED_CROSS_REGIONAL_RECEIVED_OR_DIGITAL_VARIANT")
        self.assertFalse(v["propagate_to_ming_primary"])

    def test_limit_101_compact_surface_is_a_philological_bridge_not_a_variant(self) -> None:
        controls=self.data["philological_normalization_controls"]
        self.assertEqual(len(controls),1)
        c=controls[0]
        self.assertEqual(c["id"],"NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING")
        self.assertEqual(c["ming_1569_primary_normalized"],"5.20481125")
        self.assertEqual(c["krdb_o_surface"],"五度二十四八一一二五")
        self.assertEqual(c["explicit_place_groups"],["5","20","48","11","25"])
        self.assertEqual(c["krdb_r_korean_normalized_surface"],"5′20″48‴11''''25'''''")
        self.assertEqual(c["symmetric_control_limit_67"]["krdb_o_surface"],"五度二十〇四八一一二五")
        self.assertEqual(c["symmetric_control_limit_67"]["ming_1569_primary_normalized"],"5.20481125")
        self.assertEqual(c["classification"],"SURFACE_NOTATION_DIFFERENCE_SAME_MECHANICAL_VALUE")
        self.assertEqual(c["variant_count_effect"],0)
        self.assertEqual(self.data["epistemic_firewalls"]["compact_han_numeric_surface_as_simple_decimal_digits"],"FORBIDDEN")
        self.assertEqual(self.data["epistemic_firewalls"]["philological_normalization_bridge_as_numeric_variant"],"FORBIDDEN")
        self.assertFalse(self.data["krdb_evidence_layers"]["r_korean_translation_or_normalized_rendering"]["independent_textual_witness"])
        self.assertFalse(self.data["krdb_evidence_layers"]["r_korean_translation_or_normalized_rendering"]["direct_original_image_glyph_inspection"])

    def test_early_physical_shoushi_witness_is_bound_without_prepopulated_readings(self) -> None:
        source="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893"
        witnesses={w["source_id"]:w for w in self.data["comparison_witnesses"]}
        self.assertIn(source,witnesses)
        self.assertEqual(witnesses[source]["direct_target_image_status"],"PENDING_FOLIO_BINDING")
        adjudication=self.data["independent_physical_image_adjudication"]
        self.assertEqual(adjudication["source_id"],source)
        self.assertEqual(adjudication["status"],"SOURCE_LOCATED_TARGET_FOLIOS_NOT_YET_BOUND")
        self.assertEqual(len(adjudication["targets"]),6)
        self.assertTrue(all(t["target_reading_status"]=="PENDING_DIRECT_IMAGE" for t in adjudication["targets"]))
        self.assertEqual(
            adjudication["no_prepopulation_rule"],
            "NO_NUMERIC_VALUE_MAY_BE_ENTERED_FOR_G893_BEFORE_DIRECT_TARGET_IMAGE_READING",
        )
        self.assertEqual(
            self.data["epistemic_firewalls"]["catalog_original_image_availability_as_direct_target_glyph_reading"],
            "FORBIDDEN",
        )
        self.assertEqual(
            self.data["epistemic_firewalls"]["earlier_cross_regional_physical_witness_as_ming_1569_edition_authority"],
            "FORBIDDEN",
        )

    def test_ledger_remains_open_until_image_and_exhaustive_comparison_complete(self) -> None:
        self.assertFalse(self.data["exhaustive_cross_witness_row_comparison_complete"])
        self.assertFalse(self.data["image_level_variant_cause_adjudication_complete"])
        self.assertEqual(self.data["current_variant_count"],5)
        self.assertEqual(self.data["epistemic_firewalls"]["digital_transcript_difference_as_manuscript_variant_without_image"],"FORBIDDEN")
        self.assertEqual(self.data["epistemic_firewalls"]["krdb_r_normalized_rendering_as_independent_textual_witness"],"FORBIDDEN")
        self.assertEqual(self.data["epistemic_firewalls"]["krdb_r_normalized_rendering_as_direct_original_image_glyph"],"FORBIDDEN")
        self.assertTrue(self.data["reading_layer_comparison_complete_for_current_controls"])
        self.assertEqual(self.data["current_classification_summary"]["shared_cross_regional_received_or_digital_variant_count"],4)
        self.assertEqual(self.data["current_classification_summary"]["krdb_o_text_surface_divergence_pending_image_adjudication_count"],1)
        self.assertEqual(self.data["current_classification_summary"]["philological_same_mechanical_value_bridge_count"],1)
        self.assertEqual(self.data["philological_normalization_control_count"],1)
        self.assertFalse(self.data["runtime_selection_authorized"])
        self.assertFalse(self.data["general_calendar_arithmetic_certified"])


if __name__=="__main__":
    unittest.main()
