from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-YIMEN-1597-SIZIJING-DIRECT-GLYPH-COLLATION-BS"
PREV_ID = "BATCH-12-ZIWEI-SIZIJING-INDEPENDENT-MING-PRINT-TRANSMISSION-BR"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YIMEN-1597-SIZIJING-DIRECT-GLYPH-COLLATION-BS.md"
RESEARCH_ARTIFACT = "docs/research/ZIWEI-YIMEN-1597-SIZIJING-DIRECT-GLYPH-COLLATION-R1.json"
SOURCE_ID = "EXT-NLC-YIMEN-GUANGDU-1597-SIZIJING"
PRIOR_RESEARCH = "docs/research/ZIWEI-SIZIJING-INDEPENDENT-MING-PRINT-TRANSMISSION-R1.json"

EVIDENCE_HEAD = "8e087490a48c42303c61cfe50840e3568624653a"
EVIDENCE_TREE = "415c67fccddfad0a5f44307b139db8639d6a89bf"
WORKFLOW_RUN = 34824084899
ARTIFACT_ID = 10339620251
ARTIFACT_DIGEST = "sha256:8e728d108f3e4f0b828e7fe6de3e8bc2ac53ae7cc41fec45c2c60fb5f58c5904"
SOURCE_DJVU_SHA256 = "30ffe1ae111fc72d816cb9d2a507bb051b0b67a3eb6be0e80497f02ff4c853e2"
PAGE_HASHES = {
    "p27.jpg": "6356cdbc5880accfdb0d327ba75b7e7709db1b0c1988ac14e1bf71d2c74fe916",
    "p28.jpg": "9a96a2f82313a74d24472d33a789258757ee2dbb5d8f470e94d1c7913d31f64a",
    "p29.jpg": "4ee4441255716dda76ac0a04eb8aa6460feb3f213526667a451a08bcd1038246",
}


def dump_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_continuity_verifier() -> None:
    path = Path("scripts/verify-project-continuity-state-r1.py")
    text = path.read_text(encoding="utf-8")
    if BATCH_ID not in text:
        needle = f'    "{PREV_ID}",\n]'
        replacement = f'    "{PREV_ID}",\n    "{BATCH_ID}",\n]'
        if needle not in text:
            raise SystemExit("cannot locate Batch 12BR tail in continuity verifier")
        text = text.replace(needle, replacement, 1)
    expected = f'LATEST_BATCH_DOC = "{BATCH_DOC}"'
    if expected not in text:
        text, count = re.subn(
            r'^LATEST_BATCH_DOC = ".*"$', expected, text, count=1, flags=re.MULTILINE
        )
        if count != 1:
            raise SystemExit("cannot update LATEST_BATCH_DOC")
    path.write_text(text, encoding="utf-8")


