from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORKBENCH = ROOT / "knowledge-workbench"
SOURCE_CASE_ROLE = "USAGE_DEMONSTRATION_ONLY_NOT_INDEPENDENT_VALIDATION"
UNVALIDATED = {
    "distinct_case_count": 0,
    "support_count": 0,
    "counterexample_count": 0,
    "case_ids": [],
    "validation_note": "来源梳理完成；未读取答案，尚无独立案例支持或反例。",
}


def anchor(source_id: str, start: int, end: int, role: str, hint: str) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "line_start": start,
        "line_end": end,
        "anchor_role": role,
        "anchor_text_hint": hint,
    }


def tags(
    source_routes: list[str],
    *,
    topics: list[str] | None = None,
    subjects: list[str] | None = None,
    times: list[str] | None = None,
    endpoints: list[str] | None = None,
    skills: list[str] | None = None,
) -> dict[str, list[str]]:
    return {
        "topic_tags": topics or [],
        "subject_tags": subjects or [],
        "time_scope_tags": times or [],
        "endpoint_tags": endpoints or [],
        "reasoning_skill_tags": skills or [],
        "source_routes": source_routes,
    }


def card(
    card_id: str,
    title: str,
    source_scope: list[str],
    method_family: str,
    school: str,
    text_layer: str,
    attribution_note: str,
    claim_scope: str,
    required_inputs: list[str],
    prerequisites: list[str],
    procedure: list[str],
    applicability: list[str],
    negation: list[str],
    conflicts: list[str],
    counterexamples: list[str],
    anchors: list[dict[str, Any]],
    dedup_key: str,
    highest: str,
    limitations: list[str],
    forbidden: list[str],
    question_tags: dict[str, list[str]],
) -> dict[str, Any]:
    return {
        "card_id": card_id,
        "title": title,
        "batch": "A-ZIWEI-STATIC-S04-S07",
        "source_scope": source_scope,
        "method_family": method_family,
        "school_attribution": {
            "school": school,
            "text_layer": text_layer,
            "attribution_note": attribution_note,
        },
        "claim_scope": claim_scope,
        "required_inputs": required_inputs,
        "prerequisites": prerequisites,
        "ordered_procedure": procedure,
        "applicability_conditions": applicability,
        "negation_conditions": negation,
        "variant_or_conflicts": conflicts,
        "counterexamples": counterexamples,
        "source_anchors": anchors,
        "source_case_role": SOURCE_CASE_ROLE,
        "dedup_key": dedup_key,
        "highest_provable_level": highest,
        "limitations": limitations,
        "forbidden_shortcuts": forbidden,
        "question_tags": question_tags,
        "status": "CURATED_UNVALIDATED",
        "validation": dict(UNVALIDATED),
    }


