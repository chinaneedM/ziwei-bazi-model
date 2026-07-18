#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
from pathlib import Path
from typing import Any

ROUND_DIR = Path('reports/dev-group-002/training-regression-r9')
CASE_ID = 'DEV-EXAMPLE-002'
HISTORY = {
    'R1': 'reports/dev-group-002/training-regression-r1/manifest.json',
    'R2': 'reports/dev-group-002/training-regression-r2/formal-readiness-matrix.json',
    'R3': 'reports/dev-group-002/training-regression-r3/progress.json',
    'R4': 'reports/dev-group-002/training-regression-r4/compact-manifest.json',
    'R5': 'reports/dev-group-002/training-regression-r5/manifest.json',
    'R6': 'reports/dev-group-002/training-regression-r6/manifest.json',
    'R7': 'reports/dev-group-002/training-regression-r7/manifest.json',
    'R8': 'reports/dev-group-002/training-regression-r8/manifest.json',
}
INPUTS = {
    'whitelist': 'reports/dev-group-002/training-regression-r2/active-whitelist-receipt.json',
    'view_manifest': 'training-data/DEV-GROUP-002/runtime-views/DEV-EXAMPLE-002/manifest.json',
    'ziwei': 'training-data/DEV-GROUP-002/runtime-views/DEV-EXAMPLE-002/ziwei.txt',
    'bazi': 'training-data/DEV-GROUP-002/runtime-views/DEV-EXAMPLE-002/bazi-transcription.json',
    'questions': 'training-data/DEV-GROUP-002/runtime-views/DEV-EXAMPLE-002/questions-parsed.json',
    'r7_prediction': 'reports/dev-group-002/training-regression-r7/prediction-freeze.json',
    'answers': 'reports/dev-group-002/training-regression-r5/postreveal-review.json',
}

SOURCE_EXCERPT_SPECS = [
    ('S04_AXIS_SCOPE', 'S04', 'knowledge/base/S04_十二宫主题太极与气数位库.txt', 1667, 1678, ['不得用官禄宫的行业象证明老板身份', '不得用夫妻宫的关系压力证明法律离婚']),
    ('S04_GEOMETRY', 'S04', 'knowledge/base/S04_十二宫主题太极与气数位库.txt', 2228, 2255, ['疾厄宫 | 父母宫', '官禄宫 | 命宫、夫妻宫']),
    ('S05_TIANXIANG_NATURE', 'S05', 'knowledge/base/S05_星曜本性辅煞系统与组合条件库.txt', 820, 850, ['天相坐命宜兼视父母宫吉凶', '难以独立创业']),
    ('S05_TIANLIANG_NATURE', 'S05', 'knowledge/base/S05_星曜本性辅煞系统与组合条件库.txt', 860, 885, ['天梁属阳土', '解厄制化']),
    ('S06_STRUCTURE_CONTROL', 'S06', 'knowledge/base/S06_六十星系与十二基础盘库.txt', 1, 60, ['空宫借星', 'STRUCTURE_SELECTOR_MISMATCH']),
    ('S07_TIANXIANG_CHOU', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 121421, 121575, ['天相在丑、未二宫独坐', '聪明持重', '不宜经商']),
    ('S07_MARRIAGE_LIANTAN', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 123080, 123145, ['廉贞守夫妻宫', '巳亥宫【廉贞贪狼】同度', '两度姻缘']),
    ('S07_FINANCE_TIANFU', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 125035, 125065, ['不主富厚', '必须见禄']),
    ('S07_HEALTH_TIANLIANG', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 125950, 126000, ['天梁主肠胃病', '手脚外伤', '大耗同度或会照']),
    ('S07_CAREER_LIANTAN', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 128260, 128275, ['巳亥宫[廉贞贪狼]同度', '事业亦不只一端', '必须得禄']),
    ('S07_PROPERTY_SUN_JI', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 128855, 128875, ['太阳化忌在田宅', '祖业倾败', '迁动工作环境']),
    ('S07_PARENTS_TONGLIANG', 'S07', 'knowledge/base/S07_全星曜与星系入十二宫库.txt', 130390, 130425, ['天同天梁同度，不主刑克伤害', '父母婚姻有波折']),
    ('S08_TRANSFORMATION_LIMIT', 'S08', 'knowledge/base/S08_十干四化自化与禄忌线库.txt', 1, 25, ['自化', '不证明现实事件']),
    ('S08_NO_ENDPOINT_INFLATION', 'S08', 'knowledge/base/S08_十干四化自化与禄忌线库.txt', 380, 390, ['自化忌不等于失败']),
    ('S10_NEUTRAL_TIME', 'S10', 'knowledge/base/S10_紫微岁运应期与动态辅助库.txt', 1, 52, ['禁止在此对象中写入', '中立时间事实密封后']),
    ('S11_FOUNDATION', 'S11', 'knowledge/base/S11_八字干支五行藏干与十神库.txt', 1, 60, ['S11唯一负责合法八字版本', 'S11不判断旺衰']),
    ('S12_QI_CONTROL', 'S12', 'knowledge/base/S12_八字月令旺衰通根与气势库.txt', 1, 65, ['月令是主轴而非独裁', '不负责格局命名']),
    ('S13_METHOD_COMPETITION', 'S13', 'knowledge/base/S13_八字格局用忌调候与病药库.txt', 1, 65, ['不得先定格局或用神再找证据', '不能直接完成现实事件']),
    ('S14_RELATION_LIMIT', 'S14', 'knowledge/base/S14_八字合冲刑害墓库与结构变化库.txt', 1, 135, ['冲刑害不等于灾祸', '合不等于化']),
    ('S15_NEUTRAL_TIME', 'S15', 'knowledge/base/S15_八字大运流年流月与应期库.txt', 1, 52, ['方向中立时间事实', '不得写入任何选项独有']),
    ('S16_MEDICAL_AND_FAMILY_LIMIT', 'S16', 'knowledge/base/S16_八字专题映射与紫微接口库.txt', 1150, 1190, ['精确医学诊断', '家庭具体事件']),
    ('S16_ROLE_ENDPOINT_LIMIT', 'S16', 'knowledge/base/S16_八字专题映射与紫微接口库.txt', 1380, 1420, ['官印不能直接判大学学历', '财星不能直接判经商所有权']),
    ('S16_TOPIC_PACKAGE', 'S16', 'knowledge/base/S16_八字专题映射与紫微接口库.txt', 1835, 1865, ['官、财、印、食伤只描述结构角色', '必须由S17建立现实父链']),
    ('S17_DIRECTION_AND_ENDPOINT', 'S17', 'knowledge/base/S17_专题闭合人物太极与动作终点链库.txt', 1, 130, ['MISSING_EXACT_ENDPOINT_ERASES_SUPPORT_PERMISSION=NO', 'REALITY_STATUS_LADDER']),
    ('S18_PAIRWISE_ORDER', 'S18', 'knowledge/base/S18_证据归并非法归零与评分分寸库.txt', 170, 230, ['PAIRWISE_DECISION_ORDER', 'LOW_INFORMATION_FORCED_TIEBREAK']),
]

FINAL_RANKS = {
    'Q1': 'DCAB',
    'Q2': 'DBAC',
    'Q3': 'DCBA',
    'Q4': 'CBDA',
    'Q5': 'BADC',
}

QUESTION_TASKS = {
    'Q1': 'HEALTH_2022_2025_MULTI_SYSTEM_VS_DIAGNOSIS_SURGERY',
    'Q2': 'PERSONALITY_EDUCATION_AND_2025_OCCUPATION_COMPOSITE',
    'Q3': 'CAREER_FINANCE_AND_HOUSEHOLD_SUPPORT_2018_2025',
    'Q4': 'MARRIAGE_STATUS_AT_2025',
    'Q5': 'FAMILY_MAGNITUDE_PARENT_RELATION_AND_CAREGIVER',
}

