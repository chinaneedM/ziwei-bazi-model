from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-CHILJEONGSAN-G894-HANYANG-DAYNIGHT-REGIONAL-CALIBRATION-CK"
PREV_ID = "BATCH-12-ZIWEI-HUQIANJING-TIANYIGE-SIKU-CROSS-RECENSION-COLLATION-CJ"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-CHILJEONGSAN-G894-HANYANG-DAYNIGHT-REGIONAL-CALIBRATION-CK.md"
RESEARCH = "docs/research/ZIWEI-CHILJEONGSAN-G894-HANYANG-DAYNIGHT-REGIONAL-CALIBRATION-R1.json"
KYU_SOURCE_ID = "EXT-KYUJANGGAK-CHILJEONGSAN-NAEPYEON-G894-1444"
SILLOK_SOURCE_ID = "EXT-SILLOK-SEJONG158-HANYANG-DAYNIGHT"

G894_RUN = 34937262190
G894_ARTIFACT = 10383449874
G894_ARTIFACT_DIGEST = "sha256:a3941a77566bb2ac2a963ed376c5ba5023e290e7e4a319c8c2dc4d0a67742f1c"
G894_PAGE_SHA256 = {
    "039b": "9554aea9fa1e7b57f755b53ca0a01f1455c282b4957057f5420ceb9bd6fc4977",
    "040a": "b2cef4e5efd3bb4a0646e9cb6c60bb1ea49ee808ebe27db8ab328f8f01a64cb9",
    "040b": "1141cc04897ce245920b5b57e8ec4fd0ed3f8123020b5c403a68f6f013229913",
    "041a": "d6a9b73f24ef9423b23458e836e64331b829f6e1d44d92ba5dfebfb9380084c4",
    "041b": "4f226c70396f7386fc9844e178ce9792fefee150fb585a88c420e7000f01aa56",
    "042a": "30c80b088c768e5bcf98f8b126c9f990428ba97288b878ed01656296f1b54a07",
    "042b": "2a23980f0f1eb106b3a9d5141e5975dd6208241ed0b0bb56733de658f1caaca1",
    "043a": "1962ad385f721e8256c49a4926cc94a4e979587d9d9b2a9b26c0df3cfcf6f456",
    "043b": "52a6befb279ef393d9c86180d297862c9c10f0042aa6376c2993cba78a25183c",
    "044a": "d9d3c9042f15f43b8a1b30c24cc0d6a26904ff0fba6cf9edf8d4e845ee4268f2",
    "044b": "07caa02533ea919c65cb45f0ab6d3ed88622feeb5a7cfa0d30f157bdc8401e61",
}
SILLOK_RUN = 34939861102
SILLOK_ARTIFACT = 10385325116
SILLOK_ARTIFACT_DIGEST = "sha256:5376bb544b775b023d6450d4a00fcbab11c0049fc09f702f11ff782068bec5a9"
SILLOK_HTML_SHA256 = {
    "wda_50034001": "e3e8b212bc3a16c0d80c9ebe0b249ae16c3610b870217dfdbefef2e2a8cc3110",
    "wda_50034002": "3326988a79c437ed29cddbb11a11921a9678181470cd219d22aff029ec430c7f",
}


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate Batch 12CJ tail in continuity verifier")
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
    if KYU_SOURCE_ID not in ids:
        d["sources"].append({
            "source_id": KYU_SOURCE_ID,
            "title": "《七政算內篇》奎貴894-v.1-3 / 甲寅字 / 1444",
            "author_attribution": "李純之、金淡（朝鮮）受命編",
            "historical_period": "JOSEON_SEJONG_1444",
            "provider": "Seoul National University Kyujanggak Institute for Korean Studies",
            "url": "https://kyudb.snu.ac.kr/book/view.do?book_cd=GK00894_00&mid=GDS&target=master",
            "source_role": "DIRECT_PHYSICAL_1444_GABINJA_WITNESS_FOR_HANYANG_LOCALIZED_DAILY_SUNRISE_SUNSET_DAY_NIGHT_TABLE",
            "quality_notes": "Provider catalog identifies call number 奎貴894-v.1-3, compilers 李純之/金淡, movable-type edition 甲寅字, publication year 1444. Batch 12CK binds volume 0003 provider pages 039b..044b through direct renderer responses and reviews target glyphs without OCR."
        })
    if SILLOK_SOURCE_ID not in ids:
        d["sources"].append({
            "source_id": SILLOK_SOURCE_ID,
            "title": "《世宗實錄》卷158《內篇》下卷《二至後日出入晝夜辰刻》冬至後 / 夏至後",
            "historical_period": "JOSEON_SEJONG_SILLOK_ANNEX_RECEIVED_TEXT",
            "provider": "National Institute of Korean History / Joseon Wangjo Sillok",
            "url": "https://sillok.history.go.kr/id/wda_50034002",
            "source_role": "OFFICIAL_INSTITUTIONAL_TRANSCRIPTION_AND_ARTICLE_BINDING_FOR_HANYANG_LOCAL_CALIBRATION_STATEMENT",
            "quality_notes": "Official route wda_50034001 binds 冬至後 to Taebaeksan copy 62책 158권 28장 A면; wda_50034002 binds 夏至後 and the locality statement to 29장 B면. The locator records official HTML hashes; this evidence is institutional transcription, not a substitute for physical-image glyph adjudication."
        })
    d["access_date"] = "2026-09-15"
    dump(p, d)


