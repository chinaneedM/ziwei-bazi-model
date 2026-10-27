from __future__ import annotations

from .models import Address, RingInstance, RingMemberBinding, Sex
from .registries import address, branch_index


RING_ALGORITHM_ID = "ZIWEI-RING-RUNTIME-V1"
RING_ALGORITHM_VERSION = "1.0.0"
WENMO_DEFAULT_RING_RULE_SET_ID = "WENMO_DEFAULT_RING_R1"
WENMO_DEFAULT_RING_RULE_SET_VERSION = "1.0.0"


class RingGenerationError(ValueError):
    def __init__(self, diagnostic_code: str) -> None:
        super().__init__(diagnostic_code)
        self.diagnostic_code = diagnostic_code


YANG_STEMS = {"甲", "丙", "戊", "庚", "壬"}

CHANGSHENG_MEMBERS = (
    ("CHANGSHENG", "长生"),
    ("MUYU", "沐浴"),
    ("GUANDAI", "冠带"),
    ("LINGUAN", "临官"),
    ("DIWANG", "帝旺"),
    ("SHUAI", "衰"),
    ("BING", "病"),
    ("SI", "死"),
    ("MU", "墓"),
    ("JUE", "绝"),
    ("TAI", "胎"),
    ("YANG", "养"),
)

TAISUI_MEMBERS = (
    ("SUIJIAN", "岁建"),
    ("HUIQI", "晦气"),
    ("SANGMEN", "丧门"),
    ("GUANSUO", "贯索"),
    ("GUANFU", "官符"),
    ("XIAOHAO", "小耗"),
    ("SUIPO", "岁破"),
    ("LONGDE", "龙德"),
    ("BAIHU", "白虎"),
    ("TIANDE", "天德"),
    ("DIAOKE", "吊客"),
    ("BINGFU", "病符"),
)

JIANGQIAN_MEMBERS = (
    ("JIANGXING", "将星"),
    ("PANAN", "攀鞍"),
    ("SUIYI", "岁驿"),
    ("XISHEN", "息神"),
    ("HUAGAI", "华盖"),
    ("JIESHA", "劫煞"),
    ("ZAISHA", "灾煞"),
    ("TIANSHA", "天煞"),
    ("ZHIBEI", "指背"),
    ("XIANCHI", "咸池"),
    ("YUESHA", "月煞"),
    ("WANGSHEN", "亡神"),
)

BOSHI_MEMBERS = (
    ("BOSHI", "博士"),
    ("LISHI", "力士"),
    ("QINGLONG", "青龙"),
    ("XIAOHAO", "小耗"),
    ("JIANGJUN", "将军"),
    ("ZOUSHU", "奏书"),
    ("FEILIAN", "飞廉"),
    ("XISHEN", "喜神"),
    ("BINGFU", "病符"),
    ("DAHAO", "大耗"),
    ("FUBING", "伏兵"),
    ("GUANFU", "官符"),
)

CHANGSHENG_ANCHOR_BY_ELEMENT = {
    "金": "巳",
    "木": "亥",
    "火": "寅",
    "水": "申",
    "土": "申",
}

JIANGQIAN_ANCHOR_BY_YEAR_BRANCH = {
    "申": "子", "子": "子", "辰": "子",
    "寅": "午", "午": "午", "戌": "午",
    "巳": "酉", "酉": "酉", "丑": "酉",
    "亥": "卯", "卯": "卯", "未": "卯",
}


def _direction(year_stem: str, sex: Sex) -> int:
    is_yang = year_stem in YANG_STEMS
    forward = (is_yang and sex is Sex.MALE) or ((not is_yang) and sex is Sex.FEMALE)
    return 1 if forward else -1


def _direction_name(direction: int) -> str:
    return "FORWARD" if direction == 1 else "REVERSE"