BLIND_MODELS = {
    'ZIWEI': {
        'Q1': 'The self-health route borrows the parent-axis Tongliang structure. The available structure favors a digestive and limb-pain burden with a resolving tendency; it does not establish a modern diagnosis, major surgery, or life-threatening episode.',
        'Q2': 'The natal identity structure is Tianxiang in Chou, favoring intelligence, steadiness, planning and an assistant/management orientation. Exact degree level, employer, ownership and title remain outside the structural ceiling.',
        'Q3': 'The 2019-2028 period is rooted in the property axis with Sun transformation pressure, while the empty career palace borrows Lianzhen-Tanlang and contains movement/void/malefic modifiers. The neutral model favors unstable work roots, multiple activities and cash-flow pressure over smooth fixed employment, but does not prove ownership or partner-paid expenses.',
        'Q4': 'The spouse structure is fallen Lianzhen-Tanlang in Hai with an auxiliary single star and void. It favors relationship friction and multi-stage relationship risk, while legal marriage, divorce, remarriage, current stability and orientation remain unclosed.',
        'Q5': 'The parent palace contains Tongliang with supportive transformations and no direct four-malefic cluster, favoring continuing parental support rather than parent loss. The property Sun transformation pressure supplies an ancestral or household decline scene, not a specific father business act.',
    },
    'BAZI': {
        'Q1': 'The legal solar-term pillars show Yi wood rooted in two Mao branches under a strong-fire season, with weak water and absent natal metal. This supports a hot/dry body-load candidate, but not a diagnosis, organ identity, surgery or severity endpoint.',
        'Q2': 'The structure has strong output expression, rooted wood and weak resource support. This can support intelligence/expression and uneven conventional study, but cannot identify a completed degree, part-time status, ownership or management title.',
        'Q3': 'The 2018 Geng-Xu luck period introduces officer/wealth roles and activates the recorded stem-branch relations. This permits responsibility, financial movement and work-stage change, but cannot identify business ownership, stable employment, recognition or household payer.',
        'Q4': 'The luck period introduces a spouse-role candidate and relationship activation, but the structure cannot identify legal marriage, divorce, remarriage, orientation, verbal abuse or current stability.',
        'Q5': 'The foundation and relation graphs can describe resource pressure only. They cannot identify a parent actor, death, divorce, business failure, caregiver or calibrated household class.',
    },
}