def build_batch_a_cards() -> list[dict[str, Any]]:
    common_static = ["NATAL_STRUCTURE", "EVIDENCE_WEIGHTING", "COUNTEREVIDENCE_REVERSAL"]
    all_topics = [
        "FAMILY_ORIGIN", "PARENTS", "SIBLINGS", "MARRIAGE_RELATIONSHIP",
        "CHILDREN_FERTILITY", "CAREER_EDUCATION", "WEALTH_FINANCE",
        "PROPERTY_HOUSING", "HEALTH", "PERSONALITY_APPEARANCE",
        "SOCIAL_FRIENDS", "BUSINESS_PARTNERSHIP", "MIGRATION_RELOCATION",
        "TRAVEL_ACCIDENT_SAFETY", "LEGAL_CONFLICT", "MAJOR_YEAR_EVENT",
    ]
    cards = [
        card(
            "A-S04-001", "十二宫主题轴与唯一主题宫", ["S04"], "PALACE_TOPIC_ROUTING",
            "派生综合（S04活动控制根）", "EDITORIAL_CONTROL", "宫位定义来自S04活动段，卡片只做执行化整理。",
            "把题目原子路由到唯一主题宫和评价轴；只能证明主题入口与观察范围。",
            ["冻结盘面十二宫", "题目主语、动作、对象与评价轴"],
            ["先完成题目原子化", "原始宫位坐标不得被人物或动态坐标覆盖"],
            ["识别主语类型", "拆出动作和对象", "确定评价轴", "选择唯一主题宫", "登记禁止越级点"],
            ["题目原子可以归入十二宫之一", "同一原子只有一个事件本体"],
            ["主题本体不明确", "复合事实尚未拆分", "仅凭显眼星曜反推主题宫"],
            ["命宫不能抢占事业、财富、婚姻或疾病终点", "辅助宫和动态宫不得覆盖主题宫"],
            ["命宫强但具体职业仍未知", "财帛宫活跃但个人期末资产仍可能不高"],
            [anchor("S04", 1723, 1750, "宫位职责、固定路由顺序与坐标隔离", "S04是十二宫基础定义与主题宫权威；固定顺序从主语到气数位。"), anchor("S04", 1750, 2031, "十二宫定义及逐宫禁止越级点", "六至十二节逐宫列出允许定位和禁止直接推出。")],
            "S04:PALACE_TOPIC_AXIS", "ROUTING_ONLY",
            ["宫位只定位领域，不证明动作或正式结果", "必须由后续来源承担星系语义与现实闭合"],
            ["单宫定终点", "用星名替代主题路由", "把多个宫位当多票"],
            tags(["S04"], topics=all_topics, skills=["TOPIC_PALACE_ROUTING"]),
        ),
        card(
            "A-S04-002", "人物入口与人物太极交接", ["S04"], "PERSON_ENTRY_ROUTING",
            "派生综合（S04人物角色表）", "EDITORIAL_CONTROL", "角色入口表为S04运行注册表，人物太极计算仍交S17。",
            "为自然人选择入口宫并判断是否必须转人物太极；最高只证明人物路线已建立。",
            ["明确自然人身份", "人物与命主关系", "目标事件主题"],
            ["人物必须是自然人", "机构、资产、关系和事件不得伪装成人物"],
            ["锁定人物身份", "查默认入口宫", "区分入口宫与人物太极起点", "重大人物事件转S17", "未完成则保留UNKNOWN"],
            ["题目明确父母、配偶、子女、兄弟或其他自然人", "人物事件需要其内部主题宫"],
            ["主体是机构或资产", "人物身份不唯一且没有消歧", "命主自身不需要另立人物太极"],
            ["父母宫只是父母入口，不自动等于父亲或母亲个人盘", "平级、下属、门生分别路由"],
            ["父母宫受冲但无法区分父母主体", "交友宫风险不能直接证明某员工犯罪"],
            [anchor("S04", 2035, 2072, "人物角色、入口宫与硬边界", "S04-PR-01至S04-PR-22及主语硬边界。"), anchor("S04", 2175, 2194, "人物入口向人物太极的交接条件", "人物重大事件必须转人物太极；未完成保持UNKNOWN。")],
            "S04:PERSON_ENTRY_HANDOFF", "ROUTING_ONLY",
            ["不建立人物太极内部结论", "入口宫变化只能形成场景候选"],
            ["父母宫直接断父亡或母亡", "用命主疾厄宫替代他人健康路线", "给机构建立人物太极"],
            tags(["S04"], subjects=["FATHER", "MOTHER", "PARENTS", "SPOUSE_PARTNER", "CHILDREN", "SIBLINGS", "FRIEND_BUSINESS_PARTNER", "EXTERNAL_ACTOR"], skills=["SUBJECT_ENTITY_ROUTING"]),
        ),
        card(
            "A-S04-003", "资金、房产与所有权主语分离", ["S04"], "ENTITY_OWNERSHIP_ROUTING",
            "派生综合（S04实体拓扑）", "EDITORIAL_CONTROL", "将传统宫位场景拆为个人、家庭、公司和受托对象。",
            "区分掌管、使用、居住、家庭共有、公司名下与个人所有；最高证明正确的实体轴。",
            ["资金或房产对象", "法律或现实所有人", "使用人、管理人和参考期"],
            ["先区分自然人、家庭单位与组织", "题目中的所有权词不能由宫位自行补全"],
            ["建立资金或物业实体", "分别登记拥有、使用、管理和负债边", "选择财帛或田宅主题宫", "把缺失所有权标为终点缺口"],
            ["财富、负债、房产、祖业或公司场所题", "选项区分个人与组织资产"],
            ["对象不存在或主体不明", "只有宫位场景没有财产边", "题目只问一般居住环境"],
            ["公司营业额与个人收入冲突", "家庭房产与个人名下资产冲突", "居住与产权冲突"],
            ["命主管理大量客户资金但个人净资产一般", "居住豪宅但没有产权"],
            [anchor("S04", 2074, 2100, "财务与物业主语门", "掌管资金不等于拥有资金；实际居住不等于产权。")],
            "S04:ENTITY_OWNERSHIP_AXIS", "ROUTING_ONLY",
            ["不证明财富等级或产权已正式成立", "需S17动作与法律终点闭合"],
            ["公司收入算个人财富", "居住等于持有", "祖业候选等于继承完成"],
            tags(["S04"], topics=["WEALTH_FINANCE", "PROPERTY_HOUSING", "FAMILY_ORIGIN", "BUSINESS_PARTNERSHIP"], endpoints=["FINANCIAL_LEVEL", "PROPERTY_HOLDING", "BUSINESS_OUTCOME"], skills=["SUBJECT_ENTITY_ROUTING", "REALITY_SCALE_MAPPING"]),
        ),
        card(
            "A-S04-004", "复合事实原子化后重新定宫", ["S04"], "PALACE_ATOMIZATION",
            "派生综合（S04两次调用协议）", "EDITORIAL_CONTROL", "ROUTE_PASS与ATOM_PASS是S04派生执行协议。",
            "复合选项先拆原子，再为每个原子独立确定主题宫、主语和评价轴。",
            ["完整题干和全部选项", "复合原子清单"],
            ["ROUTE_PASS只建立初始实体", "ATOM_PASS前不得合并不同终点"],
            ["初步识别复合事实", "拆分关系、动作与终点", "逐原子重新定宫", "记录共同原子和最弱原子", "交下游闭合"],
            ["一个选项同时包含两种以上动作或终点", "题目存在因果链或先后阶段"],
            ["每个选项只有单一同质原子", "拆分后原子仍无法确定主体"],
            ["关系成立与离婚不能共用单一宫位证据", "收入增长与资产增加是不同原子"],
            ["创业能力成立但公司未注册", "有症状但未确诊或手术"],
            [anchor("S04", 2104, 2148, "ROUTE_PASS、ATOM_PASS与复合事实清单", "ROUTE_PASS不生成结果；ATOM_PASS要求每个原子唯一主题宫。")],
            "S04:ATOMIZED_THEME_ROUTE", "ROUTING_ONLY",
            ["原子化不等于原子已发生", "共同背景不得重复贡献"],
            ["一宫包办复合故事", "用最显眼原子替代最弱原子", "把拆分数量当证据数量"],
            tags(["S04"], topics=all_topics, skills=["COMPOSITE_OPTION_ATOMIZATION", "TOPIC_PALACE_ROUTING"]),
        ),
        card(
            "A-S04-005", "对宫三方、辅助宫与主题太极限权", ["S04"], "PALACE_RELATIONAL_CONTEXT",
            "传统宫位关系的派生控制", "DERIVED_SYNTHESIS", "保留传统对宫三方关系，但依S04限制其贡献层级。",
            "对宫、三方、夹宫和辅助宫只补结构语境；主题太极只改变观察参照，不复制证据。",
            ["本宫", "对宫与三方", "主题原子", "必要主题太极点"],
            ["先确定唯一主题宫", "区分本宫坐守与借照"],
            ["标记本宫证据", "分别标记对宫、三方和辅助宫", "建立主题太极", "同源结构归并一次", "交星系与终点模块"],
            ["主题宫已确定且关系宫位确有结构作用", "需要换参照解释同一主题"],
            ["用辅助宫另立主题", "无限递归立太极", "关系宫缺物理结构"],
            ["本宫坐守、对宫、三方、夹宫和借照不能混称", "主题太极不能替代人物太极或一四四体用"],
            ["对宫吉不代表本宫正式结果完成", "三方多吉仍可能缺动作与终点"],
            [anchor("S04", 2219, 2270, "辅助宫、对宫三方与主题太极边界", "对宫三方只补结构；主题太极不得无限递归或替代人物太极。")],
            "S04:RELATIONAL_PALACE_CONTEXT", "ROUTING_ONLY",
            ["只提供关系语境", "不得以关系宫数量累加独立票"],
            ["三方四正当三份证据", "借星当本宫坐守", "主题太极直接定吉凶"],
            tags(["S04"], topics=all_topics, skills=["TOPIC_PALACE_ROUTING", "EVIDENCE_WEIGHTING"]),
        ),
        card(
            "A-S05-001", "十四主星稳定本性按轴投影", ["S05"], "STAR_STABLE_NATURE",
            "全书系与中州整理的来源综合", "DERIVED_SYNTHESIS", "S05保留多来源星性；卡片不把不同来源数当投票。",
            "读取实际星曜的稳定倾向和条件，只投影到当前题轴；最高为静态倾向。",
            ["实际坐守或合法借照的星曜", "性别、日夜、庙旺输入", "题目现实轴"],
            ["先由盘面确认星曜实存", "角色标签不得冒充实际坐守"],
            ["建立案例级星性对象", "读取同轴父句段", "应用性别日夜庙旺修饰", "记录冲突和未知", "输出静态倾向"],
            ["题目轴与来源直接承担轴一致", "星曜在案例物理结构中真实存在"],
            ["仅星名词面重合", "来源未承担目标题轴", "组合条件未满足"],
            ["古典星性与现代终点之间需语义桥接", "不同来源可能对庙旺、性别或组合有异文"],
            ["有领导倾向但未任管理职位", "有财星倾向但没有个人净资产证据"],
            [anchor("S05", 20, 59, "案例静态星性、题级投影与S05/S06/S07边界", "不得因一个星名展开全部人生主题；通用星性只到同轴倾向。")],
            "S05:STAR_STABLE_NATURE", "STATIC_TENDENCY",
            ["不证明物理星系或入宫原子", "不证明具体行为、职业、疾病或正式终点"],
            ["单星定职业", "单星确诊", "星性广播全部宫位", "按来源数量投票"],
            tags(["S05"], topics=all_topics, skills=common_static),
        ),
        card(
            "A-S05-002", "性别日夜庙旺与辅煞条件修饰", ["S05"], "STAR_CONDITION_MODIFIERS",
            "全书系与中州条件分支综合", "DERIVED_SYNTHESIS", "条件、否定、例外和异文必须随父句段保存。",
            "修饰既有星性或组合强弱，不得独立产生相反方向或正式事件。",
            ["性别", "昼夜", "庙旺落陷", "实际辅煞会照", "目标星曜对象"],
            ["基础星性对象已建立", "条件字段来自冻结盘面而非猜测"],
            ["读取父句段全部条件", "分别标记增强、削弱、限制或未知", "检查相反分支", "修正静态倾向", "保留能力上限"],
            ["来源明确声明条件分支", "当前盘面具备对应输入"],
            ["条件未知", "辅煞并未真实同度或会照", "条件来自另一星系"],
            ["庙旺、性别和日夜表可能存在来源异文", "辅曜在不同主星组合中的作用不可广播"],
            ["煞曜出现但原局有制化或条件不全", "吉曜出现但结构选择器错配"],
            [anchor("S05", 20, 45, "静态对象字段和题级投影触发", "静态对象保存条件、性别日夜、庙旺、组合和冲突。"), anchor("S05", 57, 59, "多轴知识按来源实际承担轴投影", "未承担的轴不得补写。")],
            "S05:CONDITION_MODIFIER", "STATIC_TENDENCY",
            ["修饰不等于独立证据家族", "条件不足必须降为UNKNOWN或不适用"],
            ["吉曜等于成功", "煞曜等于灾祸", "庙旺直接翻转所有负面", "落陷直接判失败"],
            tags(["S05"], topics=all_topics, skills=common_static),
        ),
        card(
            "A-S05-003", "格局成立门：结构、辅佐与条件齐备", ["S05", "S06"], "PATTERN_FORMATION_GATE",
            "全书格局与中州条件校核", "DERIVED_SYNTHESIS", "格局名保留来源归属；物理结构必须由S06另行确认。",
            "格局只有在正曜结构、辅佐会合、位置和必要条件齐备时成立为条件化结构倾向。",
            ["候选格局名", "实际星系", "三方四正与夹宫", "辅佐煞曜和四化条件"],
            ["S06物理选择器匹配", "读取格局定义的全部必要条件"],
            ["提取必要条件", "逐项验证物理结构", "检查辅佐与缺失", "检查破格条件", "只输出成立范围内倾向"],
            ["来源定义和盘面结构一一匹配", "必要正曜与辅佐条件齐备"],
            ["缺任一必要条件", "只有格局名称相似", "来源属于不同地支或不同星系"],
            ["同名格局在不同来源可有宽严差异", "正曜、辅曜和杂曜的成立权重不可混为一谈"],
            ["只见紫微和一颗吉曜不足称百官朝拱", "格局成立但现实职位或财富未必完成"],
            [anchor("S05", 227, 245, "百官朝拱的正曜、辅曜、佐曜与条件示例", "定义要求府相、辅弼、魁钺、昌曲等分层条件。"), anchor("S06", 34, 46, "物理结构选择器与错配归零", "双星、地支、对拱、借照条件必须逐项匹配。")],
            "S05_S06:PATTERN_FORMATION", "CONDITIONED_STRUCTURE_TENDENCY",
            ["格局成立不是现代身份、金额或事件终点", "动态应期仍需S08/S10"],
            ["见格局名即成格", "辅曜数量投票", "格局成立直接定富贵", "忽略破格条件"],
            tags(["S05", "S06"], topics=all_topics, skills=["NATAL_STRUCTURE", "EVIDENCE_WEIGHTING"]),
        ),
        card(
            "A-S05-004", "破格与制化：限制原倾向而非自动反转", ["S05"], "PATTERN_BREAK_AND_MITIGATION",
            "全书格局与中州条件校核", "DERIVED_SYNTHESIS", "破格、制化、吉化与异文作为同一父条件树处理。",
            "识别空劫、煞忌、刑夹、条件缺失及制化；最高只能修正格局或星性倾向。",
            ["已通过成立门的格局候选", "煞忌空劫和夹宫", "制化与保护条件"],
            ["先证明原格局成立", "限制和保护必须来自同一结构语境"],
            ["列出破格分支", "列出制化分支", "区分削弱、失效和条件转化", "搜索直接反证", "输出修正后上限"],
            ["来源明确给出破格或制化条件", "相关星曜关系真实存在"],
            ["原格局本就未成立", "煞曜来自无关宫位或不同父链", "保护条件只是一般吉象"],
            ["有的来源将条件视为破格，有的只视为减等", "制化不能删除仍存在的负面条件"],
            ["天府见空形成空库限制，但不自动证明破产", "刑忌夹印修正天相但不直接证明法律灾祸"],
            [anchor("S05", 227, 245, "格局条件及空曜、夹印等限制示例", "天府空库、天相刑忌夹印等条件只修正结构。"), anchor("S05", 247, 263, "特殊星曜关系、吉凶与制化分支", "喜忌总诀含例外和制化，不能只取凶词。")],
            "S05:PATTERN_BREAK_MITIGATION", "CONDITIONED_STRUCTURE_TENDENCY",
            ["破格不等于相反事件必然发生", "制化不等于风险归零"],
            ["见煞即破格", "有吉即完全解厄", "破格直接等于失败或死亡", "只检索支持不检索制化"],
            tags(["S05"], topics=all_topics, skills=["NATAL_STRUCTURE", "COUNTEREVIDENCE_REVERSAL", "EVIDENCE_WEIGHTING"]),
        ),
        card(
            "A-S06-001", "十二基础盘一次识别与案例级静态结构", ["S06"], "TWELVE_BASE_CHART",
            "中州六十星系结构", "SOURCE_TEXT", "十二基础盘和六十星系物理坐标由S06承担。",
            "每案只识别一次基础盘、十二宫主星结构、空宫借星、对宫和三方；最高证明结构存在。",
            ["紫微所在支", "十二宫主星坐守", "空宫和对宫关系", "冻结盘面哈希"],
            ["盘面校准完成", "同一案例使用同一活动来源版本"],
            ["确定BASE_CHART_ID", "生成十二宫结构行", "登记空宫借星和对宫三方", "生成结构键", "题级只引用结构对象"],
            ["任何需要主星组合或空宫借照的题目", "盘面十二宫可完整读取"],
            ["基础盘无法识别", "盘面星曜缺失或冲突", "题目只用单星一般本性且不需结构"],
            ["六组结构对不能替代十二基础盘方向", "同一组合在不同地支可有分支"],
            ["同为紫微独坐，子宫与午宫不能默认完全相同", "空宫不能当无星无信息"],
            [anchor("S06", 19, 32, "案例级静态结构字段与只建一次规则", "十二基础盘、六十星系和借星结构只证明物理结构。")],
            "S06:CASE_STATIC_STRUCTURE", "STRUCTURE_EXISTENCE",
            ["不解释现代事件", "不允许每题或每选项重建基础盘"],
            ["逐颗星重建星系", "每题重算十二基础盘", "把结构事实当终点"],
            tags(["S06"], topics=all_topics, skills=["NATAL_STRUCTURE"]),
        ),
        card(
            "A-S06-002", "六十星系优先于单星相加", ["S05", "S06"], "SIXTY_STAR_SYSTEM",
            "中州六十星系", "SOURCE_TEXT", "组合星系及地支分支来自六十星系来源，单星本性只作条件输入。",
            "当完整主星组合存在时，以星系和地支分支为物理单位，单星本性不能替代组合性质。",
            ["完整主星组合", "宫位地支", "对宫三方结构", "S05单星条件对象"],
            ["S06基础盘已锁定", "组合与来源系统章节完全匹配"],
            ["识别系统章节", "读取组合主轴", "读取地支分支", "把S05本性作为修饰", "保留冲突和状态转移"],
            ["双星同度、对拱或明确六十星系章节适用", "单星在特定系统内发生交涉"],
            ["只有单星一般本性", "系统章节或地支不匹配", "空宫借星尚未确认"],
            ["单星本性与星系整体可能方向不同", "同一星系在不同支位有变体"],
            ["紫微贪狼不能用紫微与贪狼两个一般性简单相加", "太阳太阴星系不能套给太阴独坐异构盘"],
            [anchor("S06", 19, 19, "六十星系物理结构职责", "S06只证明当前盘物理结构与来源选择器。"), anchor("S06", 17273, 17276, "单星本性不能替代六十星系及地支分支", "六十星系组合各具特性，且同一独坐在不同支略有不同。")],
            "S06:SIXTY_SYSTEM_PHYSICAL", "CONDITIONED_STRUCTURE_TENDENCY",
            ["星系倾向仍非现实终点", "不能跨系统借用语义"],
            ["逐星加减", "星名重合即调用", "忽略地支变体", "六十星系全库无差别展开"],
            tags(["S05", "S06"], topics=all_topics, skills=["NATAL_STRUCTURE", "EVIDENCE_WEIGHTING"]),
        ),
        card(
            "A-S06-003", "空宫借星、对宫与本宫坐守分离", ["S04", "S06"], "EMPTY_PALACE_BORROWING",
            "中州基础盘结构", "SOURCE_TEXT", "空宫借星为物理结构关系，不等于本宫直接坐守。",
            "登记空宫借自何宫、何星系及其对宫三方关系；最高证明合法借照结构。",
            ["空宫位置", "对宫星系", "基础盘ID", "借星状态"],
            ["确认本宫无主星", "S06表中存在对应借星关系"],
            ["标记EMPTY_MAIN_STAR", "查BORROWED_FROM_BRANCH", "绑定借入系统章节", "区分借照与坐守", "将结构交S07"],
            ["当前宫位为空宫且来源允许借照", "对宫结构完整"],
            ["本宫已有主星", "借入宫位或系统不匹配", "只凭三方见星而称借星"],
            ["借照、对宫、三方和夹宫是不同位置关系", "借星语义可能受本宫辅煞与主题限制"],
            ["借入星系有某倾向，但不能说该星实际坐守本宫", "空宫借照仍可能因选择器条件不足而UNKNOWN"],
            [anchor("S06", 21, 32, "案例结构中的空宫借星行", "静态结构对象分别保存EMPTY_PALACE_BORROW_ROWS。"), anchor("S06", 119, 125, "双星、对拱、借照选择器硬规则", "空宫借照或特定地支必须逐项满足。")],
            "S06:EMPTY_PALACE_BORROW", "STRUCTURE_EXISTENCE",
            ["借星不拥有本宫坐守身份", "仅证明结构关系，不证明事件"],
            ["空宫等于没有信息", "借照当坐守", "对宫星性全量复制", "三方星曜当借星"],
            tags(["S04", "S06"], topics=all_topics, skills=["NATAL_STRUCTURE", "TOPIC_PALACE_ROUTING"]),
        ),
        card(
            "A-S06-004", "来源物理选择器错配归零", ["S06"], "STRUCTURE_SELECTOR_GATE",
            "中州结构选择器的派生控制", "EDITORIAL_CONTROL", "S06活动控制根把结构匹配设为所有下游语义前置门。",
            "逐项核对宫位、地支、主星组合、对宫、借照和四化要求；错配贡献固定为零。",
            ["当前盘结构对象", "来源要求的物理选择器", "目标原子"],
            ["来源锚点可解析出明确物理要求", "案例结构哈希有效"],
            ["比较宫位", "比较地支", "比较主星组合", "比较对宫与借照", "输出FULL_MATCH、PARTIAL或MISMATCH"],
            ["S07或其他语义来源要求具体结构", "组合证据将进入排序"],
            ["来源只陈述单星一般本性", "选择器字段未知且无法补建", "来源与当前结构完全不同"],
            ["PARTIAL_GENERIC_ONLY只能保留一般本性", "MISMATCH即使词面命中也不得恢复"],
            ["职业词直接重合但结构不符仍为零", "只出现双星中的一颗不构成组合匹配"],
            [anchor("S06", 34, 62, "题级选择器字段、精准调用与上下游边界", "STRUCTURE_SELECTOR_MISMATCH固定归零。"), anchor("S06", 83, 125, "选择器状态与硬规则", "无回执的组合证据不得进入排序。")],
            "S06:STRUCTURE_SELECTOR", "STRUCTURE_EXISTENCE",
            ["匹配只授权下游读取，不代表语义蕴含", "未知结构必须失败关闭"],
            ["词面重合恢复错配证据", "部分结构当完整匹配", "跳过选择器直接读入宫断语"],
            tags(["S06"], topics=all_topics, skills=["NATAL_STRUCTURE", "EVIDENCE_WEIGHTING", "COUNTEREVIDENCE_REVERSAL"]),
        ),
        card(
            "A-S07-001", "入宫父句段逐原子蕴含回执", ["S05", "S06", "S07"], "PALACE_ATOM_ENTAILMENT",
            "全星曜与星系入十二宫来源综合", "DERIVED_SYNTHESIS", "S07保存父句段，S05/S06只提供本性与物理前置。",
            "对每个选项原子绑定真实父句段、条件、主体、动作、对象和时间范围；最高为入宫轴蕴含。",
            ["S06选择器回执", "S05本性对象", "目标现实轴", "来源父句段"],
            ["S00已路由来源", "S06选择器适用", "目标原子明确"],
            ["建立内容寻址摘录", "读取全部条件与限制", "逐项核对主体动作对象时间", "登记直接反证", "机械派生能力上限"],
            ["父句段直接承担目标题轴", "条件和选择器闭合"],
            ["字面重合但跨轴", "父句段缺失或仅有ID", "主体、动作或对象不匹配"],
            ["直接蕴含、部分前置、场景、限制和反证必须分开", "同一父句段的替代结果需完整召回"],
            ["来源提到行业族但不能证明精确职位", "来源提到健康风险但不能直接确诊"],
            [anchor("S07", 248, 275, "来源摘录和逐原子蕴含回执", "父句段保存条件、限制、替代结果；能力由回执机械派生。")],
            "S07:PARENT_ATOM_ENTAILMENT", "PALACE_AXIS_ENTAILMENT",
            ["不建立正式现实终点", "必须保留来源条件、否定和例外"],
            ["只凭短ID调用", "用章节名代替父句段", "先写强支持再找来源", "跨轴词面匹配"],
            tags(["S05", "S06", "S07"], topics=all_topics, skills=["NATAL_STRUCTURE", "EVIDENCE_WEIGHTING", "COMPOSITE_OPTION_ATOMIZATION"]),
        ),
        card(
            "A-S07-002", "星系入十二宫能力上限", ["S07"], "PALACE_CAPABILITY_CEILING",
            "入宫来源综合的派生控制", "EDITORIAL_CONTROL", "传统结果词保留，但现代终点资格由S07上限和S17闭合共同控制。",
            "入宫来源只承担其直接语义轴；具体行为、法律状态、金额、精确职业、手术、牢狱和死亡须外部闭合。",
            ["逐原子蕴含回执", "来源直接承担轴", "目标正式终点"],
            ["来源物理和语义均匹配", "直接结果词与现代概念已区分"],
            ["识别来源轴", "标记场景或前置", "列出未闭合人物动作对象时间", "设置能力上限", "交S17正式闭合"],
            ["任何入宫语义向现代选项转译", "选项包含具体行为或正式终点"],
            ["来源已直接包含全部现实动作且另有S17闭合", "目标仅问静态倾向"],
            ["传统结果词与现代法律、医学、财务概念不等价", "保护因素只能修饰原方向"],
            ["破耗不能独立证明负债或破产", "刑忌不能独立证明坐牢", "疾病词不能独立完成诊断"],
            [anchor("S07", 277, 300, "调用集合、能力上限与下游职责", "具体行为和正式终点必须交S17闭合。")],
            "S07:CAPABILITY_CEILING", "SCENE_OR_PRECONDITION_ONLY",
            ["传统断语不得未经校准直译为现代事实", "能力上限本身固定零贡献"],
            ["星系入宫直接定离婚", "风险词直接定死亡", "职业族直接定具体职业", "结果词当完成证明"],
            tags(["S07"], topics=all_topics, skills=["EVENT_ENDPOINT_CLOSURE", "OPTION_GRANULARITY", "EVIDENCE_WEIGHTING"]),
        ),
        card(
            "A-S07-003", "同父链支持、限制、替代与直接反证并读", ["S07"], "PALACE_PARENT_CHAIN_COUNTEREVIDENCE",
            "入宫来源综合的派生控制", "EDITORIAL_CONTROL", "同一父句段各分支必须成组召回，禁止只取支持赢家的片段。",
            "同一物理结构与父链内同时检索支持、限制、例外、替代和直接反证，并对互斥原子保持单向贡献。",
            ["来源父链", "目标原子与互斥原子", "当前条件分支"],
            ["父句段可完整复读", "赢家与最强挑战者采用同等检索深度"],
            ["召回支持分支", "召回限制和例外", "召回同级替代", "搜索直接反证", "记录最弱原子与剩余冲突"],
            ["选项互斥或共享场景", "来源包含转折、并列、替代或条件分支"],
            ["来源只有单一无条件陈述", "父句段未知", "反证来自不同物理结构"],
            ["同一解释不能同时支持富裕与贫穷等互斥方向", "共享场景不能完成复合选项"],
            ["来源同时支持能力又限制现实完成", "普通正状态可能是戏剧性负状态的强反证"],
            [anchor("S07", 24, 69, "互斥原子方向、支持限制反证分离", "同一父句段不得以同一解释支持互斥原子。"), anchor("S07", 248, 260, "父句段全部条件、限制和替代结果一次保存", "摘录对象必须保存完整父链且可复读。")],
            "S07:PARENT_CHAIN_POLARITY", "PALACE_AXIS_ENTAILMENT",
            ["反证必须与同一目标题轴相关", "无调用不等于反证"],
            ["只召回支持赢家", "限制当零证据后丢弃", "同源正反各算一票", "共享场景完成复合终点"],
            tags(["S07"], topics=all_topics, skills=["COUNTEREVIDENCE_REVERSAL", "EVIDENCE_WEIGHTING", "COMPOSITE_OPTION_ATOMIZATION"]),
        ),
    ]
    return cards


