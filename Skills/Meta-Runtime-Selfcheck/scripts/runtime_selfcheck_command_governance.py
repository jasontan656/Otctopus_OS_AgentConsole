from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shlex
import subprocess
from typing import cast

from runtime_pain_types import CommandGovernanceContext
from runtime_pain_types import CommandNormalizationResult
from runtime_pain_types import ExpectedFailureMatch
from runtime_pain_types import ExpectedFailureRule
from runtime_pain_types import KeywordFirstEditDecision
from runtime_pain_types import KeywordFirstReplacement
from runtime_pain_types import PreExecCheckResult
from runtime_pain_types import RuntimeFailureAnalysis


_PATH_EXCEPTIONS = (OSError, RuntimeError, ValueError)
_SUBPROCESS_EXCEPTIONS = (OSError, ValueError, subprocess.SubprocessError)
_TRACEABILITY_MESSAGE_KEYWORDS = (
    "problem",
    "issue",
    "resolved",
    "resolve",
    "fixed",
    "fix",
    "root cause",
    "impact",
    "risk",
    "问题",
    "解决",
    "修复",
    "根因",
    "影响",
    "风险",
)
_NO_PYTEST_RE = re.compile(r"no module named pytest", re.IGNORECASE)
_LINT_TARGET_DIR_RE = re.compile(r"--target 必须是存在的目录")
_TRACEABILITY_RE = re.compile(r"traceability_message_must_describe_problem_or_resolution")


def _console_repo_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is None:
        raise RuntimeError("cannot resolve Otctopus_OS_AgentConsole repo root")
    return repo_root


CONSOLE_REPO_ROOT = _console_repo_root()
WORKSPACE_ROOT = CONSOLE_REPO_ROOT.parent
KNOWN_REPO_ROOTS = {
    "Otctopus_OS_AgentConsole": CONSOLE_REPO_ROOT,
    "Octopus_OS": WORKSPACE_ROOT / "Octopus_OS",
}
_KEYWORD_FIRST_FORBIDDEN_MARKERS = (
    "legacy",
    "compatibility",
    "compatibility layer",
    "alias",
    "mapping",
    "adapter",
    "bridge",
    "dual-track",
    "dual track",
    "双轨",
    "兼容",
    "过渡",
)
_REPAIR_TYPE_REPLACEMENTS: dict[str, tuple[str, str, str]] = {
    "repo_local_python_alignment": (
        "python3 / system python",
        ".venv_backend_skills/bin/python3",
        "Align repo-local Python execution in-place instead of adding wrappers.",
    ),
    "lint_target_directory_normalization": (
        "file-level lint target",
        "governed directory target",
        "Replace invalid target shape directly at the command surface.",
    ),
    "traceability_message_normalization": (
        "invalid traceability message",
        "governed traceability message template",
        "Replace the message body instead of layering explanatory patches.",
    ),
}
_REPLACE_SUBKINDS = {
    "installed_copy_product_root_mismatch",
    "unknown_option",
    "unknown_subcommand",
    "system_python_missing_repo_pytest",
    "lint_target_requires_directory",
    "traceability_message_contract_violation",
    "non_repo_git_target",
}


def _safe_resolve(path: Path) -> Path:
    try:
        return path.expanduser().resolve()
    except _PATH_EXCEPTIONS:
        return path.expanduser()


def _resolve_path_token(path_token: str, workdir: str | None) -> Path:
    base = _safe_resolve(Path(str(workdir or "").strip() or os.getcwd()))
    candidate = Path(path_token).expanduser()
    if not candidate.is_absolute():
        candidate = base / candidate
    return _safe_resolve(candidate)


