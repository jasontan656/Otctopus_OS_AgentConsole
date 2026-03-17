from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict, TypeAlias, cast

import yaml


JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]
JsonArray: TypeAlias = list[JsonValue]
YamlValue: TypeAlias = JsonScalar | list["YamlValue"] | dict[str, "YamlValue"]
YamlObject: TypeAlias = dict[str, YamlValue]


class StatusPayload(TypedDict, total=False):
    status: str


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
REPO_ROOT = SKILL_ROOT.parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent
DEFAULT_OCTOPUS_ROOT = WORKSPACE_ROOT / "Octopus_OS"
RUNTIME_ROOT = SKILL_ROOT / "references" / "runtime_contracts"
CONTRACT_PATH = RUNTIME_ROOT / "SKILL_RUNTIME_CONTRACT.json"
DIRECTIVE_INDEX_PATH = RUNTIME_ROOT / "DIRECTIVE_INDEX.json"
RESULT_ROOT = WORKSPACE_ROOT / "Codex_Skills_Result" / "Workflow-SiteMap-Creation"
SKILL_RUNTIME_ROOT = WORKSPACE_ROOT / "Codex_Skill_Runtime" / "Workflow-SiteMap-Creation"
SUBAGENT_RUN_ROOT = SKILL_RUNTIME_ROOT / "subagent_runs"

META_ENHANCE_ROOT = REPO_ROOT / "Skills" / "Meta-Enhance-Prompt"
META_ENHANCE_CLI = META_ENHANCE_ROOT / "scripts" / "Cli_Toolbox.py"
META_ENHANCE_FILTER = META_ENHANCE_ROOT / "scripts" / "filter_active_invoke_output.py"

RUNTASK_ROOT = REPO_ROOT / "Skills" / "Functional-Analysis-Runtask"
RUNTASK_CLI = RUNTASK_ROOT / "scripts" / "Cli_Toolbox.py"

BACKEND_PYTHON = REPO_ROOT / ".venv_backend_skills" / "bin" / "python3"

ENTRY_CHAINS = {
    "self_governance": [
        "path/self_governance/00_SELF_GOVERNANCE_ENTRY.md",
        "path/self_governance/10_CONTRACT.md",
        "path/self_governance/20_FACTORY_CONVERSION.md",
        "path/self_governance/30_INTENT_ENHANCE.md",
        "path/self_governance/40_BACKGROUND_SUBAGENT.md",
        "path/self_governance/50_ARTIFACT_REFRESH.md",
        "path/self_governance/60_VALIDATION_CLOSEOUT.md",
    ],
    "artifact_lint_audit": [
        "path/artifact_lint_audit/00_ARTIFACT_AUDIT_ENTRY.md",
        "path/artifact_lint_audit/10_CONTRACT.md",
        "path/artifact_lint_audit/20_RULEBOOK.md",
        "path/artifact_lint_audit/30_VALIDATION.md",
    ],
}


def emit(payload: JsonObject, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(payload.get("status", "ok"))
    return 0 if payload.get("status", "ok") not in {"fail", "error"} else 1


def read_json(path: Path) -> JsonObject:
    return cast(JsonObject, json.loads(path.read_text(encoding="utf-8")))


def read_yaml(path: Path) -> YamlObject:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return payload if isinstance(payload, dict) else {}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_request_text(request_text: str | None, request_file: str | None) -> str:
    if request_text:
        return request_text.strip()
    if request_file:
        return Path(request_file).read_text(encoding="utf-8").strip()
    raise SystemExit("either --request-text or --request-file is required")


def resolve_runtime(target_root: str | None, mirror_root: str | None) -> JsonObject:
    repo_root = Path(target_root).resolve() if target_root else DEFAULT_OCTOPUS_ROOT.resolve()
    development_docs_root = repo_root / "Development_Docs"
    mother_doc_root = development_docs_root / "mother_doc"
    client_root = Path(mirror_root).resolve() if mirror_root else repo_root / "Client_Applications" / "mother_doc"
    missing: list[str] = []
    if not repo_root.exists():
        missing.append(str(repo_root))
    if not development_docs_root.exists():
        missing.append(str(development_docs_root))
    status = "pass" if not missing else "fail"
    return {
        "status": status,
        "repo_root": str(repo_root),
        "development_docs_root": str(development_docs_root),
        "mother_doc_root": str(mother_doc_root),
        "client_mirror_root": str(client_root),
        "missing_prerequisites": missing,
    }


def compile_reading_chain(entry: str) -> JsonObject:
    chain = ENTRY_CHAINS.get(entry)
    if chain is None:
        raise SystemExit(f"unknown entry: {entry}")
    return {"status": "ok", "entry": entry, "resolved_chain": chain}


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: JsonObject | JsonArray) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: YamlObject) -> None:
    ensure_parent(path)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def reset_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def parse_frontmatter(content: str) -> YamlObject:
    if not content.startswith("---\n"):
        return {}
    try:
        _, body = content.split("---\n", 1)
        header, _ = body.split("---\n", 1)
    except ValueError:
        return {}
    payload = yaml.safe_load(header)
    return payload if isinstance(payload, dict) else {}


def run_command(
    argv: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    text: bool = True,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    effective_env = os.environ.copy()
    if env:
        effective_env.update(env)
    return subprocess.run(
        argv,
        cwd=str(cwd) if cwd else None,
        env=effective_env,
        check=check,
        capture_output=True,
        text=text,
    )


def summarize_completed_process(completed: subprocess.CompletedProcess[str]) -> JsonObject:
    return {
        "args": completed.args,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def relpath(path: Path, root: Path) -> str:
    return str(path.resolve().relative_to(root.resolve()))