def migrate_foundation_cards(payload: dict[str, Any]) -> dict[str, Any]:
    school_map = {
        "CLASSICAL_QUANSHU_STATIC": "全书系静态体系",
        "ZHONGZHOU_STAR_SYSTEM": "中州派",
        "FLYING_STAR_LIANG": "梁派飞星",
        "HELUO_FANGWAI": "河洛方外",
        "ONE_HUNDRED_FORTY_FOUR": "一四四诀",
        "BAZI_ZIPING": "子平法",
        "DUAL_TRACK_FUSION": "派生双轨融合",
    }
    highest_map = {
        "CLASSICAL_QUANSHU_STATIC": "CONDITIONED_STRUCTURE_TENDENCY",
        "ZHONGZHOU_STAR_SYSTEM": "CONDITIONED_STRUCTURE_TENDENCY",
        "FLYING_STAR_LIANG": "SCENE_OR_PRECONDITION_ONLY",
        "HELUO_FANGWAI": "ROUTING_ONLY",
        "ONE_HUNDRED_FORTY_FOUR": "SCENE_OR_PRECONDITION_ONLY",
        "BAZI_ZIPING": "CONDITIONED_STRUCTURE_TENDENCY",
        "DUAL_TRACK_FUSION": "FORMAL_ENDPOINT_WITH_EXTERNAL_CLOSURE_ONLY",
    }
    migrated = []
    for old in payload["cards"]:
        source_scope = sorted({item["source_id"] for item in old["source_anchors"]})
        validation = dict(old["validation"])
        validation["validation_note"] = "总纲卡仅完成来源梳理；未读取答案，尚无独立案例验证。"
        migrated.append({
            "card_id": old["card_id"],
            "title": old["title"],
            "batch": "FOUNDATION-METHOD-OVERVIEW",
            "source_scope": source_scope,
            "method_family": old["method_family"],
            "school_attribution": {
                "school": school_map[old["method_family"]],
                "text_layer": "DERIVED_SYNTHESIS",
                "attribution_note": "总纲卡跨来源整理；具体判断必须回到所列精确锚点。",
            },
            "claim_scope": old["claim_scope"],
            "required_inputs": old["required_inputs"],
            "prerequisites": ["冻结输入有效", "来源锚点可复读", "题目轴已明确"],
            "ordered_procedure": old["ordered_procedure"],
            "applicability_conditions": ["方法前置输入齐全", "目标题轴落在卡片声明范围内"],
            "negation_conditions": ["关键输入缺失", "来源条件或物理选择器不匹配", "目标超出能力上限"],
            "variant_or_conflicts": old["limitations"],
            "counterexamples": [f"反例候选：{item}" for item in old["limitations"]],
            "source_anchors": [
                {**item, "anchor_text_hint": item["anchor_role"]}
                for item in old["source_anchors"]
            ],
            "source_case_role": SOURCE_CASE_ROLE,
            "dedup_key": f"FOUNDATION:{old['card_id'].replace('-', '_')}",
            "highest_provable_level": highest_map[old["method_family"]],
            "limitations": old["limitations"],
            "forbidden_shortcuts": old["forbidden_shortcuts"],
            "question_tags": tags(source_scope, topics=["OTHER"], subjects=["SELF"], times=["NATAL"], endpoints=["OTHER"], skills=["EVIDENCE_WEIGHTING"]),
            "status": old["status"],
            "validation": validation,
        })
    return {
        "schema": "FORTUNE-SCHOOL-METHOD-CARDS-V2",
        "authority": payload["authority"],
        "cards": migrated,
    }


