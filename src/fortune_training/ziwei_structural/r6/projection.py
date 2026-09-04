from __future__ import annotations

from dataclasses import dataclass

from fortune_training.ziwei_structural.r2 import RelativePalaceFrameState

from .models import QiShuPositionFact
from .profile import QISHU_CLOCKWISE_OFFSET, QISHU_RELATIVE_ORDINAL


@dataclass(frozen=True)
class QiShuMappingSpec:
    source_mapping_id: str
    origin_designation_id: str
    target_designation_id: str
    fixed_support_meaning: str


QISHU_MAPPING_SPECS = (
    QiShuMappingSpec("S04-QS-01", "LIFE", "CAREER", "本人状态落实为现实行为、责任与外显结构"),
    QiShuMappingSpec("S04-QS-02", "SIBLINGS", "PROPERTY", "同辈关系、内部资源和平级合作如何沉淀与承接"),
    QiShuMappingSpec("S04-QS-03", "SPOUSE", "FORTUNE", "关系如何进入长期相处、内在感受和精神承接"),
    QiShuMappingSpec("S04-QS-04", "CHILDREN", "PARENTS", "生育、子女、晚辈和产出如何进入制度、责任与现实承接"),
    QiShuMappingSpec("S04-QS-05", "WEALTH", "LIFE", "收入、现金流和价值交换如何回到命主或目标财务主体"),
    QiShuMappingSpec("S04-QS-06", "HEALTH", "SIBLINGS", "身体风险和医疗过程如何进入内部系统、资源调配和持续承载"),
    QiShuMappingSpec("S04-QS-07", "TRAVEL", "SPOUSE", "外部环境和移动如何形成对接、关系、契约与长期承接"),
    QiShuMappingSpec("S04-QS-08", "SERVANTS_FRIENDS", "CHILDREN", "团队、客户和外部人群如何转为执行、产出和后续承接"),
    QiShuMappingSpec("S04-QS-09", "CAREER", "WEALTH", "工作、职位和经营如何形成收入、现金流与现实回报"),
    QiShuMappingSpec("S04-QS-10", "PROPERTY", "HEALTH", "居住、产权和场所如何进入维护、使用与长期压力系统"),
    QiShuMappingSpec("S04-QS-11", "FORTUNE", "TRAVEL", "内在状态、欲望与价值取向如何外显为环境选择和行为"),
    QiShuMappingSpec("S04-QS-12", "PARENTS", "SERVANTS_FRIENDS", "父母、上司和制度如何通过组织、人群与平台承接"),
)


class QiShuProjectionError(ValueError):
    def __init__(self, diagnostic_code: str, detail: str) -> None:
        super().__init__(detail)
        self.diagnostic_code = diagnostic_code


def project_qishu_positions(r2_state: RelativePalaceFrameState) -> tuple[QiShuPositionFact, ...]:
    by_key = {
        (row.origin_designation_id, row.relative_ordinal): row
        for row in r2_state.frame_facts
    }
    facts: list[QiShuPositionFact] = []
    for spec in QISHU_MAPPING_SPECS:
        frame = by_key.get((spec.origin_designation_id, QISHU_RELATIVE_ORDINAL))
        if frame is None:
            raise QiShuProjectionError(
                "MISSING_R2_QISHU_FRAME_FACT",
                f"missing R2 ordinal {QISHU_RELATIVE_ORDINAL} fact for {spec.origin_designation_id}",
            )
        if frame.relative_role_designation_id != "CAREER":
            raise QiShuProjectionError(
                "R2_QISHU_ROLE_MISMATCH",
                f"{spec.origin_designation_id} ordinal 9 must carry CAREER relative role",
            )
        if frame.target_designation_id != spec.target_designation_id:
            raise QiShuProjectionError(
                "S04_QISHU_TARGET_MISMATCH",
                f"{spec.source_mapping_id} expected {spec.target_designation_id}, got {frame.target_designation_id}",
            )
        if frame.clockwise_offset != QISHU_CLOCKWISE_OFFSET:
            raise QiShuProjectionError(
                "R2_QISHU_GEOMETRY_MISMATCH",
                f"{spec.source_mapping_id} expected clockwise offset 4, got {frame.clockwise_offset}",
            )
        facts.append(
            QiShuPositionFact(
                source_mapping_id=spec.source_mapping_id,
                origin_designation_id=frame.origin_designation_id,
                origin_address=frame.origin_address,
                target_designation_id=frame.target_designation_id,
                target_address=frame.target_address,
                relative_ordinal=frame.relative_ordinal,
                clockwise_offset=frame.clockwise_offset,
                fixed_support_meaning=spec.fixed_support_meaning,
            )
        )
    return tuple(facts)
