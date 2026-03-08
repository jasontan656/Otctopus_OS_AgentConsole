#!/usr/bin/env python3
"""@scenario: tooling @purpose: skill_template_generation 从标准化模板包创建或更新 Codex 技能骨架。"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from string import Template
DEFAULT_RESOURCES = ("scripts", "references", "assets")
HEADING_TAG_RE = re.compile(r"^(##\s+[1-7]\.\s+[^\n（(]+?)\s*[（(][^）)\n]+[）)]\s*$", re.MULTILINE)
def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str, overwrite: bool) -> str:
    # observability anchor
    trace_id = "trace_id:write_text"
    run_id = "run_id:create_skill_from_template"
    _ = (trace_id, run_id)
    if path.exists() and not overwrite:
        return "已跳过"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return "已写入"
def parse_resources(raw: str) -> list[str]:
    if not raw.strip():
        return []
    return [x.strip() for x in raw.split(",") if x.strip()]


def title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def normalize_generated_skill_md(text: str) -> str:
    """
    Keep 1-7 headings stable while stripping authoring-only heading tags.
    This prevents generated skeletons from carrying "(必须)/(可选)" semantics.
    """
    return HEADING_TAG_RE.sub(r"\1", text)


def main() -> int:
    trace_id = "trace_id:main"
    run_id = "run_id:create_skill_from_template"
    _ = (trace_id, run_id)
    parser = argparse.ArgumentParser(description="基于模板创建或更新技能骨架。")
    parser.add_argument("--skill-name", required=True, help="目标技能目录名称。")
    parser.add_argument("--target-root", default=str(Path.home() / ".codex" / "skills"))
    parser.add_argument("--resources", default="scripts,references,assets")
    parser.add_argument("--description", default="")
    parser.add_argument("--profile", default="basic", choices=("basic", "staged_cli_first"))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    skill_name = args.skill_name.strip()
    if not skill_name:
        raise ValueError("skill-name 不能为空")

    resources = parse_resources(args.resources)
    target_root = Path(os.path.expanduser(args.target_root))
    skill_dir = target_root / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    script_dir = Path(__file__).resolve().parent
    template_dir = script_dir.parent / "assets" / "skill_template"
    skill_template_name = "SKILL_TEMPLATE_STAGED.md" if args.profile == "staged_cli_first" else "SKILL_TEMPLATE.md"
    skill_template = Template(load_text(template_dir / skill_template_name))
    openai_template = Template(load_text(template_dir / "openai_template.yaml"))
    toolbox_usage_template = Template(load_text(template_dir / "Cli_Toolbox_USAGE_TEMPLATE.md"))
    toolbox_development_template = Template(load_text(template_dir / "Cli_Toolbox_DEVELOPMENT_TEMPLATE.md"))
    toolbox_dev_architecture_template = Template(load_text(template_dir / "Cli_Toolbox_DEV_ARCHITECTURE_TEMPLATE.md"))
    toolbox_dev_catalog_template = Template(load_text(template_dir / "Cli_Toolbox_DEV_MODULE_CATALOG_TEMPLATE.yaml"))
    toolbox_dev_category_template = Template(load_text(template_dir / "Cli_Toolbox_DEV_CATEGORY_INDEX_TEMPLATE.md"))
    toolbox_dev_module_template = Template(load_text(template_dir / "Cli_Toolbox_DEV_MODULE_TEMPLATE.md"))
    toolbox_dev_changelog_template = Template(load_text(template_dir / "Cli_Toolbox_DEV_CHANGELOG_TEMPLATE.md"))
    runtime_contract_json_template = Template(load_text(template_dir / "runtime" / "SKILL_RUNTIME_CONTRACT_TEMPLATE.json"))
    runtime_contract_md_template = Template(load_text(template_dir / "runtime" / "SKILL_RUNTIME_CONTRACT_TEMPLATE.md"))
    stage_system_template = Template(load_text(template_dir / "stages" / "README_STAGE_SYSTEM_TEMPLATE.md"))
    stage_index_template = Template(load_text(template_dir / "stages" / "00_STAGE_INDEX_TEMPLATE.md"))

    description = args.description.strip() or (
        f"用于 {skill_name} 的实际业务目标（请按真实用途改写该描述）。"
    )
    display_name = title_from_slug(skill_name.replace("_", "-"))
    short_description = f"{display_name} 的模板化骨架。"
    if args.profile == "staged_cli_first":
        default_prompt = (
            f"请围绕 {skill_name} 的实际业务目标执行任务；先读取 runtime contract 与阶段合同，"
            "不要把创建技能流程本身当作技能目标。"
        )
    else:
        default_prompt = (
            f"请围绕 {skill_name} 的实际业务目标执行任务；不要把创建技能流程本身当作技能目标。"
        )

    skill_md = normalize_generated_skill_md(
        skill_template.safe_substitute(skill_name=skill_name, description=description)
    )
    openai_yaml = openai_template.safe_substitute(
        display_name=display_name,
        short_description=short_description,
        default_prompt=default_prompt,
    )
    toolbox_usage_md = toolbox_usage_template.safe_substitute(skill_name=skill_name)
    toolbox_development_md = toolbox_development_template.safe_substitute(skill_name=skill_name)
    toolbox_dev_architecture_md = toolbox_dev_architecture_template.safe_substitute(skill_name=skill_name)
    toolbox_dev_catalog_yaml = toolbox_dev_catalog_template.safe_substitute(skill_name=skill_name)
    toolbox_dev_category_md = toolbox_dev_category_template.safe_substitute(skill_name=skill_name)
    toolbox_dev_module_md = toolbox_dev_module_template.safe_substitute(skill_name=skill_name)
    toolbox_dev_changelog_md = toolbox_dev_changelog_template.safe_substitute(skill_name=skill_name)
    runtime_contract_json = runtime_contract_json_template.safe_substitute(skill_name=skill_name)
    runtime_contract_md = runtime_contract_md_template.safe_substitute(skill_name=skill_name)
    stage_system_md = stage_system_template.safe_substitute(skill_name=skill_name)
    stage_index_md = stage_index_template.safe_substitute(skill_name=skill_name)

    results: dict[str, str] = {}
    results[str(skill_dir / "SKILL.md")] = write_text(skill_dir / "SKILL.md", skill_md, args.overwrite)
    results[str(skill_dir / "agents" / "openai.yaml")] = write_text(
        skill_dir / "agents" / "openai.yaml", openai_yaml, args.overwrite
    )
    results[str(skill_dir / "references" / "tooling" / "Cli_Toolbox_USAGE.md")] = write_text(
        skill_dir / "references" / "tooling" / "Cli_Toolbox_USAGE.md", toolbox_usage_md, args.overwrite
    )
    results[str(skill_dir / "references" / "tooling" / "Cli_Toolbox_DEVELOPMENT.md")] = write_text(
        skill_dir / "references" / "tooling" / "Cli_Toolbox_DEVELOPMENT.md", toolbox_development_md, args.overwrite
    )
    results[str(skill_dir / "references" / "tooling" / "development" / "00_ARCHITECTURE_OVERVIEW.md")] = write_text(
        skill_dir / "references" / "tooling" / "development" / "00_ARCHITECTURE_OVERVIEW.md",
        toolbox_dev_architecture_md,
        args.overwrite,
    )
    results[str(skill_dir / "references" / "tooling" / "development" / "10_MODULE_CATALOG.yaml")] = write_text(
        skill_dir / "references" / "tooling" / "development" / "10_MODULE_CATALOG.yaml",
        toolbox_dev_catalog_yaml,
        args.overwrite,
    )
    results[str(skill_dir / "references" / "tooling" / "development" / "20_CATEGORY_INDEX.md")] = write_text(
        skill_dir / "references" / "tooling" / "development" / "20_CATEGORY_INDEX.md",
        toolbox_dev_category_md,
        args.overwrite,
    )
    results[str(skill_dir / "references" / "tooling" / "development" / "modules" / "MODULE_TEMPLATE.md")] = write_text(
        skill_dir / "references" / "tooling" / "development" / "modules" / "MODULE_TEMPLATE.md",
        toolbox_dev_module_md,
        args.overwrite,
    )
    results[str(skill_dir / "references" / "tooling" / "development" / "90_CHANGELOG.md")] = write_text(
        skill_dir / "references" / "tooling" / "development" / "90_CHANGELOG.md",
        toolbox_dev_changelog_md,
        args.overwrite,
    )
    if args.profile == "staged_cli_first":
        results[str(skill_dir / "references" / "runtime" / "SKILL_RUNTIME_CONTRACT.json")] = write_text(
            skill_dir / "references" / "runtime" / "SKILL_RUNTIME_CONTRACT.json",
            runtime_contract_json,
            args.overwrite,
        )
        results[str(skill_dir / "references" / "runtime" / "SKILL_RUNTIME_CONTRACT.md")] = write_text(
            skill_dir / "references" / "runtime" / "SKILL_RUNTIME_CONTRACT.md",
            runtime_contract_md,
            args.overwrite,
        )
        results[str(skill_dir / "references" / "stages" / "00_STAGE_INDEX.md")] = write_text(
            skill_dir / "references" / "stages" / "00_STAGE_INDEX.md",
            stage_index_md,
            args.overwrite,
        )
        results[str(skill_dir / "assets" / "templates" / "stages" / "README_STAGE_SYSTEM.md")] = write_text(
            skill_dir / "assets" / "templates" / "stages" / "README_STAGE_SYSTEM.md",
            stage_system_md,
            args.overwrite,
        )
        for relative_path in (
            "assets/templates/stages/00_STAGE_INDEX_TEMPLATE.md",
            "assets/templates/stages/STAGE_TEMPLATE/INSTRUCTION.md",
            "assets/templates/stages/STAGE_TEMPLATE/WORKFLOW.md",
            "assets/templates/stages/STAGE_TEMPLATE/RULES.md",
            "assets/templates/stages/STAGE_TEMPLATE/DOC_CONTRACT.json",
            "assets/templates/stages/STAGE_TEMPLATE/COMMAND_CONTRACT.json",
            "assets/templates/stages/STAGE_TEMPLATE/GRAPH_CONTRACT.json",
        ):
            source = template_dir / relative_path.replace("assets/templates/", "")
            results[str(skill_dir / relative_path)] = write_text(
                skill_dir / relative_path,
                load_text(source),
                args.overwrite,
            )

    selected = resources if resources else list(DEFAULT_RESOURCES)
    for resource in selected:
        (skill_dir / resource).mkdir(parents=True, exist_ok=True)
    # Cli_Toolbox docs are mandatory by contract.
    (skill_dir / "references" / "tooling").mkdir(parents=True, exist_ok=True)
    (skill_dir / "references" / "tooling" / "development" / "modules").mkdir(parents=True, exist_ok=True)

    payload = {
        "skill_dir": str(skill_dir),
        "profile": args.profile,
        "resources_created": sorted(selected),
        "write_results": results,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
