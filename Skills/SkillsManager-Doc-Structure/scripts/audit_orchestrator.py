from __future__ import annotations

from pathlib import Path

from doc_models import CompilePayload, InspectPayload, LintPayload
from facade_linter import lint_facade
from profile_detector import detect_profile
from reference_graph import lint_references
from workflow_compiler import compile_context, lint_workflow


def inspect_target(target_root: Path) -> InspectPayload:
    profile = detect_profile(target_root)
    available_entries = ["routing", "policy", "runtime_contract", "tooling"]
    if profile.doc_topology == "workflow_path":
        available_entries = sorted({path.parent.name for path in (target_root / "path").rglob("00_*.md") if "steps" not in path.parts})
    return {
        "status": "ok",
        "target_root": str(target_root),
        "profile": profile.as_dict(),
        "root_entries": sorted(path.name for path in target_root.iterdir() if not path.name.startswith(".")),
        "available_context_entries": available_entries,
    }


def lint_target(target_root: Path) -> LintPayload:
    profile = detect_profile(target_root)
    issues = []
    issues.extend(lint_facade(target_root, profile))
    issues.extend(lint_references(target_root, profile))
    issues.extend(lint_workflow(target_root, profile))
    return {
        "status": "ok" if not issues else "error",
        "target_root": str(target_root),
        "profile": profile.as_dict(),
        "issues": [issue.as_dict() for issue in issues],
    }


def compile_target_context(target_root: Path, entry: str | None, selection: list[str]) -> CompilePayload:
    profile = detect_profile(target_root)
    payload = compile_context(target_root, profile, entry, selection)
    payload["target_root"] = str(target_root)
    payload["profile"] = profile.as_dict()
    return payload
