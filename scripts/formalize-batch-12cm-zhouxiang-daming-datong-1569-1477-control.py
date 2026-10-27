from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-ZHOUXIANG-DAMING-DATONG-1569-1477-COMPUTATION-REPRINT-CONTROL-CM"
PREV_ID = "BATCH-12-ZIWEI-YINGZONG-SHILU-1449-DATONG-OLD-STYLE-RESTORATION-CL"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-ZHOUXIANG-DAMING-DATONG-1569-1477-COMPUTATION-REPRINT-CONTROL-CM.md"
RESEARCH = "docs/research/ZIWEI-ZHOUXIANG-DAMING-DATONG-1569-1477-PHYSICAL-COLLATION-R1.json"
SOURCE_ID = "EXT-KOTENMON-ZHOUXIANG-DAMING-DATONG-VOL6-1569"
SCHOLARSHIP_ID = "EXT-JSTAGE-KOBAYASHI-2014-ZHOUXIANG-DATONG"
RUN_ID = 35009608549
ARTIFACT_ID = 10412298745
ARTIFACT_DIGEST = "sha256:7ba11d497bd40e7683d0429662316e91ac900b60ab5f9f492a10d9d076c3356e"
SOURCE_SHA256 = "4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c"
PAGE_SHA256 = {
    "01": "826b6f828bd2cc71cd4820c1f4d5180a6ae9fa039802db28930a17746d319e1a",
    "07": "6d79a3b51c8d8b291b8826f6df4034f495281ee19dbb9cceb0e330355f75052c",
    "09": "c17b46ad82f9e619c2b90903fa6250d9bc9274e0673a51abed6f579054612010",
    "14": "7389bab8c933cc6b9c3ebd033cb6145769072d0c9521daae1ca57b82b8ed5b56",
    "19": "33db862f8ba5cedd8094d26afb9f2f8656db2ebb6e5e692fee62de607d767257",
    "24": "cbaa75b6dff21f87c7432b790cdb04005b930afa0808e3de0ea5d8a66e3c4453",
    "25": "845144997e9d39c29cb7320cdac2d050d0a07330381f37589b2c79d98bb595e0",
    "33": "502aba602acf14da5d4901c1435d8209927ac018470b57232c85f0d1f86bdec9",
    "42": "61db78a82caffd457eb02acc6e290693f9cfda469acc0d3636ec256fbf009519",
    "43": "f2da7ae2411680e86a75951b5126b184a5218ea32d8578860708f76e55851273",
    "44": "d56ed8b2ade8fd0f219ed2ede90d980f5e25626a613d540a4317ccb7115bd4f9",
    "45": "8e6b9beba38161d03d86aa6a1f3c7df3958eb473ac9bf64127c86bd5a887ed55",
}


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate Batch 12CL tail in continuity verifier")
        s = s.replace(needle, f'    "{PREV_ID}",\n    "{BATCH_ID}",\n]', 1)
    latest = f'LATEST_BATCH_DOC = "{BATCH_DOC}"'
    if latest not in s:
        s, n = re.subn(r'^LATEST_BATCH_DOC = ".*"$', latest, s, count=1, flags=re.MULTILINE)
        if n != 1:
            raise SystemExit("cannot update latest batch doc")
    p.write_text(s, encoding="utf-8")


