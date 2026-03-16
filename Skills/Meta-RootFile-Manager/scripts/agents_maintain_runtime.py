from __future__ import annotations

import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from rootfile_runtime import (
    _duplicate_phrase,
    _extract_header_prefix,
    _iter_part_a_strings,
    _iter_payload_strings,
    _parent_agents_source_path,
    _relative_source_key,
    build_entry,
    extract_contract_body_from_part_a,
    extract_external_agents_part_a_body,
    extract_external_surface_from_internal,
    extract_reminder_body_from_part_a,
    find_channel_for_source_path,
    graft_frontmatter_from_template,
    iter_governed_sources,
    lint_managed_entry,
    load_machine_payload,
    render_external_agents,
    render_internal_agents_human,
    render_part_a_body,
    sync_managed_targets_tree_to_installed,
    upsert_frontmatter_owner,
    write_text,
)


MUTATION_KEYWORDS = {
    "add": ("新增", "添加", "加入", "增加", "append", "add"),
    "remove": ("移除", "删除", "删掉", "去掉", "remove", "delete"),
    "replace": ("替换", "改成", "改为", "改写", "重写", "replace", "rewrite"),
}

PART_A_SECTION_ALIASES: dict[str, tuple[str, ...]] = {
    "1. 合同定位": ("1. 合同定位", "合同定位", "hook contract identity", "contract identity"),
    "2. 一级读取入口": ("2. 一级读取入口", "一级读取入口", "primary contract read", "primary read"),
    "3. 二级分域读取": ("3. 二级分域读取", "二级分域读取", "secondary domain reads", "domain reads"),
    "4. 执行约束": ("4. 执行约束", "执行约束", "enforcement", "execution gate"),
    "1. 环境提醒": ("1. 环境提醒", "环境提醒", "environment reminder"),
    "2. 协作提醒": ("2. 协作提醒", "协作提醒", "coordination reminder", "repo reminder"),
    "1. 根入口命令": ("1. 根入口命令", "根入口命令", "root entry", "entry command"),
    "2. 技能类任务附加入口": ("2. 技能类任务附加入口", "技能类任务附加入口", "skill task entry"),
    "3. 语言规范": ("3. 语言规范", "语言规范", "language policy"),
    "4. 当前受管 repo 边界": ("4. 当前受管 repo 边界", "当前受管 repo 边界", "repo 边界", "repo boundary"),
    "5. Multi-AGENT 工作模式": ("5. Multi-AGENT 工作模式", "multi-agent 工作模式", "multi-agent", "并行改动"),
    "6. 治理链约束": ("6. 治理链约束", "治理链约束", "governance chain"),
}

PAYLOAD_FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "turn_start.contract.required_actions": ("turn_start", "turn start actions", "启动动作", "回合开始动作"),
    "runtime_constraints.contract.rules": ("runtime_constraints", "运行时约束", "runtime constraints"),
    "repo_handoff.contract.rules": ("repo_handoff", "repo handoff", "repo 本地 contract 交接"),
    "turn_end.contract.required_actions": ("turn_end", "turn end actions", "回合结束动作"),
    "execution_modes.contract.READ_EXEC.goal": ("read_exec goal", "READ_EXEC goal", "READ_EXEC 目标"),
    "execution_modes.contract.READ_EXEC.default_actions": (
        "read_exec default_actions",
        "READ_EXEC default_actions",
        "READ_EXEC 默认动作",
    ),
    "execution_modes.contract.WRITE_EXEC.goal": ("write_exec goal", "WRITE_EXEC goal", "WRITE_EXEC 目标"),
    "execution_modes.contract.WRITE_EXEC.default_actions": (
        "write_exec default_actions",
        "WRITE_EXEC default_actions",
        "WRITE_EXEC 默认动作",
    ),
}

QUOTED_TEXT_PATTERN = re.compile(r"`([^`]+)`|“([^”]+)”|\"([^\"]+)\"|'([^']+)'")


