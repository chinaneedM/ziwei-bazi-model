from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-GEXIANG-HUQIAN-COMPOSITE-TIMEKEEPING-ANCESTRY-CD"
PREV_ID = "BATCH-12-ZIWEI-DATONG-1569-VOL6-DIRECT-SCOPE-AND-TABLE-FINGERPRINT-CC"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-GEXIANG-HUQIAN-COMPOSITE-TIMEKEEPING-ANCESTRY-CD.md"
RESEARCH = "docs/research/ZIWEI-GEXIANG-HUQIAN-COMPOSITE-TIMEKEEPING-ANCESTRY-R1.json"
GEXIANG_SRC = "EXT-WIKIMEDIA-GEXIANG-XINSHU-CADAL06054852"
HUQIAN_SRC = "EXT-TIANYIGE-HUQIANJING-MING-CHUANJIAN"
SANMING_SRC = "EXT-SANMING-NCL-1578-MAIN"

GEXIANG_URL = "https://commons.wikimedia.org/wiki/Special:Redirect/file/CADAL06054852_%E9%9D%A9%E8%B1%A1%E6%96%B0%E6%9B%B8%C2%B7%E5%8D%B7%E4%B8%80~%E5%8D%B7%E4%BA%94.djvu"
GEXIANG_RUN = 34863878875
GEXIANG_ARTIFACT = 10356238369
GEXIANG_DIGEST = "sha256:1b6f1c2f665b97794022a02e75cc85eb5cfb72501dfb8063acc2fc11464a7dbe"
GEXIANG_DJVU_SHA256 = "e6199e9a7e9381adec1d9b4f418a2fd6321add6bf72f6fb28add6ab379b8dbd4"
GEXIANG_PDF_SHA256 = "9a8e15384a3d2898f2fc28747c6dd847dad587190fe67a2ac5b019edfb042bbb"
GEXIANG_PAGE_SHA256 = {
    "78": "55fa822b1b809f519d79df36701191c95d2c9873fcd52a7035d33501bdb2e1ba",
    "79": "f8baf1814afe70728f537a7bea865e5d8a5589cbd8e8ebb9992e9df6988d24ca",
    "80": "3c74fc0d59ff735ec089ccda777784f05900d3c1e19d97abc9b4f9f68904409b",
}
GEXIANG_TRIGGER = "2d3331304524bfe5b8fc2797bedb05894c1cf788"
GEXIANG_CI_RUN = 34863878945

HUQIAN_RUN = 34832306143
HUQIAN_ARTIFACT = 10342711240
HUQIAN_DIGEST = "sha256:87bd11223e5fdbfe1ec79b2bc4e2a7577fbe459559e0386287c96f3074f2f27d"
HUQIAN_PAGE_SHA256 = {
    "74": "a86cade9b99ed1b5cc943370e4b66e914d7968bc08943225bb99530fb15721ab",
    "75": "cc7546f4d93b85fb0327e30cead9c994ae017d81dc2f1dd1b86e994babb3cf83",
    "76": "2136201c372c0f8ea51dce46c1babcfc135758a98c775afa52c09c39fc8d5534",
}


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate 12CC tail in continuity verifier")
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
    if GEXIANG_SRC not in ids:
        d["sources"].append({
            "source_id": GEXIANG_SRC,
            "title": "趙友欽《革象新書》卷一至卷五 CADAL 公開影像",
            "author": "趙友欽",
            "historical_period": "YUAN_WORK_IN_LATER_RECEIVED_FACSIMILE_TRANSMISSION",
            "edition": "CADAL06054852 公開影像；卷二《時分百刻》《晝夜短長》；物理影像本身不得倒推為元刻本",
            "provider": "Wikimedia Commons / CADAL",
            "url": GEXIANG_URL,
            "source_role": "DIRECT_FACSIMILE_OF_RECEIVED_YUAN_WORK_FOR_HUNDRED_KE_AND_HALF_ZI_TEXTUAL_ANTECEDENT",
            "quality_notes": "Batch 12CD rendered the full 202-page object without OCR. Physical pp78-79 directly show 時分百刻, the hundred-ke subdivision, and 子時之上一半在夜半前屬昨日 / 下一半在夜半後屬今日; p79-80 continue into 晝夜短長. The work is Yuan, but this physical scan is a later received witness, so it is not labeled a surviving Yuan print."
        })
    h = next((x for x in d["sources"] if x.get("source_id") == HUQIAN_SRC), None)
    if h is not None:
        h["batch_12cd_sequence_comparison"] = {
            "physical_pages": [74, 75, 76],
            "shared_numeric_ladder_with_sanming": True,
            "exact_table_identity_with_sanming": False,
            "reason": "The Song-work leak-arrow sequence physically carries 40/60 through 60/40 in one-ke steps and includes many exact Sanming pairs, but term/date anchors differ and Huqianjing reaches 60/40 while Sanming displays 59/41 at summer solstice."
        }
    d["access_date"] = "2026-09-14"
    dump(p, d)


