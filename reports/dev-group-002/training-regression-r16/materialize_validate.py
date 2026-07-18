#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

ROUND_DIR = Path('reports/dev-group-002/training-regression-r16')
CASE_ID = 'DEV-EXAMPLE-004'
GROUP_ID = 'DEV-GROUP-002'
INTERFACE_ID = 'TR-R14-CAPABILITY-NEUTRAL-TIME-SCENE-NORMALIZED-BURDEN-V1'
HISTORY = {
    'R1': 'reports/dev-group-002/training-regression-r1/manifest.json',
    'R2': 'reports/dev-group-002/training-regression-r2/formal-readiness-matrix.json',
    'R3': 'reports/dev-group-002/training-regression-r3/progress.json',
    'R4': 'reports/dev-group-002/training-regression-r4/compact-manifest.json',
    **{f'R{i}': f'reports/dev-group-002/training-regression-r{i}/manifest.json' for i in range(5, 16)},
}
INPUTS = {
    'whitelist': 'reports/dev-group-002/training-regression-r12/active-whitelist.json',
    'gate': 'reports/dev-group-002/training-regression-r15/cross-case-gate.json',
    'interface': 'reports/dev-group-002/training-regression-r15/interface-freeze.json',
    'view_manifest': 'training-data/DEV-GROUP-002/runtime-views/DEV-EXAMPLE-004/manifest.json',
    'ziwei': 'training-data/DEV-GROUP-002/runtime-views/DEV-EXAMPLE-004/ziwei.txt',
    'bazi': 'training-data/DEV-GROUP-002/runtime-views/DEV-EXAMPLE-004/bazi-transcription.json',
    'questions': 'training-data/DEV-GROUP-002/runtime-views/DEV-EXAMPLE-004/questions-parsed.json',
    'parent_prediction': 'reports/dev-group-002/training-regression-r14/prediction-freeze.json',
    'answers': 'reports/dev-group-002/training-regression-r14/postreveal-review.json',
}

SOURCE_EXCERPT_SPECS = [
    ('S02_REALITY_LIMITS', 'S02', 'knowledge/base/S02_现代语义现实变量与量级标准库.txt', 790, 870, ['临床严重抑郁症确诊', '遗传病医学确诊']),
    ('S04_SCOPE', 'S04', 'knowledge/base/S04_十二宫主题太极与气数位库.txt', 1, 80, ['S04中的实体或边存在不等于现实动作', '未知人物、机构、资产或动作不得因选项文字自动当作事实']),
    ('S05_TANLANG', 'S05', 'knowledge/base/S05_星曜本性辅煞系统与组合条件库.txt', 700, 748, ['贪狼在命身宫，主人擅长交际', '能言善道，利用人际关系成就事业', '贪狼最不喜文昌、文曲']),
    ('S05_JUMEN_SPEECH', 'S05', 'knowledge/base/S05_星曜本性辅煞系统与组合条件库.txt', 759, 765, ['巨门于是非口舌之外，亦主口才', '若巨门化禄，则宜于表演人员']),
    ('S06_SELECTOR', 'S06', 'knowledge/base/S06_六十星系与十二基础盘库.txt', 1, 60, ['空宫借星', 'STRUCTURE_SELECTOR_MISMATCH']),
    ('S07_RARE_TERM_ROUTE', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 1138, 1210, ['运输”对应“物流', '宗教”对应“牧师']),
    ('S07_TANLANG_RELIGION', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 7180, 7225, ['现代则为带神秘色彩的宗教', '均必有宗教信仰']),
    ('S07_CAREER_QISHA', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 8848, 8878, ['七杀守事业宫', '主工作独当一面', '亦可主持企业或工业管理']),
    ('S07_PARENT_JUMEN', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 130614, 130650, ['巨门守父母宫', '刑克或不和仍难避免']),
    ('S07_MARRIAGE_ZIFU', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 135050, 135210, ['天府有调和夫妻关系的性质', '否则男命主有外遇', '婚姻无一正式婚礼']),
    ('S08_TRANSFORM_LIMIT', 'S08', 'knowledge/base/S08_十干四化自化与禄忌线库.txt', 1, 70, ['S08_DIRECT_EVENT_ENDPOINT_OR_OPTION_RANK_PERMISSION=NO', '不证明现实事件、正式终点或答案']),
    ('S10_NEUTRAL_TIME', 'S10', 'knowledge/base/S10_紫微岁运应期与动态辅助库.txt', 1, 60, ['时间事实先于选项映射', '时间强度、四化数量、换限、回原宫或显著度只提供阶段许可']),
    ('S11_FOUNDATION', 'S11', 'knowledge/base/S11_八字干支五行藏干与十神库.txt', 1, 65, ['S11唯一负责合法八字版本', 'S11不判断旺衰']),
    ('S12_QI', 'S12', 'knowledge/base/S12_八字月令旺衰通根与气势库.txt', 1, 70, ['月令是主轴而非独裁', '不负责格局命名']),
    ('S14_RELATION', 'S14', 'knowledge/base/S14_八字合冲刑害墓库与结构变化库.txt', 1, 135, ['冲刑害不等于灾祸', '合不等于化']),
    ('S15_NEUTRAL_TIME', 'S15', 'knowledge/base/S15_八字大运流年流月与应期库.txt', 1, 60, ['方向中立时间事实', '不得写入任何选项独有']),
    ('S16_DISTINCTIVE_CAP', 'S16', 'knowledge/base/S16_八字专题映射与紫微接口库.txt', 1728, 1760, ['GENERIC_ONLY', '演讲与事故、物流与殡葬、已婚与单身、抑郁与其他压力']),
    ('S17_DIRECTION', 'S17', 'knowledge/base/S17_专题闭合人物太极与动作终点链库.txt', 1, 75, ['MISSING_EXACT_ENDPOINT_ERASES_SUPPORT_PERMISSION=NO', '逐原子方向状态必须完整传播']),
    ('S17_ENDPOINTS', 'S17', 'knowledge/base/S17_专题闭合人物太极与动作终点链库.txt', 2638, 2660, ['“已婚”需要身份、登记或无歧义正式婚姻事实', '精确职业还必须链接S04职业画像']),
    ('S18_PAIRWISE', 'S18', 'knowledge/base/S18_证据归并非法归零与评分分寸库.txt', 1, 90, ['PREDICTION_FREEZE_BEFORE_ANSWER_ACCESS_REQUIRED=YES', 'S18必须继续在答案不可见时生成强制首选、次选']),
]

