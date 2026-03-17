from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .catalog import REMOTE_PREFIXES, STAGE_ARTIFACTS, WORKSPACE_LAYOUT
from .types import CheckedFilesPayload, LintMessage


def _checked_files_payload(workspace_root: Path) -> CheckedFilesPayload:
    payload = {key: str((workspace_root / value).resolve()) for key, value in WORKSPACE_LAYOUT.items()}
    payload.update({f"artifact_{stage}": str((workspace_root / relative).resolve()) for stage, relative in STAGE_ARTIFACTS.items()})
    return payload  # type: ignore[return-value]


def _load_workspace(workspace_root: Path, errors: list[LintMessage]) -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for key, relative in WORKSPACE_LAYOUT.items():
        target = workspace_root / relative
        if not target.exists():
            _error(errors, "missing_file", relative, f"缺少必需对象文件：{relative}")
            continue
        try:
            payload = yaml.safe_load(target.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            _error(errors, "yaml_parse_error", relative, f"YAML 解析失败：{exc}")
            continue
        if not isinstance(payload, dict):
            _error(errors, "invalid_root_type", relative, "对象根节点必须是映射。")
            continue
        loaded[key] = payload
    return loaded


def _resolve_local_path(raw_path: str, workspace_root: Path) -> Path | None:
    if raw_path.startswith(REMOTE_PREFIXES):
        return None
    path = Path(raw_path)
    return (path if path.is_absolute() else workspace_root / path).resolve()


def _error(errors: list[LintMessage], code: str, source: str, message: str) -> None:
    errors.append({"code": code, "source": source, "message": message})


def _warning(warnings: list[LintMessage], code: str, source: str, message: str) -> None:
    warnings.append({"code": code, "source": source, "message": message})