def _detect_repo_root(candidate_dir: str) -> str:
    target = str(candidate_dir or "").strip()
    if not target:
        return ""
    try:
        proc = subprocess.run(
            ["git", "-C", target, "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
    except _SUBPROCESS_EXCEPTIONS:
        return ""
    return str(proc.stdout or "").strip() if proc.returncode == 0 else ""


def _extract_flag_value(tokens: list[str], flag: str) -> str:
    for idx, token in enumerate(tokens):
        raw = str(token or "").strip()
        if raw == flag:
            return str(tokens[idx + 1] or "").strip() if idx + 1 < len(tokens) else ""
        if raw.startswith(f"{flag}="):
            return raw.partition("=")[2]
    return ""


def _replace_single_flag_value(tokens: list[str], flag: str, new_value: str) -> list[str]:
    result: list[str] = []
    replaced = False
    skip_next = False
    for idx, token in enumerate(tokens):
        raw = str(token or "")
        if skip_next:
            skip_next = False
            continue
        if raw == flag:
            result.extend([flag, new_value])
            skip_next = idx + 1 < len(tokens)
            replaced = True
            continue
        if raw.startswith(f"{flag}="):
            result.append(f"{flag}={new_value}")
            replaced = True
            continue
        result.append(raw)
    if not replaced:
        result.extend([flag, new_value])
    return result


def _extract_repeated_flag_values(tokens: list[str], flag: str) -> list[str]:
    values: list[str] = []
    idx = 0
    while idx < len(tokens):
        token = str(tokens[idx] or "").strip()
        if token == flag:
            if idx + 1 < len(tokens):
                values.append(str(tokens[idx + 1] or "").strip())
            idx += 2
            continue
        if token.startswith(f"{flag}="):
            values.append(token.partition("=")[2].strip())
        idx += 1
    return values


def _replace_repeated_flag_values(tokens: list[str], flag: str, new_values: list[str]) -> list[str]:
    result: list[str] = []
    inserted = False
    skip_next = False
    for idx, token in enumerate(tokens):
        raw = str(token or "")
        if skip_next:
            skip_next = False
            continue
        if raw == flag:
            if not inserted:
                for value in new_values:
                    result.extend([flag, value])
                inserted = True
            skip_next = idx + 1 < len(tokens)
            continue
        if raw.startswith(f"{flag}="):
            if not inserted:
                for value in new_values:
                    result.append(f"{flag}={value}")
                inserted = True
            continue
        result.append(raw)
    if not inserted:
        for value in new_values:
            result.extend([flag, value])
    return result


def _message_is_valid(message: str) -> bool:
    normalized = str(message or "").strip()
    if not normalized:
        return False
    lines = [line.strip() for line in normalized.splitlines()]
    subject = next((line for line in lines if line), "")
    body_lines = [line for line in lines[1:] if line]
    if not subject or len(body_lines) < 2:
        return False
    body_text = " ".join(body_lines).lower()
    return any(keyword in body_text for keyword in _TRACEABILITY_MESSAGE_KEYWORDS)


def _command_tokens(command: str) -> list[str]:
    try:
        return list(shlex.split(str(command or "").strip()))
    except ValueError:
        return []


def _infer_repo_root_from_tokens(tokens: list[str], fallback_workdir: str | None) -> str:
    workdir_repo = _detect_repo_root(str(_resolve_path_token(".", fallback_workdir)))
    if workdir_repo:
        return workdir_repo

    repo_flag = _extract_flag_value(tokens, "--repo")
    repo_from_flag = KNOWN_REPO_ROOTS.get(repo_flag)
    if repo_from_flag and repo_from_flag.exists():
        return str(repo_from_flag.resolve())

    for token in tokens:
        value = str(token or "").strip()
        if not value:
            continue
        if value.startswith("Skills/") or value.startswith("./.venv_backend_skills") or value.startswith(".venv_backend_skills/"):
            return str(CONSOLE_REPO_ROOT)
        if "Otctopus_OS_AgentConsole" in value:
            return str(CONSOLE_REPO_ROOT)
        if "Octopus_OS/" in value and KNOWN_REPO_ROOTS["Octopus_OS"].exists():
            return str(KNOWN_REPO_ROOTS["Octopus_OS"].resolve())
        if value.startswith(("/", "./", "../", "~")):
            resolved = _resolve_path_token(value, fallback_workdir)
            candidate = resolved if resolved.is_dir() else resolved.parent
            repo_root = _detect_repo_root(str(candidate))
            if repo_root:
                return repo_root
    return ""


def derive_command_context(command: str, *, workdir: str | None = None) -> CommandGovernanceContext:
    tokens = _command_tokens(command)
    repo_root = _infer_repo_root_from_tokens(tokens, workdir)
    effective_workdir = repo_root or str(_resolve_path_token(".", workdir))
    repo_path = Path(repo_root) if repo_root else None
    backend_python = ""
    if repo_path is not None:
        candidate = repo_path / ".venv_backend_skills" / "bin" / "python3"
        if candidate.exists():
            backend_python = str(candidate)
    return {
        "repo_root": repo_root,
        "workdir": effective_workdir,
        "change_detection_root": repo_root or effective_workdir,
        "backend_python": backend_python,
    }


def _should_use_repo_python(tokens: list[str], context: dict[str, str]) -> bool:
    backend_python = str(context.get("backend_python", "") or "").strip()
    if not backend_python or not tokens:
        return False
    executable = Path(str(tokens[0] or "").strip()).name.lower()
    if executable not in {"python", "python3"} and str(tokens[0] or "").strip() != backend_python:
        return False
    if len(tokens) > 2 and tokens[1] == "-m" and tokens[2] == "pytest":
        return True
    if len(tokens) > 1 and str(tokens[1] or "").strip().endswith(".py"):
        resolved_script = _resolve_path_token(str(tokens[1] or "").strip(), context.get("workdir"))
        try:
            return resolved_script.is_file() and resolved_script.is_relative_to(CONSOLE_REPO_ROOT)
        except ValueError:
            return False
    return False


def _normalize_lint_targets(tokens: list[str], context: dict[str, str]) -> tuple[list[str], bool]:
    if not tokens:
        return tokens, False
    if len(tokens) < 2 or not str(tokens[1] or "").strip().endswith("run_python_code_lints.py"):
        return tokens, False
    targets = _extract_repeated_flag_values(tokens, "--target")
    if not targets:
        return tokens, False
    normalized_paths: list[Path] = []
    seen: set[str] = set()
    changed = False
    for target in targets:
        resolved = _resolve_path_token(target, context.get("workdir"))
        if resolved.exists() and resolved.is_file():
            resolved = resolved.parent
            changed = True
        normalized_paths.append(resolved)

    skill_roots: set[str] = set()
    for resolved in normalized_paths:
        try:
            parts = resolved.parts
            if "Skills" in parts:
                idx = parts.index("Skills")
                if idx + 1 < len(parts):
                    skill_roots.add(str(Path(*parts[: idx + 2])))
        except ValueError:
            continue
    if len(skill_roots) == 1:
        normalized_paths = [Path(next(iter(skill_roots)))]
        changed = True

    normalized_targets: list[str] = []
    for resolved in normalized_paths:
        normalized = str(resolved)
        if normalized not in seen:
            seen.add(normalized)
            normalized_targets.append(normalized)
    return _replace_repeated_flag_values(tokens, "--target", normalized_targets), changed


def _message_scope_hint(tokens: list[str], context: dict[str, str]) -> str:
    paths = _extract_repeated_flag_values(tokens, "--path")
    if paths:
        path = paths[0]
        parts = Path(path).parts
        if "Skills" in parts:
            skill_index = parts.index("Skills")
            if skill_index + 1 < len(parts):
                return parts[skill_index + 1]
        return Path(path).name
    repo_root = str(context.get("repo_root", "") or "")
    return Path(repo_root).name if repo_root else "governed change"


def _build_traceability_message(tokens: list[str], context: dict[str, str], current_message: str) -> str:
    current_lines = [line.strip() for line in str(current_message or "").splitlines() if line.strip()]
    subject = current_lines[0] if current_lines else f"record governed update for {_message_scope_hint(tokens, context)}"
    if len(subject) > 72:
        subject = subject[:72].rstrip()
    scope_hint = _message_scope_hint(tokens, context)
    body_lines = [
        f"- problem: normalize governed runtime behavior for {scope_hint}",
        f"- impact: reduce repo-local execution drift and keep traceability aligned",
    ]
    return "\n".join([subject, "", *body_lines])


def _normalize_traceability_message(tokens: list[str], context: dict[str, str]) -> tuple[list[str], bool]:
    if not tokens:
        return tokens, False
    if len(tokens) < 3:
        return tokens, False
    script_hint = str(tokens[1] or "").strip()
    subcommand = str(tokens[2] or "").strip()
    if "Meta-github-operation" not in script_hint and "meta_github_operation_family.py" not in script_hint:
        return tokens, False
    if subcommand not in {"commit", "commit-and-push", "repo-bootstrap"}:
        return tokens, False
    message = _extract_flag_value(tokens, "--message")
    if _message_is_valid(message):
        return tokens, False
    normalized = _build_traceability_message(tokens, context, message)
    return _replace_single_flag_value(tokens, "--message", normalized), True


def _collect_forbidden_markers(*texts: str) -> list[str]:
    lowered = " ".join(str(text or "") for text in texts).lower()
    return [marker for marker in _KEYWORD_FIRST_FORBIDDEN_MARKERS if marker in lowered]


def _replacement_pairs_for_repair_types(repair_types: list[str]) -> list[KeywordFirstReplacement]:
    pairs: list[KeywordFirstReplacement] = []
    for repair_type in repair_types:
        payload = _REPAIR_TYPE_REPLACEMENTS.get(str(repair_type or "").strip())
        if payload is None:
            continue
        old_value, new_value, reason = payload
        pairs.append({"old": old_value, "new": new_value, "reason": reason})
    return pairs


def adjudicate_keyword_first_edit(
    *,
    issue_kind: str,
    issue_subkind: str,
    title: str = "",
    summary: str = "",
    why: str = "",
    suggested_action: str = "",
    repair_types: list[str] | None = None,
) -> KeywordFirstEditDecision:
    normalized_repair_types = [str(item).strip() for item in repair_types or [] if str(item).strip()]
    forbidden_markers = _collect_forbidden_markers(title, summary, why, suggested_action, " ".join(normalized_repair_types))
    if forbidden_markers:
        return {
            "decision": "rewrite",
            "rationale": "The described remediation path already carries legacy or compatibility residue, so local patch stacking is disallowed.",
            "seamless_state": "Not seamless until the target surface is rewritten without legacy, compatibility shells, aliases, mappings, or bridge layers.",
            "requires_user_confirmation": True,
            "confirmation_reason": "Rewrite/delete path detected; enumerate the exact files or blocks to be removed or fully replaced before executing.",
            "deletion_scope": [],
            "replacement_pairs": [],
            "forbidden_patterns_present": forbidden_markers,
            "why_not_add": "Adding new layers would preserve the incompatible structure instead of converging the target surface.",
        }

    replacement_pairs = _replacement_pairs_for_repair_types(normalized_repair_types)
    if replacement_pairs or issue_subkind in _REPLACE_SUBKINDS:
        return {
            "decision": "replace",
            "rationale": "The target surface can converge by directly replacing the wrong governed entrypoint, parameter shape, or contract wording.",
            "seamless_state": "Seamless once the incorrect governed surface is replaced in place with no compatibility residue.",
            "requires_user_confirmation": False,
            "confirmation_reason": "",
            "deletion_scope": [],
            "replacement_pairs": replacement_pairs,
            "forbidden_patterns_present": [],
            "why_not_add": "Adding a second track would leave the broken surface alive and violate keyword-first governance.",
        }

    return {
        "decision": "add",
        "rationale": "The current evidence points to a missing governed capability, and no safe rewrite or direct replacement can be proven from this signal alone.",
        "seamless_state": "Seamless only if the new content is a single canonical addition rather than a compatibility overlay.",
        "requires_user_confirmation": False,
        "confirmation_reason": "",
        "deletion_scope": [],
        "replacement_pairs": [],
        "forbidden_patterns_present": [],
        "why_not_add": "",
    }


def normalize_command(command: str, *, workdir: str | None = None) -> CommandNormalizationResult:
    tokens = _command_tokens(command)
    if not tokens:
        return {
            "command": str(command or ""),
            "normalized_command": str(command or ""),
            "changed": False,
            "repair_types": [],
            "context": derive_command_context(str(command or ""), workdir=workdir),
        }
    context = derive_command_context(command, workdir=workdir)
    changed = False
    repair_types: list[str] = []
    if _should_use_repo_python(tokens, context):
        backend_python = str(context.get("backend_python", "") or "").strip()
        if backend_python and str(tokens[0] or "").strip() != backend_python:
            tokens[0] = backend_python
            changed = True
            repair_types.append("repo_local_python_alignment")
    tokens, lint_changed = _normalize_lint_targets(tokens, context)
    if lint_changed:
        changed = True
        repair_types.append("lint_target_directory_normalization")
    tokens, message_changed = _normalize_traceability_message(tokens, context)
    if message_changed:
        changed = True
        repair_types.append("traceability_message_normalization")
    return {
        "command": str(command or ""),
        "normalized_command": shlex.join(tokens),
        "changed": changed,
        "repair_types": repair_types,
        "context": context,
    }


def load_expected_failure_rules(path: str | None) -> list[ExpectedFailureRule]:
    if not path:
        return []
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        rules = payload.get("rules", [])
        return [cast(ExpectedFailureRule, dict(rule)) for rule in rules if isinstance(rule, dict)] if isinstance(rules, list) else []
    if isinstance(payload, list):
        return [cast(ExpectedFailureRule, dict(rule)) for rule in payload if isinstance(rule, dict)]
    return []


def match_expected_failure(
    *,
    command: str,
    stage: str | None = None,
    output_text: str = "",
    reason_code: str = "",
    rules: list[ExpectedFailureRule] | None = None,
) -> ExpectedFailureMatch:
    lowered_command = str(command or "").lower()
    lowered_output = str(output_text or "").lower()
    lowered_stage = str(stage or "").strip().lower()
    lowered_reason_code = str(reason_code or "").strip().lower()
    for rule in rules or []:
        command_contains = [str(item).lower() for item in list(rule.get("command_contains", [])) if str(item).strip()]
        output_contains = [str(item).lower() for item in list(rule.get("output_contains", [])) if str(item).strip()]
        reason_codes = [str(item).lower() for item in list(rule.get("reason_codes", [])) if str(item).strip()]
        stages = [str(item).lower() for item in list(rule.get("stages", [])) if str(item).strip()]
        if command_contains and not all(item in lowered_command for item in command_contains):
            continue
        if output_contains and not all(item in lowered_output for item in output_contains):
            continue
        if reason_codes and lowered_reason_code not in reason_codes:
            continue
        if stages and lowered_stage not in stages:
            continue
        return {
            "matched": True,
            "rule_id": str(rule.get("rule_id", "") or ""),
            "reason": str(rule.get("reason", "") or "expected failure rule matched"),
            "action": str(rule.get("action", "") or "allow_expected_failure"),
        }
    return {"matched": False}


def adjudicate_pre_exec_command(
    *,
    command: str,
    workdir: str | None = None,
    stage: str | None = None,
    expected_failure_rules: list[ExpectedFailureRule] | None = None,
) -> PreExecCheckResult:
    context = derive_command_context(command, workdir=workdir)
    expected = match_expected_failure(command=command, stage=stage, rules=expected_failure_rules or [])
    normalized = normalize_command(command, workdir=context.get("workdir"))
    keyword_first_edit = adjudicate_keyword_first_edit(
        issue_kind="pre_exec_command_governance",
        issue_subkind="normalized_command" if normalized.get("changed") else "preflight_gate",
        summary="Meta-Runtime-Selfcheck must converge command surfaces through rewrite/replace/add governance before execution.",
        suggested_action=", ".join(list(normalized.get("repair_types", []))) or "Record the pending command and decide whether a governed capability is missing.",
        repair_types=list(normalized.get("repair_types", [])),
    )
    from runtime_pain_repair_exec import preflight

    preflight_ok, reason_code, detail = preflight(
        command=normalized["normalized_command"],
        workdir=str(context.get("workdir", "") or ""),
    )
    if expected.get("matched"):
        return {
            "status": "ok",
            "decision": "allow_expected_failure",
            "command": command,
            "normalized_command": normalized["normalized_command"],
            "reason_code": reason_code,
            "detail": detail,
            "expected_failure": expected,
            "repair_types": normalized["repair_types"],
            "repair_context": context,
            "keyword_first_edit": keyword_first_edit,
        }
    if normalized["changed"]:
        return {
            "status": "ok",
            "decision": "immediate_repair",
            "command": command,
            "normalized_command": normalized["normalized_command"],
            "reason_code": "normalized_before_exec",
            "detail": ", ".join(normalized["repair_types"]),
            "expected_failure": {"matched": False},
            "repair_types": normalized["repair_types"],
            "repair_context": context,
            "keyword_first_edit": keyword_first_edit,
        }
    if not preflight_ok:
        return {
            "status": "ok",
            "decision": "pending_decision",
            "command": command,
            "normalized_command": normalized["normalized_command"],
            "reason_code": reason_code,
            "detail": detail,
            "expected_failure": {"matched": False},
            "repair_types": [],
            "repair_context": context,
            "keyword_first_edit": keyword_first_edit,
        }
    return {
        "status": "ok",
        "decision": "allow",
        "command": command,
        "normalized_command": normalized["normalized_command"],
        "reason_code": "",
        "detail": "",
        "expected_failure": {"matched": False},
        "repair_types": [],
        "repair_context": context,
        "keyword_first_edit": keyword_first_edit,
    }


def analyze_runtime_failure(
    *,
    command: str,
    output_text: str,
    workdir: str | None = None,
    stage: str | None = None,
    expected_failure_rules: list[ExpectedFailureRule] | None = None,
) -> RuntimeFailureAnalysis:
    expected = match_expected_failure(
        command=command,
        stage=stage,
        output_text=output_text,
        rules=expected_failure_rules or [],
    )
    normalized = normalize_command(command, workdir=workdir)
    normalized_changed = bool(normalized.get("changed", False))
    lowered_output = str(output_text or "").lower()
    if _NO_PYTEST_RE.search(lowered_output) and "pytest" in str(command or ""):
        keyword_first_edit = adjudicate_keyword_first_edit(
            issue_kind="repo_local_env_mismatch",
            issue_subkind="system_python_missing_repo_pytest",
            title="Repo-local pytest command used the wrong Python interpreter",
            summary="命令落到了系统 Python，未切到 repo-local `.venv_backend_skills`。",
            why="repo-local Python contract 没有在执行前生效。",
            suggested_action="把 repo-local pytest 与 repo-local Python script 执行统一归一化到 `.venv_backend_skills/bin/python3`。",
            repair_types=list(normalized.get("repair_types", [])),
        )
        return {
            "matched": True,
            "issue_kind": "repo_local_env_mismatch",
            "issue_subkind": "system_python_missing_repo_pytest",
            "title": "Repo-local pytest command used the wrong Python interpreter",
            "summary": "命令落到了系统 Python，未切到 repo-local `.venv_backend_skills`。",
            "why": "repo-local Python contract 没有在执行前生效。",
            "suggested_action": "把 repo-local pytest 与 repo-local Python script 执行统一归一化到 `.venv_backend_skills/bin/python3`。",
            "adjudication": "allow_expected_failure" if expected.get("matched") else ("immediate_repair" if normalized_changed else "strengthen_now"),
            "expected_failure": expected,
            "auto_repair": normalized if normalized_changed and not expected.get("matched") else {},
            "keyword_first_edit": keyword_first_edit,
        }
    if _LINT_TARGET_DIR_RE.search(output_text):
        keyword_first_edit = adjudicate_keyword_first_edit(
            issue_kind="contract_shape_mismatch",
            issue_subkind="lint_target_requires_directory",
            title="Governed lint command received file targets instead of directories",
            summary="lint CLI 的输入合同只接受目录，但命令把文件路径直接传了进去。",
            why="contract shape 没有在执行前被校验或归一化。",
            suggested_action="在 pre-exec 阶段把 file targets 提升到受管目录集合。",
            repair_types=list(normalized.get("repair_types", [])),
        )
        return {
            "matched": True,
            "issue_kind": "contract_shape_mismatch",
            "issue_subkind": "lint_target_requires_directory",
            "title": "Governed lint command received file targets instead of directories",
            "summary": "lint CLI 的输入合同只接受目录，但命令把文件路径直接传了进去。",
            "why": "contract shape 没有在执行前被校验或归一化。",
            "suggested_action": "在 pre-exec 阶段把 file targets 提升到受管目录集合。",
            "adjudication": "allow_expected_failure" if expected.get("matched") else ("immediate_repair" if normalized_changed else "strengthen_now"),
            "expected_failure": expected,
            "auto_repair": normalized if normalized_changed and not expected.get("matched") else {},
            "keyword_first_edit": keyword_first_edit,
        }
    if _TRACEABILITY_RE.search(output_text):
        keyword_first_edit = adjudicate_keyword_first_edit(
            issue_kind="governed_validation_failure",
            issue_subkind="traceability_message_contract_violation",
            title="Governed traceability message did not satisfy commit contract",
            summary="受管 Git traceability message 没写清问题、风险或结果，触发了技能级校验失败。",
            why="governed CLI validation 是已知 contract，但命令未在执行前做 message adjudication。",
            suggested_action="在 pre-exec 阶段校验并规范化 traceability message；无法安全生成时转 pending decision。",
            repair_types=list(normalized.get("repair_types", [])),
        )
        return {
            "matched": True,
            "issue_kind": "governed_validation_failure",
            "issue_subkind": "traceability_message_contract_violation",
            "title": "Governed traceability message did not satisfy commit contract",
            "summary": "受管 Git traceability message 没写清问题、风险或结果，触发了技能级校验失败。",
            "why": "governed CLI validation 是已知 contract，但命令未在执行前做 message adjudication。",
            "suggested_action": "在 pre-exec 阶段校验并规范化 traceability message；无法安全生成时转 pending decision。",
            "adjudication": "allow_expected_failure" if expected.get("matched") else ("immediate_repair" if normalized_changed else "pending_decision"),
            "expected_failure": expected,
            "auto_repair": normalized if normalized_changed and not expected.get("matched") else {},
            "keyword_first_edit": keyword_first_edit,
        }
    return {"matched": False}
