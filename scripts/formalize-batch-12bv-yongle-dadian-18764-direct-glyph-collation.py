from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-YONGLE-DADIAN-18764-DIRECT-GLYPH-COLLATION-BV"
PREV_ID = "BATCH-12-ZIWEI-TAIWAN-NCL-FIRST-PARTY-VIEWER-ACCESS-BOUNDARY-BU"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YONGLE-DADIAN-18764-DIRECT-GLYPH-COLLATION-BV.md"
RESEARCH_ARTIFACT = "docs/research/ZIWEI-YONGLE-DADIAN-18764-DIRECT-GLYPH-COLLATION-R1.json"
SRC_YONGLE = "EXT-TIME-YONGLE-DADIAN-18764-QIANDINGSHU-SIZIJING"
SRC_YIMEN = "EXT-NLC-YIMEN-GUANGDU-1597-SIZIJING"
PRIOR_YONGLE = "docs/research/ZIWEI-YONGLE-DADIAN-18764-INCLEMENT-BIRTH-TIME-EARLY-TEXTUAL-BRIDGE-R1.json"
PRIOR_YIMEN = "docs/research/ZIWEI-YIMEN-1597-SIZIJING-DIRECT-GLYPH-COLLATION-R1.json"

EVIDENCE_HEAD = "0f5a6daa9e7e0bc3901412083c07dd0183f58a88"
EVIDENCE_TREE = "0c2f707d6dcea3e8e8b2b542c7bab427954b1006"
WORKFLOW_RUN = 34826953257
ARTIFACT_ID = 10340044845
ARTIFACT_DIGEST = "sha256:7ba40557f877f583830ee7d66838473ad5bbd73f99fb73cc679f220e8b83f05b"
SOURCE_PDF_SHA256 = "69a2f0e63685d674fd5e0ddcd7a5ccd687a725f19cc601f8e77d6d446beb9f87"
PAGE_HASHES = {
    "p2.jpg": "af9453278946f1b289b74aaae59d43e1bd9a8effa25dc4d8a351f77bf2047006",
    "p3.jpg": "12e3f12fc9aeeeab06c459788757de0325f0f6214e1d062a77cc4c77483d038f",
    "p4.jpg": "f42749d1e299caf73e46fde8d811c891a0e919d38c0077c1b8736c94cd420fdb",
}
COMMONS_URL = "https://commons.wikimedia.org/wiki/File:%E6%B0%B8%E6%A8%82%E5%A4%A7%E5%85%B818764.pdf"
WIKISOURCE_PAGE = "https://zh.wikisource.org/wiki/Page:%E6%B0%B8%E6%A8%82%E5%A4%A7%E5%85%B818764.pdf/3"


