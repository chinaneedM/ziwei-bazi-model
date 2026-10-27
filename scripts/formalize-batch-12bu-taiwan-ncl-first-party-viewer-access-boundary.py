from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-TAIWAN-NCL-FIRST-PARTY-VIEWER-ACCESS-BOUNDARY-BU"
PREV_ID = "BATCH-12-ZIWEI-TAIWAN-NCL-SIZIJING-PUBLIC-SCAN-LACUNA-BT"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TAIWAN-NCL-FIRST-PARTY-VIEWER-ACCESS-BOUNDARY-BU.md"
RESEARCH_ARTIFACT = "docs/research/ZIWEI-TAIWAN-NCL-FIRST-PARTY-VIEWER-ACCESS-BOUNDARY-R1.json"
SRC_CATALOG = "EXT-TW-NCL-SIZIJING-15275-0058-MING-WANLI"
SRC_SCAN = "EXT-COMMONS-NCL-15275-0058-SIZIJING-SCAN"
SRC_RBOOK = "EXT-TW-NCL-RBOOK-SIZIJING-15275-0058-CURRENT-FIRST-PARTY"
PRIOR_RESEARCH = "docs/research/ZIWEI-TAIWAN-NCL-SIZIJING-PUBLIC-SCAN-LACUNA-R1.json"

EVIDENCE_HEAD = "3a78c8886d86db7b1904bcaaff4ee6b3c11d6457"
EVIDENCE_TREE = "367683b259f6fe8c935222040711b9dfdd54f996"
WORKFLOW_RUN = 34826374689
ARTIFACT_ID = 10340003938
ARTIFACT_DIGEST = "sha256:8f76217d9614eda5f291614cae43fa0b6d58dbe68e388ec2b6ccbceb6f57517a"
HASHES = {
    "catalog_html": "b1ae87e2742faa16e5df46dea2f4693a2fd5ecf5c4db96ef9e0d52d30a2619d2",
    "image_s1_html": "24512ba9983778f8cdad16c0ec944019cd0880dc7c4a18f6daf623f640f800d4",
    "image_blank_html": "e33d8e23c4db3da68de42eacd27ed2b7739570ff18479af0555948eac92569b8",
    "image_control_js": "fa9a91352d743357cf854b89f303454187825c3cfe6a3d337d5df57ca5b5dfb9",
    "puzzle_captcha_js": "f5a65376ac35efecbd2b1592ae61d7472298ddba2f5de4eddd0697cee638ad22",
}
RBOOK_URL = "https://rbook.ncl.edu.tw/NCLSearch/Search/SearchDetail?item=4f498ed65b97408aaf74cfcc1bec50abfDU0NDQ40.ug9YiJNB_UJXAc_XtEgviCIhdiQ0ZG3qjeyuaPAXm5Q_&page=&SourceID=1&HasImage="
VIEWER_PATH = "/NCLSearch/Search/SearchDetail?item=4f498ed65b97408aaf74cfcc1bec50abfDU0NDQ40.ug9YiJNB_UJXAc_XtEgviCIhdiQ0ZG3qjeyuaPAXm5Q_&image=1&page=&SourceID=1&HasImage="


