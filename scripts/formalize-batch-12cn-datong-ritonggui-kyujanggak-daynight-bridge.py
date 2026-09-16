from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-DATONG-RITONGGUI-KYUJANGGAK-DAYNIGHT-BRIDGE-CN"
PREV_ID = "BATCH-12-ZIWEI-ZHOUXIANG-DAMING-DATONG-1569-1477-COMPUTATION-REPRINT-CONTROL-CM"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-DATONG-RITONGGUI-KYUJANGGAK-DAYNIGHT-BRIDGE-CN.md"
RESEARCH = "docs/research/ZIWEI-DATONG-RITONGGUI-KYUJANGGAK-DAYNIGHT-BRIDGE-R1.json"
KOSTMA_ID = "EXT-KOSTMA-DATONGLI-RITONGGUI-DIC-A3-000150"
KYU_ID = "EXT-KYUJANGGAK-DATONGLI-RITONGGUI-GR35954-LEGACY"
DIC_ID = "DIC_A3_000150"
HOLDING_ID = "GR35954_00"
DICVIEW_RUN_ID = 35057301901
DICVIEW_JOB_ID = 104670045742
ROUTE_RUN_ID = 35057437846
ROUTE_JOB_ID = 104670447349
KOSTMA_URL = "https://kostma.aks.ac.kr/dic/dicMain.aspx?mT=A&searchid=DIC_A3_000150"
DICVIEW_URL = "https://kostma.aks.ac.kr/dic/dicView.aspx?searchid=DIC_A3_000150"
LEGACY_URL = "http://e-kyujanggak.snu.ac.kr/MOK/CONVIEW.jsp?ptype=list&subtype=oo&lclass=01&mclass=B124&sclass=G&ntype=oo&cn=GR35954_00"


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate Batch 12CM tail in continuity verifier")
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
    if KOSTMA_ID not in ids:
        d["sources"].append({
            "source_id": KOSTMA_ID,
            "title": "대통력일통궤(大統曆日通軌) KOSTMA institutional dictionary record",
            "historical_period": "JOSEON_SEJONG_REFORM_RECORD_DATED_1433_1445; PHYSICAL_IMPRESSION_DATE_NOT_INDEPENDENTLY_REVERIFIED_HERE",
            "provider": "한국학자료센터 KOSTMA / 한국학중앙연구원",
            "url": KOSTMA_URL,
            "source_role": "INSTITUTIONAL_CONTENT_AND_HOLDING_BINDING_RECORD_FOR_PRE_1578_DATONG_RITONGGUI_DAYNIGHT_TABLE_FAMILY",
            "quality_notes": "Direct dicView retrieval in Batch 12CN identifies the record as 大統曆日通軌, dates the represented Joseon compilation context to 1433-1445, names Seoul National University Kyujanggak Institute for Korean Studies as repository, and explicitly describes 日出入晨刻表, 晝夜刻分表, and 四方每時初昏去中星度數表. This is institutional database evidence, not a substitute for direct facsimile glyph or numeric-cell collation."
        })
    if KYU_ID not in ids:
        d["sources"].append({
            "source_id": KYU_ID,
            "title": "Kyujanggak legacy object binding for 大統曆日通軌",
            "provider": "Seoul National University Kyujanggak legacy e-kyujanggak route emitted by KOSTMA",
            "url": LEGACY_URL,
            "source_role": "PHYSICAL_HOLDING_LOCATOR_AND_CURRENT_ACCESS_BOUNDARY_CONTROL",
            "quality_notes": "KOSTMA dicView emits the legacy Kyujanggak CONVIEW binding with cn=GR35954_00. Batch 12CN direct route probe observes HTTP 404 on the legacy HTTP endpoint and connection reset on HTTPS from GitHub Actions. Therefore the holding/object binding is recorded, while scan availability, physical impression details, and page-glyph authority remain unresolved."
        })
    d["access_date"] = "2026-09-16"
    dump(p, d)