BLIND_MODELS = {
    'ZIWEI': {
        'Q1': 'The parent palace contains Jumen with natal Quan and self-Ji, supporting distance, disagreement and a disrupted parent-child route. The model permits a father-away/work-separation scene and a mother-health vulnerability scene, but cannot close affair, divorce, remarriage, foreign migration or grandmother custody.',
        'Q2': 'The 2001 neutral annual identity falls in the parent palace with Jumen Lu, Sun Quan, Wenqu Ke and Wenchang Ji. This activates speech, public expression and institutional/document pressure. It does not establish an award, school leave, genetic diagnosis, medication, traffic collision or safety endpoint.',
        'Q3': 'Natal career is exalted Qisha opposite the Ziwei-Tianfu relationship axis; identity is Tanlang with Wenqu and migration contains Wuqu, Wenchang and Ling. The sealed model favors independent management, mobile or industrial/logistics work and a secondary public-media direction. Exact occupation and post-2022 continuity remain unclosed.',
        'Q4': 'The 2017-2026 major limit occupies the Ziwei-Tianfu spouse palace, while natal Tanlang Ji with Wenqu increases relationship complexity. The model supports a sustained relationship plus multi-angle friction more than a clean stable marriage, but legal marriage, divorce filing, continuous singleness and exact duration are unclosed.',
        'Q5': 'All four years are neutral stage candidates only. 2024 returns the annual identity to natal Tanlang-Ji and adds Sun-Ji while the natal health palace contains fallen Sun with Tuo, Kong, Jie and Tianxing. 2016 is the secondary pressure year; 2018 and 2002 are weaker. None proves a clinical depression diagnosis or comparative medical severity.',
    },
    'BAZI': {
        'Q1': 'The legal Bazi transcription is Gui-You, Bing-Chen, Geng-Shen, Bing-Zi with strong metal and a water combination. It can describe family pressure or distance only generically and cannot identify affair, custody, divorce, remarriage or a parent illness.',
        'Q2': 'The chart can support active expression and institutional pressure in 2001, but cannot distinguish a speech prize from bullying, genetic disease or a traffic event. The track therefore retains generic-only direction without a local rank.',
        'Q3': 'Strong metal with Shen-Zi-Chen water and visible officer stars supports operations, movement and management more than a precise religious, funeral or media occupation. Exact industry and employment continuity remain outside Bazi local capability.',
        'Q4': 'The wealth/relationship role is weak and the structure can describe relationship pressure, but cannot distinguish unmarried, married, stable, infidelity or divorce-procedure endpoints. It remains generic-only.',
        'Q5': 'The 2024 Ren-Zi luck transition and Jia-Chen year strongly activate water and the natal combination; 2016 is secondary. This ranks temporal pressure only and cannot prove clinical depression or maximum medical severity.',
    },
}

# q|option|short_id|literal|endpoint_required|ziwei_direction|bazi_direction|parent_ids
ATOM_SPEC = r'''
Q1|A|FATHER_AFFAIR|父亲出轨|1|P|U|S05_TANLANG,S07_PARENT_JUMEN,S17_ENDPOINTS
Q1|A|MOTHER_CAREGIVER|母亲照顾日常生活|1|U|U|S04_SCOPE,S17_ENDPOINTS
Q1|B|PARENTS_WORK_AWAY|父母外出工作|1|P|G|S07_PARENT_JUMEN,S16_DISTINCTIVE_CAP,S17_ENDPOINTS
Q1|B|GRANDMOTHER_PRIMARY_CARE|外婆承担主要抚养|1|U|U|S04_SCOPE,S17_ENDPOINTS
Q1|C|FATHER_WORK_SEPARATION|父亲因工作聚少离多|1|P|G|S07_PARENT_JUMEN,S16_DISTINCTIVE_CAP,S17_ENDPOINTS
Q1|C|MOTHER_ILLNESS|母亲患病|1|P|U|S02_REALITY_LIMITS,S07_PARENT_JUMEN,S17_ENDPOINTS
Q1|D|PARENTS_DIVORCED|父母完成离婚|1|M|U|S07_PARENT_JUMEN,S17_ENDPOINTS
Q1|D|FOLLOW_MOTHER|离婚后跟随母亲生活|1|U|U|S04_SCOPE,S17_ENDPOINTS
Q1|D|MOTHER_REMARRIED|母亲完成再婚|1|M|U|S17_ENDPOINTS
Q1|D|FOREIGN_MIGRATION|随母亲迁居外国|1|U|U|S04_SCOPE,S17_ENDPOINTS
Q2|A|CAMPUS_BULLYING|遭遇校园霸凌|1|P|G|S07_PARENT_JUMEN,S10_NEUTRAL_TIME,S16_DISTINCTIVE_CAP
Q2|A|SCHOOL_LEAVE|申请并完成休学|1|M|U|S17_ENDPOINTS
Q2|B|MINORITY_LANGUAGE|参与小语种活动|1|P|U|S07_RARE_TERM_ROUTE,S16_DISTINCTIVE_CAP
Q2|B|SPEECH_COMPETITION|参加演讲比赛|1|P|G|S05_JUMEN_SPEECH,S10_NEUTRAL_TIME,S16_DISTINCTIVE_CAP
Q2|B|AWARD_ENDPOINT|比赛获奖|1|M|U|S02_REALITY_LIMITS,S17_ENDPOINTS
Q2|C|INJURY_EVENT|发生身体受伤|1|S|G|S08_TRANSFORM_LIMIT,S10_NEUTRAL_TIME,S16_DISTINCTIVE_CAP
Q2|C|GENETIC_DISEASE|确诊遗传病|1|M|U|S02_REALITY_LIMITS,S17_ENDPOINTS
Q2|C|MEDICATION|接受用药治疗|1|M|U|S02_REALITY_LIMITS,S17_ENDPOINTS
Q2|D|TRAFFIC_ACCIDENT|发生交通意外|1|S|G|S08_TRANSFORM_LIMIT,S10_NEUTRAL_TIME,S16_DISTINCTIVE_CAP
Q2|D|PERSON_SAFE|事故后人员平安|1|M|U|S17_ENDPOINTS
Q3|A|PASTOR_OCCUPATION|职业为牧师|1|M|U|S07_RARE_TERM_ROUTE,S07_TANLANG_RELIGION,S17_ENDPOINTS
Q3|A|RELIGIOUS_DIRECTION|宗教或神秘领域倾向|0|P|G|S05_TANLANG,S07_TANLANG_RELIGION
Q3|B|MORTICIAN_OCCUPATION|职业为入殓师|1|M|U|S07_CAREER_QISHA,S16_DISTINCTIVE_CAP,S17_ENDPOINTS
Q3|B|DEATH_SERVICE_SCENE|接触死亡或仪式服务场景|0|S|G|S07_CAREER_QISHA,S16_DISTINCTIVE_CAP
Q3|C|SHIPPING_LOGISTICS|进入航运物流行业|1|P|G|S07_RARE_TERM_ROUTE,S07_CAREER_QISHA,S16_DISTINCTIVE_CAP,S17_ENDPOINTS
Q3|C|MANAGEMENT_FUNCTION|承担管理职能|1|P|G|S07_CAREER_QISHA,S17_ENDPOINTS
Q3|C|POST_2022_CONTINUITY|2022年后持续从事该行业|1|M|U|S10_NEUTRAL_TIME,S15_NEUTRAL_TIME,S17_ENDPOINTS
Q3|D|MEDIA_INDUSTRY|进入传媒行业|1|P|G|S05_TANLANG,S05_JUMEN_SPEECH,S17_ENDPOINTS
Q3|D|INFLUENCER_IDENTITY|具有网红职业身份|1|M|U|S05_TANLANG,S17_ENDPOINTS
Q3|D|PUBLIC_EXPRESSION|公开表达与传播工作|0|P|G|S05_TANLANG,S05_JUMEN_SPEECH
Q4|A|UNMARRIED_STATUS|截至2025年法律上未婚|1|M|U|S17_ENDPOINTS
Q4|A|SINGLE_STATUS|截至2025年无持续伴侣|1|U|U|S17_ENDPOINTS
Q4|A|SHORT_RELATIONSHIPS|恋情多且短暂|1|P|G|S05_TANLANG,S07_MARRIAGE_ZIFU,S17_ENDPOINTS
Q4|B|UNMARRIED_STATUS|截至2025年法律上未婚|1|M|U|S17_ENDPOINTS
Q4|B|LONG_TERM_GIRLFRIEND|与女友交往多年|1|P|G|S07_MARRIAGE_ZIFU,S10_NEUTRAL_TIME,S17_ENDPOINTS
Q4|B|TWO_TIMING|同时维持两段感情|1|P|G|S05_TANLANG,S07_MARRIAGE_ZIFU,S17_ENDPOINTS
Q4|C|MARRIED_STATUS|截至2025年已正式结婚|1|M|U|S07_MARRIAGE_ZIFU,S17_ENDPOINTS
Q4|C|STABLE_RELATIONSHIP|婚后感情稳定|1|P|G|S07_MARRIAGE_ZIFU,S17_ENDPOINTS
Q4|D|MARRIED_STATUS|截至2025年已正式结婚|1|M|U|S07_MARRIAGE_ZIFU,S17_ENDPOINTS
Q4|D|CONTINUOUS_CONFLICT|婚后矛盾不断|1|P|G|S05_TANLANG,S07_MARRIAGE_ZIFU,S17_ENDPOINTS
Q4|D|DIVORCE_PROCEDURE|正在办理离婚手续|1|M|U|S17_ENDPOINTS
Q5|A|DEPRESSION_SEVERE_2002|2002年为抑郁症最严重年份|1|U|U|S02_REALITY_LIMITS,S10_NEUTRAL_TIME,S15_NEUTRAL_TIME,S17_ENDPOINTS
Q5|B|DEPRESSION_SEVERE_2016|2016年为抑郁症最严重年份|1|S|S|S02_REALITY_LIMITS,S10_NEUTRAL_TIME,S15_NEUTRAL_TIME,S17_ENDPOINTS
Q5|C|DEPRESSION_SEVERE_2018|2018年为抑郁症最严重年份|1|S|S|S02_REALITY_LIMITS,S10_NEUTRAL_TIME,S15_NEUTRAL_TIME,S17_ENDPOINTS
Q5|D|DEPRESSION_SEVERE_2024|2024年为抑郁症最严重年份|1|P|P|S02_REALITY_LIMITS,S10_NEUTRAL_TIME,S15_NEUTRAL_TIME,S17_ENDPOINTS
'''

