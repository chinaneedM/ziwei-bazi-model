from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-SANMING-SHOUSHI-BIRTH-TIME-BRIDGE-BZ"
PREV_ID = "BATCH-12-ZIWEI-SIZIJING-SEASONAL-TIMEKEEPING-GEOGRAPHIC-CALIBRATION-BY"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SANMING-SHOUSHI-BIRTH-TIME-BRIDGE-BZ.md"
RESEARCH = "docs/research/ZIWEI-SANMING-SHOUSHI-BIRTH-TIME-BRIDGE-R1.json"
AT_RESEARCH = "docs/research/ZIWEI-SANMING-TONGHUI-1578-TIMEKEEPING-PHYSICAL-COLLATION-R1.json"
SRC_NLC_CHINA = "EXT-NLC-CHINA-SANMING-TONGHUI-WANLI-JUAN2-BIRTH-TIME-BRIDGE"
URL_V3 = "https://commons.wikimedia.org/wiki/File:NLC892-411999029701-67186_%E4%B8%89%E5%91%BD%E9%80%9A%E6%9C%83_%E7%AC%AC3%E5%86%8A.pdf"
URL_V4 = "https://commons.wikimedia.org/wiki/File:NLC892-411999029701-67187_%E4%B8%89%E5%91%BD%E9%80%9A%E6%9C%83_%E7%AC%AC4%E5%86%8A.pdf"

V3_RUN = 34830209613
V3_ARTIFACT = 10341698973
V3_DIGEST = "sha256:cd7da63c991023c32ef6e730bb023bad74d43c78e3a16047ab59c86c918992f7"
V3_PDF_SHA256 = "112084f6f463038285d87c477a6f80527d44a3e3d4d16a5e0ecfb24159f320d2"
V3_PAGE34_SHA256 = "e101938a24c86ec8baa756b3983360e24e82afb20cec48a450c7d5f242393d4b"
V4_RUN = 34830529198
V4_ARTIFACT = 10341699530
V4_DIGEST = "sha256:849473a7e9006c79ad9070c5cd8778ef641e73adeee0b8a1add04e3037ccbd7c"
V4_PDF_SHA256 = "3e2e924984f51628207bfec441729b1b616e4f051cfa3ea6661262888bba1f18"
V4_PAGE02_SHA256 = "f508e224012c4694a81d2a985bd1fb1911e9134afd2d77fc07cfb5b7c6aa4d14"


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def locate_at_source_id(registry: dict) -> str:
    for src in registry["sources"]:
        if src.get("research_artifact") == AT_RESEARCH:
            return src["source_id"]
        if "三命通會》萬曆六年（1578）刻本" in src.get("title", ""):
            return src["source_id"]
    raise SystemExit("cannot locate Batch 12AT Sanming source in registry")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate 12BY tail in continuity verifier")
        s = s.replace(needle, f'    "{PREV_ID}",\n    "{BATCH_ID}",\n]', 1)
    latest = f'LATEST_BATCH_DOC = "{BATCH_DOC}"'
    if latest not in s:
        s, n = re.subn(r'^LATEST_BATCH_DOC = ".*"$', latest, s, count=1, flags=re.MULTILINE)
        if n != 1:
            raise SystemExit("cannot update latest batch doc")
    p.write_text(s, encoding="utf-8")


def registry() -> str:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    at_id = locate_at_source_id(d)
    ids = {x.get("source_id") for x in d["sources"]}
    if SRC_NLC_CHINA not in ids:
        d["sources"].append({
            "source_id": SRC_NLC_CHINA,
            "title": "中國國家圖書館藏《三命通會》明萬曆刻本卷二上/下（第3、4冊）",
            "author": "萬民英",
            "historical_period": "MING_WANLI_1573_1620",
            "edition": "刻本；10行22字，白口，四周雙邊；Commons/NLC metadata dates the object only to 明萬曆[1573-1620]",
            "provider": "National Library of China scan via Wikimedia Commons",
            "url": URL_V3,
            "related_urls": [URL_V4],
            "source_role": "DIRECT_PHYSICAL_CROSS_HOLDING_CONTROL_FOR_SANMING_JUAN2_MANTIC_BIRTH_TIME_TO_SHOUSHI_CALENDAR_BRIDGE",
            "quality_notes": "No-OCR review. Volume 3 is 卷之二上 and volume 4 is 卷之二下. The reviewed public metadata does not prove this NLC copy is the same 1578 impression as the Taiwan NCL witness; treat it as a separate Wanli physical holding/control, not an independent textual vote."
        })
    d["access_date"] = "2026-09-14"
    dump(p, d)
    return at_id


