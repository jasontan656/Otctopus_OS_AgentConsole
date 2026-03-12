from __future__ import annotations

import shutil
from pathlib import Path

from construction_plan_contract import GUIDANCE_MARKERS, PACK_DIR_PATTERN
from construction_plan_contract import PACK_MACHINE_FILES, PACK_MARKDOWN_FILES, ROOT_REQUIRED_FILES
from construction_plan_rendering import default_steps, design_steps_from_plan
from construction_plan_rendering import render_pack_registry, render_root_index, slugify, write_pack
from construction_plan_schema import machine_schema_violations


def construction_plan_init_payload(target: Path, design_plan_path: Path, force: bool) -> tuple[dict, int]:
    if target.exists() and any(target.iterdir()) and not force:
        return {"status": "fail", "target": str(target), "reason": "target_not_empty", "hint": "rerun with --force to overwrite the execution_atom_plan_validation_packs skeleton"}, 1
    if target.exists() and force:
        shutil.rmtree(target)
    steps = design_steps_from_plan(design_plan_path) or default_steps()
    target.mkdir(parents=True, exist_ok=True)
    target.joinpath("00_index.md").write_text(render_root_index(steps), encoding="utf-8")
    target.joinpath("pack_registry.yaml").write_text(render_pack_registry(steps), encoding="utf-8")
    pack_dirs: list[str] = []
    for index, step in enumerate(steps, start=1):
        pack_dir = target / f"{index:02d}_{slugify(step['design_step_id'])}"
        write_pack(pack_dir, step, index)
        pack_dirs.append(str(pack_dir))
    return {"status": "pass", "target": str(target), "created_packs": pack_dirs, "construction_plan_lint_command": f"./.venv_backend_skills/bin/python Skills/Disabled-Octupos-OS-Backend/scripts/Cli_Toolbox.py construction-plan-lint --path {target} --json"}, 0


def construction_plan_lint_payload(path: Path) -> dict:
    root = path if path.is_dir() else path.parent if path.name == "00_index.md" else path
    exists = root.exists()
    pack_dirs = sorted([pack_dir for pack_dir in root.iterdir() if pack_dir.is_dir() and PACK_DIR_PATTERN.match(pack_dir.name)]) if exists else []
    missing_root_files = [name for name in ROOT_REQUIRED_FILES if not (root / name).exists()] if exists else list(ROOT_REQUIRED_FILES)
    missing_pack_files = {pack_dir.name: [name for name in PACK_MARKDOWN_FILES + PACK_MACHINE_FILES if not (pack_dir / name).exists()] for pack_dir in pack_dirs}
    missing_pack_files = {key: value for key, value in missing_pack_files.items() if value}
    files_to_check = [root / name for name in ROOT_REQUIRED_FILES if (root / name).exists()] + [pack_dir / name for pack_dir in pack_dirs for name in PACK_MARKDOWN_FILES + PACK_MACHINE_FILES if (pack_dir / name).exists()]
    replace_me_hits = [str(file_path.relative_to(root)) for file_path in files_to_check if "replace_me" in file_path.read_text(encoding="utf-8")]
    guidance_hits = [str(file_path.relative_to(root)) for file_path in files_to_check if file_path.suffix == ".md" and any(marker in file_path.read_text(encoding="utf-8") for marker in GUIDANCE_MARKERS)]
    schema_violations = [violation for pack_dir in pack_dirs if not missing_pack_files.get(pack_dir.name) for violation in machine_schema_violations(pack_dir)]
    status = "pass" if exists and pack_dirs and not missing_root_files and not missing_pack_files and not replace_me_hits and not guidance_hits and not schema_violations else "fail"
    return {"path": str(path), "resolved_root": str(root), "exists": exists, "status": status, "missing_root_files": missing_root_files, "missing_pack_dirs": [] if pack_dirs else ["expected at least one NN_* pack directory"], "missing_pack_files": missing_pack_files, "files_with_replace_me": replace_me_hits, "files_with_template_guidance": guidance_hits, "machine_schema_violations": schema_violations, "pack_markdown_files": PACK_MARKDOWN_FILES, "pack_machine_files": PACK_MACHINE_FILES, "construction_plan_gate_allowed": status == "pass"}
