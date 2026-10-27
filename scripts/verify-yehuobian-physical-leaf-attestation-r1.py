#!/usr/bin/env python3
"""Scope-only, fail-closed admission contract for 12SM Tokyo physical leaf queue.

This verifies declared record structure. It never verifies a historical
glyph, physical copy authenticity, or that a remote scan was legally viewed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "docs/research/MING-DATONG-YEHUOBIAN-12SM-TOKYO-TARGET-LEAF-ATTESTATION-QUEUE-R1.json"
SCHEMA = "MING-DATONG-YEHUOBIAN-12SM-TARGET-LEAF-QUEUE-R1"
LOCI = {"WINTER_BEIJING_SUNRISE", "SUMMER_BEIJING_SUNSET", "PRECINCT_TERM", "CLOCK_TERM"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")

def file_sha256(artifact_root: Path | None, relative_path: str) -> str:
    """Verify actual captured bytes, never a self-asserted digest alone."""
    if artifact_root is None:
        raise ValueError("positive original leaf requires actual artifact root and bytes")
    if (not isinstance(relative_path, str) or not relative_path
        or "\\" in relative_path or Path(relative_path).is_absolute()
        or any(p in ("", ".", "..") for p in relative_path.split("/"))):
        raise ValueError("unsafe source/page artifact path")
    root = Path(artifact_root).resolve(strict=True)
    file = (root / relative_path).resolve(strict=True)
    if not file.is_relative_to(root) or not file.is_file():
        raise ValueError("artifact path escapes root or not a file")
    result = hashlib.sha256()
    with file.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def verify(record: dict, artifact_root: Path | None = None) -> dict:
    if record.get("schema") != SCHEMA or set(record.get("required_loci", [])) != LOCI:
        raise ValueError("wrong leaf-queue schema or collation locus set")
    if record.get("target_article") != "改造漏刻":
        raise ValueError("unexpected target article")
    entries = record.get("entries")
    if not isinstance(entries, list) or len(entries) != 2:
        raise ValueError("two known distinct Tokyo catalog objects required")
    expected = {("BC0492354X", "6403767830", 1827), ("BB23196128", "6403148395", 1869)}
    if {(e.get("ncid"), e.get("physical_item"), e.get("cataloged_year")) for e in entries} != expected:
        raise ValueError("Tokyo NCID, item number or cataloged print layer changed")
    votes = 0
    positive_source_hashes = set()
    positive_page_hashes = set()
    for item in entries:
        if item.get("digital_access") not in {"NOT_VERIFIED", "ITEM_ORIGINAL_LEAF_VERIFIED"}:
            raise ValueError("unrecognized image access state")
        collated = item.get("collated_loci")
        if not isinstance(collated, dict):
            raise ValueError("loci must be explicit mapping, even when empty")
        leaf = item.get("original_target_leaf")
        vote = item.get("independent_target_glyph_vote")
        if leaf is None:
            if (item["digital_access"] != "NOT_VERIFIED" or
                item.get("copy_image_identity_bound") is not False or collated or vote != 0):
                raise ValueError("unverified target leaf cannot attest a digit or a copy")
            continue
        if (item["digital_access"] != "ITEM_ORIGINAL_LEAF_VERIFIED"
            or item.get("copy_image_identity_bound") is not True or vote != 1):
            raise ValueError("target leaf needs explicit image and physical identity verification")
        if not isinstance(leaf, dict) or not isinstance(leaf.get("source_url"), str) or not leaf["source_url"].startswith("https://"):
            raise ValueError("target leaf requires first-party/source image URL")
        if not (isinstance(leaf.get("page"), int) and leaf["page"] > 0):
            raise ValueError("target leaf needs original page locator")
        if not all(isinstance(leaf.get(k), str) and SHA256.fullmatch(leaf[k]) for k in ("source_sha256","page_sha256")):
            raise ValueError("target leaf requires sha256 source and page digests")
        if set(collated) != LOCI or any(not isinstance(v,str) or not v.strip() for v in collated.values()):
            raise ValueError("four individually collated word/number loci required")
        if (not isinstance(leaf.get("human_reviewer"), str) or
            not leaf["human_reviewer"].strip() or
            not isinstance(leaf.get("edition_control"), str) or not leaf["edition_control"].strip()):
            raise ValueError("direct source leaf needs independent human/edition controls")
        for claimed_hash, path_key in (("source_sha256", "source_local_file"),
                                       ("page_sha256", "page_local_file")):
            local = leaf.get(path_key)
            actual = file_sha256(artifact_root, local)
            if actual != leaf[claimed_hash]:
                raise ValueError("actual file bytes sha256 mismatch for " + path_key)
        if (leaf["source_sha256"] in positive_source_hashes
                or leaf["page_sha256"] in positive_page_hashes):
            raise ValueError("same digitized bytes cannot cast independent copy votes")
        positive_source_hashes.add(leaf["source_sha256"])
        positive_page_hashes.add(leaf["page_sha256"])
        votes += 1
    if record.get("independent_target_glyph_votes") != votes:
        raise ValueError("aggregate vote count does not match independently admitted targets")
    return {"status":"PASS","catalog_items":len(entries),"admitted_target_glyph_votes":votes}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", type=Path,
                        help="local authorized source PDF and page-image directory; mandatory for positive votes")
    args = parser.parse_args()
    try:
        print(json.dumps(verify(json.loads(QUEUE.read_text(encoding="utf-8")), args.artifact_root),sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as err:
        print(json.dumps({"status":"FAIL","reason":str(err)},ensure_ascii=False))
        return 1

if __name__ == "__main__":
    sys.exit(main())
