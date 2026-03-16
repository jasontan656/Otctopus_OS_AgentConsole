from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CLI = SKILL_ROOT / "scripts" / "Cli_Toolbox.py"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))


def run_cli(*args: str) -> dict:
    completed = subprocess.run(
        ["python3", str(CLI), *args, "--json"],
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(completed.stdout)


def run_cli_raw(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(CLI), *args, "--json"],
        text=True,
        capture_output=True,
        check=False,
    )


def create_runtime_layout(root: Path) -> dict[str, Path | str]:
    repo_root = root.resolve()
    codebase_root = repo_root / "sample_repo"
    docs_root = codebase_root / "Development_Docs"
    docs_root.mkdir(parents=True, exist_ok=True)
    return {
        "target_root": repo_root,
        "codebase_root": codebase_root,
        "development_docs_root": docs_root,
        "docs_root": docs_root,
        "module_dir": "sample_repo",
    }


def workspace_tempdir() -> tempfile.TemporaryDirectory[str]:
    return tempfile.TemporaryDirectory(dir=str(SKILL_ROOT.parents[2]))


def runtime_scope(layout: dict[str, Path | str]) -> tuple[str, ...]:
    return (
        "--target-root",
        str(layout["target_root"]),
        "--development-docs-root",
        str(layout["development_docs_root"]),
        "--docs-root",
        str(layout["docs_root"]),
        "--module-dir",
        str(layout["module_dir"]),
        "--codebase-root",
        str(layout["codebase_root"]),
    )


def init_git_repo(repo_root: Path) -> None:
    repo_root.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init"], cwd=repo_root, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.name", "Codex"], cwd=repo_root, check=True)
    subprocess.run(["git", "config", "user.email", "codex@example.com"], cwd=repo_root, check=True)
