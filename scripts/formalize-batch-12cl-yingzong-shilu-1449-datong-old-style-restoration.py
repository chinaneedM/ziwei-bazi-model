from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-YINGZONG-SHILU-1449-DATONG-OLD-STYLE-RESTORATION-CL"
PREV_ID = "BATCH-12-ZIWEI-CHILJEONGSAN-G894-HANYANG-DAYNIGHT-REGIONAL-CALIBRATION-CK"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YINGZONG-SHILU-1449-DATONG-OLD-STYLE-RESTORATION-CL.md"
RESEARCH = "docs/research/ZIWEI-YINGZONG-SHILU-1449-DATONG-OLD-STYLE-RESTORATION-R1.json"
SOURCE_ID = "EXT-NLC-WIKIMEDIA-YINGZONG-SHILU-V18-186-1449"

RUN_ID = 34943188353
ARTIFACT_ID = 10386575936
ARTIFACT_DIGEST = "sha256:d0955fd7d29c05a2b1c2abcede8cd31d26269897af7eccc3f91b5fa5a5388fad"
SOURCE_SHA256 = "ca44b5b876559842335f264950d36535cad3a95838e72c637fe8e27bda5459fd"
PAGE_SHA256 = {
    "090": "0e845f89966e8f2b594962ceabbb5e3535f1040f2961358bed78fd13fa357aa3",
    "091": "2a16c48279773be48e4c00fffb7d2a04794789988c9bfabf3862b48407f58942",
}
CONTINUATION_RUN_ID = 35007522124
CONTINUATION_ARTIFACT_ID = 10411764656
CONTINUATION_ARTIFACT_DIGEST = "sha256:422cb871c13b2fe2ba4a2db6532accd39238c78a45ce54127e7e945adf4f23a0"
CONTINUATION_SOURCE_SHA256 = "8c917af7b8a86450b6fffe8eaba1264d6537d081fd19516f473c6b50d05be9a7"


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate Batch 12CK tail in continuity verifier")
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
            "title": "《明英宗睿皇帝實錄》三百六十一卷 第18冊（卷182-186）NLC892-CBM0103-366392",
            "author_attribution": "〔明〕孫繼宗等纂修",
            "historical_period": "MING_YINGZONG_SHILU_RECEIVED_TEXT; TARGET_EVENT_ZHENGTONG_14_12_1449",
            "provider": "National Library of China digitized ancient book surrogate mirrored by Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:NLC892-CBM0103-366392_%E6%98%8E%E8%8B%B1%E5%AE%97%E7%9D%BF%E7%9A%87%E5%B8%9D%E5%AF%A6%E9%8C%84_%E4%B8%89%E7%99%BE%E5%85%AD%E5%8D%81%E4%B8%80%E5%8D%B7_%E7%AC%AC18%E5%86%8A.pdf",
            "source_role": "DIRECT_NO_OCR_PHYSICAL_PAGE_SURROGATE_FOR_1449_DATONG_CALENDAR_DAYNIGHT_KE_OLD_STYLE_RESTORATION_PASSAGE",
            "quality_notes": "Commons/NLC metadata identifies volume 18 as a manuscript-format surrogate containing卷182-186. Batch 12CL uses GitHub Actions-rendered source PDF page 090 to bind卷186 and page 091 to adjudicate the target passage directly without OCR. Surrogate date is modern and must not be confused with event, compilation, manuscript-copy, or digitization dates."
        })
    d["access_date"] = "2026-09-16"
    dump(p, d)


