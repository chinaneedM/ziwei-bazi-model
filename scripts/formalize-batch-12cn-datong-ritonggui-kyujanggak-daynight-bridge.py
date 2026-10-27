"""Retired Batch 12CN formalizer.

Batch 12CO (BATCH-12-ZIWEI-DATONG-RITONGGUI-KOSTMA-ATTRIBUTION-REPAIR-CO) proved that the original Batch 12CN generator
mixed record-field and holding-identifier provenance. Re-running the old generator
would reintroduce withdrawn claims, so it is intentionally disabled.
"""

REPAIR_BATCH = "BATCH-12-ZIWEI-DATONG-RITONGGUI-KOSTMA-ATTRIBUTION-REPAIR-CO"
REPAIR_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-DATONG-RITONGGUI-KOSTMA-ATTRIBUTION-REPAIR-CO.md"


def main() -> None:
    raise SystemExit(
        "Batch 12CN formalizer is retired after Batch 12CO provenance repair; "
        f"see {REPAIR_DOC}"
    )


if __name__ == "__main__":
    main()
