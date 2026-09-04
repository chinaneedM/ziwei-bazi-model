from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DefectClass(str, Enum):
    IMPLEMENTATION_DEFECT = "IMPLEMENTATION_DEFECT"
    EXPECTED_PROFILE_DIFFERENCE = "EXPECTED_PROFILE_DIFFERENCE"
    DISPUTED_CANDIDATE = "DISPUTED_CANDIDATE"
    REFERENCE_DIFFERENCE = "REFERENCE_DIFFERENCE"
    TEST_ORACLE_DEFECT = "TEST_ORACLE_DEFECT"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class DefectRecord:
    defect_id: str
    classification: DefectClass
    capability_id: str
    case_id: str
    summary: str
    evidence: tuple[str, ...] = ()
    algorithm_reopened: bool = False

    def __post_init__(self) -> None:
        if not self.defect_id.strip():
            raise ValueError("defect_id must not be empty")
        if not self.capability_id.strip():
            raise ValueError("capability_id must not be empty")
        if not self.case_id.strip():
            raise ValueError("case_id must not be empty")
        if not self.summary.strip():
            raise ValueError("summary must not be empty")
        if self.algorithm_reopened and self.classification is not DefectClass.IMPLEMENTATION_DEFECT:
            raise ValueError(
                "only IMPLEMENTATION_DEFECT may authorize a local algorithm reopen"
            )
