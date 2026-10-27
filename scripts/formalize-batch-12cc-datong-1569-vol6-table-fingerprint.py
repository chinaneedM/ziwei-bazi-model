from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-DATONG-1569-VOL6-DIRECT-SCOPE-AND-TABLE-FINGERPRINT-CC"
PREV_ID = "BATCH-12-ZIWEI-YUNQI-YILAN-1533-SEASONAL-EXTREMA-CB"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-DATONG-1569-VOL6-DIRECT-SCOPE-AND-TABLE-FINGERPRINT-CC.md"
RESEARCH = "docs/research/ZIWEI-DATONG-1569-VOL6-TABLE-FINGERPRINT-R1.json"
SRC = "EXT-KOTENMON-DAMING-DATONG-1569"

WORKFLOW_RUN = 34860488890
ARTIFACT_ID = 10354907760
ARTIFACT_DIGEST = "sha256:55dce049de5bf8ede84b0f2bae89dc4733617136033e6f6f8700964b7c8e981b"
SOURCE_PDF_SHA256 = "4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c"
PAGE_COUNT = 45
EXACT_HEAD_CI_RUN = 34860488925
RENDER_TRIGGER_COMMIT = "35f401a92e0d23f1292301b9372fea6546eab71b"
CONTACT_SHA256 = {
    "all": "46c6087fc3a6ec781e552c18730fd50a3abe3f44aa1c7dfc7bb88d4b67ff3317",
    "1_9": "d3041585b634f4dfecf48ba698b3ecc10fd26857de597bda54eb7b0b746c03ce",
    "10_18": "7d6e15ef5b07e1e615d7eacb54e1e551ff4ab8ba478ce2484422ffc188c60ab9",
    "19_27": "2b86d22b1a805a6e4b0a697fb0e56d098f662e263e3ffbca34b4a883f0f9d21f",
    "28_36": "817bdf4a24d7e2bd3aaf1f31216afe452713438cdb8cd4fef48adecf155edc60",
    "37_45": "ca8770343852bd6f3aecb1efbde0cab9db5397e24ecd23ecc801c91572ab55cb",
}
PAGE_SHA256 = {
    "1": "85dbb5145bd060c5daa1fb11bcc1bec153ae437848dcaf3424aa206b3c84f5f7",
    "2": "bf5454c7eb3841ac83f78af2febb40673269d32f5782964c419b043d9ed0c66e",
    "3": "25fad617d57211f5475dc675a4b97cc92af9badcf5674027135b843820fc9388",
    "14": "cc76b8ef313fab42205ba027959244bb2cf94caa04cb20056ef8f5291f9f8be7",
    "42": "449503670d4b2a9bb60c435c527b1f2ac9403b7156db11857859fcd84f9652f4",
}


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate 12CB tail in continuity verifier")
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
    source = next((x for x in d["sources"] if x.get("source_id") == SRC), None)
    if source is None:
        raise SystemExit(f"missing existing source registry entry: {SRC}")
    source["batch_12cc_direct_volume_review"] = {
        "workflow_run_id": WORKFLOW_RUN,
        "artifact_id": ARTIFACT_ID,
        "artifact_digest": ARTIFACT_DIGEST,
        "source_pdf_sha256": SOURCE_PDF_SHA256,
        "page_count": PAGE_COUNT,
        "ocr_used_for_glyph_claims": False,
        "exact_head_ci_run": EXACT_HEAD_CI_RUN,
        "review_scope": "ALL_45_RENDERED_PAGES_OF_THIS_PUBLIC_VOL6_OBJECT_VIA_CONTACT_SHEETS_PLUS_TARGETED_FULL_PAGE_REVIEW",
        "observed_content_scope": "MING_DATONG_CALENDAR_METHODS_AND_TABLES_INCLUDING_YING_SUO_SOLAR_ANOMALY_LUNAR_MOTION_AND_RELATED_CALCULATION_MATERIAL",
        "sanming_exact_multipoint_day_night_table_observed": False,
        "global_datong_absence_authorized": False,
        "quality_note": "The reviewed 1569 physical volume is a strong primary Ming Datong method witness, but this exact 45-page object does not directly expose Sanming Tonghui's distinctive seasonal day/night-ke fingerprint. This is a volume-scoped nonattestation, not a claim that no Datong recension, almanac, attached table, or other fascicle ever carried such data."
    }
    d["access_date"] = "2026-09-14"
    dump(p, d)


