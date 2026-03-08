#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_VERSION = 2
MAX_LOG_CHARS = 8000

DEFAULT_BUDGETS = {
    "dependency_missing": 3,
    "transient_runtime": 4,
    "context_overflow": 2,
    "logic_or_spec_gap": 4,
    "hard_blocker": 1,
}

DEFAULT_GUARDRAILS = {
    "max_total_attempts": 12,
    "max_runtime_minutes": 45,
    "max_stagnation": 4,
    "repeat_failure_limit": 3,
}

DEFAULT_BACKGROUND_WORKER_GUARDRAILS = {
    "max_total_attempts": 6,
    "max_runtime_minutes": 30,
    "max_stagnation": 2,
    "repeat_failure_limit": 2,
}

DEFAULT_BACKGROUND_WORKER_BUDGETS = {
    "dependency_missing": 2,
    "transient_runtime": 2,
    "context_overflow": 1,
    "logic_or_spec_gap": 2,
    "hard_blocker": 1,
}

FAILURE_KINDS = {
    "dependency_missing",
    "transient_runtime",
    "context_overflow",
    "logic_or_spec_gap",
    "hard_blocker",
}

RESULT_KINDS = {"retry", "progress", "done", "blocked"}

SAFE_PKG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._@+\-/]{0,120}$")
def _resolve_default_skill_runtime_root() -> Path:
    env = os.environ.get("CODEX_SKILL_RUNTIME_ROOT", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return (Path.home() / "Codex_Skill_Runtime").resolve()


DEFAULT_CODEX_SKILL_RUNTIME_ROOT = _resolve_default_skill_runtime_root()
SKILL_RUNTIME_ID = "openclaw-relentless-execution"


def get_background_worker_profile() -> dict[str, dict[str, int]]:
    return {
        "guardrails": DEFAULT_BACKGROUND_WORKER_GUARDRAILS.copy(),
        "budgets": DEFAULT_BACKGROUND_WORKER_BUDGETS.copy(),
    }


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_iso_z(ts: str) -> datetime:
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def cut(text: str, limit: int = MAX_LOG_CHARS) -> str:
    t = text or ""
    if len(t) <= limit:
        return t
    return t[: limit - 1] + "\u2026"


def first_line(text: str) -> str:
    for line in (text or "").splitlines():
        line = norm(line)
        if line:
            return line
    return ""


def _skill_runtime_layout() -> dict[str, Path]:
    root = (DEFAULT_CODEX_SKILL_RUNTIME_ROOT / SKILL_RUNTIME_ID).resolve()
    layout = {
        "root": root,
        "logs": root / "logs",
        "tmp": root / "tmp",
        "artifacts": root / "artifacts",
    }
    for path in layout.values():
        path.mkdir(parents=True, exist_ok=True)
    return layout


def default_root() -> Path:
    return _skill_runtime_layout()["artifacts"] / "state"


def default_memory_runtime_path() -> Path | None:
    raw = os.environ.get("OPENCLAW_HOOK_RUNTIME", "").strip()
    if not raw:
        return None
    return Path(raw).expanduser().resolve()


def _resolve_memory_runtime(raw: str | None) -> tuple[Path | None, bool]:
    configured = str(raw or "").strip()
    if configured:
        return Path(configured).expanduser().resolve(), True
    return default_memory_runtime_path(), False


def _skipped_hook_payload(reason: str) -> dict[str, Any]:
    return {
        "status": "skipped",
        "reason": reason,
    }


def has_bin(name: str) -> bool:
    return shutil.which(name) is not None


def state_path(root: Path, goal_id: str) -> Path:
    return root / f"{goal_id}.json"


def ensure_state_shape(data: dict[str, Any]) -> dict[str, Any]:
    # Backward compatibility for v1 files.
    if not isinstance(data.get("version"), int):
        data["version"] = 1
    if data["version"] < STATE_VERSION:
        data["done_criteria"] = data.get("done_criteria") or data.get("done") or ""
        data.pop("done", None)
        data.setdefault("constraints", [])
        data.setdefault("guardrails", DEFAULT_GUARDRAILS.copy())
        budgets = DEFAULT_BUDGETS.copy()
        existing_budgets = data.get("budgets_remaining")
        if isinstance(existing_budgets, dict):
            for k, v in existing_budgets.items():
                if k in budgets and isinstance(v, int):
                    budgets[k] = v
        data["budgets_remaining"] = budgets
        data.setdefault(
            "stats",
            {
                "total_attempts": len(data.get("history", [])),
                "no_progress_streak": 0,
                "repeated_failure_streak": 0,
                "last_failure_signature": "",
            },
        )
        data.setdefault(
            "hooks",
            {
                "before_agent_start": None,
                "agent_end": None,
                "pre_compaction_flush": None,
            },
        )
        data.setdefault("history", data.get("attempts", []))
        data.pop("attempts", None)
        data["version"] = STATE_VERSION

    # Normalization for current shape.
    data.setdefault("constraints", [])
    data.setdefault("guardrails", DEFAULT_GUARDRAILS.copy())
    data.setdefault("budgets_remaining", DEFAULT_BUDGETS.copy())
    data.setdefault(
        "stats",
        {
            "total_attempts": 0,
            "no_progress_streak": 0,
            "repeated_failure_streak": 0,
            "last_failure_signature": "",
        },
    )
    data.setdefault(
        "hooks",
        {
            "before_agent_start": None,
            "agent_end": None,
            "pre_compaction_flush": None,
        },
    )
    data.setdefault("history", [])
    data.setdefault("status", "in_progress")
    data.setdefault("done_criteria", "")

    # Fill missing keys defensively.
    for k, v in DEFAULT_BUDGETS.items():
        data["budgets_remaining"].setdefault(k, v)
    for k, v in DEFAULT_GUARDRAILS.items():
        data["guardrails"].setdefault(k, v)
    for k in ["total_attempts", "no_progress_streak", "repeated_failure_streak", "last_failure_signature"]:
        data["stats"].setdefault(k, 0 if k != "last_failure_signature" else "")

    return data


def load_state(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("state file is not an object")
    return ensure_state_shape(data)


def save_state(path: Path, data: dict[str, Any]) -> None:
    data["updated_at"] = utc_now()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def classify_failure(stderr: str, stdout: str, *, timed_out: bool = False) -> str:
    text = f"{stderr}\n{stdout}".lower()
    if timed_out:
        return "transient_runtime"
    if re.search(r"context (length|window)|token limit|too many tokens|max context", text):
        return "context_overflow"
    if re.search(r"command not found|not recognized as an internal or external command", text):
        return "dependency_missing"
    if re.search(r"modulenotfounderror|no module named|cannot find module|package .* not found", text):
        return "dependency_missing"
    if re.search(r"temporary failure|temporarily unavailable|connection reset|econn|timed out|timeout|rate limit|429|503", text):
        return "transient_runtime"
    if re.search(r"permission denied|operation not permitted|authentication failed|forbidden|unauthorized|sudo: a password is required", text):
        return "hard_blocker"
    return "logic_or_spec_gap"


def extract_dependency(stderr: str, stdout: str) -> dict[str, str] | None:
    text = f"{stderr}\n{stdout}"

    # Python module
    m = re.search(r"No module named ['\"]([^'\"]+)['\"]", text)
    if m:
        return {"type": "python_module", "name": m.group(1)}

    # Node module
    m = re.search(r"Cannot find module ['\"]([^'\"]+)['\"]", text)
    if m:
        return {"type": "node_module", "name": m.group(1)}

    # Command not found forms
    m = re.search(r"command not found:?\s*([A-Za-z0-9._+\-]+)", text)
    if m:
        return {"type": "bin", "name": m.group(1)}
    m = re.search(r"'([A-Za-z0-9._+\-]+)' is not recognized as an internal or external command", text)
    if m:
        return {"type": "bin", "name": m.group(1)}

    return None


def run_shell(command: str, *, workdir: Path, timeout_sec: int) -> dict[str, Any]:
    started = time.time()
    try:
        proc = subprocess.run(
            ["bash", "-lc", command],
            cwd=str(workdir),
            capture_output=True,
            text=True,
            timeout=max(1, timeout_sec),
            check=False,
        )
        return {
            "exit_code": int(proc.returncode),
            "stdout": cut(proc.stdout),
            "stderr": cut(proc.stderr),
            "timed_out": False,
            "duration_sec": round(time.time() - started, 3),
        }
    except subprocess.TimeoutExpired as err:
        out = ""
        err_text = ""
        if isinstance(err.stdout, str):
            out = err.stdout
        elif isinstance(err.stdout, bytes):
            out = err.stdout.decode("utf-8", errors="ignore")
        if isinstance(err.stderr, str):
            err_text = err.stderr
        elif isinstance(err.stderr, bytes):
            err_text = err.stderr.decode("utf-8", errors="ignore")
        return {
            "exit_code": 124,
            "stdout": cut(out),
            "stderr": cut(err_text),
            "timed_out": True,
            "duration_sec": round(time.time() - started, 3),
        }


def run_argv(argv: list[str], *, workdir: Path, timeout_sec: int, env: dict[str, str] | None = None) -> dict[str, Any]:
    started = time.time()
    try:
        proc = subprocess.run(
            argv,
            cwd=str(workdir),
            capture_output=True,
            text=True,
            timeout=max(1, timeout_sec),
            check=False,
            env=env,
        )
        return {
            "exit_code": int(proc.returncode),
            "stdout": cut(proc.stdout),
            "stderr": cut(proc.stderr),
            "timed_out": False,
            "duration_sec": round(time.time() - started, 3),
            "argv": argv,
        }
    except subprocess.TimeoutExpired as err:
        out = ""
        err_text = ""
        if isinstance(err.stdout, str):
            out = err.stdout
        elif isinstance(err.stdout, bytes):
            out = err.stdout.decode("utf-8", errors="ignore")
        if isinstance(err.stderr, str):
            err_text = err.stderr
        elif isinstance(err.stderr, bytes):
            err_text = err.stderr.decode("utf-8", errors="ignore")
        return {
            "exit_code": 124,
            "stdout": cut(out),
            "stderr": cut(err_text),
            "timed_out": True,
            "duration_sec": round(time.time() - started, 3),
            "argv": argv,
        }


def build_install_plan(dep: dict[str, str], *, workdir: Path) -> list[list[str]]:
    name = dep.get("name", "").strip()
    dep_type = dep.get("type", "")
    if not SAFE_PKG_RE.match(name):
        return []

    plans: list[list[str]] = []

    if dep_type == "python_module":
        if has_bin("uv"):
            plans.append(["uv", "pip", "install", name])
        if has_bin("pip3"):
            plans.append(["pip3", "install", name])
        elif has_bin("pip"):
            plans.append(["pip", "install", name])
        return plans

    if dep_type == "node_module":
        has_pkg = (workdir / "package.json").exists()
        if has_pkg:
            if has_bin("pnpm"):
                plans.append(["pnpm", "add", name])
            if has_bin("npm"):
                plans.append(["npm", "install", name])
        else:
            if has_bin("npm"):
                plans.append(["npm", "install", "-g", name])
        return plans

    if dep_type == "bin":
        if has_bin("brew"):
            plans.append(["brew", "install", name])
        if has_bin("apt-get"):
            if os.geteuid() == 0:
                plans.append(["apt-get", "install", "-y", name])
            elif has_bin("sudo"):
                plans.append(["sudo", "-n", "apt-get", "install", "-y", name])
        if has_bin("uv"):
            plans.append(["uv", "tool", "install", name])
        if has_bin("npm"):
            plans.append(["npm", "install", "-g", name])
        return plans

    return plans


def try_dependency_heal(dep: dict[str, str], *, workdir: Path, timeout_sec: int) -> dict[str, Any]:
    plans = build_install_plan(dep, workdir=workdir)
    attempts: list[dict[str, Any]] = []
    for argv in plans:
        res = run_argv(argv, workdir=workdir, timeout_sec=timeout_sec)
        attempts.append(res)
        if res["exit_code"] == 0:
            return {
                "attempted": True,
                "success": True,
                "dependency": dep,
                "installed_with": argv,
                "attempts": attempts,
            }
    return {
        "attempted": bool(plans),
        "success": False,
        "dependency": dep,
        "installed_with": None,
        "attempts": attempts,
    }


def evaluate_guard(state: dict[str, Any]) -> list[str]:
    guard = state.get("guardrails", {})
    stats = state.get("stats", {})
    reasons: list[str] = []

    if state.get("status") != "in_progress":
        reasons.append(f"goal status is {state.get('status')}")

    created_at = parse_iso_z(state["created_at"])
    elapsed_min = (datetime.now(timezone.utc) - created_at).total_seconds() / 60.0
    if elapsed_min > int(guard.get("max_runtime_minutes", DEFAULT_GUARDRAILS["max_runtime_minutes"])):
        reasons.append("max runtime exceeded")

    if int(stats.get("total_attempts", 0)) >= int(guard.get("max_total_attempts", DEFAULT_GUARDRAILS["max_total_attempts"])):
        reasons.append("max total attempts reached")

    if int(stats.get("no_progress_streak", 0)) >= int(guard.get("max_stagnation", DEFAULT_GUARDRAILS["max_stagnation"])):
        reasons.append("stagnation limit reached")

    if int(stats.get("repeated_failure_streak", 0)) >= int(guard.get("repeat_failure_limit", DEFAULT_GUARDRAILS["repeat_failure_limit"])):
        reasons.append("repeated failure limit reached")

    return reasons


def update_failure_streak(state: dict[str, Any], signature: str) -> None:
    stats = state["stats"]
    if stats.get("last_failure_signature") == signature:
        stats["repeated_failure_streak"] = int(stats.get("repeated_failure_streak", 0)) + 1
    else:
        stats["last_failure_signature"] = signature
        stats["repeated_failure_streak"] = 1


def reset_failure_streak(state: dict[str, Any]) -> None:
    stats = state["stats"]
    stats["last_failure_signature"] = ""
    stats["repeated_failure_streak"] = 0


def next_action_for(kind: str, *, blocked: bool = False) -> str:
    if blocked:
        return "stop and request user decision"
    mapping = {
        "dependency_missing": "install dependency and retry",
        "transient_runtime": "wait briefly and retry",
        "context_overflow": "split/shrink task and retry",
        "logic_or_spec_gap": "collect diagnostics and patch",
        "hard_blocker": "request explicit user permission/secret/decision",
        "progress": "continue with next concrete step",
    }
    return mapping.get(kind, "continue")


def append_event(state: dict[str, Any], event: dict[str, Any]) -> None:
    state.setdefault("history", [])
    event["seq"] = len(state["history"]) + 1
    state["history"].append(event)


def cmd_start(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve() if args.root else default_root()
    gid = args.id or f"goal_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    path = state_path(root, gid)

    if path.exists() and not args.force:
        print(json.dumps({"status": "error", "error": "goal exists", "id": gid}, ensure_ascii=False))
        return 1

    constraints = [norm(x) for x in (args.constraint or []) if norm(x)]
    now = utc_now()

    state = {
        "version": STATE_VERSION,
        "id": gid,
        "created_at": now,
        "updated_at": now,
        "objective": norm(args.objective),
        "done_criteria": norm(args.done),
        "status": "in_progress",
        "constraints": constraints,
        "guardrails": {
            "max_total_attempts": int(args.max_total_attempts),
            "max_runtime_minutes": int(args.max_runtime_minutes),
            "max_stagnation": int(args.max_stagnation),
            "repeat_failure_limit": int(args.repeat_failure_limit),
        },
        "budgets_remaining": {
            "dependency_missing": int(args.budget_dependency_missing),
            "transient_runtime": int(args.budget_transient_runtime),
            "context_overflow": int(args.budget_context_overflow),
            "logic_or_spec_gap": int(args.budget_logic_or_spec_gap),
            "hard_blocker": int(args.budget_hard_blocker),
        },
        "stats": {
            "total_attempts": 0,
            "no_progress_streak": 0,
            "repeated_failure_streak": 0,
            "last_failure_signature": "",
        },
        "hooks": {
            "before_agent_start": None,
            "agent_end": None,
            "pre_compaction_flush": None,
        },
        "history": [],
    }

    save_state(path, state)
    print(
        json.dumps(
            {
                "status": "ok",
                "action": "started",
                "id": gid,
                "path": str(path),
                "guardrails": state["guardrails"],
                "budgets_remaining": state["budgets_remaining"],
            },
            ensure_ascii=False,
        )
    )
    return 0


def cmd_before_hook(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve() if args.root else default_root()
    path = state_path(root, args.id)
    if not path.exists():
        print(json.dumps({"status": "error", "error": "goal not found", "id": args.id}, ensure_ascii=False))
        return 1

    state = load_state(path)
    memory_runtime, explicit_runtime = _resolve_memory_runtime(args.memory_runtime)
    if memory_runtime is None:
        payload = _skipped_hook_payload("external_hook_runtime_not_configured")
        state["hooks"]["before_agent_start"] = {
            "at": utc_now(),
            "prompt": norm(args.prompt),
            "result": payload,
        }
        save_state(path, state)
        print(json.dumps(payload, ensure_ascii=False))
        return 0
    if not memory_runtime.exists():
        payload = (
            {"status": "error", "error": f"memory_runtime not found: {memory_runtime}"}
            if explicit_runtime
            else _skipped_hook_payload("external_hook_runtime_not_found")
        )
        state["hooks"]["before_agent_start"] = {
            "at": utc_now(),
            "prompt": norm(args.prompt),
            "result": payload,
        }
        save_state(path, state)
        print(json.dumps(payload, ensure_ascii=False))
        return 1 if explicit_runtime else 0

    cmd = [
        "python3",
        str(memory_runtime),
        "before-agent-start",
        "--prompt",
        args.prompt,
        "--max-results",
        str(int(args.max_results)),
        "--min-score",
        str(float(args.min_score)),
    ]
    if args.include_sessions:
        cmd.append("--include-sessions")
    if args.sessions_dir:
        cmd.extend(["--sessions-dir", str(Path(args.sessions_dir).expanduser().resolve())])

    res = run_argv(cmd, workdir=Path.cwd(), timeout_sec=max(5, int(args.timeout_sec)))
    payload: dict[str, Any] = {}
    if res["exit_code"] == 0:
        try:
            payload = json.loads(res["stdout"])
        except Exception:
            payload = {"status": "error", "error": "invalid json from memory_runtime", "raw": res["stdout"]}
    else:
        payload = {"status": "error", "error": "memory_runtime failed", "stderr": res["stderr"], "stdout": res["stdout"]}

    state["hooks"]["before_agent_start"] = {
        "at": utc_now(),
        "prompt": norm(args.prompt),
        "result": payload,
    }
    save_state(path, state)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload.get("status") == "ok" else 1


def _messages_payload(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.messages_file:
        p = Path(args.messages_file).expanduser().resolve()
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, list):
            out = [row for row in data if isinstance(row, dict)]
            return out
        return []

    out: list[dict[str, Any]] = []
    if args.user_text and norm(args.user_text):
        out.append({"role": "user", "content": args.user_text})
    if args.assistant_text and norm(args.assistant_text):
        out.append({"role": "assistant", "content": args.assistant_text})
    return out


def cmd_after_hook(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve() if args.root else default_root()
    path = state_path(root, args.id)
    if not path.exists():
        print(json.dumps({"status": "error", "error": "goal not found", "id": args.id}, ensure_ascii=False))
        return 1

    state = load_state(path)
    memory_runtime, explicit_runtime = _resolve_memory_runtime(args.memory_runtime)
    if memory_runtime is None:
        payload = _skipped_hook_payload("external_hook_runtime_not_configured")
        state["hooks"]["agent_end"] = {
            "at": utc_now(),
            "result": payload,
        }
        save_state(path, state)
        print(json.dumps(payload, ensure_ascii=False))
        return 0
    if not memory_runtime.exists():
        payload = (
            {"status": "error", "error": f"memory_runtime not found: {memory_runtime}"}
            if explicit_runtime
            else _skipped_hook_payload("external_hook_runtime_not_found")
        )
        state["hooks"]["agent_end"] = {
            "at": utc_now(),
            "result": payload,
        }
        save_state(path, state)
        print(json.dumps(payload, ensure_ascii=False))
        return 1 if explicit_runtime else 0

    messages = _messages_payload(args)
    if not messages:
        print(json.dumps({"status": "error", "error": "messages are empty"}, ensure_ascii=False))
        return 1

    tmp_dir = _skill_runtime_layout()["tmp"] / "after_hook_payloads"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = (tmp_dir / f"messages-{int(time.time() * 1000)}-{os.getpid()}.json").resolve()
    tmp_path.write_text(json.dumps(messages, ensure_ascii=False), encoding="utf-8")

    cmd = [
        "python3",
        str(memory_runtime),
        "agent-end",
        "--session-id",
        args.session_id,
        "--messages-file",
        str(tmp_path),
        "--max-captures",
        str(int(args.max_captures)),
    ]
    res = run_argv(cmd, workdir=Path.cwd(), timeout_sec=max(5, int(args.timeout_sec)))
    try:
        tmp_path.unlink(missing_ok=True)
    except Exception:
        pass

    payload: dict[str, Any] = {}
    if res["exit_code"] == 0:
        try:
            payload = json.loads(res["stdout"])
        except Exception:
            payload = {"status": "error", "error": "invalid json from memory_runtime", "raw": res["stdout"]}
    else:
        payload = {"status": "error", "error": "memory_runtime failed", "stderr": res["stderr"], "stdout": res["stdout"]}

    state["hooks"]["agent_end"] = {
        "at": utc_now(),
        "result": payload,
    }
    save_state(path, state)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload.get("status") == "ok" else 1


def cmd_flush_hook(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve() if args.root else default_root()
    path = state_path(root, args.id)
    if not path.exists():
        print(json.dumps({"status": "error", "error": "goal not found", "id": args.id}, ensure_ascii=False))
        return 1

    state = load_state(path)
    memory_runtime, explicit_runtime = _resolve_memory_runtime(args.memory_runtime)
    if memory_runtime is None:
        payload = _skipped_hook_payload("external_hook_runtime_not_configured")
        state["hooks"]["pre_compaction_flush"] = {
            "at": utc_now(),
            "result": payload,
        }
        append_event(
            state,
            {
                "at": utc_now(),
                "type": "flush_hook",
                "result": payload.get("status", "skipped"),
            },
        )
        save_state(path, state)
        print(json.dumps(payload, ensure_ascii=False))
        return 0
    if not memory_runtime.exists():
        payload = (
            {"status": "error", "error": f"memory_runtime not found: {memory_runtime}"}
            if explicit_runtime
            else _skipped_hook_payload("external_hook_runtime_not_found")
        )
        state["hooks"]["pre_compaction_flush"] = {
            "at": utc_now(),
            "result": payload,
        }
        append_event(
            state,
            {
                "at": utc_now(),
                "type": "flush_hook",
                "result": payload.get("status", "error"),
            },
        )
        save_state(path, state)
        print(json.dumps(payload, ensure_ascii=False))
        return 1 if explicit_runtime else 0

    cmd = [
        "python3",
        str(memory_runtime),
        "pre-compaction-flush",
        "--session-id",
        args.session_id,
        "--category",
        args.category,
        "--content",
        args.content,
    ]
    res = run_argv(cmd, workdir=Path.cwd(), timeout_sec=max(5, int(args.timeout_sec)))
    payload: dict[str, Any] = {}
    ok = False
    if res["exit_code"] == 0:
        try:
            payload = json.loads(res["stdout"])
        except Exception:
            payload = {"status": "error", "error": "invalid json from memory_runtime", "raw": res["stdout"]}
        if isinstance(payload, dict):
            status = str(payload.get("status", "")).strip().lower()
            adapter = payload.get("memory_client_adapter_v1")
            service = payload.get("memory_service_response_v1")
            ok = status == "ok"
            if not ok and isinstance(adapter, dict):
                ok = bool(adapter.get("ok", False))
            if not ok and isinstance(service, dict):
                ok = str(service.get("status", "")).strip().lower() == "ok"
            if "status" not in payload:
                payload["status"] = "ok" if ok else "error"
    else:
        payload = {"status": "error", "error": "memory_runtime failed", "stderr": res["stderr"], "stdout": res["stdout"]}
        ok = False

    state["hooks"]["pre_compaction_flush"] = {
        "at": utc_now(),
        "result": payload,
    }
    append_event(
        state,
        {
            "at": utc_now(),
            "type": "flush_hook",
            "result": payload.get("status", "error"),
            "summary": norm(args.content),
        },
    )
    save_state(path, state)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if ok else 1


def cmd_attempt(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve() if args.root else default_root()
    path = state_path(root, args.id)
    if not path.exists():
        print(json.dumps({"status": "error", "error": "goal not found", "id": args.id}, ensure_ascii=False))
        return 1

    state = load_state(path)
    pre_guard = evaluate_guard(state)
    if pre_guard:
        state["status"] = "blocked"
        append_event(
            state,
            {
                "at": utc_now(),
                "type": "guard_block",
                "result": "blocked",
                "kind": "hard_blocker",
                "summary": "; ".join(pre_guard),
            },
        )
        save_state(path, state)
        out = {
            "status": "ok",
            "objective_status": "blocked",
            "blocked_reason": pre_guard,
            "next_action": "request user decision",
        }
        print(json.dumps(out, ensure_ascii=False))
        return 0

    workdir = Path(args.workdir).expanduser().resolve() if args.workdir else Path.cwd().resolve()
    timeout_sec = max(1, int(args.timeout_sec))
    verify_timeout = max(1, int(args.verify_timeout_sec))
    heal_timeout = max(1, int(args.heal_timeout_sec))

    state["stats"]["total_attempts"] = int(state["stats"].get("total_attempts", 0)) + 1
    attempt_no = state["stats"]["total_attempts"]

    run_res = run_shell(args.command, workdir=workdir, timeout_sec=timeout_sec)
    kind = "progress"
    result = "progress"
    summary = ""
    verify_res: dict[str, Any] | None = None
    heal_res: dict[str, Any] | None = None

    # Initial failure path.
    if run_res["exit_code"] != 0:
        kind = classify_failure(run_res["stderr"], run_res["stdout"], timed_out=run_res["timed_out"])
        summary = first_line(run_res["stderr"]) or first_line(run_res["stdout"]) or "command failed"

        if kind == "dependency_missing" and args.auto_heal:
            dep = extract_dependency(run_res["stderr"], run_res["stdout"])
            if dep:
                heal_res = try_dependency_heal(dep, workdir=workdir, timeout_sec=heal_timeout)
                if heal_res.get("success"):
                    rerun = run_shell(args.command, workdir=workdir, timeout_sec=timeout_sec)
                    run_res = rerun
                    if rerun["exit_code"] == 0:
                        kind = "progress"
                        summary = "dependency healed and command reran successfully"
                    else:
                        kind = classify_failure(rerun["stderr"], rerun["stdout"], timed_out=rerun["timed_out"])
                        summary = first_line(rerun["stderr"]) or first_line(rerun["stdout"]) or "command failed after heal"

    # Verify path.
    if run_res["exit_code"] == 0 and args.verify_command:
        verify_res = run_shell(args.verify_command, workdir=workdir, timeout_sec=verify_timeout)
        if verify_res["exit_code"] != 0:
            kind = classify_failure(verify_res["stderr"], verify_res["stdout"], timed_out=verify_res["timed_out"])
            if kind == "progress":
                kind = "logic_or_spec_gap"
            summary = first_line(verify_res["stderr"]) or first_line(verify_res["stdout"]) or "verify failed"

    if run_res["exit_code"] == 0 and (not verify_res or verify_res["exit_code"] == 0):
        if args.mark_done:
            result = "done"
            state["status"] = "done"
            summary = summary or "done criteria validated"
        else:
            result = "progress"
            summary = summary or "step succeeded"
        state["stats"]["no_progress_streak"] = 0
        reset_failure_streak(state)
    else:
        if kind not in FAILURE_KINDS:
            kind = "logic_or_spec_gap"
        result = "retry"

        state["stats"]["no_progress_streak"] = int(state["stats"].get("no_progress_streak", 0)) + 1
        signature = f"{kind}|{summary[:180]}"
        update_failure_streak(state, signature)

        remaining = int(state["budgets_remaining"].get(kind, 0)) - 1
        state["budgets_remaining"][kind] = remaining

        if remaining < 0:
            state["status"] = "blocked"
            result = "blocked"
            summary = f"retry budget exceeded for {kind}: {summary}"
        elif kind == "hard_blocker" and args.block_on_hard:
            state["status"] = "blocked"
            result = "blocked"

    event = {
        "at": utc_now(),
        "type": "attempt",
        "attempt_no": attempt_no,
        "result": result,
        "kind": kind,
        "command": args.command,
        "verify_command": args.verify_command,
        "summary": summary,
        "workdir": str(workdir),
        "run": run_res,
        "verify": verify_res,
        "heal": heal_res,
    }
    append_event(state, event)

    post_guard = evaluate_guard(state)
    if post_guard and state.get("status") == "in_progress":
        state["status"] = "blocked"
        append_event(
            state,
            {
                "at": utc_now(),
                "type": "guard_block",
                "result": "blocked",
                "kind": "hard_blocker",
                "summary": "; ".join(post_guard),
            },
        )

    save_state(path, state)

    objective_status = state.get("status", "in_progress")
    out = {
        "status": "ok",
        "id": state["id"],
        "objective_status": objective_status,
        "attempt_no": attempt_no,
        "result": result,
        "kind": kind,
        "summary": summary,
        "evidence": {
            "exit_code": run_res["exit_code"],
            "verify_exit_code": verify_res["exit_code"] if verify_res else None,
            "timed_out": run_res["timed_out"],
        },
        "budgets_remaining": state["budgets_remaining"],
        "stats": state["stats"],
        "next_action": next_action_for(kind, blocked=(objective_status == "blocked")),
        "path": str(path),
    }

    if post_guard:
        out["guardrail_reasons"] = post_guard

    print(json.dumps(out, ensure_ascii=False))
    return 0


def cmd_step(args: argparse.Namespace) -> int:
    # Compatibility manual logging mode.
    root = Path(args.root).expanduser().resolve() if args.root else default_root()
    path = state_path(root, args.id)
    if not path.exists():
        print(json.dumps({"status": "error", "error": "goal not found", "id": args.id}, ensure_ascii=False))
        return 1

    state = load_state(path)
    result = args.result
    kind = args.kind
    if result not in RESULT_KINDS:
        result = "retry"
    if kind not in FAILURE_KINDS and kind != "progress":
        kind = "logic_or_spec_gap"

    append_event(
        state,
        {
            "at": utc_now(),
            "type": "manual_step",
            "result": result,
            "kind": kind,
            "summary": norm(args.summary),
            "next": norm(args.next) if args.next else "",
            "evidence": norm(args.evidence) if args.evidence else "",
        },
    )

    if result == "done":
        state["status"] = "done"
        state["stats"]["no_progress_streak"] = 0
        reset_failure_streak(state)
    elif result == "blocked":
        state["status"] = "blocked"
    elif result == "progress":
        state["status"] = "in_progress"
        state["stats"]["no_progress_streak"] = 0
        reset_failure_streak(state)
    else:
        state["status"] = "in_progress"
        state["stats"]["no_progress_streak"] = int(state["stats"].get("no_progress_streak", 0)) + 1

    save_state(path, state)
    print(json.dumps({"status": "ok", "action": "manual_step_recorded", "id": args.id, "goal_status": state["status"]}, ensure_ascii=False))
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve() if args.root else default_root()
    path = state_path(root, args.id)
    if not path.exists():
        print(json.dumps({"status": "error", "error": "goal not found", "id": args.id}, ensure_ascii=False))
        return 1

    state = load_state(path)
    state["status"] = args.result
    append_event(
        state,
        {
            "at": utc_now(),
            "type": "complete",
            "result": args.result,
            "kind": "progress" if args.result == "done" else "hard_blocker",
            "summary": norm(args.summary),
            "evidence": norm(args.evidence) if args.evidence else "",
        },
    )
    save_state(path, state)
    print(json.dumps({"status": "ok", "id": args.id, "objective_status": state["status"], "path": str(path)}, ensure_ascii=False))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve() if args.root else default_root()
    path = state_path(root, args.id)
    if not path.exists():
        print(json.dumps({"status": "error", "error": "goal not found", "id": args.id}, ensure_ascii=False))
        return 1

    state = load_state(path)
    last = state["history"][-1] if state.get("history") else None
    guard_reasons = evaluate_guard(state)

    print(
        json.dumps(
            {
                "status": "ok",
                "id": state["id"],
                "objective_status": state["status"],
                "objective": state["objective"],
                "done_criteria": state.get("done_criteria", ""),
                "constraints": state.get("constraints", []),
                "guardrails": state.get("guardrails", {}),
                "budgets_remaining": state.get("budgets_remaining", {}),
                "stats": state.get("stats", {}),
                "attempt_count": len(state.get("history", [])),
                "latest_event": last,
                "guardrail_reasons": guard_reasons,
                "path": str(path),
            },
            ensure_ascii=False,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="OpenClaw-style relentless execution runtime with safety guardrails")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_start = sub.add_parser("start", help="Create a new objective run with guardrails and budgets.")
    p_start.add_argument("--id", default=None)
    p_start.add_argument("--objective", required=True)
    p_start.add_argument("--done", required=True)
    p_start.add_argument("--constraint", action="append", default=[])
    p_start.add_argument("--root", default=None)
    p_start.add_argument("--force", action="store_true")
    p_start.add_argument("--max-total-attempts", type=int, default=DEFAULT_GUARDRAILS["max_total_attempts"])
    p_start.add_argument("--max-runtime-minutes", type=int, default=DEFAULT_GUARDRAILS["max_runtime_minutes"])
    p_start.add_argument("--max-stagnation", type=int, default=DEFAULT_GUARDRAILS["max_stagnation"])
    p_start.add_argument("--repeat-failure-limit", type=int, default=DEFAULT_GUARDRAILS["repeat_failure_limit"])
    p_start.add_argument("--budget-dependency-missing", type=int, default=DEFAULT_BUDGETS["dependency_missing"])
    p_start.add_argument("--budget-transient-runtime", type=int, default=DEFAULT_BUDGETS["transient_runtime"])
    p_start.add_argument("--budget-context-overflow", type=int, default=DEFAULT_BUDGETS["context_overflow"])
    p_start.add_argument("--budget-logic-or-spec-gap", type=int, default=DEFAULT_BUDGETS["logic_or_spec_gap"])
    p_start.add_argument("--budget-hard-blocker", type=int, default=DEFAULT_BUDGETS["hard_blocker"])
    p_start.set_defaults(func=cmd_start)

    p_before = sub.add_parser("before-hook", help="Run optional external before hook and store result.")
    p_before.add_argument("--id", required=True)
    p_before.add_argument("--prompt", required=True)
    p_before.add_argument("--root", default=None)
    p_before.add_argument("--memory-runtime", default=None)
    p_before.add_argument("--include-sessions", action="store_true")
    p_before.add_argument("--sessions-dir", default=None)
    p_before.add_argument("--max-results", type=int, default=3)
    p_before.add_argument("--min-score", type=float, default=0.3)
    p_before.add_argument("--timeout-sec", type=int, default=20)
    p_before.set_defaults(func=cmd_before_hook)

    p_after = sub.add_parser("after-hook", help="Run optional external after hook and store result.")
    p_after.add_argument("--id", required=True)
    p_after.add_argument("--session-id", required=True)
    p_after.add_argument("--root", default=None)
    p_after.add_argument("--memory-runtime", default=None)
    p_after.add_argument("--messages-file", default=None)
    p_after.add_argument("--user-text", default="")
    p_after.add_argument("--assistant-text", default="")
    p_after.add_argument("--max-captures", type=int, default=3)
    p_after.add_argument("--timeout-sec", type=int, default=20)
    p_after.set_defaults(func=cmd_after_hook)

    p_flush = sub.add_parser("flush-hook", help="Run optional external flush hook and store result.")
    p_flush.add_argument("--id", required=True)
    p_flush.add_argument("--session-id", required=True)
    p_flush.add_argument("--content", required=True)
    p_flush.add_argument("--category", default="constraint")
    p_flush.add_argument("--root", default=None)
    p_flush.add_argument("--memory-runtime", default=None)
    p_flush.add_argument("--timeout-sec", type=int, default=20)
    p_flush.set_defaults(func=cmd_flush_hook)

    p_attempt = sub.add_parser("attempt", help="Execute one attempt with classification/healing/guardrails.")
    p_attempt.add_argument("--id", required=True)
    p_attempt.add_argument("--command", required=True)
    p_attempt.add_argument("--verify-command", default="")
    p_attempt.add_argument("--workdir", default=None)
    p_attempt.add_argument("--root", default=None)
    p_attempt.add_argument("--timeout-sec", type=int, default=180)
    p_attempt.add_argument("--verify-timeout-sec", type=int, default=120)
    p_attempt.add_argument("--auto-heal", action="store_true")
    p_attempt.add_argument("--heal-timeout-sec", type=int, default=300)
    p_attempt.add_argument("--mark-done", action="store_true")
    p_attempt.add_argument("--block-on-hard", action="store_true", default=True)
    p_attempt.set_defaults(func=cmd_attempt)

    p_step = sub.add_parser("step", help="Manual compatibility logging.")
    p_step.add_argument("--id", required=True)
    p_step.add_argument("--result", required=True, choices=sorted(RESULT_KINDS))
    p_step.add_argument("--kind", required=True)
    p_step.add_argument("--summary", required=True)
    p_step.add_argument("--next", default="")
    p_step.add_argument("--evidence", default="")
    p_step.add_argument("--root", default=None)
    p_step.set_defaults(func=cmd_step)

    p_complete = sub.add_parser("complete", help="Mark run done or blocked.")
    p_complete.add_argument("--id", required=True)
    p_complete.add_argument("--result", required=True, choices=["done", "blocked"])
    p_complete.add_argument("--summary", required=True)
    p_complete.add_argument("--evidence", default="")
    p_complete.add_argument("--root", default=None)
    p_complete.set_defaults(func=cmd_complete)

    p_status = sub.add_parser("status", help="Show run status.")
    p_status.add_argument("--id", required=True)
    p_status.add_argument("--root", default=None)
    p_status.set_defaults(func=cmd_status)

    return ap


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
