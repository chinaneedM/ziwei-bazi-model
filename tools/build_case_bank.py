#!/usr/bin/env python3
"""Build the answer-free, question-level case bank from user-supplied examples.

This is an intake tool, not a prediction tool. It normalizes source formatting,
binds every artifact by hash, derives only deterministic chart metadata, and
creates topic/skill routing labels without consulting any answer material.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageEnhance, ImageOps


CASE_SCHEMA = "FORTUNE-CASE-BANK-CASE-V1"
MANIFEST_SCHEMA = "FORTUNE-CASE-BANK-MANIFEST-V1"
REVEALED_HISTORY_CASE_IDS = {"CASE-001"}
QUESTION_HEADING = re.compile(
    r"(?m)^\s*(?:问题|题目|題目)\s*(?::\s*)?"
    r"([0-9一二三四五六七八九十]+)?\s*[:：]?\s*"
)
OPTION_LABEL = re.compile(
    r"(?m)(?:^[ \t]*([A-Ea-eΑ])\s*[.、:：)]?\s*(?=\S)"
    r"|(?<=[ \t])([A-Ea-eΑ])\s*[.、:：)]?\s*(?=[\u3400-\u9fff\d$]))"
)
ANSWER_MARKER = re.compile(
    r"正确答案|参考答案|答案\s*[:：]|评分|得分|揭盲|复盘|"
    r"top[ _-]?1|prediction|answer[_ -]?key|correct[_ -]?answer|secret|密钥",
    re.IGNORECASE,
)
YEAR = re.compile(r"(?<!\d)((?:18|19|20)\d{2})(?!\d)")

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
GANZHI = [STEMS[index % 10] + BRANCHES[index % 12] for index in range(60)]
HIDDEN_STEMS = {
    "子": "癸",
    "丑": "己癸辛",
    "寅": "甲丙戊",
    "卯": "乙",
    "辰": "戊乙癸",
    "巳": "丙戊庚",
    "午": "丁己",
    "未": "己丁乙",
    "申": "庚壬戊",
    "酉": "辛",
    "戌": "戊辛丁",
    "亥": "壬甲",
}
ELEMENT = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
}
GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

TOPIC_KEYWORDS = {
    "FAMILY_ORIGIN": ("出身", "家境", "原生家庭", "家庭背景", "富裕家庭", "贫穷家庭"),
    "PARENTS": ("父亲", "母亲", "父母", "双亲", "父母亲", "父死", "母死"),
    "SIBLINGS": ("兄弟", "姐妹", "哥哥", "弟弟", "姐姐", "妹妹", "手足", "一兄", "一姐"),
    "MARRIAGE_RELATIONSHIP": ("婚姻", "结婚", "离婚", "夫妻", "丈夫", "妻子", "配偶", "姻缘", "感情", "男友", "女友", "初恋", "外遇", "第三者"),
    "CHILDREN_FERTILITY": ("子女", "生子", "生女", "儿子", "女儿", "小孩", "孩子", "怀孕", "流产", "孙儿"),
    "CAREER_EDUCATION": ("工作", "职业", "事业", "学历", "学业", "读书", "上学", "大学", "中学", "小学", "科系", "老师", "公司", "创业", "生意", "老板", "职位", "升职", "退休"),
    "WEALTH_FINANCE": ("财富", "财运", "收入", "存款", "年薪", "工资", "金钱", "欠债", "破产", "富裕", "贫穷", "横财", "彩票", "六合彩", "注资"),
    "PROPERTY_HOUSING": ("买房", "购屋", "房产", "物业", "地产", "田宅", "住房", "自购屋"),
    "HEALTH": ("健康", "身体", "病", "癌", "手术", "医院", "失明", "残缺", "肥胖", "肝", "肠胃", "暗疾"),
    "PERSONALITY_APPEARANCE": ("性格", "样貌", "外貌", "相貌", "身材", "眼睛", "眼晴", "耳朵", "特质", "外界评价"),
    "SOCIAL_FRIENDS": ("朋友", "交友", "人缘", "社交", "拍挡", "伙伴", "客户", "贵人"),
    "BUSINESS_PARTNERSHIP": ("合作", "拍挡", "伙伴", "合伙", "注资", "公司合作"),
    "MIGRATION_RELOCATION": ("搬迁", "移民", "迁移", "外出工作", "北上", "去厦门", "离乡"),
    "TRAVEL_ACCIDENT_SAFETY": ("车祸", "意外", "事故", "火灾", "被劫", "受伤", "断脚", "失明"),
    "LEGAL_CONFLICT": ("坐牢", "牢狱", "监狱", "官非", "诉讼", "拘捕", "违法", "刑事"),
    "SPIRITUAL_PARANORMAL": ("通灵", "神明", "灵异", "宗教", "茹素", "出家"),
    "GAMBLING_WINDFALL": ("横财", "彩票", "六合彩", "赌博", "博彩", "中奖"),
    "SEXUALITY_INTIMACY": ("性取向", "同性", "男性第三者", "情欲", "外遇"),
    "MAJOR_YEAR_EVENT": ("发生何事", "遭遇", "以下哪年", "哪一年", "何年", "哪段时间"),
}

SUBJECT_KEYWORDS = {
    "FATHER": ("父亲", "父死", "父亡"),
    "MOTHER": ("母亲", "母死", "母亡"),
    "PARENTS": ("父母", "双亲", "父母亲"),
    "SPOUSE_PARTNER": ("丈夫", "妻子", "老公", "老婆", "配偶", "男友", "女友", "夫妻", "初恋"),
    "CHILDREN": ("子女", "儿子", "女儿", "孩子", "小孩", "长子", "孙儿"),
    "SIBLINGS": ("兄弟", "姐妹", "哥哥", "弟弟", "姐姐", "妹妹", "大姐"),
    "FRIEND_BUSINESS_PARTNER": ("朋友", "交友", "拍挡", "伙伴", "合伙"),
    "EMPLOYER_ORGANIZATION": ("公司", "组织", "单位", "雇主", "企业", "学校", "政府"),
    "EXTERNAL_ACTOR": ("客户", "长官", "明星", "外界", "他人"),
}

ENDPOINT_KEYWORDS = {
    "BACKGROUND_LEVEL": ("出身", "家境", "家庭背景", "富裕家庭", "贫穷家庭"),
    "FAMILY_COMPOSITION": ("父母双全", "父死母在", "兄弟", "姐妹", "一儿一女", "子女"),
    "RELATIONSHIP_STATUS": ("婚姻状态", "未婚", "已婚", "离婚", "单身", "结婚"),
    "RELATIONSHIP_QUALITY": ("感情", "夫妻", "婚后", "争吵", "和谐", "第三者", "外遇"),
    "DIVORCE": ("离婚", "分手"),
    "DEATH": ("去世", "死亡", "病逝", "离世", "过身", "仙游", "父死", "母死", "寿终正寝"),
    "LIFE_SPAN": ("寿命", "寿终正寝", "不足50岁"),
    "CHILDBIRTH": ("生子", "生女", "怀孕", "流产"),
    "OCCUPATION": ("职业", "工作", "做什么", "职位", "老板", "创业", "公司"),
    "EDUCATION_LEVEL": ("学历", "大学", "中学", "小学", "博士", "科系", "学业"),
    "FINANCIAL_LEVEL": ("财富", "收入", "存款", "年薪", "工资", "富裕", "贫穷", "欠债"),
    "BUSINESS_OUTCOME": ("创业", "公司", "生意", "倒闭", "破产", "扩展", "注资", "合作"),
    "PROPERTY_HOLDING": ("买房", "购屋", "房产", "物业", "地产"),
    "WINDFALL": ("横财", "彩票", "六合彩", "中奖"),
    "HEALTH_CONDITION": ("健康", "身体", "病", "癌", "手术", "肥胖", "失眠"),
    "ACCIDENT_INJURY": ("车祸", "意外", "事故", "火灾", "被劫", "受伤", "失明", "残缺"),
    "LEGAL_OUTCOME": ("坐牢", "牢狱", "监狱", "官非", "诉讼"),
    "MIGRATION": ("搬迁", "移民", "迁移", "北上", "外出工作"),
    "PERSONALITY": ("性格", "特质", "外界评价"),
    "APPEARANCE": ("样貌", "外貌", "相貌", "身材", "眼睛", "眼晴", "耳朵"),
    "SEXUAL_ORIENTATION": ("性取向", "同性", "男性第三者"),
    "MAJOR_EVENT": ("发生何事", "遭遇", "以下哪年", "哪一年", "何年"),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def object_sha256(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").strip() + "\n"


def option_label(match: re.Match[str]) -> str:
    return (match.group(1) or match.group(2)).replace("Α", "A").upper()


def parse_questions(text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    text = text.replace("Α", "A")
    headings = list(QUESTION_HEADING.finditer(text))
    questions: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    source_numbers: list[str | None] = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        block = text[heading.end():end].strip()
        option_matches = list(OPTION_LABEL.finditer(block))
        labels = [option_label(match) for match in option_matches]
        stem = block[: option_matches[0].start()].strip() if option_matches else block
        options: list[dict[str, str]] = []
        for option_index, match in enumerate(option_matches):
            option_end = option_matches[option_index + 1].start() if option_index + 1 < len(option_matches) else len(block)
            options.append({
                "option_id": option_label(match),
                "text": re.sub(r"\s+", " ", block[match.end():option_end].strip()),
            })
        question_id = f"Q{index + 1}"
        source_number = heading.group(1)
        source_numbers.append(source_number)
        if labels not in (list("ABCD"), list("ABCDE")):
            issues.append({
                "code": "QUESTION_OPTION_SET_INVALID",
                "question_id": question_id,
                "observed_option_ids": labels,
                "severity": "BLOCKING",
            })
        if not stem:
            issues.append({"code": "QUESTION_STEM_EMPTY", "question_id": question_id, "severity": "BLOCKING"})
        questions.append({
            "question_id": question_id,
            "source_question_number": source_number,
            "stem": re.sub(r"\s+", " ", stem),
            "options": options,
        })
    expected = [str(index) for index in range(1, len(source_numbers) + 1)]
    if source_numbers != expected:
        issues.append({
            "code": "SOURCE_QUESTION_NUMBERING_NORMALIZED",
            "observed": source_numbers,
            "normalized": expected,
            "severity": "NON_BLOCKING",
        })
    if not questions:
        issues.append({"code": "NO_QUESTIONS_PARSED", "severity": "BLOCKING"})
    return questions, issues


def extract_basic_info(ziwei_text: str) -> dict[str, str]:
    labels = {
        "gender": "性别",
        "longitude": "地理经度",
        "clock_time": "钟表时间",
        "true_solar_time": "真太阳时",
        "lunar_time": "农历时间",
        "solar_term_pillars": "节气四柱",
        "non_solar_term_pillars": "非节气四柱",
        "five_element_bureau": "五行局数",
    }
    result: dict[str, str] = {}
    for key, label in labels.items():
        match = re.search(rf"{re.escape(label)}\s*:\s*([^\n]+)", ziwei_text)
        if match:
            result[key] = match.group(1).strip()
    final = re.search(r"身主:([^;\n]+);\s*命主:([^;\n]+);\s*子年斗君:([^;\n]+);\s*身宫:([^\n]+)", ziwei_text)
    if final:
        result.update({
            "body_lord": final.group(1).strip(),
            "life_lord": final.group(2).strip(),
            "year_doujun": final.group(3).strip(),
            "body_palace_branch": final.group(4).strip(),
        })
    return result


def ten_god(day_stem: str, other_stem: str) -> str:
    day_element = ELEMENT[day_stem]
    other_element = ELEMENT[other_stem]
    same_polarity = STEMS.index(day_stem) % 2 == STEMS.index(other_stem) % 2
    if day_element == other_element:
        return "比肩" if same_polarity else "劫财"
    if GENERATES[day_element] == other_element:
        return "食神" if same_polarity else "伤官"
    if CONTROLS[day_element] == other_element:
        return "偏财" if same_polarity else "正财"
    if CONTROLS[other_element] == day_element:
        return "七杀" if same_polarity else "正官"
    if GENERATES[other_element] == day_element:
        return "偏印" if same_polarity else "正印"
    raise ValueError(f"unsupported element relation: {day_stem}/{other_stem}")


def infer_luck_cycles(gender: str, pillars: list[str], first_year: int, birth_year: int) -> dict[str, Any]:
    year_stem = pillars[0][0]
    month_pillar = pillars[1]
    is_yang_year = STEMS.index(year_stem) % 2 == 0
    forward = (gender == "男" and is_yang_year) or (gender == "女" and not is_yang_year)
    month_index = GANZHI.index(month_pillar)
    direction = 1 if forward else -1
    cycles = []
    for offset in range(1, 10):
        cycle_pillar = GANZHI[(month_index + direction * offset) % 60]
        year = first_year + (offset - 1) * 10
        nominal_age = year - birth_year + 1
        cycles.append({"start_year": year, "nominal_age": nominal_age, "pillar": cycle_pillar})
    return {
        "direction": "FORWARD" if forward else "REVERSE",
        "first_major_luck_year": first_year,
        "first_major_luck_nominal_age": first_year - birth_year + 1,
        "cycles": cycles,
    }


def ocr_first_luck_year(image_path: Path, birth_year: int, tesseract: str) -> tuple[int | None, list[int]]:
    with Image.open(image_path) as image:
        crop = image.crop((int(image.width * 0.54), 0, image.width, int(image.height * 0.27)))
        crop = crop.resize((int(image.width * 0.92), int(image.height * 0.54)))
        crop = ImageEnhance.Contrast(ImageOps.grayscale(crop)).enhance(2)
        with tempfile.NamedTemporaryFile(suffix=".png") as temp:
            crop.save(temp.name)
            result = subprocess.run(
                [tesseract, temp.name, "stdout", "-l", "eng", "--psm", "6"],
                check=False,
                capture_output=True,
                text=True,
            )
    years: list[int] = []
    for value in YEAR.findall(result.stdout):
        year = int(value)
        if birth_year - 2 <= year <= birth_year + 110 and (not years or years[-1] != year):
            years.append(year)
    best: list[int] = []
    for start in range(len(years)):
        run = [years[start]]
        for candidate in years[start + 1:]:
            if candidate == run[-1] + 10:
                run.append(candidate)
            elif len(run) >= 2:
                break
        if len(run) > len(best):
            best = run
    if len(best) < 4:
        return None, years
    first = best[1] if best[0] == birth_year and len(best) > 1 else best[0]
    return first, years


def split_atoms(text: str) -> list[str]:
    chunks = re.split(r"[，；;]|而且|并且|以及|但(?:是)?|所以|后来|然后", text)
    atoms = [re.sub(r"\s+", " ", chunk).strip(" ,，。") for chunk in chunks]
    return [atom for atom in atoms if atom]


def has_any(text: str, words: Iterable[str]) -> bool:
    return any(word in text for word in words)


def classify_question(question: dict[str, Any]) -> dict[str, Any]:
    option_texts = [option["text"] for option in question["options"]]
    text = question["stem"] + " " + " ".join(option_texts)
    topics = [tag for tag, words in TOPIC_KEYWORDS.items() if has_any(text, words)]
    if re.search(r"(?:18|19|20)\d{2}", text) and "MAJOR_YEAR_EVENT" not in topics:
        topics.append("MAJOR_YEAR_EVENT")
    if not topics:
        topics = ["OTHER"]

    subjects = [tag for tag, words in SUBJECT_KEYWORDS.items() if has_any(text, words)]
    if not subjects:
        subjects = ["SELF"]

    time_tags: list[str] = []
    if re.search(r"(?:18|19|20)\d{2}", text):
        time_tags.append("SPECIFIC_YEAR")
    if re.search(r"\d{4}\s*年?\s*(?:至|到|[-—~～]+)\s*\d{4}", text) or has_any(text, ("大限", "十年", "哪段时间", "哪个运", "运中")):
        time_tags.append("MULTI_YEAR_PERIOD")
    if has_any(text, ("出生", "出身", "原生家庭", "先天")):
        time_tags.append("NATAL")
    if has_any(text, ("儿时", "童年", "小时", "岁前", "中学时期", "大学时期")):
        time_tags.append("CHILDHOOD")
    if has_any(text, ("截至", "截止", "目前", "现时", "现在")):
        time_tags.append("CURRENT_STATUS")
    if has_any(text, ("一生", "寿命", "终身", "整体")):
        time_tags.append("LIFETIME")
    if not time_tags:
        time_tags = ["OTHER"]

    endpoints = [tag for tag, words in ENDPOINT_KEYWORDS.items() if has_any(text, words)]
    if not endpoints:
        endpoints = ["OTHER"]

    option_atoms = {
        option["option_id"]: split_atoms(option["text"])
        for option in question["options"]
    }
    compound = any(len(atoms) > 1 for atoms in option_atoms.values())
    skills = [
        "TOPIC_PALACE_ROUTING",
        "NATAL_STRUCTURE",
        "EVIDENCE_WEIGHTING",
        "COUNTEREVIDENCE_REVERSAL",
        "ZIWEI_BAZI_ARBITRATION",
        "OPTION_GRANULARITY",
        "STATIC_DYNAMIC_LAYERING",
        "PALACE_TRANSFORMATION_CHAIN",
        "BAZI_STRUCTURE_THEN_TRIGGER",
        "UNCERTAINTY_CALIBRATION",
    ]
    if subjects != ["SELF"]:
        skills.extend(["SUBJECT_ENTITY_ROUTING", "CAUSAL_ACTOR_DIRECTION"])
    if "SPECIFIC_YEAR" in time_tags or "MULTI_YEAR_PERIOD" in time_tags:
        skills.extend(["TIME_LAYER_ACTIVATION", "EVENT_ENDPOINT_CLOSURE"])
    if compound:
        skills.append("COMPOSITE_OPTION_ATOMIZATION")
    if any(tag in topics for tag in ("WEALTH_FINANCE", "PROPERTY_HOUSING", "CAREER_EDUCATION")):
        skills.extend(["REALITY_SCALE_MAPPING", "REGION_ERA_NORMALIZATION"])
    if "DEATH" in endpoints or "LIFE_SPAN" in endpoints:
        skills.append("DEATH_ENTITY_TIME_CLOSURE")
    if any(tag in topics for tag in ("SEXUALITY_INTIMACY", "SPIRITUAL_PARANORMAL", "GAMBLING_WINDFALL")):
        skills.extend(["SENSITIVE_ATTRIBUTE_CAUTION", "RARE_TOPIC_SAMPLE_GUARD"])
    if "CAREER_EDUCATION" in topics:
        skills.append("CAREER_PROFILE_CLOSURE")
    if "MARRIAGE_RELATIONSHIP" in topics:
        skills.append("RELATIONSHIP_SEQUENCE")
    if "HEALTH" in topics:
        skills.append("HEALTH_SEVERITY_LOCALIZATION")

    routes = {"S00", "S01", "S03", "S04", "S08", "S09", "S11", "S16", "S17", "S18", "S19"}
    if "NATAL" in time_tags or any(tag in topics for tag in ("PERSONALITY_APPEARANCE", "FAMILY_ORIGIN")):
        routes.update({"S05", "S06", "S07", "S12", "S13"})
    if "SPECIFIC_YEAR" in time_tags or "MULTI_YEAR_PERIOD" in time_tags:
        routes.update({"S10", "S14", "S15"})
    if any(tag in topics for tag in ("WEALTH_FINANCE", "PROPERTY_HOUSING", "CAREER_EDUCATION", "LEGAL_CONFLICT", "SEXUALITY_INTIMACY")):
        routes.add("S02")

    governance: list[str] = []
    if "SEXUALITY_INTIMACY" in topics:
        governance.append("SENSITIVE_PERSONAL_ATTRIBUTE")
    if "SPIRITUAL_PARANORMAL" in topics:
        governance.append("NON_FALSIFIABLE_OR_CULTURAL_CLAIM")
    if "GAMBLING_WINDFALL" in topics:
        governance.append("HIGH_VARIANCE_RARE_EVENT")
    if "DEATH" in endpoints:
        governance.append("HIGH_SEVERITY_OUTCOME")

    order = lambda values: list(dict.fromkeys(values))
    return {
        "topic_tags": order(topics),
        "subject_tags": order(subjects),
        "time_scope_tags": order(time_tags),
        "endpoint_tags": order(endpoints),
        "reasoning_skill_tags": order(skills),
        "source_routes": sorted(routes),
        "governance_tags": order(governance),
        "atomization_required": compound,
        "option_atom_hints": option_atoms,
    }


def case_fingerprint(gender: str, true_solar_time: str, pillars: list[str]) -> str:
    value = "|".join([gender, true_solar_time, *pillars]).encode("utf-8")
    return "PERSON-" + hashlib.sha256(value).hexdigest()[:16].upper()


def image_metadata(path: Path, relative_path: str) -> dict[str, Any]:
    with Image.open(path) as image:
        width, height = image.size
    return {
        "path": relative_path,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "width": width,
        "height": height,
    }


def normalize_existing_case(root: Path, number: int) -> dict[str, Any]:
    legacy_id = f"DEV-EXAMPLE-{number:03d}"
    source_path = root / "examples" / "DEV-GROUP-002" / "cases" / f"{legacy_id}.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    ziwei_text = source["ziwei"]["text"].replace("\r\n", "\n").strip() + "\n"
    basic = extract_basic_info(ziwei_text)
    pillars = basic["solar_term_pillars"].split()
    questions = []
    for question in source["questions"]["parsed"]:
        normalized = {
            "question_id": question["question_id"],
            "source_question_number": question["question_id"].removeprefix("Q"),
            "stem": question["stem"],
            "options": question["options"],
        }
        normalized["preblind_profile"] = classify_question(normalized)
        questions.append(normalized)
    bazi = source["bazi"]["transcription"]
    return {
        "schema": CASE_SCHEMA,
        "case_id": f"CASE-{number:03d}",
        "legacy_case_id": legacy_id,
        "source_label": f"例题{number}",
        "answer_isolation": source["answer_isolation"],
        "identity_group_id": case_fingerprint(basic["gender"], basic["true_solar_time"], pillars),
        "input": {**basic, "pillars": {"year": pillars[0], "month": pillars[1], "day": pillars[2], "hour": pillars[3]}},
        "ziwei": {"text": ziwei_text, "sha256": source["ziwei"]["sha256"], "source_path": source_path.relative_to(root).as_posix()},
        "bazi": {**bazi, "source_image": source["bazi"]["source_image"], "transcription_status": source["bazi"]["transcription_status"]},
        "questions": {"question_count": len(questions), "parsed": questions, "source_sha256": source["questions"]["sha256"]},
        "quality": {
            "status": "ACCEPTED_REVEALED_HISTORY" if number == 1 else "ACCEPTED",
            "issues": [],
        },
        "binding": {"source_manifest": "sources/canonical-manifest.json", "training_policy": "config/training-policy.json"},
    }


def build_new_case(repo: Path, case_number: int, source_dir: Path, raw_root: Path, tesseract: str) -> dict[str, Any]:
    label = f"例题{case_number}"
    ziwei_source = source_dir / f"{label}紫微排盘.txt"
    questions_source = source_dir / f"{label}选择.txt"
    bazi_source = source_dir / f"{label}八字排盘.png"
    missing = [path.name for path in (ziwei_source, questions_source, bazi_source) if not path.is_file()]
    if missing:
        raise ValueError(f"{label} missing required files: {missing}")
    raw_dir = raw_root / f"CASE-{case_number:03d}"
    raw_dir.mkdir(parents=True, exist_ok=True)
    ziwei_target = raw_dir / "ziwei.txt"
    questions_target = raw_dir / "questions.txt"
    bazi_target = raw_dir / "bazi.png"
    published_raw_dir = Path("case-bank") / raw_dir.relative_to(raw_root.parent)
    ziwei_text = normalized_text(ziwei_source)
    question_text = normalized_text(questions_source)
    ziwei_target.write_text(ziwei_text, encoding="utf-8")
    questions_target.write_text(question_text, encoding="utf-8")
    shutil.copy2(bazi_source, bazi_target)

    issues: list[dict[str, Any]] = []
    if ANSWER_MARKER.search(question_text):
        issues.append({"code": "ANSWER_OR_REVIEW_MARKER_DETECTED", "severity": "BLOCKING"})
    questions, parse_issues = parse_questions(question_text)
    issues.extend(parse_issues)
    for question in questions:
        question["preblind_profile"] = classify_question(question)

    basic = extract_basic_info(ziwei_text)
    required = {"gender", "clock_time", "true_solar_time", "solar_term_pillars"}
    absent = sorted(required - set(basic))
    if absent:
        issues.append({"code": "ZIWEI_BASIC_INFO_MISSING", "fields": absent, "severity": "BLOCKING"})
        pillars = ["??", "??", "??", "??"]
        birth_year = 0
    else:
        pillars = basic["solar_term_pillars"].split()
        birth_year = int(basic["clock_time"][:4])
        if len(pillars) != 4 or any(pillar not in GANZHI for pillar in pillars):
            issues.append({"code": "SOLAR_TERM_PILLARS_INVALID", "observed": pillars, "severity": "BLOCKING"})

    first_luck_year = None
    ocr_years: list[int] = []
    if birth_year and len(pillars) == 4:
        first_luck_year, ocr_years = ocr_first_luck_year(bazi_target, birth_year, tesseract)
    if first_luck_year is None:
        issues.append({"code": "BAZI_LUCK_BOUNDARY_OCR_UNRESOLVED", "observed_years": ocr_years, "severity": "BLOCKING"})

    bazi: dict[str, Any] = {
        "source_image": image_metadata(
            bazi_target,
            (published_raw_dir / bazi_target.name).as_posix(),
        ),
        "transcription_status": "DERIVED_FROM_ZIWEI_TEXT_AND_IMAGE_YEAR_BOUNDARY",
        "calendar": {
            "gender": basic.get("gender"),
            "solar": basic.get("clock_time"),
            "true_solar": basic.get("true_solar_time"),
            "lunar": basic.get("lunar_time"),
        },
        "pillars": {"year": pillars[0], "month": pillars[1], "day": pillars[2], "hour": pillars[3]},
    }
    if all(pillar in GANZHI for pillar in pillars):
        day_stem = pillars[2][0]
        bazi["hidden_stems_ten_gods"] = {
            name: [f"{stem} {ten_god(day_stem, stem)}" for stem in HIDDEN_STEMS[pillar[1]]]
            for name, pillar in zip(("year", "month", "day", "hour"), pillars, strict=True)
        }
    if first_luck_year is not None:
        bazi["luck"] = infer_luck_cycles(basic["gender"], pillars, first_luck_year, birth_year)
        bazi["luck"]["ocr_year_candidates"] = ocr_years

    blocking = [issue for issue in issues if issue["severity"] == "BLOCKING"]
    return {
        "schema": CASE_SCHEMA,
        "case_id": f"CASE-{case_number:03d}",
        "legacy_case_id": None,
        "source_label": label,
        "answer_isolation": {"answer_payload_present": False, "answer_reference_disclosed": False, "status": "PROGRAMMATICALLY_SCANNED"},
        "identity_group_id": case_fingerprint(basic.get("gender", ""), basic.get("true_solar_time", ""), pillars),
        "input": {**basic, "pillars": bazi["pillars"]},
        "ziwei": {
            "text": ziwei_text,
            "sha256": sha256_file(ziwei_target),
            "source_path": (published_raw_dir / ziwei_target.name).as_posix(),
        },
        "bazi": bazi,
        "questions": {
            "question_count": len(questions),
            "parsed": questions,
            "source_sha256": sha256_file(questions_target),
            "source_path": (published_raw_dir / questions_target.name).as_posix(),
        },
        "quality": {"status": "BLOCKED_INPUT" if blocking else "ACCEPTED", "issues": issues},
        "binding": {"source_manifest": "sources/canonical-manifest.json", "training_policy": "config/training-policy.json"},
    }


def assign_splits(cases: list[dict[str, Any]]) -> dict[str, list[str]]:
    accepted = [case for case in cases if not case["quality"]["status"].startswith("BLOCKED")]
    reserved_validation_cases = 21
    reserved_holdout_cases = 21
    development_cases = len(accepted) - reserved_validation_cases - reserved_holdout_cases
    if development_cases < 1:
        raise ValueError(f"at least 43 accepted cases are required, found {len(accepted)}")
    targets = {
        "DEVELOPMENT": development_cases,
        "STAGE_VALIDATION": reserved_validation_cases,
        "FINAL_HOLDOUT": reserved_holdout_cases,
    }
    assignments: dict[str, list[str]] = {name: [] for name in targets}
    tag_counts: dict[str, Counter[str]] = {name: Counter() for name in targets}
    all_tag_counts: Counter[str] = Counter()
    case_tags: dict[str, set[str]] = {}
    for case in accepted:
        tags = {tag for question in case["questions"]["parsed"] for tag in question["preblind_profile"]["topic_tags"]}
        case_tags[case["case_id"]] = tags
        all_tag_counts.update(tags)

    legacy = [case for case in accepted if case["legacy_case_id"]]
    for case in sorted(legacy, key=lambda item: item["case_id"]):
        assignments["DEVELOPMENT"].append(case["case_id"])
        tag_counts["DEVELOPMENT"].update(case_tags[case["case_id"]])

    remaining = [case for case in accepted if not case["legacy_case_id"]]
    remaining.sort(
        key=lambda case: (
            -sum(1 / all_tag_counts[tag] for tag in case_tags[case["case_id"]]),
            hashlib.sha256(case["case_id"].encode()).hexdigest(),
        )
    )
    proportions = {name: targets[name] / len(accepted) for name in targets}
    for case in remaining:
        case_id = case["case_id"]
        candidates = [name for name in targets if len(assignments[name]) < targets[name]]
        governance = {tag for question in case["questions"]["parsed"] for tag in question["preblind_profile"]["governance_tags"]}
        rare_sensitive = governance and any(all_tag_counts[tag] < 5 for tag in case_tags[case_id])
        if rare_sensitive and len(assignments["DEVELOPMENT"]) < targets["DEVELOPMENT"]:
            chosen = "DEVELOPMENT"
        else:
            def penalty(name: str) -> tuple[float, str]:
                tag_penalty = 0.0
                for tag in case_tags[case_id]:
                    target = all_tag_counts[tag] * proportions[name]
                    before = tag_counts[name][tag] - target
                    after = tag_counts[name][tag] + 1 - target
                    tag_penalty += after * after - before * before
                fill = (len(assignments[name]) + 1) / targets[name]
                return tag_penalty + fill * 0.05, name
            chosen = min(candidates, key=penalty)
        assignments[chosen].append(case_id)
        tag_counts[chosen].update(case_tags[case_id])
    return assignments


def coverage(cases: list[dict[str, Any]], case_ids: set[str] | None = None) -> dict[str, Any]:
    topics: Counter[str] = Counter()
    endpoints: Counter[str] = Counter()
    skills: Counter[str] = Counter()
    governance: Counter[str] = Counter()
    question_count = 0
    selected_case_count = 0
    for case in cases:
        if case_ids is not None and case["case_id"] not in case_ids:
            continue
        selected_case_count += 1
        for question in case["questions"]["parsed"]:
            question_count += 1
            profile = question["preblind_profile"]
            topics.update(profile["topic_tags"])
            endpoints.update(profile["endpoint_tags"])
            skills.update(profile["reasoning_skill_tags"])
            governance.update(profile["governance_tags"])
    return {
        "case_count": selected_case_count,
        "question_count": question_count,
        "topic_question_counts": dict(sorted(topics.items())),
        "endpoint_question_counts": dict(sorted(endpoints.items())),
        "reasoning_skill_question_counts": dict(sorted(skills.items())),
        "governance_question_counts": dict(sorted(governance.items())),
    }


def parse_assignment(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("expected NAME=PATH")
    name, path = value.split("=", 1)
    return name, Path(path).resolve()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--source", action="append", type=parse_assignment, required=True)
    parser.add_argument("--tesseract", default="tesseract")
    args = parser.parse_args()
    repo = args.repo.resolve()
    final_output = repo / "case-bank"
    output = repo / "case-bank.building"
    cases_root = output / "cases"
    raw_root = output / "raw"
    if output.exists():
        shutil.rmtree(output)
    cases_root.mkdir(parents=True)
    raw_root.mkdir(parents=True)

    discovered: dict[int, tuple[str, Path]] = {}
    replacement_events: list[dict[str, Any]] = []
    for source_name, source_root in args.source:
        for directory in source_root.glob("**/例题*"):
            if not directory.is_dir():
                continue
            match = re.fullmatch(r"例题(\d+)", directory.name)
            if not match:
                continue
            number = int(match.group(1))
            if number < 6 or number > 107:
                continue
            if number in discovered:
                replacement_events.append({
                    "case_id": f"CASE-{number:03d}",
                    "discarded_source": discovered[number][0],
                    "selected_source": source_name,
                    "content_retained_from_discarded_source": False,
                })
            discovered[number] = (source_name, directory)
    missing = sorted(set(range(6, 108)) - set(discovered))
    if missing:
        raise ValueError(f"missing cases: {missing}")

    cases = [normalize_existing_case(repo, number) for number in range(1, 6)]
    for number in range(6, 108):
        cases.append(build_new_case(repo, number, discovered[number][1], raw_root, args.tesseract))
    fingerprints: defaultdict[str, list[str]] = defaultdict(list)
    for case in cases:
        fingerprints[case["identity_group_id"]].append(case["case_id"])
    duplicate_people = {key: value for key, value in fingerprints.items() if len(value) > 1}
    assignments = assign_splits(cases)
    split_for_case = {case_id: split for split, ids in assignments.items() for case_id in ids}
    for case in cases:
        case["dataset_split"] = split_for_case.get(case["case_id"], "BLOCKED")
        write_json(cases_root / f"{case['case_id']}.json", case)

    partition_root = output / "partitions"
    for split, ids in assignments.items():
        write_json(partition_root / f"{split.lower().replace('_', '-')}.json", {
            "schema": "FORTUNE-CASE-BANK-PARTITION-V1",
            "partition_id": split,
            "case_order": ids,
            "historical_case_ids": [case_id for case_id in ids if case_id in REVEALED_HISTORY_CASE_IDS],
            "first_blind_schedule": [case_id for case_id in ids if case_id not in REVEALED_HISTORY_CASE_IDS],
            "cases": {case_id: f"case-bank/cases/{case_id}.json" for case_id in ids},
            "coverage": coverage(cases, set(ids)),
        })

    blocked = [case for case in cases if case["quality"]["status"].startswith("BLOCKED")]
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "corpus_id": "FORTUNE-CASE-BANK-107-V1",
        "expected_case_range": {"first": 1, "last": 107, "count": 107},
        "case_count": len(cases),
        "question_count": sum(case["questions"]["question_count"] for case in cases),
        "accepted_case_count": len(cases) - len(blocked),
        "blocked_case_count": len(blocked),
        "revealed_history_case_ids": sorted(REVEALED_HISTORY_CASE_IDS),
        "blocked_cases": [{"case_id": case["case_id"], "issues": case["quality"]["issues"]} for case in blocked],
        "answer_payload_present": False,
        "duplicate_identity_groups": duplicate_people,
        "replacement_events": replacement_events,
        "partitions": {name: ids for name, ids in assignments.items()},
        "coverage": coverage(cases),
        "case_hashes": {case["case_id"]: object_sha256(case) for case in cases},
    }
    write_json(output / "manifest.json", manifest)
    write_json(output / "intake-audit.json", {
        "schema": "FORTUNE-CASE-BANK-INTAKE-AUDIT-V1",
        "archive_or_batch_sources": [
            {"label": name, "path_excluded_from_repository": True, "case_directories_found": sum(1 for path in root.glob("**/例题*") if path.is_dir())}
            for name, root in args.source
        ],
        "discarded_source_contents_retained": False,
        "replacement_events": replacement_events,
        "source_question_numbering_is_not_authoritative": True,
        "normalized_question_ids": "Q1..Qn in source order",
        "answer_scan": "PASS_FOR_SELECTED_SOURCES" if not any(issue["code"] == "ANSWER_OR_REVIEW_MARKER_DETECTED" for case in cases for issue in case["quality"]["issues"]) else "BLOCKED_MATCH_FOUND",
    })
    previous_output = repo / "case-bank.previous"
    if previous_output.exists():
        shutil.rmtree(previous_output)
    if final_output.exists():
        final_output.rename(previous_output)
    try:
        output.rename(final_output)
    except Exception:
        if previous_output.exists() and not final_output.exists():
            previous_output.rename(final_output)
        raise
    if previous_output.exists():
        shutil.rmtree(previous_output)
    print(json.dumps({
        "case_count": manifest["case_count"],
        "question_count": manifest["question_count"],
        "accepted_case_count": manifest["accepted_case_count"],
        "blocked_cases": [case["case_id"] for case in blocked],
        "split_counts": {name: len(ids) for name, ids in assignments.items()},
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
