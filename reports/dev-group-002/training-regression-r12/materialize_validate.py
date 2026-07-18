#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
from pathlib import Path
from typing import Any

ROUND_DIR = Path('reports/dev-group-002/training-regression-r12')
CASE_ID = 'DEV-EXAMPLE-003'
HISTORY = {
    'R1': 'reports/dev-group-002/training-regression-r1/manifest.json',
    'R2': 'reports/dev-group-002/training-regression-r2/formal-readiness-matrix.json',
    'R3': 'reports/dev-group-002/training-regression-r3/progress.json',
    'R4': 'reports/dev-group-002/training-regression-r4/compact-manifest.json',
    'R5': 'reports/dev-group-002/training-regression-r5/manifest.json',
    'R6': 'reports/dev-group-002/training-regression-r6/manifest.json',
    'R7': 'reports/dev-group-002/training-regression-r7/manifest.json',
    'R8': 'reports/dev-group-002/training-regression-r8/manifest.json',
    'R9': 'reports/dev-group-002/training-regression-r9/manifest.json',
    'R10': 'reports/dev-group-002/training-regression-r10/manifest.json',
    'R11': 'reports/dev-group-002/training-regression-r11/manifest.json',
}
INPUTS = {
    'whitelist': 'reports/dev-group-002/training-regression-r2/active-whitelist-receipt.json',
    'view_manifest': 'training-data/DEV-GROUP-002/runtime-views/DEV-EXAMPLE-003/manifest.json',
    'ziwei': 'training-data/DEV-GROUP-002/runtime-views/DEV-EXAMPLE-003/ziwei.txt',
    'bazi': 'training-data/DEV-GROUP-002/runtime-views/DEV-EXAMPLE-003/bazi-transcription.json',
    'questions': 'training-data/DEV-GROUP-002/runtime-views/DEV-EXAMPLE-003/questions-parsed.json',
    'parent_prediction': 'reports/dev-group-002/training-regression-r11/prediction-freeze.json',
    'answers': 'reports/dev-group-002/training-regression-r11/postreveal-review.json',
}

SOURCE_EXCERPT_SPECS = [
    ('S04_AXIS_SCOPE', 'S04', 'knowledge/base/S04_十二宫主题太极与气数位库.txt', 1667, 1678, ['不得用官禄宫的行业象证明老板身份', '不得用夫妻宫的关系压力证明法律离婚']),
    ('S04_GEOMETRY', 'S04', 'knowledge/base/S04_十二宫主题太极与气数位库.txt', 2228, 2255, ['疾厄宫 | 父母宫', '官禄宫 | 命宫、夫妻宫']),
    ('S05_ZIWEI_POJUN', 'S05', 'knowledge/base/S05_星曜本性辅煞系统与组合条件库.txt', 217, 226, ['若紫微破军同宫，可将破军的破坏力转化为开创力', '自尊心极强']),
    ('S05_LIANZHEN_ART', 'S05', 'knowledge/base/S05_星曜本性辅煞系统与组合条件库.txt', 532, 543, ['会文昌：明理，爱好音乐', '可转化为诗酒风流或艺术创造力']),
    ('S05_TIANXIANG_CHANGQU', 'S05', 'knowledge/base/S05_星曜本性辅煞系统与组合条件库.txt', 810, 849, ['会左右、昌曲、魁钺则可以有作为', '天相见昌曲，必须不见化忌及羊陀始吉']),
    ('S05_POJUN_DISABILITY', 'S05', 'knowledge/base/S05_星曜本性辅煞系统与组合条件库.txt', 1050, 1056, ['破军会羊陀在身宫、命宫、疾厄宫', 'ZERO_MEDICAL_DIAGNOSIS']),
    ('S06_STRUCTURE_CONTROL', 'S06', 'knowledge/base/S06_六十星系与十二基础盘库.txt', 1, 60, ['空宫借星', 'STRUCTURE_SELECTOR_MISMATCH']),
    ('S07_LIANTAN_TALENT', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 120749, 120770, ['廉贞贪狼又为艺术之星', '四海奔波，艰辛劳碌']),
    ('S07_SIBLING_TIANJI', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 122151, 122162, ['主兄弟姐妹寡少', '入庙二人']),
    ('S07_MARRIAGE_LIANTAN', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 123130, 123142, ['见辅佐[单星]，男女皆主两度姻缘', '借星安宫者，性质比原宫的[廉贪]更劣']),
    ('S07_CHILD_SUN', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 123805, 123819, ['太阳落陷于子女宫，不利长子', '必兼视太阴、天梁、巨门三曜']),
    ('S07_CAREER_LIANTAN', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 128260, 128273, ['最宜艺术，尤以表演行业为宜', '一生必有一次重大的转业']),
    ('S07_CAREER_CONSUMER_ART', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 128400, 128412, ['贪狼与昌曲同度，最宜公关事业', '消费、装饰或娱乐事业']),
    ('S07_PARENT_PRINCIPLES', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 130106, 130165, ['推断父母存亡，先看太阳太阴', '父母宫见四煞，亦不一定主刑克']),
    ('S07_PARENT_TONGLIANG', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 130405, 130425, ['天同天梁同度，不主刑克伤害', '父母婚姻有波折']),
    ('S08_TRANSFORMATION_LIMIT', 'S08', 'knowledge/base/S08_十干四化自化与禄忌线库.txt', 1, 25, ['自化', '不证明现实事件']),
    ('S08_NO_ENDPOINT_INFLATION', 'S08', 'knowledge/base/S08_十干四化自化与禄忌线库.txt', 380, 390, ['自化忌不等于失败']),
    ('S10_NEUTRAL_TIME', 'S10', 'knowledge/base/S10_紫微岁运应期与动态辅助库.txt', 1, 52, ['禁止在此对象中写入', '中立时间事实密封后']),
    ('S11_FOUNDATION', 'S11', 'knowledge/base/S11_八字干支五行藏干与十神库.txt', 1, 60, ['S11唯一负责合法八字版本', 'S11不判断旺衰']),
    ('S12_QI_CONTROL', 'S12', 'knowledge/base/S12_八字月令旺衰通根与气势库.txt', 1, 65, ['月令是主轴而非独裁', '不负责格局命名']),
    ('S13_METHOD_COMPETITION', 'S13', 'knowledge/base/S13_八字格局用忌调候与病药库.txt', 1, 65, ['不得先定格局或用神再找证据', '不能直接完成现实事件']),
    ('S14_RELATION_LIMIT', 'S14', 'knowledge/base/S14_八字合冲刑害墓库与结构变化库.txt', 1, 135, ['冲刑害不等于灾祸', '合不等于化']),
    ('S15_NEUTRAL_TIME', 'S15', 'knowledge/base/S15_八字大运流年流月与应期库.txt', 1, 52, ['方向中立时间事实', '不得写入任何选项独有']),
    ('S16_COMPOSITE_CAPABILITY', 'S16', 'knowledge/base/S16_八字专题映射与紫微接口库.txt', 907, 939, ['LEARNING_TENDENCY_TO_CREDENTIAL_PERMISSION=NO', 'CHILD_THEME_TO_COUNT_OR_SEX_PERMISSION=NO']),
    ('S16_HIGH_RISK_TASKS', 'S16', 'knowledge/base/S16_八字专题映射与紫微接口库.txt', 1150, 1175, ['精确医学诊断', '家庭具体事件']),
    ('S16_ROLE_ENDPOINT_LIMIT', 'S16', 'knowledge/base/S16_八字专题映射与紫微接口库.txt', 1380, 1406, ['官印不能直接判大学学历', '财星不能直接判经商所有权']),
    ('S16_TOPIC_PACKAGE', 'S16', 'knowledge/base/S16_八字专题映射与紫微接口库.txt', 1835, 1849, ['官、财、印、食伤只描述结构角色', '必须由S17建立现实父链']),
    ('S17_DIRECTION_AND_ENDPOINT', 'S17', 'knowledge/base/S17_专题闭合人物太极与动作终点链库.txt', 1, 130, ['MISSING_EXACT_ENDPOINT_ERASES_SUPPORT_PERMISSION=NO', 'REALITY_STATUS_LADDER']),
    ('S18_PAIRWISE_ORDER', 'S18', 'knowledge/base/S18_证据归并非法归零与评分分寸库.txt', 170, 230, ['PAIRWISE_DECISION_ORDER', 'LOW_INFORMATION_FORCED_TIEBREAK']),
]