def write_research(at_id: str) -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-SANMING-SHOUSHI-BIRTH-TIME-BRIDGE-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Does a primary Ming mantic source directly bridge uncertain natal birth-time adjudication to a historical calendrical/timekeeping framework strongly enough to narrow HPA-ZDATE-006 runtime time-standard provenance?",
        "existing_primary_witness": {
            "source_id": at_id,
            "research_artifact": AT_RESEARCH,
            "edition": "萬曆六年（1578）刻本 / Taiwan National Central Library physical scan",
            "direct_no_ocr_sequence": [
                "論日刻: 銅壺貯水漏下壺箭 / 一日百刻",
                "論時刻: 子時上半在夜半前為昨日、下半在夜半後屬今日",
                "論曰: 看命之法以時為低昂 / 子亥中間厥時難定",
                "論曰: 陰晴倏忽寒煖迥別",
                "論曰: 余姑就授時曆分之 / 要在智者密察而詳問之"
            ]
        },
        "new_cross_holding_physical_control": {
            "source_id": SRC_NLC_CHINA,
            "bibliographic_scope": "National Library of China Ming Wanli [1573-1620] 刻本; exact 1578 impression identity not established",
            "volume3": {
                "role": "卷之二上",
                "url": URL_V3,
                "workflow_run_id": V3_RUN,
                "artifact_id": V3_ARTIFACT,
                "artifact_digest": V3_DIGEST,
                "pdf_sha256": V3_PDF_SHA256,
                "decisive_render_page_34_sha256": V3_PAGE34_SHA256,
                "direct_no_ocr_findings": [
                    "page 33 begins 論日刻",
                    "page 34 begins 論時刻",
                    "論時刻 directly states 大晝夜十二時均分百刻 and the upper/lower Zi midnight split",
                    "the section then proceeds into seasonal solar-term sunrise/sunset and day/night-ke data and continues across the fascicle boundary"
                ]
            },
            "volume4": {
                "role": "卷之二下",
                "url": URL_V4,
                "workflow_run_id": V4_RUN,
                "artifact_id": V4_ARTIFACT,
                "artifact_digest": V4_DIGEST,
                "pdf_sha256": V4_PDF_SHA256,
                "decisive_render_page_02_sha256": V4_PAGE02_SHA256,
                "direct_no_ocr_findings": [
                    "opening continues the late-year seasonal table through 立冬、小雪、大雪",
                    "the same physical page continues into 論曰看命之法以時為低昂時有八刻初正之氣不同",
                    "the continuation includes 子亥中間厥時難定 and the final appeal to 授時曆分之、密察而詳問"
                ]
            },
            "independent_physical_holding_increment": 1,
            "independent_textual_vote_increment": 0,
            "same_impression_identity_proved": False,
            "ocr_used_for_glyph_claims": False
        },
        "philological_and_operational_adjudication": {
            "mantic_birth_time_to_shoushi_calendar_bridge": "DIRECT_PRIMARY_MING_PHYSICAL_ATTESTATION_CROSS_HOLDING_STABLE",
            "bridge_scope": "The mantic text itself places uncertain natal birth-time adjudication beside sub-hour ke, seasonal solar-term sunrise/sunset/day-night data, and explicitly says to divide/adjudicate by the Shoushi calendar.",
            "historical_time_standard_narrowing": "SIGNIFICANT: runtime provenance is no longer limited to an unspecified generic traditional clock; the source horizon explicitly invokes Shoushi-calendar time division and seasonal calendrical tables.",
            "automatic_inverse_birth_time_formula_recovered": False,
            "reason_formula_not_closed": "The passage does not supply a deterministic mapping from biographical/narrative birth evidence to an exact clock instant; it explicitly retains 密察而詳問 as part of adjudication.",
            "location_binding_closed": False,
            "modern_local_apparent_solar_time_equivalence_proved": False,
            "upper_half_zi_reclassified_to_hai_branch": False,
            "fullbook_luojing_sentence_explained": False,
            "direct_textual_dependency_between_sizijing_and_sanming": False,
            "functional_semantic_bridge_sizijing_to_sanming": "PLAUSIBLE_AND_NOW_PRIMARY-CONTROLLED: both concern difficult birth-time determination and seasonal/timekeeping context, but wording/formula identity is not proved."
        },
        "impact_on_hpa_zdate_006": {
            "status_before": "MISSING_FROM_PRODUCT",
            "status_after": "MISSING_FROM_PRODUCT",
            "runtime_time_standard_binding": "PARTIALLY_NARROWED_TO_SHOUSHI_CALENDAR / SEASONAL KE FRAMEWORK, NOT CLOSED TO A MODERN INSTANT",
            "new_runtime_candidate_created": False,
            "runtime_winner_selected": False,
            "hai_branch_mechanical_vote_increment": 0,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False,
            "remaining_blockers": [
                "source-close the Fullbook-specific upper-five-ke -> previous-night Hai branch reassignment as a mechanical rule across sufficient direct witnesses",
                "resolve how the source-scoped Shoushi/seasonal framework maps to birthplace/locality and a reproducible modern instant or preserve it as a non-runtime historical practice",
                "recover an explicit operational input rule if automated uncertain-birth-time reconstruction is ever proposed; do not infer one from 密察而詳問"
            ]
        },
        "accounting": {
            "matrix_rows": 198,
            "audited_rows": 166,
            "current_missing_from_product_rows": 10,
            "identified_missing_candidate_families": 14,
            "confirmed_provenance_metadata_defect_count": 11,
            "repaired_provenance_metadata_defect_count": 11,
            "confirmed_chart_algorithm_defect_count": 0,
            "algorithm_reopen_count": 0,
            "candidate_collapse_count": 0
        }
    })


