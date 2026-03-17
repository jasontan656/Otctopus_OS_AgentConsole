from __future__ import annotations

import json
import time
from pathlib import Path
from typing import cast

from runtime_types import JSONDict
from runtime_types import Worker


def load_result(worker: Worker, *, attempts: int = 10, sleep_seconds: float = 1.0) -> JSONDict:
    last_error: Exception | None = None
    for _ in range(attempts):
        if not worker.result_json_path.exists():
            last_error = RuntimeError(f"{worker.skill} missing result file: {worker.result_json_path}")
        else:
            try:
                data = json.loads(worker.result_json_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                last_error = exc
            else:
                if not isinstance(data, dict):
                    raise RuntimeError(f"{worker.skill} result file must contain a JSON object")
                return cast(JSONDict, data)
        time.sleep(sleep_seconds)
    if last_error is not None:
        raise last_error
    raise RuntimeError(f"{worker.skill} failed to load result file: {worker.result_json_path}")


def expected_exit_code(result: JSONDict, keyword: str) -> int | None:
    commands = result.get("verification_commands", [])
    if not isinstance(commands, list):
        return None
    for item in commands:
        exit_code: int | None = None
        if isinstance(item, dict):
            command = str(item.get("command", ""))
            value = item.get("exit_code")
            if isinstance(value, int):
                exit_code = value
        else:
            command = str(item)
        if keyword in command:
            if exit_code is not None:
                return exit_code
            evidence = result.get("verification_evidence", {})
            if isinstance(evidence, dict):
                pytest_evidence = evidence.get("pytest", {})
                if isinstance(pytest_evidence, dict):
                    value = pytest_evidence.get("exit_code")
                    if isinstance(value, int):
                        return value
    return None


def read_tail(path: Path) -> str:
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    if not lines:
        return ""
    tail = lines[-1]
    return tail if len(tail) <= 320 else f"{tail[:317]}..."


def log_has_turn_completed(path: Path) -> bool:
    return path.exists() and '"type":"turn.completed"' in path.read_text(encoding="utf-8", errors="ignore")


def worker_ready(worker: Worker) -> bool:
    if worker.exit_code_path.exists():
        return True
    if worker.result_json_path.exists() and worker.result_md_path.exists():
        return True
    return log_has_turn_completed(worker.log_path)