def write_research() -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-DATONG-1569-VOL6-TABLE-FINGERPRINT-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Does the directly reviewed 1569 Zhou Xiang Da Ming Datong Lifa volume physically print the exact seasonal day/night-ke multi-point table used by the 1578 Sanming Tonghui witness?",
        "physical_witness": {
            "source_id": SRC,
            "work": "大明大統曆法",
            "author": "周相",
            "edition": "明隆慶三年（1569）刊本公開影像；日本國立公文書館內閣文庫藏本路線",
            "workflow_run_id": WORKFLOW_RUN,
            "artifact_id": ARTIFACT_ID,
            "artifact_digest": ARTIFACT_DIGEST,
            "source_pdf_sha256": SOURCE_PDF_SHA256,
            "page_count": PAGE_COUNT,
            "ocr_used_for_glyph_claims": False,
            "render_trigger_commit": RENDER_TRIGGER_COMMIT,
            "exact_head_ci_run": EXACT_HEAD_CI_RUN,
            "contact_sheet_sha256": CONTACT_SHA256,
            "selected_page_sha256": PAGE_SHA256
        },
        "direct_physical_review": {
            "all_rendered_pages_reviewed": True,
            "page_1": "title/cover identifies 大明大統曆法",
            "page_2": "曆原 and historical/calendrical exposition",
            "page_14": "推盈縮曆初末限分法; adjacent heading 太陽冬至前後立成卷第二; table is solar-anomaly/calculation material, not a seasonal day/night-ke table",
            "page_42": "later calculation/date-grid material associated with calendrical time calculation, not the Sanming seasonal multi-point day/night-ke table",
            "overall_visible_scope": [
                "calendar computational methods",
                "solar anomaly / 盈縮 material",
                "lunar motion / 遲疾 material",
                "eclipse and related calculation tables"
            ],
            "sanming_exact_table_fingerprint_observed": False,
            "target_fingerprint": [
                "小寒 42/58",
                "立春 45/55",
                "雨水 47/53 then 48/52",
                "春秋分 near/equal 50/50",
                "夏至 59/41"
            ]
        },
        "scope_firewall": {
            "reviewed_object_nonattestation": True,
            "all_datong_texts_absence_claim_authorized": False,
            "all_1569_related_fascicles_absence_claim_authorized": False,
            "all_ming_almanacs_absence_claim_authorized": False,
            "reason": "The physical review closes only this 45-page public volume object's visible scope. A missing table in this object cannot be generalized to every Datong recension, separately transmitted table, official almanac, or companion fascicle."
        },
        "relationship_to_batch_12cb": {
            "yunqi_yilan_1533_closes_broad_50_50_60_40_tradition": True,
            "datong_1569_volume_is_primary_ming_method_witness": True,
            "datong_1569_volume_directly_closes_sanming_exact_table_genealogy": False,
            "exact_sanming_table_provenance_closed": False
        },
        "historical_hypothesis_status": {
            "later_ming_datong_59_41_nanjing_explanatory_tradition_is_research_lead": True,
            "promoted_to_pre1578_direct_table_proof": False,
            "possible_composite_transmission_model": "older hundred-ke/midnight prose + older seasonal leak-arrow traditions + Ming locality/calendar adaptation",
            "composite_model_proved": False
        },
        "adjudication": {
            "direct_1569_datong_method_witness_strengthened": True,
            "reviewed_1569_object_exact_sanming_table_match": False,
            "exact_sanming_table_provenance_closed": False,
            "new_runtime_candidate_created": False,
            "runtime_winner_selected": False,
            "upper_zi_to_hai_mechanical_vote_increment": 0,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False,
            "most_conservative_reading": "The 1569 Zhou Xiang object is a direct pre-1578 Ming Datong method witness, but the reviewed 45-page volume does not itself print the Sanming 42/58...59/41 seasonal table. It therefore cannot be used as direct proof of that table's ancestry."
        },
        "impact_on_hpa_zdate_006": {
            "status_before": "MISSING_FROM_PRODUCT",
            "status_after": "MISSING_FROM_PRODUCT",
            "new_runtime_candidate_created": False,
            "runtime_winner_selected": False,
            "upper_zi_to_hai_mechanical_vote_increment": 0,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False,
            "remaining_blockers": [
                "find a pre-1578 source that directly prints the distinctive Sanming seasonal multi-point numeric fingerprint or a demonstrably generative parent table",
                "separate locality-specific Ming Datong/Nanjing 59/41 evidence from generic 40/60 traditions and from later retrospective explanations",
                "independently close the Fullbook upper-five-ke -> previous-night Hai branch mechanism"
            ]
        },
        "next_gate": [
            "audit pre-Ming/Song-Yuan leak-arrow lineages for structural ancestry rather than endpoint coincidence",
            "collate Zhao Youqin Gexiang Xinshu hundred-ke prose against Sanming wording and preserve the 40/60 versus Yandu 62/38 geographic distinction",
            "collate Huqianjing and Leibian Lifa Tongshu seasonal arrow/table sequences against the Sanming fingerprint",
            "continue search for a pre-1578 Ming Datong/Nanjing table witness carrying the 59/41 layer"
        ]
    })