def write_doc(at_id: str) -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit R1 — Batch 12BZ

    ## 《三命通會》命理生時 → 《授時曆》操作桥：跨馆藏实体复核与 runtime 边界

    Status: **PRIMARY MING MANTIC SOURCE DIRECTLY BRIDGES UNCERTAIN NATAL BIRTH-TIME ADJUDICATION TO SHOUSHI-CALENDAR TIME DIVISION / 1578 TAIWAN NCL PHYSICAL WITNESS ALREADY DIRECTLY COLLATES THE BRIDGE / CHINA NLC SEPARATE WANLI PHYSICAL HOLDING RECONFIRMS THE JUAN-2 SEQUENCE ACROSS VOLUMES 3–4 / HISTORICAL TIME-STANDARD PROVENANCE SIGNIFICANTLY NARROWED / AUTOMATIC INVERSE BIRTH-TIME FORMULA NOT RECOVERED / NLC CHINA COPY NOT ASSUMED TO BE SAME 1578 IMPRESSION / NO UPPER-ZI-TO-HAI MECHANICAL VOTE / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

    ## 1. Why this is a new step after 12BY

    Batch 12BY showed that seasonal day/night timekeeping was technically location-calibrated and therefore a universal month-only correction table would be historically under-specified. Its next gate asked for a fate-calculation text that explicitly applies a calendrical/timekeeping framework to uncertain **birth time**.

    That bridge already existed in the repository's Batch 12AT physical collation, but had not yet been integrated with the later Sizijing seasonal-timekeeping findings.

    ## 2. Existing decisive primary witness: 1578 physical 《三命通會》

    Batch 12AT's Taiwan National Central Library physical witness (`{at_id}`) directly reads, without OCR, the sequence:

    - `論日刻`: copper-clepsydra / hundred-ke timekeeping;
    - `論時刻`: twelve double-hours, hundred ke, and the upper/lower Zi midnight date split;
    - seasonal solar-term sunrise/sunset and day/night-ke material;
    - `論曰`: `看命之法以時為低昂`;
    - `子亥中間厥時難定`;
    - `余姑就授時曆分之`;
    - `要在智者密察而詳問之`.

    This is direct Ming mantic evidence that difficult natal-time adjudication was consciously connected to a calendrical/timekeeping framework rather than to an unspecified modern clock convention.

    ## 3. New cross-holding physical control: China NLC Wanli print

    To avoid relying on one digitized physical object, this batch rendered and directly reviewed another National Library of China Wanli-print holding.

    ### Volume 3 / 卷之二上

    - Commons/NLC object: `{URL_V3}`
    - catalog date: `明萬曆[1573-1620]`, not narrowed to 1578 on the reviewed metadata;
    - renderer run `{V3_RUN}`, artifact `{V3_ARTIFACT}`, digest `{V3_DIGEST}`;
    - source PDF SHA-256 `{V3_PDF_SHA256}`;
    - rendered page 34 SHA-256 `{V3_PAGE34_SHA256}`.

    Direct no-OCR review shows `論日刻` immediately followed by `論時刻`; the latter directly contains the hundred-ke / Zi-midnight split and then proceeds into seasonal sunrise/sunset/day-night data.

    ### Volume 4 / 卷之二下

    - Commons/NLC object: `{URL_V4}`
    - renderer run `{V4_RUN}`, artifact `{V4_ARTIFACT}`, digest `{V4_DIGEST}`;
    - source PDF SHA-256 `{V4_PDF_SHA256}`;
    - rendered page 2 SHA-256 `{V4_PAGE02_SHA256}`.

    The opening continues the late-year seasonal table (`立冬 / 小雪 / 大雪`) and on the same physical page continues into the mantic conclusion beginning `論曰看命之法以時為低昂…`, including the Zi/Hai difficulty and the appeal to `授時曆分之` and detailed inquiry.

    This establishes **cross-holding physical stability** of the bridge. It does not prove the China NLC copy is the same 1578 impression, and therefore it is not counted as a new independent textual vote.

    ## 4. What the bridge now closes

    The historical time-standard problem is materially narrower:

    ```text
    uncertain natal birth time
      -> sub-hour ke / midnight-boundary problem
      -> seasonal solar-term sunrise/sunset/day-night framework
      -> explicit 授時曆 reference
      -> practitioner 密察而詳問
    ```

    Therefore it is no longer accurate to say that the historical mantic material supplies only a vague traditional clock. A primary Ming fate-calculation witness explicitly anchors adjudication to the Shoushi-calendar/time-division horizon.

    ## 5. What it still does NOT close

    This batch does **not** create a runtime algorithm:

    - no deterministic inverse formula maps an uncertain birth narrative to an exact instant;
    - the text itself retains `密察而詳問`, i.e. human evidentiary inquiry;
    - birthplace/locality binding of the relevant historical table is not source-closed;
    - no equivalence to modern local apparent solar time is established;
    - no clause says upper-half Zi is mechanically reassigned to the Hai branch;
    - the Fullbook `陰雨之際必須羅經以定真確時候` sentence is not thereby explained away.

    Hence `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`.

    ## 6. Relationship to 《四字經》

    The Sizijing `旦夕 / 月建(月運) / 長短` evidence and the Sanming `授時曆分之` evidence now occupy a strongly overlapping **functional semantic field**: both address hard-to-determine birth time through seasonal/timekeeping concepts. But there is still no proof of direct textual dependence, identical formula, or shared numeric table. That firewall remains mandatory.

    ## 7. Next gate

    1. Continue direct Fullbook-family work on the mechanically decisive `上五刻屬昨夜亥時` wording and its time-coordinate assumptions.
    2. Search Ming/Yuan `授時曆` derivative tables and fate-calculation manuals for an explicit birthplace/locality binding used by practitioners, without importing official formulas merely because they are mathematically compatible.
    3. Treat uncertain-birth-time reconstruction as a separately evidenced human-assisted workflow unless an explicit deterministic inverse rule is found.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def matrix(at_id: str) -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next(x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12bz_sanming_shoushi_birth_time_bridge"] = {
        "source_ids": [at_id, SRC_NLC_CHINA],
        "primary_ming_mantic_birth_time_to_shoushi_bridge": True,
        "cross_holding_physical_stability_confirmed": True,
        "china_nlc_exact_1578_impression_identity_proved": False,
        "runtime_time_standard_binding_status": "PARTIALLY_NARROWED_TO_SHOUSHI_CALENDAR_SEASONAL_KE_FRAMEWORK_NOT_CLOSED_TO_MODERN_INSTANT",
        "automatic_inverse_birth_time_formula_found": False,
        "birthplace_locality_binding_closed": False,
        "upper_zi_to_hai_mechanical_vote_increment": 0,
        "new_runtime_candidate_created": False,
        "runtime_winner_selected": False,
        "candidate_collapsed": False,
        "algorithm_reopen_authorized": False,
        "research_artifact": RESEARCH
    }
    dump(p, d)

    mdp = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md")
    md = mdp.read_text(encoding="utf-8")
    if "## Progress through Batch 12BZ" not in md:
        md += dedent('''

        ## Progress through Batch 12BZ

        - The 1578 physical Sanming Tonghui witness already directly connects natal birth-time adjudication to Shoushi-calendar division after a seasonal sunrise/sunset/day-night-ke table; Batch 12BZ integrates that primary bridge with the later Sizijing seasonal-timekeeping research.
        - A separate China National Library Ming-Wanli physical holding (juan 2 upper/lower across volumes 3–4) was rendered without OCR and reconfirms the same structural/textual sequence. Its exact identity with the 1578 impression is not assumed and it adds no independent textual vote.
        - HPA-ZDATE-006 historical time-standard provenance is therefore significantly narrowed to a Shoushi-calendar/seasonal-ke horizon, but no deterministic inverse birth-time formula, locality binding, modern-instant mapping, or upper-Zi-to-Hai reassignment is closed.
        - Result: HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; no runtime candidate, winner, collapse, or algorithm reopen.
        ''')
    mdp.write_text(md, encoding="utf-8")