def dump_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_continuity_verifier() -> None:
    path = Path("scripts/verify-project-continuity-state-r1.py")
    text = path.read_text(encoding="utf-8")
    if BATCH_ID not in text:
        needle = f'    "{PREV_ID}",\n]'
        replacement = f'    "{PREV_ID}",\n    "{BATCH_ID}",\n]'
        if needle not in text:
            raise SystemExit("cannot locate Batch 12BU tail in continuity verifier")
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
        # Fusion Chart Historical Provenance Audit R1 — Batch 12BV

        ## 《永樂大典》卷18764《四字經序》目標頁直接字形校勘：`古經云`、`雨露`、`子丑寅亥`

        Status: **DIRECT NO-OCR PHYSICAL-GLYPH COLLATION COMPLETE FOR YONGLE-DADIAN 18764 PUBLIC FACSIMILE PAGE 3 / PHYSICAL PAGE DIRECTLY READS 四字經序 AND 且子丑寅亥 / 四箇時辰難以推分 / 古經云 / 天陰雨露時難定 / 便是神仙也有差 / BATCH-12BQ TRANSCRIPTION NOW PHYSICALLY ADJUDICATED / 1597 YIMEN PHYSICAL READINGS REMAIN 古人云 / 雨落 / 亥子丑寅 / REAL RECENSION VARIATION NOW PHYSICALLY CONFIRMED ON BOTH SIDES / NO STEMMATIC OR RUNTIME WINNER SELECTED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI-BRANCH MECHANICAL VOTE +0 / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

        ## 1. Scope and exact evidence chain

        Batch 12BQ located the inclement-birth-time passage on public scan page 3 of 《永樂大典》卷18764 but deliberately withheld glyph authority because the project had not yet rendered the facsimile directly. Batch 12BS subsequently established the 1597 《夷門廣牘》 side from physical glyphs. Batch 12BV closes the missing Yongle-side physical collation.

        Exact evidence chain:

        - source: Wikimedia Commons `永樂大典18764.pdf`, 42 pages;
        - Commons file page: `{COMMONS_URL}`;
        - Wikisource target-page binding: `{WIKISOURCE_PAGE}`;
        - source PDF SHA-256: `{SOURCE_PDF_SHA256}`;
        - renderer commit/tree: `{EVIDENCE_HEAD}` / `{EVIDENCE_TREE}`;
        - successful GitHub Actions run: `{WORKFLOW_RUN}`;
        - artifact: `{ARTIFACT_ID}`, digest `{ARTIFACT_DIGEST}`;
        - rendered target page 3 SHA-256: `{PAGE_HASHES['p3.jpg']}`;
        - final glyph judgment was made by direct visual review of the 300-dpi rendered facsimile; no OCR was used.

        ## 2. Direct page-3 reading

        Direct visual review of physical scan page 3 reads the local sequence as:

        ```text
        四字經序
        ...
        內有同時共數者有富有貴有壽有夭殊不知刻差時別且子丑寅亥
        四箇時辰難以推分古經云天陰雨露時難定便是神仙也有差
        旦夕將月建長短而推言萬無一失矣
        ```

        The material loci are therefore physically adjudicated on the Yongle-Dadian extant facsimile side as:

        | Locus | Direct physical reading |
        | --- | --- |
        | quoted-source formula | `古經云` |
        | inclement phrase | `天陰雨露時難定` |
        | difficult-hour order | `子丑寅亥` |
        | positive continuation | `便是神仙也有差` |

        This upgrades Batch 12BQ from convergent transcription plus facsimile locator to direct no-OCR physical-glyph authority for these exact loci.

        ## 3. Two-sided physical recension comparison

        Batch 12BS directly read the securely dated 1597 《夷門廣牘》 《四字經》 witness as:

        ```text
        唐明皇論
        ...
        亥子丑寅
        古人云
        天陰雨落難定
        便是神仙也有差別
        ```

        Batch 12BV now establishes that the apparent differences are not artifacts of CText OCR on one side or Wikisource transcription on the other. The admissible classification is:

        ```text
        SAME_SIZIJING_TEXT_FAMILY_AT_LONG_SEQUENCE_LEVEL
        + REAL_RECENSION_VARIATION_PHYSICALLY_CONFIRMED_ON_BOTH_SIDES
        + YONGLE_EXTANT_PHYSICAL_RECENSION = JIAJING_DUPLICATE_LINEAGE
        + YIMEN_PHYSICAL_PRINT = 1597
        + NO_STEMMATIC_WINNER_SELECTED
        ```

        The physical readings do not establish that either recension is the archetype. `古經` identity remains unresolved, Taiwan NCL 15275-0058 target-body glyphs remain inaccessible at the current lawful public-route boundary, and no direct-copying direction is inferred.

        ## 4. Effect on HPA-ZDATE-006

        The sequence `子丑寅亥` is a list of four difficult birth hours. It does **not** say that the upper half of Zi hour becomes Hai, nor does it define a runtime branch-reclassification function. Likewise `天陰雨露時難定` describes uncertainty under inclement conditions but gives no complete current-time acquisition mechanism.

        Therefore:

        - `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`;
        - direct Yongle-Dadian target-page physical-glyph witness increment: `+1` at the textual-variant layer;
        - two-sided physical recension-variation confirmation: `true`;
        - Hai-branch mechanical vote increment: `0`;
        - Fullbook cloudy/rain current-time acquisition mechanism closed: `false`;
        - runtime winner selected: `false`;
        - candidate collapsed: `false`;
        - algorithm reopen authorized: `false`.

        Global accounting remains `198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families`; provenance defects remain `11/11`; chart algorithm defect/reopen/collapse remain `0/0/0`.

        ## 5. Next gate

        1. Continue the distinct Fullbook-line operational question: find an explicit cloudy/rainy **current-time acquisition procedure**, not merely a statement that time is difficult to determine.
        2. Continue lawful search for a Taiwan NCL 15275-0058 target-body image route; if eventually obtained, compare it against both physically adjudicated recensions without assuming impression identity.
        3. Treat the Yongle/Yimen physical differences as genuine recension evidence for philology and provenance only; do not convert their four-hour order into a late-Zi-to-Hai mechanical vote without an explicit operational rule.

        Research record: `{RESEARCH_ARTIFACT}`.
        """
    )
    Path(BATCH_DOC).write_text(text, encoding="utf-8")


def write_research_artifact() -> None:
    data = {
        "schema": "ZIWEI-YONGLE-DADIAN-18764-DIRECT-GLYPH-COLLATION-R1",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "prior_yongle_research": PRIOR_YONGLE,
        "prior_yimen_research": PRIOR_YIMEN,
        "question": "Do the Yongle-Dadian 18764 physical facsimile glyphs directly confirm the three transcription-level loci and establish real recension variation against the 1597 Yimen witness?",
        "source_id": SRC_YONGLE,
        "evidence_chain": {
            "source_file": "永樂大典18764.pdf",
            "source_pdf_sha256": SOURCE_PDF_SHA256,
            "public_scan_page_count": 42,
            "target_page_1_based": 3,
            "renderer_head": EVIDENCE_HEAD,
            "renderer_tree": EVIDENCE_TREE,
            "workflow_run_id": WORKFLOW_RUN,
            "artifact_id": ARTIFACT_ID,
            "artifact_digest": ARTIFACT_DIGEST,
            "render_method": "pdftoppm page render at 300 dpi; final adjudication by direct visual review without OCR",
            "rendered_page_sha256": PAGE_HASHES,
        },
        "direct_collation": {
            "heading": "四字經序",
            "difficult_hour_order": "子丑寅亥",
            "attribution": "古經云",
            "inclement_phrase": "天陰雨露時難定",
            "positive_continuation": "便是神仙也有差",
            "local_sequence": "且子丑寅亥四箇時辰難以推分古經云天陰雨露時難定便是神仙也有差",
        },
        "two_sided_recension_comparison": {
            "yongle_physical": {
                "heading": "四字經序",
                "attribution": "古經云",
                "inclement_phrase": "天陰雨露時難定",
                "difficult_hour_order": "子丑寅亥",
            },
            "yimen_1597_physical": {
                "heading": "唐明皇論",
                "attribution": "古人云",
                "inclement_phrase": "天陰雨落難定",
                "difficult_hour_order": "亥子丑寅",
            },
            "classification": "REAL_RECENSION_VARIATION_PHYSICALLY_CONFIRMED_ON_BOTH_SIDES",
            "same_text_family_at_long_sequence_level": True,
            "stemmatic_winner_selected": False,
            "direct_copying_direction_proved": False,
        },
        "dating_firewall": {
            "yongle_textual_incorporation_layer": "YONGLE-DADIAN COMPILATION TRADITION",
            "yongle_extant_physical_recension": "MING_JIAJING_DUPLICATE_LINEAGE",
            "extant_1408_original_leaf_claimed": False,
            "yimen_physical_print_year": 1597,
        },
        "effect": {
            "hpa_zdate_006_status": "MISSING_FROM_PRODUCT",
            "direct_yongle_target_page_glyph_witness_increment": 1,
            "two_sided_physical_recension_variation_confirmed": True,
            "hai_branch_mechanical_vote_increment": 0,
            "fullbook_inclement_current_time_acquisition_mechanism_closed": False,
            "runtime_winner_selected": False,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False,
            "matrix_counts_changed": False,
        },
    }
    dump_json(Path(RESEARCH_ARTIFACT), data)


def update_registry() -> None:
    path = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    src = next(s for s in data["sources"] if s.get("source_id") == SRC_YONGLE)
    src["batch_12bv_direct_glyph_collation"] = {
        "source_pdf_sha256": SOURCE_PDF_SHA256,
        "renderer_head": EVIDENCE_HEAD,
        "workflow_run_id": WORKFLOW_RUN,
        "artifact_id": ARTIFACT_ID,
        "artifact_digest": ARTIFACT_DIGEST,
        "page_3_sha256": PAGE_HASHES["p3.jpg"],
        "direct_no_ocr_readings": ["四字經序", "子丑寅亥", "古經云", "天陰雨露時難定", "便是神仙也有差"],
        "scope": "DIRECT_PHYSICAL_GLYPH_AUTHORITY_FOR_LISTED_YONGLE-DADIAN PAGE-3 LOCI; NOT A HPA-ZDATE-006 HAI-BRANCH MECHANICAL VOTE",
    }
    yimen = next(s for s in data["sources"] if s.get("source_id") == SRC_YIMEN)
    yimen["batch_12bv_two_sided_physical_recension_comparison"] = {
        "other_source_id": SRC_YONGLE,
        "yongle_readings": ["古經云", "天陰雨露時難定", "子丑寅亥"],
        "yimen_1597_readings": ["古人云", "天陰雨落難定", "亥子丑寅"],
        "classification": "REAL_RECENSION_VARIATION_PHYSICALLY_CONFIRMED_ON_BOTH_SIDES",
        "stemmatic_winner_selected": False,
    }
    data["access_date"] = "2026-09-14"
    dump_json(path, data)


def update_matrix() -> None:
    path = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    row = next(r for r in data["rows"] if r.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12bv_yongle_dadian_18764_direct_glyph_collation"] = {
        "source_ids": [SRC_YONGLE, SRC_YIMEN],
        "workflow_run_id": WORKFLOW_RUN,
        "artifact_id": ARTIFACT_ID,
        "yongle_direct_readings": ["四字經序", "子丑寅亥", "古經云", "天陰雨露時難定", "便是神仙也有差"],
        "yimen_1597_direct_readings": ["唐明皇論", "亥子丑寅", "古人云", "天陰雨落難定", "便是神仙也有差別"],
        "two_sided_physical_recension_variation_confirmed": True,
        "stemmatic_winner_selected": False,
        "hai_branch_mechanical_vote_increment": 0,
        "candidate_status_effect": "NONE; HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT",
        "runtime_winner_selected": False,
        "algorithm_reopen_authorized": False,
        "research_artifact": RESEARCH_ARTIFACT,
    }
    dump_json(path, data)

    md_path = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md")
    md = md_path.read_text(encoding="utf-8")
    if "## Progress through Batch 12BV" not in md:
        md += dedent(
            """

            ## Progress through Batch 12BV

            - The public facsimile of 《永樂大典》卷18764 has now been directly rendered and reviewed without OCR. Page 3 physically reads `四字經序`, `且子丑寅亥`, `四箇時辰難以推分`, `古經云`, `天陰雨露時難定`, and `便是神仙也有差`.
            - This closes the exact-glyph authority gap left by Batch 12BQ. Combined with Batch 12BS, both sides of the Sizijing comparison now have physical glyph authority: Yongle/Jiajing-duplicate recension `古經 / 雨露 / 子丑寅亥` versus 1597 Yimen `古人 / 雨落 / 亥子丑寅`.
            - The differences are therefore genuine recension variation, not OCR/transcription noise. No archetype, copying direction, stemmatic winner or runtime winner is selected.
            - The four-hour ordering remains a textual list, not an operational late-Zi-to-Hai reclassification rule. HPA-ZDATE-006 remains `MISSING_FROM_PRODUCT`; Hai mechanical vote, candidate collapse and algorithm reopen remain unchanged.
            """
        )
    md_path.write_text(md, encoding="utf-8")


def update_state() -> None:
    path = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    state = json.loads(path.read_text(encoding="utf-8"))
    state["schema_version"] = "1.81.0"
    audit = state["historical_audit"]
    if BATCH_ID not in audit["completed_batches"]:
        audit["completed_batches"].append(BATCH_ID)
    audit["latest_batch_doc"] = BATCH_DOC
    additions = [
        "Batch 12BV directly renders and collates Yongle-Dadian 18764 public facsimile page 3 without OCR. Physical glyphs read 四字經序 / 且子丑寅亥 / 四箇時辰難以推分 / 古經云 / 天陰雨露時難定 / 便是神仙也有差, closing the exact-glyph authority gap left by Batch 12BQ.",
        "Together with Batch 12BS, real Sizijing recension variation is now physically confirmed on both sides: Yongle extant Jiajing-duplicate recension 古經/雨露/子丑寅亥 versus 1597 Yimen 古人/雨落/亥子丑寅. No archetype, copying direction or stemmatic winner is selected.",
        "Batch 12BV does not convert the four-hour list into a late-Zi-to-Hai mechanical rule and does not provide a cloudy/rainy current-time acquisition procedure. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; Hai mechanical vote/runtime winner/candidate collapse/algorithm reopen remain unchanged. Next priority is the distinct Fullbook operational-current-time mechanism plus lawful Taiwan target-leaf access if it becomes available.",
    ]
    for item in additions:
        if item not in audit["current_focus"]:
            audit["current_focus"].append(item)
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