def build_agents_maintain_command(paths: object, source_path: Path) -> str:
    from rootfile_runtime import build_agents_maintain_command as build_root_agents_maintain_command

    try:
        # Reuse source-specific template when it exists.
        from rootfile_runtime import load_source_specific_agents_rules, _relative_source_key, _repo_root_for_runtime_paths
    except ImportError:
        return build_root_agents_maintain_command(paths, source_path)

    source_rule = load_source_specific_agents_rules(paths).get(_relative_source_key(paths, source_path))
    if isinstance(source_rule, dict):
        command_template = source_rule.get("entry_command_template")
        if isinstance(command_template, str):
            return command_template

    repo_root = _repo_root_for_runtime_paths(paths)
    python_path = repo_root / ".venv_backend_skills" / "bin" / "python3"
    script_path = Path(paths.mirror_skill_root) / "scripts" / "Cli_Toolbox.py"
    return f'{python_path} {script_path} agents-maintain --intent "<natural language request>" --json'


def maintain_agents(paths: object, intent: str, *, dry_run: bool = False) -> dict[str, Any]:
    normalized_intent = " ".join(intent.split())
    mutation_mode = _detect_mutation_mode(normalized_intent)
    candidates = _rank_candidates(paths, normalized_intent)
    target_decision = _select_target(normalized_intent, candidates)
    semantic = _classify_semantics(normalized_intent)

    response: dict[str, Any] = {
        "stage": "agents_maintain",
        "intent": intent,
        "normalized_intent": normalized_intent,
        "governed_target_candidates": [item["report"] for item in candidates],
        "selected_target": target_decision.get("selected_target"),
        "semantic_family": semantic["semantic_family"],
        "selected_part": semantic["selected_part"],
        "payload_atoms": semantic["payload_atoms"],
        "part_a_atoms": semantic["part_a_atoms"],
        "inheritance_hits": [],
        "duplicate_gate": {"status": "block", "reason": "uninitialized"},
        "mutation_mode": mutation_mode,
        "push_plan": None,
        "write_status": "blocked",
        "operations": [],
        "lint_failures": [],
        "summary": "",
        "details": [],
        "collect_used": False,
    }

    if semantic["semantic_family"] == "new_target_request":
        return _blocked(response, "reject", "user_must_decide_new_target")
    if target_decision["status"] != "ok":
        return _blocked(response, "block", target_decision["reason"])
    if mutation_mode == "no_write":
        return _blocked(response, "block", "unsupported_mutation_mode")
    if semantic["semantic_family"] in {"ambiguous", "mixed_semantics"}:
        return _blocked(response, "block", semantic["reason"])

    entry = target_decision["entry"]
    source_path = Path(entry["source_path"])
    managed_human = Path(entry["managed_files"]["human"])
    human_text = managed_human.read_text(encoding="utf-8")
    payload = load_machine_payload(managed_human)
    if not isinstance(payload, dict):
        return _blocked(response, "block", "managed_payload_not_object")

    quoted_texts = _extract_quoted_texts(normalized_intent)
    mutation = _build_mutation_request(mutation_mode, semantic, quoted_texts)
    if mutation["status"] != "ok":
        return _blocked(response, "block", mutation["reason"])

    response["push_plan"] = {
        "internal_truth_source": str(managed_human),
        "external_render_target": str(source_path),
        "lint_required": True,
    }

    gate = _evaluate_duplicate_gate(paths, source_path, entry, human_text, payload, semantic, mutation)
    response["inheritance_hits"] = gate["inheritance_hits"]
    response["duplicate_gate"] = gate["duplicate_gate"]
    if gate["duplicate_gate"]["status"] != "pass":
        response["semantic_family"] = gate.get("semantic_family", response["semantic_family"])
        response["write_status"] = "blocked"
        response["summary"] = f"agents-maintain blocked for {entry['relative_path']}"
        response["details"] = [gate["duplicate_gate"]["reason"]]
        return response

    updated_part_a_body = extract_external_agents_part_a_body(human_text)
    updated_payload = payload
    if semantic["selected_part"] == "part_a":
        updated_part_a_body = _apply_part_a_mutation(updated_part_a_body, semantic["section_heading"], mutation)
    else:
        try:
            updated_payload = _apply_payload_mutation(payload, semantic["payload_field"], mutation)
        except ValueError as exc:
            return _blocked(response, "block", str(exc))

    prefix = _extract_header_prefix(human_text)
    rendered_external = render_external_agents(updated_part_a_body, prefix)
    rendered_human = render_internal_agents_human(
        upsert_frontmatter_owner(
            graft_frontmatter_from_template(rendered_external, human_text),
            str(entry["owner"]),
        ),
        updated_payload,
    )
    rendered_part_a = extract_external_surface_from_internal(rendered_human)

    original_external = source_path.read_text(encoding="utf-8") if source_path.exists() else ""
    original_human = human_text
    managed_changed = write_text(managed_human, rendered_human, dry_run)
    external_changed = write_text(source_path, rendered_part_a, dry_run)
    lint_failures: list[str] = []
    if not dry_run:
        lint_failures = lint_managed_entry(paths, entry)
        if lint_failures:
            write_text(managed_human, original_human, False)
            write_text(source_path, original_external, False)
            return _blocked(response, "block", f"lint_failed:{', '.join(lint_failures)}", lint_failures)
        installed_sync = sync_managed_targets_tree_to_installed(paths, False)
        installed_synced = bool(installed_sync["copied_files"] or installed_sync["removed_extra_files"])
    else:
        installed_sync = {"copied_files": [], "removed_extra_files": []}
        installed_synced = False

    response["write_status"] = "applied" if not dry_run else "dry_run"
    response["operations"] = [
        {
            "managed_human_changed": bool(managed_changed),
            "external_pushed": bool(external_changed),
            "installed_synced": bool(installed_synced),
            "installed_sync_copied_files": installed_sync["copied_files"],
            "installed_sync_removed_extra_files": installed_sync["removed_extra_files"],
        }
    ]
    response["summary"] = f"agents-maintain {response['write_status']} for {entry['relative_path']}"
    response["details"] = [
        f"selected target: {entry['relative_path']}",
        f"selected part: {semantic['selected_part']}",
        f"mutation: {mutation_mode}",
    ]
    return response