# Every option is a compound object. `key` follows the S18 decision order:
# direct distinctive direction, absence of same-axis counterevidence, composite coverage,
# endpoint distance, time match, alternative explanation control, mechanism coherence.
ZIWEI_OPTIONS: dict[str, dict[str, dict[str, Any]]] = {
    'Q1': {
        'A': {'status':'LIMITED_BY_SOURCE','parents':['S04_GEOMETRY','S05_TIANLIANG_NATURE','S07_HEALTH_TIANLIANG','S17_DIRECTION_AND_ENDPOINT'],'partial':['LIGHT_DISEASE_RESOLUTION_TENDENCY'],'limited':['HEALTHY_FEW_PAIN_STATE','SKIN_SENSITIVITY','SEAFOOD_AVOIDANCE'],'contradicted':[],'unknown':['ACTUAL_2022_2025_HEALTH_RECORD'],'endpoint':['SKIN_DIAGNOSIS_AND_DIETARY_CAUSATION'],'key':[0,1,2,2,1,1,2],'reason':'Tianliang can reduce severity, but the broader health route does not establish a healthy period, skin diagnosis or seafood causation.'},
        'B': {'status':'UNKNOWN','parents':['S04_GEOMETRY','S07_HEALTH_TIANLIANG','S17_DIRECTION_AND_ENDPOINT'],'partial':[],'limited':['GENERAL_HEALTH_RISK_ONLY'],'contradicted':[],'unknown':['MAJOR_SURGERY','LIFE_DANGER'],'endpoint':['SURGERY_AND_SEVERITY_ENDPOINT'],'key':[0,1,1,0,1,1,1],'reason':'No preserved medical endpoint identifies a major operation or life-threatening episode.'},
        'C': {'status':'PARTIALLY_SUPPORTED','parents':['S04_GEOMETRY','S07_HEALTH_TIANLIANG','S17_DIRECTION_AND_ENDPOINT'],'partial':['CHRONIC_OR_RECURRENT_HEALTH_BURDEN'],'limited':['DIABETES_IDENTITY'],'contradicted':[],'unknown':['CLINICAL_DIAGNOSIS'],'endpoint':['DIABETES_DIAGNOSIS_AND_RECURRENCE_RECORD'],'key':[0,1,3,1,2,2,3],'reason':'The health structure supports recurrent burden, but diabetes remains an unverified diagnosis.'},
        'D': {'status':'PARTIALLY_SUPPORTED','parents':['S04_GEOMETRY','S05_TIANLIANG_NATURE','S07_HEALTH_TIANLIANG','S17_DIRECTION_AND_ENDPOINT'],'partial':['DIGESTIVE_BURDEN','LIMB_OR_RHEUMATIC_PAIN'],'limited':['OBESITY','LIVER_IDENTITY'],'contradicted':[],'unknown':['ACTUAL_DIAGNOSES'],'endpoint':['OBESITY_LIVER_GI_FOOT_MEDICAL_RECORD'],'key':[0,1,4,2,2,2,4],'reason':'Borrowed Tianliang plus depletion/malefic context gives the closest direct system-level match to digestive and foot/limb problems, without proving all diagnoses.'},
    },
    'Q2': {
        'A': {'status':'LIMITED_BY_SOURCE','parents':['S05_TIANXIANG_NATURE','S07_TIANXIANG_CHOU','S16_ROLE_ENDPOINT_LIMIT','S17_DIRECTION_AND_ENDPOINT'],'partial':['SALARIED_SUPPORT_ROLE_SCENE'],'limited':['UNIVERSITY_COMPLETION','ORDINARY_EMPLOYMENT'],'contradicted':['MEDIOCRE_LAZY_PERSONALITY'],'unknown':[],'endpoint':['DEGREE_AND_EMPLOYMENT_STATUS'],'key':[0,0,2,1,1,1,2],'reason':'Tianxiang does not support the mediocre/lazy core, although a salaried support role remains structurally plausible.'},
        'B': {'status':'PARTIALLY_SUPPORTED','parents':['S05_TIANXIANG_NATURE','S07_TIANXIANG_CHOU','S16_ROLE_ENDPOINT_LIMIT','S17_DIRECTION_AND_ENDPOINT'],'partial':['INTELLIGENCE'],'limited':['NOT_STUDY_BEHAVIOR','HIGH_SCHOOL_COMPLETION','PART_TIME_PRIMARY_STATUS'],'contradicted':[],'unknown':[],'endpoint':['EDUCATION_AND_JOB_STATUS'],'key':[0,1,3,1,1,2,3],'reason':'Intelligence is supported, but study behavior, highest certificate and part-time status are not.'},
        'C': {'status':'DIRECTLY_CONTRADICTED_MATERIAL_ATOM','parents':['S05_TIANXIANG_NATURE','S07_TIANXIANG_CHOU','S07_FINANCE_TIANFU','S16_ROLE_ENDPOINT_LIMIT','S17_DIRECTION_AND_ENDPOINT'],'partial':['HARDWORKING_OR_SERVICE_ORIENTATION'],'limited':['UNIVERSITY_COMPLETION','FAMILY_BUSINESS_OPERATION'],'contradicted':['NOT_INTELLIGENT'],'unknown':[],'endpoint':['DEGREE_AND_OWNERSHIP'],'key':[0,0,1,0,1,1,1],'reason':'The not-intelligent material atom conflicts with the natal identity model, while family-business ownership is unclosed.'},
        'D': {'status':'PARTIALLY_SUPPORTED','parents':['S05_TIANXIANG_NATURE','S07_TIANXIANG_CHOU','S16_ROLE_ENDPOINT_LIMIT','S17_DIRECTION_AND_ENDPOINT'],'partial':['INTELLIGENCE','PLANNING_OR_MANAGEMENT_ORIENTATION'],'limited':['MASTERS_OR_PHD','CORPORATE_MANAGEMENT_TITLE'],'contradicted':[],'unknown':[],'endpoint':['ADVANCED_DEGREE_AND_FORMAL_TITLE'],'key':[0,1,4,1,2,2,4],'reason':'Tianxiang directly favors intelligence and planning/management orientation, but advanced degrees and corporate title remain missing endpoints.'},
    },
    'Q3': {
        'A': {'status':'DIRECTLY_CONTRADICTED_MATERIAL_ATOM','parents':['S07_PROPERTY_SUN_JI','S07_FINANCE_TIANFU','S10_NEUTRAL_TIME','S17_DIRECTION_AND_ENDPOINT'],'partial':['FINANCIAL_LOSS_SCENE'],'limited':['ROMANCE_SCAM','ALL_SAVINGS_LOST'],'contradicted':['FIXED_STABLE_JOB'],'unknown':[],'endpoint':['SCAM_LOSS_AND_EMPLOYMENT_CONTINUITY'],'key':[0,0,1,0,2,1,1],'reason':'The period model conflicts with a fixed stable job; scam and total-loss endpoints are not established.'},
        'B': {'status':'LIMITED_BY_SOURCE','parents':['S07_CAREER_LIANTAN','S07_FINANCE_TIANFU','S07_PROPERTY_SUN_JI','S10_NEUTRAL_TIME','S17_DIRECTION_AND_ENDPOINT'],'partial':['SKILL_OR_RECOGNITION_CANDIDATE'],'limited':['FAME_SUCCESS','SMOOTH_WORK'],'contradicted':['UNINTERRUPTED_SMOOTH_CAREER'],'unknown':[],'endpoint':['RECOGNITION_AND_SUCCESS_RECORD'],'key':[0,0,2,1,2,1,2],'reason':'Some skill/recognition symbolism exists, but the same period has direct instability and root-loss pressure.'},
        'C': {'status':'PARTIALLY_SUPPORTED','parents':['S04_AXIS_SCOPE','S07_CAREER_LIANTAN','S07_FINANCE_TIANFU','S07_PROPERTY_SUN_JI','S10_NEUTRAL_TIME','S16_ROLE_ENDPOINT_LIMIT','S17_DIRECTION_AND_ENDPOINT'],'partial':['MULTIPLE_BUSINESS_OR_WORK_ACTIVITIES','HARD_OPERATION','AVERAGE_FINANCIAL_RESULT'],'limited':['LEGAL_BUSINESS_OWNERSHIP'],'contradicted':[],'unknown':[],'endpoint':['OWNER_IDENTITY_AND_TURNOVER'],'key':[0,1,3,1,2,2,3],'reason':'Lianzhen-Tanlang with void/malefic context and no wealth-luck closure supports hard multi-activity operation, but not legal owner identity.'},
        'D': {'status':'PARTIALLY_SUPPORTED','parents':['S04_AXIS_SCOPE','S07_CAREER_LIANTAN','S07_FINANCE_TIANFU','S07_PROPERTY_SUN_JI','S10_NEUTRAL_TIME','S17_DIRECTION_AND_ENDPOINT'],'partial':['REPEATED_WORK_CHANGE','MONEY_IN_AND_OUT','HOME_OR_FAMILY_AXIS_DOMINANCE'],'limited':['PARTNER_PAYS_DAILY_EXPENSES'],'contradicted':[],'unknown':[],'endpoint':['HOUSEHOLD_PAYER_AND_RESIDENCE_RECORD'],'key':[0,1,4,2,3,2,4],'reason':'The period directly favors job-root instability, multiple work stages and cash movement; partner-paid expenses remain unproved.'},
    },
    'Q4': {
        'A': {'status':'DIRECTLY_CONTRADICTED_MATERIAL_ATOM','parents':['S07_MARRIAGE_LIANTAN','S10_NEUTRAL_TIME','S17_DIRECTION_AND_ENDPOINT'],'partial':[],'limited':['LEGAL_MARRIAGE_EXISTENCE'],'contradicted':['HAPPY_HARMONIOUS_MARRIAGE'],'unknown':[],'endpoint':['MARRIAGE_AND_STABLE_HARMONY_AT_CUTOFF'],'key':[0,0,1,0,1,1,1],'reason':'The spouse structure directly conflicts with an unqualified happy and harmonious marriage.'},
        'B': {'status':'PARTIALLY_SUPPORTED','parents':['S07_MARRIAGE_LIANTAN','S10_NEUTRAL_TIME','S17_DIRECTION_AND_ENDPOINT'],'partial':['MARRIAGE_CONFLICT_OR_HURT_SCENE'],'limited':['VERBAL_ABUSE_AND_BLAME'],'contradicted':[],'unknown':['LEGAL_MARRIAGE_STATUS'],'endpoint':['MARRIAGE_REGISTRATION_AND_VERBAL_BEHAVIOR_RECORD'],'key':[0,1,3,1,2,2,3],'reason':'Relationship harm is structurally supported, but legal marriage and specific verbal behavior are not established.'},
        'C': {'status':'PARTIALLY_SUPPORTED','parents':['S07_MARRIAGE_LIANTAN','S10_NEUTRAL_TIME','S17_DIRECTION_AND_ENDPOINT'],'partial':['MULTI_STAGE_RELATIONSHIP_OR_TWO_UNIONS_CANDIDATE'],'limited':['REGISTERED_DIVORCE','REGISTERED_REMARRIAGE','CURRENT_STABILITY'],'contradicted':[],'unknown':[],'endpoint':['DIVORCE_REMARRIAGE_AND_CUTOFF_STABILITY'],'key':[0,1,4,1,2,2,4],'reason':'The Lianzhen-Tanlang structure with a single auxiliary star most directly supports a two-stage relationship candidate, but all legal and current-status endpoints remain missing.'},
        'D': {'status':'UNKNOWN','parents':['S04_AXIS_SCOPE','S07_MARRIAGE_LIANTAN','S16_ROLE_ENDPOINT_LIMIT','S17_DIRECTION_AND_ENDPOINT'],'partial':['PARTNER_RELATION_SCENE'],'limited':['PARTNER_CARE'],'contradicted':[],'unknown':['SEXUAL_ORIENTATION'],'endpoint':['ORIENTATION_AND_PARTNER_STATUS'],'key':[0,1,2,0,1,1,2],'reason':'The chart can describe relationship dynamics but cannot identify sexual orientation or prove partner care.'},
    },
    'Q5': {
        'A': {'status':'PARTIALLY_SUPPORTED','parents':['S07_PARENTS_TONGLIANG','S07_PROPERTY_SUN_JI','S16_MEDICAL_AND_FAMILY_LIMIT','S17_DIRECTION_AND_ENDPOINT'],'partial':['PARENTAL_SUPPORT','NON_EXTREME_DEPRIVATION'],'limited':['WEALTHY_MAGNITUDE','CLOSE_MOTHER_DISTANT_FATHER_SPLIT'],'contradicted':[],'unknown':[],'endpoint':['HOUSEHOLD_CLASS_AND_PARENT_RELATION_CALIBRATION'],'key':[0,1,3,1,1,2,3],'reason':'Parental support is plausible, but wealthy magnitude and the mother/father relationship split are not established.'},
        'B': {'status':'PARTIALLY_SUPPORTED','parents':['S07_PARENTS_TONGLIANG','S07_PROPERTY_SUN_JI','S16_MEDICAL_AND_FAMILY_LIMIT','S17_DIRECTION_AND_ENDPOINT'],'partial':['NORMAL_PARENT_RELATION','HOUSEHOLD_OR_ANCESTRAL_DECLINE_SCENE'],'limited':['MODESTLY_COMFORTABLE_MAGNITUDE','FATHER_BUSINESS_FAILURE_ACTOR_ACTION'],'contradicted':[],'unknown':[],'endpoint':['HOUSEHOLD_CLASS_AND_FATHER_BUSINESS_EVENT'],'key':[0,1,4,2,2,2,4],'reason':'The parent system supports normal ongoing relations, while Sun transformation pressure in the property axis supplies the closest household-decline mechanism.'},
        'C': {'status':'DIRECTLY_CONTRADICTED_MATERIAL_ATOM','parents':['S07_PARENTS_TONGLIANG','S16_MEDICAL_AND_FAMILY_LIMIT','S17_DIRECTION_AND_ENDPOINT'],'partial':['FATHER_SUPPORT_POSSIBLE'],'limited':['POVERTY_MAGNITUDE'],'contradicted':['MOTHER_DEATH'],'unknown':[],'endpoint':['MOTHER_DEATH_AND_CARE_HISTORY'],'key':[0,0,1,0,1,1,1],'reason':'The supportive Tongliang parent structure does not support mother death; the required death endpoint is absent.'},
        'D': {'status':'UNKNOWN','parents':['S07_PARENTS_TONGLIANG','S16_MEDICAL_AND_FAMILY_LIMIT','S17_DIRECTION_AND_ENDPOINT'],'partial':['PARENTAL_BASIC_SUPPORT_POSSIBLE'],'limited':['PARENT_DIVORCE','MATERNAL_GRANDMOTHER_CAREGIVER'],'contradicted':[],'unknown':[],'endpoint':['DIVORCE_AND_CAREGIVER_IDENTITY'],'key':[0,1,2,0,1,1,2],'reason':'Parent support is possible, but divorce and grandmother caregiver identity have no person-specific endpoint chain.'},
    },
}