def build_conflict_matrix() -> dict[str, Any]:
    rows = [
        ("A-CONFLICT-001", "人物入口宫与人物太极不可互换", ["A-S04-002"], "保留两套坐标；具体人物重大事件必须转人物太极。"),
        ("A-CONFLICT-002", "机构、资产、资金、关系不得建立人物太极", ["A-S04-002", "A-S04-003"], "改走非人物实体与所有权路线。"),
        ("A-CONFLICT-003", "本宫坐守、借照、对宫、三方和辅助宫不得合并计票", ["A-S04-005", "A-S06-003"], "分别登记位置关系，同一物理结构基础贡献一次。"),
        ("A-CONFLICT-004", "单星一般本性不能替代完整六十星系", ["A-S05-001", "A-S06-002"], "优先S06组合系统；S05只作条件修饰。"),
        ("A-CONFLICT-005", "格局名称与格局成立不是同一事实", ["A-S05-003"], "逐项核对正曜、辅佐、位置和必要条件。"),
        ("A-CONFLICT-006", "破格、制化和保护因素不得自动反转方向", ["A-S05-004"], "分别记录削弱、失效、缓解和仍存风险。"),
        ("A-CONFLICT-007", "结构选择器错配时词面命中固定归零", ["A-S06-004"], "不得用职业词、疾病词或选项词恢复贡献。"),
        ("A-CONFLICT-008", "入宫场景或传统结果词不等于现代正式终点", ["A-S07-002"], "保持能力上限并转S17补齐人物、动作、对象、时间和终点。"),
        ("A-CONFLICT-009", "同一父句段不得同时支持互斥原子", ["A-S07-003"], "显式标注方向，支持、限制、替代和反证分离。"),
        ("A-CONFLICT-010", "来源命例不构成独立验证", [card["card_id"] for card in build_batch_a_cards()], "命例只登记作者用法；验证计数保持零，等待独立案例。"),
    ]
    return {
        "schema": "FORTUNE-BATCH-A-CONFLICT-MATRIX-V1",
        "authority": "DERIVED_NO_INDEPENDENT_ASTROLOGICAL_AUTHORITY",
        "source_scope": ["S04", "S05", "S06", "S07"],
        "rows": [
            {
                "conflict_id": row_id,
                "conflict": conflict,
                "card_ids": card_ids,
                "resolution": resolution,
                "validation_status": "CURATED_UNVALIDATED",
            }
            for row_id, conflict, card_ids, resolution in rows
        ],
    }


