#!/usr/bin/env python3
"""Fail-closed copy-condition gate: Tokyo Yuran catalogue is not a juan20 glyph witness."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = "docs/research/MING-DATONG-YEHUOBIAN-12UT-TOKYO-YURAN-DAMAGED-COPY-GATE-R1.json"
REGISTRY = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
BASE = "docs/research/MING-DATONG-YEHUOBIAN-12UK-ORIGINAL-LEAF-INTAKE-QUEUE-R1.json"
EXTRA = "docs/research/MING-DATONG-YEHUOBIAN-12UN-ADDITIONAL-1827-PHYSICAL-COPY-BACKLOG-R1.json"
LOCI = {"GONGJIN", "CLOCK_NOUN", "BEIJING_WINTER_SUNRISE", "BEIJING_SUMMER_SUNSET"}

def validate(d, registry, base, extra):
    if d.get("schema") != "TIANWEN-12UT-TOKYO-YURAN-DAMAGED-COPY-SCOPE-FIREWALL-R1":
        raise ValueError("schema")
    p, a, f = d["physical_copy"], d["institutional_access"], d["scope_firewall"]
    if p.get("ncid") != "BC08398372" or p.get("source_issued_identifier") != "夕嵐草堂:S2024:3 6411758714" or p.get("binding") != "卷19-20":
        raise ValueError("exact source item binding")
    rows = [s for s in registry["sources"] if s.get("source_id") == p.get("registry_id")]
    if len(rows) != 1 or rows[0].get("url") != p.get("catalog_url"):
        raise ValueError("source registry / source-issued catalog mismatch")
    if p.get("lacuna_scope_volume") != "19" or "卷19第30葉以降落丁" != p.get("lacuna_scope"):
        raise ValueError("catalogued lacuna cannot be broadened")
    if p.get("volume20_target_folio_absence_proven") is not False or a.get("physical_original_missing_in_volume20") is not False:
        raise ValueError("juan19 damage cannot prove juan20 original missing")
    if p.get("catalogued_condition") != "虫損甚だし(劣化につき利用不可)" or a.get("access_priority") != "LOW_CONDITIONAL_CATALOG_UNAVAILABLE":
        raise ValueError("do not promote inaccessible item without new evidence")
    if p.get("physical_copy_original_printing_state") != "UNVERIFIED":
        raise ValueError("catalog date does not prove impression")
    if set(p.get("four_locus_readings", {})) != LOCI or any(v is not None for v in p["four_locus_readings"].values()):
        raise ValueError("no unobserved original target glyphs")
    if any(p.get(k) is not None for k in ("original_image_url", "original_binary_sha256", "original_page_sha256", "target_original_folio")):
        raise ValueError("no original leaf capture")
    if a.get("library_portal") != "https://www.ioc.u-tokyo.ac.jp/~library/" or a.get("published_copy_rules") != "https://www.ioc.u-tokyo.ac.jp/~library/guide/copy.html":
        raise ValueError("do not transfer other library policies to IOC")
    if not a.get("institutional_confirmation_required") or a.get("image_alternative_identified") or a.get("individualized_permission_granted") or a.get("application_submitted") or a.get("fees_confirmed"):
        raise ValueError("catalog/general policy is not item authorization")
    names = [c["id"] for c in base["candidates"]] + [c["id"] for c in extra["candidates"]]
    if len(names) != 8 or len(names) != len(set(names)):
        raise ValueError("unexpected predecessor image queue")
    if "TOKYO_YURAN_1827_6411758714" in names:
        raise ValueError("inaccessible item silently promoted into actionable queue")
    competitors = d.get("priority_comparators", [])
    if {c.get("item") for c in competitors} != {"6403767830", "6403148395"}:
        raise ValueError("wrong alternative Tokyo original copy identities")
    for k in ("catalog_unavailable_is_permanent_loss", "chapter_target_lacuna_inferred_from_volume19",
              "general_copy_policy_is_item_copy_authorization", "two_catalog_items_are_proved_different_plates",
              "old_chronological_20_same_as_thematic_20", "source_original_folio_acquired", "algorithm_reopen_authorized"):
        if f.get(k) is not False:
            raise ValueError("unsafe inference: " + k)
    if f.get("historical_vote_authority") != "NONE" or any(f.get(k) != 0 for k in ("glyph_votes", "new_external_sources", "graph_nodes_added", "graph_edges_added")):
        raise ValueError("catalog-only metadata cannot change historical evidence counts")
    return {"status": "PASS", "catalogued_damaged_items": 1, "actionable_predecessor_queue": 8,
            "image_captures": 0, "original_juan20_glyph_votes": 0}

def verify(root=ROOT):
    def load(path):
        return json.loads((root / path).read_text(encoding="utf-8"))
    return validate(load(DATA), load(REGISTRY), load(BASE), load(EXTRA))

if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, sort_keys=True))
