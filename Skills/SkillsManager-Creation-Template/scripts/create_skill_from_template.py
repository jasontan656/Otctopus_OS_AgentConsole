#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from skill_blueprints import (
    GUIDE_ONLY_MODE,
    SKILL_MODE_CHOICES,
    build_generated_skill_files,
    root_entries_for_mode,
)


def _default_target_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is not None:
        local_skills_root = (repo_root.parent / ".codex" / "skills").resolve()
        if local_skills_root.exists():
            return local_skills_root
    env_home = os.environ.get("CODEX_HOME", "").strip()
    if env_home:
        return (Path(env_home).expanduser().resolve() / "skills").resolve()
    return (Path.home() / ".codex" / "skills").resolve()


def write_text(path: Path, text: str, overwrite: bool) -> str:
    if path.exists() and not overwrite:
        return "已跳过"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return "已写入"


def main() -> int:
    parser = argparse.ArgumentParser(description="基于新 root 结构创建或更新技能骨架。")
    parser.add_argument("--skill-name", required=True, help="目标技能目录名称。")
    parser.add_argument("--target-root", default=str(_default_target_root()))
    parser.add_argument("--resources", default="")
    parser.add_argument("--description", default="")
    parser.add_argument("--skill-mode", choices=SKILL_MODE_CHOICES)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    skill_name = args.skill_name.strip()
    if not skill_name:
        raise ValueError("skill-name 不能为空")

    skill_mode = args.skill_mode or GUIDE_ONLY_MODE
    description = args.description.strip() or f"用于 {skill_name} 的实际业务目标（请按真实用途改写该描述）。"
    skill_dir = Path(os.path.expanduser(args.target_root)) / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    files = build_generated_skill_files(skill_name, description, skill_mode)
    results: dict[str, str] = {}
    for relative_path, content in files.items():
        target = skill_dir / relative_path
        results[str(target)] = write_text(target, content, args.overwrite)

    payload = {
        "skill_dir": str(skill_dir),
        "skill_mode": skill_mode,
        "resources_created": root_entries_for_mode(skill_mode)[1:],
        "write_results": results,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
