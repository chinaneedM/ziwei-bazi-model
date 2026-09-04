from __future__ import annotations

from copy import deepcopy
import unittest

from fortune_training.bazi_application.temporal_annotations import (
    TEMPORAL_CLASSICAL_ANNOTATION_HASH_VERSION,
    TEMPORAL_CLASSICAL_ANNOTATION_PROFILE_VERSION,
    temporal_classical_annotation,
    temporal_classical_annotation_hashes,
)


class BaziTemporalHiddenStemOrderLineageR1Tests(unittest.TestCase):
    def _annotation(self):
        return temporal_classical_annotation(
            "乙丑",
            "甲",
            source_layer="ANNUAL",
            context_id="TEST:HIDDEN-STEM-ORDER",
        )

    def test_order_is_lineage_not_fact_identity(self) -> None:
        annotation = self._annotation()
        self.assertEqual("1.0.2", TEMPORAL_CLASSICAL_ANNOTATION_PROFILE_VERSION)
        self.assertEqual("1.0.1", TEMPORAL_CLASSICAL_ANNOTATION_HASH_VERSION)
        self.assertEqual(
            ["己", "癸", "辛"],
            [row["stem"] for row in annotation["hidden_stems"]],
        )

        reordered = deepcopy(annotation)
        by_stem = {row["stem"]: row for row in reordered["hidden_stems"]}
        reordered["hidden_stems"] = [
            {**by_stem[stem], "registry_ordinal": ordinal}
            for ordinal, stem in enumerate(("癸", "辛", "己"))
        ]
        reordered["fact_hash"] = ""
        reordered["computation_hash"] = ""

        original_hashes = temporal_classical_annotation_hashes(annotation)
        reordered_hashes = temporal_classical_annotation_hashes(reordered)
        self.assertEqual(original_hashes[0], reordered_hashes[0])
        self.assertNotEqual(original_hashes[1], reordered_hashes[1])

    def test_membership_change_still_changes_fact_identity(self) -> None:
        annotation = self._annotation()
        changed = deepcopy(annotation)
        changed["hidden_stems"] = changed["hidden_stems"][:-1]
        changed["fact_hash"] = ""
        changed["computation_hash"] = ""
        self.assertNotEqual(
            temporal_classical_annotation_hashes(annotation)[0],
            temporal_classical_annotation_hashes(changed)[0],
        )


if __name__ == "__main__":
    unittest.main()