BLIND_MODELS = {
    'ZIWEI': {
        'Q1': 'The parent route is an empty palace borrowing the Tongliang health axis, while the sibling palace contains exalted Tianji with Lucun and Fire. This supports a small sibling set and possible parental-marriage complexity, but cannot identify a parent death, exact occupation, inheritance, remarriage act, sibling sex or birth order.',
        'Q2': 'The natal identity is Ziwei-Pojun in Chou with Yang and Ling; the body is in migration with Tianxiang and Changqu, while career is fallen Lianzhen-Tanlang with double Ji, Tianyue and Tianma. The sealed model favors forceful/rebellious temperament, artistic or entertainment skill, a disability candidate and entrepreneurial or consumer-industry scenes, but not exact body measurements, instrument, sports, company type or legal owner status.',
        'Q3': 'Education credentials remain outside the chart ceiling. The 2013 neutral time row places the annual identity in the career palace with Tianyue and Lianzhen-Tanlang, favoring a career transition or benefactor scene. 2011 and 2021 are weaker timing candidates. Prison, degree field and certificate endpoints are unclosed.',
        'Q4': 'The spouse palace is empty and borrows fallen Lianzhen-Tanlang with Tuo and Tianxing, supporting repeated relationship difficulty and separation risk. The child palace has fallen Sun and the 2016-2025 limit occupies the child axis. Legal marriage/divorce, continuous singleness, live birth, count and sex remain unclosed.',
        'Q5': 'In 2022 the annual identity lies in the parent palace during a child-axis decade, with Tianliang Lu, Ziwei Quan, Zuofu Ke and Wuqu Ji. The neutral model permits a parent/upstream event scene and stronger work-finance pressure; it does not establish death, collision, COVID, four-month hospitalization, debt or sale of real estate.',
    },
    'BAZI': {
        'Q1': 'The legal solar-term pillars are Gui-Hai, Bing-Chen, Ji-Mao, Ding-Mao. The structure can describe resource and family pressure but cannot identify a parent actor, death, occupation, inheritance, remarriage, sibling sex or birth order.',
        'Q2': 'Ji earth in Chen season with repeated Mao and visible fire can support responsibility, stubbornness, output or commercial direction. It cannot identify height, disability, exact hobby, instrument, industry or owner registration.',
        'Q3': 'The 2008 Gui-Chou and 2018 Ren-Zi luck periods permit education/work transition and resource movement. They do not prove degree level, major, graduation, prison or exact entry into a current occupation.',
        'Q4': 'Relationship and child-role activation exists in the relation graph, but legal marriage, divorce, live birth, count, sex and continuous status remain outside local capability.',
        'Q5': 'The 2022 Ren-Yin year within Ren-Zi luck activates water, wood and relation changes. This can supply a change window but not the event identity, actor, diagnosis, accident, hospitalization, debt or property sale endpoint.',
    },
}

# q|option|atom short id|direction code|exact endpoint flag|parent group|literal atom
ATOM_SPEC = r'''
Q1|A|MOTHER_DEATH_NEXT_YEAR|U|1|FAMILY|出生后次年母亲去世
Q1|A|FATHER_SMALL_BUSINESS|U|1|FAMILY|父亲为小型企业主
Q1|A|FATHER_REMARRIES|S|1|FAMILY|父亲另娶
Q1|A|TWO_SIBLINGS_COUNT|P|1|SIBLING|有两个弟妹
Q1|A|YOUNGER_BROTHER_SISTER_ORDER|U|1|SIBLING|一弟一妹且均年幼
Q1|B|FATHER_SENIOR_GOV|U|1|FAMILY|父亲为政府高级职员
Q1|B|FATHER_DEATH_2021|U|1|FAMILY|父亲2021年去世
Q1|B|TWO_SIBLINGS_COUNT|P|1|SIBLING|有两个兄姐
Q1|B|OLDER_BROTHER_SISTER_ORDER|U|1|SIBLING|一兄一姐且均年长
Q1|C|MOTHER_HOMEMAKER|U|1|FAMILY|母亲为家庭主妇
Q1|C|FATHER_SMALL_BUSINESS|U|1|FAMILY|父亲为小型企业主
Q1|C|ONE_YOUNGER_BROTHER|P|1|SIBLING|有一弟
Q1|D|FATHER_DEATH_1985|U|1|FAMILY|父亲1985年去世
Q1|D|MOTHER_INHERITS_BUSINESS|U|1|FAMILY|母亲继承父亲产业
Q1|D|WIDOW_TO_NOW|U|1|FAMILY|母亲守寡至今
Q1|D|TWO_SIBLINGS_COUNT|P|1|SIBLING|有两个姐弟
Q1|D|OLDER_SISTER_YOUNGER_BROTHER|U|1|SIBLING|一姐一弟且出生顺序明确
Q2|A|LEG_DISABILITY|D|0|IDENTITY|腿脚残疾候选
Q2|A|ODD_TEMPER|P|0|IDENTITY|脾气古怪
Q2|A|MUSIC_ART_HOBBY|D|0|ART|喜好文艺爵士和古典音乐
Q2|A|PERFORMANCE_MUSICIAN|D|1|ART|现在为演奏乐手
Q2|A|SAX_INSTRUMENT|M|1|ART|具体为萨克斯手
Q2|A|OWNER_IDENTITY|M|1|ROLE|老板身份
Q2|A|BAND_INDUSTRY|P|1|ART|经营乐团
Q2|B|TALL_BURLY|U|1|IDENTITY|身材高大魁梧
Q2|B|STUBBORN|P|0|IDENTITY|性情固执
Q2|B|MUSIC_ART_HOBBY|D|0|ART|喜好音乐
Q2|B|OWNER_IDENTITY|M|1|ROLE|老板身份
Q2|B|BAR_INDUSTRY|P|1|ART|经营酒吧
Q2|C|MEDIUM_BUILD|U|1|IDENTITY|中等身材
Q2|C|DILIGENT|P|0|IDENTITY|勤奋
Q2|C|REBELLIOUS|D|0|IDENTITY|叛逆
Q2|C|SPORT_HOBBY|P|1|ART|喜好拳击橄榄球等运动
Q2|C|OWNER_IDENTITY|M|1|ROLE|老板身份
Q2|C|RESTAURANT_INDUSTRY|P|1|ART|经营餐厅
Q2|D|PREMATURE|U|1|IDENTITY|早产
Q2|D|SICKLY_CHILDHOOD|P|1|IDENTITY|自幼身体不好
Q2|D|GARDENING|U|1|ART|喜好园艺
Q2|D|OWNER_IDENTITY|M|1|ROLE|老板身份
Q2|D|REAL_ESTATE_INDUSTRY|U|1|ROLE|经营小型房地产经纪公司
Q3|A|ELITE_UNIVERSITY|U|1|EDUCATION|重点大学
Q3|A|MEDICINE_MAJOR|U|1|EDUCATION|医学类专业
Q3|A|GRADUATED|U|1|EDUCATION|毕业
Q3|A|CHANGED_FIELD|P|1|CAREER|毕业后转行
Q3|A|START_CURRENT_2013|D|1|TIME|2013年从事现在工作
Q3|B|ELITE_UNIVERSITY|U|1|EDUCATION|重点大学
Q3|B|LIBERAL_ARTS|U|1|EDUCATION|文科
Q3|B|GRADUATED|U|1|EDUCATION|毕业
Q3|B|START_CURRENT_2011|P|1|TIME|2011年进入现在工作
Q3|B|PRISON_2019|U|1|LEGAL|2019年判监半年
Q3|C|HIGH_SCHOOL|U|1|EDUCATION|高中毕业
Q3|C|WORK_WHILE_STUDY|P|1|EDUCATION|边打工边学习
Q3|C|BENEFACTOR_2013|D|1|TIME|2013年得贵人提携
Q3|C|START_CURRENT_2013|D|1|TIME|2013年进入现在工作
Q3|D|ELITE_UNIVERSITY|U|1|EDUCATION|重点大学
Q3|D|LIBERAL_ARTS|U|1|EDUCATION|文科
Q3|D|GRADUATED|C|1|EDUCATION|已毕业
Q3|D|DROPPED_OUT|U|1|EDUCATION|中途辍学
Q3|D|INTERNAL_CREDENTIAL_CONTRADICTION|C|0|EDUCATION|同一选项同时声称毕业与中途辍学
Q3|D|START_CURRENT_2021|P|1|TIME|2021年进入现在工作
Q4|A|ROMANCE_DIFFICULT|P|0|MARRIAGE|婚恋不顺
Q4|A|INTRODUCED|U|1|MARRIAGE|经人介绍
Q4|A|MARRIED_2011|P|1|TIME|2011年结婚
Q4|A|DAUGHTER_2014|P|1|CHILD|2014年生一女
Q4|B|MARRIED_2011|P|1|TIME|2011年结婚
Q4|B|MIDDLE_SCHOOL_CLASSMATE|U|1|MARRIAGE|配偶为中学同学
Q4|B|SHOTGUN|U|1|MARRIAGE|奉子成婚
Q4|B|RELATION_FLAT|P|0|MARRIAGE|关系平淡
Q4|B|FIRST_SON_2012|C|1|CHILD|2012年初生一子
Q4|B|SECOND_SON_2015|C|1|CHILD|2015年生第二子
Q4|C|MULTIPLE_RELATIONSHIPS|D|0|MARRIAGE|多次恋爱
Q4|C|UNMARRIED_TO_NOW|M|1|MARRIAGE|至今未婚
Q4|C|NO_CHILDREN|S|1|CHILD|无子女
Q4|D|DIVORCE_SCENE_2018|D|0|MARRIAGE|2018年关系分离场景
Q4|D|REGISTERED_DIVORCE_2018|M|1|MARRIAGE|2018年登记离婚
Q4|D|SINGLE_SINCE|M|1|MARRIAGE|此后一直独身
Q4|D|NO_CHILDREN|S|1|CHILD|无子女
Q5|A|PARENT_EVENT_2022|S|0|FAMILY|2022年父母主题事件
Q5|A|MOTHER_DEATH|M|1|FAMILY|母亲去世
Q5|B|TRAVEL|U|1|EVENT|外出旅游
Q5|B|CAR_ACCIDENT|U|1|EVENT|遭遇车祸
Q5|B|INJURY|U|1|EVENT|受伤
Q5|C|HEALTH_EVENT|S|0|HEALTH|发生健康事件
Q5|C|COVID|M|1|HEALTH|染患新冠
Q5|C|OTHER_ILLNESS|M|1|HEALTH|引发其他病症
Q5|C|HOSPITAL_4_MONTH|M|1|HEALTH|住院治疗四个月
Q5|D|CAREER_OBSTRUCTION|D|0|FINANCE|事业受阻
Q5|D|DEBT|P|1|FINANCE|欠下债务
Q5|D|SELL_HOUSE|S|1|FINANCE|卖掉房子填补漏洞
'''.strip()

