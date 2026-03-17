from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from cli_support import JsonObject, SKILL_ROOT, now_iso, write_json, write_text


BANNED_TERMS = ["文档知识库"]
TARGET_SKILL_ROOT = SKILL_ROOT


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _clean_lines(request_text: str) -> list[str]:
    lines = [line.strip(" -\t") for line in request_text.splitlines()]
    compact = [line for line in lines if line]
    return compact or [request_text.strip()]


def _extract_matches(request_text: str, mapping: dict[str, list[str]]) -> list[str]:
    lowered = request_text.lower()
    matches: list[str] = []
    for label, needles in mapping.items():
        if any(needle.lower() in lowered for needle in needles):
            matches.append(label)
    return matches


def _primary_mode(request_text: str) -> str:
    lowered = request_text.lower()
    if any(token in lowered for token in ("重构", "改造", "refactor", "subagent", "runtask")):
        return "skill_governance"
    if any(token in lowered for token in ("lint", "审计", "校验")):
        return "audit_and_govern"
    if any(token in lowered for token in ("刷新", "refresh", "同步产物")):
        return "artifact_refresh"
    return "skill_governance"


def _keyword_first_hints(request_text: str) -> JsonObject:
    lowered = request_text.lower()
    rewrite = any(token in lowered for token in ("删掉重写", "重写", "rewrite"))
    replace = any(token in lowered for token in ("keyword first", "替换", "replace"))
    minimal_add = any(token in lowered for token in ("最小必要新增", "新增", "minimal add"))
    priority = []
    if rewrite:
        priority.append("rewrite")
    if replace:
        priority.append("keyword_first_replace")
    if minimal_add:
        priority.append("minimal_add")
    if not priority:
        priority = ["rewrite", "keyword_first_replace", "minimal_add"]
    return {
        "requested_signals": {"rewrite": rewrite, "keyword_first_replace": replace, "minimal_add": minimal_add},
        "priority_order": priority,
        "must_decide_explicitly": True,
    }


def _split_objectives(request_text: str) -> dict[str, list[str]]:
    lines = _clean_lines(request_text)
    artifact_objectives: list[str] = []
    skill_objectives: list[str] = []
    validation_objectives: list[str] = []
    for line in lines:
        lowered = line.lower()
        if any(token in lowered for token in ("验证", "校验", "acceptance", "evidence", "证据", "git")):
            validation_objectives.append(line)
            continue
        if any(token in lowered for token in ("skill", "技能", "runtime", "subagent", "tmux", "runtask", "factory", "intent")):
            skill_objectives.append(line)
            continue
        artifact_objectives.append(line)
    if not artifact_objectives:
        artifact_objectives.append("刷新并收敛 mother_doc 真源与 client mirror 的实验性框架产物。")
    if not skill_objectives:
        skill_objectives.append("改造 Workflow-SiteMap-Creation 本体，使 factory 后进入 intent 强化、background subagent 与 Functional-Analysis-Runtask 九阶段闭环。")
    if not validation_objectives:
        validation_objectives.append("使用 backend terminal 做真实验证，补齐 evidence、lint、git traceability 与产物一致性检查。")
    return {
        "artifact_objectives": artifact_objectives,
        "skill_objectives": skill_objectives,
        "validation_objectives": validation_objectives,
    }


def factoryize_request(request_text: str) -> JsonObject:
    excerpt = request_text.strip().replace("\n", " ")
    objectives = _split_objectives(request_text)
    architecture_axes = _extract_matches(
        request_text,
        {
            "factory_first": ["factory", "双重目的", "拆分"],
            "intent_enhancement": ["Meta-Enhance-Prompt", "意图强化", "intent"],
            "runtask_nine_stage": ["Functional-Analysis-Runtask", "analysis_loop", "research", "architect", "preview", "impact", "plan", "validation"],
            "background_subagent": ["subagent", "tmux", "background terminal"],
            "artifact_refresh": ["产物", "frontmatter", "字段语义", "文档关系", "mirror"],
        },
    )
    validation_axes = _extract_matches(
        request_text,
        {
            "backend_terminal": ["backend terminal", "终端", "validation"],
            "git_traceability": ["git", "push", "留痕"],
            "artifact_consistency": ["mirror", "一致", "refresh", "lint"],
        },
    )
    return {
        "status": "pass",
        "source_digest": _digest(request_text),
        "source_excerpt": excerpt[:500],
        "primary_mode": _primary_mode(request_text),
        "dual_purpose": objectives,
        "factory_split": {
            "architecture_axes": architecture_axes,
            "validation_axes": validation_axes,
            "keyword_first": _keyword_first_hints(request_text),
            "must_use_meta_enhance_prompt": True,
            "must_use_runtask_analysis_loop": True,
            "required_runtask_stages": [
                "research",
                "architect",
                "preview",
                "design",
                "impact",
                "plan",
                "implementation",
                "validation",
                "final_delivery",
            ],
        },
        "target_scope": {
            "skill_root": str(TARGET_SKILL_ROOT),
            "truth_root": "Octopus_OS/Development_Docs/mother_doc",
            "client_mirror_root": "Octopus_OS/Client_Applications/mother_doc",
        },
        "framework_constraints": {
            "banned_terms": BANNED_TERMS,
            "must_preserve_single_truth_source": True,
            "must_refresh_experimental_artifacts": True,
            "must_not_reduce_to_static_template": True,
        },
        "created_at": now_iso(),
    }


