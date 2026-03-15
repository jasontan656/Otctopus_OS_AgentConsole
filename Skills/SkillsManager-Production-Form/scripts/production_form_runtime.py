from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


WORKING_CONTRACT_PAYLOAD: dict[str, Any] = {
    "skill_name": "SkillsManager-Production-Form",
    "display_name": "SkillsManager-Production-Form",
    "contract_version": "0.3.4",
    "status": "active_console_product_form",
    "mission": "Continuously maintain the console directory as a product-shaped surface, preserve local design history for skills-as-console productization decisions, and keep the project narrative aligned around an AI-native customizable personal assistant methodology.",
    "current_product_target": {
        "brand_name": "Octopus OS",
        "engineering_repo": "Otctopus_OS_AgentConsole",
        "console_root": "Skills/",
        "product_positioning": "console directory maintained as the product surface for the governed skill stack",
        "current_phase": "continuous console productization around the Skills directory",
        "product_role": "advanced personal assistant customization approach built through governed skills, workflows, and tool contracts",
        "runtime_strategy": "maximize GPT-5.4 with high reasoning effort plus Codex CLI native capability while minimizing token overhead through skill-first behavior shaping",
    },
    "hard_boundaries": [
        "the editable source of truth stays inside Otctopus_OS_AgentConsole/Skills rather than ~/.codex/skills",
        "the Skills directory should be maintained as a coherent console product surface instead of a loose scratch area",
        "when console productization touches rootfile-managed files, their body changes must go through Meta-RootFile-Manager rather than direct external edits",
        "the project should express behavior through atomic skills, workflows, governance contracts, and tool entrypoints rather than ad-hoc prompt patches",
        "public product README and docs stay English-only",
        "end-user wizard and TUI surfaces stay bilingual English/Chinese",
        "internal skill core and governance docs may stay Chinese-first",
        "product-facing docs and product tools must not be pushed into the codex installation directory",
        "console productization decisions should prefer governed skill roots, registry, and runtime contracts over ad-hoc notes",
        "skill roots still evolve here first and then flow to ~/.codex/skills through the governed sync path",
        "the codex installation directory is a deployment surface, not the authoring surface for console productization",
        "disabled skills are incomplete and should not be recommended for normal use",
        "the current product narrative is for learning, local reuse, and testing rather than commercial use",
        "external suggestions are acceptable, but external code collaboration is currently out of scope",
        "the project maintenance narrative should state that implementation and maintenance are AI-driven rather than based on human code contribution",
    ],
    "product_narrative": {
        "assistant_goal": "strengthen the model into a more capable personal assistant by continuously adding norms, skills, skill-management methods, workflows, and governed tooling",
        "design_method": "atomize skills so model behavior can be attached to explicit norms, workflows, and tool contracts",
        "behavior_governance_goal": "progressively move more agent behavior into governed skills, workflows, and tool contracts instead of leaving large behavior surfaces implicit",
        "multi_agent_direction": "use skills to support daily development and broader work through multi-agent workflows, then continue toward richer multi-agent team collaboration",
        "repo_release_model": {
            "release_repo": "slower-moving public release surface",
            "dev_repo": "fast-moving public development surface with frequent and larger changes",
        },
        "usage_policy": {
            "allowed": ["learning", "local reuse", "testing"],
            "disallowed": ["commercial use"],
        },
    },
    "local_history_contract": {
        "primary_log_path": "/home/jasontan656/AI_Projects/Codex_Skill_Runtime/SkillsManager-Production-Form/ITERATION_LOG.md",
        "legacy_seed_log_path": "path/latest_log/25_LOG_SEED.md",
        "intent_snapshot_path": "path/current_intent/20_INTENT_SNAPSHOT.md",
        "log_update_rule": "append a log entry whenever a new console productization decision, directory boundary change, or skill-management convergence is made",
        "migration_rule": "if the governed runtime log does not exist yet, seed it from path/latest_log/25_LOG_SEED.md and continue writing only to the runtime root afterward",
        "future_switch_rule": "once the console product form is stable enough, the main release-facing narrative may move back to GitHub while this local log becomes a narrower continuity aid",
    },
    "runtime_observability": {
        "skill_runtime_root": "/home/jasontan656/AI_Projects/Codex_Skill_Runtime/SkillsManager-Production-Form",
        "result_root": "/home/jasontan656/AI_Projects/Codex_Skills_Result/SkillsManager-Production-Form",
        "default_runtime_log_path": "/home/jasontan656/AI_Projects/Codex_Skill_Runtime/SkillsManager-Production-Form/ITERATION_LOG.md",
        "legacy_seed_log_path": "path/latest_log/25_LOG_SEED.md",
        "runtime_log_policy": "active console-productization logs must append only under the governed runtime root; the repo copy is a read-only migration seed",
        "result_policy": "this skill currently emits machine-readable stdout and runtime log writes only; future file artifacts must accept an explicit target path or default under the governed result root",
    },
    "governed_write_dependencies": {
        "rootfile_manager_skill": "Meta-RootFile-Manager",
        "rootfile_rule": "if a console productization task touches a rootfile-managed external file, route the body maintenance through Meta-RootFile-Manager and do not directly edit the governed external file from this skill",
    },
    "tooling": {
        "working_contract_command": "python3 ./scripts/Cli_Toolbox.py working-contract --json",
        "intent_snapshot_command": "python3 ./scripts/Cli_Toolbox.py intent-snapshot --json",
        "latest_log_command": "python3 ./scripts/Cli_Toolbox.py latest-log --json",
        "append_log_command": "python3 ./scripts/Cli_Toolbox.py append-iteration-log --title \"<title>\" --summary \"<summary>\" --decision \"<decision>\" --affected-path \"<path>\" --next-step \"<next>\"",
        "rootfile_target_contract_example": "python3 ../Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path \"<rootfile-path>\" --json",
    },
}


