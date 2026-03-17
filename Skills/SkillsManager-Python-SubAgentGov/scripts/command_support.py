from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import cast

from runtime_types import DEFAULT_REPO_ROOT
from runtime_types import JSONDict


def run_cmd(
    cmd: list[str],
    *,
    check: bool = True,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd or DEFAULT_REPO_ROOT),
        text=True,
        capture_output=True,
        check=check,
    )


def run_json_cmd(cmd: list[str], *, cwd: Path | None = None) -> JSONDict:
    completed = run_cmd(cmd, cwd=cwd)
    try:
        data = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"failed to parse JSON from command: {' '.join(cmd)}\nstdout={completed.stdout}\nstderr={completed.stderr}"
        ) from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"command did not return a JSON object: {' '.join(cmd)}")
    return cast(JSONDict, data)


def tmux_exists(session_name: str) -> bool:
    if shutil.which("tmux") is None:
        return False
    proc = run_cmd(["tmux", "has-session", "-t", session_name], check=False)
    return proc.returncode == 0


def tmux_kill(session_name: str) -> None:
    if shutil.which("tmux") is None:
        return
    run_cmd(["tmux", "kill-session", "-t", session_name], check=False)
