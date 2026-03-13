from __future__ import annotations

import hashlib
import html
import json
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone


SKILL_ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = SKILL_ROOT / "assets" / "os_graph_engine" / "gitnexus_core"
DIST_ENTRY = ENGINE_ROOT / "dist" / "cli" / "index.js"


def _resolve_product_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "Otctopus_OS_AgentConsole"), None)
    if repo_root is None:
        raise RuntimeError("cannot resolve product root from Disabled-Octupos-FullStack script path")
    return repo_root.parent


OCTOPUS_OS_ROOT = (_resolve_product_root() / "Octopus_OS").resolve()
GRAPH_ROOT = (OCTOPUS_OS_ROOT / "Mother_Doc" / "graph").resolve()
RUNTIME_ROOT = GRAPH_ROOT / "runtime"
DOC_ROOT = (OCTOPUS_OS_ROOT / "Mother_Doc" / "docs").resolve()
LOG_ROOT = DOC_ROOT / "Mother_Doc" / "common" / "development_logs"
RUNTIME_DIRS = (
    "registry",
    "indexes",
    "reports",
    "maps",
    "wiki",
    "snapshots",
    "frontend_views",
)
ENGINE_COMMANDS = {
    "analyze",
    "list",
    "clean",
    "query",
    "context",
    "impact",
    "detect-changes",
    "rename",
    "augment",
    "resource",
    "cypher",
}


def ensure_runtime_layout() -> list[str]:
    created: list[str] = []
    for relative in RUNTIME_DIRS:
        path = RUNTIME_ROOT / relative
        path.mkdir(parents=True, exist_ok=True)
        created.append(str(path))
    return created


def _run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=str(cwd), check=True)


def ensure_engine() -> None:
    node_modules = ENGINE_ROOT / "node_modules"
    if not node_modules.exists():
        _run(["npm", "install"], ENGINE_ROOT)
    if not DIST_ENTRY.exists():
        _run(["npm", "run", "build"], ENGINE_ROOT)


def engine_ready_summary() -> dict[str, object]:
    return {
        "engine_asset_root": str(ENGINE_ROOT),
        "engine_root": str(ENGINE_ROOT),
        "dist_entry": str(DIST_ENTRY),
        "node_modules_ready": (ENGINE_ROOT / "node_modules").exists(),
        "dist_ready": DIST_ENTRY.exists(),
        "runtime_root": str(RUNTIME_ROOT),
    }


def engine_run(command: list[str], *, cwd: Path | None = None, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    ensure_engine()
    ensure_runtime_layout()
    env = os.environ.copy()
    env["META_CODE_GRAPH_RUNTIME_ROOT"] = str(RUNTIME_ROOT)
    return subprocess.run(
        ["node", str(DIST_ENTRY), *command],
        cwd=str(cwd or Path.cwd()),
        env=env,
        text=True,
        capture_output=capture_output,
        check=True,
    )


def emit_subprocess(result: subprocess.CompletedProcess[str]) -> int:
    payload = result.stdout if result.stdout.strip() else result.stderr
    if payload:
        print(payload, end="" if payload.endswith("\n") else "\n")
    return result.returncode


def load_registry() -> list[dict[str, object]]:
    registry_path = RUNTIME_ROOT / "registry" / "registry.json"
    if not registry_path.exists():
        return []
    return json.loads(registry_path.read_text(encoding="utf-8"))


def repo_key(repo_path: str) -> str:
    resolved = str(Path(repo_path).resolve())
    base = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in Path(resolved).name) or "repo"
    if not base.endswith("_repo"):
        base = f"{base}_repo"
    digest = hashlib.sha1(resolved.encode("utf-8")).hexdigest()[:12]
    return f"{base}-{digest}"


def _contract_marked_markdown(*, contract_name: str, body: str) -> str:
    return (
        "## Contract Markers\n\n"
        f"contract_name: {contract_name}\n"
        "contract_version: v1\n"
        "validation_mode: placeholder\n"
        "required_fields:\n"
        "- runtime_source\n"
        "optional_fields:\n"
        "- graph_layer\n\n"
        f"{body.rstrip()}\n"
    )