def write_doc() -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit R1 — Batch 12CC

    ## 1569周相《大明大統曆法》实体卷范围与《三命通會》节气刻数指纹核验

    Status: **1569 ZHOU-XIANG DATONG PHYSICAL METHOD WITNESS DIRECTLY REVIEWED / ALL 45 RENDERED PAGES OF THE PUBLIC VOL6 OBJECT VISUALLY COLLATED WITHOUT OCR / REVIEWED OBJECT DOES NOT DIRECTLY EXPOSE SANMING 42/58...59/41 SEASONAL DAY-NIGHT TABLE / VOLUME-SCOPED NONATTESTATION ONLY / GLOBAL DATONG ABSENCE FORBIDDEN / EXACT SANMING TABLE PROVENANCE STILL OPEN / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO HAI VOTE / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

    ## 1. Why this batch follows 12CB

    Batch 12CB physically established that the 1533 Chengqiao-print 《運氣易覽》 carries an earlier 50/50 and 60/40 seasonal-extrema tradition, but not the exact multi-point sequence displayed by the 1578 《三命通會》 witness.

    A natural next candidate is Zhou Xiang's 1569 《大明大統曆法》: it is pre-1578, belongs to the Ming Datong calendrical horizon, and therefore must be checked directly rather than inferred from later descriptions of Ming day/night standards.

    ## 2. Physical witness and machine evidence

    A dedicated workflow downloaded and rendered the entire public volume without OCR.

    ```text
    WORKFLOW_RUN={WORKFLOW_RUN}
    ARTIFACT={ARTIFACT_ID}
    ARTIFACT_DIGEST={ARTIFACT_DIGEST}
    SOURCE_PDF_SHA256={SOURCE_PDF_SHA256}
    PAGE_COUNT={PAGE_COUNT}
    OCR_USED_FOR_GLYPH_CLAIMS=false
    RENDER_TRIGGER_COMMIT={RENDER_TRIGGER_COMMIT}
    EXACT_HEAD_CI_RUN={EXACT_HEAD_CI_RUN}
    ```

    The render workflow and the normal CI both passed on the same triggering HEAD. This provides a reproducible evidence object and closes the acquisition layer for this particular public volume.

    ## 3. Direct physical scope review

    The full 45-page object was reviewed through full-volume contact sheets and targeted full-page renders.

    Key controls include:

    - PDF p1: title/cover `大明大統曆法`;
    - PDF p2: `曆原` and calendrical exposition;
    - PDF p14: `推盈縮曆初末限分法`, with adjacent `太陽冬至前後立成卷第二`; its table is solar-anomaly/calculation material rather than a day/night-ke table;
    - later pages continue calendar arithmetic, lunar-motion/遲疾, eclipse and related computational tables;
    - PDF p42 is likewise calculation/date-grid material, not the target seasonal day/night table.

    Across the reviewed object, the distinctive Sanming fingerprint was not directly observed:

    ```text
    小寒 42/58
    立春 45/55
    雨水 47/53 -> 48/52
    春秋分 near/equal 50/50
    夏至 59/41
    ```

    ## 4. The negative is strictly volume scoped

    This batch does **not** authorize:

    ```text
    reviewed 45-page object lacks the target table
      -> no Ming Datong text ever contained such a table
    ```

    That inference is invalid. The Datong tradition includes multiple books, recensions, official almanacs, separately transmitted calculation tables and locality-sensitive material. This batch only establishes:

    ```text
    THIS_PUBLIC_1569_VOL6_OBJECT -> exact Sanming multipoint table NOT OBSERVED
    ```

    Therefore the 1569 object remains a strong primary Ming Datong **method witness**, but it is not yet a direct table-genealogy witness for the Sanming sequence.

    ## 5. Consequence for the 59/41 hypothesis

    Later Ming/received explanatory material makes the Datong 59/41 and Nanjing-locality layer an important research lead. However, chronology and source scope matter:

    - later explanation cannot be promoted into pre-1578 direct proof;
    - the reviewed 1569 object does not itself close that table;
    - a genuine ancestor claim still requires a pre-1578 direct table witness, a demonstrably generative calculation, or an edition-scoped textual bridge.

    A composite transmission remains plausible but unproved:

    ```text
    older hundred-ke / midnight prose
      + older seasonal leak-arrow tables
      + Ming locality/calendar adaptation
      -> Sanming displayed table
    ```

    Plausibility is not genealogy.

    ## 6. Product adjudication

    For `HPA-ZDATE-006`:

    - 1569 Zhou-Xiang Datong primary method witness: **directly reviewed**;
    - exact Sanming multi-point table in this reviewed object: **not observed**;
    - global Datong absence: **not authorized**;
    - exact Sanming table ancestry/locality: **open**;
    - upper-Zi -> Hai mechanical vote: **0**;
    - new runtime candidate: **none**;
    - runtime winner: **none**;
    - candidate collapse: **none**;
    - algorithm reopen: **no**;
    - `HPA-ZDATE-006`: remains `MISSING_FROM_PRODUCT`.

    ## 7. Next gate

    The search now moves one layer deeper: reconstruct the **pre-Ming/Song-Yuan seasonal leak-clock lineages** and compare their whole sequence against Sanming, not just 40/60 endpoints. Priority controls are Zhao Youqin's 《革象新書》 hundred-ke/midnight prose, the Song-work 《虎鈐經·傳箭》 stepwise arrow sequence, and the Yuan/Song-Luzhen 《類編曆法通書大全》 24-qi day/night table. In parallel, continue looking for a pre-1578 Ming Datong/Nanjing witness that directly carries the 59/41 layer.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def matrix() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next(x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12cc_datong_1569_vol6_direct_scope_and_table_fingerprint"] = {
        "source_ids": [SRC, "EXT-SANMING-NCL-1578-MAIN"],
        "direct_1569_datong_method_witness_reviewed": True,
        "reviewed_public_object_page_count": PAGE_COUNT,
        "reviewed_object_exact_sanming_multipoint_table_observed": False,
        "global_datong_absence_authorized": False,
        "exact_sanming_table_provenance_closed": False,
        "later_datong_59_41_nanjing_layer_status": "RESEARCH_LEAD_NOT_PRE1578_DIRECT_PROOF_IN_THIS_BATCH",
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
    if "## Progress through Batch 12CC" not in md:
        md += dedent('''

        ## Progress through Batch 12CC

        - The complete 45-page public 1569 Zhou-Xiang 《大明大統曆法》 volume was rendered and visually reviewed without OCR. It directly strengthens the pre-1578 Ming Datong method-source stack.
        - The reviewed physical object does not directly expose the distinctive Sanming seasonal 42/58...59/41 table. This is strictly a volume-scoped nonattestation; it does not authorize a claim that the wider Datong tradition, other fascicles, official almanacs or separately transmitted tables lack such material.
        - Exact Sanming table provenance/locality therefore remains open. `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`; no Hai-branch vote, runtime candidate, winner, collapse or algorithm reopen is introduced.
        ''')
    mdp.write_text(md, encoding="utf-8")