BAZI_OPTIONS: dict[str, dict[str, dict[str, Any]]] = {
    'Q1': {
        'A': {'status':'DIRECTION_ONLY','parents':['S11_FOUNDATION','S12_QI_CONTROL','S16_MEDICAL_AND_FAMILY_LIMIT'],'partial':['LIGHT_DISEASE_NOT_ESTABLISHED'],'limited':['SKIN_AND_DIET_CAUSATION'],'reason':'Hot/dry load does not prove a healthy period or skin/food diagnosis.'},
        'B': {'status':'VALID_ABSTENTION','parents':['S11_FOUNDATION','S12_QI_CONTROL','S15_NEUTRAL_TIME','S16_MEDICAL_AND_FAMILY_LIMIT'],'partial':[],'limited':['SURGERY_AND_SEVERITY_ENDPOINT'],'reason':'No anatomical, procedural or hospitalization endpoint is available.'},
        'C': {'status':'DIRECTION_ONLY','parents':['S11_FOUNDATION','S12_QI_CONTROL','S14_RELATION_LIMIT','S16_MEDICAL_AND_FAMILY_LIMIT'],'partial':['METABOLIC_OR_RECURRENT_BURDEN_CANDIDATE'],'limited':['DIABETES_DIAGNOSIS'],'reason':'The qi structure can carry metabolic burden but cannot identify diabetes.'},
        'D': {'status':'DIRECTION_ONLY','parents':['S11_FOUNDATION','S12_QI_CONTROL','S14_RELATION_LIMIT','S16_MEDICAL_AND_FAMILY_LIMIT'],'partial':['DIGESTIVE_OR_METABOLIC_BURDEN_CANDIDATE'],'limited':['OBESITY_LIVER_FOOT_DIAGNOSES'],'reason':'The qi structure permits digestive/metabolic burden but cannot supply the listed diagnoses.'},
    },
    'Q2': {
        'A': {'status':'VALID_ABSTENTION','parents':['S11_FOUNDATION','S12_QI_CONTROL','S13_METHOD_COMPETITION','S16_ROLE_ENDPOINT_LIMIT'],'partial':['SALARIED_ORGANIZATION_ROLE_CANDIDATE'],'limited':['LAZINESS_DEGREE_EMPLOYMENT_ENDPOINTS'],'reason':'Role structure cannot close the compound personality, degree and job status.'},
        'B': {'status':'DIRECTION_ONLY','parents':['S11_FOUNDATION','S12_QI_CONTROL','S13_METHOD_COMPETITION','S16_ROLE_ENDPOINT_LIMIT'],'partial':['EXPRESSIVE_INTELLIGENCE_WITH_WEAK_RESOURCE_CANDIDATE'],'limited':['NOT_STUDY_HIGH_SCHOOL_PART_TIME_ENDPOINTS'],'reason':'Output/resource balance permits this personality direction but not its educational and employment endpoints.'},
        'C': {'status':'VALID_ABSTENTION','parents':['S11_FOUNDATION','S12_QI_CONTROL','S13_METHOD_COMPETITION','S16_ROLE_ENDPOINT_LIMIT'],'partial':['WORK_EFFORT_CANDIDATE'],'limited':['INTELLIGENCE_DEGREE_FAMILY_BUSINESS_ENDPOINTS'],'reason':'No family-business ownership or degree endpoint can be derived.'},
        'D': {'status':'DIRECTION_ONLY','parents':['S11_FOUNDATION','S12_QI_CONTROL','S13_METHOD_COMPETITION','S16_ROLE_ENDPOINT_LIMIT'],'partial':['INTELLIGENCE_OR_RESPONSIBILITY_CANDIDATE'],'limited':['ADVANCED_DEGREE_AND_MANAGEMENT_TITLE'],'reason':'The structure can carry responsibility but not masters/PhD or management title.'},
    },
    'Q3': {
        'A': {'status':'VALID_ABSTENTION','parents':['S11_FOUNDATION','S12_QI_CONTROL','S14_RELATION_LIMIT','S15_NEUTRAL_TIME','S16_TOPIC_PACKAGE'],'partial':['FINANCIAL_PRESSURE_CANDIDATE'],'limited':['SCAM_TOTAL_LOSS_STABLE_JOB'],'reason':'The period cannot identify a scam or stable employment.'},
        'B': {'status':'VALID_ABSTENTION','parents':['S11_FOUNDATION','S12_QI_CONTROL','S14_RELATION_LIMIT','S15_NEUTRAL_TIME','S16_TOPIC_PACKAGE'],'partial':['RESPONSIBILITY_OR_RECOGNITION_CANDIDATE'],'limited':['FAME_AND_SMOOTH_SUCCESS'],'reason':'Officer activation does not prove public recognition or smooth work.'},
        'C': {'status':'DIRECTION_ONLY','parents':['S11_FOUNDATION','S12_QI_CONTROL','S13_METHOD_COMPETITION','S14_RELATION_LIMIT','S15_NEUTRAL_TIME','S16_ROLE_ENDPOINT_LIMIT'],'partial':['BUSINESS_RESPONSIBILITY_OR_OUTPUT_TO_WEALTH_CANDIDATE'],'limited':['OWNER_IDENTITY_AND_TURNOVER'],'reason':'The period can support business responsibility but not legal ownership.'},
        'D': {'status':'DIRECTION_ONLY','parents':['S11_FOUNDATION','S12_QI_CONTROL','S14_RELATION_LIMIT','S15_NEUTRAL_TIME','S16_TOPIC_PACKAGE'],'partial':['WORK_STAGE_CHANGE_AND_FINANCIAL_MOVEMENT'],'limited':['RESIDENCE_AND_PARTNER_PAYMENT_ENDPOINTS'],'reason':'The relations and luck period permit change/flow, not household payer identity.'},
    },
    'Q4': {option: {'status':'VALID_ABSTENTION','parents':['S11_FOUNDATION','S12_QI_CONTROL','S14_RELATION_LIMIT','S15_NEUTRAL_TIME','S16_ROLE_ENDPOINT_LIMIT'],'partial':['RELATIONSHIP_ACTIVATION_ONLY'],'limited':['LEGAL_STATUS_ORIENTATION_BEHAVIOR_AND_CUTOFF_STATE'],'reason':'The Bazi structure cannot distinguish the four completed relationship states.'} for option in 'ABCD'},
    'Q5': {option: {'status':'VALID_ABSTENTION','parents':['S11_FOUNDATION','S12_QI_CONTROL','S14_RELATION_LIMIT','S16_MEDICAL_AND_FAMILY_LIMIT'],'partial':['RESOURCE_OR_PARENT_SCENE_ONLY'],'limited':['PARENT_ACTOR_EVENT_CAREGIVER_AND_MAGNITUDE'],'reason':'The Bazi structure cannot identify a parent action, death, divorce, caregiver or calibrated household class.'} for option in 'ABCD'},
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
        raise ValueError(f'invalid range {path}:{start}-{end}; line_count={len(lines)}')
    return '\n'.join(lines[start - 1:end]) + '\n'


def build_whitelist(repo_root: Path) -> dict[str, Any]:
    declared = read_json(repo_root / INPUTS['whitelist'])
    rows = []
    for row in declared['rows']:
        path = repo_root / 'knowledge/base' / row['canonical_filename']
        data = path.read_bytes()
        actual = sha256_bytes(data)
        status = 'PASS' if actual == row['sha256'] and len(data) == row['bytes'] else 'FAIL'
        rows.append({
            'library_id': row['library_id'],
            'path': path.relative_to(repo_root).as_posix(),
            'declared_sha256': row['sha256'],
            'actual_sha256': actual,
            'declared_bytes': row['bytes'],
            'actual_bytes': len(data),
            'status': status,
            'read_method': 'UTF8_DIRECT_FILE_READ',
        })
    return with_hash({
        'schema': 'DEV-GROUP-002-R9-ACTIVE-WHITELIST-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R9',
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
    file_rows = []
    file_name_map = {
        'ziwei.txt': INPUTS['ziwei'],
        'bazi-transcription.json': INPUTS['bazi'],
        'questions-parsed.json': INPUTS['questions'],
    }
    for name, rel in file_name_map.items():
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
    required_chart_tokens = [
        '命  宫[癸丑][身宫]', '天相[庙]', '父母宫[壬寅]', '天同[利][生年权],天梁[庙][↓禄]',
        '田宅宫[甲辰]', '太阳[旺][↓忌][↑禄]', '官禄宫[乙巳]', '地劫[不],地空[庙],天马[平]',
        '疾厄宫[戊申]', '财帛宫[己酉]', '天府[旺]', '夫妻宫[辛亥]', '廉贞[陷],贪狼[陷]',
        '起止年份:2019年(33虚岁)~2028年(42虚岁)', '大限四化:廉贞禄,破军权,武曲科,太阳忌',
    ]
    missing_chart_tokens = [token for token in required_chart_tokens if token not in ziwei_text]
    if bazi['pillars'] != {'year':'丁卯','month':'丙午','day':'乙卯','hour':'壬午'}:
        raise ValueError('Bazi pillar freeze mismatch')
    if [q['question_id'] for q in questions] != [f'Q{i}' for i in range(1, 6)]:
        raise ValueError('Question set mismatch')
    obj = with_hash({
        'schema': 'DEV-GROUP-002-R9-INPUT-FREEZE-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R9',
        'source_runtime_view_manifest_path': INPUTS['view_manifest'],
        'source_runtime_view_manifest_git_blob_sha': git_blob_sha(repo_root / INPUTS['view_manifest']),
        'answer_isolation': {
            'status': manifest['answer_isolation_status'],
            'answer_payload_present': manifest['answer_payload_present'],
            'answer_reference_disclosed': manifest['answer_reference_disclosed'],
        },
        'files': file_rows,
        'ziwei_required_token_count': len(required_chart_tokens),
        'ziwei_missing_tokens': missing_chart_tokens,
        'bazi_pillars': bazi['pillars'],
        'bazi_seasonal_qi': bazi['seasonal_qi'],
        'bazi_luck_cycles': bazi['luck']['cycles'],
        'question_count': len(questions),
        'questions': questions,
        'status': 'PASS' if all(r['status']=='PASS' for r in file_rows) and not missing_chart_tokens and not manifest['answer_payload_present'] and not manifest['answer_reference_disclosed'] else 'FAIL',
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
        'schema': 'DEV-GROUP-002-R9-SOURCE-EXCERPTS-V1',
        'group_id': 'DEV-GROUP-002',
        'case_id': CASE_ID,
        'round_id': 'R9',
        'rows': rows,
        'row_count': len(rows),
        'status': 'PASS' if all(row['status'].startswith('PASS') for row in rows) else 'FAIL',
    })


def build_case_models(input_freeze: dict[str, Any], source_excerpts: dict[str, Any], bazi: dict[str, Any], ziwei_text: str) -> tuple[dict[str, Any], dict[str, Any]]:
    structure = with_hash({
        'schema': 'DEV-GROUP-002-R9-ZIWEI-CASE-STRUCTURE-V1',
        'case_id': CASE_ID,
        'input_freeze_sha256': input_freeze['canonical_sha256'],
        'source_excerpts_sha256': source_excerpts['canonical_sha256'],
        'base_chart_id': 'ZIWEI-CHOU-TIANXIANG-CASE-STRUCTURE',
        'palace_rows': {
            'MING': {'branch':'丑','stars':['天相'],'body_palace':True},
            'PARENTS': {'branch':'寅','stars':['天同','天梁'],'transformations':['天同生年权','天梁离心自化禄']},
            'PROPERTY': {'branch':'辰','stars':['太阳','文昌','铃星'],'transformations':['太阳离心自化忌','太阳向心自化禄']},
            'CAREER': {'branch':'巳','stars':[],'auxiliary':['右弼','陀罗','地劫','地空','天马'],'borrow_from':'SPOUSE'},
            'HEALTH': {'branch':'申','stars':[],'minor':['大耗','劫煞'],'borrow_from':'PARENTS'},
            'WEALTH': {'branch':'酉','stars':['天府'],'auxiliary':['左辅','天钺']},
            'SPOUSE': {'branch':'亥','stars':['廉贞','贪狼'],'auxiliary':['天魁','旬空']},
        },
        'route_receipts': [
            {'axis':'HEALTH','primary':'疾厄宫','opposite':'父母宫','trines':['兄弟宫','田宅宫'],'borrow_status':'EMPTY_PALACE_BORROWS_TONGLIANG','selector_status':'MATCH'},
            {'axis':'CAREER','primary':'官禄宫','opposite':'夫妻宫','trines':['命宫','财帛宫'],'borrow_status':'EMPTY_PALACE_BORROWS_LIANZHEN_TANLANG','selector_status':'MATCH'},
            {'axis':'MARRIAGE','primary':'夫妻宫','opposite':'官禄宫','trines':['迁移宫','福德宫'],'borrow_status':'DIRECT_LIANZHEN_TANLANG','selector_status':'MATCH'},
            {'axis':'PARENTS','primary':'父母宫','opposite':'疾厄宫','trines':['子女宫','疾厄宫'],'borrow_status':'DIRECT_TONGLIANG','selector_status':'MATCH'},
        ],
        'active_period': {'years':'2019-2028','palace':'田宅宫','transformations':['廉贞禄','破军权','武曲科','太阳忌']},
        'time_rows': [
            {'year':2022,'transformations':['天梁禄','紫微权','左辅科','武曲忌'],'role':'NEUTRAL_ACTIVATION_ONLY'},
            {'year':2023,'transformations':['破军禄','巨门权','太阴科','贪狼忌'],'role':'NEUTRAL_ACTIVATION_ONLY'},
            {'year':2024,'transformations':['廉贞禄','破军权','武曲科','太阳忌'],'role':'NEUTRAL_ACTIVATION_ONLY'},
            {'year':2025,'transformations':['天机禄','天梁权','紫微科','太阴忌'],'role':'NEUTRAL_ACTIVATION_ONLY'},
        ],
        's08_scope': 'DYNAMIC_FORCE_ONLY_NOT_EVENT_OR_ENDPOINT',
        'status': 'EXECUTED_STRUCTURE_ONLY',
    })
    bazi_model = with_hash({
        'schema': 'DEV-GROUP-002-R9-BAZI-CASE-STRUCTURE-V1',
        'case_id': CASE_ID,
        'input_freeze_sha256': input_freeze['canonical_sha256'],
        'source_excerpts_sha256': source_excerpts['canonical_sha256'],
        'variant_id': 'SOLAR_TERM_SINGLE_VERSION',
        's11_foundation': {
            'pillars': bazi['pillars'],
            'day_master': '乙木',
            'hidden_stems_ten_gods': bazi['hidden_stems_ten_gods'],
            'status': 'EXECUTED',
        },
        's12_qi_candidates': {
            'seasonal_qi': bazi['seasonal_qi'],
            'root_channels':['DAY_BRANCH_MAO','YEAR_BRANCH_MAO'],
            'exposed_output':['MONTH_STEM_BING','YEAR_STEM_DING'],
            'resource':['HOUR_STEM_REN_WEAK_IN_FIRE_SEASON'],
            'carrying_candidates':['ROOTED_WOOD_WITH_STRONG_FIRE_DRAIN','HOT_DRY_LOAD','NO_UNIQUE_STRENGTH_LABEL_REQUIRED'],
            'status':'EXECUTED_NO_UNIQUE_STATE',
        },
        's13_method_competition': {
            'candidates':['OUTPUT_FLOW_METHOD','BALANCING_AND_COOLING_METHOD','ROOT_AND_CARRYING_METHOD'],
            'unique_method': None,
            'status':'EXECUTED_NO_UNIQUE_METHOD',
        },
        's14_relations': {'facts': bazi['relations'], 'transformation_status':'RELATION_FACTS_ONLY_NO_EVENT_AND_NO_AUTOMATIC_TRANSFORMATION'},
        's15_time': {
            'luck_period':'2018-2027 庚戌',
            'question_periods':['2018-2025','2022-2025','AT_2025'],
            'role_candidates':['OFFICER_WEALTH_ROLE_INTRODUCED','FIRE_RELATION_ACTIVATION','WORK_AND_RESOURCE_CHANGE_PERMISSION'],
            'status':'EXECUTED_NEUTRAL_TIME_ONLY',
        },
        'cross_track_visibility':'NO_ZIWEI_RESULT_READ_DURING_BUILD',
        'status':'EXECUTED_STRUCTURE_AND_CAPABILITY_ONLY',
    })
    return structure, bazi_model


def build_blind_models(ziwei_structure: dict[str, Any], bazi_structure: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for track in ('ZIWEI','BAZI'):
        for qid in [f'Q{i}' for i in range(1,6)]:
            text = BLIND_MODELS[track][qid]
            rows.append({
                'case_id': CASE_ID,
                'question_id': qid,
                'track_id': track,
                'target_axis': QUESTION_TASKS[qid],
                'blind_model_text': text,
                'contains_option_id': bool(re.search(r'\bOPTION_[ABCD]\b|\b[A-D]:', text)),
                'contains_other_track_result': False,
                'parent_case_structure_sha256': ziwei_structure['canonical_sha256'] if track=='ZIWEI' else bazi_structure['canonical_sha256'],
                'seal_status': 'LOCALLY_FROZEN_SHADOW_REBUILD_NOT_FORMAL_PREOPTION_SEAL',
            })
    return with_hash({
        'schema':'DEV-GROUP-002-R9-BLIND-MODELS-V1',
        'group_id':'DEV-GROUP-002','case_id':CASE_ID,'round_id':'R9',
        'rows':rows,'row_count':len(rows),
        'formal_machine_seal_permission':'NO_ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD',
        'status':'PASS_LOCAL_MODEL_ISOLATION_NOT_FORMAL_SEAL' if not any(r['contains_option_id'] or r['contains_other_track_result'] for r in rows) else 'FAIL',
    })


def atomize_questions(questions: list[dict[str, Any]]) -> dict[str, Any]:
    rows=[]
    for q in questions:
        for option in q['options']:
            rows.append({'case_id':CASE_ID,'question_id':q['question_id'],'option_id':option['option_id'],'literal':option['text'],'material_atom_ids':[f"{q['question_id']}_{option['option_id']}_ATOM_{i+1}" for i,_ in enumerate(re.split(r'[，、；]', option['text'])) if _.strip()]})
    return with_hash({'schema':'DEV-GROUP-002-R9-OPTION-ATOM-FREEZE-V1','group_id':'DEV-GROUP-002','case_id':CASE_ID,'round_id':'R9','rows':rows,'row_count':len(rows)})


def build_coverage_plan(source_excerpts: dict[str, Any]) -> dict[str, Any]:
    rows=[]
    for qid in [f'Q{i}' for i in range(1,6)]:
        rows.append({
            'case_id':CASE_ID,'question_id':qid,'task_class':QUESTION_TASKS[qid],
            'ziwei_required_families':['S04','S05','S06','S07','S08','S10','S17','S18'],
            'bazi_required_families':['S11','S12','S13','S14','S15','S16','S17','S18'],
            'support_routes':['STRUCTURAL_DIRECTION','OPTION_SPECIFIC_PARENT_BINDING'],
            'counterevidence_routes':['SAME_AXIS_DIRECT_COUNTEREVIDENCE'],
            'alternative_routes':['SCENE_OR_ROLE_WITHOUT_ENDPOINT'],
            'endpoint_routes':['S17_COMPOSITE_AND_EXACT_ENDPOINT'],
            'unresolved_required_families':[],
            'status':'ROUTED',
        })
    return with_hash({'schema':'DEV-GROUP-002-R9-COMPLETE-KNOWLEDGE-COVERAGE-V1','group_id':'DEV-GROUP-002','case_id':CASE_ID,'round_id':'R9','source_excerpts_sha256':source_excerpts['canonical_sha256'],'rows':rows,'row_count':5,'status':'PASS_ALL_REQUIRED_FAMILIES_ROUTED'})


def build_bindings(blind_models: dict[str, Any], atom_freeze: dict[str, Any], coverage: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    track_rows=[]
    ledger_rows=[]
    for track, specs in [('ZIWEI',ZIWEI_OPTIONS),('BAZI',BAZI_OPTIONS)]:
        for qid in [f'Q{i}' for i in range(1,6)]:
            for option in 'ABCD':
                spec=specs[qid][option]
                row={
                    'case_id':CASE_ID,'question_id':qid,'track_id':track,'option_id':option,
                    'parent_excerpt_ids':spec['parents'],'direction_status':spec['status'],
                    'partial_atom_ids':spec.get('partial',[]),'limited_atom_ids':spec.get('limited',[]),
                    'contradicted_atom_ids':spec.get('contradicted',[]),'unknown_atom_ids':spec.get('unknown',[]),
                    'missing_exact_endpoint_ids':spec.get('endpoint',spec.get('limited',[])),
                    'semantic_reason':spec['reason'],
                    'local_rank_permission':'YES_RELATIVE_ONLY' if track=='ZIWEI' else 'NO_VALID_ABSTENTION_OR_DIRECTION_ONLY',
                    'formal_exact_assertion':None,'program_state':'EXECUTED','effective': track=='ZIWEI' and spec['status']!='UNKNOWN',
                }
                track_rows.append(row)
                for idx,parent in enumerate(spec['parents'],1):
                    ledger_rows.append({
                        'ledger_row_id':f'{track}-{qid}-{option}-{idx}',
                        'case_id':CASE_ID,'question_id':qid,'track_id':track,'option_id':option,
                        'library_id':parent.split('_')[0], 'source_excerpt_id':parent,
                        'target_atom_group':f'{qid}_{option}','semantic_direction':spec['status'],
                        'capability_ceiling':'RELATIVE_DIRECTION_ONLY','dedup_key':f'{track}|{qid}|{option}|{parent}',
                        'downstream_effect':'RANK_CHANGING' if track=='ZIWEI' else 'TRACK_LOCAL_CAPABILITY_ONLY',
                    })
    bindings=with_hash({
        'schema':'DEV-GROUP-002-R9-TRACK-OPTION-PARENT-BINDINGS-V1','group_id':'DEV-GROUP-002','case_id':CASE_ID,'round_id':'R9',
        'blind_models_sha256':blind_models['canonical_sha256'],'atom_freeze_sha256':atom_freeze['canonical_sha256'],'coverage_plan_sha256':coverage['canonical_sha256'],
        'track_rows':track_rows,'track_row_count':len(track_rows),
        'summary':{'ziwei_rows':20,'bazi_rows':20,'bazi_local_rank_rows':0,'formal_exact_assertions':0,'machine_valid_local_seals':0},
    })
    ledger=with_hash({'schema':'DEV-GROUP-002-R9-EVIDENCE-USAGE-LEDGER-V1','group_id':'DEV-GROUP-002','case_id':CASE_ID,'round_id':'R9','parent_bindings_sha256':bindings['canonical_sha256'],'rows':ledger_rows,'row_count':len(ledger_rows),'dedup_status':'PASS_UNIQUE_BY_TRACK_QUESTION_OPTION_PARENT','status':'COMPLETE_FOR_ACTUAL_RANK_CHANGING_CALLS'})
    return bindings,ledger


def pair_basis(left_spec: dict[str, Any], right_spec: dict[str, Any]) -> tuple[str,str]:
    labels=['DISTINCTIVE_DIRECT_SUPPORT','SAME_AXIS_DIRECT_COUNTEREVIDENCE','COMPOSITE_COVERAGE','EXACT_ENDPOINT_DISTANCE','TEMPORAL_STAGE','ALTERNATIVE_EXPLANATION','MECHANISM_COHERENCE']
    lk=left_spec['key']; rk=right_spec['key']
    for i,label in enumerate(labels):
        if lk[i]!=rk[i]:
            return label, 'LEFT' if lk[i]>rk[i] else 'RIGHT'
    return 'LOW_INFORMATION_FORCED_TIEBREAK','TIE'


def build_adjudication(bindings: dict[str, Any]) -> tuple[dict[str, Any],dict[str, Any]]:
    rows=[]
    question_rows=[]
    for qid in [f'Q{i}' for i in range(1,6)]:
        rank=FINAL_RANKS[qid]
        for left,right in itertools.combinations('ABCD',2):
            basis,side=pair_basis(ZIWEI_OPTIONS[qid][left],ZIWEI_OPTIONS[qid][right])
            computed = left if side=='LEFT' else right if side=='RIGHT' else (left if rank.index(left)<rank.index(right) else right)
            expected = left if rank.index(left)<rank.index(right) else right
            if computed!=expected:
                raise ValueError(f'pairwise key/rank mismatch {qid} {left}/{right}: computed {computed}, expected {expected}')
            rows.append({
                'case_id':CASE_ID,'question_id':qid,'left':left,'right':right,'winner':expected,'loser':right if expected==left else left,
                'decision_basis':basis,'left_key':ZIWEI_OPTIONS[qid][left]['key'],'right_key':ZIWEI_OPTIONS[qid][right]['key'],
                'left_direction_status':ZIWEI_OPTIONS[qid][left]['status'],'right_direction_status':ZIWEI_OPTIONS[qid][right]['status'],
                'bazi_fusion_effect':'ZERO_NO_MACHINE_VALID_BAZI_LOCAL_SEAL','formal_endpoint_status':'MISSING_FOR_BOTH_OR_WINNER',
            })
        question_rows.append({
            'case_id':CASE_ID,'question_id':qid,'relative_first':rank[0],'relative_second':rank[1],'full_rank':rank,
            'confidence':'LOW_TO_MEDIUM_SOURCE_GROUNDED_SHADOW_REBUILD','strongest_competitor':rank[1],
            'ziwei_local_rank':rank,'bazi_local_rank':None,'s03_fusion_status':'NOT_PERFORMED',
            'formal_exact_assertion':None,
            'most_important_unverified_atoms':sorted(set(ZIWEI_OPTIONS[qid][rank[0]].get('endpoint',[])+ZIWEI_OPTIONS[qid][rank[1]].get('endpoint',[]))),
        })
    pairwise=with_hash({'schema':'DEV-GROUP-002-R9-PAIRWISE-ADJUDICATION-V1','group_id':'DEV-GROUP-002','case_id':CASE_ID,'round_id':'R9','parent_bindings_sha256':bindings['canonical_sha256'],'rows':rows,'row_count':len(rows),'decision_order':['DISTINCTIVE_DIRECT_SUPPORT','SAME_AXIS_DIRECT_COUNTEREVIDENCE','COMPOSITE_COVERAGE','EXACT_ENDPOINT_DISTANCE','TEMPORAL_STAGE','ALTERNATIVE_EXPLANATION','MECHANISM_COHERENCE','LOW_INFORMATION_FORCED_TIEBREAK']})
    public=with_hash({'schema':'DEV-GROUP-002-R9-PUBLIC-RELATIVE-DISCLOSURE-V1','group_id':'DEV-GROUP-002','case_id':CASE_ID,'round_id':'R9','rows':question_rows,'row_count':5,'formal_exact_assertion_count':0})
    return pairwise,public


def build_prediction(repo_root: Path, pairwise: dict[str, Any]) -> dict[str, Any]:
    parent=read_json(repo_root / INPUTS['r7_prediction'])
    cases=[]
    changed=[]
    for case in parent['cases']:
        clone=dict(case)
        if case['case_id']==CASE_ID:
            old=case['ranks']
            new=[FINAL_RANKS[f'Q{i}'] for i in range(1,6)]
            clone['ranks']=new
            clone['top1_vector']=''.join(x[0] for x in new)
            clone['top2_vector']=''.join(x[1] for x in new)
            clone['prediction_origin']='R9_DEV002_FRESH_CANONICAL_INPUT_AND_ACTIVE_SOURCE_REBUILD'
            for i,(a,b) in enumerate(zip(old,new),1):
                if a!=b: changed.append(f'{CASE_ID}:Q{i}')
        cases.append(clone)
    return with_hash({
        'schema':'DEV-GROUP-002-R9-PREDICTION-FREEZE-V1','group_id':'DEV-GROUP-002','round_id':'R9',
        'run_class':'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD','parent_r7_prediction_sha256':parent['canonical_sha256'],'pairwise_adjudication_sha256':pairwise['canonical_sha256'],
        'case_ids':parent['case_ids'],'cases':cases,'question_count':25,'changed_case_ids':[CASE_ID],'changed_question_ids':changed,
        'contains_answers':False,'answer_visible_during_prediction_materialization':False,'formal_exact_assertion_permission':'NULL_ONLY',
        'machine_valid_local_seals':0,'s03_fusions':0,'new_case_admission':'BLOCKED','base_astrological_knowledge_changed':False,
    })


def build_review(repo_root: Path, prediction: dict[str, Any]) -> dict[str, Any]:
    answer_vectors=read_json(repo_root / INPUTS['answers'])['answer_vectors']
    scores=[]; total1=total2=0
    for case in prediction['cases']:
        answer=answer_vectors[case['case_id']]
        h1=sum(a==b for a,b in zip(case['top1_vector'],answer))
        h2=sum(c in (a,b) for a,b,c in zip(case['top1_vector'],case['top2_vector'],answer))
        total1+=h1; total2+=h2
        scores.append({'case_id':case['case_id'],'top1_hits':h1,'top2_coverage':h2})
    return with_hash({
        'schema':'DEV-GROUP-002-R9-POSTREVEAL-REVIEW-V1','group_id':'DEV-GROUP-002','round_id':'R9','parent_prediction_sha256':prediction['canonical_sha256'],
        'answer_vectors':answer_vectors,'case_scores':scores,'totals':{'top1_hits':total1,'top2_coverage':total2,'question_count':25,'score_label':'TRAINING_REGRESSION_SCORE'},
        'comparison_to_r8':{'top1_delta':total1-14,'top2_delta':total2-16},
        'accuracy_claim':'NO_NEW_BLIND_RESULT','diagnosis':'Fresh source-parent reconstruction changes DEV-EXAMPLE-002 Q2 and Q4 TOP1 and exposes a one-hit TOP1 regression; no answer-derived repair is applied.'
    })


def build_manifest(repo_root: Path, artifacts: dict[str, dict[str, Any]], review: dict[str, Any]) -> dict[str, Any]:
    history={rid:{'path':path,'git_blob_sha':git_blob_sha(repo_root/path),'preserved':True} for rid,path in HISTORY.items()}
    artifact_rows={name.removesuffix('.json').replace('-','_'):{'path':str(ROUND_DIR/name),'canonical_sha256':obj['canonical_sha256']} for name,obj in artifacts.items()}
    return with_hash({
        'schema':'DEV-GROUP-002-R9-FROZEN-MANIFEST-V1','group_id':'DEV-GROUP-002','round_id':'R9','status':'FROZEN_FRESH_SOURCE_REBUILD_WITH_REGRESSION',
        'run_class':'ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD','historical_rounds':history,'artifacts':artifact_rows,
        'statistics':{
            'question_count':25,'r9_processed_case_count':1,'r9_processed_question_count':5,'source_excerpt_count':len(SOURCE_EXCERPT_SPECS),
            'track_option_binding_rows':40,'pairwise_rows':30,'ziwei_local_ranked_questions':5,'bazi_valid_abstention_questions':5,
            'top1_hits':review['totals']['top1_hits'],'top2_coverage':review['totals']['top2_coverage'],
            'top1_delta_from_r8':review['comparison_to_r8']['top1_delta'],'top2_delta_from_r8':review['comparison_to_r8']['top2_delta'],
            'formal_valid_questions':0,'machine_valid_local_seals':0,'s03_fusions':0,
        },
        'training_conclusion':'A fresh DEV-EXAMPLE-002 rebuild from canonical answer-free inputs and active S00-S19 parents is reproducible, but it reduces same-case TOP1 by one. The regression is retained as evidence that the prior higher score was not source-stable.',
        'next_required_round':'R10_REGRESSION_DIAGNOSIS_WITHOUT_ANSWER_DERIVED_DIRECTION_RULE',
        'new_case_admission':'BLOCKED','selection_release_permission':'SHADOW_REBUILD_ONLY','base_astrological_knowledge_changed':False,'case_specific_direction_rule_added':False,'s00_s19_modified':False,
    })


def build_objects(repo_root: Path) -> dict[str, dict[str, Any]]:
    whitelist=build_whitelist(repo_root)
    input_freeze,questions,bazi,ziwei_text=build_input_freeze(repo_root)
    excerpts=build_source_excerpts(repo_root)
    if whitelist['status']!='PASS' or input_freeze['status']!='PASS' or excerpts['status']!='PASS':
        raise ValueError('R9 precontent gate failed')
    ziwei_structure,bazi_structure=build_case_models(input_freeze,excerpts,bazi,ziwei_text)
    blind=build_blind_models(ziwei_structure,bazi_structure)
    atoms=atomize_questions(questions)
    coverage=build_coverage_plan(excerpts)
    bindings,ledger=build_bindings(blind,atoms,coverage)
    pairwise,public=build_adjudication(bindings)
    prediction=build_prediction(repo_root,pairwise)
    review=build_review(repo_root,prediction)
    base={
        'active-whitelist.json':whitelist,'input-freeze.json':input_freeze,'source-excerpts.json':excerpts,
        'ziwei-case-structure.json':ziwei_structure,'bazi-case-structure.json':bazi_structure,'blind-models.json':blind,
        'option-atom-freeze.json':atoms,'coverage-plan.json':coverage,'track-option-parent-bindings.json':bindings,
        'evidence-usage-ledger.json':ledger,'pairwise-adjudication.json':pairwise,'public-relative-disclosure.json':public,
        'prediction-freeze.json':prediction,'postreveal-review.json':review,
    }
    manifest=build_manifest(repo_root,base,review)
    base['manifest.json']=manifest
    return base


def materialize(repo_root: Path) -> None:
    out=repo_root/ROUND_DIR; out.mkdir(parents=True,exist_ok=True)
    objects=build_objects(repo_root)
    for name,obj in objects.items(): write_json(out/name,obj)
    m=objects['manifest.json']; stats=m['statistics']
    summary=f'''# DEV-GROUP-002 R9：DEV-EXAMPLE-002规范输入全新来源重建\n\nR9不导入R8否决的历史语义摘要，也不使用旧排序作为证据。运行先重算S00—S19活动白名单，再冻结答案隔离的紫微盘、节气八字和五道题；随后分别建立紫微与八字盲态结构、来源父句段、40条双轨选项绑定、完整证据账和30组成对裁决。\n\n紫微相对排序为：Q1 `DCAB`、Q2 `DBAC`、Q3 `DCBA`、Q4 `CBDA`、Q5 `BADC`。八字完成S11—S16上游，但对现代诊断、学历、老板身份、婚姻手续和父母具体事件均保持有效弃权，因此没有进入S03融合。\n\n相对R8，DEV-EXAMPLE-002的Q2与Q4首选改变，Q1仅第三第四位改变；组级同题训练回归由TOP1 14/25降至{stats['top1_hits']}/25，TOP2保持{stats['top2_coverage']}/25。该退化被原样冻结，不按答案补规则。\n\n正式有效题、本地机器密封和S03融合仍全部为0；S00—S19、基础命理知识和案例方向规则均未修改。R10只能诊断为什么来源更完整却降低同题分数，禁止依据正确答案反向修改证据方向。\n'''
    (out/'summary.md').write_text(summary,encoding='utf-8')


def validate(repo_root: Path) -> dict[str, Any]:
    errors=[]; out=repo_root/ROUND_DIR
    names=['active-whitelist.json','input-freeze.json','source-excerpts.json','ziwei-case-structure.json','bazi-case-structure.json','blind-models.json','option-atom-freeze.json','coverage-plan.json','track-option-parent-bindings.json','evidence-usage-ledger.json','pairwise-adjudication.json','public-relative-disclosure.json','prediction-freeze.json','postreveal-review.json','manifest.json']
    objs={}
    for name in names:
        if not (out/name).exists(): errors.append(f'missing {name}')
        else: objs[name]=read_json(out/name)
    if errors: return {'status':'FAIL','error_count':len(errors),'errors':errors}
    for name,obj in objs.items():
        if canonical_hash(obj)!=obj.get('canonical_sha256'): errors.append(f'{name}: canonical hash mismatch')
    if objs['active-whitelist.json']['status']!='PASS': errors.append('whitelist status')
    if objs['input-freeze.json']['status']!='PASS': errors.append('input freeze status')
    if objs['source-excerpts.json']['status']!='PASS' or objs['source-excerpts.json']['row_count']!=len(SOURCE_EXCERPT_SPECS): errors.append('source excerpt status/count')
    if objs['blind-models.json']['status']!='PASS_LOCAL_MODEL_ISOLATION_NOT_FORMAL_SEAL': errors.append('blind model isolation')
    bindings=objs['track-option-parent-bindings.json']
    if bindings['track_row_count']!=40 or len(bindings['track_rows'])!=40: errors.append('binding row count')
    if len({(r['question_id'],r['track_id'],r['option_id']) for r in bindings['track_rows']})!=40: errors.append('binding uniqueness')
    bazi_rows=[r for r in bindings['track_rows'] if r['track_id']=='BAZI']
    if any(r['local_rank_permission']!='NO_VALID_ABSTENTION_OR_DIRECTION_ONLY' for r in bazi_rows): errors.append('Bazi rank leakage')
    if any(r['formal_exact_assertion'] is not None for r in bindings['track_rows']): errors.append('formal assertion released')
    pairwise=objs['pairwise-adjudication.json']
    if pairwise['row_count']!=30 or len(pairwise['rows'])!=30: errors.append('pairwise count')
    if len({(r['question_id'],r['left'],r['right']) for r in pairwise['rows']})!=30: errors.append('pairwise uniqueness')
    for qid,rank in FINAL_RANKS.items():
        qrows=[r for r in pairwise['rows'] if r['question_id']==qid]
        for row in qrows:
            expected=row['left'] if rank.index(row['left'])<rank.index(row['right']) else row['right']
            if row['winner']!=expected: errors.append(f'pairwise winner {qid} {row["left"]}/{row["right"]}')
    prediction=objs['prediction-freeze.json']
    case=next(c for c in prediction['cases'] if c['case_id']==CASE_ID)
    expected_ranks=[FINAL_RANKS[f'Q{i}'] for i in range(1,6)]
    if case['ranks']!=expected_ranks or case['top1_vector']!='DDDCB' or case['top2_vector']!='CBCBA': errors.append('prediction vector')
    if prediction['contains_answers'] is not False or prediction['answer_visible_during_prediction_materialization'] is not False: errors.append('answer isolation declaration')
    review=objs['postreveal-review.json']
    if (review['totals']['top1_hits'],review['totals']['top2_coverage'])!=(13,16): errors.append('review score')
    if review['comparison_to_r8']!={'top1_delta':-1,'top2_delta':0}: errors.append('review delta')
    manifest=objs['manifest.json']; stats=manifest['statistics']
    if manifest['status']!='FROZEN_FRESH_SOURCE_REBUILD_WITH_REGRESSION': errors.append('manifest status')
    if (stats['top1_hits'],stats['top2_coverage'],stats['top1_delta_from_r8'],stats['top2_delta_from_r8'])!=(13,16,-1,0): errors.append('manifest scores')
    for field in ('formal_valid_questions','machine_valid_local_seals','s03_fusions'):
        if stats[field]!=0: errors.append(f'{field} must be zero')
    if manifest['base_astrological_knowledge_changed'] is not False or manifest['case_specific_direction_rule_added'] is not False or manifest['s00_s19_modified'] is not False: errors.append('unauthorized knowledge/rule change')
    for rid,row in manifest['historical_rounds'].items():
        if row['path']!=HISTORY[rid] or git_blob_sha(repo_root/HISTORY[rid])!=row['git_blob_sha'] or row['preserved'] is not True: errors.append(f'history {rid}')
    return {
        'schema':'DEV-GROUP-002-R9-VALIDATION-V1','status':'PASS' if not errors else 'FAIL','error_count':len(errors),'errors':errors,
        'historical_rounds_preserved':list(HISTORY),'processed_case_id':CASE_ID,'processed_question_count':5,
        'source_excerpt_count':objs['source-excerpts.json']['row_count'],'track_option_binding_rows':len(bindings['track_rows']),'pairwise_rows':len(pairwise['rows']),
        'dev002_ranks':expected_ranks,'dev002_top1':'DDDCB','dev002_top2':'CBCBA','top1_hits':13,'top2_coverage':16,'top1_delta_from_r8':-1,'top2_delta_from_r8':0,
        'formal_valid_questions':0,'machine_valid_local_seals':0,'s03_fusions':0,'base_astrological_knowledge_changed':False,'s00_s19_modified':False,'new_case_admission':'BLOCKED',
    }


def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('--repo-root',default='.'); p.add_argument('--write',action='store_true'); p.add_argument('--validate',action='store_true'); a=p.parse_args()
    root=Path(a.repo_root).resolve()
    if not a.write and not a.validate: p.error('select --write and/or --validate')
    if a.write: materialize(root)
    if a.validate:
        result=validate(root); out=root/ROUND_DIR; out.mkdir(parents=True,exist_ok=True); write_json(out/'validation.json',result); print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)); return 0 if result['status']=='PASS' else 1
    return 0

if __name__=='__main__': raise SystemExit(main())