def research() -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-DATONG-RITONGGUI-KYUJANGGAK-DAYNIGHT-BRIDGE-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Does a pre-1578 Datong Tonggui-line witness explicitly contain sunrise/sunset and day/night-ke tables relevant to the Sanming 1578 day/night-ke ancestry search, and what is the strongest current physical-object binding?",
        "evidence_runs": {
            "kostma_dicview": {
                "workflow_run_id": DICVIEW_RUN_ID,
                "job_id": DICVIEW_JOB_ID,
                "record_id": DIC_ID,
                "record_url": KOSTMA_URL,
                "dicview_url": DICVIEW_URL
            },
            "kyujanggak_legacy_route": {
                "workflow_run_id": ROUTE_RUN_ID,
                "job_id": ROUTE_JOB_ID,
                "holding_identifier": HOLDING_ID,
                "legacy_url": LEGACY_URL,
                "http_result": "HTTP_404_NOT_FOUND",
                "https_result": "CONNECTION_RESET_BY_PEER_FROM_GITHUB_RUNNER"
            }
        },
        "institutional_record_direct_fields": {
            "title_hanja": "大統曆日通軌",
            "title_hangul": "대통력일통궤",
            "record_id": DIC_ID,
            "record_type": "고서/기술서",
            "recorded_creation_context": "1433-1445 (Sejong-era calendar-reform context in the institutional record)",
            "repository": "서울대학교 규장각한국학연구원",
            "explicit_table_families": [
                "日出入晨刻表 — sunrise/sunset morning-ke table by the 24 solar terms",
                "晝夜刻分表 — day/night ke-fen table",
                "四方每時初昏去中星度數表 — initial-dusk stellar-degree table by direction/time"
            ],
            "lineage_summary": "The record describes the work as produced in the Joseon Sejong calendar-reform context on the basis of Ming/Datong calendrical principles associated with Yuan Tong's tradition.",
            "numeric_cells_directly_collated": False,
            "physical_page_glyphs_directly_collated": False
        },
        "physical_object_binding": {
            "repository": "Seoul National University Kyujanggak Institute for Korean Studies",
            "legacy_identifier": HOLDING_ID,
            "legacy_conview_binding_emitted_by_kostma": True,
            "legacy_http_current_status": "404_NOT_FOUND",
            "legacy_https_current_status": "RUNNER_CONNECTION_RESET",
            "current_scan_obtained": False,
            "physical_impression_date_independently_verified_from_scan_or_live_item_page": False,
            "rule": "Do not convert the institutional record or legacy identifier into a claim that a specific physical scan or Ming-China edition has been directly inspected."
        },
        "date_and_recension_firewall": {
            "underlying_work_lineage": "Datong/Tonggui technical lineage attributed in the institutional record to the Ming calendrical tradition associated with Yuan Tong.",
            "joseon_compilation_recension_layer": "Institutional record places the represented Joseon technical compilation in the Sejong-era 1433-1445 reform context.",
            "physical_holding_layer": "Kyujanggak legacy object identifier GR35954_00; exact impression/copy description remains unverified through a presently reachable item page or scan in this batch.",
            "digital_metadata_layer": "KOSTMA dictionary record DIC_A3_000150 and its current/legacy routing surfaces.",
            "forbidden_collapse": "Do not call GR35954_00 a Chinese Ming Zhengtong physical edition merely because the underlying work lineage and historical era are Ming-contemporary."
        },
        "historical_adjudication": {
            "pre_1578_daynight_table_family_witness_recorded": True,
            "explicit_daynight_table_family": True,
            "explicit_sunrise_sunset_table_family": True,
            "direct_physical_scan_reviewed": False,
            "exact_numeric_table_match_to_sanming_1578_proved": False,
            "nanjing_59_ke_cap_proved_for_this_witness": False,
            "daily_ladder_change_day_match_proved": False,
            "rounding_quantization_rule_proved": False,
            "sanming_direct_parentage_proved": False,
            "impact": "The search gate advances from existence/title-level uncertainty to a concrete pre-1578 Joseon Datong-line technical record that explicitly contains the required sunrise/sunset and day/night-ke table classes. The next gate is numeric and stemmatic, not merely bibliographic."
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
            "Acquire a lawful readable scan or replacement first-party item surface for GR35954_00 and collate the actual 日出入晨刻表 / 晝夜刻分表 cells.",
            "Test whether the table's solstitial cap, daily ladder, and intra-term change days reproduce the Nanjing 59/41 and Sanming 1578 stepped display fingerprints.",
            "Continue pre-1578 annual Datong almanac and 楊瓚《閑中錄》 search in parallel, because a Joseon recension cannot by itself prove the exact Chinese Sanming transmission path.",
            "Keep Batch 12CI quantization/rounding selection unresolved until an explicit historical rule or exact table-cell reconstruction closes it."
        ]
    })