def registry() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    ids = {x.get("source_id") for x in d["sources"]}
    if SOURCE_ID not in ids:
        d["sources"].append({
            "source_id": SOURCE_ID,
            "title": "《大明大統曆法》周相重刊本第6冊公開影像",
            "author_attribution": "周相等重刊；卷內保存前代大統曆計算材料",
            "historical_period": "MING_LONGQING_3_1569_REPRINT_WITH_CHENGHUA_13_1477_CALCULATION_EPOCH",
            "provider": "kotenmon.com public reproduction; physical-copy lineage independently discussed in peer-reviewed scholarship as National Archives of Japan holding",
            "url": "https://www.kotenmon.com/cal/arabe/vol6.pdf",
            "source_role": "DIRECT_NO_OCR_PUBLIC_REPRODUCTION_FOR_1569_REPRINT_AND_1477_CALCULATION_EPOCH_CONTROL",
            "quality_notes": "Batch 12CM directly reviews all 45 rendered pages without OCR. Page 1 visibly titles the fascicle 大明大統曆法; page 7 visibly bears 隆慶三年七月 and 周相; page 9 步氣朔卷第一 explicitly computes from 大元至元十八年辛巳 to 大明成化十三年丁酉. No independent 晨昏分/日出入/晝夜刻 table is observed on this finite 45-page public reproduction; that nonattestation is fascicle-scoped only."
        })
    if SCHOLARSHIP_ID not in ids:
        d["sources"].append({
            "source_id": SCHOLARSHIP_ID,
            "title": "小林博行『関訂書』に見られる明代後期の中国・回回暦法研究について",
            "author": "小林博行",
            "publication": "科学史研究 53巻269号 (2014), 85-98",
            "provider": "J-STAGE / 日本科学史学会",
            "url": "https://www.jstage.jst.go.jp/article/jhsj/53/269/53_85/_article/-char/ja",
            "source_role": "PEER_REVIEWED_SECONDARY_PROVENANCE_AND_REPRINT_HYPOTHESIS_CONTROL",
            "quality_notes": "Note 38 identifies the National Archives holding as Zhou Xiang's reprint, says books 1-5 are Huihui li and book 6 appends Daming Datong lifa, notes a Longqing 3 (1569) Zhou Xiang preface and Chenghua 13 (1477) Datong calculation content, and proposes that Zhou Xiang probably reprinted the paired materials associated with Bei Lin. The final direct-reprint ancestry claim remains secondary/probabilistic, not a confirmed graph edge."
        })
    d["access_date"] = "2026-09-16"
    dump(p, d)