def write_batch_doc() -> None:
    text = dedent(
        f"""\
        # Fusion Chart Historical Provenance Audit R1 — Batch 12BS

        ## 1597《夷門廣牘》本《四字經》直接字形校勘：`唐明皇論`、`古人云`、`雨落`、`亥子丑寅`

        Status: **DIRECT NO-OCR MING-PRINT GLYPH COLLATION COMPLETE FOR THE YIMEN-GUANGDU SIZIJING OPENING / P28 DIRECTLY PRINTS 四字經, 唐德行禪師著, 明周履靖校正, 唐明皇論 / P29 DIRECTLY PRINTS 古人云 AND 天陰雨落難定 AND THE CONTIGUOUS HOUR ORDER 亥子丑寅 / BATCH-12BR YIMEN-SIDE OCR VARIANTS PHYSICALLY ADJUDICATED / YONGLE-DADIAN READINGS REMAIN A SEPARATE RECENSION WITNESS / TAIWAN-NCL EDITION IDENTITY STILL UNRESOLVED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI-BRANCH MECHANICAL VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

        ## 1. Scope and evidence chain

        Batch 12BR proved an independent Ming-print 《四字經》 transmission and isolated three exact variants that could not be trusted from CText automatic OCR alone. The next gate was direct, no-OCR collation of the 1597 《夷門廣牘》 physical scan.

        Reproducible evidence chain:

        - source object: Wikimedia Commons `明刻本夷門廣牘26.djvu`, already bound to the NLC-sourced 1597 《夷門廣牘》 route;
        - source DjVu SHA-256: `{SOURCE_DJVU_SHA256}`;
        - renderer commit/tree: `{EVIDENCE_HEAD}` / `{EVIDENCE_TREE}`;
        - successful exact-HEAD renderer run: `{WORKFLOW_RUN}`;
        - artifact: `{ARTIFACT_ID}`, digest `{ARTIFACT_DIGEST}`;
        - rendering used `ddjvu` and Pillow; no OCR was used for final glyph judgment.

        ## 2. Page 28: title, responsibility and heading

        Direct review of p28 (`{PAGE_HASHES['p28.jpg']}`) reads:

        ```text
        四字經
        唐德行禪師著
        明周履靖校正
        唐明皇論
        ```

        This physically closes the Yimen-side heading as `唐明皇論` and confirms the printed responsibility/correction lines. It does not authenticate a Tang composition date merely from `唐德行禪師著`.

        ## 3. Page 29: three Batch-12BR variants

        Direct review of p29 (`{PAGE_HASHES['p29.jpg']}`) resolves the Yimen-side readings:

        | Variant question | 1597 Yimen physical reading | Result |
        | --- | --- | --- |
        | `古經云` vs `古人云` | `古人云` | YIMEN SIDE DIRECTLY ADJUDICATED |
        | `天陰雨露時難定` vs `天陰雨落難定` | `天陰雨落難定` | YIMEN SIDE DIRECTLY ADJUDICATED |
        | `子丑寅亥` vs `亥子丑寅` | contiguous sequence `亥子丑寅` | YIMEN SIDE DIRECTLY ADJUDICATED |

        The same page visibly continues `便是神仙也有差別`. This batch intentionally avoids a diplomatic transcription of every surrounding glyph because only the three listed variant loci are material to this gate.

        ## 4. Philological effect

        These three differences are no longer merely automatic-OCR artifacts on the Yimen side. The 1597 physical print itself supports `古人云 / 雨落 / 亥子丑寅`.

        The opposite conclusion is **not** authorized: Batch 12BS does not call the Yongle-Dadian `古經云 / 雨露 / 子丑寅亥` readings errors. They remain a separate transmission/recension witness until their own physical-glyph chain is adjudicated. The current classification is:

        ```text
        SAME_SIZIJING_TEXT_FAMILY_AT_LONG_SEQUENCE_LEVEL
        + REAL_RECENSION_VARIATION_NOW_PHYSICALLY_CONFIRMED_ON_YIMEN_SIDE
        + NO_STEMMATIC_WINNER_SELECTED
        ```

        Taiwan NCL 15275-0058 is still not proved to be the same impression, a disbound/extracted copy, or an independent edition relative to the NLC/Yimen object.

        ## 5. Effect on HPA-ZDATE-006

        The literal `亥` here belongs to the difficult-hour list `亥子丑寅`; it is not an instruction to reclassify upper-half Zi as Hai. Likewise `天陰雨落難定` states time-determination difficulty under inclement weather but gives no complete operational time-acquisition procedure.

        Therefore:

        - `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`;
        - direct 1597 Sizijing target-leaf glyph witness increment: `+1` at the textual-variant layer;
        - HPA-ZDATE-006 Hai-branch mechanical vote increment: `0`;
        - Fullbook cloudy/rain current-time acquisition mechanism closed: `false`;
        - runtime winner selected: `false`;
        - candidate collapsed: `false`;
        - algorithm reopen authorized: `false`.

        Global accounting remains `198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families`; provenance defects remain `11/11`; chart algorithm defect/reopen/collapse remain `0/0/0`.

        ## 6. Next gate

        1. Directly collate the Taiwan NCL 15275-0058 《四字經》 opening leaf for the same heading and three variant loci, to test edition/impression identity with physical glyphs.
        2. If accessible, directly collate the Yongle-Dadian physical target leaf for the same loci rather than treating its transcription as final glyph authority.
        3. Separately continue the Fullbook-line cloudy/rain operational-current-time acquisition chain; the Sizijing sentence remains an uncertainty statement rather than a complete clock-recovery method.

        Research record: `{RESEARCH_ARTIFACT}`.
        """
    )
    Path(BATCH_DOC).write_text(text, encoding="utf-8")


