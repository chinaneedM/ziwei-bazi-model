#!/usr/bin/env python3
"""Replay the recovered journal bytes without promoting them to ancient-copy evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOC = "docs/research/TIANWEN-13IS-SYSU-PDF-BYTES-AND-GK3467-FRONT-ACCESS-R1.json"
PDF_SHA = "3fc3408cc07e62f48556c95634b2858da76cc68bcbd2ac33c4dce73aef7ed1d2"


def read(path=DOC):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def check(e, *, state=None, ledger=None):
    assert e["schema"] == "TIANWEN-13IS-SYSU-PDF-BYTES-AND-GK3467-FRONT-ACCESS-R1"
    assert e["issue_id"] == "TW-OPEN-0005"
    p = e["journal_byte_recovery"]
    assert p["raw_pdf_sha256"] == PDF_SHA and p["raw_pdf_bytes"] == 433784
    assert p["status"] == 200 and p["content_type"] == "application/pdf"
    assert p["pages"] == 12 and p["pdf_magic_verified"] and p["same_hash_successful_gets"] == 2
    old = read(e["immutable_predecessors"][0]["path"])
    assert p["url"] == old["journal_original"]["direct_url"]
    assert old["journal_original"]["raw_pdf_bytes_sha256"] is None
    assert old["journal_original"]["hosted_pdf_file_byte_hash_not_yet_verified"] is True
    for item in e["immutable_predecessors"]:
        raw = (ROOT / item["path"]).read_bytes()
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == item["git_blob_sha"]
    page = e["page100_replay"]
    assert (page["page_index"], page["printed_page"]) == (7, 100)
    assert page["woodblock_supplement_volumes"] == [19,20,21,31,73,74,77,78,79,81,82,83]
    assert page["unused_alternate_eulhae_volumes"] == [31,77,78,79,81,82]
    assert page["unembedded_font_xrefs"] == [6,77]
    assert page["original_CJK_glyphs_exhaustively_verified"] is False
    assert page["text_extraction_is_not_original_glyph_shape"] is True
    assert page["content_streams"] == [
        {"xref":39,"raw_bytes":8344,"sha256":"fb1eb96cb03c09993b1608e7d452edbe345bc23dfb1413465d7e9a2cf17e1370"},
        {"xref":40,"raw_bytes":20352,"sha256":"c803872bd52f4f13158556fca7717ec754769f042696ddf2958de5d8941a5efe"},
    ]
    access = e["gk3467_front_retry"]
    assert access["selected_provider_listed_pages"] == ["000a","000b","001a"]
    assert access["statuses"] == [503,503,503] and access["new_original_images"] == 0
    assert access["seed_renderer_sha256"] == "d18eda904b621ffa309ee6ec299d43714c3346f9561d831b251ad1a8e5e25f3d"
    assert hashlib.sha256((ROOT/access["response_file"]).read_bytes()).hexdigest() == access["response_sha256"]
    assert access["response_sha256"] == "33fbc61ad080ef68dd7a6479f8c53f1bf864dba2930567dbbc4ceb47490a1909"
    assert not access["physical_leaf_loss_proven"] and not access["target_page_absence_proven"]
    scope = e["scope"]
    for key in ("GK3467_table_start_recovered","GK5553_book29_to_juan81_83_bound","G893_six_adjudicated","ancient_glyph_decisions_added"):
        assert scope[key] is False
    assert scope["GK5553_13IO_status"] == "RETRACTED_UNBOUND"
    assert e["counts"] == {"matrix":[222,222],"sources":761,"graph":[252,238],"open_issues":11,"chart":"CLOSED","algorithm_reopens":0,"candidate_collapses":0}
    assert e["transmission_impact"]["edges_supported"] == []
    s = state if state is not None else read("docs/PROJECT-CURRENT-STATE-R1.json")
    l = ledger if ledger is not None else read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
    assert s["schema_version"] == l["binding"]["reviewed_state_version"] == s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert tuple(map(int,s["schema_version"].split("."))) >= (1,898,0)
    focus = s["historical_audit"]["current_focus"]
    assert any(x.startswith("13IS ") for x in focus)
    assert len(focus) == l["binding"]["source_focus_count"]
    assert focus[-1].split(" ",1)[0] == l["binding"]["latest_research_focus_prefix"]
    issue = next(i for i in l["issues"] if i["id"] == "TW-OPEN-0005")
    assert issue["priority"] == "P0" and issue["status"] == "OPEN"
    assert DOC in issue["source_refs"]
    assert any(h.get("event") == "ISSUE_REVISION" and h.get("revision_id","").startswith("TW-OPEN-0005-13IS-") and DOC in h.get("evidence_refs",[]) and "next_action" in h.get("changed_fields",[]) for h in issue["history"])
    return True


def replay_pdf(path, evidence):
    raw = Path(path).read_bytes()
    assert raw.startswith(b"%PDF-") and len(raw) == evidence["journal_byte_recovery"]["raw_pdf_bytes"]
    assert hashlib.sha256(raw).hexdigest() == PDF_SHA
    import fitz
    with fitz.open(stream=raw, filetype="pdf") as doc:
        assert len(doc) == 12
        page = doc[7]
        for stream in evidence["page100_replay"]["content_streams"]:
            assert stream["xref"] in page.get_contents()
            data = doc.xref_stream_raw(stream["xref"])
            assert len(data) == stream["raw_bytes"] and hashlib.sha256(data).hexdigest() == stream["sha256"]
        absent = sorted(x[0] for x in page.get_fonts(full=True) if not doc.extract_font(x[0])[3])
        assert absent == [6,77]
        text = re.sub(r"\s+", "", page.get_text())
        numbers = lambda pattern: [int(n) for n in re.findall(r"\d+", re.search(pattern,text).group(1))]
        assert numbers(r"其中卷([\d，,]+)由") == evidence["page100_replay"]["woodblock_supplement_volumes"]
        assert numbers(r"导致卷([\d、,]+)可以") == evidence["page100_replay"]["unused_alternate_eulhae_volumes"]
        assert "选用了奎5554" in text and "未选用奎5553" in text
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, help="Optional independently downloaded firstparty PDF")
    args = parser.parse_args()
    e = read()
    assert check(e)
    if args.pdf:
        assert replay_pdf(args.pdf,e)
    print("TIANWEN_13IS_PDF_BYTES_AND_ORIGINAL_SCOPE_PASS")