def _blocked(
    payload: dict[str, Any],
    gate_status: str,
    reason: str,
    lint_failures: list[str] | None = None,
) -> dict[str, Any]:
    payload["duplicate_gate"] = {"status": gate_status, "reason": reason}
    payload["lint_failures"] = lint_failures or []
    payload["summary"] = "agents-maintain blocked"
    payload["details"] = [reason]
    payload["write_status"] = "blocked"
    return payload


def _detect_mutation_mode(intent: str) -> str:
    lowered = intent.lower()
    for mode, keywords in MUTATION_KEYWORDS.items():
        if any(keyword in intent or keyword in lowered for keyword in keywords):
            return mode
    return "no_write"


def _rank_candidates(paths: object, intent: str) -> list[dict[str, Any]]:
    ranked: list[dict[str, Any]] = []
    for source_path, channel_id, channel in iter_governed_sources(paths):
        if channel_id != "AGENTS_MD":
            continue
        entry = build_entry(paths, source_path, channel_id, channel)
        relative = entry["relative_path"]
        score = 0
        reasons: list[str] = []
        if str(source_path) in intent or relative in intent:
            score += 100
            reasons.append("exact_path_match")
        parent_tokens = [part for part in Path(relative).parts if part != "AGENTS.md"]
        for token in parent_tokens:
            if token and token.lower() in intent.lower():
                score += 20
                reasons.append(f"path_token:{token}")
        if relative == "AGENTS.md" and any(token in intent.lower() for token in ("workspace", "workspace root", "工作区根", "ai_projects")):
            score += 40
            reasons.append("workspace_root_signal")
        if len(Path(relative).parts) == 2 and any(token in intent.lower() for token in ("repo root", "仓库根", "repository root")):
            score += 10
            reasons.append("repo_root_signal")
        hierarchy_role = _hierarchy_role(relative)
        ranked.append(
            {
                "entry": entry,
                "score": score,
                "report": {
                    "source_path": entry["source_path"],
                    "relative_path": relative,
                    "rank_score": score,
                    "hierarchy_role": hierarchy_role,
                    "reason": ", ".join(reasons) if reasons else "no_explicit_signal",
                },
            }
        )
    ranked.sort(key=lambda item: (-item["score"], item["entry"]["relative_path"]))
    for index, item in enumerate(ranked, start=1):
        item["report"]["rank"] = index
    return ranked


