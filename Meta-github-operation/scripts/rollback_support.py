from __future__ import annotations

from pathlib import Path


def path_exists_in_ref(run_git, repo_root: Path, to_ref: str, raw_path: str) -> bool:
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