def write_research_artifact() -> None:
    research = {
        "schema": "ZIWEI-YIMEN-1597-SIZIJING-DIRECT-GLYPH-COLLATION-R1",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "prior_research": PRIOR_RESEARCH,
        "question": "Do the 1597 Yimen-Guangdu physical scan glyphs resolve the three Sizijing OCR-level variants isolated in Batch 12BR?",
        "source_id": SOURCE_ID,
        "evidence_chain": {
            "source_file": "明刻本夷門廣牘26.djvu",
            "source_djvu_sha256": SOURCE_DJVU_SHA256,
            "renderer_head": EVIDENCE_HEAD,
            "renderer_tree": EVIDENCE_TREE,
            "workflow_run_id": WORKFLOW_RUN,
            "artifact_id": ARTIFACT_ID,
            "artifact_digest": ARTIFACT_DIGEST,
            "render_method": "ddjvu page render -> Pillow JPEG; final adjudication by direct visual review without OCR",
            "rendered_page_sha256": PAGE_HASHES,
        },
        "direct_collation": {
            "p28": {
                "readings": ["四字經", "唐德行禪師著", "明周履靖校正", "唐明皇論"],
                "heading_directly_closed": "唐明皇論",
                "tang_composition_date_authenticated": False,
            },
            "p29": {
                "variant_readings": {
                    "attribution": "古人云",
                    "inclement_phrase": "天陰雨落難定",
                    "difficult_hour_order": "亥子丑寅",
                },
                "continuation_positive_control": "便是神仙也有差別",
            },
        },
        "variant_adjudication": {
            "yimen_古人_vs_yongle_古經": "YIMEN_1597_PHYSICAL=古人云; YONGLE READING PRESERVED SEPARATELY",
            "yimen_雨落_vs_yongle_雨露": "YIMEN_1597_PHYSICAL=天陰雨落難定; YONGLE READING PRESERVED SEPARATELY",
            "yimen_亥子丑寅_vs_yongle_子丑寅亥": "YIMEN_1597_PHYSICAL=亥子丑寅; YONGLE READING PRESERVED SEPARATELY",
            "stemmatic_winner_selected": False,
            "classification": "REAL_RECENSION_VARIATION_PHYSICALLY_CONFIRMED_ON_YIMEN_SIDE",
        },
        "edition_identity": {
            "taiwan_ncl_15275_0058_vs_nlc_yimen_same_impression_proved": False,
            "taiwan_ncl_disbound_from_yimen_proved": False,
            "next_test": "DIRECT_TAIWAN_NCL_TARGET_LEAF_COLLATION",
        },
        "effect": {
            "hpa_zdate_006_status": "MISSING_FROM_PRODUCT",
            "direct_1597_sizijing_target_leaf_glyph_witness_increment": 1,
            "hai_branch_mechanical_vote_increment": 0,
            "fullbook_inclement_current_time_acquisition_mechanism_closed": False,
            "runtime_winner_selected": False,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False,
            "matrix_counts_changed": False,
        },
    }
    dump_json(Path(RESEARCH_ARTIFACT), research)


def update_registry() -> None:
    path = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    src = next(s for s in data["sources"] if s.get("source_id") == SOURCE_ID)
    src["batch_12bs_direct_glyph_collation"] = {
        "source_djvu_sha256": SOURCE_DJVU_SHA256,
        "renderer_head": EVIDENCE_HEAD,
        "workflow_run_id": WORKFLOW_RUN,
        "artifact_id": ARTIFACT_ID,
        "page_28_sha256": PAGE_HASHES["p28.jpg"],
        "page_29_sha256": PAGE_HASHES["p29.jpg"],
        "direct_no_ocr_readings": [
            "四字經",
            "唐德行禪師著",
            "明周履靖校正",
            "唐明皇論",
            "古人云",
            "天陰雨落難定",
            "亥子丑寅",
        ],
        "scope": "DIRECT_PHYSICAL_GLYPH_AUTHORITY_FOR_THE_LISTED_YIMEN_1597_LOCI_ONLY; NOT_A_HPA_ZDATE_006_HAI_BRANCH_MECHANICAL_VOTE",
    }
    note = (
        " Batch 12BS directly collates the exact 1597 Yimen scan without OCR: p28 prints "
        "四字經 / 唐德行禪師著 / 明周履靖校正 / 唐明皇論, and p29 prints "
        "古人云 / 天陰雨落難定 / 亥子丑寅. These readings are glyph authority for the listed "
        "Yimen loci only; they do not establish upper-Zi-to-Hai branch reassignment or a complete "
        "inclement-weather time-acquisition procedure."
    )
    if note.strip() not in src.get("quality_notes", ""):
        src["quality_notes"] = src.get("quality_notes", "") + note
    data["access_date"] = "2026-09-14"
    dump_json(path, data)


