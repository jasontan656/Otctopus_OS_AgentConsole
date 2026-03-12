#!/usr/bin/env python3
import hashlib
import html
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = SKILL_ROOT / "assets" / "gitnexus_core"
REPO_ROOT = SKILL_ROOT.parents[1]
PRODUCT_ROOT = REPO_ROOT.parent
RUNTIME_ROOT = (PRODUCT_ROOT / "OctuposOS_Runtime_Backend" / "code_graph_runtime").resolve()
DIST_ENTRY = ENGINE_ROOT / "dist" / "cli" / "index.js"


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=str(cwd), check=True)


def ensure_engine() -> None:
    node_modules = ENGINE_ROOT / "node_modules"
    if not node_modules.exists():
        run(["npm", "install"], ENGINE_ROOT)
    if not DIST_ENTRY.exists():
        run(["npm", "run", "build"], ENGINE_ROOT)


def engine_run(args: list[str], cwd: Path | None = None, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["META_CODE_GRAPH_RUNTIME_ROOT"] = str(RUNTIME_ROOT)
    return subprocess.run(
        ["node", str(DIST_ENTRY), *args],
        cwd=str(cwd or Path.cwd()),
        env=env,
        text=True,
        capture_output=capture_output,
        check=True,
    )


def emit_result(result: subprocess.CompletedProcess[str]) -> int:
    payload = result.stdout if result.stdout.strip() else result.stderr
    if payload:
        sys.stdout.write(payload)
        if not payload.endswith("\n"):
            sys.stdout.write("\n")
    return result.returncode


def load_registry() -> list[dict]:
    registry_path = RUNTIME_ROOT / "registry" / "registry.json"
    if not registry_path.exists():
        return []
    return json.loads(registry_path.read_text(encoding="utf-8"))


def repo_key(repo_path: str) -> str:
    resolved = str(Path(repo_path).resolve())
    base = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in Path(resolved).name) or "repo"
    digest = hashlib.sha1(resolved.encode("utf-8")).hexdigest()[:12]
    return f"{base}-{digest}"


def resolve_repo(user_value: str | None) -> dict:
    registry = load_registry()
    if not registry:
        raise SystemExit("Meta-code-graph-base: no indexed repositories found. Run analyze first.")

    if user_value:
        candidate_path = Path(user_value).resolve()
        for entry in registry:
            if Path(entry["path"]).resolve() == candidate_path or entry["name"] == user_value:
                return entry
        raise SystemExit(f'Meta-code-graph-base: repository "{user_value}" not found in registry.')

    cwd = Path.cwd().resolve()
    best = None
    for entry in registry:
        repo_path = Path(entry["path"]).resolve()
        if cwd == repo_path or repo_path in cwd.parents:
            if best is None or len(str(repo_path)) > len(str(Path(best["path"]).resolve())):
                best = entry
    if best:
        return best

    raise SystemExit("Meta-code-graph-base: current directory is not inside an indexed repository.")


def write_map(repo_value: str | None, emit: bool = True) -> int:
    repo = resolve_repo(repo_value)
    key = repo_key(repo["path"])
    map_dir = RUNTIME_ROOT / "maps" / key
    map_dir.mkdir(parents=True, exist_ok=True)

    resources = {
        "repo_context.md": f'codegraph://repo/{repo["name"]}/context',
        "clusters.md": f'codegraph://repo/{repo["name"]}/clusters',
        "processes.md": f'codegraph://repo/{repo["name"]}/processes',
        "schema.md": f'codegraph://repo/{repo["name"]}/schema',
    }

    written = []
    for filename, uri in resources.items():
        result = engine_run(["resource", uri], cwd=Path(repo["path"]), capture_output=True)
        target = map_dir / filename
        payload = result.stdout if result.stdout.strip() else result.stderr
        target.write_text(payload, encoding="utf-8")
        written.append(str(target))

    manifest = {
        "repo_name": repo["name"],
        "repo_path": str(Path(repo["path"]).resolve()),
        "repo_key": key,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": [Path(path).name for path in written],
    }
    manifest_path = map_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if emit:
        print(json.dumps({"status": "success", "map_dir": str(map_dir), "files": written + [str(manifest_path)]}, indent=2))
    return 0