def _select_target(intent: str, candidates: list[dict[str, Any]]) -> dict[str, Any]:
    if not candidates:
        return {"status": "error", "reason": "no_governed_agents_targets"}
    top = candidates[0]
    if top["score"] == 0 and len(candidates) > 1:
        return {"status": "error", "reason": "ambiguous_target_no_scope_signal"}
    if len(candidates) > 1 and candidates[1]["score"] == top["score"] and top["score"] > 0:
        return {"status": "error", "reason": "ambiguous_target_tied_ranking"}
    entry = top["entry"]
    return {
        "status": "ok",
        "reason": "selected",
        "entry": entry,
        "selected_target": {
            "source_path": entry["source_path"],
            "relative_path": entry["relative_path"],
            "hierarchy_role": _hierarchy_role(entry["relative_path"]),
        },
    }


def _classify_semantics(intent: str) -> dict[str, Any]:
    lowered = intent.lower()
    if any(token in intent or token in lowered for token in ("新建 agents", "新增受管", "new target", "new agents.md")):
        return {
            "semantic_family": "new_target_request",
            "selected_part": "none",
            "payload_atoms": [],
            "part_a_atoms": [],
            "reason": "new_target_request_blocked",
        }
    matched_sections = [
        heading
        for heading, aliases in PART_A_SECTION_ALIASES.items()
        if any(alias.lower() in lowered or alias in intent for alias in aliases)
    ]
    matched_payloads = [
        field
        for field, aliases in PAYLOAD_FIELD_ALIASES.items()
        if any(alias.lower() in lowered or alias in intent for alias in aliases)
    ]
    if matched_sections and matched_payloads:
        return {
            "semantic_family": "mixed_semantics",
            "selected_part": "none",
            "payload_atoms": matched_payloads,
            "part_a_atoms": matched_sections,
            "reason": "mixed_part_a_and_payload_signals",
        }
    if len(matched_sections) == 1:
        return {
            "semantic_family": "narrative_guidance",
            "selected_part": "part_a",
            "payload_atoms": [],
            "part_a_atoms": matched_sections,
            "section_heading": matched_sections[0],
            "reason": "classified_as_part_a",
        }
    if len(matched_payloads) == 1:
        return {
            "semantic_family": "runtime_action",
            "selected_part": "payload",
            "payload_atoms": matched_payloads,
            "part_a_atoms": [],
            "payload_field": matched_payloads[0],
            "reason": "classified_as_payload",
        }
    return {
        "semantic_family": "ambiguous",
        "selected_part": "none",
        "payload_atoms": matched_payloads,
        "part_a_atoms": matched_sections,
        "reason": "unable_to_classify_target_part",
    }


def _extract_quoted_texts(intent: str) -> list[str]:
    extracted: list[str] = []
    for match in QUOTED_TEXT_PATTERN.finditer(intent):
        value = next((group for group in match.groups() if group), None)
        if value:
            extracted.append(value)
    return extracted


def _build_mutation_request(mode: str, semantic: dict[str, Any], quoted_texts: list[str]) -> dict[str, Any]:
    if mode in {"add", "remove"}:
        if not quoted_texts:
            return {"status": "error", "reason": "missing_rule_text"}
        return {"status": "ok", "operation": mode, "text": quoted_texts[-1]}
    if mode == "replace":
        if len(quoted_texts) < 2:
            return {"status": "error", "reason": "replace_requires_old_and_new_text"}
        return {
            "status": "ok",
            "operation": mode,
            "old_text": quoted_texts[-2],
            "new_text": quoted_texts[-1],
        }
    return {"status": "error", "reason": "unsupported_mutation_mode"}