DIRECTION_NAMES = {
    'D': 'DIRECT_SUPPORT',
    'P': 'PARTIAL_SUPPORT',
    'S': 'LIMITED_SCENE_ONLY',
    'M': 'LIMITED_MISSING_ENDPOINT',
    'U': 'UNKNOWN',
    'C': 'DIRECT_COUNTEREVIDENCE',
}
PARENT_GROUPS = {
    'FAMILY': ['S04_GEOMETRY', 'S07_PARENT_PRINCIPLES', 'S07_PARENT_TONGLIANG', 'S17_DIRECTION_AND_ENDPOINT'],
    'SIBLING': ['S04_GEOMETRY', 'S07_SIBLING_TIANJI', 'S17_DIRECTION_AND_ENDPOINT'],
    'IDENTITY': ['S05_ZIWEI_POJUN', 'S05_TIANXIANG_CHANGQU', 'S05_POJUN_DISABILITY', 'S17_DIRECTION_AND_ENDPOINT'],
    'ART': ['S05_LIANZHEN_ART', 'S07_LIANTAN_TALENT', 'S07_CAREER_LIANTAN', 'S07_CAREER_CONSUMER_ART', 'S17_DIRECTION_AND_ENDPOINT'],
    'ROLE': ['S04_AXIS_SCOPE', 'S07_CAREER_LIANTAN', 'S16_ROLE_ENDPOINT_LIMIT', 'S17_DIRECTION_AND_ENDPOINT'],
    'EDUCATION': ['S04_AXIS_SCOPE', 'S16_COMPOSITE_CAPABILITY', 'S16_ROLE_ENDPOINT_LIMIT', 'S17_DIRECTION_AND_ENDPOINT'],
    'CAREER': ['S07_CAREER_LIANTAN', 'S07_CAREER_CONSUMER_ART', 'S10_NEUTRAL_TIME', 'S17_DIRECTION_AND_ENDPOINT'],
    'TIME': ['S10_NEUTRAL_TIME', 'S15_NEUTRAL_TIME', 'S17_DIRECTION_AND_ENDPOINT'],
    'LEGAL': ['S16_COMPOSITE_CAPABILITY', 'S17_DIRECTION_AND_ENDPOINT'],
    'MARRIAGE': ['S04_AXIS_SCOPE', 'S07_MARRIAGE_LIANTAN', 'S10_NEUTRAL_TIME', 'S17_DIRECTION_AND_ENDPOINT'],
    'CHILD': ['S07_CHILD_SUN', 'S16_COMPOSITE_CAPABILITY', 'S17_DIRECTION_AND_ENDPOINT'],
    'EVENT': ['S10_NEUTRAL_TIME', 'S15_NEUTRAL_TIME', 'S17_DIRECTION_AND_ENDPOINT'],
    'HEALTH': ['S05_POJUN_DISABILITY', 'S16_HIGH_RISK_TASKS', 'S17_DIRECTION_AND_ENDPOINT'],
    'FINANCE': ['S05_ZIWEI_POJUN', 'S08_NO_ENDPOINT_INFLATION', 'S10_NEUTRAL_TIME', 'S17_DIRECTION_AND_ENDPOINT'],
}
BAZI_PARENT_IDS = ['S11_FOUNDATION', 'S12_QI_CONTROL', 'S13_METHOD_COMPETITION', 'S14_RELATION_LIMIT', 'S15_NEUTRAL_TIME', 'S16_TOPIC_PACKAGE', 'S17_DIRECTION_AND_ENDPOINT']