def build_intent_draft(factory_payload: JsonObject) -> str:
    dual_purpose = factory_payload["dual_purpose"]
    split = factory_payload["factory_split"]
    assert isinstance(dual_purpose, dict)
    assert isinstance(split, dict)
    artifact_objectives = dual_purpose["artifact_objectives"]
    skill_objectives = dual_purpose["skill_objectives"]
    validation_objectives = dual_purpose["validation_objectives"]
    assert isinstance(artifact_objectives, list)
    assert isinstance(skill_objectives, list)
    assert isinstance(validation_objectives, list)
    architecture_axes = split["architecture_axes"]
    validation_axes = split["validation_axes"]
    keyword_first = split["keyword_first"]
    assert isinstance(architecture_axes, list)
    assert isinstance(validation_axes, list)
    assert isinstance(keyword_first, dict)
    return (
        "INTENT:\n"
        "围绕 Workflow-SiteMap-Creation 执行一次可落地闭环治理：先消费 factory 输出，"
        "再调用 Meta-Enhance-Prompt 生成可执行强化意图，然后由主 agent 在 tmux background terminal 中启动固定模型 "
        "gpt-5.4 / reasoning high 的 subagent，强制其使用 Functional-Analysis-Runtask 的 analysis_loop 九阶段改造目标技能本体。"
        f" artifact 目标：{'；'.join(artifact_objectives)}。"
        f" skill 目标：{'；'.join(skill_objectives)}。"
        f" validation 目标：{'；'.join(validation_objectives)}。"
        f" 必须覆盖的结构轴：{', '.join(architecture_axes) or 'factory-first, intent-enhancement, runtask-nine-stage'}。"
        f" 必须覆盖的验证轴：{', '.join(validation_axes) or 'backend-terminal, git-traceability, artifact-consistency'}。"
        " 进入具体修改决策时必须显式输出 keyword-first 判定，"
        f"优先序为 {', '.join(keyword_first['priority_order'])}；不得退化为常量意图、固定模板重刷或伪闭环。"
    )


def register_run_snapshot(snapshot: JsonObject) -> JsonObject:
    registry_path = SKILL_ROOT / "references" / "governance" / "SELF_EVOLUTION_SIGNAL_REGISTRY.json"
    log_path = SKILL_ROOT / "references" / "governance" / "ROUND_EVOLUTION_LOG.md"
    if registry_path.exists():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    else:
        registry = {"skill_name": "Workflow-SiteMap-Creation", "round_history": []}
    round_history = registry.get("round_history", [])
    if not isinstance(round_history, list):
        round_history = []
    history_entry = {
        "run_id": snapshot.get("run_id", ""),
        "factory_digest": snapshot.get("factory_payload", {}).get("source_digest", ""),
        "enhanced_intent": snapshot.get("enhanced_intent", {}).get("final_intent_output", ""),
        "subagent_status": snapshot.get("subagent_run", {}).get("status", ""),
        "artifact_refresh_status": snapshot.get("artifact_refresh", {}).get("status", ""),
        "validation_status": snapshot.get("lint_audit", {}).get("status", ""),
        "recorded_at": now_iso(),
    }
    round_history.append(history_entry)
    registry["round_history"] = round_history[-20:]
    registry["latest_run"] = snapshot
    registry["framework_protocol"] = {
        "execution_chain": [
            "factory",
            "meta_enhance_prompt",
            "background_tmux_subagent",
            "functional_analysis_runtask_analysis_loop",
            "artifact_refresh",
            "validation_closeout",
        ],
        "keyword_first_decision_required": True,
        "mandatory_runtask_stages": snapshot.get("factory_payload", {}).get("factory_split", {}).get("required_runtask_stages", []),
        "managed_frontmatter_keys": [
            "doc_id",
            "doc_type",
            "topic",
            "artifact_role",
            "semantic_layer",
            "producer_skill",
            "writeback_mode",
            "consumer_boundary",
            "anchors",
        ],
    }
    write_json(registry_path, registry)

    log_content = log_path.read_text(encoding="utf-8") if log_path.exists() else "# Round Evolution Log\n"
    log_content = log_content.rstrip() + (
        f"\n\n## {history_entry['recorded_at']} :: {history_entry['run_id'] or 'manual'}\n"
        f"- factory_digest: {history_entry['factory_digest']}\n"
        f"- subagent_status: {history_entry['subagent_status']}\n"
        f"- artifact_refresh_status: {history_entry['artifact_refresh_status']}\n"
        f"- validation_status: {history_entry['validation_status']}\n"
        f"- enhanced_intent_excerpt: {str(history_entry['enhanced_intent'])[:300]}\n"
    )
    write_text(log_path, log_content + "\n")
    return {
        "status": "pass",
        "registry_path": str(registry_path),
        "round_log_path": str(log_path),
        "recorded_run_id": str(history_entry["run_id"]),
    }


def latest_registry_snapshot() -> JsonObject:
    registry_path = SKILL_ROOT / "references" / "governance" / "SELF_EVOLUTION_SIGNAL_REGISTRY.json"
    if not registry_path.exists():
        return {}
    return json.loads(registry_path.read_text(encoding="utf-8"))
