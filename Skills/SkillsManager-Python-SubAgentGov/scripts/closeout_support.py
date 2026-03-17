from __future__ import annotations

import json
from pathlib import Path

from command_support import run_cmd
from command_support import run_json_cmd
from command_support import tmux_exists
from command_support import tmux_kill
from result_support import expected_exit_code
from result_support import load_result
from runtime_types import ClosurePayload
from runtime_types import JSONDict
from runtime_types import JSONValue
from runtime_types import RESULT_STATUSES
from runtime_types import RuntimeConfig
from runtime_types import VerificationSummary
from runtime_types import Worker


def _quality_gain_text(value: JSONValue) -> str:
    if isinstance(value, dict):
        parts = [value.get("label") or value.get("type"), value.get("description") or value.get("detail")]
        return " / ".join(str(part) for part in parts if part)
    return str(value)


def verify_skill(config: RuntimeConfig, skill: str, result: JSONDict) -> VerificationSummary:
    skill_root = config.skills_root / skill
    summary: VerificationSummary = {"lint": None, "pytest": None, "help": None}
    summary["lint"] = run_json_cmd(
        [str(config.python_executable), str(config.lint_script), "--target", f"Skills/{skill}"],
        cwd=config.repo_root,
    )
    tests_dir = skill_root / "tests"
    if tests_dir.exists():
        pytest_proc = run_cmd(
            [str(config.python_executable), "-m", "pytest", f"Skills/{skill}/tests"],
            check=False,
            cwd=config.repo_root,
        )
        expected_pytest = expected_exit_code(result, f"pytest Skills/{skill}")
        pytest_no_tests = pytest_proc.returncode == 5 and "collected 0 items" in pytest_proc.stdout
        if expected_pytest is not None and pytest_proc.returncode != expected_pytest:
            raise RuntimeError(f"{skill} pytest exit code drifted from result contract")
        if expected_pytest is None and pytest_proc.returncode != 0 and not pytest_no_tests:
            raise RuntimeError(f"{skill} pytest failed\nstdout={pytest_proc.stdout}\nstderr={pytest_proc.stderr}")
        summary["pytest"] = {
            "exit_code": pytest_proc.returncode,
            "expected_exit_code": expected_pytest,
            "accepted_no_tests": pytest_no_tests,
            "stdout_tail": pytest_proc.stdout[-2000:],
            "stderr_tail": pytest_proc.stderr[-2000:],
        }
        return summary
    cli_toolbox = skill_root / "scripts" / "Cli_Toolbox.py"
    if cli_toolbox.exists():
        help_proc = run_cmd([str(config.python_executable), str(cli_toolbox), "--help"], check=False, cwd=config.repo_root)
        if help_proc.returncode != 0:
            raise RuntimeError(f"{skill} Cli_Toolbox --help failed\nstdout={help_proc.stdout}\nstderr={help_proc.stderr}")
        summary["help"] = {
            "exit_code": help_proc.returncode,
            "stdout_tail": help_proc.stdout[-2000:],
            "stderr_tail": help_proc.stderr[-2000:],
        }
    return summary


def build_commit_message(skill: str, result: JSONDict, changed: bool) -> str:
    quality_gain = result.get("quality_gain", "no_change_needed")
    summary = str(result.get("summary", "完成目标技能的 Python 代码规范治理。"))
    risk_line = (
        "风险降低: 通过最小目标内改动修复 Python 规范问题，并保持 OEC 与可观察副作用不变。"
        if changed
        else "风险降低: 证明当前技能无需修复并避免无证据 churn，仍保留独立 traceability。"
    )
    return "\n".join(
        [
            f"Govern skill {skill} Python code under traceable loop",
            f"- 解决问题: {summary}",
            f"- {risk_line}",
            f"- 代码质量增益: {_quality_gain_text(quality_gain)}",
            "- 验证: Dev-PythonCode-Constitution lint 通过，并完成目标技能的串行收口前验证。",
        ]
    )


def _collect_changed_files(config: RuntimeConfig, skill: str) -> list[str]:
    diff_proc = run_cmd(["git", "diff", "--name-only", "--", f"Skills/{skill}"], check=False, cwd=config.repo_root)
    changed = [line.strip() for line in diff_proc.stdout.splitlines() if line.strip()]
    untracked_proc = run_cmd(
        ["git", "ls-files", "--others", "--exclude-standard", "--", f"Skills/{skill}"],
        check=False,
        cwd=config.repo_root,
    )
    for line in untracked_proc.stdout.splitlines():
        value = line.strip()
        if value and value not in changed:
            changed.append(value)
    return changed


def _commit_and_push(config: RuntimeConfig, skill: str, result: JSONDict, changed: bool) -> JSONDict:
    cmd = [
        str(config.python_executable),
        str(config.git_tool),
        "commit-and-push",
        "--repo",
        config.repo_root.name,
        "--path",
        f"Skills/{skill}",
        "--message",
        build_commit_message(skill, result, changed),
        "--remote",
        "origin",
        "--json",
    ]
    if not changed:
        cmd.append("--allow-empty")
    return run_json_cmd(cmd, cwd=config.repo_root)


def _mirror_sync(config: RuntimeConfig, skill: str) -> JSONDict:
    return run_json_cmd(
        [
            str(config.python_executable),
            str(config.mirror_tool),
            "--scope",
            "skill",
            "--skill-name",
            skill,
            "--mode",
            "push",
        ],
        cwd=config.repo_root,
    )


def process_completion(config: RuntimeConfig, worker: Worker) -> ClosurePayload:
    result = load_result(worker)
    status = result.get("status")
    if not isinstance(status, str) or status not in RESULT_STATUSES:
        raise RuntimeError(f"{worker.skill} subagent did not complete successfully: {json.dumps(result, ensure_ascii=False, indent=2)}")
    changed_files = _collect_changed_files(config, worker.skill)
    verification = verify_skill(config, worker.skill, result)
    commit_payload = _commit_and_push(config, worker.skill, result, bool(changed_files))
    mirror_payload = _mirror_sync(config, worker.skill)
    tmux_kill(worker.session_name)
    closure: ClosurePayload = {
        "skill": worker.skill,
        "status": status,
        "changed_files": changed_files,
        "verification": verification,
        "commit_payload": commit_payload,
        "mirror_payload": mirror_payload,
        "session_name": worker.session_name,
        "session_closed": not tmux_exists(worker.session_name),
        "result_json_path": str(worker.result_json_path),
        "result_md_path": str(worker.result_md_path),
    }
    worker.closure_path.write_text(json.dumps(closure, ensure_ascii=False, indent=2), encoding="utf-8")
    return closure
