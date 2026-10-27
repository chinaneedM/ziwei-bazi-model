from __future__ import annotations

import unittest

from fortune_training.combined_chart_application.local_app import (
    APP_JS,
    INDEX_HTML,
    STYLE_CSS,
)


class CombinedSharedTimeUiR1Tests(unittest.TestCase):
    def test_page_exposes_shared_time_identity_and_full_export(self) -> None:
        for element_id in (
            "shared-time-status",
            "shared-time-hash",
            "shared-time-panel",
            "shared-time-facts",
            "candidate-lineage-status",
            "download-combined",
        ):
            self.assertIn(f'id="{element_id}"', INDEX_HTML)
        self.assertIn("统一时间轴与规则凭证", INDEX_HTML)
        self.assertIn("同一物理时间底座", INDEX_HTML)

    def test_renderer_keeps_ziwei_and_bazi_conventions_visibly_separate(self) -> None:
        self.assertIn("function renderSharedTime(credential,lineage)", APP_JS)
        self.assertIn("['紫微换日',policies.ziwei?.day_boundary_policy", APP_JS)
        self.assertIn("['八字换日',policies.bazi?.bazi_day_boundary_policy", APP_JS)
        self.assertIn("['八字晚子时',policies.bazi?.bazi_late_zi_hour_stem_policy", APP_JS)
        self.assertIn("候选联动：${statuses.join(' / ')}", APP_JS)

    def test_complete_combined_export_includes_shared_credential(self) -> None:
        self.assertIn("download('ziwei-bazi-combined-chart.json',last.combined_export)", APP_JS)
        self.assertIn(".shared-time-facts", STYLE_CSS)
        self.assertNotIn("预测结论", APP_JS)

    def test_bazi_classical_fact_annotations_are_visible_without_interpretation(self) -> None:
        self.assertIn("旬空：${p.xunkong?.display_name||'-'}", APP_JS)
        self.assertIn("星运：${p.day_master_twelve_growth?.phase||'-'}", APP_JS)
        self.assertIn("自坐：${p.self_twelve_growth?.phase||'-'}", APP_JS)
        self.assertIn(".pillar .classical-annotations", STYLE_CSS)
        self.assertNotIn("旺衰结论", APP_JS)

    def test_bazi_derived_coordinates_are_visible_as_separate_fact_cards(self) -> None:
        self.assertIn("['胎元',derived.taiyuan]", APP_JS)
        self.assertIn("['命宫',derived.minggong]", APP_JS)
        self.assertIn("['身宫',derived.shengong]", APP_JS)
        self.assertIn(".bazi-derived-card", STYLE_CSS)

    def test_xiaoyun_classical_alternatives_are_visible_without_arbitration(self) -> None:
        self.assertIn("function renderXiaoyun(root,set)", APP_JS)
        self.assertIn("小运候选 · ${candidate.profile_id}", APP_JS)
        self.assertIn("renderXiaoyun(root,view.xiaoyun)", APP_JS)
        self.assertIn(".xiaoyun-candidate", STYLE_CSS)


if __name__ == "__main__":
    unittest.main()