def write_research() -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-GEXIANG-HUQIAN-COMPOSITE-TIMEKEEPING-ANCESTRY-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Do the received Yuan Gexiang Xinshu prose and the Song-work Huqianjing leak-arrow sequence jointly explain the structural ancestry of Sanming Tonghui's timekeeping passage and seasonal numeric table without falsely collapsing them into one exact source?",
        "gexiang_physical_witness": {
            "source_id": GEXIANG_SRC,
            "workflow_run_id": GEXIANG_RUN,
            "artifact_id": GEXIANG_ARTIFACT,
            "artifact_digest": GEXIANG_DIGEST,
            "source_djvu_sha256": GEXIANG_DJVU_SHA256,
            "converted_pdf_sha256": GEXIANG_PDF_SHA256,
            "page_sha256": GEXIANG_PAGE_SHA256,
            "render_trigger_commit": GEXIANG_TRIGGER,
            "exact_head_ci_run": GEXIANG_CI_RUN,
            "page_count": 202,
            "ocr_used_for_glyph_claims": False,
            "edition_scope_firewall": "Yuan-authored work in a later received facsimile; not a surviving Yuan physical print."
        },
        "gexiang_direct_collation": {
            "page_78_heading": "時分百刻",
            "page_78_79_readings": [
                "晝夜十二時均分為百刻",
                "一時有八大刻二小刻",
                "子時之上一半在夜半前屬昨日",
                "下一半在夜半後屬今日"
            ],
            "page_79_continuation": "今夜以及他夜皆然；並論古曆二小刻與今曆籌策及子午卯酉九刻俗說之非",
            "page_79_80_heading": "晝夜短長",
            "page_79_80_mechanics": "春秋約六七日增減晝夜一刻；二至前後增減一刻相去二十餘日；未出/既入之昏明五刻不直接作太陽在地平線以上的晝長。"
        },
        "sanming_textual_comparison": {
            "source_id": SANMING_SRC,
            "physical_reference": "Batch 12AT, NCL 1578 PDF p133",
            "shared_structure": [
                "晝夜十二時 / 百刻",
                "每時八大刻二小刻",
                "總大刻九十六 / 小刻二十四 / 六小刻準一大刻",
                "上半時初初至初四 / 下半時正初至正四",
                "子時上半夜半前 previous-day orientation / 下半夜半後 current-day orientation",
                "古曆二小刻開頭與俗說子午卯酉九刻之辨"
            ],
            "important_recension_variant": "Gexiang received facsimile has 屬昨日; 1578 Sanming physical witness has 為昨日 while retaining 屬今日.",
            "near_verbatim_textual_antecedent_supported": True,
            "direct_copying_direction_proved": False,
            "common_earlier_source_excluded": False
        },
        "huqian_physical_sequence": {
            "source_id": HUQIAN_SRC,
            "workflow_run_id": HUQIAN_RUN,
            "artifact_id": HUQIAN_ARTIFACT,
            "artifact_digest": HUQIAN_DIGEST,
            "page_sha256": HUQIAN_PAGE_SHA256,
            "ocr_used_for_glyph_claims": False,
            "mechanical_family": "one-day hundred-ke seasonal leak-arrow ladder",
            "extrema": "winter 40/60; summer 60/40",
            "shared_pairs_with_sanming_examples": [
                "小寒 42/58",
                "立春 45/55",
                "雨水 47/53",
                "雨水後段 48/52",
                "49/51",
                "51/49",
                "53/47",
                "55/45",
                "56/44",
                "58/42",
                "59/41"
            ],
            "exact_anchor_equivalence": False,
            "summer_solstice_difference": "Huqianjing reaches 60/40 at summer-solstice arrow; Sanming displays 59/41 at 夏至.",
            "interpretation": "Sanming belongs to the same stepwise numeric family, but its solar-term/date anchoring and solstitial cap are adapted rather than copied as an exact table."
        },
        "composite_ancestry_model": {
            "prose_layer": "Gexiang-like hundred-ke / half-Zi textual lineage",
            "numeric_layer": "older leak-arrow 40<->60 one-ke-step seasonal ladder represented by Huqianjing",
            "adaptation_layer": "Ming calendrical/locality/astronomical anchoring producing Sanming's displayed term-specific values including 59/41",
            "model_status": "MATERIALLY_STRENGTHENED_NOT_STEMMATICALLY_CLOSED",
            "why_not_closed": [
                "the Gexiang physical object is a later received witness of a Yuan work, not a Yuan print",
                "Huqianjing and Sanming do not share identical change dates/term anchors",
                "the pre-1578 Ming/Nanjing direct source for the 59/41 cap is still not locked"
            ]
        },
        "adjudication": {
            "sanming_hundred_ke_prose_has_earlier_received_textual_antecedent": True,
            "sanming_numeric_table_belongs_to_older_stepwise_leak_arrow_family": True,
            "sanming_exact_table_equals_huqianjing": False,
            "direct_gexiang_to_sanming_copying_proved": False,
            "direct_huqianjing_to_sanming_copying_proved": False,
            "exact_sanming_table_provenance_closed": False,
            "new_runtime_candidate_created": False,
            "runtime_winner_selected": False,
            "upper_zi_to_hai_mechanical_vote_increment": 0,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False
        },
        "impact_on_hpa_zdate_006": {
            "status_before": "MISSING_FROM_PRODUCT",
            "status_after": "MISSING_FROM_PRODUCT",
            "reason": "This batch materially clarifies the textual and numeric ancestry of the generic hundred-ke/half-Zi framework, but still does not supply the Fullbook-specific upper-five-ke -> previous-night Hai branch reassignment.",
            "remaining_blockers": [
                "lock a pre-1578 Ming/Nanjing or equivalent direct witness for the 59/41 seasonal cap and its term anchoring",
                "determine whether Sanming's seasonal table is generated from a locality-specific official table or an adapted leak-arrow tradition",
                "independently close the Fullbook upper-five-ke -> previous-night Hai branch mechanism"
            ]
        }
    })


