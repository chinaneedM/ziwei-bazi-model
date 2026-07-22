from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
WORKBENCH = ROOT / "knowledge-workbench"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate() -> dict[str, int]:
    card_schema = load(WORKBENCH / "knowledge-card.schema.json")
    hypothesis_schema = load(WORKBENCH / "research-hypothesis.schema.json")
    card_validator = Draft202012Validator(card_schema)
    hypothesis_validator = Draft202012Validator(hypothesis_schema)
    manifest = load(ROOT / "sources/canonical-manifest.json")
    source_paths = {row["source_id"]: ROOT / row["path"] for row in manifest["sources"]}
    source_line_counts = {
        source_id: sum(1 for _ in path.open(encoding="utf-8"))
        for source_id, path in source_paths.items()
    }

    collections = [
        load(WORKBENCH / "school-method-cards.json"),
        load(WORKBENCH / "batch-a-static-cards.json"),
    ]
    cards = [card for collection in collections for card in collection["cards"]]
    card_ids = [card["card_id"] for card in cards]
    if len(card_ids) != len(set(card_ids)):
        raise ValueError("knowledge card ids must be unique")
    for card in cards:
        card_validator.validate(card)
        if card["status"] == "CURATED_UNVALIDATED" and any(
            card["validation"][key] != 0
            for key in ("distinct_case_count", "support_count", "counterexample_count")
        ):
            raise ValueError(f"unvalidated card carries outcome evidence: {card['card_id']}")
        for source_anchor in card["source_anchors"]:
            source_id = source_anchor["source_id"]
            if source_id not in source_paths:
                raise ValueError(f"unknown source id in {card['card_id']}: {source_id}")
            if source_anchor["line_start"] > source_anchor["line_end"]:
                raise ValueError(f"reversed source anchor in {card['card_id']}")
            if source_anchor["line_end"] > source_line_counts[source_id]:
                raise ValueError(f"source anchor exceeds file in {card['card_id']}")

    conflict = load(WORKBENCH / "batch-a-conflict-matrix.json")
    known_batch_ids = {card["card_id"] for card in collections[1]["cards"]}
    for row in conflict["rows"]:
        if not set(row["card_ids"]).issubset(known_batch_ids):
            raise ValueError(f"conflict row references unknown Batch A card: {row['conflict_id']}")

    coverage = load(WORKBENCH / "batch-a-case-coverage.json")
    if coverage["answer_data_used"] is not False:
        raise ValueError("Batch A coverage must remain answer-free")
    if {row["card_id"] for row in coverage["mappings"]} != known_batch_ids:
        raise ValueError("Batch A coverage does not map every card exactly once")
    for row in coverage["mappings"]:
        if row["eligible_case_count"] != len(row["eligible_case_ids"]):
            raise ValueError(f"coverage case count mismatch: {row['card_id']}")
        if row["eligible_question_count"] != len(row["eligible_question_refs"]):
            raise ValueError(f"coverage question count mismatch: {row['card_id']}")

    registry = load(WORKBENCH / "research-hypotheses.json")
    policy = registry["origin_policy"]
    if policy != {
        "allowed_origins": ["USER_HYPOTHESIS", "AI_HYPOTHESIS"],
        "equal_validation_threshold": True,
        "identity_grants_extra_weight": False,
        "direct_promotion_to_truth_allowed": False,
    }:
        raise ValueError("user and AI hypotheses must use the same validation policy")
    for hypothesis in registry["hypotheses"]:
        hypothesis_validator.validate(hypothesis)

    return {
        "cards": len(cards),
        "batch_a_cards": len(known_batch_ids),
        "conflicts": len(conflict["rows"]),
        "coverage_mappings": len(coverage["mappings"]),
        "hypotheses": len(registry["hypotheses"]),
    }


def main() -> int:
    print(json.dumps(validate(), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
