from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

OLD_BATCH = "BATCH-12-ZIWEI-DATONG-RITONGGUI-KYUJANGGAK-DAYNIGHT-BRIDGE-CN"
REPAIR_BATCH = "BATCH-12-ZIWEI-DATONG-RITONGGUI-KOSTMA-ATTRIBUTION-REPAIR-CO"
OLD_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-DATONG-RITONGGUI-KYUJANGGAK-DAYNIGHT-BRIDGE-CN.md"
REPAIR_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-DATONG-RITONGGUI-KOSTMA-ATTRIBUTION-REPAIR-CO.md"
OLD_RESEARCH = "docs/research/ZIWEI-DATONG-RITONGGUI-KYUJANGGAK-DAYNIGHT-BRIDGE-R1.json"
REPAIR_RESEARCH = "docs/research/ZIWEI-DATONG-RITONGGUI-KOSTMA-ATTRIBUTION-REPAIR-R1.json"
AUDIT_WORKFLOW_RUN = 35058829315
AUDIT_JOB = 104674602946
DIC_ID = "DIC_A3_000150"
CORRECT_HOLDING = "GK12437_00"
WITHDRAWN_HOLDING = "GR35954_00"
KOSTMA_URL = "https://kostma.aks.ac.kr/dic/dicMain.aspx?mT=A&searchid=DIC_A3_000150"
DICVIEW_URL = "https://kostma.aks.ac.kr/dic/dicView.aspx?searchid=DIC_A3_000150"
KOSTMA_SOURCE_ID = "EXT-KOSTMA-DATONGLI-RITONGGUI-DIC-A3-000150"
WITHDRAWN_SOURCE_ID = "EXT-KYUJANGGAK-DATONGLI-RITONGGUI-GR35954-LEGACY"
CORRECT_HOLDING_SOURCE_ID = "EXT-KYUJANGGAK-DATONGLI-RITONGGUI-GK12437-BINDING"

EXACT_TABLES = [
    "太陽冬至前後二象盈初縮末限",
    "太陽夏至前後二象縮初盈末限",
    "太陰遲疾度立成",
]