def write_doc() -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit R1 — Batch 12CD

    ## 《革象新書》百刻文本祖型 + 《虎鈐經》傳箭數列：1578《三命通會》時刻材料的複合傳承模型

    Status: **RECEIVED YUAN-WORK GEXIANG FACSIMILE PHYSICALLY CONFIRMS A NEAR-VERBATIM HUNDRED-KE / HALF-ZI TEXTUAL ANTECEDENT / SONG-WORK HUQIANJING MING-PRINT PHYSICALLY CONFIRMS THE OLDER 40↔60 ONE-KE STEP LADDER / SANMING SHARES BOTH STRUCTURES BUT IS NOT AN EXACT COPY OF EITHER / COMPOSITE ANCESTRY MODEL MATERIALLY STRENGTHENED / EXACT 59/41 MING TABLE PARENT STILL OPEN / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO HAI VOTE / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

    ## 1. Why this batch follows 12CC

    Batch 12CC ruled out a shortcut: the reviewed 1569 Zhou-Xiang Datong volume does not itself expose the Sanming 42/58...59/41 table. The next task is therefore structural: separate the **prose lineage** from the **numeric ladder lineage** before looking for the Ming adaptation that joined them.

    ## 2. 《革象新書》 physical collation

    A dedicated workflow rendered all 202 pages of CADAL06054852 without OCR.

    ```text
    RUN={GEXIANG_RUN}
    ARTIFACT={GEXIANG_ARTIFACT}
    DIGEST={GEXIANG_DIGEST}
    DJVU_SHA256={GEXIANG_DJVU_SHA256}
    PDF_SHA256={GEXIANG_PDF_SHA256}
    P78_SHA256={GEXIANG_PAGE_SHA256['78']}
    P79_SHA256={GEXIANG_PAGE_SHA256['79']}
    P80_SHA256={GEXIANG_PAGE_SHA256['80']}
    EXACT_HEAD_CI_RUN={GEXIANG_CI_RUN}
    OCR_USED_FOR_GLYPH_CLAIMS=false
    ```

    Scope firewall: 《革象新書》 is a Yuan work by Zhao Youqin, but this physical object is a **later received facsimile transmission**. It is not called a surviving Yuan print.

    PDF p78 directly carries `時分百刻` and reads the hundred-ke system, including:

    ```text
    晝夜十二時均分為百刻
    一時有八大刻二小刻
    ...
    子時之上一半在夜半前屬昨日
    下一半在夜半後屬今日
    ```

    p79 continues the same discussion into the old-calendar two-small-ke arrangement and rejects the popular `子午卯酉各九刻` claim, then opens `晝夜短長`. p79-80 further explains that spring/autumn day-night change is faster and solstitial change slower.

    ## 3. Near-verbatim relation to 1578《三命通會》

    Batch 12AT physically locked the 1578 NCL Sanming p133 passage. The architecture is overwhelmingly the same: twelve shi / hundred ke, eight large + two small ke, 96 large + 24 small with six small equaling one large, upper/lower half labels, midnight half-Zi date orientation, the old-calendar small-ke note, and the rejection of the `子午卯酉九刻` folk rule.

    One valuable recension difference is preserved rather than normalized:

    ```text
    received Gexiang facsimile: 屬昨日 / 屬今日
    1578 Sanming physical:      為昨日 / 屬今日
    ```

    This establishes a strong **earlier-work textual antecedent / common-text lineage** for the Sanming prose. It does not by itself prove direct copying direction or exclude an earlier common source.

    ## 4. 《虎鈐經·傳箭》 supplies the older numeric ladder family

    The Tianyige Ming-print physical witness of the Song work was already rendered without OCR in Batch 12CA. Re-reading pp74-76 as a whole sequence shows why endpoint-only comparison was insufficient.

    The table runs by one-ke steps from winter `40/60` toward summer `60/40`, and it directly contains many of the same numeric pairs later displayed by Sanming, including:

    ```text
    小寒 42/58
    立春 45/55
    雨水 47/53
    later 48/52
    ...
    55/45
    56/44
    58/42
    59/41
    ```

    The similarity is structural, not identity. Huqianjing changes arrows on its own day offsets and reaches `60/40` at the summer-solstice arrow. Sanming changes solar-term/date anchoring and displays `59/41` at 夏至.

    Therefore the correct statement is:

    ```text
    Sanming numeric table belongs to the older stepwise leak-arrow family
    != Sanming copied the Huqianjing table unchanged
    ```

    ## 5. Composite transmission model

    The evidence now supports a substantially narrower model:

    ```text
    Gexiang-like hundred-ke / half-Zi prose lineage
      + older 40↔60 seasonal leak-arrow numeric ladder
      + Ming calendrical/locality/astronomical adaptation
      -> Sanming 1578 displayed timekeeping material
    ```

    This is no longer a loose thematic analogy. Two different structural layers now have concrete antecedents. What remains open is the **Ming adaptation layer**, especially the direct pre-1578 source that turns the old solstitial 60/40 family into Sanming's displayed 59/41 cap and fixes its term/date anchors.

    ## 6. Product adjudication

    For `HPA-ZDATE-006`:

    - generic half-Zi / hundred-ke textual ancestry: **materially strengthened**;
    - older stepwise seasonal numeric family: **materially strengthened**;
    - exact Sanming = Gexiang: **no**;
    - exact Sanming = Huqianjing: **no**;
    - direct borrowing direction: **not proved**;
    - exact pre-1578 59/41 Ming parent: **open**;
    - upper-Zi -> Hai branch vote: **0**;
    - runtime candidate/winner/collapse: **none**;
    - algorithm reopen: **no**;
    - `HPA-ZDATE-006`: remains `MISSING_FROM_PRODUCT`.

    ## 7. Next gate

    Stop searching only for isolated numbers. Search for a pre-1578 Ming/Nanjing witness that combines the **same one-ke ladder** with the **59/41 solstitial cap and Sanming-like solar-term anchoring**. Priority targets are Datong almanac appendices, official leak-clock/day-night tables, local Nanjing calendrical tables, and pre-1578 tongshu/medical-yunqi compilations.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def matrix() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next(x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12cd_gexiang_huqian_composite_timekeeping_ancestry"] = {
        "source_ids": [GEXIANG_SRC, HUQIAN_SRC, SANMING_SRC],
        "gexiang_near_verbatim_hundred_ke_textual_antecedent": True,
        "huqian_stepwise_numeric_family_antecedent": True,
        "sanming_exactly_equals_gexiang": False,
        "sanming_exactly_equals_huqianjing": False,
        "composite_ancestry_model_materially_strengthened": True,
        "exact_59_41_ming_parent_closed": False,
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
    if "## Progress through Batch 12CD" not in md:
        md += dedent('''

        ## Progress through Batch 12CD

        - Direct no-OCR review of received 《革象新書》 pp78-80 physically locks the near-verbatim hundred-ke / half-Zi prose lineage later seen in the 1578 《三命通會》, while preserving the `屬昨日` versus Sanming `為昨日` recension difference.
        - Re-reading the Tianyige Ming-print 《虎鈐經·傳箭》 as a complete sequence shows an older 40↔60 one-ke-step ladder containing many exact Sanming numeric pairs. Sanming changes term/date anchors and caps summer solstice at 59/41 rather than Huqianjing's 60/40.
        - The composite model—older prose lineage + older leak-arrow numeric ladder + Ming adaptation—is materially strengthened, but the exact pre-1578 Ming/Nanjing 59/41 parent remains open. `HPA-ZDATE-006` stays `MISSING_FROM_PRODUCT`; no Hai vote or algorithm reopen is introduced.
        ''')
    mdp.write_text(md, encoding="utf-8")


def state() -> None:
    p = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    d["schema_version"] = "1.89.0"
    a = d["historical_audit"]
    if BATCH_ID not in a["completed_batches"]:
        a["completed_batches"].append(BATCH_ID)
    a["latest_batch_doc"] = BATCH_DOC
    notes = [
        "Batch 12CD physically locks a near-verbatim Gexiang hundred-ke/half-Zi textual antecedent for the Sanming prose, with edition-scope caution that the scanned witness is later received transmission of a Yuan work.",
        "Batch 12CD reclassifies the Huqianjing 40<->60 sequence from generic endpoint parallel to a concrete stepwise numeric-family antecedent sharing many Sanming pairs, while rejecting exact table identity because term anchors and the 60/40 vs 59/41 solstitial cap differ.",
        "Next gate: find a pre-1578 Ming/Nanjing source combining the one-ke ladder with the 59/41 cap and Sanming-like solar-term anchoring; Fullbook upper-five-ke -> Hai remains independently unresolved."
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