def state() -> None:
    p = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    d["schema_version"] = "1.88.0"
    a = d["historical_audit"]
    if BATCH_ID not in a["completed_batches"]:
        a["completed_batches"].append(BATCH_ID)
    a["latest_batch_doc"] = BATCH_DOC
    notes = [
        "Batch 12CC directly reviews all 45 rendered pages of the public 1569 Zhou-Xiang Datong volume; the object is a strong pre-1578 Ming calendar-method witness but does not directly expose the Sanming 42/58...59/41 seasonal table.",
        "The 12CC negative is strictly volume scoped: no global absence claim is authorized for other Datong recensions, official almanacs, companion fascicles or separately transmitted tables.",
        "Next gate: compare pre-Ming/Song-Yuan leak-clock lineages (Gexiang Xinshu, Huqianjing, Leibian Lifa Tongshu) against the whole Sanming numeric fingerprint while continuing the search for a pre-1578 Ming Datong/Nanjing 59/41 witness."
    ]
    for n in notes:
        if n not in a["current_focus"]:
            a["current_focus"].append(n)
    d["updated_at"] = "2026-09-14"
    dump(p, d)


def main() -> None:
    continuity()
    registry()
    write_research()
    write_doc()
    matrix()
    state()


if __name__ == "__main__":
    main()
