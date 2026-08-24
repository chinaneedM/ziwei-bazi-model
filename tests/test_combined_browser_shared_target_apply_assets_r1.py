from __future__ import annotations

import unittest

from fortune_training.combined_chart_application.shared_apply_assets import (
    SHARED_APPLY_JS,
    shared_apply_index_html,
)


class CombinedBrowserSharedTargetApplyAssetsR1Tests(unittest.TestCase):
    def test_assets_are_additive_and_explicitly_opt_in(self) -> None:
        html = shared_apply_index_html("<html><head></head><body><main>x</main></body></html>")
        self.assertIn('/shared-apply.css', html)
        self.assertIn('/shared-apply.js', html)
        self.assertIn('id="resolve-shared-ziwei-projection"', SHARED_APPLY_JS)
        self.assertIn('id="apply-shared-ziwei-projection" disabled', SHARED_APPLY_JS)
        self.assertIn("calculateButton.addEventListener('click', calculateProjection)", SHARED_APPLY_JS)
        self.assertIn("applyButton.addEventListener('click', applyProjection)", SHARED_APPLY_JS)

    def test_calculation_never_writes_ziwei_selectors_or_invokes_apply(self) -> None:
        calculate = SHARED_APPLY_JS.split("async function calculateProjection()", 1)[1].split(
            "function applyProjection()", 1
        )[0]
        self.assertNotIn("daxianNav.value =", calculate)
        self.assertNotIn("annualNav.value =", calculate)
        self.assertNotIn("monthNav.value =", calculate)
        self.assertNotIn("minorNav.value =", calculate)
        self.assertNotIn("applyProjection()", calculate)
        self.assertIn("fetch('/api/shared-ziwei-projection'", calculate)

    def test_multi_candidate_never_auto_selects_candidate_zero(self) -> None:
        self.assertIn("candidateSelect.value = rows.length === 1 ? '0' : ''", SHARED_APPLY_JS)
        self.assertIn("if (rows.length > 1)", SHARED_APPLY_JS)
        self.assertIn("请选择候选", SHARED_APPLY_JS)
        self.assertNotIn("projection.candidates[0]", SHARED_APPLY_JS)
        self.assertNotIn("new Set", SHARED_APPLY_JS)
        self.assertNotIn(".filter((row", SHARED_APPLY_JS)

    def test_apply_uses_server_returned_four_selectors_and_existing_change_path(self) -> None:
        apply_block = SHARED_APPLY_JS.split("function applyProjection()", 1)[1].split(
            "candidateSelect.addEventListener", 1
        )[0]
        self.assertIn("daxianNav.value = row.daxian_frame_id || ''", apply_block)
        self.assertIn("annualNav.value = String(row.annual_year)", apply_block)
        self.assertIn("monthNav.value = row.monthly_projection_status", apply_block)
        self.assertIn("minorNav.value = String(row.minor_limit_age)", apply_block)
        self.assertIn("annualNav.dispatchEvent(new Event('change'", apply_block)
        self.assertNotIn("fetch('/api/ziwei-interaction'", SHARED_APPLY_JS)
        self.assertNotIn("ziwei-daxian-frame-id').value =", SHARED_APPLY_JS)
        self.assertNotIn("ziwei-annual-year').value =", SHARED_APPLY_JS)
        self.assertNotIn("ziwei-minor-limit-age').value =", SHARED_APPLY_JS)

    def test_apply_never_rewrites_target_or_bazi_fields(self) -> None:
        forbidden_assignments = (
            "target-datetime').value =",
            "target-place').value =",
            "target-latitude').value =",
            "target-longitude').value =",
            "target-timezone-id').value =",
            "target-precision').value =",
            "target-uncertainty-seconds').value =",
            "target-temporal-profile').value =",
            "bazi-natal-profile').value =",
            "bazi-temporal-profile').value =",
            "bazi-dayun-count').value =",
        )
        for assignment in forbidden_assignments:
            with self.subTest(assignment=assignment):
                self.assertNotIn(assignment, SHARED_APPLY_JS)

    def test_daily_fact_and_hourly_candidates_are_read_only_and_visible(self) -> None:
        self.assertIn("daily_projection=${row.daily_projection_status}", SHARED_APPLY_JS)
        self.assertIn("daily_transformations=${row.daily_transformation_status}", SHARED_APPLY_JS)
        self.assertIn("row.daily_designation_overlay.map", SHARED_APPLY_JS)
        self.assertIn("候选命宫=${hour.active_address_branch}", SHARED_APPLY_JS)
        self.assertIn("daily_auxiliary=${row.daily_auxiliary_status}", SHARED_APPLY_JS)
        self.assertIn("hour.auxiliary_activations.map", SHARED_APPLY_JS)
        self.assertIn("流昌曲=", SHARED_APPLY_JS)
        self.assertIn("流魁钺候选=", SHARED_APPLY_JS)
        self.assertIn("CANDIDATES_PRESERVED_NO_SELECTION", SHARED_APPLY_JS)
        self.assertIn("row.hourly_method_candidates.map", SHARED_APPLY_JS)
        self.assertIn("hour.transformations.map", SHARED_APPLY_JS)
        self.assertIn("CANDIDATES_PRESERVED_NO_SELECTED_FRAME", SHARED_APPLY_JS)
        apply_block = SHARED_APPLY_JS.split("function applyProjection()", 1)[1].split(
            "candidateSelect.addEventListener", 1
        )[0]
        self.assertNotIn("daily_frame_id", apply_block)
        self.assertNotIn("hourly_method_candidates", apply_block)

    def test_birth_and_target_edits_invalidate_projection(self) -> None:
        for field_id in (
            "birth-datetime",
            "birth-place",
            "latitude",
            "longitude",
            "timezone-id",
            "sex",
            "precision",
            "uncertainty-seconds",
            "ziwei-daxian-count",
            "ziwei-lunar-month",
            "target-datetime",
            "target-place",
            "target-latitude",
            "target-longitude",
            "target-timezone-id",
            "target-precision",
            "target-uncertainty-seconds",
        ):
            with self.subTest(field_id=field_id):
                self.assertIn(f"'{field_id}'", SHARED_APPLY_JS)
        self.assertIn("element.addEventListener('input', invalidateOnEdit)", SHARED_APPLY_JS)
        self.assertIn("element.addEventListener('change', invalidateOnEdit)", SHARED_APPLY_JS)
        self.assertIn("输入已变化；已清除旧 Projection", SHARED_APPLY_JS)

    def test_fresh_ziwei_render_invalidates_old_projection(self) -> None:
        self.assertIn("observer.observe(ziweiRoot, {childList: true, subtree: true})", SHARED_APPLY_JS)
        self.assertIn("紫微显示源已刷新；旧 Projection 已失效", SHARED_APPLY_JS)
        self.assertIn("displayedSourceFingerprint", SHARED_APPLY_JS)
        self.assertIn("displayedSourceIsCurrent()", SHARED_APPLY_JS)

    def test_source_hash_and_candidate_lineage_tamper_are_rejected(self) -> None:
        self.assertIn("responseLineageIsConsistent(data)", SHARED_APPLY_JS)
        self.assertIn(
            "data.source_ziwei_bundle_hash !== projection.source_ziwei_application_bundle_hash",
            SHARED_APPLY_JS,
        )
        self.assertIn(
            "data.target_coordinate_fact_hash !== projection.source_target_coordinate_fact_hash",
            SHARED_APPLY_JS,
        )
        self.assertIn(
            "data.target_coordinate_computation_hash !== projection.source_target_coordinate_computation_hash",
            SHARED_APPLY_JS,
        )
        self.assertIn("row.source_target_candidate_index === index", SHARED_APPLY_JS)
        self.assertIn("row.candidate_hash.length === 64", SHARED_APPLY_JS)
        self.assertIn("Projection source/hash lineage 不一致", SHARED_APPLY_JS)

    def test_browser_contains_no_ziwei_temporal_mapping_or_bazi_reinterpretation(self) -> None:
        forbidden_algorithm_fragments = (
            "nominal_age",
            "parent_daxian_frame_id",
            "absolute_year",
            "local_apparent_solar_datetime",
            "year_boundary_policy",
            "day_boundary_policy",
            "late_zi",
            "sexagenary",
            "jiaoyun",
            "hourly_frame",
        )
        lowered = SHARED_APPLY_JS.lower()
        for fragment in forbidden_algorithm_fragments:
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, lowered)
        self.assertIn("row.annual_year", SHARED_APPLY_JS)
        self.assertIn("row.minor_limit_age", SHARED_APPLY_JS)
        self.assertIn("row.daxian_frame_id", SHARED_APPLY_JS)
        self.assertIn("row.source_annual_frame_id", SHARED_APPLY_JS)
        self.assertIn("row.effective_lunar_month", SHARED_APPLY_JS)
        self.assertIn("row.monthly_projection_status", SHARED_APPLY_JS)

    def test_leap_month_projection_is_not_silently_applied_as_regular_month(self) -> None:
        self.assertIn("LEAP_MONTH_UNRESOLVED_NO_FRAME", SHARED_APPLY_JS)
        self.assertIn("闰月，常规流月保持未选", SHARED_APPLY_JS)
        self.assertIn(": '';", SHARED_APPLY_JS)


if __name__ == "__main__":
    unittest.main()