def state() -> None:
    p = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    d["schema_version"] = "1.85.0"
    a = d["historical_audit"]
    if BATCH_ID not in a["completed_batches"]:
        a["completed_batches"].append(BATCH_ID)
    a["latest_batch_doc"] = BATCH_DOC
    notes = [
        "Batch 12BZ integrates the 1578 Sanming Tonghui physical evidence with the Sizijing seasonal-timekeeping line: uncertain natal birth-time adjudication is directly anchored to a Shoushi-calendar / seasonal-ke framework in a primary Ming mantic source.",
        "A separate China NLC Ming-Wanli physical holding reconfirms the juan-2 sequence across volumes 3-4; exact same-impression identity with the 1578 Taiwan witness is not assumed and no independent textual vote is added.",
        "HPA-ZDATE-006 runtime time-standard provenance is materially narrowed but still not source-closed to a modern instant; no inverse birth-time algorithm or upper-Zi-to-Hai mechanical vote is created."
    ]
    for n in notes:
        if n not in a["current_focus"]:
            a["current_focus"].append(n)
    d["updated_at"] = "2026-09-14"
    dump(p, d)


def main() -> None:
    continuity()
    at_id = registry()
    write_research(at_id)
    write_doc(at_id)
    matrix(at_id)
    state()


if __name__ == "__main__":
    main()
