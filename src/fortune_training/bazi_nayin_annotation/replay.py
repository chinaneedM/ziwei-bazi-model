from __future__ import annotations

from fortune_training.bazi_chart.models import BaziNatalState
from fortune_training.bazi_chart.profile import ResolvedBaziCalculationProfile
from fortune_training.calendar_foundation.models import json_value

from .models import BaziNayinAnnotationResolution, NayinIntegrityDiagnostic, NayinIntegrityReport
from .service import BaziNayinAnnotationService


NAYIN_REPLAY_ALGORITHM_ID = "BAZI-NAYIN-FULL-REPLAY-R1"
NAYIN_REPLAY_ALGORITHM_VERSION = "1.0.0"


def validate_nayin_full_replay(
    natal: BaziNatalState,
    profile: ResolvedBaziCalculationProfile,
    resolution: BaziNayinAnnotationResolution,
) -> NayinIntegrityReport:
    diagnostics: list[NayinIntegrityDiagnostic] = []
    try:
        expected = BaziNayinAnnotationService().resolve(natal, profile)
    except ValueError as exc:
        diagnostics.append(
            NayinIntegrityDiagnostic(
                code="FULL_REPLAY_SOURCE_FAILED",
                path="source",
                detail=str(exc),
            )
        )
    else:
        if json_value(resolution) != json_value(expected):
            diagnostics.append(
                NayinIntegrityDiagnostic(
                    code="FULL_REPLAY_MISMATCH",
                    path="resolution",
                    detail="published annotation resolution does not exactly replay",
                )
            )

    return NayinIntegrityReport(
        status="PASS" if not diagnostics else "FAIL",
        diagnostics=tuple(diagnostics),
        algorithm_id=NAYIN_REPLAY_ALGORITHM_ID,
        algorithm_version=NAYIN_REPLAY_ALGORITHM_VERSION,
    )
