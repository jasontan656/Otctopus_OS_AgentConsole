from __future__ import annotations

from pathlib import Path


DOMAIN_DESCRIPTIONS = {
    "common": "current container's abstract layer root; choose one abstract domain below",
    "architecture": "architecture abstraction scope for the current container",
    "stack": "technology stack abstraction scope for the current container",
    "naming": "naming rules abstraction scope for the current container",
    "contracts": "contract rules abstraction scope for the current container",
    "operations": "operations and maintenance abstraction scope for the current container",
}


def titleize(name: str) -> str:
    return name.replace("_", " ")


def describe_directory(path: Path, document_root: Path) -> str:
    rel = path.relative_to(document_root)
    parts = rel.parts
    if not parts:
        return "root navigation scope for Mother_Doc; choose the container documentation scope to enter"
    if len(parts) == 1:
        if parts[0] == "Mother_Doc":
            return "self-description container scope for the Mother_Doc container itself"
        return f"container documentation scope for `{parts[0]}`"
    if parts[-1] in DOMAIN_DESCRIPTIONS:
        return DOMAIN_DESCRIPTIONS[parts[-1]]
    if len(parts) >= 2 and parts[-2] == "common":
        return f"leaf abstract domain scope for `{parts[-1]}` under the current container"
    return f"nested documentation scope for `{parts[-1]}`"


def describe_leaf_file(path: Path, document_root: Path) -> str:
    rel = path.relative_to(document_root)
    if path.name == "README.md":
        return "peer purpose document for the current scope"
    if path.name == "agents.md":
        return "navigation index for the current scope"
    stem = path.stem
    parent = path.parent.name
    if parent in DOMAIN_DESCRIPTIONS:
        return f"`{titleize(stem)}` leaf rule file inside the `{parent}` abstract domain"
    return f"`{titleize(stem)}` leaf markdown file for the current scope"


def build_directory_readme(path: Path, document_root: Path) -> str:
    rel = path.relative_to(document_root)
    title = rel.name if rel.parts else "Mother_Doc"
    description = describe_directory(path, document_root)
    lines = [
        f"# {title}",
        "",
        description + ".",
        "",
        "- Use `agents.md` in the same directory as the navigation index for the next scope selection.",
        "- Keep this file focused on what the current scope is for, not on child-path enumeration.",
        "",
    ]
    return "\n".join(lines)


def build_agents_index(path: Path, document_root: Path) -> str:
    rel = path.relative_to(document_root)
    scope_label = str(rel) if rel.parts else "Mother_Doc"
    children = sorted(
        [child for child in path.iterdir() if child.name not in {"README.md", "agents.md", "__pycache__"}],
        key=lambda item: (item.is_file(), item.name.lower()),
    )
    lines = [
        "# agents",
        "",
        f"Current scope: `{scope_label}`.",
        f"Purpose: {describe_directory(path, document_root)}.",
        "",
        "## Peer",
        "",
        "- `README.md`",
        "  - status: present",
        "  - purpose: peer purpose document for the current scope",
        "",
        "## Index",
        "",
    ]
    if not children:
        lines.extend(
            [
                "- none",
                "  - status: terminal",
                "  - purpose: no deeper scope exists under the current directory",
            ]
        )
    else:
        for child in children:
            child_rel = child.relative_to(document_root)
            lines.append(f"- `{child_rel}`")
            lines.append("  - status: present")
            if child.is_dir():
                lines.append(f"  - purpose: {describe_directory(child, document_root)}")
            else:
                lines.append(f"  - purpose: {describe_leaf_file(child, document_root)}")
    lines.extend(
        [
            "",
            "## Selection Rule",
            "",
            "- Read the current `README.md` first to understand the current scope.",
            "- Then choose the next path from `## Index` according to the strengthened user intent.",
            "- Continue recursively until the full impact surface is covered.",
            "",
        ]
    )
    return "\n".join(lines)


def sync_navigation_tree(document_root: Path, *, dry_run: bool) -> dict[str, list[str]]:
    created_readmes: list[str] = []
    updated_agents: list[str] = []
    removed_legacy_indexes: list[str] = []

    legacy_indexes = sorted(document_root.rglob("00_INDEX.md"))
    for legacy in legacy_indexes:
        removed_legacy_indexes.append(str(legacy))
        if not dry_run:
            legacy.unlink()

    dirs = sorted([path for path in document_root.rglob("*") if path.is_dir()], key=lambda item: (len(item.parts), str(item)))
    dirs.insert(0, document_root)
    # remove duplicate root if present from rglob sequence
    seen: set[Path] = set()
    ordered_dirs: list[Path] = []
    for path in dirs:
        if path not in seen:
            seen.add(path)
            ordered_dirs.append(path)

    for directory in ordered_dirs:
        readme_path = directory / "README.md"
        if not readme_path.exists():
            created_readmes.append(str(readme_path))
            if not dry_run:
                readme_path.write_text(build_directory_readme(directory, document_root), encoding="utf-8")
        agents_path = directory / "agents.md"
        updated_agents.append(str(agents_path))
        if not dry_run:
            agents_path.write_text(build_agents_index(directory, document_root), encoding="utf-8")

    return {
        "created_readmes": created_readmes,
        "updated_agents": updated_agents,
        "removed_legacy_indexes": removed_legacy_indexes,
    }