def research() -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-CHILJEONGSAN-G894-HANYANG-DAYNIGHT-REGIONAL-CALIBRATION-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Does a directly dated 1444 Chiljeongsan Naepyeon witness establish a Hanyang-localized day/night-ke standard distinct from contemporary Nanjing/Beijing standards, and what does that do to Sanming lineage inference?",
        "kyujanggak_bibliographic_binding": {
            "source_id": KYU_SOURCE_ID,
            "book_cd": "GK00894_00",
            "call_number": "奎貴894-v.1-3",
            "title": "七政算內篇",
            "compilers": ["李純之", "金淡"],
            "edition": "甲寅字",
            "provider_publication_year": 1444,
            "date_firewall": "1444 is the provider catalog publication/impression attribution for this G894 witness; it is not inferred from the modern digital surrogate filename."
        },
        "g894_direct_physical_pages": {
            "workflow_run_id": G894_RUN,
            "artifact_id": G894_ARTIFACT,
            "artifact_digest": G894_ARTIFACT_DIGEST,
            "volume": "0003",
            "provider_pages": list(G894_PAGE_SHA256),
            "provider_page_sha256": G894_PAGE_SHA256,
            "page_identity_basis": "EVERY_IMAGE_PATH_PARSED_FROM_DIRECT_PROVIDER_RENDERER_RESPONSE_FOR_REQUESTED_PAGE_ID",
            "filename_sequence_inference": "FORBIDDEN",
            "ocr_used_for_glyph_claims": False,
            "direct_readings": [
                "040a heading: 二至後日出入晝夜辰刻 / 冬至後",
                "040a winter-solstice first day: 日出辰初一刻; 日入申正二刻; 晝三十九刻; 夜六十一刻",
                "040a eleventh day already shows the next sunrise/sunset step while the small day/night annotation has advanced to the 40/60 regime",
                "042a pre-summer entry 一百五十九日: 晝六十刻; 夜四十刻",
                "042a heading: 夏至後",
                "042a summer-solstice first day: 日出寅正二刻; 日入戌初一刻; 晝六十一刻; 夜三十九刻"
            ],
            "extreme_pair": {
                "winter_solstice": "39/61",
                "summer_solstice": "61/39",
                "total_ke": 100
            }
        },
        "official_sillok_article_binding": {
            "source_id": SILLOK_SOURCE_ID,
            "workflow_run_id": SILLOK_RUN,
            "artifact_id": SILLOK_ARTIFACT,
            "artifact_digest": SILLOK_ARTIFACT_DIGEST,
            "locator_schema": "SILLOK-SEJONG158-DAYNIGHT-ARTICLE-LOCATOR-R2",
            "prior_rejected_locator_prefix": "wda_50018",
            "correct_route_prefix": "wda_50034",
            "article_html_sha256": SILLOK_HTML_SHA256,
            "articles": {
                "wda_50034001": "世宗實錄158卷 / 內篇 下卷 / 二至後日出入晝夜辰刻 / 冬至後 / 太白山事故本62책158권28장A면",
                "wda_50034002": "世宗實錄158卷 / 內篇 下卷 / 二至後日出入晝夜辰刻 / 夏至後 / 太白山事故本62책158권29장B면"
            },
            "official_transcription": "日出入隨處各異,諸曆不同。內篇據漢陽日至之晷,推求至差,得每日日出入,晝夜刻分,定爲本國所用。外篇則因西域曆之舊,無所增損。但以備參驗耳。",
            "evidence_class": "OFFICIAL_INSTITUTIONAL_HTML_TRANSCRIPTION_PLUS_EXACT_ARTICLE_BINDING",
            "glyph_scope_note": "The wording is cited as official institutional transcription. Critical table numerals in this batch are adjudicated from the independent G894 physical-page images, not from OCR."
        },
        "regional_adjudication": {
            "hanyang_1444": "summer extreme 61 ke daylight / 39 ke night; winter extreme 39/61",
            "nanjing_1447": "official memorial records solstitial extreme 59 ke; 41 is its complement under the established 100-ke total",
            "beijing_1447": "same official memorial records 62 ke; 38 is its complement under the established 100-ke total",
            "same_period_regional_variability_directly_material": True,
            "single_universal_east_asian_solstitial_ke_value_rejected": True,
            "numeric_similarity_alone_proves_lineage": False
        },
        "relationship_to_sanming_1578": {
            "sanming_summer_anchor": "59/41",
            "hanyang_summer_anchor": "61/39",
            "exact_table_identity": False,
            "direct_hanyang_to_sanming_copying_proved": False,
            "lineage_effect": "Hanyang is a confirmed parallel regional calibration branch and therefore a negative control against universalizing 59/41. The next Sanming ancestry search should preferentially target Nanjing/Jiangnan or another 59-ke-cap intermediary rather than assume every East-Asian day/night table belongs to one numerical lineage."
        },
        "transmission_impact": {
            "nodes_added": [
                "PHYSICAL-COPY-CHILJEONGSAN-NAEPYEON-G894-1444",
                "PASSAGE-SEJONG158-HANYANG-LOCAL-CALIBRATION",
                "STANDARD-HANYANG-61KE-1444"
            ],
            "edges_added": ["TG-E0013", "TG-E0014", "TG-E0015"],
            "claim_strengthening": "Region/locality is now an explicitly attested transmission variable, not a retrospective explanatory convenience.",
            "claims_not_made": [
                "Hanyang -> Nanjing direct transmission",
                "Nanjing -> Hanyang direct transmission",
                "Hanyang -> Sanming direct transmission",
                "shared title/numeric neighborhood = shared direct parent"
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
            "Search pre-1578 Nanjing/Jiangnan or otherwise securely localized intermediaries that combine a Huqian-style intra-term one-ke ladder with a 59-ke cap or Sanming-like change-day fingerprint.",
            "Search for an explicit historical selection/rounding instruction capable of explaining the Batch 12CI (78,81]/147 precision-to-coarse threshold.",
            "Continue the independent Fullbook upper-five-ke -> previous-night Hai lineage without conflating it with regional seasonal-table ancestry."
        ]
    })


