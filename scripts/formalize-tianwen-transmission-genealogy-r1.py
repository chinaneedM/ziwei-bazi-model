from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
CONTINUITY = ROOT / "docs/PROJECT-CONTINUITY-PROTOCOL-R1.md"
MAIN_VERIFIER = ROOT / "scripts/verify-project-continuity-state-r1.py"
CHARTER = "docs/TIANWEN-SYSTEM-CHARTER-R1.md"
GENEALOGY_PROTOCOL = "docs/TRANSMISSION-GENEALOGY-PROTOCOL-R1.md"
GENEALOGY_GRAPH = "docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json"


def dump(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_state() -> None:
    d = json.loads(STATE.read_text(encoding="utf-8"))
    d["tianwen_identity"] = {
        "umbrella_name_zh": "天问",
        "umbrella_name_en": "TIANWEN",
        "working_motto": "天以命运问人，人以命理问天。",
        "system_charter": CHARTER,
        "transmission_genealogy_protocol": GENEALOGY_PROTOCOL,
        "transmission_genealogy_graph": GENEALOGY_GRAPH,
        "transmission_genealogy_status": "ACTIVE_INCREMENTAL",
        "historical_backfill_status": "INCREMENTAL",
        "future_material_historical_batches_require_transmission_impact": True,
        "prediction_model_status": "FUTURE_NOT_CURRENT_SCOPE"
    }

    bootstrap = d.get("new_chat_bootstrap_order", [])
    wanted_after_authority = [
        "read docs/TIANWEN-SYSTEM-CHARTER-R1.md",
        "read docs/TRANSMISSION-GENEALOGY-PROTOCOL-R1.md",
    ]
    wanted_after_registry = ["read docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json"]
    bootstrap = [x for x in bootstrap if x not in wanted_after_authority + wanted_after_registry]

    try:
        authority_i = bootstrap.index("read docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md")
    except ValueError as exc:
        raise SystemExit("current-state bootstrap authority anchor missing") from exc
    for offset, item in enumerate(wanted_after_authority, start=1):
        bootstrap.insert(authority_i + offset, item)

    try:
        registry_i = bootstrap.index("read external historical source registry")
    except ValueError as exc:
        raise SystemExit("current-state bootstrap registry anchor missing") from exc
    for offset, item in enumerate(wanted_after_registry, start=1):
        bootstrap.insert(registry_i + offset, item)
    d["new_chat_bootstrap_order"] = bootstrap

    focus = d["historical_audit"]["current_focus"]
    additions = [
        "Tianwen (天问) is now the project umbrella identity. The deterministic chart product, historical provenance/philology, and transmission genealogy are separate layers; future empirical/prediction work remains outside the current stage.",
        "Transmission Genealogy R1 is ACTIVE_INCREMENTAL. Future materially historical batches should emit transmission_impact; existing batches will be backfilled incrementally rather than rewritten in one pass.",
        "Transmission genealogy is modeled as an evidence-scoped graph, not a forced lineage tree. Work composition date, edition/impression date, physical-copy date and digital-surrogate date must remain separate when material.",
        "Batch 12CH is the first explicit graph seed: 1447 Nanjing 59-ke standard and 1455 Tongshu Xiazhi 60/40 are confirmed as parallel-coexisting layers; both remain only candidate components in the unresolved 1578 Sanming composite ancestry."
    ]
    for item in additions:
        if item not in focus:
            focus.append(item)

    d["schema_version"] = "1.94.0"
    d["updated_at"] = "2026-09-15"
    dump(STATE, d)


def update_continuity_protocol() -> None:
    s = CONTINUITY.read_text(encoding="utf-8")
    old = """6. Read `docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md`.\n7. Read the historical provenance Matrix JSON/MD and external source registry.\n8. Read the latest batch document named by the current-state JSON.\n9. Check recent commits for any batch/state changes newer than that document.\n10. Only then open the source/tests/docs needed for the next rule family.\n"""
    new = """6. Read `docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md`.\n7. Read `docs/TIANWEN-SYSTEM-CHARTER-R1.md`.\n8. Read `docs/TRANSMISSION-GENEALOGY-PROTOCOL-R1.md`.\n9. Read the historical provenance Matrix JSON/MD and external source registry.\n10. Read `docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json`.\n11. Read the latest batch document named by the current-state JSON.\n12. Check recent commits for any batch/state changes newer than that document.\n13. Only then open the source/tests/docs needed for the next rule family.\n"""
    if old in s:
        s = s.replace(old, new, 1)
    elif "docs/TIANWEN-SYSTEM-CHARTER-R1.md" not in s:
        raise SystemExit("continuity startup sequence anchor changed unexpectedly")

    section_marker = "## Tianwen transmission-genealogy continuity rule"
    if section_marker not in s:
        anchor = "## No self-referential HEAD in the handoff\n"
        if anchor not in s:
            raise SystemExit("continuity section insertion anchor missing")
        section = """## Tianwen transmission-genealogy continuity rule\n\nThe project umbrella identity is `天问 / TIANWEN`. Every new historical-research session must preserve the separate layers defined by `docs/TIANWEN-SYSTEM-CHARTER-R1.md`:\n\n```text\ndeterministic charting != historical provenance/philology != transmission genealogy != future empirical/prediction work\n```\n\nTransmission genealogy is an evidence-scoped graph, not a presumed single lineage tree. When a research batch materially changes historical lineage, it should record a `transmission_impact` containing nodes, supported/revised/rejected edges and remaining lineage questions. Existing batches are backfilled incrementally.\n\nThe following scope firewall is mandatory:\n\n```text\nwork composition date != edition/impression date != physical-copy date != digital-surrogate date\nsame wording != proven direct copying\nsame numeric pair != proven same table\nsame title != proven same edition/copy\nparallel coexistence != proven lineage\n```\n\nGraph revisions are forward-only. New evidence may strengthen, weaken or disprove a lineage edge, but the earlier status and revision reason must remain auditable. A genealogy revision never automatically reopens a deterministic chart algorithm and never activates prediction/AI interpretation.\n\nMachine graph: `docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json`.\n\n"""
        s = s.replace(anchor, section + anchor, 1)

    invariant_line = "TIANWEN_TRANSMISSION_GENEALOGY_R1=ACTIVE_INCREMENTAL"
    if invariant_line not in s:
        needle = "PREDICTION_AI_INTERPRETATION=CURRENTLY_OUT_OF_SCOPE\n"
        if needle not in s:
            raise SystemExit("continuity invariant insertion anchor missing")
        s = s.replace(needle, needle + invariant_line + "\n", 1)

    CONTINUITY.write_text(s, encoding="utf-8")


def update_main_verifier() -> None:
    s = MAIN_VERIFIER.read_text(encoding="utf-8")
    constant_marker = 'TIANWEN_CHARTER = ROOT / "docs/TIANWEN-SYSTEM-CHARTER-R1.md"'
    if constant_marker not in s:
        anchor = 'AUTHORITY = ROOT / "docs" / "FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md"\n'
        if anchor not in s:
            raise SystemExit("main verifier authority constant anchor missing")
        addition = (
            'TIANWEN_CHARTER = ROOT / "docs/TIANWEN-SYSTEM-CHARTER-R1.md"\n'
            'TRANSMISSION_PROTOCOL = ROOT / "docs/TRANSMISSION-GENEALOGY-PROTOCOL-R1.md"\n'
            'TRANSMISSION_GRAPH = ROOT / "docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json"\n'
            'TIANWEN_VERIFIER = ROOT / "scripts/verify-tianwen-transmission-genealogy-r1.py"\n'
        )
        s = s.replace(anchor, anchor + addition, 1)

    check_marker = "# Tianwen / transmission-genealogy continuity gate."
    if check_marker not in s:
        anchor = "def main() -> int:\n"
        if anchor not in s:
            raise SystemExit("main verifier main() anchor missing")
        check = '''    # Tianwen / transmission-genealogy continuity gate.\n    for path in (TIANWEN_CHARTER, TRANSMISSION_PROTOCOL, TRANSMISSION_GRAPH, TIANWEN_VERIFIER):\n        if not path.is_file():\n            fail(f"Tianwen continuity artifact missing: {path.relative_to(ROOT)}")\n    tianwen_state = json.loads(STATE.read_text(encoding="utf-8"))\n    tianwen_identity = tianwen_state.get("tianwen_identity", {})\n    if tianwen_identity.get("umbrella_name_zh") != "天问" or tianwen_identity.get("umbrella_name_en") != "TIANWEN":\n        fail("Tianwen project identity missing from current state")\n    if tianwen_identity.get("transmission_genealogy_status") != "ACTIVE_INCREMENTAL":\n        fail("Tianwen transmission genealogy status regressed")\n    tianwen_graph = json.loads(TRANSMISSION_GRAPH.read_text(encoding="utf-8"))\n    if tianwen_graph.get("schema") != "TIANWEN-TRANSMISSION-GENEALOGY-GRAPH-R1" or tianwen_graph.get("status") != "ACTIVE_INCREMENTAL":\n        fail("Tianwen transmission graph identity/status regressed")\n    if not tianwen_graph.get("backfill", {}).get("future_material_batches_require_transmission_impact"):\n        fail("Tianwen future transmission-impact contract regressed")\n    protocol_text = TRANSMISSION_PROTOCOL.read_text(encoding="utf-8")\n    if "GENEALOGY_MODEL=EVIDENCE_SCOPED_GRAPH_NOT_SINGLE_TREE" not in protocol_text:\n        fail("Tianwen transmission graph-model contract missing")\n    if tianwen_state.get("invariants", {}).get("deterministic_fusion_chart_product_r1") != "CLOSED":\n        fail("Tianwen formalization reopened deterministic product")\n    if tianwen_state.get("invariants", {}).get("prediction_ai_interpretation_scope") != "OUT_OF_SCOPE_FOR_CURRENT_STAGE":\n        fail("Tianwen formalization changed prediction scope")\n\n'''
        s = s.replace(anchor, anchor + check, 1)

    MAIN_VERIFIER.write_text(s, encoding="utf-8")


def main() -> None:
    for rel in (CHARTER, GENEALOGY_PROTOCOL, GENEALOGY_GRAPH, "scripts/verify-tianwen-transmission-genealogy-r1.py"):
        if not (ROOT / rel).is_file():
            raise SystemExit(f"required Tianwen artifact missing before formalization: {rel}")
    update_state()
    update_continuity_protocol()
    update_main_verifier()


if __name__ == "__main__":
    main()
