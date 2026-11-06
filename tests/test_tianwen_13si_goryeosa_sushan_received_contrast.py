import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/research/TIANWEN-13SI-GORYEOSA-SUSHAN-RECEIVED-EDITORIAL-LAYER-COLLATION-R1.json"
SHARD = ROOT / "docs/research/TIANWEN-13SI-GORYEOSA-SUSHAN-RECEIVED-EDITORIAL-SOURCE-SHARD-R1.json"

def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_13si_distinct_received_readings_not_normalized():
    d = _load(DOC)
    assert d["collation"]["lexical_pair"]["goryeosa"] == "非當時所用"
    assert d["collation"]["lexical_pair"]["sushan"] == "非今時所用"
    assert d["collation"]["lexical_pair"]["status"] == "RECEIVED_TEXT_VARIANT_NOT_PHYSICALLY_ADJUDICATED"
    assert "作曆志" in d["collation"]["divergence_at_end"]["goryeosa"]
    assert "嗚呼" in d["collation"]["divergence_at_end"]["sushan"]

def test_13si_original_and_numeric_firewall():
    d = _load(DOC)
    e = d["evidence_gate"]
    for key in ("new_physically_authenticated_original_folios", "new_same_field_solar_short_digits",
                "new_period_same_field_shao_wei_carry_rules", "independent_original_votes",
                "transmission_edges_established", "algorithm_reopens", "candidate_collapses",
                "omitted_risk_issues_closed"):
        assert e[key] == 0
    assert e["six_historical_numeric_finals"] == "0/6"
    assert e["chart_product"] == "CLOSED"
    assert d["source_loci"]["sushan_parallel_site"]["physical_leaf"] is None

def test_13si_source_registry_identity_not_duplicate_voting():
    d, s = _load(DOC), _load(SHARD)
    assert len(s["sources"]) == d["evidence_gate"]["source_registry_new_entries"] == 2
    ids = [x["source_id"] for x in s["sources"]]
    assert len(set(ids)) == len(ids)
    assert all(x["physical_glyph_authority"] is False for x in s["sources"])
    assert all(x["evidence"] == "docs/research/TIANWEN-13SI-GORYEOSA-SUSHAN-RECEIVED-EDITORIAL-LAYER-COLLATION-R1.json" for x in s["sources"])
