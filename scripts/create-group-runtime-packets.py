from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


DOMAIN_TERMS = {
    "health": ["健康", "疾厄", "疾病", "病痛", "手术", "住院", "生命危险", "糖尿病", "皮肤", "肝", "肠胃", "胃", "脚", "腿", "伤", "血刃", "羊刃", "体弱", "肥胖", "抑郁", "精神"],
    "marriage": ["婚姻", "婚恋", "结婚", "离婚", "再婚", "夫妻", "配偶", "丈夫", "妻子", "女友", "伴侣", "感情", "桃花", "红鸾", "天喜", "廉贞", "贪狼"],
    "children": ["子女", "孩子", "儿女", "生子", "生女", "生育", "流产", "无子嗣", "子息"],
    "family": ["家庭", "家境", "父母", "父亲", "母亲", "兄弟", "姐妹", "外婆", "抚养", "出生", "儿时", "田宅", "父母宫"],
    "career": ["事业", "职业", "工作", "官禄", "公司", "企业", "老板", "管理", "经营", "生意", "创业", "打工", "兼职", "行业", "传媒", "物流", "航运", "牧师", "入殓师", "舞女", "卖艺", "乐团", "餐厅", "房地产"],
    "wealth": ["财富", "财运", "财政", "财帛", "收入", "存款", "负债", "债务", "得财", "破财", "偏财", "积蓄", "开支", "富裕", "贫穷", "小康"],
    "education": ["学历", "读书", "大学", "中学", "高中", "硕士", "博士", "毕业", "辍学", "学校", "休学", "比赛", "获奖"],
    "personality": ["性格", "性情", "个性", "聪明", "聪敏", "勤力", "懒惰", "固执", "叛逆", "内向", "外向", "情绪化", "急性子", "可靠", "慷慨", "好色", "风流"],
    "appearance": ["样貌", "体貌", "身材", "高大", "魁梧", "残疾", "腿脚", "早产"],
    "accident": ["意外", "车祸", "交通", "打劫", "受伤", "手脚", "遗传病", "入院", "手术"],
    "legal": ["官非", "判监", "监禁", "举报", "赶出学校", "手续"],
    "time": ["大限", "流年", "流月", "应期", "四化", "化禄", "化权", "化科", "化忌", "合", "冲", "刑", "害", "破", "开始", "发生", "截至", "一直", "持续"],
    "endpoint": ["实际发生", "正式终点", "手续", "结婚", "离婚", "去世", "病亡", "死亡", "当上", "获任", "卖掉", "入院", "手术", "生育"],
}

LIBRARY_DOMAIN_SCOPE = {
    "S00": ["time", "endpoint"],
    "S01": ["time", "endpoint"],
    "S02": list(DOMAIN_TERMS),
    "S03": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident", "legal", "time", "endpoint"],
    "S04": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident"],
    "S05": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident"],
    "S06": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident"],
    "S07": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident"],
    "S08": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident", "time"],
    "S09": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident", "time"],
    "S10": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident", "time"],
    "S11": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident"],
    "S12": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident"],
    "S13": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident"],
    "S14": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident", "time"],
    "S15": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident", "time"],
    "S16": ["health", "marriage", "children", "family", "career", "wealth", "education", "personality", "appearance", "accident", "time", "endpoint"],
    "S17": list(DOMAIN_TERMS),
    "S18": list(DOMAIN_TERMS),
    "S19": ["time", "endpoint"],
}

STAR_NAMES = [
    "紫微", "天机", "太阳", "武曲", "天同", "廉贞", "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军",
    "文昌", "文曲", "左辅", "右弼", "天魁", "天钺", "禄存", "擎羊", "陀罗", "火星", "铃星", "地空", "地劫",
    "红鸾", "天喜", "天姚", "咸池", "天马", "天刑", "天空", "天哭", "华盖", "孤辰", "寡宿", "血刃", "羊刃",
]

