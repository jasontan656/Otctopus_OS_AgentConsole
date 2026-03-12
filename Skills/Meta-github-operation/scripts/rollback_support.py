from __future__ import annotations

from pathlib import Path
from subprocess import CompletedProcess
from typing import Protocol


class GitRunner(Protocol):
    def __call__(self, repo_root: Path, *args: str, check: bool = True) -> CompletedProcess[str]:
        ...


def normalize_explicit_paths(repo_root: Path, raw_paths: list[str]) -> list[str]:
    if not raw_paths:
        raise ValueError("at least one --path is required")
    repo_resolved = repo_root.resolve()
    normalized: list[str] = []
    seen: set[str] = set()
    for raw_path in raw_paths:
        candidate = (repo_root / raw_path).resolve()
        if candidate != repo_resolved and repo_resolved not in candidate.parents:
            raise ValueError(f"path escapes repo root: {raw_path}")
        rel_path = candidate.relative_to(repo_root).as_posix() if candidate != repo_resolved else "."
        if rel_path in seen:
            continue
        seen.add(rel_path)
        normalized.append(rel_path)
    normalized.sort(key=lambda item: (len(Path(item).parts), item))
    collapsed: list[str] = []
    for rel_path in normalized:
        path_obj = Path(rel_path)
        if any(path_obj != Path(parent) and Path(parent) in path_obj.parents for parent in collapsed):
            continue
        collapsed.append(rel_path)
    return collapsed


def path_exists_in_ref(run_git: GitRunner, repo_root: Path, to_ref: str, raw_path: str) -> bool:
    completed = run_git(repo_root, "cat-file", "-e", f"{to_ref}:{raw_path}", check=False)
    return completed.returncode == 0


def remove_explicit_path(target: Path) -> None:
    if not target.exists():
        return
    if target.is_file() or target.is_symlink():
        target.unlink()
        return
    for child in sorted(target.iterdir(), key=lambda item: len(item.parts), reverse=True):
        remove_explicit_path(child)
    target.rmdir()


def prune_empty_path_ancestors(repo_root: Path, raw_path: str) -> list[str]:
    pruned: list[str] = []
    repo_resolved = repo_root.resolve()
    target = (repo_root / raw_path).resolve()
    if target != repo_resolved and repo_resolved not in target.parents:
        return pruned
    current = target if target.is_dir() else target.parent
    while current != repo_resolved:
        try:
            next(current.iterdir())
            break
        except StopIteration:
            current.rmdir()
            pruned.append(str(current.relative_to(repo_root)))
            current = current.parent
    return pruned