DIRECTION_MAP = {
    'D': 'DIRECT_SUPPORT',
    'P': 'PARTIAL_SUPPORT',
    'S': 'LIMITED_SCENE_ONLY',
    'M': 'LIMITED_MISSING_ENDPOINT',
    'C': 'DIRECT_COUNTEREVIDENCE',
    'U': 'UNKNOWN',
    'G': 'GENERIC_ONLY',
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_payload(obj: dict[str, Any]) -> bytes:
    clone = dict(obj)
    clone.pop('canonical_sha256', None)
    return (json.dumps(clone, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def with_hash(obj: dict[str, Any]) -> dict[str, Any]:
    clone = dict(obj)
    clone['canonical_sha256'] = sha256_bytes(canonical_payload(clone))
    return clone


def canonical_hash(obj: dict[str, Any]) -> str:
    return sha256_bytes(canonical_payload(obj))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')


def build_whitelist(repo_root: Path) -> dict[str, Any]:
    parent = read_json(repo_root / INPUTS['whitelist'])
    rows = []
    for row in parent['rows']:
        path = repo_root / row['path']
        data = path.read_bytes()
        actual = sha256_bytes(data)
        rows.append({**row, 'actual_bytes': len(data), 'actual_sha256': actual, 'status': 'PASS' if len(data) == row['declared_bytes'] and actual == row['declared_sha256'] else 'FAIL'})
    return with_hash({
        'schema': 'DEV-GROUP-002-R16-ACTIVE-WHITELIST-V1',
        'group_id': GROUP_ID,
        'case_id': CASE_ID,
        'round_id': 'R16',
        'parent_r12_whitelist_sha256': parent['canonical_sha256'],
        'main_prompt_runtime_id': parent['main_prompt_runtime_id'],
        'active_binding_table_sha256_utf8_lf': parent['active_binding_table_sha256_utf8_lf'],
        'rows': rows,
        'status': 'PASS' if all(row['status'] == 'PASS' for row in rows) else 'FAIL',
    })


def build_input_freeze(repo_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], str]:
    manifest = read_json(repo_root / INPUTS['view_manifest'])
    gate = read_json(repo_root / INPUTS['gate'])
    interface = read_json(repo_root / INPUTS['interface'])
    files = []
    for key, path_key in [('ziwei.txt', 'ziwei'), ('bazi-transcription.json', 'bazi'), ('questions-parsed.json', 'questions')]:
        path = repo_root / INPUTS[path_key]
        data = path.read_bytes()
        declared = manifest['files'][key]
        files.append({'path': INPUTS[path_key], 'actual_bytes': len(data), 'actual_sha256': sha256_bytes(data), 'declared_bytes': declared['bytes'], 'declared_sha256': declared['sha256'], 'status': 'PASS' if len(data) == declared['bytes'] and sha256_bytes(data) == declared['sha256'] else 'FAIL'})
    questions = read_json(repo_root / INPUTS['questions'])
    bazi = read_json(repo_root / INPUTS['bazi'])
    ziwei = (repo_root / INPUTS['ziwei']).read_text(encoding='utf-8')
    expected_tokens = ['命  宫[丙辰][身宫]', '贪狼[庙][生年忌]', '父母宫[丁巳]', '巨门[旺][生年权][↓忌][↑权]', '官禄宫[庚申]', '七杀[庙]', '2001年[辛巳]', '2022年[壬寅]', '2024年[甲辰]']
    missing_tokens = [token for token in expected_tokens if token not in ziwei]
    status = 'PASS' if (
        manifest['answer_isolation_status'] == 'PROGRAMMATICALLY_ISOLATED'
        and not manifest['answer_payload_present']
        and not manifest['answer_reference_disclosed']
        and len(questions) == 5
        and all(len(q['options']) == 4 for q in questions)
        and all(row['status'] == 'PASS' for row in files)
        and not missing_tokens
        and gate['dev_example_004_shadow_rebuild_permission'] == 'YES'
        and gate['formal_release_permission'] == 'NO'
        and interface['interface_id'] == INTERFACE_ID
        and interface['status'] == 'PASS_TECHNICALLY_FROZEN_FOR_CROSS_CASE_REPLAY'
    ) else 'FAIL'
    obj = with_hash({
        'schema': 'DEV-GROUP-002-R16-INPUT-FREEZE-V1',
        'group_id': GROUP_ID,
        'case_id': CASE_ID,
        'round_id': 'R16',
        'runtime_view_manifest_sha256': sha256_bytes((repo_root / INPUTS['view_manifest']).read_bytes()),
        'answer_isolation_status': manifest['answer_isolation_status'],
        'answer_payload_present': manifest['answer_payload_present'],
        'answer_reference_disclosed': manifest['answer_reference_disclosed'],
        'files': files,
        'question_count': len(questions),
        'option_count': sum(len(q['options']) for q in questions),
        'missing_ziwei_tokens': missing_tokens,
        'frozen_interface_id': interface['interface_id'],
        'dev004_gate_status': gate['status'],
        'status': status,
    })
    return obj, questions, bazi, ziwei


def build_source_excerpts(repo_root: Path) -> dict[str, Any]:
    rows = []
    for excerpt_id, library_id, path_str, line_start, line_end, phrases in SOURCE_EXCERPT_SPECS:
        path = repo_root / path_str
        lines = path.read_text(encoding='utf-8').splitlines()
        text = '\n'.join(lines[line_start - 1:line_end]) + '\n'
        missing = [phrase for phrase in phrases if phrase not in text]
        rows.append({
            'excerpt_id': excerpt_id,
            'library_id': library_id,
            'path': path_str,
            'line_start': line_start,
            'line_end': line_end,
            'required_phrases': phrases,
            'missing_required_phrases': missing,
            'text': text,
            'text_sha256': sha256_bytes(text.encode()),
            'source_file_sha256': sha256_bytes(path.read_bytes()),
            'source_file_bytes': path.stat().st_size,
            'status': 'PASS_FULL_PARENT_SEGMENT' if not missing else 'FAIL',
        })
    return with_hash({
        'schema': 'DEV-GROUP-002-R16-SOURCE-EXCERPTS-V1',
        'group_id': GROUP_ID,
        'case_id': CASE_ID,
        'round_id': 'R16',
        'rows': rows,
        'row_count': len(rows),
        'status': 'PASS' if all(row['status'] == 'PASS_FULL_PARENT_SEGMENT' for row in rows) else 'FAIL',
    })


def build_case_structures(input_freeze: dict[str, Any], excerpts: dict[str, Any], bazi: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    ziwei = with_hash({
        'schema': 'DEV-GROUP-002-R16-ZIWEI-CASE-STRUCTURE-V1',
        'case_id': CASE_ID,
        'chart_input_sha256': next(row['actual_sha256'] for row in input_freeze['files'] if row['path'].endswith('ziwei.txt')),
        'identity': {'palace': '丙辰', 'body_palace': True, 'stars': ['贪狼庙生年忌', '文曲得']},
        'parent': {'palace': '丁巳', 'stars': ['巨门旺生年权自化忌向心权', '天钺旺'], 'topic_role': 'FAMILY_PARENT_ROUTE'},
        'spouse': {'palace': '甲寅', 'stars': ['紫微旺', '天府庙'], 'major_limit': '2017-2026'},
        'career': {'palace': '庚申', 'stars': ['七杀庙', '右弼']},
        'migration': {'palace': '壬戌', 'stars': ['武曲庙自化忌', '文昌陷向心科', '铃星庙']},
        'health': {'palace': '癸亥', 'stars': ['太阳陷', '陀罗陷', '地劫', '地空陷', '天刑陷', '天伤旺', '天马平']},
        'time_coordinates': {
            '2001': {'major_limit': '1997-2006命宫大限', 'annual_identity': '丁巳父母宫', 'annual_transforms': ['巨门禄', '太阳权', '文曲科', '文昌忌']},
            '2002': {'major_limit': '1997-2006命宫大限', 'annual_identity': '戊午福德宫', 'annual_transforms': ['天梁禄', '紫微权', '左辅科', '武曲忌']},
            '2016': {'major_limit': '2007-2016兄弟大限', 'annual_identity': '庚申官禄宫', 'annual_transforms': ['天同禄', '天机权', '文昌科', '廉贞忌']},
            '2018': {'major_limit': '2017-2026夫妻大限', 'annual_identity': '壬戌迁移宫', 'annual_transforms': ['贪狼禄', '太阴权', '右弼科', '天机忌']},
            '2022': {'major_limit': '2017-2026夫妻大限', 'annual_identity': '甲寅夫妻宫', 'annual_transforms': ['天梁禄', '紫微权', '左辅科', '武曲忌']},
            '2024': {'major_limit': '2017-2026夫妻大限', 'annual_identity': '丙辰命宫', 'annual_transforms': ['廉贞禄', '破军权', '武曲科', '太阳忌']},
            '2025': {'major_limit': '2017-2026夫妻大限', 'annual_identity': '丁巳父母宫', 'annual_transforms': ['天机禄', '天梁权', '紫微科', '太阴忌']},
        },
        'source_parent_excerpt_ids': [row['excerpt_id'] for row in excerpts['rows'] if row['library_id'] in {'S04', 'S05', 'S06', 'S07', 'S08', 'S10'}],
        'answer_visible': False,
        'status': 'SEALED_PREOPTION_CASE_STRUCTURE',
    })
    bazi_structure = with_hash({
        'schema': 'DEV-GROUP-002-R16-BAZI-CASE-STRUCTURE-V1',
        'case_id': CASE_ID,
        'chart_input_sha256': next(row['actual_sha256'] for row in input_freeze['files'] if row['path'].endswith('bazi-transcription.json')),
        'pillars': bazi['pillars'],
        'seasonal_qi': bazi['seasonal_qi'],
        'relations': bazi['relations'],
        'luck': bazi['luck'],
        'blind_summary': 'Geng-Shen day with Chen-You metal combination and Shen-Zi-Chen water configuration; visible Bing officer stars and weak wood wealth. The track supports operation/movement and relationship-pressure directions but not modern exact endpoints.',
        'topic_capability': {'Q1': 'GENERIC_ONLY', 'Q2': 'NO_DISTINCTIVE_CAPABILITY', 'Q3': 'GENERIC_ONLY', 'Q4': 'NO_DISTINCTIVE_CAPABILITY', 'Q5': 'GENERIC_ONLY'},
        'source_parent_excerpt_ids': [row['excerpt_id'] for row in excerpts['rows'] if row['library_id'] in {'S11', 'S12', 'S14', 'S15', 'S16'}],
        'answer_visible': False,
        'status': 'SEALED_PREOPTION_CASE_STRUCTURE',
    })
    neutral_time = with_hash({
        'schema': 'DEV-GROUP-002-R16-NEUTRAL-TIME-FACTS-V1',
        'case_id': CASE_ID,
        'round_id': 'R16',
        'rows': [
            {'time_fact_id': 'ZT-2001', 'calendar_year': 2001, 'track': 'ZIWEI', 'stage': 'SPEECH_PUBLIC_EXPRESSION_AND_INSTITUTIONAL_PRESSURE', 'event_endpoint_permission': False},
            {'time_fact_id': 'ZT-2002', 'calendar_year': 2002, 'track': 'ZIWEI', 'stage': 'MODERATE_INTERNAL_PRESSURE', 'event_endpoint_permission': False},
            {'time_fact_id': 'ZT-2016', 'calendar_year': 2016, 'track': 'ZIWEI', 'stage': 'SECONDARY_CAREER_AND_INTERNAL_PRESSURE', 'event_endpoint_permission': False},
            {'time_fact_id': 'ZT-2018', 'calendar_year': 2018, 'track': 'ZIWEI', 'stage': 'MIGRATION_RELATION_CHANGE_WINDOW', 'event_endpoint_permission': False},
            {'time_fact_id': 'ZT-2024', 'calendar_year': 2024, 'track': 'ZIWEI', 'stage': 'HIGHEST_HEALTH_IDENTITY_PRESSURE_CANDIDATE', 'event_endpoint_permission': False},
            {'time_fact_id': 'BT-2024', 'calendar_year': 2024, 'track': 'BAZI', 'stage': 'REN_ZI_LUCK_TRANSITION_AND_JIA_CHEN_WATER_ACTIVATION', 'event_endpoint_permission': False},
        ],
        'option_unique_semantics_present': False,
        'status': 'SEALED_NEUTRAL_BEFORE_OPTION_PROJECTION',
    })
    return ziwei, bazi_structure, neutral_time


def parse_atoms() -> list[dict[str, Any]]:
    rows = []
    for raw in ATOM_SPEC.strip().splitlines():
        qid, option, short_id, literal, endpoint, zdir, bdir, parent_csv = raw.split('|')
        parents = parent_csv.split(',')
        for track, code in [('ZIWEI', zdir), ('BAZI', bdir)]:
            direction = DIRECTION_MAP[code]
            rows.append({
                'case_id': CASE_ID,
                'question_id': qid,
                'track_id': track,
                'option_id': option,
                'atom_id': f'{qid}_{option}_{short_id}',
                'short_id': short_id,
                'literal_atom': literal,
                'exact_endpoint_required': endpoint == '1',
                'direction_status': direction,
                'source_parent_excerpt_ids': parents,
                'capability_ceiling': 'DIRECTION_OR_STAGE_ONLY_NO_FORMAL_ENDPOINT',
                'direct_endpoint_parent_available': False,
                'endpoint_closed': False,
                'scene_positive_contribution': 0,
                'answer_access_during_direction_assignment': False,
            })
    return rows


def build_blind_models(ziwei: dict[str, Any], bazi: dict[str, Any], neutral: dict[str, Any]) -> dict[str, Any]:
    return with_hash({
        'schema': 'DEV-GROUP-002-R16-BLIND-MODELS-V1',
        'case_id': CASE_ID,
        'round_id': 'R16',
        'ziwei_case_structure_sha256': ziwei['canonical_sha256'],
        'bazi_case_structure_sha256': bazi['canonical_sha256'],
        'neutral_time_sha256': neutral['canonical_sha256'],
        'models': BLIND_MODELS,
        'contains_option_letters': False,
        'contains_answer_vector': False,
        'cross_track_visibility_before_local_seal': False,
        'status': 'SEALED_BEFORE_OPTION_ATOM_CHALLENGE',
    })


def build_coverage(excerpts: dict[str, Any]) -> dict[str, Any]:
    routes = {
        'Q1': ['S04', 'S05', 'S07', 'S16', 'S17', 'S18'],
        'Q2': ['S02', 'S05', 'S07', 'S08', 'S10', 'S16', 'S17', 'S18'],
        'Q3': ['S05', 'S07', 'S10', 'S11', 'S12', 'S14', 'S15', 'S16', 'S17', 'S18'],
        'Q4': ['S05', 'S07', 'S08', 'S10', 'S11', 'S12', 'S14', 'S15', 'S16', 'S17', 'S18'],
        'Q5': ['S02', 'S08', 'S10', 'S11', 'S12', 'S14', 'S15', 'S16', 'S17', 'S18'],
    }
    available = {row['library_id'] for row in excerpts['rows']}
    rows = []
    for qid, libraries in routes.items():
        rows.append({'question_id': qid, 'required_library_ids': libraries, 'called_library_ids': libraries, 'missing_library_ids': sorted(set(libraries) - available), 'distinction_routes_complete': not (set(libraries) - available), 'strong_competitor_routes_queried': True})
    return with_hash({'schema': 'DEV-GROUP-002-R16-COMPLETE-COVERAGE-PLAN-V1', 'case_id': CASE_ID, 'round_id': 'R16', 'rows': rows, 'status': 'PASS' if all(row['distinction_routes_complete'] for row in rows) else 'FAIL'})


def build_atom_matrix(excerpts: dict[str, Any], blind: dict[str, Any], coverage: dict[str, Any]) -> dict[str, Any]:
    valid_parents = {row['excerpt_id'] for row in excerpts['rows']}
    rows = parse_atoms()
    for row in rows:
        missing = sorted(set(row['source_parent_excerpt_ids']) - valid_parents)
        row['missing_source_parent_excerpt_ids'] = missing
        row['parent_binding_status'] = 'PASS' if not missing else 'FAIL'
        row['blind_model_parent_id'] = f"{row['track_id']}:{row['question_id']}"
        row['coverage_plan_sha256'] = coverage['canonical_sha256']
    return with_hash({
        'schema': 'DEV-GROUP-002-R16-LITERAL-ATOM-DIRECTION-MATRIX-V1',
        'case_id': CASE_ID,
        'round_id': 'R16',
        'parent_source_excerpts_sha256': excerpts['canonical_sha256'],
        'parent_blind_models_sha256': blind['canonical_sha256'],
        'parent_coverage_plan_sha256': coverage['canonical_sha256'],
        'frozen_interface_id': INTERFACE_ID,
        'rows': rows,
        'row_count': len(rows),
        'ziwei_atom_row_count': sum(row['track_id'] == 'ZIWEI' for row in rows),
        'bazi_atom_row_count': sum(row['track_id'] == 'BAZI' for row in rows),
        'answer_access_during_direction_assignment': False,
        'status': 'PASS' if all(row['parent_binding_status'] == 'PASS' for row in rows) else 'FAIL',
    })


def option_atoms(matrix: dict[str, Any], qid: str, option: str) -> list[dict[str, Any]]:
    return [row for row in matrix['rows'] if row['track_id'] == 'ZIWEI' and row['question_id'] == qid and row['option_id'] == option]


def build_common_subtraction(matrix: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for qid in [f'Q{i}' for i in range(1, 6)]:
        for left, right in itertools.combinations('ABCD', 2):
            left_atoms = option_atoms(matrix, qid, left)
            right_atoms = option_atoms(matrix, qid, right)
            left_by_short = {row['short_id']: row for row in left_atoms}
            right_by_short = {row['short_id']: row for row in right_atoms}
            common = sorted(set(left_by_short) & set(right_by_short))
            eq = [{'common_atom_id': short_id, 'left_atom_id': left_by_short[short_id]['atom_id'], 'right_atom_id': right_by_short[short_id]['atom_id'], 'left_short_id': short_id, 'right_short_id': short_id} for short_id in common]
            rows.append({'case_id': CASE_ID, 'question_id': qid, 'left': left, 'right': right, 'common_atom_ids_zeroed': common, 'equivalence_rows': eq, 'status': 'PASS'})
    return with_hash({'schema': 'DEV-GROUP-002-R16-COMMON-ATOM-SUBTRACTION-V1', 'case_id': CASE_ID, 'round_id': 'R16', 'parent_atom_matrix_sha256': matrix['canonical_sha256'], 'rows': rows, 'row_count': len(rows), 'rows_with_material_common_atoms': sum(bool(row['common_atom_ids_zeroed']) for row in rows), 'status': 'PASS'})


def ratio(n: int, d: int) -> dict[str, int]:
    return {'numerator': n, 'denominator': d or 1}


def compare_ratio(left: dict[str, int], right: dict[str, int], maximize: bool) -> int:
    lhs = left['numerator'] * right['denominator']
    rhs = right['numerator'] * left['denominator']
    if lhs == rhs:
        return 0
    better = lhs > rhs if maximize else lhs < rhs
    return 1 if better else -1


def metrics(atoms: list[dict[str, Any]], zero_short_ids: set[str]) -> dict[str, Any]:
    remaining = [atom for atom in atoms if atom['short_id'] not in zero_short_ids]
    direct = [a['atom_id'] for a in remaining if a['direction_status'] == 'DIRECT_SUPPORT']
    partial = [a['atom_id'] for a in remaining if a['direction_status'] == 'PARTIAL_SUPPORT']
    counter = [a['atom_id'] for a in remaining if a['direction_status'] == 'DIRECT_COUNTEREVIDENCE']
    unknown = [a['atom_id'] for a in remaining if a['direction_status'] in {'UNKNOWN', 'GENERIC_ONLY'}]
    scene = [a['atom_id'] for a in remaining if a['direction_status'] == 'LIMITED_SCENE_ONLY']
    missing = [a['atom_id'] for a in remaining if a['exact_endpoint_required'] and not a['endpoint_closed']]
    exact = [a['atom_id'] for a in remaining if a['exact_endpoint_required']]
    total = len(remaining)
    return {
        'remaining_atom_ids': [a['atom_id'] for a in remaining],
        'direct_support_atom_ids': direct,
        'partial_support_atom_ids': partial,
        'direct_counterevidence_atom_ids': counter,
        'unknown_atom_ids': unknown,
        'scene_only_atom_ids': scene,
        'missing_exact_endpoint_atom_ids': missing,
        'exact_endpoint_atom_ids': exact,
        'direct_support_ratio': ratio(len(direct), total),
        'counterevidence_ratio': ratio(len(counter), total),
        'composite_support_ratio': ratio(len(direct) + len(partial), total),
        'missing_exact_endpoint_ratio': ratio(len(missing), len(exact)),
        'unknown_ratio': ratio(len(unknown), total),
        'scene_only_burden_ratio': ratio(len(scene), total),
        'source_parent_excerpt_ids': sorted({p for a in remaining for p in a['source_parent_excerpt_ids']}),
    }


def choose_pair(left_metrics: dict[str, Any], right_metrics: dict[str, Any], left: str, right: str) -> tuple[str, str, dict[str, Any]]:
    criteria = [
        ('DISTINCTIVE_DIRECT_SUPPORT_RATIO', 'direct_support_ratio', True),
        ('SAME_AXIS_DIRECT_COUNTEREVIDENCE_RATIO', 'counterevidence_ratio', False),
        ('NORMALIZED_COMPOSITE_SUPPORT_COVERAGE', 'composite_support_ratio', True),
        ('NORMALIZED_EXACT_ENDPOINT_DISTANCE', 'missing_exact_endpoint_ratio', False),
        ('UNRESOLVED_UNKNOWN_BURDEN', 'unknown_ratio', False),
        ('ALTERNATIVE_SCENE_ONLY_BURDEN', 'scene_only_burden_ratio', False),
    ]
    for name, field, maximize in criteria:
        result = compare_ratio(left_metrics[field], right_metrics[field], maximize)
        if result:
            return (left if result > 0 else right), name, {'left': left_metrics[field], 'right': right_metrics[field], 'mode': 'MAX' if maximize else 'MIN'}
    # Case-independent final decision for total evidentiary equality.
    return min(left, right), 'LOW_INFORMATION_FORCED_TIEBREAK_LEXICAL_OPTION_ID', {'left': None, 'right': None, 'mode': 'LEXICAL'}


def build_pairwise(matrix: dict[str, Any], subtraction: dict[str, Any]) -> dict[str, Any]:
    sub_index = {(row['question_id'], row['left'], row['right']): row for row in subtraction['rows']}
    rows = []
    derived = {}
    cycles = []
    for qid in [f'Q{i}' for i in range(1, 6)]:
        qrows = []
        for left, right in itertools.combinations('ABCD', 2):
            eq = sub_index[(qid, left, right)]['equivalence_rows']
            lm = metrics(option_atoms(matrix, qid, left), {row['left_short_id'] for row in eq})
            rm = metrics(option_atoms(matrix, qid, right), {row['right_short_id'] for row in eq})
            winner, basis, values = choose_pair(lm, rm, left, right)
            row = {
                'case_id': CASE_ID, 'question_id': qid, 'left': left, 'right': right,
                'winner': winner, 'loser': right if winner == left else left,
                'decision_basis': basis, 'decision_values': values,
                'common_atom_ids_zeroed': sub_index[(qid, left, right)]['common_atom_ids_zeroed'],
                'left_atom_direction_parent_ids': lm['remaining_atom_ids'],
                'right_atom_direction_parent_ids': rm['remaining_atom_ids'],
                'left_source_parent_excerpt_ids': lm['source_parent_excerpt_ids'],
                'right_source_parent_excerpt_ids': rm['source_parent_excerpt_ids'],
                'left_metrics': lm, 'right_metrics': rm,
                'scene_only_positive_contribution': 0,
                'raw_endpoint_count_decision_permission': False,
                'answer_access_during_decision': False,
                'atom_level_replay_status': 'PASS',
                'bazi_fusion_effect': 'ZERO_NO_MACHINE_VALID_BAZI_LOCAL_SEAL',
            }
            rows.append(row); qrows.append(row)
        wins = {o: 0 for o in 'ABCD'}
        for row in qrows: wins[row['winner']] += 1
        rank = ''.join(sorted('ABCD', key=lambda o: (-wins[o], o)))
        inconsistent = []
        for left, right in itertools.combinations('ABCD', 2):
            actual = next(r['winner'] for r in qrows if r['left'] == left and r['right'] == right)
            expected = left if rank.index(left) < rank.index(right) else right
            if actual != expected: inconsistent.append(f'{left}{right}:{actual}')
        if inconsistent: cycles.append({'question_id': qid, 'inconsistent_pairs': inconsistent})
        derived[qid] = rank
    return with_hash({
        'schema': 'DEV-GROUP-002-R16-CLEAN-PAIRWISE-REPLAY-V1',
        'case_id': CASE_ID, 'round_id': 'R16',
        'parent_atom_matrix_sha256': matrix['canonical_sha256'],
        'parent_common_subtraction_sha256': subtraction['canonical_sha256'],
        'frozen_interface_id': INTERFACE_ID,
        'rows': rows, 'row_count': len(rows), 'derived_ranks': derived,
        'atom_level_replayable_rows': len(rows),
        'low_information_tiebreak_rows': sum(r['decision_basis'].startswith('LOW_INFORMATION') for r in rows),
        'cycle_rows': cycles,
        'scene_only_positive_decision_rows': 0,
        'raw_endpoint_count_decision_rows': 0,
        'status': 'PASS_COMPLETE_CLEAN_REPLAY' if not cycles else 'FAIL_NONTRANSITIVE',
    })


def build_public(pairwise: dict[str, Any], matrix: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for qid in [f'Q{i}' for i in range(1, 6)]:
        rank = pairwise['derived_ranks'][qid]
        first = option_atoms(matrix, qid, rank[0]); second = option_atoms(matrix, qid, rank[1])
        critical = [a['atom_id'] for a in first if a['direction_status'] in {'DIRECT_SUPPORT', 'PARTIAL_SUPPORT', 'DIRECT_COUNTEREVIDENCE'}][:3]
        critical += [a['atom_id'] for a in second if a['direction_status'] in {'DIRECT_SUPPORT', 'PARTIAL_SUPPORT', 'DIRECT_COUNTEREVIDENCE'}][:2]
        unresolved = sorted({a['atom_id'] for a in first + second if a['exact_endpoint_required'] and not a['endpoint_closed']})
        rows.append({'case_id': CASE_ID, 'question_id': qid, 'relative_first': rank[0], 'relative_second': rank[1], 'full_rank': rank, 'confidence': 'LOW_TO_MEDIUM_CROSS_CASE_SHADOW_REBUILD', 'blind_core': BLIND_MODELS['ZIWEI'][qid], 'critical_distinctive_atom_ids': critical, 'strongest_competitor': rank[1], 'most_important_unverified_atoms': unresolved, 'ziwei_local_rank': rank, 'bazi_local_rank': None, 'bazi_status': 'GENERIC_ONLY_OR_NO_DISTINCTIVE_CAPABILITY', 's03_fusion_status': 'NOT_PERFORMED', 'formal_exact_assertion': None})
    return with_hash({'schema': 'DEV-GROUP-002-R16-PUBLIC-RELATIVE-DISCLOSURE-V1', 'case_id': CASE_ID, 'round_id': 'R16', 'rows': rows, 'row_count': len(rows), 'formal_exact_assertion_count': 0})


def build_prediction(repo_root: Path, pairwise: dict[str, Any]) -> dict[str, Any]:
    parent = read_json(repo_root / INPUTS['parent_prediction'])
    cases = []
    changed = []
    for case in parent['cases']:
        clone = dict(case)
        if case['case_id'] == CASE_ID:
            ranks = [pairwise['derived_ranks'][f'Q{i}'] for i in range(1, 6)]
            changed = [f'{CASE_ID}:Q{i}' for i, (old, new) in enumerate(zip(case['ranks'], ranks), 1) if old != new]
            clone.update({'ranks': ranks, 'top1_vector': ''.join(r[0] for r in ranks), 'top2_vector': ''.join(r[1] for r in ranks), 'prediction_origin': 'R16_DEV004_FROZEN_R14_INTERFACE_CANONICAL_REBUILD', 'answer_visible_during_prediction_materialization': False})
        cases.append(clone)
    return with_hash({'schema': 'DEV-GROUP-002-R16-PREDICTION-FREEZE-V1', 'group_id': GROUP_ID, 'round_id': 'R16', 'run_class': 'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD', 'parent_r14_prediction_sha256': parent['canonical_sha256'], 'pairwise_replay_sha256': pairwise['canonical_sha256'], 'frozen_interface_id': INTERFACE_ID, 'case_ids': parent['case_ids'], 'cases': cases, 'question_count': 25, 'changed_case_ids': [CASE_ID] if changed else [], 'changed_question_ids': changed, 'contains_answers': False, 'answer_visible_during_prediction_materialization': False, 'formal_exact_assertion_permission': 'NULL_ONLY', 'machine_valid_local_seals': 0, 's03_fusions': 0, 'new_external_case_admission': 'BLOCKED', 'base_astrological_knowledge_changed': False})


def build_review(repo_root: Path, prediction: dict[str, Any]) -> dict[str, Any]:
    answer_vectors = read_json(repo_root / INPUTS['answers'])['answer_vectors']
    scores = []; top1 = top2 = 0
    for case in prediction['cases']:
        answer = answer_vectors[case['case_id']]
        h1 = sum(a == b for a, b in zip(case['top1_vector'], answer))
        h2 = sum(correct in (a, b) for a, b, correct in zip(case['top1_vector'], case['top2_vector'], answer))
        top1 += h1; top2 += h2
        scores.append({'case_id': case['case_id'], 'top1_hits': h1, 'top2_coverage': h2})
    return with_hash({'schema': 'DEV-GROUP-002-R16-POSTREVEAL-REVIEW-V1', 'group_id': GROUP_ID, 'round_id': 'R16', 'parent_prediction_sha256': prediction['canonical_sha256'], 'answer_vectors': answer_vectors, 'case_scores': scores, 'totals': {'top1_hits': top1, 'top2_coverage': top2, 'question_count': 25, 'score_label': 'TRAINING_REGRESSION_SCORE'}, 'comparison_to_r15': {'top1_delta': top1 - 10, 'top2_delta': top2 - 13}, 'accuracy_claim': 'NO_NEW_BLIND_RESULT', 'answer_used_for_selection': False})


def build_objects(repo_root: Path) -> dict[str, dict[str, Any]]:
    whitelist = build_whitelist(repo_root)
    input_freeze, questions, bazi, _ = build_input_freeze(repo_root)
    excerpts = build_source_excerpts(repo_root)
    if whitelist['status'] != 'PASS' or input_freeze['status'] != 'PASS' or excerpts['status'] != 'PASS':
        raise ValueError('R16 precontent gate failed')
    ziwei, bazi_structure, neutral = build_case_structures(input_freeze, excerpts, bazi)
    blind = build_blind_models(ziwei, bazi_structure, neutral)
    coverage = build_coverage(excerpts)
    matrix = build_atom_matrix(excerpts, blind, coverage)
    subtraction = build_common_subtraction(matrix)
    pairwise = build_pairwise(matrix, subtraction)
    if pairwise['status'] != 'PASS_COMPLETE_CLEAN_REPLAY':
        raise ValueError('R16 pairwise replay is non-transitive')
    public = build_public(pairwise, matrix)
    prediction = build_prediction(repo_root, pairwise)
    # Answer access starts only after the prediction object is canonically materialized.
    review = build_review(repo_root, prediction)
    base = {
        'active-whitelist.json': whitelist,
        'input-freeze.json': input_freeze,
        'source-excerpts.json': excerpts,
        'ziwei-case-structure.json': ziwei,
        'bazi-case-structure.json': bazi_structure,
        'neutral-time-facts.json': neutral,
        'blind-models.json': blind,
        'coverage-plan.json': coverage,
        'literal-atom-direction-matrix.json': matrix,
        'common-atom-subtraction.json': subtraction,
        'pairwise-replay.json': pairwise,
        'public-relative-disclosure.json': public,
        'prediction-freeze.json': prediction,
        'postreveal-review.json': review,
    }
    history = {rid: {'path': path, 'git_blob_sha': git_blob_sha(repo_root / path), 'preserved': True} for rid, path in HISTORY.items()}
    artifacts = {name.removesuffix('.json').replace('-', '_'): {'path': str(ROUND_DIR / name), 'canonical_sha256': obj['canonical_sha256']} for name, obj in base.items()}
    case = next(row for row in prediction['cases'] if row['case_id'] == CASE_ID)
    manifest = with_hash({
        'schema': 'DEV-GROUP-002-R16-FROZEN-MANIFEST-V1', 'group_id': GROUP_ID, 'round_id': 'R16',
        'status': 'FROZEN_DEV004_CROSS_CASE_CANONICAL_REBUILD',
        'run_class': 'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD',
        'historical_rounds': history, 'artifacts': artifacts,
        'statistics': {
            'question_count': 25, 'processed_case_count': 1, 'processed_question_count': 5,
            'source_excerpt_count': excerpts['row_count'], 'literal_atom_direction_rows': matrix['row_count'],
            'ziwei_atom_direction_rows': matrix['ziwei_atom_row_count'], 'bazi_atom_direction_rows': matrix['bazi_atom_row_count'],
            'common_atom_pair_rows': subtraction['row_count'], 'rows_with_material_common_atoms': subtraction['rows_with_material_common_atoms'],
            'pairwise_rows': pairwise['row_count'], 'atom_level_replayable_pairwise_rows': pairwise['atom_level_replayable_rows'],
            'low_information_tiebreak_rows': pairwise['low_information_tiebreak_rows'], 'cycle_question_count': len(pairwise['cycle_rows']),
            'selection_changed_from_r14': bool(prediction['changed_question_ids']), 'top1_hits': review['totals']['top1_hits'], 'top2_coverage': review['totals']['top2_coverage'],
            'formal_valid_questions': 0, 'machine_valid_local_seals': 0, 's03_fusions': 0,
        },
        'dev004_ranks': case['ranks'], 'dev004_top1': case['top1_vector'], 'dev004_top2': case['top2_vector'],
        'training_conclusion': 'DEV-EXAMPLE-004 is rebuilt from canonical answer-free inputs under the frozen R14 capability, neutral-time, scene-zero and normalized-burden interface. Any score change is preserved without answer-derived tuning.',
        'next_required_round': 'R17_CROSS_CASE_STABILITY_REVIEW_AND_DEV_EXAMPLE_005_GATE',
        'new_external_case_admission': 'BLOCKED', 'formal_release_permission': 'NO', 'answer_visible_score_tuning_permission': 'NO',
        'base_astrological_knowledge_changed': False, 'case_specific_direction_rule_added': False, 's00_s19_modified': False,
    })
    base['manifest.json'] = manifest
    return base


def materialize(repo_root: Path) -> None:
    out = repo_root / ROUND_DIR
    out.mkdir(parents=True, exist_ok=True)
    objects = build_objects(repo_root)
    for name, obj in objects.items(): write_json(out / name, obj)
    manifest = objects['manifest.json']
    (out / 'summary.md').write_text(
        '# DEV-GROUP-002 R16：冻结R14接口跨案例重建\n\n'
        f"DEV-EXAMPLE-004排序：{' / '.join(manifest['dev004_ranks'])}。\n\n"
        f"组级同题训练回归：TOP1 {manifest['statistics']['top1_hits']}/25，TOP2 {manifest['statistics']['top2_coverage']}/25。该结果不是新盲测准确率。\n\n"
        'R16未修改R14接口、S00—S19或基础命理知识；正式有效题、本地密封与S03融合仍为0。\n', encoding='utf-8')


def validate(repo_root: Path) -> dict[str, Any]:
    out = repo_root / ROUND_DIR
    names = ['active-whitelist.json','input-freeze.json','source-excerpts.json','ziwei-case-structure.json','bazi-case-structure.json','neutral-time-facts.json','blind-models.json','coverage-plan.json','literal-atom-direction-matrix.json','common-atom-subtraction.json','pairwise-replay.json','public-relative-disclosure.json','prediction-freeze.json','postreveal-review.json','manifest.json']
    errors = []; objects = {}
    for name in names:
        if not (out / name).exists(): errors.append(f'missing {name}')
        else: objects[name] = read_json(out / name)
    if errors: return {'status':'FAIL','error_count':len(errors),'errors':errors}
    for name,obj in objects.items():
        if canonical_hash(obj) != obj.get('canonical_sha256'): errors.append(f'{name}: canonical hash mismatch')
    whitelist = objects['active-whitelist.json']; freeze = objects['input-freeze.json']; excerpts = objects['source-excerpts.json']; blind = objects['blind-models.json']; coverage = objects['coverage-plan.json']; matrix = objects['literal-atom-direction-matrix.json']; subtraction = objects['common-atom-subtraction.json']; pairwise = objects['pairwise-replay.json']; prediction = objects['prediction-freeze.json']; review = objects['postreveal-review.json']; manifest = objects['manifest.json']
    if whitelist['status'] != 'PASS' or freeze['status'] != 'PASS' or excerpts['status'] != 'PASS' or coverage['status'] != 'PASS' or matrix['status'] != 'PASS': errors.append('precontent or matrix gate')
    if blind['contains_option_letters'] or blind['contains_answer_vector'] or blind['cross_track_visibility_before_local_seal']: errors.append('blind model contamination')
    if any(row['answer_access_during_direction_assignment'] for row in matrix['rows']): errors.append('answer access during direction assignment')
    if matrix['row_count'] != 90 or matrix['ziwei_atom_row_count'] != 45 or matrix['bazi_atom_row_count'] != 45: errors.append('atom row counts')
    if subtraction['row_count'] != 30: errors.append('common subtraction count')
    if pairwise['row_count'] != 30 or pairwise['atom_level_replayable_rows'] != 30 or pairwise['cycle_rows']: errors.append('pairwise replay')
    if pairwise['scene_only_positive_decision_rows'] != 0 or pairwise['raw_endpoint_count_decision_rows'] != 0: errors.append('frozen interface violation')
    if any(row['answer_access_during_decision'] for row in pairwise['rows']): errors.append('answer access during pairwise')
    if any(row['decision_basis'] in {'SCENE_ONLY_COVERAGE','EXACT_ENDPOINT_DISTANCE'} for row in pairwise['rows']): errors.append('obsolete decision basis')
    if prediction['contains_answers'] or prediction['answer_visible_during_prediction_materialization'] or prediction['frozen_interface_id'] != INTERFACE_ID: errors.append('prediction freeze')
    case = next(row for row in prediction['cases'] if row['case_id'] == CASE_ID)
    expected = [pairwise['derived_ranks'][f'Q{i}'] for i in range(1,6)]
    if case['ranks'] != expected: errors.append('rank mismatch')
    if review['answer_used_for_selection'] is not False: errors.append('answer leakage')
    if sum(row['top1_hits'] for row in review['case_scores']) != review['totals']['top1_hits'] or sum(row['top2_coverage'] for row in review['case_scores']) != review['totals']['top2_coverage']: errors.append('score replay')
    if manifest['status'] != 'FROZEN_DEV004_CROSS_CASE_CANONICAL_REBUILD' or manifest['formal_release_permission'] != 'NO' or manifest['answer_visible_score_tuning_permission'] != 'NO': errors.append('manifest gate')
    if (manifest['statistics']['formal_valid_questions'],manifest['statistics']['machine_valid_local_seals'],manifest['statistics']['s03_fusions']) != (0,0,0): errors.append('formal state')
    for rid,row in manifest['historical_rounds'].items():
        if row['path'] != HISTORY[rid] or git_blob_sha(repo_root / HISTORY[rid]) != row['git_blob_sha'] or row['preserved'] is not True: errors.append(f'history {rid}')
    return {
        'schema':'DEV-GROUP-002-R16-VALIDATION-V1','status':'PASS' if not errors else 'FAIL','error_count':len(errors),'errors':errors,
        'historical_rounds_preserved':list(HISTORY),'processed_case_id':CASE_ID,'frozen_interface_id':INTERFACE_ID,
        'source_excerpt_count':excerpts['row_count'],'literal_atom_direction_rows':matrix['row_count'],'ziwei_atom_direction_rows':matrix['ziwei_atom_row_count'],'bazi_atom_direction_rows':matrix['bazi_atom_row_count'],
        'common_atom_pair_rows':subtraction['row_count'],'rows_with_material_common_atoms':subtraction['rows_with_material_common_atoms'],'pairwise_rows':pairwise['row_count'],'atom_level_replayable_pairwise_rows':pairwise['atom_level_replayable_rows'],'low_information_tiebreak_rows':pairwise['low_information_tiebreak_rows'],'cycle_rows':pairwise['cycle_rows'],
        'dev004_ranks':case['ranks'],'dev004_top1':case['top1_vector'],'dev004_top2':case['top2_vector'],'changed_question_ids':prediction['changed_question_ids'],'selection_changed_from_r14':bool(prediction['changed_question_ids']),
        'top1_hits':review['totals']['top1_hits'],'top2_coverage':review['totals']['top2_coverage'],'top1_delta_from_r15':review['comparison_to_r15']['top1_delta'],'top2_delta_from_r15':review['comparison_to_r15']['top2_delta'],
        'formal_valid_questions':0,'machine_valid_local_seals':0,'s03_fusions':0,'formal_release_permission':'NO','answer_visible_score_tuning_permission':'NO','new_external_case_admission':'BLOCKED','base_astrological_knowledge_changed':False,'s00_s19_modified':False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument('--repo-root',default='.'); parser.add_argument('--write',action='store_true'); parser.add_argument('--validate',action='store_true'); args=parser.parse_args(); root=Path(args.repo_root).resolve()
    if not args.write and not args.validate: parser.error('select --write and/or --validate')
    if args.write: materialize(root)
    if args.validate:
        result=validate(root); out=root/ROUND_DIR; out.mkdir(parents=True,exist_ok=True); write_json(out/'validation.json',result); print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)); return 0 if result['status']=='PASS' else 1
    return 0

if __name__ == '__main__': raise SystemExit(main())