TEN_GODS = ["比肩", "劫财", "食神", "伤官", "偏财", "正财", "七杀", "正官", "偏印", "正印"]
STEMS_BRANCHES = list("甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥")
STOP_TERMS = {"命主", "如何", "怎样", "情况", "截至", "时候", "何事", "发生", "现在", "此人", "数年", "问题", "题目"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def object_hash(value: dict[str, Any]) -> str:
    body = dict(value)
    body.pop("object_hash", None)
    return hashlib.sha256(canonical_bytes(body)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json_new(path: Path, value: dict[str, Any]) -> None:
    if path.exists():
        raise SystemExit(f"immutable output exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    value["object_hash"] = object_hash(value)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def detect_domains(text: str) -> set[str]:
    domains: set[str] = set()
    for domain, terms in DOMAIN_TERMS.items():
        if any(term in text for term in terms):
            domains.add(domain)
    if re.search(r"(?:19|20)\d{2}", text):
        domains.add("time")
    return domains or {"endpoint"}


def extract_chart_terms(case: dict[str, Any]) -> set[str]:
    text = case.get("ziwei", {}).get("text", "")
    terms = {name for name in STAR_NAMES if name in text}
    terms.update({palace for palace in ["命宫", "兄弟宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫", "迁移宫", "交友宫", "官禄宫", "田宅宫", "福德宫", "父母宫"] if palace in text.replace(" ", "")})
    bazi = case.get("bazi", {}).get("transcription", {})
    bazi_text = json.dumps(bazi, ensure_ascii=False)
    terms.update({term for term in TEN_GODS if term in bazi_text})
    terms.update({char for char in STEMS_BRANCHES if char in bazi_text})
    return terms


def build_profile(case: dict[str, Any]) -> dict[str, Any]:
    qmap: dict[str, set[str]] = {}
    domain_map: dict[str, set[str]] = {}
    chart_terms = extract_chart_terms(case)
    for question in case["questions"]["parsed"]:
        qid = question["question_id"]
        text = question.get("stem", "") + " " + " ".join(option.get("text", "") for option in question.get("options", []))
        domains = detect_domains(text)
        terms = set()
        for domain in domains:
            terms.update(DOMAIN_TERMS[domain])
        terms.update(term for term in chart_terms if term in text or term in {"命宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫", "官禄宫", "父母宫", "田宅宫"})
        terms.update(re.findall(r"(?:19|20)\d{2}", text))
        terms.difference_update(STOP_TERMS)
        qmap[qid] = terms
        domain_map[qid] = domains
    return {"case": case, "question_keywords": qmap, "question_domains": domain_map, "chart_terms": chart_terms}


def keywords_for_library(profile: dict[str, Any], library_id: str) -> tuple[set[str], dict[str, set[str]]]:
    allowed_domains = set(LIBRARY_DOMAIN_SCOPE.get(library_id, DOMAIN_TERMS.keys()))
    keyword_qids: dict[str, set[str]] = defaultdict(set)
    for qid, domains in profile["question_domains"].items():
        if not (domains & allowed_domains):
            continue
        for keyword in profile["question_keywords"][qid]:
            if len(keyword) >= 2 or keyword in STEMS_BRANCHES:
                keyword_qids[keyword].add(qid)
    if library_id in {"S05", "S06", "S07", "S08", "S09", "S10"}:
        for keyword in profile["chart_terms"]:
            if len(keyword) >= 2:
                keyword_qids[keyword].update(profile["question_keywords"].keys())
    if library_id in {"S11", "S12", "S13", "S14", "S15", "S16"}:
        bazi_text = json.dumps(profile["case"].get("bazi", {}).get("transcription", {}), ensure_ascii=False)
        for keyword in TEN_GODS + STEMS_BRANCHES:
            if keyword in bazi_text:
                keyword_qids[keyword].update(profile["question_keywords"].keys())
    return set(keyword_qids), keyword_qids


def extract_source_items(
    source_row: dict[str, Any],
    profiles: dict[str, dict[str, Any]],
    max_per_question: int,
) -> dict[str, list[dict[str, Any]]]:
    library_id = source_row["library_id"]
    path = Path(source_row["repository_relative_path"])
    if not path.is_file():
        raise SystemExit(f"missing source file: {path}")
    actual_sha = sha256_file(path)
    if actual_sha != source_row["sha256_raw_file_bytes"]:
        raise SystemExit(f"source sha mismatch: {path}")
    if path.stat().st_size != source_row["file_size_bytes"]:
        raise SystemExit(f"source size mismatch: {path}")

    per_case_keywords: dict[str, set[str]] = {}
    per_case_targets: dict[str, dict[str, set[str]]] = {}
    union_keywords: set[str] = set()
    for case_id, profile in profiles.items():
        keywords, targets = keywords_for_library(profile, library_id)
        per_case_keywords[case_id] = keywords
        per_case_targets[case_id] = targets
        union_keywords.update(keywords)

    if not union_keywords:
        return {case_id: [] for case_id in profiles}

    pattern = re.compile("|".join(re.escape(k) for k in sorted(union_keywords, key=lambda x: (-len(x), x))))
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    heaps: dict[tuple[str, str], list[tuple[int, int, dict[str, Any]]]] = defaultdict(list)

    for index, line in enumerate(lines):
        found = set(pattern.findall(line))
        if not found:
            continue
        for case_id in profiles:
            matched = found & per_case_keywords[case_id]
            if not matched:
                continue
            qids: set[str] = set()
            for keyword in matched:
                qids.update(per_case_targets[case_id].get(keyword, set()))
            if not qids:
                continue
            start = max(0, index - 1)
            end = min(len(lines), index + 2)
            segment = "\n".join(lines[start:end]).strip()
            score = sum(max(2, len(keyword)) for keyword in matched) + 8 * len(qids)
            item = {
                "library_id": library_id,
                "repository_relative_path": str(path),
                "source_sha256": actual_sha,
                "source_size_bytes": path.stat().st_size,
                "physical_selector": {"line_start": start + 1, "line_end": end},
                "parent_sentence_segment": segment,
                "matched_keywords": sorted(matched),
                "target_question_ids": sorted(qids),
                "direction": "UNASSESSED_PRECONTENT",
                "capability_ceiling": "CONTEXT_OR_MECHANISM_ONLY_UNTIL_EVIDENCE_LEDGER_ASSESSMENT",
            }
            for qid in qids:
                heap = heaps[(case_id, qid)]
                entry = (score, -(index + 1), item)
                if len(heap) < max_per_question:
                    heapq.heappush(heap, entry)
                elif entry[:2] > heap[0][:2]:
                    heapq.heapreplace(heap, entry)

    results: dict[str, list[dict[str, Any]]] = {}
    for case_id in profiles:
        selected: dict[tuple[int, int], dict[str, Any]] = {}
        for qid in profiles[case_id]["question_keywords"]:
            for _, _, item in heaps.get((case_id, qid), []):
                selector = item["physical_selector"]
                key = (selector["line_start"], selector["line_end"])
                if key not in selected:
                    selected[key] = dict(item)
                else:
                    merged = set(selected[key]["target_question_ids"]) | set(item["target_question_ids"])
                    selected[key]["target_question_ids"] = sorted(merged)
        results[case_id] = [selected[key] for key in sorted(selected)]
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True)
    parser.add_argument("--max-per-question", type=int, default=8)
    args = parser.parse_args()

    request_path = Path(args.request)
    request = read_json(request_path)
    if request.get("schema") != "GROUP-RUNTIME-PACKET-REQUEST-V1" or request.get("status") != "REQUESTED":
        raise SystemExit("invalid runtime packet request")

    clean_path = Path(request["clean_start_path"])
    clean = read_json(clean_path)
    if clean.get("status") != "READY_FOR_CLEAN_GROUP_PREDICTION" or clean.get("answer_data_available") is not False:
        raise SystemExit("clean start not ready")
    if clean.get("group_run_id") != request.get("group_run_id") or clean.get("group_id") != request.get("group_id"):
        raise SystemExit("group identity mismatch")

    knowledge_manifest_path = Path(request["knowledge_manifest_path"])
    method_release_path = Path(request["method_release_path"])
    model_release_path = Path(request["model_release_path"])
    knowledge = read_json(knowledge_manifest_path)
    method = read_json(method_release_path)
    model = read_json(model_release_path)

    bindings = request["bindings"]
    checks = {
        "knowledge_release_id": knowledge.get("knowledge_release_id"),
        "method_release_id": method.get("method_release_id"),
        "model_release_id": model.get("model_release_id"),
        "main_prompt_runtime_id": method.get("main_prompt_runtime_id"),
    }
    for key, actual in checks.items():
        if bindings.get(key) != actual:
            raise SystemExit(f"binding mismatch {key}: {bindings.get(key)} != {actual}")

    profiles: dict[str, dict[str, Any]] = {}
    case_rows: dict[str, dict[str, Any]] = {}
    output_root = Path(request["output_root"])
    for case_row in clean["cases"]:
        case_id = case_row["case_id"]
        case_path = Path(case_row["input_path"])
        case = read_json(case_path)
        if case.get("case_id") != case_id:
            raise SystemExit(f"case id mismatch: {case_path}")
        if case.get("answer_isolation", {}).get("answer_payload_present") is not False:
            raise SystemExit(f"answer payload present: {case_id}")
        if case.get("answer_isolation", {}).get("answer_reference_disclosed") is not False:
            raise SystemExit(f"answer reference disclosed: {case_id}")
        profiles[case_id] = build_profile(case)
        case_rows[case_id] = case_row

        sidecar_root = output_root / "case-input-sidecars" / case_id
        sidecar_root.mkdir(parents=True, exist_ok=True)
        ziwei_path = sidecar_root / "ziwei.txt"
        bazi_path = sidecar_root / "bazi.json"
        questions_path = sidecar_root / "questions.json"
        for target in [ziwei_path, bazi_path, questions_path]:
            if target.exists():
                raise SystemExit(f"immutable output exists: {target}")
        ziwei_path.write_text(case.get("ziwei", {}).get("text", ""), encoding="utf-8", newline="\n")
        bazi_path.write_text(json.dumps(case.get("bazi", {}), ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        questions_path.write_text(json.dumps(case.get("questions", {}), ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    extracted_by_case: dict[str, list[dict[str, Any]]] = {case_id: [] for case_id in profiles}
    route_rows: dict[str, list[dict[str, Any]]] = {case_id: [] for case_id in profiles}
    for source_row in knowledge["source_files"]:
        library_id = source_row["library_id"]
        results = extract_source_items(source_row, profiles, args.max_per_question)
        for case_id, items in results.items():
            for item in items:
                item["packet_item_id"] = f"SP-{case_id}-{library_id}-{len(extracted_by_case[case_id]) + 1:05d}"
                extracted_by_case[case_id].append(item)
            route_rows[case_id].append({
                "library_id": library_id,
                "repository_relative_path": source_row["repository_relative_path"],
                "sha256_raw_file_bytes": source_row["sha256_raw_file_bytes"],
                "file_size_bytes": source_row["file_size_bytes"],
                "selected_item_count": len(items),
                "route_status": "ITEMS_SELECTED" if items else "NO_KEYWORD_MATCH_REQUIRES_NOT_APPLICABLE_OR_FOLLOWUP",
            })

    generated_paths: list[str] = []
    for case_id, profile in profiles.items():
        case_row = case_rows[case_id]
        case_root = output_root / "runtime-packets" / case_id
        source_packet_path = case_root / "source-packet.json"
        method_packet_path = case_root / "method-packet.json"
        run_contract_path = case_root / "run-contract.json"

        source_packet = {
            "schema": "FORTUNE-SOURCE-PACKET-V1",
            "status": "PRECONTENT_READY",
            "case_id": case_id,
            "run_id": case_row["case_run_id"],
            "group_run_id": clean["group_run_id"],
            "knowledge_release_id": knowledge["knowledge_release_id"],
            "knowledge_manifest_path": str(knowledge_manifest_path),
            "knowledge_manifest_object_hash": knowledge["object_hash"],
            "answer_data_available": False,
            "route_rows": route_rows[case_id],
            "items": extracted_by_case[case_id],
            "question_coverage": {
                qid: {
                    "domains": sorted(profile["question_domains"][qid]),
                    "planned_keywords": sorted(profile["question_keywords"][qid]),
                    "packet_item_ids": [item["packet_item_id"] for item in extracted_by_case[case_id] if qid in item["target_question_ids"]],
                }
                for qid in profile["question_keywords"]
            },
        }
        write_json_new(source_packet_path, source_packet)

        method_items = []
        for stage in method["stages"]:
            for rule in stage["rules"]:
                method_items.append({
                    "packet_item_id": f"MP-{case_id}-{rule['rule_id']}",
                    "stage_id": stage["stage_id"],
                    "rule_id": rule["rule_id"],
                    "requirement": rule["requirement"],
                    "failure_status": rule["failure_status"],
                    "source_authority": rule["source_authority"],
                })
        method_packet = {
            "schema": "FORTUNE-METHOD-PACKET-V1",
            "status": "READY",
            "case_id": case_id,
            "run_id": case_row["case_run_id"],
            "group_run_id": clean["group_run_id"],
            "method_release_id": method["method_release_id"],
            "method_release_path": str(method_release_path),
            "method_release_object_hash": method["object_hash"],
            "mandatory_stage_ids": method["mandatory_stage_ids"],
            "items": method_items,
        }
        write_json_new(method_packet_path, method_packet)

        sidecar_root = output_root / "case-input-sidecars" / case_id
        run_contract = {
            "schema": "FORTUNE-RUN-CONTRACT-V1",
            "status": "READY_FOR_BLIND_PREDICTION",
            "case_id": case_id,
            "run_id": case_row["case_run_id"],
            "group_id": clean["group_id"],
            "group_run_id": clean["group_run_id"],
            "group_session_id": clean["group_session_id"],
            "bindings": bindings,
            "answer_data_available": False,
            "input_snapshot": {
                "path": case_row["input_path"],
                "sha256": case_row["input_sha256"],
                "ziwei_sidecar_path": str(sidecar_root / "ziwei.txt"),
                "ziwei_sidecar_sha256": sha256_file(sidecar_root / "ziwei.txt"),
                "bazi_sidecar_path": str(sidecar_root / "bazi.json"),
                "bazi_sidecar_sha256": sha256_file(sidecar_root / "bazi.json"),
                "questions_sidecar_path": str(sidecar_root / "questions.json"),
                "questions_sidecar_sha256": sha256_file(sidecar_root / "questions.json"),
            },
            "source_packet_path": str(source_packet_path),
            "method_packet_path": str(method_packet_path),
            "prediction_skeleton_path": case_row["skeleton_path"],
            "required_stages": method["mandatory_stage_ids"],
            "formal_scoring_permission": "CONDITIONAL_ON_CAUSAL_USE_RECEIPT_PASS",
        }
        write_json_new(run_contract_path, run_contract)
        generated_paths.extend([
            str(sidecar_root / "ziwei.txt"),
            str(sidecar_root / "bazi.json"),
            str(sidecar_root / "questions.json"),
            str(source_packet_path),
            str(method_packet_path),
            str(run_contract_path),
        ])

    source_paths = [row["repository_relative_path"] for row in knowledge["source_files"]]
    exact_paths = list(dict.fromkeys(
        clean["retrieval_policy"]["exact_allowed_paths"]
        + [str(request_path), str(clean_path), str(knowledge_manifest_path), str(method_release_path), str(model_release_path)]
        + source_paths
        + generated_paths
    ))
    transport_path = output_root / "retrieval-transport-plan.json"
    transport = {
        "schema": "FORTUNE-RETRIEVAL-TRANSPORT-PLAN-V1",
        "status": "READY",
        "group_id": clean["group_id"],
        "group_run_id": clean["group_run_id"],
        "parent_clean_start_path": str(clean_path),
        "parent_clean_start_blob_sha": request.get("parent_clean_start_blob_sha"),
        "mode": "EXACT_PATH_ONLY",
        "repository_search_allowed": False,
        "history_navigation_allowed": False,
        "answer_data_available": False,
        "exact_allowed_paths": exact_paths,
        "generated_paths": generated_paths,
    }
    write_json_new(transport_path, transport)

    result = {
        "schema": "GROUP-RUNTIME-PACKET-BUILD-RESULT-V1",
        "status": "READY_FOR_BLIND_PREDICTION",
        "group_run_id": clean["group_run_id"],
        "case_count": len(profiles),
        "source_packet_item_counts": {case_id: len(extracted_by_case[case_id]) for case_id in profiles},
        "transport_plan_path": str(transport_path),
        "generated_path_count": len(generated_paths) + 1,
        "answer_data_available": False,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