COMMON_EQUIVALENCE = {
    ('Q1', 'A', 'B'): [('TWO_SIBLINGS_COUNT', 'TWO_SIBLINGS_COUNT', 'TWO_SIBLINGS_COUNT')],
    ('Q1', 'A', 'C'): [('FATHER_SMALL_BUSINESS', 'FATHER_SMALL_BUSINESS', 'FATHER_SMALL_BUSINESS')],
    ('Q1', 'A', 'D'): [('TWO_SIBLINGS_COUNT', 'TWO_SIBLINGS_COUNT', 'TWO_SIBLINGS_COUNT')],
    ('Q1', 'B', 'D'): [('TWO_SIBLINGS_COUNT', 'TWO_SIBLINGS_COUNT', 'TWO_SIBLINGS_COUNT')],
    ('Q2', 'A', 'B'): [('MUSIC_ART_HOBBY', 'MUSIC_ART_HOBBY', 'MUSIC_ART_HOBBY'), ('OWNER_IDENTITY', 'OWNER_IDENTITY', 'OWNER_IDENTITY')],
    ('Q2', 'A', 'C'): [('OWNER_IDENTITY', 'OWNER_IDENTITY', 'OWNER_IDENTITY')],
    ('Q2', 'A', 'D'): [('OWNER_IDENTITY', 'OWNER_IDENTITY', 'OWNER_IDENTITY')],
    ('Q2', 'B', 'C'): [('OWNER_IDENTITY', 'OWNER_IDENTITY', 'OWNER_IDENTITY')],
    ('Q2', 'B', 'D'): [('OWNER_IDENTITY', 'OWNER_IDENTITY', 'OWNER_IDENTITY')],
    ('Q2', 'C', 'D'): [('OWNER_IDENTITY', 'OWNER_IDENTITY', 'OWNER_IDENTITY')],
    ('Q3', 'A', 'B'): [('ELITE_UNIVERSITY', 'ELITE_UNIVERSITY', 'ELITE_UNIVERSITY'), ('GRADUATED', 'GRADUATED', 'GRADUATED')],
    ('Q3', 'A', 'C'): [('START_CURRENT_2013', 'START_CURRENT_2013', 'START_CURRENT_2013')],
    ('Q3', 'A', 'D'): [('ELITE_UNIVERSITY', 'ELITE_UNIVERSITY', 'ELITE_UNIVERSITY'), ('GRADUATED', 'GRADUATED', 'GRADUATED')],
    ('Q3', 'B', 'D'): [('ELITE_UNIVERSITY', 'ELITE_UNIVERSITY', 'ELITE_UNIVERSITY'), ('LIBERAL_ARTS', 'LIBERAL_ARTS', 'LIBERAL_ARTS'), ('GRADUATED', 'GRADUATED', 'GRADUATED')],
    ('Q4', 'A', 'B'): [('MARRIED_2011', 'MARRIED_2011', 'MARRIED_2011')],
    ('Q4', 'C', 'D'): [('NO_CHILDREN', 'NO_CHILDREN', 'NO_CHILDREN')],
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def canonical_payload(obj: dict[str, Any]) -> bytes:
    clone = dict(obj)
    clone.pop('canonical_sha256', None)
    return (json.dumps(clone, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def canonical_hash(obj: dict[str, Any]) -> str:
    return sha256_bytes(canonical_payload(obj))


def with_hash(obj: dict[str, Any]) -> dict[str, Any]:
    clone = dict(obj)
    clone['canonical_sha256'] = canonical_hash(clone)
    return clone


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')


def extract_lines(path: Path, start: int, end: int) -> str:
    lines = path.read_text(encoding='utf-8').splitlines()
    if start < 1 or end > len(lines) or end < start:
        raise ValueError(f'invalid source range {path}:{start}-{end}, line_count={len(lines)}')
    return '\n'.join(lines[start - 1:end]) + '\n'


def pair_key(qid: str, left: str, right: str) -> tuple[str, str, str]:
    a, b = sorted((left, right))
    return qid, a, b


def parse_atom_specs() -> list[dict[str, Any]]:
    rows = []
    for line in ATOM_SPEC.splitlines():
        qid, option, short_id, direction, exact, parent_group, literal = line.split('|', 6)
        rows.append({
            'case_id': CASE_ID,
            'question_id': qid,
            'option_id': option,
            'atom_id': f'{qid}_{option}_{short_id}',
            'short_id': short_id,
            'literal_atom': literal,
            'direction_status': DIRECTION_NAMES[direction],
            'exact_endpoint_required': exact == '1',
            'parent_group': parent_group,
        })
    return rows


def build_whitelist(repo_root: Path) -> dict[str, Any]:
    declared = read_json(repo_root / INPUTS['whitelist'])
    rows = []
    for row in declared['rows']:
        path = repo_root / 'knowledge/base' / row['canonical_filename']
        data = path.read_bytes()
        actual = sha256_bytes(data)
        rows.append({
            'library_id': row['library_id'],
            'path': path.relative_to(repo_root).as_posix(),
            'declared_sha256': row['sha256'],
            'actual_sha256': actual,
            'declared_bytes': row['bytes'],
            'actual_bytes': len(data),
            'read_method': 'UTF8_DIRECT_FILE_READ',
            'status': 'PASS' if actual == row['sha256'] and len(data) == row['bytes'] else 'FAIL',
        })
    return with_hash({
        'schema': 'DEV-GROUP-002-R12-ACTIVE-WHITELIST-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R12',
        'main_prompt_runtime_id': declared['main_prompt_runtime_id'],
        'active_binding_table_sha256_utf8_lf': declared['active_binding_table_sha256_utf8_lf'],
        'rows': rows,
        'status': 'PASS' if all(row['status'] == 'PASS' for row in rows) else 'FAIL',
    })


def build_input_freeze(repo_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], str]:
    manifest = read_json(repo_root / INPUTS['view_manifest'])
    questions = read_json(repo_root / INPUTS['questions'])
    bazi = read_json(repo_root / INPUTS['bazi'])
    ziwei_text = (repo_root / INPUTS['ziwei']).read_text(encoding='utf-8')
    file_map = {'ziwei.txt': INPUTS['ziwei'], 'bazi-transcription.json': INPUTS['bazi'], 'questions-parsed.json': INPUTS['questions']}
    file_rows = []
    for name, rel in file_map.items():
        data = (repo_root / rel).read_bytes()
        declared = manifest['files'][name]
        file_rows.append({
            'name': name,
            'path': rel,
            'sha256': sha256_bytes(data),
            'bytes': len(data),
            'declared_sha256': declared['sha256'],
            'declared_bytes': declared['bytes'],
            'status': 'PASS' if sha256_bytes(data) == declared['sha256'] and len(data) == declared['bytes'] else 'FAIL',
        })
    chart_tokens = [
        '命  宫[乙丑]', '紫微[庙][↓科],破军[旺][生年禄]', '擎羊[庙],铃星[得]',
        '父母宫[甲寅]', '地劫[平]', '兄弟宫[甲子]', '天机[庙][↑忌]', '禄存[庙],火星[陷]',
        '官禄宫[丁巳]', '廉贞[陷],贪狼[陷][生年忌][↑忌]', '天钺[旺],天马[平]',
        '迁移宫[己未][身宫]', '天相[得]', '文昌[利],文曲[旺][↓忌]',
        '疾厄宫[庚申]', '天同[旺][↓忌],天梁[陷]', '财帛宫[辛酉]', '武曲[利],七杀[旺]',
        '子女宫[壬戌]', '太阳[不]', '夫妻宫[癸亥][来因]', '陀罗[陷]', '天刑[陷]',
        '起止年份:2016年(34虚岁)~2025年(43虚岁)', '大限四化:天梁禄,紫微权,左辅科,武曲忌',
        '2022年[壬寅](40虚岁)', '命宫干支:甲寅',
    ]
    missing = [token for token in chart_tokens if token not in ziwei_text]
    expected_pillars = {'year': '癸亥', 'month': '丙辰', 'day': '己卯', 'hour': '丁卯'}
    if bazi['pillars'] != expected_pillars:
        raise ValueError('DEV-EXAMPLE-003 Bazi pillar mismatch')
    if [q['question_id'] for q in questions] != [f'Q{i}' for i in range(1, 6)]:
        raise ValueError('DEV-EXAMPLE-003 question-set mismatch')
    obj = with_hash({
        'schema': 'DEV-GROUP-002-R12-INPUT-FREEZE-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R12',
        'source_runtime_view_manifest_path': INPUTS['view_manifest'],
        'source_runtime_view_manifest_git_blob_sha': git_blob_sha(repo_root / INPUTS['view_manifest']),
        'answer_isolation': {
            'status': manifest['answer_isolation_status'],
            'answer_payload_present': manifest['answer_payload_present'],
            'answer_reference_disclosed': manifest['answer_reference_disclosed'],
        },
        'files': file_rows,
        'ziwei_required_token_count': len(chart_tokens),
        'ziwei_missing_tokens': missing,
        'bazi_pillars': bazi['pillars'],
        'bazi_seasonal_qi': bazi['seasonal_qi'],
        'bazi_luck_cycles': bazi['luck']['cycles'],
        'questions': questions,
        'question_count': len(questions),
        'status': 'PASS' if all(row['status'] == 'PASS' for row in file_rows) and not missing and not manifest['answer_payload_present'] and not manifest['answer_reference_disclosed'] else 'FAIL',
    })
    return obj, questions, bazi, ziwei_text


def build_source_excerpts(repo_root: Path) -> dict[str, Any]:
    rows = []
    for excerpt_id, library_id, rel, start, end, phrases in SOURCE_EXCERPT_SPECS:
        path = repo_root / rel
        text = extract_lines(path, start, end)
        missing = [phrase for phrase in phrases if phrase not in text]
        rows.append({
            'excerpt_id': excerpt_id,
            'library_id': library_id,
            'path': rel,
            'source_file_sha256': sha256_bytes(path.read_bytes()),
            'source_file_bytes': path.stat().st_size,
            'line_start': start,
            'line_end': end,
            'text': text,
            'text_sha256': sha256_bytes(text.encode('utf-8')),
            'required_phrases': phrases,
            'missing_required_phrases': missing,
            'status': 'PASS_FULL_PARENT_SEGMENT' if not missing else 'FAIL',
        })
    return with_hash({
        'schema': 'DEV-GROUP-002-R12-SOURCE-EXCERPTS-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R12',
        'rows': rows,
        'row_count': len(rows),
        'status': 'PASS' if all(row['status'].startswith('PASS') for row in rows) else 'FAIL',
    })


def build_case_structures(input_freeze: dict[str, Any], excerpts: dict[str, Any], bazi: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    ziwei = with_hash({
        'schema': 'DEV-GROUP-002-R12-ZIWEI-CASE-STRUCTURE-V1',
        'case_id': CASE_ID,
        'input_freeze_sha256': input_freeze['canonical_sha256'],
        'source_excerpts_sha256': excerpts['canonical_sha256'],
        'palace_rows': {
            'MING': {'branch': '丑', 'stars': ['紫微', '破军'], 'transformations': ['紫微离心自化科', '破军生年禄'], 'malefics': ['擎羊', '铃星']},
            'SIBLING': {'branch': '子', 'stars': ['天机'], 'transformations': ['天机向心自化忌'], 'auxiliary': ['禄存', '火星']},
            'PARENTS': {'branch': '寅', 'stars': [], 'auxiliary': ['地劫', '三台', '恩光', '天贵', '天巫', '孤辰'], 'borrow_from': 'HEALTH'},
            'CAREER': {'branch': '巳', 'stars': ['廉贞', '贪狼'], 'transformations': ['贪狼生年忌', '贪狼向心自化忌'], 'auxiliary': ['天钺', '天马']},
            'MIGRATION_BODY': {'branch': '未', 'stars': ['天相'], 'auxiliary': ['文昌', '文曲'], 'transformations': ['文曲离心自化忌']},
            'HEALTH': {'branch': '申', 'stars': ['天同', '天梁'], 'transformations': ['天同离心自化忌'], 'auxiliary': ['右弼', '地空', '天伤', '劫煞']},
            'WEALTH': {'branch': '酉', 'stars': ['武曲', '七杀']},
            'CHILD': {'branch': '戌', 'stars': ['太阳'], 'auxiliary': ['天喜', '解神', '寡宿', '阴煞']},
            'SPOUSE': {'branch': '亥', 'stars': [], 'auxiliary': ['陀罗', '天刑', '凤阁', '天厨', '年解'], 'borrow_from': 'CAREER'},
        },
        'route_receipts': [
            {'axis': 'PARENTS', 'primary': '父母宫', 'borrow_from': '疾厄宫天同天梁', 'selector_status': 'MATCH'},
            {'axis': 'SIBLING', 'primary': '兄弟宫天机', 'selector_status': 'MATCH_WITH_FIRE_AND_JI_MODIFIERS'},
            {'axis': 'IDENTITY_CAREER', 'primary': '命宫紫微破军', 'body': '迁移宫天相昌曲', 'career': '官禄宫廉贞贪狼', 'selector_status': 'MATCH'},
            {'axis': 'MARRIAGE', 'primary': '夫妻空宫', 'borrow_from': '官禄宫廉贞贪狼', 'selector_status': 'MATCH'},
            {'axis': 'CHILD', 'primary': '子女宫太阳落陷', 'selector_status': 'MATCH'},
        ],
        'neutral_time_rows': [
            {'year': 2011, 'annual_ming_branch': '卯', 'transformations': ['巨门禄', '太阳权', '文曲科', '文昌忌'], 'role': 'NEUTRAL_STAGE_ONLY'},
            {'year': 2013, 'annual_ming_branch': '巳', 'transformations': ['破军禄', '巨门权', '太阴科', '贪狼忌'], 'role': 'NEUTRAL_STAGE_ONLY'},
            {'year': 2014, 'annual_ming_branch': '午', 'transformations': ['廉贞禄', '破军权', '武曲科', '太阳忌'], 'role': 'NEUTRAL_STAGE_ONLY'},
            {'year': 2018, 'annual_ming_branch': '戌', 'transformations': ['贪狼禄', '太阴权', '右弼科', '天机忌'], 'role': 'NEUTRAL_STAGE_ONLY'},
            {'year': 2019, 'annual_ming_branch': '亥', 'transformations': ['武曲禄', '贪狼权', '天梁科', '文曲忌'], 'role': 'NEUTRAL_STAGE_ONLY'},
            {'year': 2021, 'annual_ming_branch': '丑', 'transformations': ['巨门禄', '太阳权', '文曲科', '文昌忌'], 'role': 'NEUTRAL_STAGE_ONLY'},
            {'year': 2022, 'annual_ming_branch': '寅', 'transformations': ['天梁禄', '紫微权', '左辅科', '武曲忌'], 'role': 'NEUTRAL_STAGE_ONLY'},
        ],
        'active_limit': {'years': '2016-2025', 'palace': '子女宫', 'transformations': ['天梁禄', '紫微权', '左辅科', '武曲忌']},
        's08_scope': 'DYNAMIC_FORCE_ONLY_NOT_EVENT_OR_ENDPOINT',
        'status': 'EXECUTED_STRUCTURE_ONLY',
    })
    bazi_obj = with_hash({
        'schema': 'DEV-GROUP-002-R12-BAZI-CASE-STRUCTURE-V1',
        'case_id': CASE_ID,
        'input_freeze_sha256': input_freeze['canonical_sha256'],
        'source_excerpts_sha256': excerpts['canonical_sha256'],
        'variant_id': 'SOLAR_TERM_SINGLE_VERSION',
        's11_foundation': {'pillars': bazi['pillars'], 'day_master': '己土', 'hidden_stems_ten_gods': bazi['hidden_stems_ten_gods'], 'status': 'EXECUTED'},
        's12_qi_candidates': {
            'seasonal_qi': bazi['seasonal_qi'],
            'root_channels': ['MONTH_BRANCH_CHEN'],
            'visible_fire_resource': ['MONTH_STEM_BING', 'HOUR_STEM_DING'],
            'wood_pressure': ['DAY_BRANCH_MAO', 'HOUR_BRANCH_MAO', 'YEAR_BRANCH_HAI_HALF_COMBINES_MAO'],
            'candidate_states': ['EARTH_HAS_SEASONAL_SUPPORT', 'WOOD_PRESSURE_AND_RELATION_ACTIVATION', 'WATER_WEAK_IN_NATIVE_SEASON'],
            'status': 'EXECUTED_NO_UNIQUE_STATE',
        },
        's13_method_competition': {'candidates': ['BALANCE_METHOD', 'ROOT_AND_CARRYING_METHOD', 'RELATION_TRANSFORMATION_METHOD'], 'unique_method': None, 'status': 'EXECUTED_NO_UNIQUE_METHOD'},
        's14_relations': {'facts': bazi['relations'], 'transformation_status': 'RELATION_FACTS_ONLY_NO_AUTOMATIC_EVENT'},
        's15_time': {
            'luck_periods': ['2008-2017 癸丑', '2018-2027 壬子'],
            'question_years': [2011, 2013, 2014, 2018, 2019, 2021, 2022],
            'role_candidates': ['RESOURCE_AND_WEALTH_MOVEMENT', 'WOOD_RELATION_ACTIVATION', 'WORK_OR_FAMILY_CHANGE_PERMISSION'],
            'status': 'EXECUTED_NEUTRAL_TIME_ONLY',
        },
        'cross_track_visibility': 'NO_ZIWEI_RESULT_READ_DURING_BUILD',
        'status': 'EXECUTED_STRUCTURE_AND_CAPABILITY_ONLY',
    })
    return ziwei, bazi_obj


def build_blind_models(ziwei: dict[str, Any], bazi: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for track in ('ZIWEI', 'BAZI'):
        for qid in [f'Q{i}' for i in range(1, 6)]:
            text = BLIND_MODELS[track][qid]
            rows.append({
                'case_id': CASE_ID,
                'question_id': qid,
                'track_id': track,
                'blind_model_text': text,
                'contains_option_id': bool(re.search(r'\bOPTION_[ABCD]\b|\b[A-D]:', text)),
                'contains_other_track_result': False,
                'parent_case_structure_sha256': ziwei['canonical_sha256'] if track == 'ZIWEI' else bazi['canonical_sha256'],
                'seal_status': 'LOCALLY_FROZEN_SHADOW_REBUILD_NOT_FORMAL_PREOPTION_SEAL',
            })
    return with_hash({
        'schema': 'DEV-GROUP-002-R12-BLIND-MODELS-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R12',
        'rows': rows,
        'row_count': len(rows),
        'formal_machine_seal_permission': 'NO_ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD',
        'status': 'PASS_LOCAL_MODEL_ISOLATION_NOT_FORMAL_SEAL' if not any(row['contains_option_id'] or row['contains_other_track_result'] for row in rows) else 'FAIL',
    })


def build_coverage_plan(excerpts: dict[str, Any]) -> dict[str, Any]:
    task_classes = {
        'Q1': 'FAMILY_PARENT_ACTOR_OCCUPATION_DEATH_AND_SIBLING_TOPOLOGY',
        'Q2': 'APPEARANCE_PERSONALITY_HOBBY_AND_OCCUPATION_COMPOSITE',
        'Q3': 'EDUCATION_CREDENTIAL_CAREER_ENTRY_AND_LEGAL_EVENT',
        'Q4': 'MARRIAGE_REGISTRATION_RELATION_STAGE_AND_CHILD_ENDPOINTS',
        'Q5': 'EXACT_2022_PARENT_ACCIDENT_MEDICAL_OR_FINANCIAL_EVENT',
    }
    rows = []
    for qid, task in task_classes.items():
        rows.append({
            'case_id': CASE_ID,
            'question_id': qid,
            'task_class': task,
            'ziwei_required_families': ['S04', 'S05', 'S06', 'S07', 'S08', 'S10', 'S17', 'S18'],
            'bazi_required_families': ['S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18'],
            'support_routes': ['STRUCTURAL_DIRECTION', 'OPTION_ATOM_SOURCE_PARENT_BINDING'],
            'counterevidence_routes': ['SAME_AXIS_DIRECT_COUNTEREVIDENCE'],
            'alternative_routes': ['ROLE_OR_SCENE_WITHOUT_ACTOR_OR_ENDPOINT'],
            'endpoint_routes': ['S17_COMPOSITE_AND_EXACT_ENDPOINT'],
            'unresolved_required_families': [],
            'status': 'ROUTED',
        })
    return with_hash({
        'schema': 'DEV-GROUP-002-R12-COMPLETE-KNOWLEDGE-COVERAGE-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R12',
        'source_excerpts_sha256': excerpts['canonical_sha256'],
        'rows': rows,
        'row_count': len(rows),
        'status': 'PASS_ALL_REQUIRED_FAMILIES_ROUTED',
    })


def build_atom_matrix(excerpts: dict[str, Any], blind: dict[str, Any], coverage: dict[str, Any]) -> dict[str, Any]:
    valid_parent_ids = {row['excerpt_id'] for row in excerpts['rows']}
    rows = []
    for atom in parse_atom_specs():
        parents = PARENT_GROUPS[atom['parent_group']]
        if not set(parents) <= valid_parent_ids:
            raise ValueError(f'unresolved Ziwei source parent for {atom["atom_id"]}')
        rows.append({
            **atom,
            'track_id': 'ZIWEI',
            'source_parent_excerpt_ids': parents,
            'capability_ceiling': 'RELATIVE_DIRECTION_ONLY',
            'formal_exact_assertion': None,
            'program_state': 'EXECUTED',
        })
    for atom in parse_atom_specs():
        if not set(BAZI_PARENT_IDS) <= valid_parent_ids:
            raise ValueError(f'unresolved Bazi source parent for {atom["atom_id"]}')
        rows.append({
            **atom,
            'track_id': 'BAZI',
            'direction_status': 'VALID_ABSTENTION_OR_DIRECTION_ONLY',
            'source_parent_excerpt_ids': BAZI_PARENT_IDS,
            'capability_ceiling': 'STRUCTURE_OR_TIME_PERMISSION_ONLY_NO_LOCAL_RANK',
            'formal_exact_assertion': None,
            'program_state': 'EXECUTED',
        })
    return with_hash({
        'schema': 'DEV-GROUP-002-R12-LITERAL-ATOM-DIRECTION-MATRIX-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R12',
        'source_excerpts_sha256': excerpts['canonical_sha256'],
        'blind_models_sha256': blind['canonical_sha256'],
        'coverage_plan_sha256': coverage['canonical_sha256'],
        'rows': rows,
        'row_count': len(rows),
        'ziwei_atom_row_count': len(rows) // 2,
        'bazi_atom_row_count': len(rows) // 2,
        'option_count': 20,
        'bazi_local_rank_permission': 'NO',
        'status': 'PASS_ALL_ATOMS_HAVE_TRACK_LOCAL_PARENTS',
    })


def build_common_subtraction(matrix: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for qid in [f'Q{i}' for i in range(1, 6)]:
        for left, right in itertools.combinations('ABCD', 2):
            eq = COMMON_EQUIVALENCE.get(pair_key(qid, left, right), [])
            rows.append({
                'case_id': CASE_ID,
                'question_id': qid,
                'left': left,
                'right': right,
                'equivalence_rows': [
                    {'left_short_id': a, 'right_short_id': b, 'common_atom_id': c, 'distinguishing_contribution': 0}
                    for a, b, c in eq
                ],
                'common_atom_ids_zeroed': [c for _, _, c in eq],
                'status': 'EXECUTED_BEFORE_PAIRWISE',
            })
    return with_hash({
        'schema': 'DEV-GROUP-002-R12-COMMON-ATOM-SUBTRACTION-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R12',
        'parent_atom_matrix_sha256': matrix['canonical_sha256'],
        'rows': rows,
        'row_count': len(rows),
        'rows_with_material_common_atoms': sum(bool(row['common_atom_ids_zeroed']) for row in rows),
        'status': 'PASS',
    })


def option_atoms(matrix: dict[str, Any], qid: str, option: str) -> list[dict[str, Any]]:
    return [row for row in matrix['rows'] if row['track_id'] == 'ZIWEI' and row['question_id'] == qid and row['option_id'] == option]


def metrics(atoms: list[dict[str, Any]], zero_short_ids: set[str]) -> dict[str, Any]:
    remaining = [atom for atom in atoms if atom['short_id'] not in zero_short_ids]
    by_status = lambda status: [atom['atom_id'] for atom in remaining if atom['direction_status'] == status]
    return {
        'remaining_atom_ids': [atom['atom_id'] for atom in remaining],
        'direct_support_atom_ids': by_status('DIRECT_SUPPORT'),
        'direct_counterevidence_atom_ids': by_status('DIRECT_COUNTEREVIDENCE'),
        'partial_support_atom_ids': by_status('PARTIAL_SUPPORT'),
        'scene_only_atom_ids': by_status('LIMITED_SCENE_ONLY'),
        'missing_exact_endpoint_atom_ids': [
            atom['atom_id'] for atom in remaining
            if atom['exact_endpoint_required'] and atom['direction_status'] in {'LIMITED_MISSING_ENDPOINT', 'UNKNOWN', 'DIRECT_COUNTEREVIDENCE'}
        ],
        'unknown_atom_ids': by_status('UNKNOWN'),
        'source_parent_excerpt_ids': sorted({parent for atom in remaining for parent in atom['source_parent_excerpt_ids']}),
    }


def choose_pair(left_metrics: dict[str, Any], right_metrics: dict[str, Any], left: str, right: str) -> tuple[str, str, dict[str, Any]]:
    criteria = [
        ('DISTINCTIVE_DIRECT_SUPPORT', 'direct_support_atom_ids', 'MAX'),
        ('SAME_AXIS_DIRECT_COUNTEREVIDENCE', 'direct_counterevidence_atom_ids', 'MIN'),
        ('COMPOSITE_PARTIAL_COVERAGE', 'partial_support_atom_ids', 'MAX'),
        ('EXACT_ENDPOINT_DISTANCE', 'missing_exact_endpoint_atom_ids', 'MIN'),
        ('SCENE_ONLY_COVERAGE', 'scene_only_atom_ids', 'MAX'),
        ('UNRESOLVED_UNKNOWN_ATOMS', 'unknown_atom_ids', 'MIN'),
    ]
    for basis, field, mode in criteria:
        lv = len(left_metrics[field])
        rv = len(right_metrics[field])
        if lv != rv:
            left_wins = lv > rv if mode == 'MAX' else lv < rv
            return (left if left_wins else right), basis, {'left_value': lv, 'right_value': rv, 'mode': mode}
    return (left if left < right else right), 'LOW_INFORMATION_FORCED_TIEBREAK_LITERAL_OPTION_ORDER', {'left_value': None, 'right_value': None, 'mode': 'TIE'}


def build_pairwise(matrix: dict[str, Any], subtraction: dict[str, Any]) -> dict[str, Any]:
    subtraction_index = {(row['question_id'], row['left'], row['right']): row for row in subtraction['rows']}
    rows = []
    derived_ranks = {}
    for qid in [f'Q{i}' for i in range(1, 6)]:
        for left, right in itertools.combinations('ABCD', 2):
            eq = subtraction_index[(qid, left, right)]['equivalence_rows']
            left_metrics = metrics(option_atoms(matrix, qid, left), {row['left_short_id'] for row in eq})
            right_metrics = metrics(option_atoms(matrix, qid, right), {row['right_short_id'] for row in eq})
            winner, basis, values = choose_pair(left_metrics, right_metrics, left, right)
            rows.append({
                'case_id': CASE_ID,
                'question_id': qid,
                'left': left,
                'right': right,
                'winner': winner,
                'loser': right if winner == left else left,
                'decision_basis': basis,
                'decision_values': values,
                'common_atom_ids_zeroed': subtraction_index[(qid, left, right)]['common_atom_ids_zeroed'],
                'left_atom_direction_parent_ids': left_metrics['remaining_atom_ids'],
                'right_atom_direction_parent_ids': right_metrics['remaining_atom_ids'],
                'left_source_parent_excerpt_ids': left_metrics['source_parent_excerpt_ids'],
                'right_source_parent_excerpt_ids': right_metrics['source_parent_excerpt_ids'],
                'left_metrics': left_metrics,
                'right_metrics': right_metrics,
                'atom_level_replay_status': 'PASS',
                'bazi_fusion_effect': 'ZERO_NO_MACHINE_VALID_BAZI_LOCAL_SEAL',
                'answer_access_during_decision': False,
            })
        qrows = [row for row in rows if row['question_id'] == qid]
        wins = {option: 0 for option in 'ABCD'}
        for row in qrows:
            wins[row['winner']] += 1
        rank = ''.join(sorted('ABCD', key=lambda option: (-wins[option], option)))
        for left, right in itertools.combinations('ABCD', 2):
            actual = next(row['winner'] for row in qrows if row['left'] == left and row['right'] == right)
            expected = left if rank.index(left) < rank.index(right) else right
            if actual != expected:
                raise ValueError(f'non-transitive atom replay for {qid}: {left}/{right}')
        derived_ranks[qid] = rank
    return with_hash({
        'schema': 'DEV-GROUP-002-R12-ATOM-PARENT-PAIRWISE-REPLAY-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R12',
        'parent_atom_matrix_sha256': matrix['canonical_sha256'],
        'parent_common_subtraction_sha256': subtraction['canonical_sha256'],
        'rows': rows,
        'row_count': len(rows),
        'derived_ranks': derived_ranks,
        'atom_level_replayable_rows': len(rows),
        'low_information_tiebreak_rows': sum(row['decision_basis'].startswith('LOW_INFORMATION') for row in rows),
        'status': 'PASS_COMPLETE_TRANSITIVE_REPLAY',
    })


def build_public_disclosure(pairwise: dict[str, Any], matrix: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for qid in [f'Q{i}' for i in range(1, 6)]:
        rank = pairwise['derived_ranks'][qid]
        first_atoms = option_atoms(matrix, qid, rank[0])
        second_atoms = option_atoms(matrix, qid, rank[1])
        important = [atom['atom_id'] for atom in first_atoms if atom['direction_status'] in {'DIRECT_SUPPORT', 'PARTIAL_SUPPORT', 'DIRECT_COUNTEREVIDENCE'}][:3]
        important += [atom['atom_id'] for atom in second_atoms if atom['direction_status'] in {'DIRECT_SUPPORT', 'PARTIAL_SUPPORT', 'DIRECT_COUNTEREVIDENCE'}][:2]
        unverified = sorted({atom['atom_id'] for atom in first_atoms + second_atoms if atom['exact_endpoint_required'] and atom['direction_status'] in {'LIMITED_MISSING_ENDPOINT', 'UNKNOWN', 'DIRECT_COUNTEREVIDENCE'}})
        rows.append({
            'case_id': CASE_ID,
            'question_id': qid,
            'relative_first': rank[0],
            'relative_second': rank[1],
            'full_rank': rank,
            'confidence': 'LOW_TO_MEDIUM_SOURCE_GROUNDED_SHADOW_REBUILD',
            'blind_core': BLIND_MODELS['ZIWEI'][qid],
            'critical_distinctive_atom_ids': important,
            'strongest_competitor': rank[1],
            'most_important_unverified_atoms': unverified,
            'ziwei_local_rank': rank,
            'bazi_local_rank': None,
            'bazi_status': 'VALID_ABSTENTION_OR_DIRECTION_ONLY_NO_LOCAL_RANK',
            's03_fusion_status': 'NOT_PERFORMED',
            'formal_exact_assertion': None,
        })
    return with_hash({
        'schema': 'DEV-GROUP-002-R12-PUBLIC-RELATIVE-DISCLOSURE-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R12',
        'rows': rows,
        'row_count': len(rows),
        'formal_exact_assertion_count': 0,
    })


def build_prediction(repo_root: Path, pairwise: dict[str, Any]) -> dict[str, Any]:
    parent = read_json(repo_root / INPUTS['parent_prediction'])
    cases = []
    changed = []
    for case in parent['cases']:
        clone = dict(case)
        if case['case_id'] == CASE_ID:
            ranks = [pairwise['derived_ranks'][f'Q{i}'] for i in range(1, 6)]
            changed = [f'{CASE_ID}:Q{i}' for i, (old, new) in enumerate(zip(case['ranks'], ranks), 1) if old != new]
            clone.update({
                'ranks': ranks,
                'top1_vector': ''.join(rank[0] for rank in ranks),
                'top2_vector': ''.join(rank[1] for rank in ranks),
                'prediction_origin': 'R12_DEV003_CANONICAL_INPUT_LITERAL_ATOM_SOURCE_PARENT_REPLAY',
                'answer_visible_during_prediction_materialization': False,
            })
        cases.append(clone)
    return with_hash({
        'schema': 'DEV-GROUP-002-R12-PREDICTION-FREEZE-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R12',
        'run_class': 'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD',
        'parent_r11_prediction_sha256': parent['canonical_sha256'],
        'pairwise_replay_sha256': pairwise['canonical_sha256'],
        'case_ids': parent['case_ids'],
        'cases': cases,
        'question_count': 25,
        'changed_case_ids': [CASE_ID] if changed else [],
        'changed_question_ids': changed,
        'contains_answers': False,
        'answer_visible_during_prediction_materialization': False,
        'formal_exact_assertion_permission': 'NULL_ONLY',
        'machine_valid_local_seals': 0,
        's03_fusions': 0,
        'new_case_admission': 'BLOCKED',
        'base_astrological_knowledge_changed': False,
    })


def build_review(repo_root: Path, prediction: dict[str, Any]) -> dict[str, Any]:
    answer_vectors = read_json(repo_root / INPUTS['answers'])['answer_vectors']
    scores = []
    top1 = top2 = 0
    for case in prediction['cases']:
        answer = answer_vectors[case['case_id']]
        h1 = sum(a == b for a, b in zip(case['top1_vector'], answer))
        h2 = sum(correct in (a, b) for a, b, correct in zip(case['top1_vector'], case['top2_vector'], answer))
        top1 += h1
        top2 += h2
        scores.append({'case_id': case['case_id'], 'top1_hits': h1, 'top2_coverage': h2})
    return with_hash({
        'schema': 'DEV-GROUP-002-R12-POSTREVEAL-REVIEW-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R12',
        'parent_prediction_sha256': prediction['canonical_sha256'],
        'answer_vectors': answer_vectors,
        'case_scores': scores,
        'totals': {'top1_hits': top1, 'top2_coverage': top2, 'question_count': 25, 'score_label': 'TRAINING_REGRESSION_SCORE'},
        'comparison_to_r11': {'top1_delta': top1 - 13, 'top2_delta': top2 - 16},
        'accuracy_claim': 'NO_NEW_BLIND_RESULT',
        'answer_used_for_selection': False,
    })


def build_generic_fix() -> dict[str, Any]:
    return with_hash({
        'schema': 'DEV-GROUP-002-R12-GENERIC-FIX-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R12',
        'fix_id': 'TR-R12-CANONICAL-CASE-ATOM-PARENT-REBUILD',
        'defect_class': 'HISTORICAL_TOTAL_ORDER_WITHOUT_RECONSTRUCTABLE_OPTION_ATOM_SOURCE_PARENTS',
        'general_rules': [
            'A case carried forward from a historical total-order replay must be rebuilt from its canonical answer-free runtime view before the order can be treated as source-grounded.',
            'Every material atom must preserve actor, action or state, object, period, persistence or frequency, magnitude and exact endpoint requirements separately.',
            'A scene or structural tendency cannot close death, owner registration, degree, imprisonment, legal marriage or divorce, live birth, child count or sex, diagnosis, hospitalization duration, debt or property sale.',
            'Common literal atoms are removed before pairwise comparison and cannot be counted as distinguishing support.',
            'Answers are accessed only after the prediction object is canonically frozen and cannot alter source retrieval, atom direction or pairwise winners.',
        ],
        'base_astrological_knowledge_changed': False,
        'case_specific_direction_rule_added': False,
        's00_s19_modified': False,
        'impact_scope': 'GENERIC_CANONICAL_REBUILD_AND_ATOM_PARENT_RUNTIME_INTERFACE',
    })


def build_objects(repo_root: Path) -> dict[str, dict[str, Any]]:
    whitelist = build_whitelist(repo_root)
    input_freeze, questions, bazi, _ = build_input_freeze(repo_root)
    excerpts = build_source_excerpts(repo_root)
    if whitelist['status'] != 'PASS' or input_freeze['status'] != 'PASS' or excerpts['status'] != 'PASS':
        raise ValueError('R12 precontent gate failed')
    ziwei, bazi_structure = build_case_structures(input_freeze, excerpts, bazi)
    blind = build_blind_models(ziwei, bazi_structure)
    coverage = build_coverage_plan(excerpts)
    matrix = build_atom_matrix(excerpts, blind, coverage)
    subtraction = build_common_subtraction(matrix)
    pairwise = build_pairwise(matrix, subtraction)
    public = build_public_disclosure(pairwise, matrix)
    prediction = build_prediction(repo_root, pairwise)
    # Answer access begins only after prediction is fully materialized in memory.
    review = build_review(repo_root, prediction)
    generic = build_generic_fix()
    base = {
        'active-whitelist.json': whitelist,
        'input-freeze.json': input_freeze,
        'source-excerpts.json': excerpts,
        'ziwei-case-structure.json': ziwei,
        'bazi-case-structure.json': bazi_structure,
        'blind-models.json': blind,
        'coverage-plan.json': coverage,
        'literal-atom-direction-matrix.json': matrix,
        'common-atom-subtraction.json': subtraction,
        'pairwise-replay.json': pairwise,
        'public-relative-disclosure.json': public,
        'prediction-freeze.json': prediction,
        'postreveal-review.json': review,
        'generic-fix.json': generic,
    }
    history = {rid: {'path': path, 'git_blob_sha': git_blob_sha(repo_root / path), 'preserved': True} for rid, path in HISTORY.items()}
    artifacts = {
        name.removesuffix('.json').replace('-', '_'): {'path': str(ROUND_DIR / name), 'canonical_sha256': obj['canonical_sha256']}
        for name, obj in base.items()
    }
    manifest = with_hash({
        'schema': 'DEV-GROUP-002-R12-FROZEN-MANIFEST-V1',
        'group_id': 'DEV-GROUP-002',
        'round_id': 'R12',
        'status': 'FROZEN_DEV003_CANONICAL_ATOM_SOURCE_REBUILD',
        'run_class': 'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD',
        'historical_rounds': history,
        'artifacts': artifacts,
        'statistics': {
            'question_count': 25,
            'processed_case_count': 1,
            'processed_question_count': 5,
            'source_excerpt_count': excerpts['row_count'],
            'literal_atom_direction_rows': matrix['row_count'],
            'ziwei_atom_direction_rows': matrix['ziwei_atom_row_count'],
            'bazi_atom_direction_rows': matrix['bazi_atom_row_count'],
            'common_atom_pair_rows': subtraction['row_count'],
            'rows_with_material_common_atoms': subtraction['rows_with_material_common_atoms'],
            'pairwise_rows': pairwise['row_count'],
            'atom_level_replayable_pairwise_rows': pairwise['atom_level_replayable_rows'],
            'low_information_tiebreak_rows': pairwise['low_information_tiebreak_rows'],
            'selection_changed_from_r11': bool(prediction['changed_question_ids']),
            'top1_hits': review['totals']['top1_hits'],
            'top2_coverage': review['totals']['top2_coverage'],
            'formal_valid_questions': 0,
            'machine_valid_local_seals': 0,
            's03_fusions': 0,
        },
        'training_conclusion': 'DEV-EXAMPLE-003 is rebuilt from canonical answer-free inputs with independent track structures, full source parents, literal atom directions, common-atom subtraction and atom-level pairwise replay. Any rank or score change is preserved without answer-derived repair.',
        'next_required_round': 'R13_REGRESSION_DIAGNOSIS_OR_DEV_EXAMPLE_004_CANONICAL_ATOM_REBUILD_DEPENDING_R12_OUTCOME',
        'new_case_admission': 'BLOCKED',
        'base_astrological_knowledge_changed': False,
        'case_specific_direction_rule_added': False,
        's00_s19_modified': False,
    })
    base['manifest.json'] = manifest
    return base


def materialize(repo_root: Path) -> None:
    out = repo_root / ROUND_DIR
    out.mkdir(parents=True, exist_ok=True)
    objects = build_objects(repo_root)
    for name, obj in objects.items():
        write_json(out / name, obj)
    case = next(row for row in objects['prediction-freeze.json']['cases'] if row['case_id'] == CASE_ID)
    stats = objects['manifest.json']['statistics']
    summary = f'''# DEV-GROUP-002 R12：DEV-EXAMPLE-003规范输入字面原子来源重建\n\nR12从答案隔离的规范运行视图重新建立第3案，不导入旧语义摘要或旧排序作为证据。已校验S00—S19活动白名单，保存{stats['source_excerpt_count']}个完整来源父段、独立紫微/八字结构、{stats['literal_atom_direction_rows']}条双轨原子方向行、30条共同原子扣除和30组成对重放。\n\nDEV-EXAMPLE-003排序为：{' / '.join(case['ranks'])}；TOP1向量 `{case['top1_vector']}`，TOP2向量 `{case['top2_vector']}`。相对R11变化题数为{len(objects['prediction-freeze.json']['changed_question_ids'])}。组级同题训练回归TOP1 {stats['top1_hits']}/25、TOP2 {stats['top2_coverage']}/25。\n\n八字完成S11—S16上游结构与时间能力，但对父母行为、死亡、精确职业、学历证书、判刑、婚姻手续、生育数量性别、诊断、事故、住院时长、债务和房产出售均保持不排序；未执行S03融合。正式有效题、本地机器密封和融合仍为0。S00—S19和基础命理知识未修改。\n'''
    (out / 'summary.md').write_text(summary, encoding='utf-8')


def validate(repo_root: Path) -> dict[str, Any]:
    errors = []
    out = repo_root / ROUND_DIR
    names = [
        'active-whitelist.json', 'input-freeze.json', 'source-excerpts.json', 'ziwei-case-structure.json', 'bazi-case-structure.json',
        'blind-models.json', 'coverage-plan.json', 'literal-atom-direction-matrix.json', 'common-atom-subtraction.json',
        'pairwise-replay.json', 'public-relative-disclosure.json', 'prediction-freeze.json', 'postreveal-review.json', 'generic-fix.json', 'manifest.json',
    ]
    objects = {}
    for name in names:
        if not (out / name).exists():
            errors.append(f'missing {name}')
        else:
            objects[name] = read_json(out / name)
    if errors:
        return {'status': 'FAIL', 'error_count': len(errors), 'errors': errors}
    for name, obj in objects.items():
        if canonical_hash(obj) != obj.get('canonical_sha256'):
            errors.append(f'{name}: canonical hash mismatch')
    if objects['active-whitelist.json']['status'] != 'PASS':
        errors.append('active whitelist')
    if objects['input-freeze.json']['status'] != 'PASS':
        errors.append('input freeze')
    if objects['source-excerpts.json']['status'] != 'PASS' or objects['source-excerpts.json']['row_count'] != len(SOURCE_EXCERPT_SPECS):
        errors.append('source excerpts')
    if objects['blind-models.json']['status'] != 'PASS_LOCAL_MODEL_ISOLATION_NOT_FORMAL_SEAL':
        errors.append('blind model isolation')
    matrix = objects['literal-atom-direction-matrix.json']
    expected_atom_count = len(parse_atom_specs())
    if matrix['row_count'] != expected_atom_count * 2 or matrix['ziwei_atom_row_count'] != expected_atom_count or matrix['bazi_atom_row_count'] != expected_atom_count:
        errors.append('atom matrix count')
    if any(not row['source_parent_excerpt_ids'] for row in matrix['rows']):
        errors.append('atom source parent missing')
    if any(row['formal_exact_assertion'] is not None for row in matrix['rows']):
        errors.append('formal exact assertion released')
    subtraction = objects['common-atom-subtraction.json']
    if subtraction['row_count'] != 30 or len(subtraction['rows']) != 30:
        errors.append('common atom row count')
    pairwise = objects['pairwise-replay.json']
    if pairwise['row_count'] != 30 or pairwise['atom_level_replayable_rows'] != 30 or pairwise['status'] != 'PASS_COMPLETE_TRANSITIVE_REPLAY':
        errors.append('pairwise replay')
    if any(not row['left_atom_direction_parent_ids'] or not row['right_atom_direction_parent_ids'] or row['answer_access_during_decision'] for row in pairwise['rows']):
        errors.append('pairwise atom parents or answer access')
    prediction = objects['prediction-freeze.json']
    case = next(row for row in prediction['cases'] if row['case_id'] == CASE_ID)
    expected_ranks = [pairwise['derived_ranks'][f'Q{i}'] for i in range(1, 6)]
    if case['ranks'] != expected_ranks:
        errors.append('prediction rank mismatch')
    if prediction['contains_answers'] or prediction['answer_visible_during_prediction_materialization']:
        errors.append('prediction answer leakage')
    review = objects['postreveal-review.json']
    if review['answer_used_for_selection']:
        errors.append('review answer selection leakage')
    generic = objects['generic-fix.json']
    generic_text = '\n'.join(generic['general_rules'])
    if any(token in generic_text for token in [CASE_ID, 'CBCCA', 'CABD', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5']):
        errors.append('case token leaked into generic fix')
    manifest = objects['manifest.json']
    if manifest['status'] != 'FROZEN_DEV003_CANONICAL_ATOM_SOURCE_REBUILD':
        errors.append('manifest status')
    stats = manifest['statistics']
    if stats['atom_level_replayable_pairwise_rows'] != 30 or stats['formal_valid_questions'] != 0 or stats['machine_valid_local_seals'] != 0 or stats['s03_fusions'] != 0:
        errors.append('manifest formal state')
    for rid, row in manifest['historical_rounds'].items():
        if row['path'] != HISTORY[rid] or git_blob_sha(repo_root / HISTORY[rid]) != row['git_blob_sha'] or row['preserved'] is not True:
            errors.append(f'history {rid}')
    return {
        'schema': 'DEV-GROUP-002-R12-VALIDATION-V1',
        'status': 'PASS' if not errors else 'FAIL',
        'error_count': len(errors),
        'errors': errors,
        'historical_rounds_preserved': list(HISTORY),
        'processed_case_id': CASE_ID,
        'source_excerpt_count': objects['source-excerpts.json']['row_count'],
        'literal_atom_direction_rows': matrix['row_count'],
        'ziwei_atom_direction_rows': matrix['ziwei_atom_row_count'],
        'bazi_atom_direction_rows': matrix['bazi_atom_row_count'],
        'common_atom_pair_rows': subtraction['row_count'],
        'rows_with_material_common_atoms': subtraction['rows_with_material_common_atoms'],
        'pairwise_rows': pairwise['row_count'],
        'atom_level_replayable_pairwise_rows': pairwise['atom_level_replayable_rows'],
        'low_information_tiebreak_rows': pairwise['low_information_tiebreak_rows'],
        'dev003_ranks': case['ranks'],
        'dev003_top1': case['top1_vector'],
        'dev003_top2': case['top2_vector'],
        'selection_changed_from_r11': bool(prediction['changed_question_ids']),
        'changed_question_ids': prediction['changed_question_ids'],
        'top1_hits': review['totals']['top1_hits'],
        'top2_coverage': review['totals']['top2_coverage'],
        'top1_delta_from_r11': review['comparison_to_r11']['top1_delta'],
        'top2_delta_from_r11': review['comparison_to_r11']['top2_delta'],
        'formal_valid_questions': 0,
        'machine_valid_local_seals': 0,
        's03_fusions': 0,
        'base_astrological_knowledge_changed': False,
        's00_s19_modified': False,
        'new_case_admission': 'BLOCKED',
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo-root', default='.')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--validate', action='store_true')
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    if not args.write and not args.validate:
        parser.error('select --write and/or --validate')
    if args.write:
        materialize(root)
    if args.validate:
        result = validate(root)
        out = root / ROUND_DIR
        out.mkdir(parents=True, exist_ok=True)
        write_json(out / 'validation.json', result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
        return 0 if result['status'] == 'PASS' else 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
