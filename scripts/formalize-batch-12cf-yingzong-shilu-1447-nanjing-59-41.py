from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-YINGZONG-SHILU-1447-NANJING-59-41-PHYSICAL-COLLATION-CF"
PREV_ID = "BATCH-12-ZIWEI-LEIBIAN-MING-DUAL-DAYNIGHT-TABLES-CE"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YINGZONG-SHILU-1447-NANJING-59-41-PHYSICAL-COLLATION-CF.md"
RESEARCH = "docs/research/ZIWEI-YINGZONG-SHILU-1447-NANJING-59-41-PHYSICAL-COLLATION-R1.json"
NLC_SRC = "EXT-NLC-YINGZONG-SHILU-V16-1447-NANJING59"
CTEXT_SRC = "EXT-CTEXT-YINGZONG-SHILU-V160-1447-NANJING59"
SANMING_SRC = "EXT-SANMING-NCL-1578-MAIN"

NLC_URL = "https://commons.wikimedia.org/wiki/File:NLC892-CBM0103-366390_%E6%98%8E%E8%8B%B1%E5%AE%97%E7%9D%BF%E7%9A%87%E5%B8%9D%E5%AF%A6%E9%8C%84_%E4%B8%89%E7%99%BE%E5%85%AD%E5%8D%81%E4%B8%80%E5%8D%B7_%E7%AC%AC16%E5%86%8A.pdf"
CTEXT_URL = "https://ctext.org/wiki.pl?chapter=638064&if=gb"
RUN_ID = 34867577915
JOB_ID = 104055174135
ARTIFACT_ID = 10357442493
ARTIFACT_DIGEST = "sha256:f1bd8daba93a6c5752b99da13f465a1802ed01090dc001d2be4075bc7fa14d0f"
SOURCE_SHA256 = "1e9546177289930ae33a64793df94518fcc21c90184c935a30ea975461990268"
TRIGGER_COMMIT = "ad9aa62b0c72cc96f98dadf278b0ad01cc5be746"
PAGE_SHA256 = {
    "21": "613e026a94949cf721088225d7215dedd94f9a8faad2529f164e8886946975fb",
    "28": "b7d95f00fd529468c4242f60b7255b5305df6298d14841a9d9f6ac03eccccfea",
    "30": "fa8f7c30b2ede6b10379fb12c4ba2366ab8b93968cfb201ae565c4ae30852b35",
}


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate 12CE tail in continuity verifier")
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
    if NLC_SRC not in ids:
        d["sources"].append({
            "source_id": NLC_SRC,
            "title": "《明英宗睿皇帝實錄》三百六十一卷第16冊，卷160，正統十二年十一月甲寅條",
            "author_attribution": "〔明〕孫繼宗等纂修",
            "historical_period": "MING_OFFICIAL_RECORD_EVENT_1447; SURVIVING_COPY_CATALOGUED_MING_MANUSCRIPT_1368_1644",
            "edition": "抄本，12行24字，平館藏書；第16冊收卷158-169；Wikimedia/NLC metadata",
            "provider": "National Library of China digitization via Wikimedia Commons",
            "url": NLC_URL,
            "source_role": "DIRECT_PHYSICAL_PRE1578_OFFICIAL_MING_RECORD_FOR_NANJING_59_KE_AND_BEIJING_62_KE_SOLSTITIAL_LOCALITY_STANDARD",
            "quality_notes": "Batch 12CF direct no-OCR review. PDF p21 opens 卷160 / 正統十二年十一月; p28 contains the 甲寅 Peng Deqing memorial; p30 opens 卷161, binding the target securely inside vol.160. The physical text directly prints Nanjing winter-solstice night 59 and summer-solstice day 59, Beijing corresponding 62 values, and states palace/government clepsydra arrows were still the Nanjing old style. The complementary 41/38 values are derived only under the independently established 100-ke day/night framework; they are not printed as numerals in this memorial."
        })
    if CTEXT_SRC not in ids:
        d["sources"].append({
            "source_id": CTEXT_SRC,
            "title": "中國哲學書電子化計劃《大明英宗睿皇帝實錄》卷160 received-text control",
            "historical_period": "RECEIVED_TEXT_CONTROL_FOR_1447_EVENT",
            "provider": "Chinese Text Project",
            "url": CTEXT_URL,
            "source_role": "SEARCHABLE_RECEIVED_TEXT_CONTROL_MATCHING_THE_PHYSICAL_1447_MEMORIAL",
            "quality_notes": "Used as navigation/transcription control only; final glyph/date/location judgment rests on the NLC physical facsimile."
        })
    d["access_date"] = "2026-09-15"
    dump(p, d)