def load(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(path: str, obj) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_external_registry() -> None:
    path = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
    d = load(path)
    by_id = {x.get("source_id"): x for x in d["sources"]}
    if KOSTMA_SOURCE_ID not in by_id or WITHDRAWN_SOURCE_ID not in by_id:
        raise SystemExit("Batch 12CN external-source records missing")

    kostma = by_id[KOSTMA_SOURCE_ID]
    kostma["source_role"] = "INSTITUTIONAL_CONTENT_RECORD_FOR_DATONG_RITONGGUI_SOLAR_LUNAR_COMPUTATION_TABLES_AND_SOURCE_EMITTED_KYUJANGGAK_BINDING"
    kostma["quality_notes"] = (
        "Batch 12CO re-audit of KOSTMA dicView DIC_A3_000150 confirms the title 大統曆日通軌 and "
        "the Sejong-era 1433-1445 compilation context, but the record lists exactly three computational tables: "
        "太陽冬至前後二象盈初縮末限, 太陽夏至前後二象縮初盈末限, and 太陰遲疾度立成. "
        "The prior Batch 12CN attribution of 日出入晨刻表 / 晝夜刻分表 / 四方每時初昏去中星度數表 to this record is withdrawn. "
        "The same re-audit exposes source-emitted Kyujanggak identifier GK12437_00, not GR35954_00."
    )
    kostma["correction_batch"] = REPAIR_BATCH

    withdrawn = by_id[WITHDRAWN_SOURCE_ID]
    withdrawn["title"] = "WITHDRAWN: GR35954_00 previously misattributed to 大統曆日通軌 DIC_A3_000150"
    withdrawn["source_role"] = "WITHDRAWN_MISATTRIBUTED_LOCATOR_RETAINED_FOR_AUDIT_TRACE_ONLY"
    withdrawn["quality_notes"] = (
        "Batch 12CO exact-record audit disproves the Batch 12CN binding of GR35954_00 to DIC_A3_000150. "
        "This registry entry is retained only as an audit-trace tombstone and must not be used as evidence for 大統曆日通軌. "
        "The corrected source-emitted identifier is GK12437_00."
    )
    withdrawn["correction_batch"] = REPAIR_BATCH

    if CORRECT_HOLDING_SOURCE_ID not in by_id:
        d["sources"].append({
            "source_id": CORRECT_HOLDING_SOURCE_ID,
            "title": "Kyujanggak source-emitted holding binding for 大統曆日通軌: GK12437_00",
            "historical_period": "MODERN_INSTITUTIONAL_HOLDING_BINDING; PHYSICAL_COPY_DATE_NOT_INDEPENDENTLY_VERIFIED_HERE",
            "provider": "KOSTMA dicView record DIC_A3_000150 / Seoul National University Kyujanggak binding",
            "url": DICVIEW_URL,
            "source_role": "CORRECTED_SOURCE_EMITTED_PHYSICAL_HOLDING_IDENTIFIER_BINDING",
            "quality_notes": (
                "Batch 12CO audit run 35058829315 / job 104674602946 directly re-read DIC_A3_000150 and found "
                "the Kyujanggak identifier GK12437_00. This proves the metadata binding only; no live first-party item page, "
                "physical impression date, facsimile glyph, or table cell is claimed as directly inspected."
            )
        })
    d["access_date"] = "2026-09-16"
    dump(path, d)


def rewrite_research() -> None:
    corrected = {
        "schema": "ZIWEI-DATONG-RITONGGUI-KYUJANGGAK-DAYNIGHT-BRIDGE-R1",
        "schema_version": "1.1.0",
        "batch_id": OLD_BATCH,
        "correction_batch_id": REPAIR_BATCH,
        "status": "CORRECTED_AFTER_EXACT_RECORD_ATTRIBUTION_AUDIT",
        "question": "What does KOSTMA DIC_A3_000150 actually attest, and does it prove a pre-1578 Datong-line day/night-ke table witness?",
        "correction_audit": {
            "workflow_run_id": AUDIT_WORKFLOW_RUN,
            "job_id": AUDIT_JOB,
            "record_id": DIC_ID,
            "record_url": KOSTMA_URL,
            "dicview_url": DICVIEW_URL,
            "method": "Exact-record re-fetch with term-by-term field attribution and identifier extraction"
        },
        "institutional_record_direct_fields": {
            "title_hanja": "大統曆日通軌",
            "title_hangul": "대통력일통궤",
            "record_id": DIC_ID,
            "recorded_creation_context": "1433-1445 (Sejong-era calendar-reform context in KOSTMA)",
            "repository": "서울대학교 규장각한국학연구원",
            "tables_actually_listed": EXACT_TABLES,
            "daynight_table_names_present": False,
            "sunrise_sunset_table_name_present": False,
            "numeric_cells_directly_collated": False,
            "physical_page_glyphs_directly_collated": False
        },
        "holding_binding": {
            "correct_source_emitted_identifier": CORRECT_HOLDING,
            "withdrawn_misattributed_identifier": WITHDRAWN_HOLDING,
            "correct_binding_level": "SOURCE_EMITTED_METADATA_IDENTIFIER_ONLY",
            "first_party_item_page_directly_opened": False,
            "current_scan_obtained": False,
            "physical_impression_date_independently_verified": False
        },
        "withdrawn_batch_12cn_claims": [
            "DIC_A3_000150 explicitly lists 日出入晨刻表",
            "DIC_A3_000150 explicitly lists 晝夜刻分表",
            "DIC_A3_000150 explicitly lists 四方每時初昏去中星度數表",
            "DIC_A3_000150 binds to GR35954_00",
            "DIC_A3_000150 establishes a pre-1578 Datong-line day/night-table-class witness"
        ],
        "historical_adjudication": {
            "datong_ritonggui_bibliographic_and_computational_witness": True,
            "pre_1578_daynight_table_family_witness_recorded": False,
            "explicit_daynight_table_family": False,
            "explicit_sunrise_sunset_table_family": False,
            "direct_physical_scan_reviewed": False,
            "exact_numeric_table_match_to_sanming_1578_proved": False,
            "nanjing_59_ke_cap_proved_for_this_witness": False,
            "daily_ladder_change_day_match_proved": False,
            "rounding_quantization_rule_proved": False,
            "sanming_direct_parentage_proved": False,
            "impact": "The Batch 12CN day/night bridge is withdrawn. DIC_A3_000150 remains useful as a Sejong-era Datong/Tonggui computational witness, but the ancestry search returns to an unresolved table-level gate."
        },
        "product_adjudication": {
            "matrix_rule_id": "HPA-ZDATE-006",
            "status": "MISSING_FROM_PRODUCT",
            "new_runtime_candidate": False,
            "runtime_winner": False,
            "candidate_collapse": False,
            "confirmed_chart_algorithm_defect_count": 0,
            "algorithm_reopen_count": 0,
            "deterministic_product_state": "CLOSED"
        },
        "next_gate": [
            "Do not use DIC_A3_000150 as day/night-table evidence unless a readable page or first-party record actually exposes such material.",
            "Investigate DIC_A3_000151 大統曆註 separately: its general 日月出入 / 晝夜長短 description is not equivalent to an identified numerical table.",
            "Continue pre-1578 annual Datong almanac, 楊瓚《閑中錄》, and other first-party table witnesses for explicit 晨昏分 / 日出入 / 晝夜刻 cells.",
            "Keep Nanjing 59/41, Sanming 1578 stepped display, and Batch 12CI rounding/quantization ancestry unresolved."
        ]
    }
    dump(OLD_RESEARCH, corrected)
    repair = {
        "schema": "ZIWEI-DATONG-RITONGGUI-KOSTMA-ATTRIBUTION-REPAIR-R1",
        "schema_version": "1.0.0",
        "batch_id": REPAIR_BATCH,
        "repairs_batch": OLD_BATCH,
        "audit_run_id": AUDIT_WORKFLOW_RUN,
        "audit_job_id": AUDIT_JOB,
        "defect_class": "PROVENANCE_METADATA_WRONG_RECORD_FIELD_AND_HOLDING_ATTRIBUTION",
        "before": {
            "record_id": DIC_ID,
            "claimed_daynight_tables": ["日出入晨刻表", "晝夜刻分表", "四方每時初昏去中星度數表"],
            "claimed_holding": WITHDRAWN_HOLDING
        },
        "after": {
            "record_id": DIC_ID,
            "tables_actually_listed": EXACT_TABLES,
            "daynight_table_claim": "WITHDRAWN_NOT_PRESENT_IN_EXACT_RECORD_AUDIT",
            "correct_holding_identifier": CORRECT_HOLDING,
            "holding_binding_authority": "SOURCE_EMITTED_METADATA_IDENTIFIER_ONLY"
        },
        "runtime_impact": "NONE",
        "deterministic_product_state": "CLOSED"
    }
    dump(REPAIR_RESEARCH, repair)


def update_matrix() -> None:
    path = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
    d = load(path)
    row = next((x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006"), None)
    if row is None:
        raise SystemExit("HPA-ZDATE-006 missing")
    rp = row.setdefault("research_progress", {})
    key = "batch_12cn_datong_ritonggui_kyujanggak_daynight_bridge"
    if key not in rp:
        raise SystemExit("Batch 12CN matrix progress object missing")
    rp[key] = {
        "status": "CORRECTED_BY_BATCH_12CO",
        "record_id": DIC_ID,
        "record_context": "Sejong-era 1433-1445 Datong/Tonggui computational compilation context per KOSTMA",
        "tables_actually_listed": EXACT_TABLES,
        "explicit_daynight_table_family": False,
        "explicit_sunrise_sunset_table_family": False,
        "correct_source_emitted_holding_identifier": CORRECT_HOLDING,
        "withdrawn_misattributed_holding_identifier": WITHDRAWN_HOLDING,
        "direct_scan_reviewed": False,
        "ancestry_gate": "UNRESOLVED_TABLE_LEVEL_EVIDENCE",
        "correction_batch": REPAIR_BATCH,
        "research_artifact": OLD_RESEARCH
    }
    rp["batch_12co_kostma_attribution_repair"] = {
        "audit_run_id": AUDIT_WORKFLOW_RUN,
        "audit_job_id": AUDIT_JOB,
        "defect": "WRONG_RECORD_FIELD_AND_HOLDING_ATTRIBUTION",
        "repair": "WITHDRAW_DAYNIGHT_TABLE_CLASS_CLAIM_AND_GR35954_BINDING; RETAIN_VALID_DATONG_COMPUTATIONAL_WITNESS; BIND_METADATA_TO_GK12437",
        "runtime_change": False,
        "research_artifact": REPAIR_RESEARCH
    }
    dump(path, d)

    md_path = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md")
    s = md_path.read_text(encoding="utf-8")
    marker = "\n## Progress — Batch 12CN"
    if marker not in s:
        raise SystemExit("Batch 12CN matrix markdown section missing")
    s = s.split(marker, 1)[0].rstrip() + "\n\n" + dedent(f"""
    ## Progress — Batch 12CN (corrected by Batch 12CO)

    - KOSTMA `DIC_A3_000150` remains a valid `大統曆日通軌` institutional record in a Sejong-era `1433–1445` calendrical-reform context.
    - Exact-record re-audit shows that the record lists `{'`, `'.join(EXACT_TABLES)}`. It does **not** list `日出入晨刻表`, `晝夜刻分表`, or `四方每時初昏去中星度數表` in the audited record.
    - The source-emitted Kyujanggak identifier is `{CORRECT_HOLDING}`. The prior `{WITHDRAWN_HOLDING}` attribution is withdrawn.
    - Therefore Batch 12CN no longer establishes a pre-1578 Datong-line day/night-table-class witness. `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; no runtime change is authorized.

    ## Progress — Batch 12CO

    - Exact attribution audit: GitHub Actions run `{AUDIT_WORKFLOW_RUN}` / job `{AUDIT_JOB}`.
    - Provenance defect repaired across the external-source registry, matrix progress, research record, transmission graph, Batch 12CN narrative, continuity state, and formalizer guard.
    - Defect class: `PROVENANCE_METADATA_WRONG_RECORD_FIELD_AND_HOLDING_ATTRIBUTION`.
    - The valid evidence retained is bibliographic/computational (`大統曆日通軌`, its three solar/lunar computational tables, and metadata binding `{CORRECT_HOLDING}`), not a day/night-ke numerical table witness.
    - The next gate returns to direct table discovery and page-level collation; `59/41`, daily ladders, change days, rounding, and direct Sanming parentage remain unresolved.

    Batch document: `{REPAIR_DOC}`. Research record: `{REPAIR_RESEARCH}`.
    """).lstrip()
    md_path.write_text(s, encoding="utf-8")


def update_graph() -> None:
    path = "docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json"
    d = load(path)
    nodes = d["nodes"]
    by_id = {x.get("node_id"): x for x in nodes}
    catalog_id = "CATALOG-KOSTMA-DATONGLI-RITONGGUI-DIC-A3-000150"
    recension_id = "RECENSION-JOSEON-SEJONG-DATONGLI-RITONGGUI-1433-1445"
    wrong_holding_node = "HOLDING-KYUJANGGAK-GR35954_00-DATONGLI-RITONGGUI"
    wrong_table_node = "TABLE-FAMILY-JOSEON-DATONGLI-RITONGGUI-DAYNIGHT"
    correct_holding_node = "HOLDING-KYUJANGGAK-GK12437_00-DATONGLI-RITONGGUI"
    for required in (catalog_id, recension_id, wrong_holding_node, wrong_table_node):
        if required not in by_id:
            raise SystemExit(f"expected Batch 12CN graph node missing: {required}")
    by_id[catalog_id]["system_scope"] = "DATONG_TONGGUI_CALENDRICAL_COMPUTATION_TRANSMISSION"
    by_id[catalog_id]["evidence"] = [OLD_RESEARCH, REPAIR_RESEARCH]
    by_id[recension_id]["system_scope"] = "DATONG_TONGGUI_CALENDRICAL_COMPUTATION_TRANSMISSION"
    by_id[recension_id]["evidence"] = [OLD_RESEARCH, REPAIR_RESEARCH]
    d["nodes"] = [x for x in nodes if x.get("node_id") not in {wrong_holding_node, wrong_table_node}]
    d["nodes"].append({
        "node_id": correct_holding_node,
        "node_type": "PHYSICAL_COPY",
        "label": "奎章閣《大統曆日通軌》source-emitted holding identifier GK12437_00",
        "system_scope": "DATONG_TONGGUI_PHYSICAL_PROVENANCE",
        "date": "CURRENT_METADATA_BINDING; EXACT_PHYSICAL_IMPRESSION_DATE_UNRESOLVED",
        "locator": "KOSTMA DIC_A3_000150 source-emitted identifier GK12437_00; first-party item page not directly inspected in Batch 12CO",
        "evidence": [REPAIR_RESEARCH],
        "first_explicit_graph_batch": REPAIR_BATCH
    })
    edges = []
    for e in d["edges"]:
        if e.get("edge_id") == "TG-E0025":
            continue
        if e.get("edge_id") == "TG-E0023":
            e["evidence"] = [OLD_RESEARCH, REPAIR_RESEARCH]
            e["adjudication_batch"] = REPAIR_BATCH
        if e.get("edge_id") == "TG-E0024":
            e["to"] = correct_holding_node
            e["status"] = "CONFIRMED"
            e["confidence"] = "HIGH_FOR_SOURCE_EMITTED_IDENTIFIER_ONLY"
            e["evidence_class"] = "EXACT_KOSTMA_RECORD_IDENTIFIER_EXTRACTION"
            e["evidence"] = [REPAIR_RESEARCH]
            e["adjudication_batch"] = REPAIR_BATCH
        if e.get("from") in {wrong_holding_node, wrong_table_node} or e.get("to") in {wrong_holding_node, wrong_table_node}:
            continue
        edges.append(e)
    d["edges"] = edges
    d["updated_at"] = "2026-09-16"
    dump(path, d)


def rewrite_batch_docs() -> None:
    Path(OLD_DOC).write_text(dedent(f"""
    # Batch 12CN — 大統曆日通軌 KOSTMA route (corrected by Batch 12CO)

    Status: **CORRECTED / SUPERSEDED FOR ATTRIBUTION CLAIMS BY `{REPAIR_BATCH}`**

    ## What remains valid

    KOSTMA record `{DIC_ID}` identifies `대통력일통궤(大統曆日通軌)` in a Sejong-era `1433–1445` calendrical-reform context and associates the record with Seoul National University Kyujanggak Institute for Korean Studies. This remains useful evidence for a Datong/Tonggui calendrical-computation witness.

    ## What Batch 12CO corrected

    Exact-record re-audit (Actions run `{AUDIT_WORKFLOW_RUN}` / job `{AUDIT_JOB}`) shows that `{DIC_ID}` lists the following three tables:

    1. `太陽冬至前後二象盈初縮末限`
    2. `太陽夏至前後二象縮初盈末限`
    3. `太陰遲疾度立成`

    The audited record does **not** support the previous Batch 12CN attribution of `日出入晨刻表`, `晝夜刻分表`, or `四方每時初昏去中星度數表` to `{DIC_ID}`.

    The same audit identifies the source-emitted Kyujanggak holding identifier as `{CORRECT_HOLDING}`. The former `{WITHDRAWN_HOLDING}` association is withdrawn as a provenance attribution error.

    ## Adjudication

    ```text
    DIC_A3_000150_AS_DATONG_COMPUTATIONAL_WITNESS = RETAINED
    DIC_A3_000150_EXPLICIT_DAYNIGHT_TABLE_CLASS = WITHDRAWN_NOT_ATTESTED
    DIC_A3_000150_HOLDING_GK12437_00 = CONFIRMED_AT_SOURCE_EMITTED_METADATA_LEVEL
    DIC_A3_000150_HOLDING_GR35954_00 = WITHDRAWN_MISATTRIBUTION
    PRE_1578_DAYNIGHT_TABLE_BRIDGE_FROM_THIS_RECORD = NOT_PROVED
    59_41_NUMERIC_MATCH = NOT_PROVED
    SANMING_1578_DIRECT_PARENTAGE = NOT_PROVED
    RUNTIME_CHANGE = NONE
    ```

    The deterministic fusion-chart product remains closed. This correction is provenance-only and does not reopen any chart algorithm.

    See `{REPAIR_DOC}` and `{REPAIR_RESEARCH}` for the correction record.
    """).lstrip(), encoding="utf-8")

    Path(REPAIR_DOC).write_text(dedent(f"""
    # Batch 12CO — 《大統曆日通軌》KOSTMA 证据归属纠错

    ## Scope

    This batch repairs a provenance metadata defect introduced by Batch 12CN. It does not alter deterministic chart runtime behavior.

    ## 1. Trigger

    A cross-check against the current Korean institutional description conflicted with the earlier Batch 12CN claim that KOSTMA `{DIC_ID}` explicitly contained day/night table families. A dedicated exact-record audit was therefore run rather than propagating the conflict.

    Evidence run: GitHub Actions `{AUDIT_WORKFLOW_RUN}` / job `{AUDIT_JOB}`.

    ## 2. Exact-record result

    `{DIC_ID}` / `大統曆日通軌` lists exactly the following relevant computational tables in the audited record:

    - `太陽冬至前後二象盈初縮末限`
    - `太陽夏至前後二象縮初盈末限`
    - `太陰遲疾度立成`

    No audited field hit supports `日出入晨刻表`, `晝夜刻分表`, or `四方每時初昏去中星度數表` as contents of this record.

    ## 3. Holding-identifier repair

    The exact-record audit yields Kyujanggak identifier `{CORRECT_HOLDING}` for `{DIC_ID}`. The earlier `{WITHDRAWN_HOLDING}` binding is withdrawn and retained only as an audit-trace tombstone in the external-source registry.

    The `{CORRECT_HOLDING}` binding is **metadata-level only**. This batch does not claim a directly opened first-party item page, physical impression date, facsimile glyph, or numeric table cell.

    ## 4. Historical consequence

    Batch 12CN no longer proves a pre-1578 Datong-line day/night-ke table-class witness. The valid residue is narrower: a Sejong-era Datong/Tonggui calendrical-computation record with three named solar/lunar computational tables.

    Therefore all of the following remain unresolved:

    - an explicit pre-1578 `晨昏分 / 日出入 / 晝夜刻` numerical table witness;
    - Nanjing `59/41` cell identity;
    - daily ladder and intra-term change-day identity;
    - rounding / quantization rule ancestry;
    - direct transmission into the 1578 `三命通會` display.

    ## 5. Provenance defect accounting

    ```text
    DEFECT_CLASS = PROVENANCE_METADATA_WRONG_RECORD_FIELD_AND_HOLDING_ATTRIBUTION
    DEFECT_FOUND_INCREMENT = +1
    DEFECT_REPAIRED_INCREMENT = +1
    MATRIX_ROW_COUNT_CHANGE = 0
    AUDITED_ROW_COUNT_CHANGE = 0
    RUNTIME_ALGORITHM_CHANGE = 0
    ```

    ## 6. Next gate

    1. Audit `DIC_A3_000151 / 大統曆註` separately; its generic description of `日月出入 / 晝夜長短` must not be promoted into an exact numerical-table claim without a page or explicit field.
    2. Continue pre-1578 Datong annual-almanac and related first-party table searches.
    3. Require readable page-level cells before comparing `59/41`, ladders, change days, or rounding fingerprints.

    The deterministic product remains `CLOSED`; `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT` with no runtime change.
    """).lstrip(), encoding="utf-8")


def update_current_state() -> None:
    path = "docs/PROJECT-CURRENT-STATE-R1.json"
    d = load(path)
    h = d["historical_audit"]
    h["confirmed_provenance_metadata_defect_count"] = int(h.get("confirmed_provenance_metadata_defect_count", 0)) + 1
    h["repaired_provenance_metadata_defect_count"] = int(h.get("repaired_provenance_metadata_defect_count", 0)) + 1
    if REPAIR_BATCH not in h["completed_batches"]:
        h["completed_batches"].append(REPAIR_BATCH)
    h["latest_batch_doc"] = REPAIR_DOC
    focus = []
    for item in h.get("current_focus", []):
        if item.startswith("Batch 12CN "):
            continue
        if item.startswith("The Sanming ancestry gate is now numeric/stemmatic"):
            continue
        focus.append(item)
    focus.extend([
        f"Batch 12CO exact-record audit corrects Batch 12CN: KOSTMA {DIC_ID} lists {', '.join(EXACT_TABLES)}, not 日出入晨刻表 / 晝夜刻分表 / 四方每時初昏去中星度數表.",
        f"Batch 12CO corrects the source-emitted Kyujanggak identifier for {DIC_ID} to {CORRECT_HOLDING}; the prior {WITHDRAWN_HOLDING} attribution is withdrawn and retained only as an audit trace.",
        "The pre-1578 Datong-line day/night-table bridge is therefore reopened at the evidence level only: explicit numerical day/night cells, Nanjing 59/41 identity, ladder/change-day identity, rounding, and direct Sanming parentage all remain unresolved. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; runtime remains unchanged."
    ])
    h["current_focus"] = focus
    # Preserve semantic version shape while marking a new continuity state revision.
    ver = str(d.get("schema_version", "1.0.0"))
    parts = ver.split(".")
    if len(parts) == 3 and all(x.isdigit() for x in parts):
        d["schema_version"] = f"{parts[0]}.{int(parts[1]) + 1}.0"
    dump(path, d)


def update_continuity_verifier() -> None:
    path = Path("scripts/verify-project-continuity-state-r1.py")
    s = path.read_text(encoding="utf-8")
    if REPAIR_BATCH not in s:
        needle = f'    "{OLD_BATCH}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate Batch 12CN tail in continuity verifier")
        s = s.replace(needle, f'    "{OLD_BATCH}",\n    "{REPAIR_BATCH}",\n]', 1)
    new_latest = f'LATEST_BATCH_DOC = "{REPAIR_DOC}"'
    s, n = re.subn(r'^LATEST_BATCH_DOC = ".*"$', new_latest, s, count=1, flags=re.MULTILINE)
    if n != 1:
        raise SystemExit("cannot update continuity latest batch doc")
    path.write_text(s, encoding="utf-8")


def retire_old_formalizer() -> None:
    path = Path("scripts/formalize-batch-12cn-datong-ritonggui-kyujanggak-daynight-bridge.py")
    path.write_text(dedent(f'''\
    """Retired Batch 12CN formalizer.

    Batch 12CO ({REPAIR_BATCH}) proved that the original Batch 12CN generator
    mixed record-field and holding-identifier provenance. Re-running the old generator
    would reintroduce withdrawn claims, so it is intentionally disabled.
    """

    REPAIR_BATCH = "{REPAIR_BATCH}"
    REPAIR_DOC = "{REPAIR_DOC}"


    def main() -> None:
        raise SystemExit(
            "Batch 12CN formalizer is retired after Batch 12CO provenance repair; "
            f"see {{REPAIR_DOC}}"
        )


    if __name__ == "__main__":
        main()
    '''), encoding="utf-8")


def validate_no_live_false_claims() -> None:
    reg = load("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
    k = next(x for x in reg["sources"] if x.get("source_id") == KOSTMA_SOURCE_ID)
    assert "日出入晨刻表" in k["quality_notes"] and "withdrawn" in k["quality_notes"].lower()
    assert CORRECT_HOLDING in next(x for x in reg["sources"] if x.get("source_id") == CORRECT_HOLDING_SOURCE_ID)["title"]

    research = load(OLD_RESEARCH)
    assert research["historical_adjudication"]["pre_1578_daynight_table_family_witness_recorded"] is False
    assert research["holding_binding"]["correct_source_emitted_identifier"] == CORRECT_HOLDING

    graph = load("docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json")
    node_ids = {x.get("node_id") for x in graph["nodes"]}
    assert "HOLDING-KYUJANGGAK-GR35954_00-DATONGLI-RITONGGUI" not in node_ids
    assert "TABLE-FAMILY-JOSEON-DATONGLI-RITONGGUI-DAYNIGHT" not in node_ids
    assert "HOLDING-KYUJANGGAK-GK12437_00-DATONGLI-RITONGGUI" in node_ids

    state = load("docs/PROJECT-CURRENT-STATE-R1.json")
    h = state["historical_audit"]
    assert h["confirmed_provenance_metadata_defect_count"] == h["repaired_provenance_metadata_defect_count"]
    assert h["latest_batch_doc"] == REPAIR_DOC
    assert REPAIR_BATCH in h["completed_batches"]


def main() -> None:
    update_external_registry()
    rewrite_research()
    update_matrix()
    update_graph()
    rewrite_batch_docs()
    update_current_state()
    update_continuity_verifier()
    retire_old_formalizer()
    validate_no_live_false_claims()
    print("BATCH_12CO_KOSTMA_ATTRIBUTION_REPAIR=PASS")


if __name__ == "__main__":
    main()