def runtime_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "skill_name": "SkillsManager-Production-Form",
        "skill_mode": "guide_with_tool",
        "runtime_entry": "./scripts/Cli_Toolbox.py",
        "root_shape": ["SKILL.md", "path", "agents", "scripts"],
        "governed_scope": [
            "console product form working contract",
            "current product intent",
            "runtime continuity log",
            "iteration log append workflow",
            "rootfile routing boundary",
        ],
        "commands": [
            "runtime-contract",
            "contract",
            "read-contract-context",
            "read-path-context",
            "working-contract",
            "intent-snapshot",
            "latest-log",
            "append-iteration-log",
        ],
        "notes": [
            "documents remain the source of truth",
            "SKILL.md exposes function entries directly in section 2",
            "downstream path documents continue with frontmatter reading_chain",
        ],
    }


def working_contract_payload() -> dict[str, Any]:
    return WORKING_CONTRACT_PAYLOAD


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_frontmatter(markdown_path: Path) -> tuple[dict[str, Any], str]:
    text = _read_text(markdown_path)
    if not text.startswith("---\n"):
        return {}, text
    closing = text.find("\n---\n", 4)
    if closing == -1:
        return {}, text
    payload = yaml.safe_load(text[4:closing]) or {}
    body = text[closing + 5 :]
    return payload if isinstance(payload, dict) else {}, body


def _facade_entries(markdown_path: Path) -> list[dict[str, str]]:
    _frontmatter, body = _parse_frontmatter(markdown_path)
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_entries = False
    for raw_line in body.splitlines():
        stripped = raw_line.strip()
        if stripped == "## 2. 功能入口":
            in_entries = True
            continue
        if in_entries and stripped.startswith("## "):
            break
        if not in_entries:
            continue
        match = re.match(r"^- \[(?P<label>[^\]]+)\][：:]\s*`(?P<target>[^`]+)`", stripped)
        if match:
            current = {
                "key": match.group("label").strip(),
                "target": match.group("target").strip(),
                "hop": "entry",
            }
            items.append(current)
            continue
        if current is None:
            continue
        command_match = re.search(r"--entry\s+([A-Za-z0-9_.-]+)", stripped)
        if command_match:
            current["key"] = command_match.group(1).strip()
    return items


def _reading_chain(markdown_path: Path) -> list[dict[str, str]]:
    if markdown_path.name == "SKILL.md":
        return _facade_entries(markdown_path)
    frontmatter, _ = _parse_frontmatter(markdown_path)
    raw_chain = frontmatter.get("reading_chain")
    if not isinstance(raw_chain, list):
        return []
    chain: list[dict[str, str]] = []
    for item in raw_chain:
        if not isinstance(item, dict):
            continue
        key = item.get("key")
        target = item.get("target")
        hop = item.get("hop")
        if isinstance(key, str) and isinstance(target, str) and isinstance(hop, str):
            chain.append({"key": key, "target": target, "hop": hop})
    return chain


def _extract_title(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def _select_edge(edges: list[dict[str, str]], key: str | None) -> tuple[dict[str, str] | None, list[str]]:
    if not edges:
        return None, []
    if key is None:
        return (edges[0], []) if len(edges) == 1 else (None, [edge["key"] for edge in edges])
    for edge in edges:
        if edge["key"] == key:
            return edge, []
    return None, [edge["key"] for edge in edges]


def compile_reading_chain(target_root: Path, entry_key: str, selection_keys: list[str]) -> dict[str, Any]:
    skill_md = target_root / "SKILL.md"
    if not skill_md.is_file():
        return {"status": "error", "error": "missing_skill_md", "target_root": str(target_root)}

    skill_edges = _reading_chain(skill_md)
    first_edge, available = _select_edge(skill_edges, entry_key)
    if first_edge is None:
        return {
            "status": "error",
            "error": "entry_not_found",
            "entry": entry_key,
            "available_entries": available,
            "target_root": str(target_root),
        }

    selection_queue = list(selection_keys)
    current = (skill_md.parent / first_edge["target"]).resolve()
    resolved_chain = ["SKILL.md"]
    segments: list[dict[str, str]] = []

    _skill_frontmatter, skill_body = _parse_frontmatter(skill_md)
    segments.append({"source": "SKILL.md", "title": _extract_title(skill_body), "content": skill_body.strip()})

    while True:
        _frontmatter, body = _parse_frontmatter(current)
        relative = current.relative_to(target_root).as_posix()
        resolved_chain.append(relative)
        segments.append({"source": relative, "title": _extract_title(body), "content": body.strip()})
        edges = _reading_chain(current)
        if not edges:
            break
        if len(edges) > 1:
            requested = selection_queue.pop(0) if selection_queue else None
            next_edge, available = _select_edge(edges, requested)
            if next_edge is None:
                return {
                    "status": "branch_selection_required",
                    "target_root": str(target_root),
                    "entry": entry_key,
                    "resolved_chain": resolved_chain,
                    "available_next": available,
                    "current_source": relative,
                    "segments": segments,
                }
            current = (current.parent / next_edge["target"]).resolve()
            continue
        current = (current.parent / edges[0]["target"]).resolve()

    return {
        "status": "ok",
        "target_root": str(target_root),
        "entry": entry_key,
        "resolved_chain": resolved_chain,
        "segments": segments,
        "compiled_markdown": "\n\n".join(segment["content"] for segment in segments if segment["content"]),
    }