def research() -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-ZHOUXIANG-DAMING-DATONG-1569-1477-PHYSICAL-COLLATION-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Does the public reproduction of Zhou Xiang's Longqing-3 Daming Datong lifa preserve a pre-1578 day/night-ke bridge to Sanming, and what date/provenance layers can be established directly?",
        "source_binding": {
            "source_id": SOURCE_ID,
            "secondary_provenance_source_id": SCHOLARSHIP_ID,
            "public_pdf_url": "https://www.kotenmon.com/cal/arabe/vol6.pdf",
            "workflow_run_id": RUN_ID,
            "artifact_id": ARTIFACT_ID,
            "artifact_digest": ARTIFACT_DIGEST,
            "source_pdf_sha256": SOURCE_SHA256,
            "rendered_page_count": 45,
            "ocr_used_for_glyph_claims": False,
            "page_sha256": PAGE_SHA256
        },
        "date_firewall": {
            "work_or_calculation_layer": "Page 9 explicitly uses 大明成化十三年丁酉 (1477) as the calculation epoch paired with 大元至元十八年辛巳.",
            "edition_reprint_layer": "Page 7 visibly bears 隆慶三年七月 (1569) and 周相 in the reprint/prefatory layer.",
            "physical_copy_layer": "Peer-reviewed scholarship identifies the six-book Zhou Xiang reprint as a National Archives of Japan holding; exact current call-number binding is intentionally left unresolved here because public locators conflict.",
            "digital_surrogate_layer": "The reviewed PDF is a modern public reproduction whose PDF metadata creation date is 2019-07-08; this modern date is not the historical edition date.",
            "rule": "1477 calculation epoch, 1569 reprint, physical holding, and 2019 digital surrogate are not collapsed."
        },
        "direct_visual_collation": {
            "page_01": "Cover/title leaf visibly reads 大明大統曆法.",
            "page_07": "Reprint layer visibly contains 隆慶三年七月 and 周相; adjacent material gives 一引相傳姓氏.",
            "page_09": "步氣朔卷第一 directly states 大元至元十八年辛巳為元至 / 大明成化十三年丁酉所距積年共二百九十七算減一用之, followed by calendrical constants.",
            "page_14": "Heading 太陽冬至前後立成卷第二 with numerical solar standing tables.",
            "page_19": "Heading 太陽夏至前後立成卷第四 with numerical solar standing tables.",
            "pages_24_45_scope": "Later leaves contain 曆成, 太陰遲疾, 定朔/月大小/交泛/直宿 and related computation tables; all 45 public pages were visually reviewed through contact sheets with key leaves individually enlarged.",
            "explicit_daynight_table_observed": False,
            "finite_scope_negative": "NO_EXPLICIT_CHENHUN_RICHURU_ZHOUYE_KE_TABLE_OBSERVED_IN_REVIEWED_45_PAGE_PUBLIC_REPRODUCTION_OF_ZHOUXIANG_VOL6",
            "global_absence_claim_authorized": False
        },
        "secondary_scholarship_control": {
            "source_id": SCHOLARSHIP_ID,
            "peer_reviewed_claim": "Kobayashi note 38 identifies the National Archives Zhou Xiang reprint, states that books 1-5 are Huihui li and book 6 is Daming Datong lifa, observes a Longqing 3 (1569) Zhou Xiang preface and Chenghua 13 (1477) Datong calculation content, and argues Zhou Xiang probably reprinted both together from the Bei Lin context.",
            "direct_bei_lin_parent_edge_authorized": False,
            "reason": "The Bei Lin -> Zhou Xiang reprint relation is a scholarly reconstruction (probably), not directly printed dependency evidence on the reviewed fascicle."
        },
        "historical_adjudication": {
            "pre_1578_datong_technical_witness_confirmed": True,
            "1477_computation_epoch_directly_attested": True,
            "1569_reprint_layer_directly_attested": True,
            "target_daynight_ke_bridge_closed": False,
            "sanming_direct_parent_proved": False,
            "value_of_negative": "Closes this specific public fascicle as a false-positive route for the missing day/night table while preserving it as a strong transmission witness for Datong computational material immediately before 1578."
        },
        "transmission_impact": {
            "nodes_added": [
                "DIGITAL-SURROGATE-KOTENMON-ZHOUXIANG-DATONG-VOL6-2019",
                "EDITION-ZHOUXIANG-DAMING-DATONG-LONGQING3-1569",
                "PASSAGE-ZHOUXIANG-VOL6-LONGQING3-1569",
                "PASSAGE-ZHOUXIANG-VOL6-CHENGHUA13-EPOCH-1477"
            ],
            "edges_added": ["TG-E0020", "TG-E0021", "TG-E0022"],
            "edges_rejected_or_unproved": [
                "Bei Lin 1477 -> Zhou Xiang 1569 direct reprint edge remains secondary/probable, not confirmed",
                "Zhou Xiang vol6 -> Sanming 1578 day/night table parent is not established because the target table is not observed in the reviewed fascicle"
            ],
            "unresolved_lineage_questions": [
                "Locate a direct pre-1578 Daitong Tonggui 晨昏分/日出入/晝夜刻 witness.",
                "Locate the daily ladder/change-day rule connecting Nanjing 59-ke continuous tables to Sanming's stepped display."
            ]
        },
        "product_adjudication": {
            "matrix_rule_id": "HPA-ZDATE-006",
            "status": "MISSING_FROM_PRODUCT",
            "upper_zi_to_hai_vote_increment": 0,
            "new_runtime_candidate": False,
            "runtime_winner": False,
            "candidate_collapse": False,
            "confirmed_chart_algorithm_defect_count": 0,
            "algorithm_reopen_count": 0,
            "deterministic_product_state": "CLOSED"
        },
        "next_gate": [
            "Prioritize direct 大統曆通軌/大統曆日通軌 witnesses and the 晨昏分立成 or sunrise/sunset/day-night table family, rather than repeatedly probing Zhou Xiang vol6.",
            "Search pre-1578 annual Datong almanacs and Yang Zan 閑中錄 for Nanjing 59-ke cap plus intra-term change-day fingerprints.",
            "Keep the Batch 12CI quantization/rounding threshold question open until an explicit historical selection rule is found."
        ]
    })