def dump_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_continuity_verifier() -> None:
    path = Path("scripts/verify-project-continuity-state-r1.py")
    text = path.read_text(encoding="utf-8")
    if BATCH_ID not in text:
        needle = f'    "{PREV_ID}",\n]'
        replacement = f'    "{PREV_ID}",\n    "{BATCH_ID}",\n]'
        if needle not in text:
            raise SystemExit("cannot locate Batch 12BT tail in continuity verifier")
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
        # Fusion Chart Historical Provenance Audit R1 — Batch 12BU

        ## 臺灣國圖 15275-0058 第一方影像瀏覽路徑與人機驗證邊界

        Status: **CURRENT TAIWAN NCL FIRST-PARTY RBOOK RECORD DIRECTLY BOUND TO 四字經 / 15275-0058 / MING-WANLI JINLING JINGSHAN-SHULIN EDITION / RECORD EXPOSES AN IMAGE-VIEWER TARGET FOR THE SAME ITEM / IMAGE ENTRY IS GUARDED BY A PUZZLE CAPTCHA / DIRECT GET OF THE VIEWER URL WITHOUT SUCCESSFUL HUMAN VERIFICATION RETURNS THE DETAIL SURFACE, NOT IMAGEC PAGE LINKS / NO CAPTCHA BYPASS OR AUTOMATED SOLVING ATTEMPTED / FIRST-PARTY TARGET-LEAF IMAGE ACCESS REMAINS HUMAN-VERIFICATION-BOUNDARY / BATCH-12BT PUBLIC-SCAN LACUNA THEREFORE NOT YET CLOSED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI-BRANCH MECHANICAL VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

        ## 1. Scope

        Batch 12BT established that the 21-page Commons derivative of Taiwan NCL 15275-0058 omits the `唐明皇論` body leaf even though the physical TOC lists that unit. Batch 12BU tests the current first-party NCL `rbook.ncl.edu.tw` record and viewer contract without bypassing access controls.

        Exact probe chain:

        - first-party record: `{RBOOK_URL}`;
        - probe commit/tree: `{EVIDENCE_HEAD}` / `{EVIDENCE_TREE}`;
        - successful workflow run: `{WORKFLOW_RUN}`;
        - artifact: `{ARTIFACT_ID}`, digest `{ARTIFACT_DIGEST}`;
        - catalog HTML SHA-256: `{HASHES['catalog_html']}`;
        - direct image=1 / SourceID=1 HTML SHA-256: `{HASHES['image_s1_html']}`;
        - direct image=1 / blank-SourceID HTML SHA-256: `{HASHES['image_blank_html']}`.

        ## 2. Current first-party record and viewer binding

        The first-party detail HTML directly binds:

        - title `四字經`;
        - book/accession number `15275-0058`;
        - source `古籍影像檢索資料庫`;
        - owner `國家圖書館`;
        - a thumbnail route under `/NCLSearch/WaterMark/GetMinImage?...`;
        - hidden viewer target `{VIEWER_PATH}`.

        The viewer link does not navigate immediately. Its click handler opens a puzzle-captcha modal. The official page initializes the challenge with:

        ```text
        /NCLSearch/Users/GenerateCaptcha
        /NCLSearch/Users/VerifyCaptcha
        ```

        Only the configured success callback navigates to the hidden viewer URL.

        ## 3. No access-control bypass

        Direct unauthenticated HTTP GETs to the image=1 URL returned HTTP 200, but the returned HTML contains no `.ImageC` page entries and no exposed target-page image list. The downloaded first-party `imageControl.js` shows that an admitted viewer would normally enumerate `.ImageC` page links and request per-image watermark tokens through `../Watermark/getToken`; those admitted-viewer structures were not present in the direct GET response.

        The captcha JavaScript explicitly implements interactive puzzle movement/rotation and verification. This research batch does **not** call the verification endpoint with fabricated solutions, infer challenge answers, replay another session, or otherwise bypass the human-verification gate.

        Therefore the current result is an access boundary, not a negative holding result:

        ```text
        FIRST_PARTY_VIEWER_ROUTE_EXISTS
        HUMAN_PUZZLE_VERIFICATION_REQUIRED_BEFORE_IMAGE_ENUMERATION
        TARGET_BODY_LEAF_PRESENCE_IN_FIRST_PARTY_VIEWER = UNRESOLVED
        ```

        ## 4. Effect on Batch 12BT and HPA-ZDATE-006

        The current first-party record strengthens object identity and proves that NCL advertises an image-browse path for this exact holding. It does not yet reveal whether that viewer contains additional pages omitted from the 21-page Commons derivative.

        Consequently:

        - Batch 12BT `PUBLIC_SCAN_LACUNA` remains valid;
        - first-party target body leaf presence remains `UNRESOLVED_AT_HUMAN_VERIFICATION_BOUNDARY`;
        - Taiwan direct target-variant glyph increment remains `0`;
        - `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`;
        - Hai-branch mechanical vote increment: `0`;
        - runtime winner selected: `false`;
        - candidate collapsed: `false`;
        - algorithm reopen authorized: `false`.

        Global accounting remains `198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families`; provenance defects remain `11/11`; chart algorithm defect/reopen/collapse remain `0/0/0`.

        ## 5. Next gate

        1. Continue research without bypassing the NCL captcha: seek another lawful first-party/derivative route that exposes the omitted Taiwan target leaf.
        2. In parallel, directly locate/collate a physical or facsimile Yongle-Dadian target leaf for the `古經/古人`, `雨露/雨落`, and hour-order loci.
        3. Only if these public routes are exhausted and the Taiwan target leaf remains uniquely valuable should a human-operated NCL viewer session be requested as an explicit external-interaction step.

        Research record: `{RESEARCH_ARTIFACT}`.
        """
    )
    Path(BATCH_DOC).write_text(text, encoding="utf-8")


def write_research_artifact() -> None:
    data = {
        "schema": "ZIWEI-TAIWAN-NCL-FIRST-PARTY-VIEWER-ACCESS-BOUNDARY-R1",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "prior_research": PRIOR_RESEARCH,
        "question": "Can the current first-party Taiwan NCL viewer expose the Tang Minghuang Lun target body leaf without crossing a human-verification access boundary?",
        "source_id": SRC_RBOOK,
        "evidence_chain": {
            "record_url": RBOOK_URL,
            "probe_head": EVIDENCE_HEAD,
            "probe_tree": EVIDENCE_TREE,
            "workflow_run_id": WORKFLOW_RUN,
            "artifact_id": ARTIFACT_ID,
            "artifact_digest": ARTIFACT_DIGEST,
            "sha256": HASHES,
        },
        "first_party_binding": {
            "title": "四字經",
            "identifier_bookno": "15275-0058",
            "source": "古籍影像檢索資料庫",
            "rights_owner": "國家圖書館",
            "viewer_path": VIEWER_PATH,
            "thumbnail_route_present": True,
        },
        "access_contract": {
            "viewer_click_opens_puzzle_captcha": True,
            "generate_endpoint": "/NCLSearch/Users/GenerateCaptcha",
            "verify_endpoint": "/NCLSearch/Users/VerifyCaptcha",
            "viewer_navigation_only_on_success_callback": True,
            "direct_image_get_http_200": True,
            "direct_image_get_contains_imagec_page_entries": False,
            "admitted_viewer_js_expects_imagec_entries": True,
            "captcha_bypass_attempted": False,
            "automated_captcha_solving_attempted": False,
        },
        "effect": {
            "batch_12bt_public_scan_lacuna_reversed": False,
            "first_party_target_body_leaf_presence": "UNRESOLVED_AT_HUMAN_VERIFICATION_BOUNDARY",
            "taiwan_target_variant_glyph_witness_increment": 0,
            "hpa_zdate_006_status": "MISSING_FROM_PRODUCT",
            "hai_branch_mechanical_vote_increment": 0,
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
    if not any(s.get("source_id") == SRC_RBOOK for s in data["sources"]):
        data["sources"].append({
            "source_id": SRC_RBOOK,
            "title": "臺灣國家圖書館古籍與特藏文獻資源《四字經》15275-0058 current first-party record/viewer route",
            "historical_period": "明萬曆間刊本館藏 / current first-party digital access surface",
            "provider": "臺灣國家圖書館",
            "url": RBOOK_URL,
            "source_role": "CURRENT_FIRST_PARTY_OBJECT_BINDING_AND_IMAGE_VIEWER_ACCESS_CONTRACT_FOR_NCL_15275_0058",
            "quality_notes": "Direct Batch 12BU probe binds the exact object and viewer target, but image enumeration is gated by an interactive puzzle captcha. No bypass was attempted. This source is access/provenance evidence until the target body leaf is directly viewed.",
        })
    src = next(s for s in data["sources"] if s.get("source_id") == SRC_RBOOK)
    src["batch_12bu_probe"] = {
        "probe_head": EVIDENCE_HEAD,
        "workflow_run_id": WORKFLOW_RUN,
        "artifact_id": ARTIFACT_ID,
        "artifact_digest": ARTIFACT_DIGEST,
        "sha256": HASHES,
        "viewer_path": VIEWER_PATH,
        "puzzle_captcha_generate": "/NCLSearch/Users/GenerateCaptcha",
        "puzzle_captcha_verify": "/NCLSearch/Users/VerifyCaptcha",
        "direct_get_imagec_entry_count": 0,
        "target_leaf_presence": "UNRESOLVED_AT_HUMAN_VERIFICATION_BOUNDARY",
        "captcha_bypass_attempted": False,
    }
    cat = next(s for s in data["sources"] if s.get("source_id") == SRC_CATALOG)
    cat["batch_12bu_current_first_party_crosswalk"] = SRC_RBOOK
    scan = next(s for s in data["sources"] if s.get("source_id") == SRC_SCAN)
    scan["batch_12bu_first_party_viewer_comparison"] = {
        "first_party_source_id": SRC_RBOOK,
        "commons_public_scan_lacuna_reversed": False,
        "first_party_has_advertised_viewer_route": True,
        "first_party_target_leaf_presence": "UNRESOLVED_AT_HUMAN_VERIFICATION_BOUNDARY",
    }
    data["access_date"] = "2026-09-14"
    dump_json(path, data)


def update_matrix() -> None:
    path = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    row = next(r for r in data["rows"] if r.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12bu_taiwan_ncl_first_party_viewer_access_boundary"] = {
        "source_id": SRC_RBOOK,
        "workflow_run_id": WORKFLOW_RUN,
        "artifact_id": ARTIFACT_ID,
        "first_party_object_binding": "四字經 / 15275-0058 / 國家圖書館",
        "viewer_route_present": True,
        "interactive_puzzle_captcha_required": True,
        "direct_viewer_get_exposed_imagec_entries": False,
        "target_body_leaf_presence": "UNRESOLVED_AT_HUMAN_VERIFICATION_BOUNDARY",
        "captcha_bypass_attempted": False,
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
    if "## Progress through Batch 12BU" not in md:
        md += dedent(
            """

            ## Progress through Batch 12BU

            - The current Taiwan NCL first-party `rbook.ncl.edu.tw` record is directly rebound to 《四字經》 / 15275-0058 and advertises an image-viewer target for the same holding.
            - Entry to image enumeration is guarded by an interactive puzzle captcha. The official page only navigates to the hidden viewer URL on successful verification; direct image=1 GETs without that human-verification state return the detail surface and expose zero `.ImageC` page entries.
            - The admitted-viewer JavaScript expects `.ImageC` page links and per-image watermark tokens, but no captcha bypass, fabricated solution or session replay was attempted. Therefore first-party target-leaf presence is `UNRESOLVED_AT_HUMAN_VERIFICATION_BOUNDARY`, not a negative holding result.
            - Batch 12BT's public-scan lacuna remains intact. Taiwan contributes no new target-variant glyph vote; HPA-ZDATE-006 stays `MISSING_FROM_PRODUCT`, with Hai mechanical vote/runtime selection/candidate collapse/algorithm reopen unchanged.
            """
        )
    md_path.write_text(md, encoding="utf-8")


def update_state() -> None:
    path = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    state = json.loads(path.read_text(encoding="utf-8"))
    state["schema_version"] = "1.80.0"
    audit = state["historical_audit"]
    if BATCH_ID not in audit["completed_batches"]:
        audit["completed_batches"].append(BATCH_ID)
    audit["latest_batch_doc"] = BATCH_DOC
    additions = [
        "Batch 12BU binds the current Taiwan NCL first-party rbook record directly to 四字經 / 15275-0058 and its hidden image-viewer target. The page requires an interactive puzzle captcha before successful navigation into image enumeration.",
        "Direct image=1 GETs without successful human verification return HTTP 200 detail surfaces but expose zero ImageC page entries. The viewer JavaScript would enumerate ImageC links and watermark tokens only after admission; no captcha bypass, fabricated solution or session replay was attempted, so target-body-leaf presence is UNRESOLVED_AT_HUMAN_VERIFICATION_BOUNDARY rather than absent.",
        "Batch 12BT PUBLIC_SCAN_LACUNA remains valid and Taiwan adds no target-variant glyph vote. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT with Hai mechanical vote/runtime winner/candidate collapse/algorithm reopen unchanged; research now proceeds to lawful alternate Taiwan routes and direct Yongle-Dadian physical collation before requesting any human-operated viewer step.",
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
