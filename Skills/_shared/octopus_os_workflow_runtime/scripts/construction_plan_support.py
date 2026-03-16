from __future__ import annotations

import shutil
from pathlib import Path

from construction_plan_contract import GUIDANCE_MARKERS, PACK_DIR_PATTERN, PACK_MACHINE_FILES, PACK_MARKDOWN_FILES
from construction_plan_contract import PLAN_KIND_VALUES, ROOT_REQUIRED_FILES
from construction_plan_rendering import (
    OFFICIAL_PLAN_KIND,
    default_steps,
    render_pack_registry,
    render_root_index,
    slugify,
    write_pack,
)
from construction_plan_schema import _parse_yaml, machine_schema_violations, validate_pack_registry
from mother_doc_lint_support import mother_doc_lint_summary
from mother_doc_state_support import iter_atomic_markdown_files, parse_frontmatter
from skill_runtime_context import cli_command


LAYER_ORDER = {
    "overview": 0,
    "entry": 1,
    "resolution": 2,
    "capability": 3,
    "support": 4,
}


def _relative_doc_key(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def _parse_doc_record(root: Path, path: Path) -> dict[str, object] | None:
    metadata, body, parse_errors = parse_frontmatter(path)
    if parse_errors:
        return None
    relative_path = _relative_doc_key(path, root)
    anchors: set[str] = set()
    for field in ("anchors_down", "anchors_support"):
        raw_value = metadata.get(field)
        if isinstance(raw_value, list):
            anchors.update(str(item) for item in raw_value if str(item).strip())
    return {
        "path": path,
        "relative_path": relative_path,
        "title": str(metadata.get("thumb_title") or path.stem),
        "summary": str(metadata.get("thumb_summary") or ""),
        "state": str(metadata.get("doc_work_state") or ""),
        "display_layer": str(metadata.get("display_layer") or ""),
        "layer_index": LAYER_ORDER.get(str(metadata.get("display_layer") or ""), 99),
        "doc_role": str(metadata.get("doc_role") or ""),
        "anchors": sorted(anchors),
        "parent_dir": str(path.relative_to(root).parent),
        "body": body,
    }


def _collect_doc_records(mother_doc_root: Path) -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for file_path in iter_atomic_markdown_files(mother_doc_root):
        record = _parse_doc_record(mother_doc_root, file_path)
        if record is None:
            continue
        records[str(record["relative_path"])] = record
    return records


def _record_sort_key(record: dict[str, object]) -> tuple[int, str]:
    return int(record["layer_index"]), str(record["relative_path"])


def _anchor_graph(records: dict[str, dict[str, object]]) -> dict[str, set[str]]:
    graph = {doc_ref: set() for doc_ref in records}
    for doc_ref, record in records.items():
        for target in record["anchors"]:
            if target not in records:
                continue
            graph[doc_ref].add(target)
            graph[target].add(doc_ref)
    return graph


def _modified_doc_refs(records: dict[str, dict[str, object]]) -> list[str]:
    return sorted(
        [
            doc_ref
            for doc_ref, record in records.items()
            if record["state"] == "modified" and record["doc_role"] != "root_index"
        ],
        key=lambda doc_ref: _record_sort_key(records[doc_ref]),
    )


def _same_parent_doc_graph(records: dict[str, dict[str, object]], modified_refs: set[str]) -> dict[str, set[str]]:
    graph = {doc_ref: set() for doc_ref in modified_refs}
    parent_groups: dict[str, list[str]] = {}
    for doc_ref in modified_refs:
        parent_groups.setdefault(str(records[doc_ref]["parent_dir"]), []).append(doc_ref)
    for doc_refs in parent_groups.values():
        if len(doc_refs) < 2:
            continue
        for left_ref in doc_refs:
            graph[left_ref].update(ref for ref in doc_refs if ref != left_ref)
    return graph


def _cluster_modified_docs(records: dict[str, dict[str, object]]) -> list[list[str]]:
    modified_refs = _modified_doc_refs(records)
    modified_set = set(modified_refs)
    anchor_graph = _anchor_graph(records)
    same_parent_graph = _same_parent_doc_graph(records, modified_set)
    visited: set[str] = set()
    clusters: list[list[str]] = []
    for seed in modified_refs:
        if seed in visited:
            continue
        queue = [seed]
        component: list[str] = []
        visited.add(seed)
        while queue:
            current = queue.pop(0)
            component.append(current)
            linked_refs = set()
            linked_refs.update(ref for ref in anchor_graph[current] if ref in modified_set)
            linked_refs.update(same_parent_graph.get(current, set()))
            for neighbor in sorted(linked_refs, key=lambda doc_ref: _record_sort_key(records[doc_ref])):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                queue.append(neighbor)
        component.sort(key=lambda doc_ref: _record_sort_key(records[doc_ref]))
        clusters.append(component)
    clusters.sort(key=lambda component: _record_sort_key(records[component[0]]))
    return clusters


def _parent_index_ref(doc_ref: str) -> str | None:
    doc_path = Path(doc_ref)
    if doc_path.parent == Path("."):
        return None
    return str(doc_path.parent / "00_index.md")


def _source_refs_for_cluster(
    cluster: list[str],
    records: dict[str, dict[str, object]],
    graph: dict[str, set[str]],
) -> list[str]:
    selected: set[str] = set(cluster)
    for doc_ref in cluster:
        parent_index = _parent_index_ref(doc_ref)
        if parent_index and parent_index in records:
            selected.add(parent_index)
        selected.update(graph.get(doc_ref, set()))
    ordered = sorted(selected, key=lambda item: _record_sort_key(records[item]))
    return ordered


def _pack_slug_seed(doc_ref: str) -> str:
    doc_path = Path(doc_ref)
    if doc_path.stem == "00_index" and doc_path.parent != Path("."):
        return slugify(doc_path.parent.name)
    return slugify(doc_path.stem)


def _compact_doc_refs(doc_refs: list[str], *, limit: int = 3) -> str:
    if len(doc_refs) <= limit:
        return ", ".join(doc_refs)
    return ", ".join(doc_refs[:limit]) + f" (+{len(doc_refs) - limit} more)"


def _build_pack_specs(
    mother_doc_root: Path,
    explicit_planning_doc: Path | None = None,
) -> tuple[list[dict[str, object]], list[str], list[str]]:
    records = _collect_doc_records(mother_doc_root)
    modified_refs = _modified_doc_refs(records)
    if not modified_refs:
        return [], [], []

    graph = _anchor_graph(records)
    clusters = _cluster_modified_docs(records)
    explicit_planning_ref: str | None = None
    if explicit_planning_doc is not None and explicit_planning_doc.exists():
        try:
            explicit_planning_ref = str(explicit_planning_doc.relative_to(mother_doc_root))
        except ValueError:
            explicit_planning_ref = None

    pack_specs: list[dict[str, object]] = []
    previous_step_id: str | None = None
    all_planning_basis_refs: set[str] = set()
    for index, cluster in enumerate(clusters, start=1):
        primary_doc = cluster[0]
        primary_record = records[primary_doc]
        source_doc_refs = _source_refs_for_cluster(cluster, records, graph)
        planning_basis_refs = [
            doc_ref
            for doc_ref in source_doc_refs
            if str(records[doc_ref]["doc_role"]) == "design_plan"
        ]
        if explicit_planning_ref is not None and explicit_planning_ref not in planning_basis_refs:
            planning_basis_refs.append(explicit_planning_ref)
        all_planning_basis_refs.update(planning_basis_refs)
        design_step_id = f"AUTO-DESIGN-{index:02d}-{_pack_slug_seed(primary_doc)}"
        modified_excerpt = _compact_doc_refs(cluster)
        pack_goal = (
            f"Implement the modified mother_doc slice around `{primary_record['title']}` and keep the linked documents aligned."
        )
        pack_specs.append(
            {
                "design_step_id": design_step_id,
                "target_requirement_atoms": modified_excerpt,
                "target_requirement_atoms_list": cluster,
                "dependencies": previous_step_id or "none",
                "implementation_actions": pack_goal,
                "stage_assertions": f"Code, runtime, and writeback align with the intent described by {modified_excerpt}.",
                "stage_tests": f"Run targeted validation that proves the slice behind {modified_excerpt} behaves as intended.",
                "stage_acceptance": f"Acceptance evidence explicitly covers the delivery slice behind {modified_excerpt}.",
                "live_delivery_witness": f"Requirement-level witness collected for {modified_excerpt}.",
                "rollback_or_risk": "If this cluster is too broad or too narrow, split or regroup packs before implementation begins.",
                "source_doc_refs": source_doc_refs,
                "planning_basis_refs": planning_basis_refs,
            }
        )
        previous_step_id = design_step_id
    return pack_specs, modified_refs, sorted(all_planning_basis_refs)


def _official_plan_prerequisites(mother_doc_root: Path) -> tuple[dict, int] | None:
    mother_doc_summary = mother_doc_lint_summary(mother_doc_root)
    if mother_doc_summary["status"] != "pass":
        return {
            "status": "fail",
            "reason": "mother_doc_not_ready_for_construction_plan",
            "mother_doc_root": str(mother_doc_root),
            "mother_doc_lint": mother_doc_summary,
            "hint": "official construction plan can be created only after mother-doc-lint passes",
        }, 1
    pack_specs, modified_refs, planning_basis_refs = _build_pack_specs(mother_doc_root)
    if not modified_refs:
        return {
            "status": "fail",
            "reason": "modified_doc_missing",
            "mother_doc_root": str(mother_doc_root),
            "hint": "official construction plan now requires at least one mother_doc atom marked modified",
        }, 1
    return {
        "status": "pass",
        "pack_specs": pack_specs,
        "modified_doc_refs": modified_refs,
        "planning_basis_refs": planning_basis_refs,
    }, 0


def construction_plan_init_result(
    target: Path,
    design_plan_path: Path | None,
    force: bool,
    plan_kind: str,
) -> tuple[dict, int]:
    if plan_kind not in PLAN_KIND_VALUES:
        return {
            "status": "fail",
            "reason": "invalid_plan_kind",
            "plan_kind": plan_kind,
            "allowed_plan_kinds": PLAN_KIND_VALUES,
        }, 1
    if target.exists() and any(target.iterdir()) and not force:
        return {
            "status": "fail",
            "target": str(target),
            "reason": "target_not_empty",
            "hint": "rerun with --force to replace the existing construction plan root",
        }, 1

    modified_doc_refs: list[str] = []
    planning_basis_refs: list[str] = []
    pack_specs: list[dict[str, object]] = []
    if plan_kind == OFFICIAL_PLAN_KIND:
        prerequisite_payload, status_code = _official_plan_prerequisites(target.parent)
        if status_code != 0:
            return prerequisite_payload, status_code
        pack_specs = list(prerequisite_payload["pack_specs"])
        modified_doc_refs = list(prerequisite_payload["modified_doc_refs"])
        planning_basis_refs = list(prerequisite_payload["planning_basis_refs"])
    else:
        pack_specs, modified_doc_refs, planning_basis_refs = _build_pack_specs(target.parent, design_plan_path)
        if not pack_specs:
            pack_specs = default_steps()
            modified_doc_refs = []
            planning_basis_refs = []

    if target.exists() and force:
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    target.joinpath("00_index.md").write_text(
        render_root_index(pack_specs, plan_kind, planning_basis_refs, modified_doc_refs),
        encoding="utf-8",
    )
    target.joinpath("pack_registry.yaml").write_text(
        render_pack_registry(pack_specs, plan_kind, planning_basis_refs),
        encoding="utf-8",
    )
    pack_dirs: list[str] = []
    for index, step in enumerate(pack_specs, start=1):
        pack_dir = target / f"{index:02d}_{slugify(str(step['design_step_id']))}"
        write_pack(pack_dir, step, index, plan_kind)
        pack_dirs.append(str(pack_dir))
    return {
        "status": "pass",
        "target": str(target),
        "plan_kind": plan_kind,
        "design_plan_path": str(design_plan_path) if design_plan_path is not None and design_plan_path.exists() else None,
        "modified_doc_refs": modified_doc_refs,
        "planning_basis_refs": planning_basis_refs,
        "created_packs": pack_dirs,
        "construction_plan_lint_command": cli_command("construction-plan-lint", "--path", target, "--json"),
    }, 0


def _validate_pack_registry_structure(root: Path) -> tuple[dict[str, object] | None, list[str]]:
    violations = validate_pack_registry(root)
    if violations:
        return None, violations
    payload, parse_errors = _parse_yaml(root / "pack_registry.yaml")
    if parse_errors:
        return None, [f"pack_registry.yaml: {error}" for error in parse_errors]
    if not isinstance(payload, dict):
        return None, ["pack_registry.yaml: top-level payload must be an object"]
    return payload, []


def construction_plan_lint_summary(path: Path, require_execution_eligible: bool = False) -> dict:
    root = path if path.is_dir() else path.parent if path.name == "00_index.md" else path
    exists = root.exists()
    pack_dirs = sorted([pack_dir for pack_dir in root.iterdir() if pack_dir.is_dir() and PACK_DIR_PATTERN.match(pack_dir.name)]) if exists else []
    mother_doc_root = root.parent
    missing_root_files = [name for name in ROOT_REQUIRED_FILES if not (root / name).exists()] if exists else list(ROOT_REQUIRED_FILES)
    missing_pack_files = {
        pack_dir.name: [name for name in PACK_MARKDOWN_FILES + PACK_MACHINE_FILES if not (pack_dir / name).exists()]
        for pack_dir in pack_dirs
    }
    missing_pack_files = {key: value for key, value in missing_pack_files.items() if value}
    files_to_check = [root / name for name in ROOT_REQUIRED_FILES if (root / name).exists()] + [
        pack_dir / name
        for pack_dir in pack_dirs
        for name in PACK_MARKDOWN_FILES + PACK_MACHINE_FILES
        if (pack_dir / name).exists()
    ]
    replace_me_hits = [
        str(file_path.relative_to(root))
        for file_path in files_to_check
        if "replace_me" in file_path.read_text(encoding="utf-8")
    ]
    guidance_hits = [
        str(file_path.relative_to(root))
        for file_path in files_to_check
        if file_path.suffix == ".md"
        and any(marker in file_path.read_text(encoding="utf-8") for marker in GUIDANCE_MARKERS)
    ]
    schema_violations = [
        violation
        for pack_dir in pack_dirs
        if not missing_pack_files.get(pack_dir.name)
        for violation in machine_schema_violations(pack_dir)
    ]
    source_ref_violations: list[str] = []
    registry_payload: dict[str, object] | None = None
    registry_violations: list[str] = []
    design_coverage_violations: list[str] = []
    execution_eligibility_violations: list[str] = []
    if exists and not missing_root_files:
        registry_payload, registry_violations = _validate_pack_registry_structure(root)
        if registry_payload is not None:
            declared_step_ids = registry_payload.get("design_step_ids", [])
            packs = registry_payload.get("packs", [])
            registry_step_ids = [
                str(item["design_step_id"])
                for item in packs
                if isinstance(item, dict) and "design_step_id" in item
            ]
            missing_steps = sorted(set(declared_step_ids) - set(registry_step_ids))
            unexpected_steps = sorted(set(registry_step_ids) - set(declared_step_ids))
            if missing_steps:
                design_coverage_violations.append(
                    f"pack_registry.yaml: registry missing pack entries for design_step_ids {missing_steps}"
                )
            if unexpected_steps:
                design_coverage_violations.append(
                    f"pack_registry.yaml: packs declare unexpected design_step_ids {unexpected_steps}"
                )
            if require_execution_eligible:
                if registry_payload["execution_eligible"] is not True:
                    execution_eligibility_violations.append(
                        "pack_registry.yaml: execution-eligible lint requires execution_eligible=true"
                    )
                if registry_payload["plan_kind"] != OFFICIAL_PLAN_KIND:
                    execution_eligibility_violations.append(
                        "pack_registry.yaml: execution-eligible lint requires plan_kind=official_plan"
                    )
                if registry_payload["plan_state"] not in {"planned_unused", "in_execution"}:
                    execution_eligibility_violations.append(
                        "pack_registry.yaml: execution-eligible lint requires plan_state in {planned_unused,in_execution}"
                    )
            pack_dirs_from_registry = {
                str(item["pack_dir"]): item for item in packs if isinstance(item, dict) and "pack_dir" in item
            }
            missing_registry_pack_dirs = sorted({pack_dir.name for pack_dir in pack_dirs} - set(pack_dirs_from_registry))
            missing_disk_pack_dirs = sorted(set(pack_dirs_from_registry) - {pack_dir.name for pack_dir in pack_dirs})
            if missing_registry_pack_dirs:
                design_coverage_violations.append(
                    f"pack_registry.yaml: registry missing pack entries for directories {missing_registry_pack_dirs}"
                )
            if missing_disk_pack_dirs:
                design_coverage_violations.append(
                    f"pack_registry.yaml: pack entries missing on disk {missing_disk_pack_dirs}"
                )
            for pack_dir in pack_dirs:
                if missing_pack_files.get(pack_dir.name):
                    continue
                manifest_payload, parse_errors = _parse_yaml(pack_dir / "pack_manifest.yaml")
                if parse_errors or not isinstance(manifest_payload, dict):
                    continue
                source_refs = manifest_payload.get("source_mother_doc_refs")
                if isinstance(source_refs, list):
                    for source_ref in source_refs:
                        ref_path = mother_doc_root / str(source_ref)
                        if not ref_path.exists():
                            source_ref_violations.append(
                                f"{pack_dir.name}/pack_manifest.yaml: source_mother_doc_ref_missing={source_ref}"
                            )
                registry_pack = pack_dirs_from_registry.get(pack_dir.name)
                if isinstance(registry_pack, dict):
                    for shared_key in (
                        "pack_id",
                        "design_step_id",
                        "plan_kind",
                        "pack_state",
                        "execution_eligible",
                        "state_sync_eligible",
                        "reusable_as_official_plan",
                    ):
                        if manifest_payload.get(shared_key) != registry_pack.get(shared_key):
                            design_coverage_violations.append(
                                f"{pack_dir.name}/pack_manifest.yaml: {shared_key} must match pack_registry.yaml"
                            )
                    if require_execution_eligible:
                        if manifest_payload.get("execution_eligible") is not True:
                            execution_eligibility_violations.append(
                                f"{pack_dir.name}/pack_manifest.yaml: execution_eligible must be true"
                            )
                        if manifest_payload.get("pack_state") not in {"planned_unused", "in_execution"}:
                            execution_eligibility_violations.append(
                                f"{pack_dir.name}/pack_manifest.yaml: pack_state must be planned_unused or in_execution"
                            )
    status = (
        "pass"
        if exists
        and pack_dirs
        and not missing_root_files
        and not missing_pack_files
        and not replace_me_hits
        and not guidance_hits
        and not schema_violations
        and not registry_violations
        and not design_coverage_violations
        and not source_ref_violations
        and not execution_eligibility_violations
        else "fail"
    )
    return {
        "path": str(path),
        "resolved_root": str(root),
        "exists": exists,
        "status": status,
        "missing_root_files": missing_root_files,
        "missing_pack_dirs": [] if pack_dirs else ["expected at least one NN_* pack directory"],
        "missing_pack_files": missing_pack_files,
        "files_with_replace_me": replace_me_hits,
        "files_with_template_guidance": guidance_hits,
        "pack_registry_violations": registry_violations,
        "machine_schema_violations": schema_violations,
        "design_coverage_violations": design_coverage_violations,
        "source_mother_doc_ref_violations": source_ref_violations,
        "execution_eligibility_violations": execution_eligibility_violations,
        "pack_markdown_files": PACK_MARKDOWN_FILES,
        "pack_machine_files": PACK_MACHINE_FILES,
        "construction_plan_gate_allowed": status == "pass",
    }