def graph() -> None:
    p = Path("docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    node_ids = {x.get("node_id") for x in d["nodes"]}
    nodes = [
        {
            "node_id": "DIGITAL-SURROGATE-KOTENMON-ZHOUXIANG-DATONG-VOL6-2019",
            "node_type": "DIGITAL_SURROGATE",
            "label": "kotenmon公開《大明大統曆法》第6冊PDF（2019生成）",
            "system_scope": "MING_DATONG_CALENDRICAL_TRANSMISSION",
            "work_composition_date": "MULTILAYERED; DIRECT PAGE 9 USES CHENGHUA_13_1477_CALCULATION_EPOCH",
            "edition_impression_date": "LONGQING_3_1569_REPRINT_LAYER_DIRECTLY_VISIBLE",
            "physical_copy_date": "NAJ_HOLDING_LINEAGE_PER_SECONDARY_SCHOLARSHIP; EXACT_COPY_DATE/CALL_NUMBER_UNRESOLVED",
            "digital_surrogate_date": "PDF_METADATA_2019_07_08",
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        },
        {
            "node_id": "EDITION-ZHOUXIANG-DAMING-DATONG-LONGQING3-1569",
            "node_type": "EDITION",
            "label": "周相重刊《大明大統曆法》隆慶三年1569層",
            "system_scope": "MING_DATONG_CALENDRICAL_TRANSMISSION",
            "work_composition_date": "CONTAINS_EARLIER_CALCULATION_MATERIAL; PAGE9_ANCHOR_1477",
            "edition_impression_date": "LONGQING_3_1569_DIRECT_PAGE7",
            "physical_copy_date": "EXACT_COPY_DATE_UNRESOLVED",
            "digital_surrogate_date": "2019_PUBLIC_REPRODUCTION",
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        },
        {
            "node_id": "PASSAGE-ZHOUXIANG-VOL6-LONGQING3-1569",
            "node_type": "PASSAGE",
            "label": "周相本第6冊p7隆慶三年七月重刊層",
            "system_scope": "MING_DATONG_CALENDRICAL_BIBLIOGRAPHY",
            "date": "LONGQING_3_1569",
            "locator": "public reproduction PDF page 7",
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        },
        {
            "node_id": "PASSAGE-ZHOUXIANG-VOL6-CHENGHUA13-EPOCH-1477",
            "node_type": "PASSAGE",
            "label": "周相本第6冊p9步氣朔：成化十三年丁酉計算紀元",
            "system_scope": "MING_DATONG_CALENDRICAL_COMPUTATION",
            "date": "CHENGHUA_13_1477_CALCULATION_EPOCH",
            "locator": "public reproduction PDF page 9",
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        }
    ]
    for node in nodes:
        if node["node_id"] not in node_ids:
            d["nodes"].append(node)
            node_ids.add(node["node_id"])
    edge_ids = {x.get("edge_id") for x in d["edges"]}
    edges = [
        {
            "edge_id": "TG-E0020",
            "from": "DIGITAL-SURROGATE-KOTENMON-ZHOUXIANG-DATONG-VOL6-2019",
            "relation": "ATTESTS",
            "to": "PASSAGE-ZHOUXIANG-VOL6-LONGQING3-1569",
            "status": "CONFIRMED",
            "confidence": "HIGH",
            "evidence_class": "DIRECT_PUBLIC_REPRODUCTION_NO_OCR",
            "evidence": [RESEARCH],
            "adjudication_batch": BATCH_ID
        },
        {
            "edge_id": "TG-E0021",
            "from": "DIGITAL-SURROGATE-KOTENMON-ZHOUXIANG-DATONG-VOL6-2019",
            "relation": "ATTESTS",
            "to": "PASSAGE-ZHOUXIANG-VOL6-CHENGHUA13-EPOCH-1477",
            "status": "CONFIRMED",
            "confidence": "HIGH",
            "evidence_class": "DIRECT_PUBLIC_REPRODUCTION_NO_OCR",
            "evidence": [RESEARCH],
            "adjudication_batch": BATCH_ID
        },
        {
            "edge_id": "TG-E0022",
            "from": "PASSAGE-ZHOUXIANG-VOL6-LONGQING3-1569",
            "relation": "ATTESTS",
            "to": "EDITION-ZHOUXIANG-DAMING-DATONG-LONGQING3-1569",
            "status": "CONFIRMED",
            "confidence": "HIGH",
            "evidence_class": "DIRECT_EDITION_DATE_LAYER_ON_PUBLIC_REPRODUCTION",
            "evidence": [RESEARCH],
            "adjudication_batch": BATCH_ID
        }
    ]
    for edge in edges:
        if edge["edge_id"] not in edge_ids:
            d["edges"].append(edge)
            edge_ids.add(edge["edge_id"])
    non_edges = d.setdefault("explicit_non_edges", [])
    if not any(x.get("from") == "EDITION-ZHOUXIANG-DAMING-DATONG-LONGQING3-1569" and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE" for x in non_edges):
        non_edges.append({
            "from": "EDITION-ZHOUXIANG-DAMING-DATONG-LONGQING3-1569",
            "relation": "DIRECT_TABLE_PARENT_OF",
            "to": "TABLE-SANMING-1578-DAYNIGHT-KE",
            "status": "UNRESOLVED",
            "reason": "The reviewed 45-page public vol6 reproduction is a genuine pre-1578 Datong technical witness but no independent 晨昏分/日出入/晝夜刻 target table is observed; direct Sanming day/night parentage is therefore not established.",
            "evidence": [RESEARCH]
        })
    d["updated_at"] = "2026-09-16"
    dump(p, d)


def matrix() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next((x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006"), None)
    if row is None:
        raise SystemExit("HPA-ZDATE-006 missing")
    rp = row.setdefault("research_progress", {})
    rp["batch_12cm_zhouxiang_daming_datong_1569_1477_reprint_control"] = {
        "source_ids": [SOURCE_ID, SCHOLARSHIP_ID],
        "direct_public_reproduction_reviewed": True,
        "rendered_page_count": 45,
        "ocr_used_for_glyph_claims": False,
        "longqing3_1569_reprint_layer_direct": True,
        "chenghua13_1477_calculation_epoch_direct": True,
        "explicit_daynight_ke_table_observed_in_reviewed_fascicle": False,
        "negative_scope": "REVIEWED_PUBLIC_VOL6_ONLY",
        "global_absence_claim_authorized": False,
        "direct_sanming_parent_proved": False,
        "upper_zi_to_hai_vote_increment": 0,
        "runtime_winner_selected": False,
        "candidate_collapsed": False,
        "algorithm_reopen_authorized": False,
        "transmission_impact_recorded": True,
        "research_artifact": RESEARCH
    }
    dump(p, d)


def matrix_md() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md")
    s = p.read_text(encoding="utf-8")
    if "## Progress — Batch 12CM" not in s:
        s += dedent(f'''

        ## Progress — Batch 12CM

        - A public reproduction of Zhou Xiang's `《大明大統曆法》` book 6 was fetched and all `45` pages were rendered/reviewed without OCR (run `{RUN_ID}`, artifact `{ARTIFACT_ID}`, source SHA-256 `{SOURCE_SHA256}`).
        - Direct page-level collation separates the date layers: p7 visibly bears `隆慶三年七月` (1569) and Zhou Xiang's reprint layer, while p9 `步氣朔卷第一` explicitly computes to `大明成化十三年丁酉` (1477). The modern PDF surrogate is dated 2019 and is not collapsed into either historical date.
        - The fascicle is a strong pre-1578 Datong technical-transmission witness: p14/p19 preserve solar winter/summer standing tables and later leaves preserve lunar/朔 and related computational tables. However, no independent `晨昏分 / 日出入 / 晝夜刻` table was observed within the finite 45-page public reproduction.
        - That nonattestation is strictly fascicle-scoped. It closes Zhou Xiang vol6 as a direct target-table shortcut, not the wider Datong tradition. The next gate moves to direct `大統曆通軌/日通軌` 晨昏立成, pre-1578 annual almanacs, and `閑中錄`.
        - `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; no runtime candidate, winner, candidate collapse, chart algorithm defect, or algorithm reopen is created.

        Batch document: `{BATCH_DOC}`. Research record: `{RESEARCH}`.
        ''')
    p.write_text(s, encoding="utf-8")


def state() -> None:
    p = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    h = d["historical_audit"]
    if BATCH_ID not in h["completed_batches"]:
        h["completed_batches"].append(BATCH_ID)
    h["latest_batch_doc"] = BATCH_DOC
    additions = [
        "Batch 12CM directly reviews all 45 pages of Zhou Xiang's public Daming Datong lifa vol6 reproduction without OCR: page 7 binds the Longqing-3/1569 reprint layer, while page 9 directly uses Chenghua-13/1477 as the Datong calculation epoch.",
        "Batch 12CM closes a false-positive bridge route: the reviewed Zhou Xiang vol6 contains substantial Datong solar/lunar computational tables but no independent 晨昏分/日出入/晝夜刻 table was observed. This is a fascicle-scoped nonattestation only, not a global Datong-tradition absence claim.",
        "Next Sanming ancestry gate shifts to direct 大統曆通軌/大統曆日通軌 晨昏立成 witnesses, pre-1578 annual Datong almanacs, and Yang Zan 閑中錄; the daily ladder/change-day and Batch 12CI quantization-rule questions remain open."
    ]
    for x in additions:
        if x not in h["current_focus"]:
            h["current_focus"].append(x)
    d["schema_version"] = "1.99.0"
    d["updated_at"] = "2026-09-16"
    dump(p, d)


def write_doc() -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit — Batch 12CM

    ## Scope

    This batch tests a high-value pre-1578 route opened after Batch 12CL: Zhou Xiang's Longqing-3 `《大明大統曆法》` book 6. The question is whether this surviving technical witness directly preserves the missing Nanjing/day-night-ke bridge to the 1578 `《三命通會》` display.

    The result is a useful scope correction: the witness is genuine and chronologically close, but the reviewed public fascicle does **not** expose the target day/night-ke table. The batch therefore records a positive transmission/date control plus a strictly fascicle-scoped nonattestation. Deterministic charting remains closed.

    ## 1. Direct acquisition and no-OCR review

    GitHub Actions run `{RUN_ID}` downloaded `https://www.kotenmon.com/cal/arabe/vol6.pdf`, SHA-256 `{SOURCE_SHA256}`, rendered all 45 pages, and emitted artifact `{ARTIFACT_ID}` (`{ARTIFACT_DIGEST}`). The visual collation uses the rendered page images; OCR is not admitted for glyph claims.

    ## 2. Four-layer date firewall

    Direct review separates the historical layers rather than collapsing them:

    ```text
    p7   隆慶三年七月 ... 周相              -> 1569 reprint/prefatory layer
    p9   步氣朔卷第一
         大元至元十八年辛巳為元至
         大明成化十三年丁酉所距積年...      -> 1477 calculation epoch
    copy National Archives holding lineage       -> exact current call number/copy date unresolved here
    PDF  modern public surrogate, metadata 2019 -> digital-surrogate layer only
    ```

    The direct p9 wording is especially important: `1477` is not back-calculated from a modern scholar; the public facsimile itself states `大明成化十三年丁酉` as the calculation epoch. Conversely, that does **not** prove every textual layer was first composed in 1477.

    Peer-reviewed control: Kobayashi (2014), note 38, identifies the National Archives Zhou Xiang reprint, states that books 1–5 contain `回回暦法` while book 6 appends `《大明大統曆法》`, notes the Longqing-3/1569 preface and Chenghua-13/1477 calculation content, and proposes that Zhou Xiang probably reprinted the paired material associated with Bei Lin. The final Bei-Lin→Zhou-Xiang dependency remains a scholarly hypothesis, not a confirmed graph edge.

    ## 3. What the 45-page fascicle actually contains

    Direct visual review finds a dense technical calendrical compilation:

    ```text
    p14  太陽冬至前後立成卷第二
    p19  太陽夏至前後立成卷第四
    p24+ 曆成 / 遲疾 procedures
    p25+ 太陰立成 and lunar tables
    p33+ further calculation rules/tables
    p42  定朔 / 月大小 / 合朔時刻
    p43  盈日 and related procedures
    p44  交泛 / 直宿 procedures
    p45  closing numerical material
    ```

    Across the complete reviewed 45-page public reproduction, no independent table headed or mechanically identifiable as `晨昏分`, `日出入`, or `晝夜刻` was observed.

    The negative is deliberately narrow:

    ```text
    NO_EXPLICIT_DAYNIGHT_KE_TABLE_OBSERVED_IN_REVIEWED_PUBLIC_ZHOUXIANG_VOL6 = TRUE
    WHOLE_DATONG_TRADITION_ABSENCE = NOT_AUTHORIZED
    OTHER_FASCICLES / TONGGUI / ANNUAL_ALMANACS = UNRESOLVED
    ```

    ## 4. Consequence for the Sanming 1578 bridge

    Zhou Xiang vol6 remains important because it physically demonstrates Datong technical material in circulation immediately before 1578 and directly preserves a 1477 calculation epoch inside a 1569 reprint layer. But the inspected fascicle cannot currently supply the missing `59/41 + daily ladder + change-day` bridge because the target day/night table itself is not present on the reviewed surface.

    Therefore the search priority changes from another Datong-titled book to the mechanically relevant carriers: `大統曆通軌 / 大統曆日通軌` 晨昏分立成, actual pre-1578 annual Datong almanacs, and 楊瓚《閑中錄》.

    ## 5. Tianwen transmission impact

    New graph nodes record the 2019 digital surrogate, the Longqing-3/1569 edition layer, and the directly visible 1569/1477 passages. New confirmed edges attach the surrogate to the two direct passages and the 1569 passage to the edition layer.

    An explicit non-edge is recorded against `TABLE-SANMING-1578-DAYNIGHT-KE`: the reviewed Zhou Xiang vol6 is **not established** as a direct day/night-table parent. A separate Bei Lin 1477 -> Zhou Xiang 1569 dependency is also withheld as confirmed because the current support is secondary/probabilistic.

    ## 6. Product adjudication

    ```text
    HPA-ZDATE-006=MISSING_FROM_PRODUCT
    NEW_RUNTIME_CANDIDATE=false
    RUNTIME_WINNER=false
    CANDIDATE_COLLAPSE=false
    CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
    ALGORITHM_REOPEN_COUNT=0
    DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
    ```

    ## 7. Next gate

    1. directly acquire/collate `大統曆通軌/大統曆日通軌` surfaces that actually contain `晨昏分`, sunrise/sunset, or day/night standing tables;
    2. inspect pre-1578 annual Datong almanacs and `楊瓚《閑中錄》` for the Nanjing `59` cap and Sanming-like change-day fingerprint;
    3. continue searching for an explicit historical selection/rounding rule capable of explaining the Batch 12CI `(78,81]/147` threshold.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def main() -> int:
    continuity()
    registry()
    research()
    graph()
    matrix()
    matrix_md()
    state()
    write_doc()
    print("BATCH_12CM_FORMALIZATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