def write_research() -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-YINGZONG-SHILU-1447-NANJING-59-41-PHYSICAL-COLLATION-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Is the Nanjing 59-ke solstitial locality standard directly attested before the 1578 Sanming Tonghui witness, rather than only explained by later Ming technical works?",
        "physical_source": {
            "source_id": NLC_SRC,
            "metadata": "Wikimedia/NLC: 明英宗睿皇帝實錄三百六十一卷, 第16冊, 抄本, 明[1368-1644], 104 pages; volume contains 卷158-169",
            "event_date": "正統十二年十一月甲寅 / 1447",
            "workflow_run_id": RUN_ID,
            "job_id": JOB_ID,
            "artifact_id": ARTIFACT_ID,
            "artifact_digest": ARTIFACT_DIGEST,
            "source_pdf_sha256": SOURCE_SHA256,
            "render_trigger_commit": TRIGGER_COMMIT,
            "page_count": 104,
            "page_sha256": PAGE_SHA256,
            "ocr_used_for_glyph_claims": False
        },
        "physical_binding": {
            "p21": "directly opens 大明英宗睿皇帝實錄卷之一百六十 and 正統十二年十一月",
            "p28": "contains 甲寅欽天監監正彭德清 memorial and the Nanjing/Beijing latitude, sunrise/sunset and ke comparison",
            "p30": "directly opens 卷之一百六十一 / 正統十二年十二月, proving p28 lies inside vol.160"
        },
        "secure_direct_reading": {
            "date_marker": "甲寅",
            "speaker": "欽天監監正彭德清",
            "nanjing_latitude": "北極出地三十六度",
            "beijing_latitude": "北極出地四十度強",
            "nanjing_winter": "冬至日出辰初初刻，入申正四刻，夜刻五十九",
            "nanjing_summer": "夏至日出寅正四刻，入戌初初刻，晝刻五十九",
            "beijing_winter": "冬至日出辰初一刻，入申正二刻，夜刻六十二",
            "beijing_summer": "夏至日出寅正二刻，入戌初一刻，晝刻六十二",
            "institutional_note": "今宮禁及官府漏箭皆南京舊式不可用",
            "imperial_response": "上令內官監改造"
        },
        "numerical_adjudication": {
            "nanjing_59_direct": True,
            "nanjing_41_printed_in_this_memorial": False,
            "nanjing_41_status": "COMPLEMENT_DERIVED_FROM_INDEPENDENTLY_ESTABLISHED_100_KE_DAY_NIGHT_TOTAL",
            "beijing_62_direct": True,
            "beijing_38_printed_in_this_memorial": False,
            "beijing_38_status": "COMPLEMENT_DERIVED_FROM_INDEPENDENTLY_ESTABLISHED_100_KE_DAY_NIGHT_TOTAL",
            "pre1578_nanjing_59_ke_locality_standard_closed": True,
            "pre1578_complete_sanming_multipoint_table_closed": False
        },
        "historical_consequence": {
            "later_1600_xingyunlu_needed_to_prove_pre1578_59": False,
            "later_1600_xingyunlu_role_after_this_batch": "SECONDARY/LATER EXPLANATORY CONFIRMATION OF A STANDARD NOW DIRECTLY ATTESTED IN A 1447 OFFICIAL RECORD",
            "sanming_1578_summer_59_has_pre1578_ming_nanjing_precedent": True,
            "sanming_direct_copy_from_this_memorial_proved": False,
            "remaining_genealogy_problem": "Find a pre-1578 table or generative rule that carries the Sanming-like intermediate anchors (e.g. 42/58, 45/55, 47/53, 48/52) into the Nanjing 59-ke solstitial layer."
        },
        "adjudication": {
            "exact_pre1578_nanjing_59_layer_closed": True,
            "exact_pre1578_sanming_multipoint_table_parent_closed": False,
            "new_runtime_candidate_created": False,
            "runtime_winner_selected": False,
            "upper_zi_to_hai_mechanical_vote_increment": 0,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False
        },
        "impact_on_hpa_zdate_006": {
            "status_before": "MISSING_FROM_PRODUCT",
            "status_after": "MISSING_FROM_PRODUCT",
            "reason": "The official 1447 locality/timekeeping evidence closes the pre-1578 Nanjing 59-ke historical layer but does not establish the Fullbook-specific upper-five-ke -> previous-night Hai branch mechanism.",
            "next_gate": "Trace the 1447-to-1578 multipoint table transmission/generative bridge, while independently continuing the upper-five-ke -> Hai physical-source search."
        }
    })