def graph() -> None:
    p = Path("docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    node_ids = {x.get("node_id") for x in d["nodes"]}
    nodes = [
        {
            "node_id": "CATALOG-KOSTMA-DATONGLI-RITONGGUI-DIC-A3-000150",
            "node_type": "CATALOG_RECORD",
            "label": "KOSTMA 大統曆日通軌 DIC_A3_000150",
            "system_scope": "DATONG_TONGGUI_DAYNIGHT_TABLE_TRANSMISSION",
            "date": "MODERN_INSTITUTIONAL_DATABASE_RECORD; HISTORICAL_CONTEXT_RECORDED_AS_1433_1445",
            "locator": KOSTMA_URL,
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        },
        {
            "node_id": "RECENSION-JOSEON-SEJONG-DATONGLI-RITONGGUI-1433-1445",
            "node_type": "RECENSION",
            "label": "朝鮮世宗期《大統曆日通軌》技術編纂層（1433–1445記錄範圍）",
            "system_scope": "DATONG_TONGGUI_DAYNIGHT_TABLE_TRANSMISSION",
            "work_composition_date": "SEJONG_REFORM_CONTEXT_1433_1445_PER_KOSTMA_RECORD",
            "edition_impression_date": "NOT_INDEPENDENTLY_VERIFIED_FROM_CURRENT_SCAN_IN_BATCH_12CN",
            "physical_copy_date": "NOT_INDEPENDENTLY_VERIFIED",
            "digital_surrogate_date": "KOSTMA_CURRENT_METADATA_SURFACE",
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        },
        {
            "node_id": "HOLDING-KYUJANGGAK-GR35954_00-DATONGLI-RITONGGUI",
            "node_type": "PHYSICAL_HOLDING_LOCATOR",
            "label": "奎章閣《大統曆日通軌》legacy object GR35954_00",
            "system_scope": "DATONG_TONGGUI_PHYSICAL_PROVENANCE",
            "date": "CURRENT_HOLDING_BINDING; EXACT_PHYSICAL_IMPRESSION_DATE_UNRESOLVED",
            "locator": LEGACY_URL,
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        },
        {
            "node_id": "TABLE-FAMILY-JOSEON-DATONGLI-RITONGGUI-DAYNIGHT",
            "node_type": "TABLE_FAMILY",
            "label": "《大統曆日通軌》日出入晨刻表／晝夜刻分表 family",
            "system_scope": "DAYNIGHT_KE_TIMEKEEPING",
            "date": "SEJONG_REFORM_CONTEXT_1433_1445_PER_KOSTMA_RECORD",
            "locator": "KOSTMA DIC_A3_000150 content description; physical cells not yet directly collated",
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
            "edge_id": "TG-E0023",
            "from": "CATALOG-KOSTMA-DATONGLI-RITONGGUI-DIC-A3-000150",
            "relation": "DESCRIBES",
            "to": "RECENSION-JOSEON-SEJONG-DATONGLI-RITONGGUI-1433-1445",
            "status": "CONFIRMED",
            "confidence": "HIGH",
            "evidence_class": "DIRECT_INSTITUTIONAL_DATABASE_RECORD",
            "evidence": [RESEARCH],
            "adjudication_batch": BATCH_ID
        },
        {
            "edge_id": "TG-E0024",
            "from": "CATALOG-KOSTMA-DATONGLI-RITONGGUI-DIC-A3-000150",
            "relation": "BINDS_TO_HOLDING",
            "to": "HOLDING-KYUJANGGAK-GR35954_00-DATONGLI-RITONGGUI",
            "status": "CONFIRMED",
            "confidence": "HIGH_FOR_LEGACY_IDENTIFIER_BINDING_NOT_SCAN_ACCESS",
            "evidence_class": "SOURCE_EMITTED_LEGACY_KYUJANGGAK_CONVIEW_BINDING",
            "evidence": [RESEARCH],
            "adjudication_batch": BATCH_ID
        },
        {
            "edge_id": "TG-E0025",
            "from": "RECENSION-JOSEON-SEJONG-DATONGLI-RITONGGUI-1433-1445",
            "relation": "CONTAINS_TABLE_FAMILY",
            "to": "TABLE-FAMILY-JOSEON-DATONGLI-RITONGGUI-DAYNIGHT",
            "status": "CONFIRMED_AT_INSTITUTIONAL_CONTENT_RECORD_LEVEL",
            "confidence": "HIGH_FOR_TABLE_CLASS_MEDIUM_FOR_UNCOLLATED_PHYSICAL_CELLS",
            "evidence_class": "DIRECT_INSTITUTIONAL_CONTENT_DESCRIPTION",
            "evidence": [RESEARCH],
            "adjudication_batch": BATCH_ID
        }
    ]
    for edge in edges:
        if edge["edge_id"] not in edge_ids:
            d["edges"].append(edge)
            edge_ids.add(edge["edge_id"])
    non_edges = d.setdefault("explicit_non_edges", [])
    if not any(x.get("from") == "TABLE-FAMILY-JOSEON-DATONGLI-RITONGGUI-DAYNIGHT" and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE" for x in non_edges):
        non_edges.append({
            "from": "TABLE-FAMILY-JOSEON-DATONGLI-RITONGGUI-DAYNIGHT",
            "relation": "DIRECT_NUMERIC_PARENT_OF",
            "to": "TABLE-SANMING-1578-DAYNIGHT-KE",
            "status": "UNRESOLVED",
            "reason": "The institutional record proves the relevant pre-1578 table classes exist in the Joseon Datong-line recension, but Batch 12CN does not obtain the physical table cells, prove a Nanjing 59-ke cap, reproduce Sanming's daily ladder/change days, or establish direct Chinese transmission into Sanming.",
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
    rp["batch_12cn_datong_ritonggui_kyujanggak_daynight_bridge"] = {
        "source_ids": [KOSTMA_ID, KYU_ID],
        "institutional_record_directly_retrieved": True,
        "record_id": DIC_ID,
        "repository": "Seoul National University Kyujanggak Institute for Korean Studies",
        "legacy_holding_identifier": HOLDING_ID,
        "recorded_historical_context": "1433-1445_SEJONG_REFORM_CONTEXT",
        "sunrise_sunset_table_class_explicit": True,
        "daynight_ke_fen_table_class_explicit": True,
        "direct_physical_scan_reviewed": False,
        "legacy_http_route_status": "404_NOT_FOUND",
        "legacy_https_route_status": "CONNECTION_RESET_FROM_GITHUB_RUNNER",
        "exact_numeric_match_to_sanming_proved": False,
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
    if "## Progress — Batch 12CN" not in s:
        s += dedent(f'''

        ## Progress — Batch 12CN

        - Direct KOSTMA `dicView` retrieval binds `大統曆日通軌` to record `{DIC_ID}`, a Sejong-era `1433–1445` technical-compilation context, and Seoul National University Kyujanggak Institute for Korean Studies.
        - The institutional content record explicitly lists `日出入晨刻表`, `晝夜刻分表`, and `四方每時初昏去中星度數表`. This advances the Sanming ancestry search from title-level expectation to an explicit pre-1578 Datong-line day/night-table class witness.
        - KOSTMA also emits the legacy Kyujanggak object binding `{HOLDING_ID}`. Direct route probing records HTTP `404` on the old HTTP endpoint and a connection reset on HTTPS from the GitHub runner, so no physical scan or numeric cells are claimed as directly collated.
        - The date firewall remains strict: Ming/Datong underlying work lineage, Joseon Sejong recension/compilation context, the present Kyujanggak physical holding locator, and modern KOSTMA metadata are separate layers. The object is not relabeled as a Chinese Ming physical edition.
        - `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; no runtime candidate, winner, candidate collapse, chart algorithm defect, or algorithm reopen is created. The next gate is numeric/stemmatic: obtain the table cells and test the `59/41`, daily-ladder, change-day, and rounding fingerprints against Sanming 1578.

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
        "Batch 12CN directly retrieves KOSTMA DIC_A3_000150 for 大統曆日通軌: the institutional record places the represented Joseon technical compilation in the Sejong-era 1433-1445 reform context and explicitly lists 日出入晨刻表, 晝夜刻分表, and 四方每時初昏去中星度數表.",
        "Batch 12CN binds the KOSTMA record to Kyujanggak legacy object GR35954_00, but the old HTTP route is now 404 and HTTPS resets from the GitHub runner; physical scan/page-glyph/numeric-cell authority is therefore not claimed. Underlying Ming/Datong lineage, Joseon recension, physical holding, and modern metadata remain separate layers.",
        "The Sanming ancestry gate is now numeric/stemmatic rather than merely bibliographic: acquire GR35954_00 or an equivalent readable first-party facsimile and test its day/night cells for Nanjing 59/41, daily ladder/change-day, and Batch 12CI rounding fingerprints. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with no runtime change."
    ]
    for x in additions:
        if x not in h["current_focus"]:
            h["current_focus"].append(x)
    d["schema_version"] = "1.100.0"
    d["updated_at"] = "2026-09-16"
    dump(p, d)


def write_doc() -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit — Batch 12CN

    ## Scope

    Batch 12CM established that Zhou Xiang's 1569 public `《大明大統曆法》` fascicle is a genuine pre-1578 Datong technical witness but does not itself expose the required `晨昏分 / 日出入 / 晝夜刻` table. Batch 12CN therefore moves to the direct `《大統曆日通軌》` route.

    The result is a material narrowing of the ancestry problem: an institutional Korean record directly describes a Sejong-era Datong-line technical compilation containing both a sunrise/sunset table and a day/night-ke-fen table, and it exposes a concrete Kyujanggak legacy holding identifier. The physical scan remains inaccessible in the present route, so the evidence is recorded at the institutional-content/holding-binding level rather than promoted to page-glyph authority.

    ## 1. Direct KOSTMA record

    GitHub Actions run `{DICVIEW_RUN_ID}` / job `{DICVIEW_JOB_ID}` directly retrieved KOSTMA record `{DIC_ID}` for `대통력일통궤(大統曆日通軌)`.

    The record identifies:

    ```text
    title       大統曆日通軌
    record      DIC_A3_000150
    type        고서/기술서
    context     1433–1445 (Sejong-era calendar-reform context in the record)
    repository  서울대학교 규장각한국학연구원
    ```

    Most importantly, its content description explicitly enumerates three technical table families:

    1. `日出入晨刻表` — sunrise/sunset morning-ke table by the 24 solar terms;
    2. `晝夜刻分表` — day/night ke-fen table;
    3. `四方每時初昏去中星度數表` — initial-dusk stellar-degree table by direction/time.

    This is the first route in the present Sanming ancestry sequence that moves the target from a generic Datong title to an institutional record explicitly naming the required day/night table class before 1578.

    ## 2. Physical holding binding and access boundary

    The KOSTMA `dicView` surface emits an old Kyujanggak `CONVIEW` target with:

    ```text
    cn=GR35954_00
    ```

    Batch 12CN then probed the exact legacy route in run `{ROUTE_RUN_ID}` / job `{ROUTE_JOB_ID}`:

    ```text
    HTTP legacy route   -> 404 Not Found
    HTTPS legacy route  -> connection reset by peer from GitHub runner
    ```

    Therefore:

    ```text
    KYUJANGGAK_OBJECT_BINDING_GR35954_00 = CONFIRMED_AT_SOURCE_EMITTED_LOCATOR_LEVEL
    DIRECT_SCAN_OBTAINED = FALSE
    DIRECT_PHYSICAL_GLYPH_COLLATION = FALSE
    DIRECT_NUMERIC_CELL_COLLATION = FALSE
    ```

    A dead or reset viewer route is an access boundary, not evidence that the holding or table is absent.

    ## 3. Four-layer provenance firewall

    The following layers are deliberately not collapsed:

    ```text
    underlying work lineage  -> Ming/Datong Tonggui tradition associated by the record with Yuan Tong
    Joseon technical layer   -> Sejong-era 1433–1445 compilation/reform context in the institutional record
    physical holding layer   -> current Kyujanggak legacy object locator GR35954_00
    digital metadata layer   -> KOSTMA DIC_A3_000150 and current/legacy web routing
    ```

    In particular, `GR35954_00` is **not** called a Chinese Ming Zhengtong physical edition on the strength of title, era, or underlying work lineage. Exact physical impression/copy details remain subject to first-party item-page or scan verification.

    ## 4. What this proves — and what it does not

    Batch 12CN now supports:

    ```text
    PRE_1578_DATONG_LINE_DAYNIGHT_TABLE_CLASS_WITNESS = TRUE
    EXPLICIT_SUNRISE_SUNSET_TABLE_CLASS = TRUE
    EXPLICIT_DAYNIGHT_KE_FEN_TABLE_CLASS = TRUE
    CONCRETE_KYUJANGGAK_LEGACY_OBJECT_BINDING = TRUE
    ```

    It does **not** yet support:

    ```text
    GR35954_00_PHYSICAL_TABLE_CELLS_DIRECTLY_READ = FALSE
    NANJING_59_KE_CAP_IN_THIS_WITNESS = UNRESOLVED
    SANMING_59_41_NUMERIC_IDENTITY = UNRESOLVED
    DAILY_LADDER_CHANGE_DAY_IDENTITY = UNRESOLVED
    BATCH_12CI_ROUNDING_RULE = UNRESOLVED
    DIRECT_PARENTAGE_TO_SANMING_1578 = UNRESOLVED
    ```

    A Joseon recension is a valuable transmission witness but cannot by itself prove the exact Chinese line into Wan Minying's 1578 `《三命通會》`.

    ## 5. Tianwen transmission impact

    The graph now distinguishes four nodes: the modern KOSTMA record, the Joseon Sejong recension layer, the Kyujanggak holding locator, and the day/night table family described by the record. Confirmed edges are limited to what the database surface actually supports: the record describes the recension, binds to the holding locator, and the recension is described as containing the target table family.

    A direct numeric-parent edge from that table family to the Sanming 1578 day/night-ke table remains explicitly unresolved.

    ## 6. Product adjudication

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

    This evidence narrows the historical timekeeping ancestry search; it does not authorize a chart-runtime change.

    ## 7. Next gate

    1. acquire a lawful readable scan or replacement first-party item surface for `GR35954_00` and collate the actual `日出入晨刻表 / 晝夜刻分表` cells;
    2. test the solstitial cap, daily ladder, intra-term change days, and quantization against the Nanjing `59/41` and Sanming 1578 fingerprints;
    3. continue pre-1578 annual Datong almanac and `楊瓚《閑中錄》` search in parallel to avoid treating the Joseon recension as the Chinese transmission path by default;
    4. keep the Batch 12CI rounding/selection threshold open until explicit historical mechanics or exact cell reconstruction closes it.

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
    print("BATCH_12CN_FORMALIZATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