def _evaluate_duplicate_gate(
    paths: object,
    source_path: Path,
    entry: dict[str, Any],
    human_text: str,
    payload: dict[str, Any],
    semantic: dict[str, Any],
    mutation: dict[str, Any],
) -> dict[str, Any]:
    if semantic["selected_part"] == "part_a":
        current_values = _section_items(extract_external_agents_part_a_body(human_text)).get(semantic["section_heading"], [])
        check_text = mutation.get("new_text") or mutation.get("text")
    else:
        current_values = _payload_values_for_field(payload, semantic["payload_field"])
        check_text = mutation.get("new_text") or mutation.get("text")

    if mutation["status"] != "ok":
        return {"duplicate_gate": {"status": "block", "reason": mutation["reason"]}, "inheritance_hits": []}
    operation = mutation.get("operation")
    if operation == "add" and mutation.get("text") in current_values:
        return {"duplicate_gate": {"status": "block", "reason": "target_already_contains_text"}, "inheritance_hits": []}
    if operation == "remove" and mutation.get("text") not in current_values:
        return {"duplicate_gate": {"status": "block", "reason": "target_text_not_found"}, "inheritance_hits": []}
    if operation == "replace" and mutation.get("old_text") not in current_values:
        return {"duplicate_gate": {"status": "block", "reason": "target_text_not_found"}, "inheritance_hits": []}

    inheritance_hits = _find_inheritance_hits(paths, source_path, str(check_text or ""))
    if operation in {"add", "replace"} and inheritance_hits and semantic["selected_part"] in {"part_a", "payload"}:
        return {
            "semantic_family": "ancestor_inherited",
            "duplicate_gate": {"status": "inherit_only", "reason": "ancestor_already_covers_requested_semantic"},
            "inheritance_hits": inheritance_hits,
        }
    return {"duplicate_gate": {"status": "pass", "reason": "no_duplicate_or_inheritance_hit"}, "inheritance_hits": []}


