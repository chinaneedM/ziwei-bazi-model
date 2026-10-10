"""Regression gates for 12PZ physical-copy identity and source scope.

These tests distinguish copies, digital files, editions, historical chronology,
and deterministic charting. They do not assert a universal old20v target reading.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs" / "research"
LEDGER = RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-PRIMARY-WITNESS-BOUNDARY-LEDGER-R1.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class Yehuobian12PZWitnessBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = load(LEDGER)
        cls.by_id = {v["id"]: v for v in cls.ledger["witnesses"]}
        cls.original = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-NCL02260-PART2-RECEIVED-XUBIAN12-DIRECT-HEADING-R1.json")
        cls.shanghai = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-SHANGHAI30-GAIZAO-LOUKE-P441-P442-DIRECT-COLLATION-R1.json")
        cls.official = load(RESEARCH / "ZIWEI-YINGZONG-SHILU-1447-NANJING-59-41-PHYSICAL-COLLATION-R1.json")
        cls.variants = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-NCL02260-02261-PHYSICAL-PREFACE-BINGWU-BINGCHEN-DIRECT-COMPARISON-R1.json")

    def test_disjoint_material_copy_keys_not_digital_segment_count(self) -> None:
        self.assertEqual(len(self.by_id), len(self.ledger["witnesses"]))
        copies = [x["copy_key"] for x in self.ledger["witnesses"]]
        self.assertEqual(len(set(copies)), 5)
        a = self.by_id["TAIWAN_NCL02260_OLD20_MANUSCRIPT"]
        self.assertEqual(len(a["digital_parts"]), 2)
        self.assertEqual([x["pdf_pages"] for x in a["digital_parts"]], [1000, 35])
        self.assertEqual(a["counts_for_shen_defu_old20v_target"], 0)
        self.assertEqual(self.by_id["TAIWAN_NCL02261_GREEN_GRID_OLD20"]["counts_for_shen_defu_old20v_target"], 0)

    def test_exact_runner_pdf2_hash_and_facing_page_indices_are_source_scoped(self) -> None:
        physical = self.by_id["TAIWAN_NCL02260_OLD20_MANUSCRIPT"]
        self.assertEqual(physical["digital_parts"][1]["pdf_sha256"], self.original["source"]["source_sha256"])
        workflow = self.original["workflow_attestation_20261010"]
        self.assertEqual(workflow["run_conclusion"], "success")
        self.assertEqual(workflow["downloaded_pdf"]["pdf_pages"], 35)
        self.assertEqual(workflow["downloaded_pdf"]["sha256"], physical["digital_parts"][1]["pdf_sha256"])
        checksums = {x["pdf_page_1based"]: x["rendered_jpeg_sha256"] for x in workflow["derived_images"]}
        self.assertEqual(set(checksums), {3, 4, 5, 6})
        self.assertEqual(len(set(checksums.values())), 4)
        self.assertEqual(self.original["followup_source_page_pair_20261010"]["observed_pdf_page_1based_4"]["reading"], "萬曆野獲續編卷第十二目")
        self.assertEqual(self.original["followup_source_page_pair_20261010"]["observed_pdf_page_1based_5"]["reading"], "萬曆野獲續編卷第十二")
        self.assertFalse(workflow["artifact_zip_sha256_independently_downloaded_and_recomputed"])

    def test_1447_memorial_is_one_preexisting_official_primary_record(self) -> None:
        official = self.by_id["CHINA_NLC_YINGZONG_SHILU_V160_1447"]
        self.assertEqual(official["source_pdf_sha256"], self.official["physical_source"]["source_pdf_sha256"])
        self.assertEqual(official["target_pdf_pages_1based"], [28])
        self.assertEqual(self.official["secure_direct_reading"]["beijing_winter"], "冬至日出辰初一刻，入申正二刻，夜刻六十二")
        self.assertEqual(self.official["secure_direct_reading"]["imperial_response"], "上令內官監改造")
        self.assertEqual(sum(x["counts_for_1447_official_record"] for x in self.ledger["witnesses"]), 1)
        self.assertIn("clock construction completion", official["does_not_prove"])

    def test_shanghai_30v_physical_glyph_is_not_1827_print_or_old20(self) -> None:
        shanghai = self.by_id["SHANGHAI_REORGANIZED_30V_MANUSCRIPT"]
        self.assertEqual(shanghai["source_pdf_sha256"], self.shanghai["witness"]["source_pdf_sha256"])
        self.assertEqual(shanghai["target_pdf_pages_1based"], [441, 442])
        self.assertEqual(self.shanghai["physical_pages"][0]["visible_heading"], "改造漏刻")
        field = {x["field"]: x["source_text"] for x in self.shanghai["field_collation"]}
        self.assertEqual(field["BEIJING_WINTER_SUNRISE"], "辰初一刻")
        self.assertEqual(field["PALACE_CLOCK_ADOPTION"], "時禁中宮漏循用新製不待言")
        self.assertEqual(self.shanghai["witness"]["source_1827_fulishanfang_equivalence"], "NOT_PROVEN")
        self.assertEqual(sum(x.get("counts_for_reorganized_30v_target", 0) for x in self.ledger["witnesses"]), 1)
        self.assertEqual(sum(x["counts_for_shen_defu_old20v_target"] for x in self.ledger["witnesses"]), 0)

    def test_two_manuscript_prefaces_are_distinct_not_a_genealogy(self) -> None:
        ids = {x["witness_id"]: x["direct_year_glyphs"] for x in self.variants["source_witnesses"]}
        self.assertEqual(ids, {"NCL-02260": "丙午", "NCL-02261": "丙辰"})
        self.assertEqual(self.variants["comparison"]["physical_witness_count"], 2)
        self.assertEqual(self.variants["comparison"]["inferred_independent_textual_lineages"], "NOT_ESTABLISHED")
        self.assertEqual(sum(x.get("counts_for_old20_preface_variant", 0) for x in self.ledger["witnesses"]), 2)

    def test_gates_and_unresolved_original_are_never_auto_promoted(self) -> None:
        missing = {x["target"] for x in self.ledger["not_yet_collated"]}
        self.assertIn("original old20 改造漏刻 heading and folio", missing)
        self.assertIn("edition/copy-identified 1827 扶荔山房 print physical target leaf", missing)
        gate = self.ledger["gates"]
        self.assertFalse(gate["batch_closed"])
        self.assertFalse(gate["chart_algorithm_changed"])
        self.assertFalse(gate["matrix_changed"])
        self.assertEqual(gate["deterministic_product_r1"], "CLOSED")
        self.assertEqual(gate["md_g03"], "OPEN_BLOCKING_GENERAL_ADAPTER")
        self.assertEqual(gate["hpa_dayun_cal_002"], "MISSING_FROM_PRODUCT")
        self.assertTrue(self.ledger["prohibitions"]["original20v_equivalent_to_categorized30v_volume20"] is False)

    def test_distinct_china_nlc_v20_tail_has_source_digest_not_target_vote(self) -> None:
        china = self.by_id["CHINA_NLC_411999003250_OLD20_FASCICLE10"]
        evidence = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-CHINA-NLC411999003250-V20-TAIL-SOURCE-DIGEST-R1.json")
        self.assertEqual(evidence["source"]["pdf_sha256"], china["source_pdf_sha256"])
        self.assertEqual(evidence["acquisition"]["run_conclusion"], "success")
        self.assertEqual(evidence["source"]["pdf_pages"], 145)
        self.assertEqual(len(evidence["rendered_pages"]), 10)
        self.assertEqual([p["pdf_page_1based"] for p in evidence["rendered_pages"]], list(range(136, 146)))
        self.assertEqual(evidence["preexisting_direct_page_read"]["pdf_page_1based"], 137)
        self.assertTrue(evidence["scope"]["manually_collated_all_ten_pages"])
        self.assertEqual(evidence["scope"]["old20_kaizao_louke_present_or_absent"], "NOT_IDENTIFIED_AS_HEADING_IN_P136_TO_P145_ONLY_BROADER_UNRESOLVED")
        self.assertEqual(china["counts_for_shen_defu_old20v_target"], 0)

    def test_wikimedia_imageinfo_independently_confirms_pdf2_source_binary(self) -> None:
        attestation = self.original["commons_imageinfo_independent_verification_20261010"]
        self.assertTrue(attestation["comparison_pass"])
        self.assertEqual(attestation["commons_sha1_hex"], self.original["source"]["source_sha1"])
        self.assertEqual(attestation["commons_size_bytes"], self.original["workflow_attestation_20261010"]["downloaded_pdf"]["size_bytes"])
        self.assertEqual(attestation["source_physical_witness_number_added"], 0)



    def test_two_distinct_old20_volume20_structures_from_sha_pinned_images(self) -> None:
        evidence = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-NLC-TAIWAN-OLD20-V20-DIRECT-COMPARE-R1.json")
        china = evidence["china_nlc"]
        taiwan = evidence["taiwan_ncl02260"]
        self.assertEqual(china["p137"]["heading"], "萬曆肆拾伍丁巳卷二十")
        self.assertEqual(china["p145"]["colophon"], "萬曆野獲編二十卷紀事畢")
        self.assertEqual(taiwan["manual_toc_heading"], "萬曆野獲編卷第二十目")
        self.assertEqual(taiwan["p592_jpeg_sha256"], "f173d98c6ee32aba342ade6b377094f333871345c357284fc4f27a2d819942a2")
        self.assertTrue(evidence["comparison"]["different_volume20_structure"])
        self.assertEqual(evidence["comparison"]["independent_old20_target_glyph_count_delta"], 0)
        self.assertEqual(evidence["comparison"]["direct_copying_relation"], "NOT_PROVEN")
        self.assertEqual(china["bounded_review"]["negative_scope"], "P136_TO_P145_ONLY_NOT_THE_WHOLE_BOOK")

    def test_prior_p137_heading_is_corrected_with_forward_only_history(self) -> None:
        cross = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-OLD20-VOLUME-HEADING-CROSSWALK-R1.json")
        actual = next(x for x in cross["volume_heading_evidence"] if x["volume"] == 20)
        self.assertEqual(actual["heading"], "萬曆肆拾伍丁巳卷二十")
        self.assertEqual(actual["physical_colophon_p145"], "萬曆野獲編二十卷紀事畢")
        # Forward-only history is append-only: locate this correction by type,
        # never by array position (later digest backfills are legitimate).
        corrections = [
            item for item in cross["revision_history"]
            if item.get("type") == "CORRECT_PRIOR_PROJECT_GENERIC_VOLUME20_HEADING_FROM_ACTUAL_P137_GLYPH"
        ]
        self.assertEqual(len(corrections), 1)
        correction = corrections[0]
        self.assertEqual(correction["previous_value"], "萬曆野獲編卷二十")
        self.assertEqual(correction["corrected_value"], actual["heading"])
        self.assertEqual(correction["new_external_metadata_defect_count"], 0)
        self.assertEqual(cross["next_proof"]["old20_gaizao_louke_heading_to_leaf"], "UNRESOLVED")



    def test_12pz_postcollation_scope_fields_reconcile_forward_only(self) -> None:
        china = self.by_id["CHINA_NLC_411999003250_OLD20_FASCICLE10"]
        digest = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-CHINA-NLC411999003250-V20-TAIL-SOURCE-DIGEST-R1.json")
        cross = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-OLD20-VOLUME-HEADING-CROSSWALK-R1.json")
        self.assertTrue(digest["scope"]["manually_collated_all_ten_pages"])
        self.assertTrue(china["bounded_ten_page_visual_review_pass"])
        self.assertNotIn("the last ten PDF pages have all been glyph-reviewed", china["does_not_prove"])
        self.assertIn("a full character-by-character transcription of all ten reviewed PDF pages", china["does_not_prove"])
        self.assertTrue(china["physical_heading_revision_20261010"]["not_an_old20_target_leaf_collation"])
        self.assertTrue(digest["preexisting_direct_page_read"]["previous_reading_is_superseded_as_literal_glyph"])
        self.assertEqual(digest["preexisting_direct_page_read"]["corrected_literal_page137_reading"], "萬曆肆拾伍丁巳卷二十")
        self.assertEqual(china["physical_heading_revision_20261010"]["corrected_literal_page137"], "萬曆肆拾伍丁巳卷二十")
        self.assertEqual(cross["source"]["original_pdf_sha256"], china["source_pdf_sha256"])
        self.assertEqual(cross["digest_reconciliation_20261010"]["source_sha256"], digest["source"]["pdf_sha256"])
        self.assertIsNone(cross["revision_history"][-1]["previous_value"])
        self.assertEqual(sum(w["counts_for_shen_defu_old20v_target"] for w in self.ledger["witnesses"]), 0)
        self.assertFalse(self.ledger["gates"]["batch_closed"])


    def test_china_nlc_ten_fascicle_catalog_routes_cover_labels_not_source_glyphs(self) -> None:
        bundle = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-CHINA-NLC-OLD20-TEN-FASCICLE-PUBLIC-DIGITAL-ROUTE-CROSSWALK-R1.json")
        fascicles = bundle["fascicles"]
        self.assertEqual(len(fascicles), 10)
        self.assertEqual([f["fascicle"] for f in fascicles], list(range(1, 11)))
        self.assertEqual(sorted(v for f in fascicles for v in f["volume_numbers_in_commons_file_description"]), list(range(1, 21)))
        self.assertEqual(sum(f["public_pdf_pages"] for f in fascicles), 1030)
        self.assertEqual(len({f["file_id"] for f in fascicles}), 10)
        self.assertEqual(bundle["distinct_physical_copy_count_in_this_collection"], 1)
        self.assertEqual([f["fascicle"] for f in fascicles if f["source_pdf_sha256"] is not None], [10])
        self.assertEqual(fascicles[-1]["source_pdf_sha256"], self.by_id["CHINA_NLC_411999003250_OLD20_FASCICLE10"]["source_pdf_sha256"])
        self.assertEqual(bundle["mechanical_scope"]["old20_target_kaizao_louke_leaf"], "UNRESOLVED")
        self.assertFalse(bundle["mechanical_scope"]["complete_manuscript_page_inventory_and_target_locator"])
        self.assertEqual(self.ledger["digital_collection_index_20261010"]["reported_volume_labels"], 20)
        registry = load(ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
        item = next(s for s in registry["sources"] if s["source_id"] == "EXT-COMMONS-NLC411999003250-YEHUOBIAN-TEN-FASCICLE-ROUTES")
        self.assertFalse(item["physical_glyph_authority"])
        self.assertFalse(self.ledger["gates"]["batch_closed"])


    def test_1827_printed_alternate_copy_routes_do_not_promote_glyph_witness(self) -> None:
        routes = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-1827-PRINTED-RECORD-AND-BERLIN-IIIF-ROUTE-R1.json")
        ids = {r["item_id"] for r in routes["printed_copy_routes"]}
        self.assertEqual(ids, {"TOKYO_OMOKI_1827_V20", "HOKKAIDO_1827_V19_20", "BERLIN_1827_SAMPLES"})
        self.assertEqual(next(r for r in routes["printed_copy_routes"] if r["item_id"] == "TOKYO_OMOKI_1827_V20")["target_item_number"], "6403767830")
        self.assertEqual(next(r for r in routes["printed_copy_routes"] if r["item_id"] == "HOKKAIDO_1827_V19_20")["target_item_number"], "0181427762")
        berlin = next(r for r in routes["printed_copy_routes"] if r["item_id"] == "BERLIN_1827_SAMPLES")
        self.assertEqual(berlin["ppn"], "PPN334378186X")
        self.assertEqual(berlin["volume20_target_page_in_samples"], "UNDETERMINED")
        self.assertFalse(berlin["target_leaf_image_acquired"])
        self.assertEqual(routes["authority_scope"]["independent_full_printed_target_collations_added"], 0)
        self.assertEqual(routes["gates"]["original_target_glyph_count_delta"], 0)
        self.assertEqual(self.ledger["printed_1827_alternative_copies_20261010"]["original_target_glyph_witness_count_increment"], 0)
        registry = load(ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
        expected = {
            "EXT-CINII-BC0492354X-YEHUOBIAN-1827-TOKYO-DAIMOKU-V20",
            "EXT-CINII-BB10385966-YEHUOBIAN-1827-HOKKAIDO-V19V20",
            "EXT-SBB-DDB-PPN334378186X-YEHUOBIAN-1827-BERLIN-SAMPLES"
        }
        actual = [s for s in registry["sources"] if s["source_id"] in expected]
        self.assertEqual({s["source_id"] for s in actual}, expected)
        self.assertTrue(all(s["physical_glyph_authority"] is False for s in actual))
        self.assertFalse(self.ledger["gates"]["batch_closed"])


    def test_berlin_ppn_manifest_canvases_are_only_sample_metadata(self) -> None:
        record = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-1827-PRINTED-RECORD-AND-BERLIN-IIIF-ROUTE-R1.json")
        berlin = next(x for x in record["printed_copy_routes"] if x["item_id"] == "BERLIN_1827_SAMPLES")
        run = record["workflow_attestation_20261010"]
        self.assertTrue(berlin["manifest_object_verified"])
        self.assertEqual(berlin["public_iiif_manifest_canvas_count"], 38)
        self.assertEqual(run["manifest_canvases"], 38)
        self.assertEqual(run["manifest_status"], 200)
        self.assertEqual(run["mets_status"], 200)
        self.assertEqual(run["run_conclusion"], "success")
        self.assertEqual(run["artifact_id"], 11662685894)
        self.assertFalse(run["individual_canvas_images_downloaded"])
        self.assertFalse(run["target_glyphs_observed"])
        self.assertFalse(record["authority_scope"]["individual_sample_image_glyphs_reviewed"])
        self.assertEqual(record["authority_scope"]["original_1827_target_text_glyph_count"], 0)
        self.assertEqual(berlin["volume20_target_page_in_samples"], "UNDETERMINED")
        self.assertFalse(record["gates"]["batch_closed"])


    def test_temporary_tokyo_access_route_does_not_count_as_physical_leaf(self) -> None:
        record = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-1827-PRINTED-RECORD-AND-BERLIN-IIIF-ROUTE-R1.json")
        access = record["tokyo_public_first_party_access_control_20261010"]
        self.assertIn("BC0492354X", access["item_scope"])
        self.assertEqual(access["external_action_boundary"], "NO_REPRODUCTION_OR_VIEWING_APPLICATION_SUBMITTED")
        self.assertEqual(access["number_of_target_glyphs_observed"], 0)
        self.assertIn("OBJECT_SPECIFIC_IMAGE_AND_COPY_ELIGIBILITY_UNRESOLVED", access["status"])
        self.assertFalse(record["gates"]["batch_closed"])


    def test_berlin_twelve_of_thirty_eight_original_images_not_printed_target(self) -> None:
        sample = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-BERLIN-38-SAMPLES-12-DIRECT-IMAGE-COLLATION-R1.json")
        self.assertEqual(sample["manifest_canvas_count"], 38)
        self.assertEqual(sample["reviewed_canvas_count"], 12)
        self.assertEqual(sample["reviewed_canvas_indices"], [1,11,13,17,19,23,25,27,29,31,33,38])
        self.assertEqual(len(sample["canvas_originals"]), 12)
        self.assertEqual(len({s["source_sha256"] for s in sample["canvas_originals"]}), 12)
        self.assertTrue(all(len(s["source_sha256"]) == 64 for s in sample["canvas_originals"]))
        self.assertTrue(all(s["status"] == "IMAGE_RETRIEVED_SOURCE_EXPLICIT" for s in sample["canvas_originals"]))
        self.assertEqual(sample["run_conclusion"], "success")
        self.assertEqual(sample["bounded_adjudication"]["remaining_unreviewed_manifest_canvases"], 26)
        self.assertFalse(sample["bounded_adjudication"]["target_heading_identified_in_reviewed_twelve"])
        self.assertFalse(sample["bounded_adjudication"]["entire_1827_print_negative_claim_allowed"])
        self.assertEqual(sample["bounded_adjudication"]["historical_target_text_glyph_count_increment"], 0)
        self.assertEqual(self.ledger["berlin_1827_bounded_image_review_20261010"]["reviewed_original_jpeg_canvases"], 12)
        evidence = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-1827-PRINTED-RECORD-AND-BERLIN-IIIF-ROUTE-R1.json")
        self.assertFalse(next(x for x in evidence["printed_copy_routes"] if x["item_id"] == "BERLIN_1827_SAMPLES")["target_leaf_image_acquired"])
        self.assertEqual(evidence["gates"]["original_target_glyph_count_delta"], 0)
        self.assertFalse(self.ledger["gates"]["batch_closed"])


    def test_berlin_all_thirty_eight_source_jpegs_close_only_sample_scope(self) -> None:
        full = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-BERLIN-38-OF-38-SAMPLE-IMAGE-CLOSURE-R1.json")
        self.assertEqual(full["manifest_canvas_count"], 38)
        self.assertEqual(full["source_original_images_human_reviewed"], 38)
        self.assertEqual(full["all_canvas_indexes"], list(range(1,39)))
        images = full["all_original_jpegs_source_sha256"]
        self.assertEqual(len(images), 38)
        self.assertEqual(len({p["sha256"] for p in images}), 38)
        self.assertTrue(all(len(p["sha256"]) == 64 for p in images))
        self.assertEqual(sum(x["source_original_jpg_count"] for x in full["runs"]), 38)
        self.assertTrue(full["bounded_target_adjudication"]["reviewed_all_38_public_sample_canvases"])
        self.assertFalse(full["bounded_target_adjudication"]["kaizao_louke_heading_identified_in_any_38"])
        self.assertFalse(full["bounded_target_adjudication"]["entire_1827_print_negative_claim_allowed"])
        self.assertEqual(full["bounded_target_adjudication"]["historical_target_glyph_count_increment"], 0)
        self.assertEqual(self.ledger["berlin_1827_all_sample_image_review_20261010"]["images"], 38)
        self.assertFalse(self.ledger["gates"]["batch_closed"])

    def test_korea_cnts_1700_catalog_year_cannot_date_print_or_prove_lineage(self) -> None:
        korea = load(RESEARCH / "MING-DATONG-YEHUOBIAN-12PZ-KOREA-CNTS-00047974753-PART1-EDITION-IDENTITY-R1.json")
        self.assertEqual(korea["source_pdf_pages"], 118)
        self.assertEqual(korea["source_pdf_size_bytes"], 32023702)
        self.assertEqual(len(korea["source_pdf_sha256"]), 64)
        self.assertEqual(korea["source_pdf_sha256"], "94c127f857ad2e0b5eef2e167eccaca3c2ad275bfcbdcdd67bc61ca8990bde96")
        self.assertEqual(korea["manual_images_reviewed"], [1,2,3])
        self.assertEqual(korea["catalog_display_year"], "1700")
        self.assertTrue(korea["catalog_display_year_must_not_be_promoted_to_ancient_print_date"])
        self.assertFalse(korea["comparative_titlepage"]["direct_same_woodblock_lineage_proven"])
        self.assertFalse(korea["comparative_titlepage"]["direct_same_edition_impression_proven"])
        self.assertFalse(korea["gates"]["batch_closed"])


if __name__ == "__main__":
    unittest.main()
