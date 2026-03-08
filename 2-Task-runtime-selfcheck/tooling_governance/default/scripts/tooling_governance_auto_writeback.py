#!/usr/bin/env python3
"""Auto-run governed writeback for changed paths by mapping them to tool_id."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import subprocess
from typing import Any

import mstg_yaml as yaml

EXCLUDED_PATH_SUFFIX = {
    "governance_instance/self/runtime/TOOL_CHANGE_LEDGER.jsonl",
    "governance_instance/self/runtime/TOOLING_GOVERNANCE_STATE.yaml",
}


def load_yaml(path: Path) -> Any:
    if not path.is_file():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def run_cmd(cmd: list[str], *, cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)
    return proc.returncode, (proc.stdout or "").strip(), (proc.stderr or "")[-1500:]


def run_json_cmd(cmd: list[str], *, cwd: Path) -> tuple[int, dict[str, Any], str]:
    code, stdout, stderr = run_cmd(cmd, cwd=cwd)
    payload: dict[str, Any]
    try:
        payload = json.loads(stdout) if stdout else {}
        if not isinstance(payload, dict):
            payload = {"raw_stdout": stdout}
    except Exception:
        payload = {"raw_stdout": stdout}
    return code, payload, stderr


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def infer_target_skill_dir(instance_root: Path) -> Path:
    if len(instance_root.parents) < 2:
        return instance_root
    parent_name = instance_root.parent.name
    if parent_name in {"tooling_governance", "governance_instance"}:
        return instance_root.parents[1]
    return instance_root.parents[1]


def git_repo_root(target_skill_dir: Path) -> Path:
    code, out, _ = run_cmd(["git", "-C", str(target_skill_dir), "rev-parse", "--show-toplevel"], cwd=target_skill_dir)
    if code == 0 and out.strip():
        return Path(out.strip()).resolve()
    return target_skill_dir


def normalize_path(token: str, *, target_skill_dir: Path) -> str:
    raw = str(token).strip().replace("\\", "/")
    while raw.startswith("./"):
        raw = raw[2:]
    if not raw:
        return ""

    p = Path(raw)
    if p.is_absolute():
        try:
            return p.resolve().relative_to(target_skill_dir).as_posix()
        except Exception:
            return p.as_posix()

    prefix = f"{target_skill_dir.name}/"
    if raw.startswith(prefix):
        raw = raw[len(prefix) :]

    return raw


def load_last_ledger_ts(instance_root: Path) -> str:
    ledger = instance_root / "runtime" / "TOOL_CHANGE_LEDGER.jsonl"
    if not ledger.is_file():
        return ""
    last = ""
    for line in ledger.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw:
            continue
        try:
            row = json.loads(raw)
        except Exception:
            continue
        if isinstance(row, dict):
            ts = str(row.get("timestamp_utc", "")).strip()
            if ts:
                last = ts
    return last


def collect_changed_paths(
    *,
    instance_root: Path,
    target_skill_dir: Path,
    repo_root: Path,
    cli_paths: list[str],
    git_range: str,
    since_ledger: bool,
) -> tuple[list[str], str]:
    if cli_paths:
        rows = [normalize_path(p, target_skill_dir=target_skill_dir) for p in cli_paths]
        return sorted(set([r for r in rows if r])), "cli"

    if git_range.strip():
        code, out, _ = run_cmd(
            ["git", "-C", str(repo_root), "diff", "--name-only", git_range.strip(), "--", str(target_skill_dir)],
            cwd=target_skill_dir,
        )
        if code != 0:
            return [], "git_range_failed"
        rows = [normalize_path(line, target_skill_dir=target_skill_dir) for line in out.splitlines() if line.strip()]
        return sorted(set([r for r in rows if r])), "git_range"

    if since_ledger:
        since_ts = load_last_ledger_ts(instance_root=instance_root)
        if not since_ts:
            return [], "since_ledger_no_timestamp"
        code, out, _ = run_cmd(
            [
                "git",
                "-C",
                str(repo_root),
                "log",
                f"--since={since_ts}",
                "--name-only",
                "--pretty=format:",
                "--",
                str(target_skill_dir),
            ],
            cwd=target_skill_dir,
        )
        if code != 0:
            return [], "since_ledger_git_log_failed"
        rows = [normalize_path(line, target_skill_dir=target_skill_dir) for line in out.splitlines() if line.strip()]
        return sorted(set([r for r in rows if r])), "since_ledger"

    code, out, _ = run_cmd(["git", "-C", str(repo_root), "diff", "--name-only", "--", str(target_skill_dir)], cwd=target_skill_dir)
    if code != 0:
        return [], "git_working_tree_failed"
    rows = [normalize_path(line, target_skill_dir=target_skill_dir) for line in out.splitlines() if line.strip()]
    return sorted(set([r for r in rows if r])), "working_tree"


def load_registry_map(instance_root: Path) -> tuple[dict[str, str], set[str]]:
    reg_path = instance_root / "runtime" / "TOOL_REGISTRY.yaml"
    payload = load_yaml(reg_path)
    entrypoint_to_tool: dict[str, str] = {}
    tool_ids: set[str] = set()
    if not isinstance(payload, dict):
        return entrypoint_to_tool, tool_ids

    tools = payload.get("tools")
    if not isinstance(tools, list):
        return entrypoint_to_tool, tool_ids

    for row in tools:
        if not isinstance(row, dict):
            continue
        tid = str(row.get("tool_id", "")).strip()
        ep = str(row.get("entrypoint", "")).strip().replace("\\", "/")
        if tid:
            tool_ids.add(tid)
        if tid and ep:
            entrypoint_to_tool[ep] = tid

    return entrypoint_to_tool, tool_ids


def pick_default_tool(tool_ids: set[str]) -> str:
    if "tooling_governance_apply_change" in tool_ids:
        return "tooling_governance_apply_change"
    if "mstg_l0_l13_linear_writeback" in tool_ids:
        return "mstg_l0_l13_linear_writeback"
    return sorted(tool_ids)[0] if tool_ids else "tooling_governance_apply_change"


def map_path_to_tool_id(path: str, *, entrypoint_to_tool: dict[str, str], tool_ids: set[str], default_tool: str) -> str:
    rel = path.replace("\\", "/")

    if rel in entrypoint_to_tool:
        return entrypoint_to_tool[rel]

    if rel.startswith("scripts/"):
        stem = Path(rel).stem
        if stem in tool_ids:
            return stem

        if "audit" in stem and "mstg_target_skill_audit" in tool_ids:
            return "mstg_target_skill_audit"
        if "plan" in stem and "mstg_governance_plan_manager" in tool_ids:
            return "mstg_governance_plan_manager"
        if "writeback" in stem and "mstg_l0_l13_linear_writeback" in tool_ids:
            return "mstg_l0_l13_linear_writeback"
        if "lint" in stem and "tooling_governance_lint" in tool_ids:
            return "tooling_governance_lint"

    if rel.startswith("governance_instance/self/docs/") or rel.startswith("references/") or rel == "SKILL.md":
        if "mstg_l0_l13_linear_writeback" in tool_ids:
            return "mstg_l0_l13_linear_writeback"

    return default_tool


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto writeback docs/ledger/gate for changed paths")
    parser.add_argument("--instance-root", required=True)
    parser.add_argument("--changed-path", action="append", default=[])
    parser.add_argument("--git-range", default="")
    parser.add_argument("--since-ledger", action="store_true")
    parser.add_argument("--summary-prefix", default="auto_writeback")
    parser.add_argument("--author", default="ai_maintained")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    instance_root = Path(args.instance_root).expanduser().resolve()
    if not instance_root.is_dir():
        out = {
            "status": "FAIL",
            "error": "INSTANCE_ROOT_NOT_FOUND",
            "instance_root": str(instance_root),
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1

    target_skill_dir = infer_target_skill_dir(instance_root)
    scripts_dir = Path(__file__).resolve().parent
    apply_change_script = scripts_dir / "tooling_governance_apply_change.py"
    if not apply_change_script.is_file():
        out = {
            "status": "FAIL",
            "error": "APPLY_CHANGE_SCRIPT_NOT_FOUND",
            "path": str(apply_change_script),
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1

    repo_root = git_repo_root(target_skill_dir)
    raw_paths, source_mode = collect_changed_paths(
        instance_root=instance_root,
        target_skill_dir=target_skill_dir,
        repo_root=repo_root,
        cli_paths=args.changed_path,
        git_range=args.git_range,
        since_ledger=args.since_ledger,
    )

    changed_paths: list[str] = []
    for p in raw_paths:
        if not p:
            continue
        if p in EXCLUDED_PATH_SUFFIX:
            continue
        changed_paths.append(p)
    changed_paths = sorted(set(changed_paths))

    entrypoint_to_tool, tool_ids = load_registry_map(instance_root)
    default_tool = pick_default_tool(tool_ids)

    if not changed_paths:
        out = {
            "status": "PASS",
            "message": "no_changed_paths_detected",
            "timestamp_utc": now_utc(),
            "instance_root": str(instance_root),
            "target_skill_dir": str(target_skill_dir),
            "source_mode": source_mode,
            "changed_paths": [],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2 if args.pretty else None))
        return 0

    grouped: dict[str, list[str]] = {}
    for path in changed_paths:
        tid = map_path_to_tool_id(path, entrypoint_to_tool=entrypoint_to_tool, tool_ids=tool_ids, default_tool=default_tool)
        grouped.setdefault(tid, []).append(path)

    runs: list[dict[str, Any]] = []
    all_ok = True
    for tid in sorted(grouped.keys()):
        paths = sorted(set(grouped[tid]))
        summary = f"{args.summary_prefix}: {tid} paths={len(paths)}"
        cmd = [
            "python3",
            str(apply_change_script),
            "--instance-root",
            str(instance_root),
            "--tool-id",
            tid,
            "--summary",
            summary,
            "--author",
            args.author,
        ]
        for path in paths:
            cmd.extend(["--changed-path", path])
        if args.dry_run:
            runs.append(
                {
                    "tool_id": tid,
                    "changed_paths": paths,
                    "command": cmd,
                    "exit_code": 0,
                    "ok": True,
                    "result": {"status": "SKIP", "reason": "dry_run_preview_only"},
                    "stderr_tail": "",
                }
            )
            continue

        code, payload, stderr = run_json_cmd(cmd, cwd=target_skill_dir)
        ok = code == 0 and str(payload.get("status", "")).upper() == "PASS"
        all_ok = all_ok and ok
        runs.append(
            {
                "tool_id": tid,
                "changed_paths": paths,
                "command": cmd,
                "exit_code": code,
                "ok": ok,
                "result": payload,
                "stderr_tail": stderr,
            }
        )

    out = {
        "status": "PASS" if all_ok else "FAIL",
        "timestamp_utc": now_utc(),
        "instance_root": str(instance_root),
        "target_skill_dir": str(target_skill_dir),
        "repo_root": str(repo_root),
        "source_mode": source_mode,
        "dry_run": args.dry_run,
        "changed_path_count": len(changed_paths),
        "changed_paths": changed_paths,
        "grouped_tool_count": len(grouped),
        "grouped_paths": grouped,
        "runs": runs,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
