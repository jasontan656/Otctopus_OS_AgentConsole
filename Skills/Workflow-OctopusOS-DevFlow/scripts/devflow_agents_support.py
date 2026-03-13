from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import TypedDict


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]
META_DEFAULT_MD_MANAGER_CLI = (
    REPO_ROOT / "Skills" / "Meta-RootFile-Manager" / "scripts" / "Cli_Toolbox.py"
).resolve()
EXTERNAL_AGENTS_TEMPLATE = SKILL_ROOT / "assets" / "templates" / "agents" / "EXTERNAL_AGENTS.md"
MACHINE_AGENTS_TEMPLATE = SKILL_ROOT / "assets" / "templates" / "agents" / "AGENTS_MACHINE_TEMPLATE.json"


class MachineAgentsPayload(TypedDict):
    target_root: str
    development_docs_root: str
    codebase_root: str
    module_dir: str
    module_docs_root: str
    mother_doc_root: str
    construction_plan_root: str
    graph_runtime_root: str
    acceptance_root: str


def _render_template(path: Path, replacements: dict[str, str]) -> str:
    text = path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def render_external_agents(runtime: dict[str, object]) -> str:
    module_docs_root = Path(runtime["docs_root"])
    agents_path = module_docs_root / "AGENTS.md"
    replacements = {
        "external_agents_path": str(agents_path),
        "target_root": str(runtime["target_root"]),
        "development_docs_root": str(runtime["development_docs_root"]),
        "codebase_root": str(runtime["codebase_root"]),
        "module_dir": str(runtime["module_dir"]),
        "module_docs_root": str(runtime["docs_root"]),
        "mother_doc_root": str(runtime["mother_doc_root"]),
        "construction_plan_root": str(runtime["construction_plan_root"]),
        "graph_runtime_root": str(runtime["graph_runtime_root"]),
    }
    return _render_template(EXTERNAL_AGENTS_TEMPLATE, replacements)


def render_machine_contract(runtime: dict[str, object]) -> MachineAgentsPayload:
    replacements = {
        "target_root": str(runtime["target_root"]),
        "development_docs_root": str(runtime["development_docs_root"]),
        "codebase_root": str(runtime["codebase_root"]),
        "module_dir": str(runtime["module_dir"]),
        "module_docs_root": str(runtime["docs_root"]),
        "mother_doc_root": str(runtime["mother_doc_root"]),
        "construction_plan_root": str(runtime["construction_plan_root"]),
        "graph_runtime_root": str(runtime["graph_runtime_root"]),
        "acceptance_root": str(runtime["acceptance_root"]),
    }
    return json.loads(_render_template(MACHINE_AGENTS_TEMPLATE, replacements))


def _run_json_command(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"command_failed: {' '.join(command)}\nstdout={completed.stdout}\nstderr={completed.stderr}"
    )
    return json.loads(completed.stdout)


def _managed_machine_path(target_contract: dict[str, object]) -> Path:
    machine_path = target_contract.get("managed_machine_path")
    if isinstance(machine_path, str) and machine_path:
        return Path(machine_path)
    managed_files = target_contract.get("managed_files")
    if isinstance(managed_files, dict):
        machine_candidate = managed_files.get("machine")
        if isinstance(machine_candidate, str) and machine_candidate:
            return Path(machine_candidate)
    raise KeyError("managed_machine_path")


def scaffold_and_collect_devflow_agents(runtime: dict[str, object]) -> dict[str, object]:
    module_docs_root = Path(runtime["docs_root"])
    external_agents_path = module_docs_root / "AGENTS.md"
    scaffold_payload = _run_json_command(
        [
            "python3",
            str(META_DEFAULT_MD_MANAGER_CLI),
            "scaffold",
            "--target-dir",
            str(module_docs_root),
            "--file-kind",
            "AGENTS.md",
            "--allow-existing",
            "--json",
        ]
    )
    target_contract = _run_json_command(
        [
            "python3",
            str(META_DEFAULT_MD_MANAGER_CLI),
            "target-contract",
            "--source-path",
            str(external_agents_path),
            "--json",
        ]
    )
    machine_path = _managed_machine_path(target_contract)
    machine_path.parent.mkdir(parents=True, exist_ok=True)
    machine_path.write_text(
        json.dumps(render_machine_contract(runtime), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    external_agents_path.write_text(render_external_agents(runtime), encoding="utf-8")
    collect_payload = _run_json_command(
        [
            "python3",
            str(META_DEFAULT_MD_MANAGER_CLI),
            "collect",
            "--source-path",
            str(external_agents_path),
            "--json",
        ]
    )
    refreshed_target_contract = _run_json_command(
        [
            "python3",
            str(META_DEFAULT_MD_MANAGER_CLI),
            "target-contract",
            "--source-path",
            str(external_agents_path),
            "--json",
        ]
    )
    return {
        "external_agents_path": str(external_agents_path),
        "scaffold_payload": scaffold_payload,
        "collect_payload": collect_payload,
        "target_contract": refreshed_target_contract,
    }
