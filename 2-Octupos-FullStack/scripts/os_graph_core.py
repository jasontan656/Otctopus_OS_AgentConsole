from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


SKILL_ROOT = Path("/home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack")
BRIDGE_SKILL_ROOT = Path("/home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-code-graph-base")
ENGINE_ROOT = BRIDGE_SKILL_ROOT / "assets" / "gitnexus_core"
DIST_ENTRY = ENGINE_ROOT / "dist" / "cli" / "index.js"
GRAPH_ROOT = Path("/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/graph")
RUNTIME_ROOT = GRAPH_ROOT / "runtime"
DOC_ROOT = Path("/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/docs")
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
    "map",
    "wiki",
    "cypher",
}


def ensure_runtime_layout() -> list[str]:
    created: list[str] = []
    for relative in RUNTIME_DIRS:
        path = RUNTIME_ROOT / relative
        path.mkdir(parents=True, exist_ok=True)
        created.append(str(path))
    return created


def engine_ready_payload() -> dict[str, object]:
    return {
        "bridge_skill_root": str(BRIDGE_SKILL_ROOT),
        "engine_root": str(ENGINE_ROOT),
        "dist_entry": str(DIST_ENTRY),
        "dist_ready": DIST_ENTRY.exists(),
        "runtime_root": str(RUNTIME_ROOT),
    }


def engine_run(command: list[str], *, cwd: Path | None = None, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    if not DIST_ENTRY.exists():
        raise SystemExit(
            "OS_graph bridge engine is unavailable. Expected dist entry at "
            f"{DIST_ENTRY}. Keep Meta-code-graph-base assets available until vendoring lands."
        )
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


def status_payload() -> dict[str, object]:
    ensure_runtime_layout()
    return {
        **engine_ready_payload(),
        "graph_root": str(GRAPH_ROOT),
        "document_root": str(DOC_ROOT),
        "runtime_dirs": [str(RUNTIME_ROOT / item) for item in RUNTIME_DIRS],
        "document_nodes_ready": (RUNTIME_ROOT / "registry" / "document_nodes.json").exists(),
        "evidence_nodes_ready": (RUNTIME_ROOT / "registry" / "evidence_nodes.json").exists(),
    }