def write_doc() -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit R1 — Batch 12CF

    ## 1447《明英宗實錄》物理核讀：南京59刻層前推至正統十二年官方記錄

    Status: **PRE-1578 OFFICIAL MING RECORD PHYSICALLY CONFIRMS NANJING SOLSTITIAL 59-KE STANDARD AND BEIJING 62-KE CONTRAST / PALACE AND GOVERNMENT CLEPSYDRA ARROWS EXPLICITLY IDENTIFIED AS NANJING OLD STYLE / 59 IS DIRECTLY PRINTED; 41 IS ONLY THE HUNDRED-KE COMPLEMENT, NOT A PRINTED NUMERAL IN THIS MEMORIAL / PRE-1578 NANJING 59 LAYER CLOSED / COMPLETE SANMING MULTIPOINT TABLE GENEALOGY STILL OPEN / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO HAI VOTE / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

    ## 1. Why this is decisive after 12CE

    Batch 12CE showed that Ming calendrical transmission could preserve multiple day/night-ke tables side-by-side, and that the later 1600 Xing Yunlu text explains a Nanjing 59-ke layer distinct from Yandu 62-ke. The remaining chronology problem was whether Nanjing 59 could be locked **before 1578**.

    Batch 12CF closes that subproblem with an official 1447 record.

    ## 2. Physical source binding

    NLC/Wikimedia object:

    ```text
    TITLE=明英宗睿皇帝實錄 三百六十一卷 第16冊
    AUTHOR=孫繼宗等纂修
    EDITION=抄本, 12行24字, 平館藏書
    CATALOG_DATE=明[1368-1644]
    CONTENTS=卷158-169
    PDF_PAGES=104
    RUN={RUN_ID}
    JOB={JOB_ID}
    ARTIFACT={ARTIFACT_ID}
    ARTIFACT_DIGEST={ARTIFACT_DIGEST}
    SOURCE_SHA256={SOURCE_SHA256}
    P21_SHA256={PAGE_SHA256['21']}
    P28_SHA256={PAGE_SHA256['28']}
    P30_SHA256={PAGE_SHA256['30']}
    OCR_USED_FOR_FINAL_GLYPH_JUDGMENT=false
    ```

    Page binding is direct: p21 opens 卷160 and 正統十二年十一月; p28 contains the target 甲寅 memorial; p30 opens 卷161 / 十二月.

    ## 3. Secure p28 reading

    The target passage identifies `欽天監監正彭德清` and records a measured locality difference between Nanjing and Beijing. Secure core:

    ```text
    南京北極出地三十六度，北京出地四十度強。
    南京冬至 ... 夜刻五十九；夏至 ... 晝刻五十九。
    北京冬至 ... 夜刻六十二；夏至 ... 晝刻六十二。
    各有長短差異。今宮禁及官府漏箭，皆南京舊式，不可用。
    上令內官監改造。
    ```

    This is not a late retrospective explanation: it is an official entry dated 正統十二年十一月甲寅 (1447), about 130 years before the 1578 Sanming witness.

    ## 4. Precision firewall: 59 is printed; 41 is derived

    The memorial itself prints the Nanjing extreme as `五十九` and the Beijing extreme as `六十二`. It does **not** print the complementary numerals `四十一` or `三十八` in this locus.

    Therefore the safe formulation is:

    ```text
    DIRECT: Nanjing solstitial extreme = 59 ke
    DIRECT: Beijing solstitial extreme = 62 ke
    DERIVED under the independently established 100-ke day/night total:
      Nanjing complement = 41
      Beijing complement = 38
    ```

    This distinction is now machine-recorded so later work cannot silently turn an inferred complement into a direct quotation.

    ## 5. Historical consequence for Sanming

    The 1578 Sanming display has `夏至 59/41`. Batch 12CF now proves that a Ming Nanjing 59-ke solstitial standard was already officially articulated in 1447. Accordingly:

    - the **pre-1578 Nanjing 59 layer is closed**;
    - Xing Yunlu 1600 is no longer needed to establish that layer chronologically; it remains a useful later explanatory confirmation;
    - the Sanming summer-solstice 59 value has a genuine pre-1578 Ming/Nanjing technical precedent;
    - but this does **not** prove Sanming copied the Yingzong Shilu memorial or any specific official table.

    ## 6. What remains open

    The unresolved genealogy is now narrower:

    ```text
    1447 official Nanjing 59-ke layer  ->  ?  ->  1578 Sanming multipoint table
    ```

    We still need a pre-1578 table, manual, almanac or generative rule that links the Nanjing 59-ke endpoint to Sanming-like intermediate anchors such as `42/58`, `45/55`, `47/53`, `48/52`.

    ## 7. Product adjudication

    For `HPA-ZDATE-006`:

    - pre-1578 Nanjing 59-ke locality layer: **closed / official physical evidence**;
    - exact pre-1578 Sanming multipoint table parent: **open**;
    - upper-Zi -> Hai mechanical vote: **0**;
    - runtime candidate/winner/collapse: **none**;
    - algorithm reopen: **no**;
    - status: **MISSING_FROM_PRODUCT**.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def matrix() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next(x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12cf_yingzong_shilu_1447_nanjing_59_41"] = {
        "source_ids": [NLC_SRC, CTEXT_SRC, SANMING_SRC],
        "pre1578_official_nanjing_59_ke_physically_attested": True,
        "pre1578_official_beijing_62_ke_physically_attested": True,
        "nanjing_41_directly_printed_in_memorial": False,
        "nanjing_41_is_hundred_ke_complement": True,
        "pre1578_nanjing_59_layer_closed": True,
        "exact_pre1578_sanming_multipoint_table_parent_closed": False,
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
    if "## Progress through Batch 12CF" not in md:
        md += dedent('''

        ## Progress through Batch 12CF

        - NLC physical collation of 《明英宗睿皇帝實錄》卷160, 正統十二年十一月甲寅 (1447), directly records Nanjing solstitial 59-ke extrema, Beijing 62-ke extrema, and states that palace/government clepsydra arrows were still the Nanjing old style.
        - This closes the pre-1578 Ming/Nanjing 59-ke locality layer. The complementary 41/38 values are explicitly classified as hundred-ke complements, not numerals directly printed in this memorial.
        - The exact bridge from the 1447 Nanjing endpoint to Sanming's 1578 multipoint solar-term sequence remains open; no Fullbook upper-five-ke -> Hai vote, runtime winner, candidate collapse or algorithm reopen is introduced.
        ''')
    mdp.write_text(md, encoding="utf-8")


def state() -> None:
    p = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    d["schema_version"] = "1.91.0"
    a = d["historical_audit"]
    if BATCH_ID not in a["completed_batches"]:
        a["completed_batches"].append(BATCH_ID)
    a["latest_batch_doc"] = BATCH_DOC
    notes = [
        "Batch 12CF physically closes the pre-1578 Ming/Nanjing 59-ke locality layer: the 1447 Yingzong Shilu Peng Deqing memorial directly records Nanjing 59-ke solstitial extrema versus Beijing 62-ke and identifies palace/government clepsydra arrows as Nanjing old style.",
        "Precision firewall: the 1447 memorial directly prints 59 and 62; 41 and 38 are hundred-ke complements, not directly printed numerals in that locus.",
        "Next gate: find the pre-1578 bridge from the 1447 Nanjing 59-ke endpoint to Sanming's intermediate 42/58, 45/55, 47/53, 48/52-style anchors; Fullbook upper-five-ke -> Hai remains independently unresolved."
    ]
    for n in notes:
        if n not in a["current_focus"]:
            a["current_focus"].append(n)
    d["updated_at"] = "2026-09-15"
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