def update_matrix() -> None:
    path = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    row = next(r for r in data["rows"] if r.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12bs_yimen_1597_sizijing_direct_glyph_collation"] = {
        "source_id": SOURCE_ID,
        "source_djvu_sha256": SOURCE_DJVU_SHA256,
        "workflow_run_id": WORKFLOW_RUN,
        "artifact_id": ARTIFACT_ID,
        "physical_readings": {
            "heading": "唐明皇論",
            "attribution_formula": "古人云",
            "inclement_phrase": "天陰雨落難定",
            "difficult_hour_order": "亥子丑寅",
        },
        "philological_effect": "BATCH_12BR_YIMEN_SIDE_OCR_VARIANTS_NOW_DIRECTLY_PHYSICALLY_ADJUDICATED; YONGLE_RECENSION_READINGS_REMAIN_SEPARATE",
        "direct_sizijing_target_leaf_glyph_witness_increment": 1,
        "hai_branch_mechanical_vote_increment": 0,
        "candidate_status_effect": "NONE; HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT",
        "runtime_winner_selected": False,
        "algorithm_reopen_authorized": False,
        "research_artifact": RESEARCH_ARTIFACT,
    }
    dump_json(path, data)

    md_path = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md")
    md = md_path.read_text(encoding="utf-8")
    if "## Progress through Batch 12BS" not in md:
        md += dedent(
            """

            ## Progress through Batch 12BS

            - The 1597 NLC/Yimen 《四字經》 opening is now directly collated from a hashed physical DjVu render with no OCR used for final glyph judgment. Page 28 prints `四字經 / 唐德行禪師著 / 明周履靖校正 / 唐明皇論`.
            - Page 29 directly resolves the three Yimen-side Batch-12BR variants as `古人云`, `天陰雨落難定`, and contiguous hour order `亥子丑寅`. CText OCR is corroborated for these exact loci only.
            - The Yongle-Dadian readings `古經云 / 雨露 / 子丑寅亥` remain a separate recension/transmission witness; Batch 12BS does not call them errors or select a stemmatic winner.
            - The literal `亥` belongs to a difficult-hour list, not an upper-Zi-to-Hai reassignment rule. HPA-ZDATE-006 remains `MISSING_FROM_PRODUCT`; Hai-branch mechanical vote, runtime selection, candidate collapse and algorithm reopen remain unchanged.
            - Next high-value gate is direct Taiwan NCL 15275-0058 target-leaf collation for edition/impression comparison, while the Fullbook inclement-current-time acquisition chain remains independently open.
            """
        )
    md_path.write_text(md, encoding="utf-8")


def update_state() -> None:
    path = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    state = json.loads(path.read_text(encoding="utf-8"))
    state["schema_version"] = "1.78.0"
    audit = state["historical_audit"]
    if BATCH_ID not in audit["completed_batches"]:
        audit["completed_batches"].append(BATCH_ID)
    audit["latest_batch_doc"] = BATCH_DOC
    additions = [
        "Batch 12BS directly collates the hashed 1597 Yimen-Guangdu Sizijing physical scan without OCR for final glyph judgment: p28 prints 四字經 / 唐德行禪師著 / 明周履靖校正 / 唐明皇論, while p29 directly prints 古人云 / 天陰雨落難定 / contiguous 亥子丑寅.",
        "The three Batch-12BR Yimen-side OCR variants are now physical-glyph adjudicated, but the Yongle-Dadian readings remain a separate recension witness rather than being declared errors; no stemmatic winner is selected and Taiwan NCL 15275-0058 edition/impression identity remains unresolved.",
        "HPA-ZDATE-006 remains MISSING_FROM_PRODUCT: the literal 亥 is part of the difficult-hour list, not an upper-Zi-to-Hai mechanical rule, and the Sizijing inclement-weather sentence is not a complete time-acquisition procedure. Hai-branch vote/runtime winner/candidate collapse/algorithm reopen remain 0; next gate is direct Taiwan-NCL target-leaf collation plus the separate Fullbook operational-time chain.",
    ]
    focus = audit["current_focus"]
    for item in additions:
        if item not in focus:
            focus.append(item)
    state["updated_at"] = "2026-09-14"
    dump_json(path, state)


def main() -> None:
    update_continuity_verifier()
    write_batch_doc()
    write_research_artifact()
    update_registry()
    update_matrix()
    update_state()


if __name__ == "__main__":
    main()