def _section_items(part_a_body: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current_heading: str | None = None
    for raw_line in part_a_body.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue
        if re.match(r"^\d+\.\s+", stripped):
            current_heading = stripped
            sections.setdefault(current_heading, [])
            continue
        if current_heading is None:
            continue
        item = re.sub(r"^\s*-\s*", "", stripped)
        sections[current_heading].append(item)
    return sections


def _split_part_a_sections(part_a_body: str) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    return (
        _section_items(extract_contract_body_from_part_a(part_a_body)),
        _section_items(extract_reminder_body_from_part_a(part_a_body)),
    )


def _section_location(part_a_body: str, heading: str) -> str:
    contract_sections, reminder_sections = _split_part_a_sections(part_a_body)
    if heading in contract_sections:
        return "contract"
    if heading in reminder_sections:
        return "reminder"
    if "提醒" in heading:
        return "reminder"
    return "contract"


def _render_part_a_sections(sections: dict[str, list[str]], original_body: str) -> str:
    ordered_headings = [line.strip() for line in original_body.splitlines() if re.match(r"^\d+\.\s+", line.strip())]
    rendered: list[str] = []
    for index, heading in enumerate(ordered_headings):
        if index:
            rendered.append("")
        rendered.append(heading)
        for item in sections.get(heading, []):
            rendered.append(f"- {item}")
    return "\n".join(rendered).strip()


def _apply_part_a_mutation(part_a_body: str, heading: str, mutation: dict[str, Any]) -> str:
    contract_body = extract_contract_body_from_part_a(part_a_body)
    reminder_body = extract_reminder_body_from_part_a(part_a_body)
    contract_sections = _section_items(contract_body)
    reminder_sections = _section_items(reminder_body)
    location = _section_location(part_a_body, heading)
    if location == "reminder":
        sections = reminder_sections
        original_body = reminder_body
    else:
        sections = contract_sections
        original_body = contract_body
    items = sections.setdefault(heading, [])
    operation = mutation["operation"]
    if operation == "replace":
        for index, item in enumerate(items):
            if item == mutation["old_text"]:
                items[index] = mutation["new_text"]
                break
    elif operation == "remove":
        sections[heading] = [item for item in items if item != mutation["text"]]
    elif operation == "add":
        items.append(mutation["text"])
    if location == "reminder":
        rendered_reminder = _render_part_a_sections(sections, original_body)
        rendered_contract = _render_part_a_sections(contract_sections, contract_body)
    else:
        rendered_contract = _render_part_a_sections(sections, original_body)
        rendered_reminder = _render_part_a_sections(reminder_sections, reminder_body)
    return render_part_a_body(rendered_contract, rendered_reminder)


def _payload_values_for_field(payload: dict[str, Any], field_path: str) -> list[str]:
    value = _payload_field_get(payload, field_path)
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    if isinstance(value, str):
        return [value]
    return []


def _payload_field_get(payload: dict[str, Any], field_path: str) -> Any:
    current: Any = payload
    for part in field_path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def _payload_field_set(payload: dict[str, Any], field_path: str, value: Any) -> dict[str, Any]:
    current = payload
    parts = field_path.split(".")
    for part in parts[:-1]:
        next_value = current.get(part)
        if not isinstance(next_value, dict):
            next_value = {}
            current[part] = next_value
        current = next_value
    current[parts[-1]] = value
    return payload


def _apply_payload_mutation(payload: dict[str, Any], field_path: str, mutation: dict[str, Any]) -> dict[str, Any]:
    cloned = deepcopy(payload)
    current_value = _payload_field_get(cloned, field_path)
    if isinstance(current_value, list):
        new_value = [item for item in current_value]
        if mutation["operation"] == "replace":
            new_value = [mutation["new_text"] if item == mutation["old_text"] else item for item in new_value]
        elif mutation["operation"] == "remove":
            new_value = [item for item in new_value if item != mutation["text"]]
        else:
            new_value.append(mutation["text"])
        return _payload_field_set(cloned, field_path, new_value)
    if isinstance(current_value, str) and mutation["operation"] == "replace":
        return _payload_field_set(cloned, field_path, mutation["new_text"])
    if current_value is None and mutation["operation"] == "add":
        return _payload_field_set(cloned, field_path, [mutation["text"]])
    raise ValueError(f"unsupported_payload_field_type:{field_path}")


def _find_inheritance_hits(paths: object, source_path: Path, requested_text: str) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    current_parent = _parent_agents_source_path(paths, source_path)
    while current_parent is not None:
        found = find_channel_for_source_path(paths, current_parent)
        if found is None:
            break
        parent_entry = build_entry(paths, current_parent, found[0], found[1])
        parent_human = Path(parent_entry["managed_files"]["human"])
        parent_payload = load_machine_payload(parent_human)
        parent_strings = list(_iter_part_a_strings(current_parent.read_text(encoding="utf-8")))
        if isinstance(parent_payload, dict):
            parent_strings.extend(_iter_payload_strings(parent_payload, "$"))
        for parent_path, parent_text in parent_strings:
            phrase = _duplicate_phrase(requested_text, parent_text)
            if phrase is None:
                continue
            hits.append(
                {
                    "source_path": str(current_parent),
                    "relative_path": _relative_source_key(paths, current_parent),
                    "surface_path": parent_path,
                    "matched_phrase": phrase,
                }
            )
            break
        current_parent = _parent_agents_source_path(paths, current_parent)
    return hits


def _hierarchy_role(relative_path: str) -> str:
    relative = Path(relative_path)
    if relative_path == "AGENTS.md":
        return "workspace_root"
    if len(relative.parts) == 2:
        return "repo_root"
    return "child_scope"