def _members(
    ring_id: str,
    member_defs: tuple[tuple[str, str], ...],
    anchor_index: int,
    direction: int,
    refs: tuple[str, ...],
) -> tuple[RingMemberBinding, ...]:
    return tuple(
        RingMemberBinding(
            member_id=f"{ring_id}.{member_id}",
            display_name=display_name,
            address=address(anchor_index + direction * ordinal),
            ordinal=ordinal,
            source_refs=refs,
        )
        for ordinal, (member_id, display_name) in enumerate(member_defs)
    )


def _ring(
    ring_id: str,
    display_name: str,
    anchor: Address,
    direction: int,
    member_defs: tuple[tuple[str, str], ...],
    refs: tuple[str, ...],
) -> RingInstance:
    return RingInstance(
        ring_id=ring_id,
        display_name=display_name,
        anchor_address=anchor,
        direction=_direction_name(direction),
        generator_id=RING_ALGORITHM_ID,
        algorithm_version=RING_ALGORITHM_VERSION,
        source_refs=refs,
        members=_members(ring_id, member_defs, anchor.index, direction, refs),
    )


class WenmoDefaultRingGenerator:
    """Operational ring state matching Wenmo's default yin/yang-direction settings."""

    rule_set_id = WENMO_DEFAULT_RING_RULE_SET_ID
    rule_set_version = WENMO_DEFAULT_RING_RULE_SET_VERSION

    @staticmethod
    def changsheng(bureau_element: str, year_stem: str, sex: Sex) -> RingInstance:
        try:
            anchor_branch = CHANGSHENG_ANCHOR_BY_ELEMENT[bureau_element]
        except KeyError as exc:
            raise ValueError(f"unsupported bureau element for Changsheng ring: {bureau_element}") from exc
        direction = _direction(year_stem, sex)
        refs = ("S01:ZZZA-PR-057", "COMPAT:WENMO-CHARTDIFF-006")
        return _ring(
            "RING.CHANGSHENG12",
            "长生十二神",
            address(branch_index(anchor_branch)),
            direction,
            CHANGSHENG_MEMBERS,
            refs,
        )

    @staticmethod
    def taisui(year_branch: str) -> RingInstance:
        anchor = address(branch_index(year_branch))
        refs = ("S01:ZZZA-PR-058", "COMPAT:WENMO-CHARTDIFF-006")
        return _ring("RING.TAISUI12", "岁前十二神", anchor, 1, TAISUI_MEMBERS, refs)

    @staticmethod
    def jiangqian(year_branch: str) -> RingInstance:
        try:
            anchor_branch = JIANGQIAN_ANCHOR_BY_YEAR_BRANCH[year_branch]
        except KeyError as exc:
            raise ValueError(f"unsupported year branch for Jiangqian ring: {year_branch}") from exc
        anchor = address(branch_index(anchor_branch))
        refs = ("S01:ZZZA-PR-059", "COMPAT:WENMO-CHARTDIFF-006")
        return _ring("RING.JIANGQIAN12", "将前十二神", anchor, 1, JIANGQIAN_MEMBERS, refs)

    @staticmethod
    def boshi(lucun_address: Address, year_stem: str, sex: Sex) -> RingInstance:
        direction = _direction(year_stem, sex)
        refs = ("S01:ZZZA-PR-060", "COMPAT:WENMO-CHARTDIFF-006")
        return _ring("RING.BOSHI12", "博士十二神", lucun_address, direction, BOSHI_MEMBERS, refs)

    def generate(
        self,
        bureau_element: str,
        year_stem: str,
        year_branch: str,
        sex: Sex,
        lucun_address: Address | None,
    ) -> tuple[RingInstance, ...]:
        if lucun_address is None:
            raise RingGenerationError("BOSHI_RING_REQUIRES_LUCUN_PLACEMENT")
        return (
            self.changsheng(bureau_element, year_stem, sex),
            self.taisui(year_branch),
            self.jiangqian(year_branch),
            self.boshi(lucun_address, year_stem, sex),
        )