def iter_question_profiles() -> list[dict[str, Any]]:
    manifest = json.loads((ROOT / "case-bank/manifest.json").read_text(encoding="utf-8"))
    partitions = {
        case_id: split
        for split, case_ids in manifest["partitions"].items()
        for case_id in case_ids
    }
    rows = []
    for path in sorted((ROOT / "case-bank/cases").glob("CASE-*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        for question in case["questions"]["parsed"]:
            rows.append({
                "case_id": case["case_id"],
                "question_id": question["question_id"],
                "partition": partitions[case["case_id"]],
                "profile": question["preblind_profile"],
            })
    return rows


def profile_matches(card_payload: dict[str, Any], profile: dict[str, Any]) -> bool:
    wanted = card_payload["question_tags"]
    if not set(wanted["source_routes"]).issubset(profile["source_routes"]):
        return False
    dimensions = ("topic_tags", "subject_tags", "time_scope_tags", "endpoint_tags", "reasoning_skill_tags")
    return all(not wanted[key] or set(wanted[key]).intersection(profile[key]) for key in dimensions)


def build_coverage(cards: list[dict[str, Any]]) -> dict[str, Any]:
    questions = iter_question_profiles()
    mappings = []
    for card_payload in cards:
        matches = [row for row in questions if profile_matches(card_payload, row["profile"])]
        case_ids = sorted({row["case_id"] for row in matches})
        counts = Counter(row["partition"] for row in matches)
        mappings.append({
            "card_id": card_payload["card_id"],
            "selection_rule": "all listed source_routes and at least one listed tag in each non-empty tag dimension",
            "eligible_case_count": len(case_ids),
            "eligible_question_count": len(matches),
            "partition_question_counts": dict(sorted(counts.items())),
            "eligible_case_ids": case_ids,
            "eligible_question_refs": [f"{row['case_id']}/{row['question_id']}" for row in matches],
            "validation_status": "COVERAGE_ONLY_NOT_OUTCOME_VALIDATION",
        })
    return {
        "schema": "FORTUNE-BATCH-A-CASE-COVERAGE-V1",
        "authority": "PREBLIND_TAG_COVERAGE_ONLY",
        "answer_data_used": False,
        "source_scope": ["S04", "S05", "S06", "S07"],
        "mappings": mappings,
    }


def render(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def write_or_check(path: Path, value: Any, check: bool) -> None:
    expected = render(value)
    if check:
        if not path.is_file() or path.read_text(encoding="utf-8") != expected:
            raise SystemExit(f"stale generated knowledge artifact: {path.relative_to(ROOT)}")
        return
    path.write_text(expected, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    foundation_path = WORKBENCH / "school-method-cards.json"
    foundation = migrate_foundation_cards(json.loads(foundation_path.read_text(encoding="utf-8"))) if not foundation_path.read_text(encoding="utf-8").lstrip().startswith('{\n  "schema": "FORTUNE-SCHOOL-METHOD-CARDS-V2"') else json.loads(foundation_path.read_text(encoding="utf-8"))
    cards = build_batch_a_cards()
    batch_payload = {
        "schema": "FORTUNE-KNOWLEDGE-CARD-COLLECTION-V2",
        "authority": "DERIVED_CURATED_SUMMARY_NO_INDEPENDENT_ASTROLOGICAL_AUTHORITY",
        "batch": "A-ZIWEI-STATIC-S04-S07",
        "cards": cards,
    }
    write_or_check(foundation_path, foundation, args.check)
    write_or_check(WORKBENCH / "batch-a-static-cards.json", batch_payload, args.check)
    write_or_check(WORKBENCH / "batch-a-conflict-matrix.json", build_conflict_matrix(), args.check)
    write_or_check(WORKBENCH / "batch-a-case-coverage.json", build_coverage(cards), args.check)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