def write_wiki(repo_value: str | None) -> int:
    repo = resolve_repo(repo_value)
    key = repo_key(repo["path"])
    map_dir = RUNTIME_ROOT / "maps" / key
    if not map_dir.exists():
        write_map(repo["name"], emit=False)

    wiki_dir = RUNTIME_ROOT / "wiki" / key
    wiki_dir.mkdir(parents=True, exist_ok=True)

    source_files = {
        "overview.md": map_dir / "repo_context.md",
        "clusters.md": map_dir / "clusters.md",
        "processes.md": map_dir / "processes.md",
        "schema.md": map_dir / "schema.md",
    }

    copied = []
    for target_name, source_path in source_files.items():
        content = source_path.read_text(encoding="utf-8")
        target_path = wiki_dir / target_name
        if target_name == "overview.md":
            overview = (
                f"# {repo['name']} Local Wiki\n\n"
                "This wiki bundle is generated from local graph resources only.\n\n"
                "## Pages\n"
                "- [Overview](./overview.md)\n"
                "- [Clusters](./clusters.md)\n"
                "- [Processes](./processes.md)\n"
                "- [Schema](./schema.md)\n\n"
                "## Resource Snapshot\n\n"
                f"```\n{content.strip()}\n```\n"
            )
            target_path.write_text(overview, encoding="utf-8")
        else:
            target_path.write_text(content, encoding="utf-8")
        copied.append(str(target_path))

    meta = {
        "repo_name": repo["name"],
        "repo_path": str(Path(repo["path"]).resolve()),
        "repo_key": key,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "local-graph-resources",
        "pages": [Path(path).name for path in copied],
    }
    (wiki_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (wiki_dir / "module_tree.json").write_text(
        json.dumps(
            [
                {"name": "Overview", "slug": "overview", "files": ["overview.md"]},
                {"name": "Clusters", "slug": "clusters", "files": ["clusters.md"]},
                {"name": "Processes", "slug": "processes", "files": ["processes.md"]},
                {"name": "Schema", "slug": "schema", "files": ["schema.md"]},
            ],
            indent=2,
        ),
        encoding="utf-8",
    )

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(repo['name'])} Local Wiki</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 32px; color: #1f2937; }}
    a {{ color: #2563eb; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    code, pre {{ background: #f3f4f6; }}
    pre {{ padding: 16px; border-radius: 8px; overflow-x: auto; }}
  </style>
</head>
<body>
  <h1>{html.escape(repo['name'])} Local Wiki</h1>
  <p>Generated from local graph resources only.</p>
  <ul>
    <li><a href="./overview.md">Overview</a></li>
    <li><a href="./clusters.md">Clusters</a></li>
    <li><a href="./processes.md">Processes</a></li>
    <li><a href="./schema.md">Schema</a></li>
  </ul>
</body>
</html>
"""
    (wiki_dir / "index.html").write_text(index_html, encoding="utf-8")

    print(json.dumps({"status": "success", "wiki_dir": str(wiki_dir), "pages": copied + [str(wiki_dir / "index.html")]}, indent=2))
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: meta_code_graph_base.py <subcommand> [args...]", file=sys.stderr)
        return 1

    ensure_engine()
    if sys.argv[1] == "map":
        repo_arg = sys.argv[2] if len(sys.argv) > 2 else None
        return write_map(repo_arg)
    if sys.argv[1] == "wiki":
        if any(arg in {"-h", "--help"} for arg in sys.argv[2:]):
            print("Usage: meta_code_graph_base.py wiki [repo-name-or-path]\n\nGenerate a local wiki bundle from graph resource snapshots.")
            return 0
        repo_arg = sys.argv[2] if len(sys.argv) > 2 else None
        return write_wiki(repo_arg)
    structured_commands = {
        "list",
        "status",
        "query",
        "context",
        "impact",
        "detect-changes",
        "rename",
        "augment",
        "resource",
        "cypher",
    }
    if sys.argv[1] in structured_commands:
        result = engine_run(sys.argv[1:], cwd=Path.cwd(), capture_output=True)
        return emit_result(result)

    result = engine_run(sys.argv[1:], cwd=Path.cwd())
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