def resolve_repo(user_value: str | None) -> dict[str, object]:
    registry = load_registry()
    if not registry:
        raise SystemExit("OS_graph: no indexed repositories found. Run analyze first.")

    if user_value:
        candidate_path = Path(user_value).resolve()
        for entry in registry:
            if Path(str(entry["path"])).resolve() == candidate_path or entry["name"] == user_value:
                return entry
        raise SystemExit(f'OS_graph: repository "{user_value}" not found in registry.')

    cwd = Path.cwd().resolve()
    best: dict[str, object] | None = None
    for entry in registry:
        repo_path = Path(str(entry["path"])).resolve()
        if cwd == repo_path or repo_path in cwd.parents:
            if best is None or len(str(repo_path)) > len(str(Path(str(best["path"])).resolve())):
                best = entry
    if best:
        return best

    raise SystemExit("OS_graph: current directory is not inside an indexed repository.")


def _layer_for(rel_path: Path) -> str:
    parts = rel_path.parts
    name = rel_path.name
    if name == "AGENTS.md":
        return "contract_layer"
    if "development_logs" in parts:
        return "evidence_layer"
    if "shared" in parts:
        return "contract_layer"
    if "common" in parts:
        return "implementation_layer"
    return "narrative_layer"


def _kind_for(rel_path: Path) -> str:
    name = rel_path.name
    parent = rel_path.parent.name if rel_path.parent != Path(".") else ""
    if name == "README.md":
        return "readme"
    if name == "AGENTS.md":
        return "agents_index"
    if name == f"{parent}.md":
        return "scope_entity"
    if parent in {"overview", "features", "shared"}:
        return parent[:-1] if parent.endswith("s") else parent
    if "development_logs" in rel_path.parts:
        return "evidence_log"
    return "markdown_leaf"


def _markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def _doc_nodes() -> list[dict[str, object]]:
    nodes: list[dict[str, object]] = []
    for path in _markdown_files(DOC_ROOT):
        rel_path = path.relative_to(DOC_ROOT)
        nodes.append(
            {
                "node_id": rel_path.as_posix(),
                "node_type": _kind_for(rel_path),
                "layer": _layer_for(rel_path),
                "container": rel_path.parts[0] if rel_path.parts else "root",
                "title": path.stem,
                "path": rel_path.as_posix(),
            }
        )
    return nodes


def _doc_edges(nodes: list[dict[str, object]]) -> list[dict[str, str]]:
    known = {node["path"] for node in nodes}
    edges: list[dict[str, str]] = []
    for node in nodes:
        rel_path = Path(str(node["path"]))
        parent_readme = (rel_path.parent / "README.md").as_posix() if rel_path.parent != Path(".") else None
        if parent_readme and parent_readme in known and parent_readme != node["path"]:
            edges.append({"from": parent_readme, "to": str(node["path"]), "edge_type": "contains"})
    return edges


def _write_json(relative: str, payload: object) -> str:
    target = RUNTIME_ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(target)


def write_map(repo_value: str | None, *, emit: bool = True) -> dict[str, object]:
    repo = resolve_repo(repo_value)
    key = repo_key(str(repo["path"]))
    map_dir = RUNTIME_ROOT / "maps" / key
    map_dir.mkdir(parents=True, exist_ok=True)

    resources = {
        "graph_context.md": f'codegraph://repo/{repo["name"]}/context',
        "clusters.md": f'codegraph://repo/{repo["name"]}/clusters',
        "processes.md": f'codegraph://repo/{repo["name"]}/processes',
        "schema.md": f'codegraph://repo/{repo["name"]}/schema',
    }

    written: list[str] = []
    for filename, uri in resources.items():
        result = engine_run(["resource", uri], cwd=Path(str(repo["path"])), capture_output=True)
        target = map_dir / filename
        payload = result.stdout if result.stdout.strip() else result.stderr
        contract_name = f"os_graph_map_{Path(filename).stem}"
        target.write_text(_contract_marked_markdown(contract_name=contract_name, body=payload), encoding="utf-8")
        written.append(str(target))

    manifest = {
        "repo_name": repo["name"],
        "repo_path": str(Path(str(repo["path"])).resolve()),
        "repo_key": key,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": [Path(path).name for path in written],
    }
    manifest_path = map_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    payload = {"status": "success", "map_dir": str(map_dir), "files": written + [str(manifest_path)]}
    if emit:
        print(json.dumps(payload, indent=2))
    return payload


