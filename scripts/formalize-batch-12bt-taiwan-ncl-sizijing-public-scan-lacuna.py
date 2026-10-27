from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-TAIWAN-NCL-SIZIJING-PUBLIC-SCAN-LACUNA-BT"
PREV_ID = "BATCH-12-ZIWEI-YIMEN-1597-SIZIJING-DIRECT-GLYPH-COLLATION-BS"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TAIWAN-NCL-SIZIJING-PUBLIC-SCAN-LACUNA-BT.md"
RESEARCH_ARTIFACT = "docs/research/ZIWEI-TAIWAN-NCL-SIZIJING-PUBLIC-SCAN-LACUNA-R1.json"
SRC_CATALOG = "EXT-TW-NCL-SIZIJING-15275-0058-MING-WANLI"
SRC_SCAN = "EXT-COMMONS-NCL-15275-0058-SIZIJING-SCAN"
PRIOR_RESEARCH = "docs/research/ZIWEI-YIMEN-1597-SIZIJING-DIRECT-GLYPH-COLLATION-R1.json"

EVIDENCE_HEAD = "46c4a4493d92b7697f78163f582402fbc02691d7"
EVIDENCE_TREE = "7744f048e0dd532a3d41209868660a46b28433d9"
WORKFLOW_RUN = 34825456673
ARTIFACT_ID = 10340620803
ARTIFACT_DIGEST = "sha256:5448669de7e40c697a6a80007941514467cdb4dfb1880ac726fcf4f97ce32ffc"
SOURCE_PDF_SHA256 = "e99bee3b210d9b078b11778f2e504277c821520ba16677b917a4a434661dbe02"
PAGE_COUNT = 21
PAGE_HASHES = {
    "p01": "5545620326b950aca74c508394971f063177c819ddc2f3ac7b513949fd2188f8",
    "p03": "2a1fface07816bc46764da1be57b8e0d10f75c18fea3096d6678a2bebbf922cc",
    "p04": "8ae30532d8d0bfc64886ff88e44ac9ed84af7537cb7d5b5496a62c213f2cd794",
    "p21": "2921471d1ee787ce7d250225bfd2218ad57be740a0d914729b71c35a7388956c",
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
            raise SystemExit("cannot locate Batch 12BS tail in continuity verifier")
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
        # Fusion Chart Historical Provenance Audit R1 — Batch 12BT

        ## 臺灣國圖 15275-0058《四字經》公開掃描缺頁控制：目錄列「唐明皇論」，可見正文由「甲甲」起

        Status: **TAIWAN-NCL MING-WANLI SIZIJING 21-PAGE PUBLIC SCAN DIRECTLY REVIEWED WITHOUT OCR / P01 TOC DIRECTLY LISTS 唐明皇論 BEFORE 甲甲 / P03 DIRECTLY READS 四字經目錄終 / P04 VISIBLE BODY OPENS 四字經 THEN 甲甲, WITH NO EXPOSED 唐明皇論 BODY LEAF / P21 CONTINUES THROUGH 癸癸 MATERIAL / PUBLIC-SCAN TARGET-LEAF LACUNA CONFIRMED / PHYSICAL-HOLDING LACUNA NOT PROVED / YIMEN-TAIWAN INTERNAL-UNIT CORRESPONDENCE STRENGTHENED / SAME IMPRESSION OR DISBOUND IDENTITY NOT PROVED / TARGET VARIANT GLYPHS NOT OBSERVED IN TAIWAN SCAN / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI-BRANCH MECHANICAL VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

        ## 1. Scope and exact evidence chain

        Batch 12BS directly adjudicated the 1597 《夷門廣牘》 side of the 《四字經》 opening variants as `唐明皇論 / 古人云 / 天陰雨落難定 / 亥子丑寅`. Its next gate was to collate the independent Taiwan National Central Library single-title object 15275-0058.

        The full public 21-page PDF derivative was therefore downloaded and rendered without OCR:

        - source: `NCL-15275-0058_四字經.pdf`, Wikimedia Commons derivative sourced to Taiwan National Central Library;
        - source PDF SHA-256: `{SOURCE_PDF_SHA256}`;
        - page count: `{PAGE_COUNT}`;
        - renderer commit/tree: `{EVIDENCE_HEAD}` / `{EVIDENCE_TREE}`;
        - successful GitHub Actions run: `{WORKFLOW_RUN}`;
        - artifact: `{ARTIFACT_ID}`, digest `{ARTIFACT_DIGEST}`;
        - final judgments below are direct visual readings of the rendered physical scan, not OCR output.

        ## 2. Page 1: the internal unit is explicitly in the Taiwan witness

        Page 1 (`{PAGE_HASHES['p01']}`) directly reads the heading `四字經目錄`. The first listed internal unit is `唐明皇論`, followed by `甲甲` and the stem-pair sequence.

        This is a material advance over the earlier catalog-only relationship: the Taiwan witness itself, not a modern OCR layer, directly identifies `唐明皇論` as part of its 《四字經》 contents. The 1597 Yimen witness physically uses the same heading over the opening prose unit.

        ## 3. Pages 3–4: public derivative skips from catalogue end to 甲甲 body

        Page 3 (`{PAGE_HASHES['p03']}`) directly reads:

        ```text
        四字經目錄終
        ```

        The very next public PDF page, page 4 (`{PAGE_HASHES['p04']}`), directly opens:

        ```text
        四字經
        甲甲
        ...
        甲乙
        ...
        ```

        No `唐明皇論` prose body is exposed between the catalogue ending and the visible `甲甲` body. Review of the remaining public pages continues the stem-pair material; page 21 (`{PAGE_HASHES['p21']}`) is already in `癸癸` material.

        The admissible conclusion is therefore **public-scan lacuna**, not physical-book absence:

        ```text
        TAIWAN_PUBLIC_21_PAGE_DERIVATIVE_DOES_NOT_EXPOSE_TANG_MINGHUANG_LUN_BODY_LEAF
        PHYSICAL_HOLDING_LACUNA_NOT_PROVED
        ```

        The missing unit could reflect digitization selection, a missing leaf in the digitized object, or another physical-history condition. This batch does not choose among those explanations.

        ## 4. Edition/transmission effect

        Taiwan 15275-0058 and the 1597 NLC/Yimen witness now have a stronger internal structural bridge:

        - both are titled 《四字經》;
        - the Taiwan physical scan's own TOC lists `唐明皇論` as the first internal unit;
        - the Yimen physical scan preserves `唐明皇論` as the prose heading before the stem-pair body.

        This strengthens common transmission/edition-family correspondence, but it still does **not** prove that the two objects are the same impression, that Taiwan 15275-0058 was disbound from a Yimen-Guangdu volume, or that every target glyph is identical.

        Because the Taiwan public derivative does not expose the `唐明皇論` body leaf, it contributes **zero** direct Taiwan glyph votes for `古人/古經`, `雨落/雨露`, or `亥子丑寅/子丑寅亥`.

        ## 5. Effect on HPA-ZDATE-006

        - `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`;
        - Taiwan public-scan direct target-body glyph witness increment: `0`;
        - Taiwan physical TOC `唐明皇論` structural witness: `+1`;
        - Hai-branch mechanical vote increment: `0`;
        - Fullbook cloudy/rain current-time acquisition mechanism closed: `false`;
        - runtime winner selected: `false`;
        - candidate collapsed: `false`;
        - algorithm reopen authorized: `false`.

        Global accounting remains `198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families`; provenance defects remain `11/11`; chart algorithm defect/reopen/collapse remain `0/0/0`.

        ## 6. Next gate

        1. Search for another first-party or derivative image route for Taiwan NCL 15275-0058 that exposes the omitted `唐明皇論` body leaf; do not infer its glyphs from the TOC.
        2. Directly collate the Yongle-Dadian target physical leaf for `古經/古人`, `雨露/雨落`, and hour ordering if an admissible image route is available.
        3. Continue the separate Fullbook-line operational-current-time question; neither the Taiwan TOC nor its public-scan lacuna supplies a clock-recovery method.

        Research record: `{RESEARCH_ARTIFACT}`.
        """
    )
    Path(BATCH_DOC).write_text(text, encoding="utf-8")


def write_research_artifact() -> None:
    data = {
        "schema": "ZIWEI-TAIWAN-NCL-SIZIJING-PUBLIC-SCAN-LACUNA-R1",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "prior_research": PRIOR_RESEARCH,
        "question": "Does Taiwan NCL 15275-0058 expose the Tang Minghuang Lun body leaf needed to compare the three Sizijing variant loci with the 1597 Yimen witness?",
        "source_ids": [SRC_CATALOG, SRC_SCAN],
        "evidence_chain": {
            "source_pdf": "NCL-15275-0058_四字經.pdf",
            "source_pdf_sha256": SOURCE_PDF_SHA256,
            "page_count": PAGE_COUNT,
            "renderer_head": EVIDENCE_HEAD,
            "renderer_tree": EVIDENCE_TREE,
            "workflow_run_id": WORKFLOW_RUN,
            "artifact_id": ARTIFACT_ID,
            "artifact_digest": ARTIFACT_DIGEST,
            "render_method": "pdftoppm JPEG render; final adjudication by direct visual review without OCR",
            "key_page_sha256": PAGE_HASHES,
        },
        "direct_collation": {
            "p01": {
                "heading": "四字經目錄",
                "first_internal_unit": "唐明皇論",
                "next_visible_toc_unit": "甲甲",
            },
            "p03": {"reading": "四字經目錄終"},
            "p04": {
                "visible_body_opening": ["四字經", "甲甲"],
                "tang_minghuang_lun_body_exposed_before_jiajia": False,
            },
            "p21": {"visible_material": "癸癸 stem-pair body"},
        },
        "scan_lacuna_adjudication": {
            "public_21_page_derivative_exposes_tang_minghuang_lun_body": False,
            "public_scan_lacuna_confirmed": True,
            "physical_holding_lacuna_proved": False,
            "allowed_explanations": [
                "digitization_selection_or_omission",
                "missing_leaf_in_digitized_object",
                "other_unresolved_physical_history",
            ],
            "do_not_infer_target_glyphs_from_toc": True,
        },
        "transmission_effect": {
            "taiwan_physical_toc_and_yimen_physical_heading_both_attest_tang_minghuang_lun": True,
            "same_transmission_family_correspondence_strengthened": True,
            "same_impression_proved": False,
            "taiwan_disbound_from_yimen_proved": False,
            "exact_target_glyph_identity_proved": False,
        },
        "effect": {
            "hpa_zdate_006_status": "MISSING_FROM_PRODUCT",
            "taiwan_public_scan_target_body_glyph_witness_increment": 0,
            "taiwan_physical_toc_tang_minghuang_lun_structural_witness_increment": 1,
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
    scan = next(s for s in data["sources"] if s.get("source_id") == SRC_SCAN)
    scan["batch_12bt_direct_public_scan_collation"] = {
        "source_pdf_sha256": SOURCE_PDF_SHA256,
        "page_count": PAGE_COUNT,
        "renderer_head": EVIDENCE_HEAD,
        "workflow_run_id": WORKFLOW_RUN,
        "artifact_id": ARTIFACT_ID,
        "key_page_sha256": PAGE_HASHES,
        "direct_no_ocr_findings": [
            "p01: 四字經目錄; first listed unit 唐明皇論; followed by 甲甲",
            "p03: 四字經目錄終",
            "p04: visible body opens 四字經 / 甲甲, with no exposed 唐明皇論 body leaf between TOC end and body start",
            "p21: visible stem-pair material has reached 癸癸",
        ],
        "classification": "PUBLIC_21_PAGE_DERIVATIVE_TARGET_BODY_LEAF_LACUNA; PHYSICAL_HOLDING_LACUNA_NOT_PROVED",
        "target_variant_glyph_authority": False,
    }
    note = (
        " Batch 12BT directly reviewed the full 21-page public PDF without OCR. Its own p1 TOC lists "
        "唐明皇論 before 甲甲; p3 reads 四字經目錄終; the next public page p4 begins 四字經 / 甲甲, "
        "and the remainder proceeds through the stem-pair body to 癸癸. The public derivative therefore "
        "does not expose the 唐明皇論 body leaf. This is a public-scan lacuna only; absence from the physical "
        "holding is not proved, and no target-variant glyphs may be inferred from the TOC."
    )
    if note.strip() not in scan.get("quality_notes", ""):
        scan["quality_notes"] = scan.get("quality_notes", "") + note

    cat = next(s for s in data["sources"] if s.get("source_id") == SRC_CATALOG)
    cat["batch_12bt_scan_crosscheck"] = {
        "public_scan_source_id": SRC_SCAN,
        "physical_toc_directly_attests_tang_minghuang_lun": True,
        "same_impression_with_yimen_proved": False,
        "disbound_identity_proved": False,
    }
    data["access_date"] = "2026-09-14"
    dump_json(path, data)


def update_matrix() -> None:
    path = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    row = next(r for r in data["rows"] if r.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12bt_taiwan_ncl_sizijing_public_scan_lacuna"] = {
        "source_ids": [SRC_CATALOG, SRC_SCAN],
        "source_pdf_sha256": SOURCE_PDF_SHA256,
        "workflow_run_id": WORKFLOW_RUN,
        "artifact_id": ARTIFACT_ID,
        "physical_toc_reading": "四字經目錄 -> 唐明皇論 -> 甲甲 ...",
        "public_scan_sequence": "p03 四字經目錄終 -> p04 四字經 / 甲甲; no exposed 唐明皇論 body leaf",
        "public_scan_target_body_leaf_exposed": False,
        "physical_holding_lacuna_proved": False,
        "transmission_effect": "TAIWAN_PHYSICAL_TOC_AND_YIMEN_PHYSICAL_BODY_SHARE_TANG_MINGHUANG_LUN_INTERNAL_UNIT; SAME_IMPRESSION/DISBOUND_IDENTITY_STILL_UNPROVED",
        "taiwan_target_variant_glyph_witness_increment": 0,
        "hai_branch_mechanical_vote_increment": 0,
        "candidate_status_effect": "NONE; HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT",
        "runtime_winner_selected": False,
        "algorithm_reopen_authorized": False,
        "research_artifact": RESEARCH_ARTIFACT,
    }
    dump_json(path, data)

    md_path = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md")
    md = md_path.read_text(encoding="utf-8")
    if "## Progress through Batch 12BT" not in md:
        md += dedent(
            """

            ## Progress through Batch 12BT

            - The complete 21-page Taiwan NCL 15275-0058 public 《四字經》 PDF derivative is now rendered and directly reviewed without OCR. Page 1's physical TOC lists `唐明皇論` before `甲甲`, independently strengthening the internal-unit bridge to the 1597 Yimen witness.
            - Page 3 directly reads `四字經目錄終`; the next public page 4 opens the visible body as `四字經 / 甲甲`, and the remaining pages continue the stem-pair body through `癸癸`. No `唐明皇論` prose body leaf is exposed in the 21-page public derivative.
            - The admissible finding is a public-scan target-leaf lacuna, not proof that the physical holding lacks the leaf. Taiwan contributes no direct glyph vote for `古人/古經`, `雨落/雨露`, or hour ordering from this derivative, and same-impression/disbound identity with the Yimen object remains unproved.
            - HPA-ZDATE-006 remains `MISSING_FROM_PRODUCT`; Hai-branch mechanical vote, runtime selection, candidate collapse and algorithm reopen remain unchanged. Next gate is another Taiwan image route or direct Yongle physical collation, while the Fullbook operational-current-time chain remains separate.
            """
        )
    md_path.write_text(md, encoding="utf-8")


def update_state() -> None:
    path = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    state = json.loads(path.read_text(encoding="utf-8"))
    state["schema_version"] = "1.79.0"
    audit = state["historical_audit"]
    if BATCH_ID not in audit["completed_batches"]:
        audit["completed_batches"].append(BATCH_ID)
    audit["latest_batch_doc"] = BATCH_DOC
    additions = [
        "Batch 12BT directly reviews the complete 21-page Taiwan NCL 15275-0058 public Sizijing PDF without OCR: p1 physical TOC lists 唐明皇論 before 甲甲, p3 reads 四字經目錄終, and the next public page p4 begins the visible body 四字經 / 甲甲; the remaining scan proceeds through stem-pair material to 癸癸.",
        "The Taiwan public derivative therefore does not expose the 唐明皇論 body leaf needed for the Batch-12BS variant loci. This is classified only as PUBLIC_SCAN_LACUNA; absence from the physical holding is not proved, and no Taiwan glyph reading for 古人/古經, 雨落/雨露 or hour ordering is inferred.",
        "Taiwan's physical TOC and the Yimen physical body now independently share the 唐明皇論 internal unit, strengthening common Sizijing transmission correspondence while still not proving same impression or disbound identity. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with Hai mechanical vote/runtime winner/candidate collapse/algorithm reopen unchanged; next gate is another Taiwan image route or direct Yongle target-leaf collation plus the separate Fullbook operational-time chain.",
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