def research() -> None:
    direct_excerpt = (
        "詔更定大統曆晷刻。先是，天文生馬軾乞改大統曆晝夜時刻，命禮部會官議。"
        "欽天監監正許惇等奏：正統間監正彭德清于觀象臺測驗，以北京較之，南京北極出地上高三度，"
        "南極入地下低三度，冬至晝短三刻，夏至晝長三刻，逐一考究，奏准改入大統曆内，永爲定式。"
        "……今後造曆，宜悉照洪武、永樂間舊式。"
    )
    dump(RESEARCH, {
        "schema": "ZIWEI-YINGZONG-SHILU-1449-DATONG-OLD-STYLE-RESTORATION-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Does the 1449 Yingzong Shilu preserve a near-contemporary official policy restoration from Beijing-adjusted Datong day/night-ke values back to the Hongwu/Yongle old style, and what does that do to the pre-1578 59-ke lineage problem?",
        "source_binding": {
            "source_id": SOURCE_ID,
            "work": "明英宗睿皇帝實錄",
            "target_volume": 186,
            "target_reign_date": "正統十四年十二月戊申",
            "target_event": "詔更定大統曆晷刻",
            "date_firewall": {
                "event_date": "MING_ZHENGTONG_14_12_1449",
                "work_compilation_date": "POST_EVENT_MING_DYNASTIC_SHILU_COMPILATION; NOT_EQUATED_TO_EVENT_DATE",
                "surviving_manuscript_copy_date": "UNRESOLVED_FROM_CURRENT_SURROGATE_METADATA",
                "digital_surrogate_date": "MODERN_NLC_COMMONS_DIGITIZATION/MIRROR",
                "rule": "event/compilation/copy/surrogate dates remain distinct"
            }
        },
        "direct_physical_surrogate": {
            "workflow_run_id": RUN_ID,
            "artifact_id": ARTIFACT_ID,
            "artifact_digest": ARTIFACT_DIGEST,
            "source_pdf_sha256": SOURCE_SHA256,
            "rendered_page_count": 120,
            "ocr_used_for_glyph_claims": False,
            "page_sha256": PAGE_SHA256,
            "page_090_binding": "Right leaf directly reads the volume heading 錄卷之一百八十六, establishing the target volume boundary inside volume 18.",
            "page_091_binding": "The same rendered physical-page surrogate directly contains the Datong-calendar restoration passage; target wording is visually adjudicated against the page, while a modern transcription is used only as a locator/cross-check.",
            "direct_reading_key_phrases": [
                "詔更定大統曆晷刻",
                "以北京較之南京北極出地上高三度，南極入地下低三度",
                "冬至晝短三刻，夏至晝長三刻",
                "今後造曆，宜悉照洪武、永樂間舊式"
            ],
            "normalized_crosscheck_excerpt": direct_excerpt,
            "glyph_claim_policy": "No OCR output is admitted as evidence. The transcription only cross-checks order and normalization after direct visual localization of the target on page 091."
        },
        "continuation_control": {
            "workflow_run_id": CONTINUATION_RUN_ID,
            "artifact_id": CONTINUATION_ARTIFACT_ID,
            "artifact_digest": CONTINUATION_ARTIFACT_DIGEST,
            "volume_19_source_sha256": CONTINUATION_SOURCE_SHA256,
            "rendered_page_count": 108,
            "result": "Volume 19 starts with the卷187 sequence; it is not required for the卷186 target. This control repairs the initial mistaken suspicion that the target continued into volume 19.",
            "research_defect_class": "LOCATOR_SCOPE_CORRECTION_ONLY; NOT_PRODUCT_OR_PROVENANCE_METADATA_DEFECT"
        },
        "historical_adjudication": {
            "beijing_vs_nanjing_regional_difference_explicit": True,
            "difference_magnitude": "3 ke at both solstitial extremes according to the passage",
            "prior_beijing_adjustment_recorded": True,
            "restoration_order": "Future calendar production shall follow the Hongwu/Yongle old style.",
            "policy_meaning": "The 1449 record is an explicit official rollback/restoration decision, not merely a later commentator's numerical comparison.",
            "direct_passage_prints_59_41": False,
            "direct_passage_prints_62_38": False,
            "numeric_bridge_requires_prior_batch": "Batch 12CF directly established Nanjing 59 versus Beijing 62; Batch 12CL independently establishes the 3-ke Beijing/Nanjing differential and restoration of the older Hongwu/Yongle style.",
            "combined_inference": "The 59-ke Nanjing regional standard is no longer treated as an isolated 1447 measurement point: the 1449 court record proves a policy reversion away from the Beijing-adjusted regime toward the older standard family. Exact identity of every daily row remains unproved."
        },
        "relationship_to_sanming_1578": {
            "strengthens_59_cap_policy_continuity_candidate": True,
            "direct_copying_proved": False,
            "exact_step_ladder_identity_proved": False,
            "change_day_fingerprint_proved": False,
            "rounding_selection_rule_proved": False,
            "lineage_effect": "Strengthens the pre-1578 regional/policy ancestry layer for a 59-cap family but leaves the Huqian-style one-ke ladder and Sanming change-day/quantization bridge unresolved."
        },
        "transmission_impact": {
            "nodes_added": [
                "DIGITAL-SURROGATE-YINGZONG-SHILU-NLC892-V18",
                "PASSAGE-YINGZONG186-DATONG-OLD-STYLE-RESTORATION-1449",
                "RULE-FAMILY-MING-HONGWU-YONGLE-OLD-STYLE-DATONG"
            ],
            "edges_added": ["TG-E0016", "TG-E0017", "TG-E0018", "TG-E0019"],
            "claim_strengthening": "A Nanjing-vs-Beijing regional difference is now tied to an explicit 1449 official restoration decision rather than inferred only from later received histories.",
            "claims_not_made": [
                "1449 passage itself prints 59/41",
                "Hongwu/Yongle old style is mechanically identical row-for-row to the 1578 Sanming table",
                "1449 restoration directly copied into Sanming",
                "policy continuity proves the missing daily step-ladder/change-day bridge"
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
            "Search 1449-1578 Nanjing/Jiangnan calendars, almanacs, or technical tables that preserve the restored old-style 59-ke cap together with an explicit intra-term daily ladder/change-day fingerprint.",
            "Search for an explicit historical selection/rounding instruction capable of explaining the Batch 12CI (78,81]/147 precision-to-coarse threshold.",
            "Continue the independent Fullbook upper-five-ke -> previous-night Hai lineage without conflating it with seasonal-table ancestry."
        ]
    })


def graph() -> None:
    p = Path("docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    node_ids = {x.get("node_id") for x in d["nodes"]}
    nodes = [
        {
            "node_id": "DIGITAL-SURROGATE-YINGZONG-SHILU-NLC892-V18",
            "node_type": "DIGITAL_SURROGATE",
            "label": "NLC892-CBM0103-366392《明英宗睿皇帝實錄》第18冊數字替身",
            "system_scope": "MING_OFFICIAL_HISTORIOGRAPHICAL_TIMEKEEPING",
            "work_composition_date": "MING_SHILU_POST_EVENT_COMPILATION",
            "edition_impression_date": None,
            "physical_copy_date": "UNRESOLVED_FROM_CURRENT_METADATA",
            "digital_surrogate_date": "MODERN_NLC_COMMONS_SURROGATE",
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        },
        {
            "node_id": "PASSAGE-YINGZONG186-DATONG-OLD-STYLE-RESTORATION-1449",
            "node_type": "PASSAGE",
            "label": "《英宗實錄》卷186正統十四年十二月：詔更定大統曆晷刻／悉照洪武永樂間舊式",
            "system_scope": "MING_OFFICIAL_CALENDRICAL_POLICY",
            "historical_event_date": "ZHENGTONG_14_12_1449",
            "physical_surrogate_locator": "NLC892 volume18 PDF pages 090-091; target passage page091",
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        },
        {
            "node_id": "RULE-FAMILY-MING-HONGWU-YONGLE-OLD-STYLE-DATONG",
            "node_type": "RULE_FAMILY",
            "label": "洪武永樂舊式大統曆晝夜刻規則家族（1449恢復令見證）",
            "system_scope": "MING_OFFICIAL_CALENDRICAL_TIMEKEEPING",
            "date": "ZHENGTONG_14_12_1449",
            "mechanical_identity": "Official record states Beijing differs from Nanjing by three degrees of polar altitude and three ke at solstitial day length; court orders future calendar production to follow the Hongwu/Yongle old style. Exact 59/41 numerals and daily ladder are not printed in this passage.",
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
            "edge_id": "TG-E0016",
            "from": "DIGITAL-SURROGATE-YINGZONG-SHILU-NLC892-V18",
            "relation": "ATTESTS",
            "to": "PASSAGE-YINGZONG186-DATONG-OLD-STYLE-RESTORATION-1449",
            "status": "CONFIRMED",
            "confidence": "HIGH",
            "evidence_class": "DIRECT_RENDERED_SURROGATE_PAGE_090_091_NO_OCR",
            "evidence": [RESEARCH],
            "adjudication_batch": BATCH_ID
        },
        {
            "edge_id": "TG-E0017",
            "from": "PASSAGE-YINGZONG186-DATONG-OLD-STYLE-RESTORATION-1449",
            "relation": "ATTESTS",
            "to": "RULE-FAMILY-MING-HONGWU-YONGLE-OLD-STYLE-DATONG",
            "status": "CONFIRMED",
            "confidence": "HIGH",
            "evidence_class": "NEAR_CONTEMPORARY_OFFICIAL_SHILU_POLICY_PASSAGE_DIRECT_PAGE_COLLATION",
            "evidence": [RESEARCH],
            "adjudication_batch": BATCH_ID
        },
        {
            "edge_id": "TG-E0018",
            "from": "RULE-FAMILY-MING-HONGWU-YONGLE-OLD-STYLE-DATONG",
            "relation": "REGIONAL_ADAPTATION_CANDIDATE_FOR",
            "to": "STANDARD-NANJING-59KE-1447",
            "status": "PROBABLE",
            "confidence": "MEDIUM_HIGH",
            "evidence_class": "COMPOSITE_1447_DIRECT_NANJING59_PLUS_1449_EXPLICIT_THREE_KE_DIFFERENTIAL_AND_OLD_STYLE_RESTORATION",
            "evidence": [RESEARCH, "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YINGZONG-SHILU-1447-NANJING-59-41-PHYSICAL-COLLATION-CF.md"],
            "scope_note": "Candidate relation concerns the restored regional standard family only; row-for-row table identity is not asserted.",
            "adjudication_batch": BATCH_ID
        },
        {
            "edge_id": "TG-E0019",
            "from": "RULE-FAMILY-MING-HONGWU-YONGLE-OLD-STYLE-DATONG",
            "relation": "SYNTHESIS_COMPONENT_CANDIDATE_FOR",
            "to": "TABLE-SANMING-1578-DAYNIGHT-KE",
            "status": "POSSIBLE",
            "confidence": "MEDIUM",
            "evidence_class": "PRE1578_OFFICIAL_POLICY_CONTINUITY_FOR_59_CAP_REGIONAL_FAMILY_WITH_MISSING_DAILY_LADDER_BRIDGE",
            "evidence": [RESEARCH],
            "scope_note": "This strengthens only the regional/policy component of a possible Sanming ancestry. Huqian-style daily ladder, change-day fingerprint, and rounding rule remain unbridged.",
            "adjudication_batch": BATCH_ID
        }
    ]
    for edge in edges:
        if edge["edge_id"] not in edge_ids:
            d["edges"].append(edge)
            edge_ids.add(edge["edge_id"])

    non_edges = d.setdefault("explicit_non_edges", [])
    if not any(x.get("from") == "PASSAGE-YINGZONG186-DATONG-OLD-STYLE-RESTORATION-1449" and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE" for x in non_edges):
        non_edges.append({
            "from": "PASSAGE-YINGZONG186-DATONG-OLD-STYLE-RESTORATION-1449",
            "relation": "DIRECT_TABLE_PARENT_OF",
            "to": "TABLE-SANMING-1578-DAYNIGHT-KE",
            "status": "UNRESOLVED",
            "reason": "The 1449 passage proves a policy restoration and three-ke regional differential but does not print Sanming's full daily ladder, change-day fingerprint, or 59/41 row set.",
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
    rp["batch_12cl_yingzong_shilu_1449_datong_old_style_restoration"] = {
        "source_ids": [SOURCE_ID],
        "direct_volume_186_physical_surrogate_bound": True,
        "direct_target_page": "NLC892 volume18 PDF page091",
        "no_ocr_glyph_adjudication": True,
        "beijing_nanjing_three_ke_regional_difference_explicit": True,
        "hongwu_yongle_old_style_restoration_order_explicit": True,
        "passage_prints_59_41": False,
        "strengthens_59_cap_policy_continuity_candidate": True,
        "sanming_daily_ladder_bridge_proved": False,
        "direct_1449_to_sanming_copying_proved": False,
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
    if "## Progress — Batch 12CL" not in s:
        s += dedent(f'''

        ## Progress — Batch 12CL

        - NLC/Wikimedia volume 18 of `《明英宗睿皇帝實錄》` was rendered in GitHub Actions without OCR. Physical-surrogate page `090` binds `卷之一百八十六`; page `091` directly contains `詔更定大統曆晷刻` and the order `今後造曆，宜悉照洪武、永樂間舊式`.
        - The same official passage explicitly states that the Beijing adjustment differed from Nanjing by three degrees of polar altitude and by `冬至晝短三刻 / 夏至晝長三刻`. This is an official regional-calibration and policy-restoration statement, not a modern reconstruction.
        - The passage itself does **not** print `59/41` or `62/38`. Combined with Batch 12CF's direct 1447 `南京59 / 北京62` evidence, it strengthens the interpretation that the Nanjing 59-ke branch belonged to an older standard family restored after the Beijing-adjusted regime, while leaving row-for-row identity unresolved.
        - For the 1578 Sanming table, Batch 12CL upgrades the regional/policy continuity candidate but does not close the missing Huqian-style daily ladder, change-day fingerprint, or rounding/selection bridge. No direct-copy edge is asserted.
        - A separate continuation control rendered NLC volume 19 and confirmed that it begins with the卷187 sequence; the earlier suspicion that the target might continue into volume 19 is closed as a locator-scope correction only.
        - `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; upper-Zi→Hai vote +0; runtime winner/candidate collapse/algorithm reopen remain none/0.

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
        "Batch 12CL directly binds NLC/Wikimedia Yingzong Shilu volume 18 page 090 to卷186 and page 091 to the 正統十四年十二月 '詔更定大統曆晷刻' passage, with no OCR used for glyph claims.",
        "Batch 12CL establishes a near-contemporary official 1449 policy restoration: the record states the Beijing/Nanjing solstitial day-length difference as three ke and orders future Datong calendar production to follow the Hongwu/Yongle old style.",
        "Batch 12CL strengthens the pre-1578 59-ke regional/policy continuity candidate when combined with Batch 12CF's direct Nanjing59/Beijing62 evidence, but it does not prove Sanming row-for-row descent; the daily ladder/change-day/rounding bridge remains the next gate."
    ]
    for x in additions:
        if x not in h["current_focus"]:
            h["current_focus"].append(x)
    d["schema_version"] = "1.98.0"
    d["updated_at"] = "2026-09-16"
    dump(p, d)


def write_doc() -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit — Batch 12CL

    ## Scope

    This batch follows Batch 12CK's regional-calibration control. It asks whether a near-contemporary official Ming record documents a policy transition between Beijing-adjusted day/night-ke values and the older Hongwu/Yongle standard, and whether that transition materially strengthens the pre-1578 ancestry case for the `59`-ke regional family later seen in `《三命通會》`.

    This is historical provenance / philology / transmission-genealogy work only. It does **not** reopen deterministic charting.

    ## 1. Direct source and date firewall

    GitHub Actions run `{RUN_ID}` fetched the NLC/Wikimedia surrogate `NLC892-CBM0103-366392` (`《明英宗睿皇帝實錄》`第18冊) and rendered all 120 PDF pages. Artifact `{ARTIFACT_ID}` has digest `{ARTIFACT_DIGEST}`; the source PDF SHA-256 is `{SOURCE_SHA256}`. `NO_OCR_USED=true`.

    The evidence is date-scoped:

    - target event: `正統十四年十二月`, 1449;
    - work compilation: Ming dynastic Shilu compilation after the event;
    - surviving manuscript-copy date: unresolved from the current surrogate metadata;
    - digital surrogate: modern NLC/Wikimedia digitization/mirror.

    These dates are not collapsed.

    ## 2. Physical-page locator repair and direct collation

    Direct visual review of the rendered pages gives:

    ```text
    page 090 sha256 {PAGE_SHA256['090']}
      right leaf: 錄卷之一百八十六

    page 091 sha256 {PAGE_SHA256['091']}
      contains the target Datong-calendar passage
    ```

    Key directly adjudicated phrases on page 091 are:

    ```text
    詔更定大統曆晷刻
    以北京較之南京北極出地上高三度，南極入地下低三度
    冬至晝短三刻，夏至晝長三刻
    今後造曆，宜悉照洪武、永樂間舊式
    ```

    A modern transcription was used only to cross-check reading order and normalized wording after the page was physically localized. OCR output is not evidence.

    A continuation-control workflow (run `{CONTINUATION_RUN_ID}`, artifact `{CONTINUATION_ARTIFACT_ID}`, digest `{CONTINUATION_ARTIFACT_DIGEST}`) separately rendered NLC volume 19. It begins with the卷187 sequence, so the initial suspicion that the卷186 target might continue there is rejected. This is a research locator correction, not a historical negative result and not a product defect.

    ## 3. What the 1449 passage actually proves

    The official record preserves a concrete policy dispute. The defence of the Beijing-adjusted rule states that, compared with Nanjing, Beijing's polar altitude differs by three degrees and its solstitial daylight differs by three ke: shorter at winter solstice and longer at summer solstice. The emperor rejects Beijing as the universal reference and orders future calendars to follow the Hongwu/Yongle old style.

    Therefore the 1449 witness directly proves:

    1. `region/locality` was operationally material to official Ming day/night-ke calibration;
    2. a Beijing-adjusted regime existed and was defended as an approved Datong-calendar standard;
    3. the court then issued an explicit restoration/rollback order to the Hongwu/Yongle old style.

    It does **not** directly print `59/41` or `62/38`.

    ## 4. Composite reading with the already audited 1447 evidence

    Batch 12CF already directly established the contemporary official distinction:

    ```text
    Nanjing: 59 ke at the summer-solstice extreme
    Beijing: 62 ke at the summer-solstice extreme
    difference: 3 ke
    ```

    Batch 12CL independently supplies the policy side of the same regional contrast: Beijing versus Nanjing differs by three ke at the solstitial extreme, and the Beijing-adjusted regime is subsequently rejected in favour of the Hongwu/Yongle old style.

    The combined evidence is stronger than either item alone. It makes the Nanjing `59` branch a historically persistent regional/policy family candidate rather than an isolated 1447 numerical datum. However, the Shilu restoration order does not by itself establish exact row-for-row identity between every Hongwu/Yongle old-style daily table and the 1447 Nanjing table.

    ## 5. Consequence for the 1578 Sanming ancestry problem

    The viable chain is now sharper:

    ```text
    pre-1449 Hongwu/Yongle old-style regional family
      -> 1447 directly attested Nanjing 59-ke standard
      -> 1449 official restoration away from Beijing-adjusted regime
      ... missing daily-ladder / change-day / quantization bridge ...
      -> 1578 Sanming 59/41 display
    ```

    This is a strengthened **regional/policy ancestry candidate**, not a direct-copy proof. The missing bridge still has to explain the Huqian-style one-ke intra-term ladder, Sanming's change-day fingerprint, and the coarse selection/rounding behavior identified in Batch 12CI.

    ## 6. Tianwen transmission impact

    New nodes:

    ```text
    DIGITAL-SURROGATE-YINGZONG-SHILU-NLC892-V18
    PASSAGE-YINGZONG186-DATONG-OLD-STYLE-RESTORATION-1449
    RULE-FAMILY-MING-HONGWU-YONGLE-OLD-STYLE-DATONG
    ```

    New edges:

    ```text
    NLC volume18 surrogate --ATTESTS--> 1449 restoration passage
    1449 restoration passage --ATTESTS--> restored Hongwu/Yongle old-style policy
    Hongwu/Yongle old-style family --REGIONAL_ADAPTATION_CANDIDATE_FOR--> Nanjing 59-ke 1447
    restored policy family 1449 --SYNTHESIS_COMPONENT_CANDIDATE_FOR--> Sanming 1578 table
    ```

    No direct 1449 -> Sanming table-parent edge is asserted.

    ## 7. Product adjudication

    ```text
    HPA-ZDATE-006=MISSING_FROM_PRODUCT
    UPPER_ZI_TO_HAI_VOTE_INCREMENT=0
    NEW_RUNTIME_CANDIDATE=false
    RUNTIME_WINNER=false
    CANDIDATE_COLLAPSE=false
    CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
    ALGORITHM_REOPEN_COUNT=0
    DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
    ```

    ## 8. Next gate

    1. search 1449-1578 Nanjing/Jiangnan calendars, almanacs, or technical tables that combine the restored old-style `59`-ke cap with an explicit Huqian-like intra-term ladder or Sanming-like change-day fingerprint;
    2. search for an explicit historical selection/rounding instruction capable of explaining the Batch 12CI `(78,81]/147` precision-to-coarse threshold;
    3. continue the independent Fullbook upper-five-ke -> previous-night Hai lineage without conflating it with seasonal-table ancestry.

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
    print("BATCH_12CL_FORMALIZATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