def write_wiki(repo_value: str | None, *, emit: bool = True) -> dict[str, object]:
    repo = resolve_repo(repo_value)
    key = repo_key(str(repo["path"]))
    map_dir = RUNTIME_ROOT / "maps" / key
    if not map_dir.exists():
        write_map(str(repo["name"]), emit=False)

    wiki_dir = RUNTIME_ROOT / "wiki" / key
    wiki_dir.mkdir(parents=True, exist_ok=True)

    source_files = {
        "overview.md": map_dir / "graph_context.md",
        "clusters.md": map_dir / "clusters.md",
        "processes.md": map_dir / "processes.md",
        "schema.md": map_dir / "schema.md",
    }

    copied: list[str] = []
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
        "repo_path": str(Path(str(repo["path"])).resolve()),
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
  <title>{html.escape(str(repo["name"]))} Local Wiki</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 32px; color: #1f2937; }}
    a {{ color: #2563eb; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    code, pre {{ background: #f3f4f6; }}
    pre {{ padding: 16px; border-radius: 8px; overflow-x: auto; }}
  </style>
</head>
<body>
  <h1>{html.escape(str(repo["name"]))} Local Wiki</h1>
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

    payload = {"status": "success", "wiki_dir": str(wiki_dir), "pages": copied + [str(wiki_dir / "index.html")]}
    if emit:
        print(json.dumps(payload, indent=2))
    return payload


def sync_doc_bindings() -> dict[str, object]:
    ensure_runtime_layout()
    nodes = _doc_nodes()
    edges = _doc_edges(nodes)
    by_container: dict[str, dict[str, list[dict[str, object]]]] = {}
    for node in nodes:
        container = str(node["container"])
        by_container.setdefault(container, {}).setdefault(str(node["layer"]), []).append(node)
    written = [
        _write_json("registry/document_nodes.json", nodes),
        _write_json("indexes/document_edges.json", edges),
        _write_json("frontend_views/layered_documents.json", by_container),
        _write_json(
            "reports/document_sync_report.json",
            {
                "document_root": str(DOC_ROOT),
                "node_count": len(nodes),
                "edge_count": len(edges),
                "containers": sorted(by_container),
            },
        ),
    ]
    return {"written_files": written, "node_count": len(nodes), "edge_count": len(edges)}


def sync_evidence() -> dict[str, object]:
    ensure_runtime_layout()
    evidence_nodes: list[dict[str, str]] = []
    if LOG_ROOT.exists():
        for path in sorted(LOG_ROOT.glob("*.md")):
            if path.name in {"README.md", "AGENTS.md", "development_logs.md"}:
                continue
            evidence_nodes.append(
                {
                    "node_id": f"evidence::{path.stem}",
                    "node_type": "evidence_log",
                    "layer": "evidence_layer",
                    "path": str(path.relative_to(DOC_ROOT)),
                }
            )
    status_index: list[dict[str, str]] = []
    for path in _markdown_files(DOC_ROOT):
        text = path.read_text(encoding="utf-8")
        marker = next(
            (line.split(":", 1)[1].strip() for line in text.splitlines() if line.startswith("doc_lifecycle_state:")),
            "unknown",
        )
        status_index.append({"path": str(path.relative_to(DOC_ROOT)), "doc_lifecycle_state": marker})
    written = [
        _write_json("registry/evidence_nodes.json", evidence_nodes),
        _write_json("indexes/status_index.json", status_index),
        _write_json("frontend_views/evidence_timeline.json", evidence_nodes),
        _write_json(
            "reports/evidence_sync_report.json",
            {"log_root": str(LOG_ROOT), "evidence_node_count": len(evidence_nodes), "status_doc_count": len(status_index)},
        ),
    ]
    return {"written_files": written, "evidence_node_count": len(evidence_nodes), "status_doc_count": len(status_index)}


def status_summary() -> dict[str, object]:
    ensure_runtime_layout()
    return {
        **engine_ready_summary(),
        "graph_root": str(GRAPH_ROOT),
        "document_root": str(DOC_ROOT),
        "runtime_dirs": [str(RUNTIME_ROOT / item) for item in RUNTIME_DIRS],
        "document_nodes_ready": (RUNTIME_ROOT / "registry" / "document_nodes.json").exists(),
        "evidence_nodes_ready": (RUNTIME_ROOT / "registry" / "evidence_nodes.json").exists(),
    }
