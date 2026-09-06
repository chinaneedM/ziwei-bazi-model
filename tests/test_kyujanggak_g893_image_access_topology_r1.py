from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"docs"/"research"/"KYUJANGGAK-G893-IMAGE-ACCESS-TOPOLOGY-R1.json"

class KyujanggakG893ImageAccessTopologyR1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data=json.loads(PATH.read_text(encoding="utf-8"))

    def test_catalog_exposes_concrete_image_filename_surface_without_target_binding(self) -> None:
        self.assertEqual(self.data["source_id"],"EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893")
        self.assertEqual(self.data["book_cd"],"GK00893_00")
        self.assertEqual(self.data["item_cd"],"SIC")
        self.assertFalse(self.data["ocr_used"])
        self.assertFalse(self.data["target_glyphs_read"])
        self.assertFalse(self.data["direct_target_folio_bound"])
        files=[x["image_file"] for x in self.data["catalog_exposed_thumbnail_links"]]
        self.assertEqual(files,["GK00893_00IH_0001_000a.jpg","GK00893_00IH_0001_004b.jpg"])

    def test_access_topology_cannot_be_promoted_to_glyph_evidence(self) -> None:
        b=self.data["epistemic_boundaries"]
        self.assertEqual(b["thumbnail_filename_as_target_folio_binding"],"FORBIDDEN")
        self.assertEqual(b["sample_thumbnail_as_target_glyph_reading"],"FORBIDDEN")
        self.assertEqual(b["filename_volume_token_as_textual_volume_proof"],"FORBIDDEN")
        self.assertIn("FORBIDDEN_UNLESS_THE_TARGET_GLYPH_ITSELF_IS_VISIBLE_AND_BOUND",b["secondary_article_figure_as_target_glyph_authority"])
        self.assertIn("CURRENT_FIGURE_ONLY_LOCALIZES_NON_TARGET_OPENING_SOLAR_PAGE",b["secondary_article_figure_as_target_glyph_authority"])
        self.assertEqual(b["algorithm_or_runtime_selection_effect"],"NONE")

    def test_documented_renderer_imageservlet_protocol_is_bound_without_claiming_response(self) -> None:
        p=self.data["access_protocol_evidence"]
        self.assertEqual(p["adapter_source"]["repository"],"deweizhu/bookget")
        self.assertEqual(p["adapter_source"]["repository_commit"],"2cdbf6d6c3ce70355a5c4411c0faf3450e9ae877")
        self.assertEqual(p["adapter_source"]["blob_sha"],"d5ebadc1ba11bb35d9205e136599dffa1197708e")
        self.assertEqual(p["image_delivery"]["endpoint"],"https://kyudb.snu.ac.kr/ImageServlet.do")
        candidate=p["g893_protocol_candidate"]
        self.assertEqual(candidate["item_cd"],"SIC")
        self.assertEqual(candidate["book_cd"],"GK00893_00")
        self.assertFalse(candidate["response_observed_in_project"])
        self.assertEqual(candidate["target_folio_effect"],"NONE")
        b=self.data["epistemic_boundaries"]
        self.assertEqual(b["documented_protocol_candidate_as_observed_g893_response"],"FORBIDDEN")
        self.assertEqual(b["modern_download_adapter_as_historical_authority"],"FORBIDDEN")
        self.assertEqual(b["image_url_construction_as_target_glyph_reading"],"FORBIDDEN")

    def test_github_hosted_runner_family_is_exhausted_without_source_inference(self) -> None:
        boundary=self.data["hosted_runner_boundary"]
        self.assertEqual(
            boundary["status"],
            "DO_NOT_REPEAT_EQUIVALENT_GITHUB_HOSTED_TRANSPORTS_ON_ANY_TESTED_OS_FAMILY",
        )
        self.assertEqual(
            boundary["tested_runner_families"],
            ["GITHUB_HOSTED_UBUNTU","GITHUB_HOSTED_MACOS","GITHUB_HOSTED_WINDOWS"],
        )
        attempts=boundary["prior_attempts"]
        self.assertEqual(len(attempts),4)
        self.assertEqual({x["workflow_run_id"] for x in attempts},{33962192868,33962291588,34027558494})
        self.assertTrue(all("RESET" in x["result"] for x in attempts))
        self.assertEqual(
            boundary["inference"],
            "GITHUB_HOSTED_NETWORK_BOUNDARY_ONLY_NOT_SOURCE_PAGE_FOLIO_OR_GLYPH_EVIDENCE",
        )

    def test_non_github_success_is_only_a_network_feasibility_control(self) -> None:
        w=self.data["public_non_github_access_witness"]
        self.assertEqual(
            w["source_id"],
            "EXT-WIKIMEDIA-COMMONS-KYUJANGGAK-RENDERER-ACCESS-2026",
        )
        self.assertEqual(w["observed_object"],"Kyujanggak 奎17375 / GK17375_00")
        self.assertFalse(w["same_object_as_g893"])
        self.assertEqual(w["g893_target_folio_effect"],"NONE")
        self.assertEqual(w["g893_target_glyph_effect"],"NONE")
        b=self.data["epistemic_boundaries"]
        self.assertEqual(b["other_kyujanggak_object_renderer_success_as_g893_access_proof"],"FORBIDDEN")
        self.assertEqual(b["other_kyujanggak_object_renderer_success_as_g893_folio_or_glyph_evidence"],"FORBIDDEN")

    def test_mirror_routes_remain_locator_only_and_work_identity_stays_separate(self) -> None:
        self.assertEqual(self.data["schema_version"],"1.4.0")
        routes={x["source_id"]:x for x in self.data["mirror_and_reproduction_routes"]}
        legacy=routes["EXT-LEGACY-KYUJANGGAK-HANMUN-DVD04-CATALOG-2015"]
        self.assertFalse(legacy["actual_file_retrieved"])
        self.assertFalse(legacy["g893_identity_bound"])
        self.assertEqual(legacy["target_folio_effect"],"NONE")
        self.assertEqual(legacy["target_glyph_effect"],"NONE")
        separation=self.data["work_identity_separation_control"]
        self.assertEqual(
            separation["source_id"],
            "EXT-KASI-YU-GYUNG-RO-SEJONG-CALENDAR-PUBLICATION-1997",
        )
        self.assertIn("SEPARATE_BOOKS",separation["finding"])
        self.assertEqual(separation["target_folio_effect"],"NONE")
        self.assertEqual(separation["target_glyph_effect"],"NONE")
        b=self.data["epistemic_boundaries"]
        self.assertEqual(b["legacy_package_catalog_as_g893_copy_identity"],"FORBIDDEN")
        self.assertEqual(b["legacy_package_catalog_as_target_page_or_glyph_evidence"],"FORBIDDEN")
        self.assertEqual(b["kang_bo_jiefa_licheng_as_g893_substitute"],"FORBIDDEN")

    def test_all_six_targets_remain_explicitly_pending(self) -> None:
        self.assertEqual(len(self.data["target_controls"]),6)
        self.assertIn("VAR-NUM-SOLAR-WINTER-D16-DIFFERENCE",self.data["target_controls"])
        self.assertIn("NORM-LUNAR-L101-CHIJI-DEGREE-POSITIONAL-GROUPING",self.data["target_controls"])

if __name__=="__main__":
    unittest.main()