def graph() -> None:
    p = Path("docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    node_ids = {x.get("node_id") for x in d["nodes"]}
    new_nodes = [
        {
            "node_id": "PHYSICAL-COPY-CHILJEONGSAN-NAEPYEON-G894-1444",
            "node_type": "PHYSICAL_COPY",
            "label": "奎章閣奎貴894-v.1-3《七政算內篇》甲寅字1444",
            "system_scope": "JOSEON_CALENDRICAL_TIMEKEEPING",
            "work_composition_date": "SEJONG_ERA; COMPILED_BEFORE_1444_PRINT",
            "edition_impression_date": "PROVIDER_CATALOG_1444_GABINJA",
            "physical_copy_date": "CATALOGUED_AS_1444_GABINJA_WITNESS",
            "digital_surrogate_date": "MODERN_KYUJANGGAK_DIGITAL_SURROGATE",
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        },
        {
            "node_id": "PASSAGE-SEJONG158-HANYANG-LOCAL-CALIBRATION",
            "node_type": "PASSAGE",
            "label": "《世宗實錄》158卷：內篇據漢陽日至之晷推求本國日出入晝夜刻分",
            "system_scope": "JOSEON_CALENDRICAL_HISTORIOGRAPHICAL_ATTESTATION",
            "source_article_id": "wda_50034002",
            "physical_leaf_binding": "太白山事故本62책158권29장B면",
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        },
        {
            "node_id": "STANDARD-HANYANG-61KE-1444",
            "node_type": "REGIONAL_STANDARD",
            "label": "1444漢陽日至校準39↔61晝夜刻地域標準",
            "system_scope": "JOSEON_OFFICIAL_CALENDRICAL_TIMEKEEPING",
            "date": "PROVIDER_CATALOG_1444",
            "mechanical_identity": "100-ke total; winter-solstice day/night 39/61; summer-solstice day/night 61/39; official received-text statement says the Inner Chapter derives daily sunrise/sunset and day/night values from the Hanyang solstitial gnomon for domestic use.",
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        }
    ]
    for node in new_nodes:
        if node["node_id"] not in node_ids:
            d["nodes"].append(node)
            node_ids.add(node["node_id"])

    edge_ids = {x.get("edge_id") for x in d["edges"]}
    new_edges = [
        {
            "edge_id": "TG-E0013",
            "from": "PHYSICAL-COPY-CHILJEONGSAN-NAEPYEON-G894-1444",
            "relation": "ATTESTS",
            "to": "STANDARD-HANYANG-61KE-1444",
            "status": "CONFIRMED",
            "confidence": "HIGH",
            "evidence_class": "DIRECT_PROVIDER_BOUND_PHYSICAL_PAGE_IMAGES_NO_OCR",
            "evidence": [RESEARCH],
            "adjudication_batch": BATCH_ID
        },
        {
            "edge_id": "TG-E0014",
            "from": "PASSAGE-SEJONG158-HANYANG-LOCAL-CALIBRATION",
            "relation": "ATTESTS",
            "to": "STANDARD-HANYANG-61KE-1444",
            "status": "CONFIRMED",
            "confidence": "HIGH",
            "evidence_class": "OFFICIAL_INSTITUTIONAL_TRANSCRIPTION_WITH_EXACT_ARTICLE_AND_LEAF_BINDING",
            "evidence": [RESEARCH],
            "scope_note": "This edge attests the locality/calibration rationale; physical table numerals are independently controlled by the G894 witness.",
            "adjudication_batch": BATCH_ID
        },
        {
            "edge_id": "TG-E0015",
            "from": "STANDARD-HANYANG-61KE-1444",
            "relation": "PARALLEL_COEXISTS_WITH",
            "to": "STANDARD-NANJING-59KE-1447",
            "status": "CONFIRMED",
            "confidence": "HIGH",
            "evidence_class": "DIRECTLY_LOCALIZED_NEAR_CONTEMPORARY_REGIONAL_STANDARDS",
            "evidence": [RESEARCH, "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YINGZONG-SHILU-1447-NANJING-59-41-PHYSICAL-COLLATION-CF.md"],
            "scope_note": "Near-contemporary Hanyang 61 and Nanjing 59 are both directly localized standards. Coexistence proves regional variability, not transmission direction.",
            "adjudication_batch": BATCH_ID
        }
    ]
    for edge in new_edges:
        if edge["edge_id"] not in edge_ids:
            d["edges"].append(edge)
            edge_ids.add(edge["edge_id"])

    non_edges = d.setdefault("explicit_non_edges", [])
    if not any(x.get("from") == "STANDARD-HANYANG-61KE-1444" and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE" for x in non_edges):
        non_edges.append({
            "from": "STANDARD-HANYANG-61KE-1444",
            "relation": "DIRECT_TABLE_PARENT_OF",
            "to": "TABLE-SANMING-1578-DAYNIGHT-KE",
            "status": "UNRESOLVED",
            "reason": "Hanyang is explicitly local and has 61/39 at summer solstice, whereas Sanming prints 59/41. Regional coexistence forbids inferring a direct parent from generic day/night-table similarity.",
            "evidence": [RESEARCH]
        })
    d["updated_at"] = "2026-09-15"
    dump(p, d)


def graph_verifier() -> None:
    p = Path("scripts/verify-tianwen-transmission-genealogy-r1.py")
    s = p.read_text(encoding="utf-8")
    if '"STANDARD-HANYANG-61KE-1444",' not in s:
        needle = '        "RULE-FAMILY-HUQIANJING-CHUANJIAN-20ARROW-40-60",\n'
        block = (
            '        "PHYSICAL-COPY-CHILJEONGSAN-NAEPYEON-G894-1444",\n'
            '        "PASSAGE-SEJONG158-HANYANG-LOCAL-CALIBRATION",\n'
            '        "STANDARD-HANYANG-61KE-1444",\n'
        )
        if needle not in s:
            raise SystemExit("cannot extend Tianwen required nodes for Batch 12CK")
        s = s.replace(needle, needle + block, 1)
    if 'e15 = next((e for e in edges if e.get("edge_id") == "TG-E0015"), None)' not in s:
        needle = '    ncl = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-SISHI-QIHOU-NCL03164-OLD-MANUSCRIPT")\n'
        block = (
            '    e13 = next((e for e in edges if e.get("edge_id") == "TG-E0013"), None)\n'
            '    if not e13 or e13.get("relation") != "ATTESTS" or e13.get("status") != "CONFIRMED":\n'
            '        fail("G894 Hanyang standard attestation edge regressed")\n'
            '    e14 = next((e for e in edges if e.get("edge_id") == "TG-E0014"), None)\n'
            '    if not e14 or e14.get("relation") != "ATTESTS" or e14.get("status") != "CONFIRMED":\n'
            '        fail("Sejong 158 Hanyang-locality attestation edge regressed")\n'
            '    e15 = next((e for e in edges if e.get("edge_id") == "TG-E0015"), None)\n'
            '    if not e15 or e15.get("relation") != "PARALLEL_COEXISTS_WITH" or e15.get("status") != "CONFIRMED":\n'
            '        fail("Hanyang/Nanjing regional parallel edge regressed")\n\n'
        )
        if needle not in s:
            raise SystemExit("cannot insert Batch 12CK graph checks")
        s = s.replace(needle, block + needle, 1)
    p.write_text(s, encoding="utf-8")


def matrix() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next((x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006"), None)
    if row is None:
        raise SystemExit("HPA-ZDATE-006 missing")
    rp = row.setdefault("research_progress", {})
    rp["batch_12ck_chiljeongsan_g894_hanyang_regional_calibration"] = {
        "source_ids": [KYU_SOURCE_ID, SILLOK_SOURCE_ID],
        "direct_1444_g894_physical_pages": True,
        "official_sillok_locality_statement_bound": True,
        "hanyang_solstitial_extrema": "39/61 <-> 61/39",
        "regional_variability_against_nanjing_59_and_beijing_62": True,
        "single_universal_solstitial_value_rejected": True,
        "direct_hanyang_to_sanming_parent_proved": False,
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
    if "## Progress — Batch 12CK" not in s:
        s += dedent(f'''

        ## Progress — Batch 12CK

        - Seoul National University Kyujanggak directly catalogs `奎貴894-v.1-3《七政算內篇》` as 李純之、金淡受命編, `甲寅字`, publication year `1444`. A provider-renderer-bound no-OCR review of volume 0003 pages `039b..044b` localizes and reads the complete `二至後日出入晝夜辰刻` table family.
        - The physical 1444 witness gives winter-solstice first-day `晝39 / 夜61`, pre-summer day 159 `晝60 / 夜40`, and summer-solstice first-day `晝61 / 夜39`. This is not a Nanjing `59/41` table.
        - The official National Institute of Korean History Sillok route is now exactly bound: `wda_50034001` = 冬至後 and `wda_50034002` = 夏至後 + the statement that the Inner Chapter uses the Hanyang solstitial gnomon to derive daily sunrise/sunset and day/night values `定爲本國所用`. The previously probed `wda_50018...` prefix is recorded as a locator inference error only.
        - Combined with the already audited 1447 Ming memorial (`南京59`, `北京62`), the evidence establishes near-contemporary regional calibration as a first-order variable: Hanyang 61, Nanjing 59, Beijing 62. Numeric similarity alone is therefore insufficient for lineage claims.
        - For the 1578 Sanming `59/41` table, Hanyang becomes a parallel regional negative control rather than a proposed direct parent. The next ancestry gate should prioritize securely localized Nanjing/Jiangnan or other 59-ke-cap intermediaries with Huqian-like step ladders/change-day fingerprints.
        - `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; upper-Zi→Hai vote +0; runtime winner/candidate collapse/algorithm reopen remain none/0. Matrix counts and deterministic product invariants are unchanged.

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
        "Batch 12CK directly binds the 1444 Kyujanggak 奎貴894-v.1-3 Gabinja witness and its G894 physical day/night pages: Hanyang reaches winter 39/61 and summer 61/39.",
        "Batch 12CK fixes the Sejong 158 locator route to wda_50034: official article wda_50034002 states that the Inner Chapter derives daily sunrise/sunset and day/night values from the Hanyang solstitial gnomon for domestic use. The earlier wda_50018 probe was a research-locator inference error, not source absence.",
        "Batch 12CK establishes regional calibration as an explicit genealogy variable: near-contemporary Hanyang 61, Nanjing 59, and Beijing 62 cannot be collapsed into one universal solstitial-ke tradition. Sanming 59/41 ancestry search is therefore narrowed toward 59-ke-cap regional intermediaries rather than generic East-Asian day/night tables."
    ]
    for x in additions:
        if x not in h["current_focus"]:
            h["current_focus"].append(x)
    d["schema_version"] = "1.97.0"
    d["updated_at"] = "2026-09-15"
    dump(p, d)


def write_doc() -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit — Batch 12CK

    ## Scope

    This batch closes a regional-calibration control that emerged after Batch 12CJ. It asks whether the directly dated 1444 Joseon `《七政算內篇》` witness preserves a Hanyang-localized sunrise/sunset and day/night-ke table, and whether that localization changes how we should read the 1447 Nanjing/Beijing standards and the later 1578 `《三命通會》` 59/41 display.

    This is historical provenance / transmission-genealogy work only. It does **not** reopen deterministic charting and does not select any runtime candidate.

    ## 1. Bibliographic firewall: G894 is a dated 1444 witness

    The Seoul National University Kyujanggak provider catalog identifies:

    ```text
    title: 七政算內篇
    call number: 奎貴894-v.1-3
    compilers: 李純之、金淡（朝鮮）受命編
    edition: 甲寅字
    publication year: 1444
    provider book_cd: GK00894_00
    ```

    The 1444 attribution comes from the provider bibliography. It is not inferred from image filenames or from a modern surrogate.

    ## 2. Direct physical table collation: no OCR for glyph claims

    GitHub Actions run `{G894_RUN}` fetched provider pages `039b..044b` from volume `0003`. Every image path was parsed from the Kyujanggak renderer response for the requested page ID; filename-sequence inference is forbidden. Artifact `{G894_ARTIFACT}` has digest `{G894_ARTIFACT_DIGEST}`.

    Key direct readings:

    ```text
    040a  二至後日出入晝夜辰刻 / 冬至後
          初日 日出辰初一刻 日入申正二刻
          晝三十九刻 / 夜六十一刻

    042a  一百五十九日
          晝六十刻 / 夜四十刻

    042a  夏至後
          初日 日出寅正二刻 日入戌初一刻
          晝六十一刻 / 夜三十九刻
    ```

    Therefore the directly reviewed Hanyang table is a 100-ke regional table with solstitial extremes:

    ```text
    winter: 39 / 61
    summer: 61 / 39
    ```

    ## 3. Official Sillok article binding and locator repair

    The earlier research locator scanned a guessed `wda_50018...` prefix. That guess was wrong. It was never admissible evidence and must not be reinterpreted as a negative historical result.

    The corrected provider route is `wda_50034...`. Run `{SILLOK_RUN}` proves:

    ```text
    wda_50034001
      世宗實錄 158卷 / 內篇 下卷 / 二至後日出入晝夜辰刻 / 冬至後
      太白山事故本 62책 158권 28장 A면

    wda_50034002
      世宗實錄 158卷 / 內篇 下卷 / 二至後日出入晝夜辰刻 / 夏至後
      太白山事故本 62책 158권 29장 B면
    ```

    The official institutional transcription on `wda_50034002` states:

    > 日出入隨處各異，諸曆不同。內篇據漢陽日至之晷，推求至差，得每日日出入，晝夜刻分，定爲本國所用。

    This wording is used as an official transcriptional witness. The table numerals above are independently adjudicated from the G894 physical-page images.

    ## 4. Historical adjudication: locality is explicit, not retrospective

    The combined evidence allows a stronger claim than mere numerical comparison:

    1. the 1444 physical G894 witness supplies the Hanyang table and its 39↔61 extrema;
    2. the official Sillok text explicitly says sunrise/sunset differ by place and that the Inner Chapter derives its daily values from the **Hanyang solstitial gnomon** for domestic use;
    3. the already audited 1447 Ming memorial directly distinguishes Nanjing `59` ke from Beijing `62` ke.

    Hence `region/locality` is an explicitly attested historical variable in 15th-century East-Asian day/night-ke practice. A single universal solstitial-ke value is rejected.

    ## 5. Consequence for the Sanming 59/41 ancestry problem

    The result does **not** make Hanyang a parent of the 1578 `《三命通會》` table. Quite the opposite:

    ```text
    1444 Hanyang: summer 61/39
    1447 Nanjing: 59/(41 complement)
    1447 Beijing: 62/(38 complement)
    1578 Sanming: summer 59/41
    ```

    Hanyang is therefore a high-value parallel regional negative control. It proves that generic phrases such as “traditional day/night-ke table” or mere proximity to 60 cannot establish a direct lineage. The Sanming search should now privilege securely localized Nanjing/Jiangnan or other `59`-cap intermediaries that also reproduce its step-ladder/change-day fingerprint.

    This does not erase the Huqianjing structural ancestry candidate from Batch 12CJ. It sharpens the missing bridge: a viable intermediary must explain **both** the inherited one-ke operational family **and** the regional/quantization move to a 59-ke cap.

    ## 6. Tianwen transmission impact

    New graph nodes:

    ```text
    PHYSICAL-COPY-CHILJEONGSAN-NAEPYEON-G894-1444
    PASSAGE-SEJONG158-HANYANG-LOCAL-CALIBRATION
    STANDARD-HANYANG-61KE-1444
    ```

    New edges:

    ```text
    G894 physical copy
      --ATTESTS--> Hanyang 61-ke regional standard

    Sejong 158 locality passage
      --ATTESTS--> Hanyang 61-ke regional standard

    Hanyang 61-ke regional standard
      --PARALLEL_COEXISTS_WITH--> Nanjing 59-ke 1447 standard
    ```

    No transmission direction between Hanyang and Nanjing is inferred. No Hanyang -> Sanming direct-copy edge is asserted.

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

    The failed `wda_50018` locator is a research-tool defect only. It is not a product/provenance-metadata defect-counter increment.

    ## 8. Next gate

    1. search pre-1578 Nanjing/Jiangnan or another securely localized intermediary that combines a Huqian-style intra-term one-ke ladder with a `59`-ke cap or Sanming-like change-day fingerprint;
    2. search for an explicit historical selection/rounding instruction capable of explaining the Batch 12CI `(78,81]/147` precision-to-coarse threshold;
    3. continue the independent Fullbook upper-five-ke -> previous-night Hai lineage without conflating it with seasonal-table ancestry.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def main() -> int:
    continuity()
    registry()
    research()
    graph()
    graph_verifier()
    matrix()
    matrix_md()
    state()
    write_doc()
    print("BATCH_12CK_FORMALIZATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
