from __future__ import annotations

import filecmp
import json
import shutil
from pathlib import Path
from typing import Any

import yaml

from cli_support import parse_frontmatter, read_json, reset_directory, write_json, write_text
from factory_support import BANNED_TERMS, latest_registry_snapshot


MANIFEST_REL_PATH = "90_runtime_governance/50_artifact_manifest.json"
LEGACY_MANIFEST_REL_PATH = "90_runtime_governance/30_artifact_manifest.json"
RUNTIME_JSON_PATHS = [
    "90_runtime_governance/20_latest_factory_payload.json",
    "90_runtime_governance/30_latest_enhanced_intent.md",
    "90_runtime_governance/40_latest_subagent_run.json",
    MANIFEST_REL_PATH,
]


def _framework_snapshot(run_snapshot: dict[str, object] | None) -> dict[str, Any]:
    registry = latest_registry_snapshot()
    latest_run = registry.get("latest_run", {})
    base = latest_run if isinstance(latest_run, dict) else {}
    snapshot = dict(base)
    if run_snapshot:
        snapshot.update(run_snapshot)
    return snapshot


def _previous_managed_files(previous_manifest: dict[str, object]) -> set[str]:
    collected: set[str] = set()
    managed_files = previous_manifest.get("managed_files")
    if isinstance(managed_files, list):
        collected.update(str(item) for item in managed_files)
    for legacy_key in ("managed_markdown", "managed_json", "runtime_json_paths"):
        legacy_files = previous_manifest.get(legacy_key)
        if isinstance(legacy_files, list):
            collected.update(str(item) for item in legacy_files)
    return collected


def _yaml_frontmatter(meta: dict[str, Any]) -> str:
    return "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip() + "\n---\n\n"


def _markdown(meta: dict[str, Any], body: str) -> str:
    return _yaml_frontmatter(meta) + body.strip() + "\n"


def _doc_specs(snapshot: dict[str, Any]) -> dict[str, str]:
    factory_payload = snapshot.get("factory_payload", {})
    enhanced_intent = snapshot.get("enhanced_intent", {})
    subagent_run = snapshot.get("subagent_run", {})
    lint_audit = snapshot.get("lint_audit", {})
    intent_text = ""
    if isinstance(enhanced_intent, dict):
        intent_text = str(enhanced_intent.get("final_intent_output", "")).strip()
    consumers = ["Workflow-MotherDoc-OctopusOS", "Workflow-ConstructionPlan-OctopusOS", "Workflow-Implementation-OctopusOS", "Workflow-Acceptance-OctopusOS"]
    base_meta = {
        "producer_skill": "Workflow-SiteMap-Creation",
        "writeback_mode": "managed_refresh",
        "consumer_boundary": {
            "primary_consumers": consumers,
            "writeback_owner": "Workflow-SiteMap-Creation",
        },
    }
    docs = {
        "00_index.md": _markdown(
            {
                **base_meta,
                "doc_id": "octopus_os.mother_doc.framework.root_index",
                "doc_type": "framework_index",
                "topic": "全站开发文档框架总索引",
                "artifact_role": "root_index",
                "semantic_layer": "root",
                "anchors": [
                    {"target": "./00_governance/10_execution_chain.md", "relation": "routes_to", "direction": "downstream"},
                    {"target": "./10_site_map/10_framework_layers.md", "relation": "routes_to", "direction": "downstream"},
                ],
            },
            (
                "# 全站开发文档框架总索引\n\n"
                "## 当前定位\n"
                "- 这是 Workflow-SiteMap-Creation 管理的实验性框架真源，用来展示 folder 组织、frontmatter、字段语义、文档关系与下游消费边界。\n"
                "- factory 不是终点；当前框架默认要求先做意图强化，再进入 background subagent 的九阶段 runtask。\n\n"
                "## 当前受管层\n"
                "- `00_governance/`\n"
                "- `10_site_map/`\n"
                "- `20_code_map/`\n"
                "- `30_usage_manual/`\n"
                "- `40_derivative_specs/`\n"
                "- `90_runtime_governance/`\n"
            ),
        ),
        "00_governance/10_execution_chain.md": _markdown(
            {
                **base_meta,
                "doc_id": "octopus_os.mother_doc.framework.execution_chain",
                "doc_type": "framework_atom",
                "topic": "执行链合同",
                "artifact_role": "execution_chain_contract",
                "semantic_layer": "governance",
                "anchors": [
                    {"target": "../../Otctopus_OS_AgentConsole/Skills/Workflow-SiteMap-Creation/SKILL.md", "relation": "implemented_by", "direction": "upstream"},
                    {"target": "./20_keyword_first_decision_contract.md", "relation": "depends_on", "direction": "downstream"},
                ],
            },
            (
                "# 执行链合同\n\n"
                "1. factory 拆分请求并输出结构化对象。\n"
                "2. Meta-Enhance-Prompt 把 factory 输出强化为单段 `INTENT:`。\n"
                "3. 主 agent 在 tmux 中启动 background subagent，固定 `gpt-5.4` 与 `reasoning high`。\n"
                "4. subagent 必须显式执行 Functional-Analysis-Runtask 九阶段 analysis_loop。\n"
                "5. 主 agent 回读 runtask 证据、刷新实验产物并执行最终 lint/validation。\n"
            ),
        ),
        "00_governance/20_keyword_first_decision_contract.md": _markdown(
            {
                **base_meta,
                "doc_id": "octopus_os.mother_doc.framework.keyword_first_contract",
                "doc_type": "framework_atom",
                "topic": "keyword-first 决策合同",
                "artifact_role": "decision_contract",
                "semantic_layer": "governance",
                "anchors": [{"target": "./30_frontmatter_contract.md", "relation": "constrains", "direction": "downstream"}],
            },
            (
                "# keyword-first 决策合同\n\n"
                "- 任何结构改动必须先显式判断：`rewrite` / `keyword_first_replace` / `minimal_add`。\n"
                "- 不得用全量目录重刷掩盖决策。\n"
                "- 任何删除、迁移、改写都要留在 runtask 的 design / impact / implementation 证据里。\n"
            ),
        ),
        "00_governance/30_frontmatter_contract.md": _markdown(
            {
                **base_meta,
                "doc_id": "octopus_os.mother_doc.framework.frontmatter_contract",
                "doc_type": "framework_atom",
                "topic": "frontmatter 与字段语义合同",
                "artifact_role": "frontmatter_contract",
                "semantic_layer": "governance",
                "anchors": [{"target": "../10_site_map/20_document_relations.md", "relation": "defines", "direction": "downstream"}],
            },
            (
                "# frontmatter 与字段语义合同\n\n"
                "- 必填：`doc_id` `doc_type` `topic` `artifact_role` `semantic_layer` `producer_skill` `writeback_mode` `consumer_boundary` `anchors`。\n"
                "- `consumer_boundary.primary_consumers` 用于给后续技能提供可爬取的消费边界。\n"
                "- `anchors` 用于表达文档定位与关系，不允许只剩孤立标题文本。\n"
            ),
        ),
        "10_site_map/10_framework_layers.md": _markdown(
            {
                **base_meta,
                "doc_id": "octopus_os.mother_doc.framework.layers",
                "doc_type": "framework_atom",
                "topic": "框架层次与职责",
                "artifact_role": "layer_map",
                "semantic_layer": "site_map",
                "anchors": [{"target": "./20_document_relations.md", "relation": "adjacent_to", "direction": "peer"}],
            },
            (
                "# 框架层次与职责\n\n"
                "- `00_governance`：治理、执行链、keyword-first、frontmatter 合同。\n"
                "- `10_site_map`：框架层与文档关系。\n"
                "- `20_code_map`：技能运行面、命令入口、后台 subagent 边界。\n"
                "- `30_usage_manual`：主 agent / subagent 如何消费与回写。\n"
                "- `40_derivative_specs`：manifest、lint 与消费协议。\n"
            ),
        ),
        "10_site_map/20_document_relations.md": _markdown(
            {
                **base_meta,
                "doc_id": "octopus_os.mother_doc.framework.document_relations",
                "doc_type": "framework_atom",
                "topic": "文档关系与回写定位",
                "artifact_role": "relation_map",
                "semantic_layer": "site_map",
                "anchors": [{"target": "../30_usage_manual/10_agent_execution_flow.md", "relation": "consumed_by", "direction": "downstream"}],
            },
            (
                "# 文档关系与回写定位\n\n"
                "- 治理层定义约束，站点地图层定义承载位，代码地图层指向技能运行面，使用说明层定义 agent 消费路径。\n"
                "- 后续技能不应重新猜 frontmatter；应直接读取这些字段和 anchors。\n"
            ),
        ),
        "20_code_map/10_skill_runtime_surface.md": _markdown(
            {
                **base_meta,
                "doc_id": "octopus_os.mother_doc.framework.skill_runtime_surface",
                "doc_type": "framework_atom",
                "topic": "技能运行面地图",
                "artifact_role": "runtime_surface",
                "semantic_layer": "code_map",
                "anchors": [{"target": "../30_usage_manual/20_subagent_closeout.md", "relation": "supports", "direction": "downstream"}],
            },
            (
                "# 技能运行面地图\n\n"
                "- 当前运行链显式依赖 Workflow-SiteMap-Creation、Meta-Enhance-Prompt、Functional-Analysis-Runtask。\n"
                "- background subagent 在 tmux 中执行，主 agent 轮询其事件日志与最后消息，连续 10 分钟无新输出才允许判死。\n"
                f"- 最近一次 subagent 状态：{subagent_run.get('status', 'unknown')}。\n"
            ),
        ),
        "30_usage_manual/10_agent_execution_flow.md": _markdown(
            {
                **base_meta,
                "doc_id": "octopus_os.mother_doc.framework.agent_execution_flow",
                "doc_type": "framework_atom",
                "topic": "主 agent 执行流",
                "artifact_role": "usage_manual",
                "semantic_layer": "usage_manual",
                "anchors": [{"target": "./20_subagent_closeout.md", "relation": "next", "direction": "downstream"}],
            },
            (
                "# 主 agent 执行流\n\n"
                "- 先读取 factory payload，再调用 Meta-Enhance-Prompt。\n"
                "- 主 agent 负责创建 runtask workspace、启动 tmux subagent、轮询输出、手工终止 tmux session、回读最新改造结果并刷新产物。\n"
                f"- 最近一次强化意图：`{intent_text[:120]}`\n"
            ),
        ),
        "30_usage_manual/20_subagent_closeout.md": _markdown(
            {
                **base_meta,
                "doc_id": "octopus_os.mother_doc.framework.subagent_closeout",
                "doc_type": "framework_atom",
                "topic": "subagent closeout 与验证",
                "artifact_role": "usage_manual",
                "semantic_layer": "usage_manual",
                "anchors": [{"target": "../90_runtime_governance/40_latest_subagent_run.json", "relation": "documents", "direction": "downstream"}],
            },
            (
                "# subagent closeout 与验证\n\n"
                "- subagent 完成后，主 agent 必须读取 runtask workspace、stage lint 结果和 validation 证据。\n"
                "- 若 validation 未通过，不允许把本轮视为完成。\n"
                f"- 最近一次 lint 状态：{lint_audit.get('status', 'unknown')}。\n"
            ),
        ),
        "40_derivative_specs/10_artifact_manifest.md": _markdown(
            {
                **base_meta,
                "doc_id": "octopus_os.mother_doc.framework.artifact_manifest_doc",
                "doc_type": "framework_atom",
                "topic": "实验产物 manifest 说明",
                "artifact_role": "manifest_contract",
                "semantic_layer": "derivative_specs",
                "anchors": [{"target": "../90_runtime_governance/50_artifact_manifest.json", "relation": "mirrors", "direction": "downstream"}],
            },
            (
                "# 实验产物 manifest 说明\n\n"
                "- manifest 记录 managed files、frontmatter keys、最近一次刷新摘要与写入动作。\n"
                "- 它是后续技能爬取结构、判断回写目标和识别 stale artifact 的机器入口。\n"
            ),
        ),
    }
    runtime_json = {
        "90_runtime_governance/20_latest_factory_payload.json": json.dumps(factory_payload, ensure_ascii=False, indent=2) + "\n",
        "90_runtime_governance/30_latest_enhanced_intent.md": _markdown(
            {
                **base_meta,
                "doc_id": "octopus_os.mother_doc.framework.latest_enhanced_intent",
                "doc_type": "runtime_record",
                "topic": "最新强化意图",
                "artifact_role": "runtime_record",
                "semantic_layer": "runtime_governance",
                "anchors": [{"target": "../00_governance/10_execution_chain.md", "relation": "records", "direction": "upstream"}],
            },
            intent_text or "# 最新强化意图\n\n当前轮次尚未写入强化意图。\n",
        ),
        "90_runtime_governance/40_latest_subagent_run.json": json.dumps(subagent_run, ensure_ascii=False, indent=2) + "\n",
    }
    docs.update(runtime_json)
    return docs


def write_managed_artifacts(mother_doc_root: str, snapshot: dict[str, object] | None = None) -> dict[str, object]:
    root = Path(mother_doc_root)
    root.mkdir(parents=True, exist_ok=True)
    framework_snapshot = _framework_snapshot(snapshot)
    desired = _doc_specs(framework_snapshot)
    manifest_path = root / MANIFEST_REL_PATH
    legacy_manifest_path = root / LEGACY_MANIFEST_REL_PATH
    if manifest_path.exists():
        previous_manifest = read_json(manifest_path)
    elif legacy_manifest_path.exists():
        previous_manifest = read_json(legacy_manifest_path)
    else:
        previous_manifest = {}
    previous_files = _previous_managed_files(previous_manifest) if isinstance(previous_manifest, dict) else set()

    actions: list[dict[str, str]] = []
    written_files: list[str] = []
    for rel_path, content in desired.items():
        target = root / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            action = "minimal_add"
        elif target.read_text(encoding="utf-8") != content:
            action = "keyword_first_replace"
        else:
            action = "reuse_existing"
        if action != "reuse_existing":
            target.write_text(content, encoding="utf-8")
        written_files.append(rel_path)
        actions.append({"path": rel_path, "action": action})

    stale_files = sorted(previous_files - set(desired))
    for rel_path in stale_files:
        target = root / rel_path
        if target.exists():
            target.unlink()
        actions.append({"path": rel_path, "action": "rewrite_delete"})

    manifest = {
        "managed_files": sorted(desired),
        "required_frontmatter_keys": [
            "doc_id",
            "doc_type",
            "topic",
            "artifact_role",
            "semantic_layer",
            "producer_skill",
            "writeback_mode",
            "consumer_boundary",
            "anchors",
        ],
        "runtime_json_paths": sorted(RUNTIME_JSON_PATHS),
        "latest_subagent_status": framework_snapshot.get("subagent_run", {}).get("status", ""),
        "latest_factory_digest": framework_snapshot.get("factory_payload", {}).get("source_digest", ""),
        "latest_keyword_first_decision": framework_snapshot.get("keyword_first_decision_summary", {}).get("keyword_first_decision", ""),
        "write_actions": actions,
    }
    write_json(manifest_path, manifest)
    if MANIFEST_REL_PATH not in written_files:
        written_files.append(MANIFEST_REL_PATH)
    return {
        "status": "pass",
        "mother_doc_root": str(root),
        "written_files": sorted(set(written_files)),
        "write_actions": actions,
    }


def sync_client_mirror(source_root: str, mirror_root: str) -> dict[str, object]:
    source = Path(source_root)
    mirror = Path(mirror_root)
    reset_directory(mirror)
    for child in source.iterdir():
        target = mirror / child.name
        if child.is_dir():
            shutil.copytree(child, target)
        else:
            shutil.copy2(child, target)
    return {"status": "pass", "source_root": str(source), "mirror_root": str(mirror)}


def _recursive_mirror_diff(source: Path, mirror: Path) -> list[str]:
    diffs: list[str] = []
    if not source.exists() or not mirror.exists():
        return ["missing_source_or_mirror"]
    comparison = filecmp.dircmp(source, mirror)
    diffs.extend(sorted(str(Path(comparison.left) / name) for name in comparison.left_only))
    diffs.extend(sorted(str(Path(comparison.right) / name) for name in comparison.right_only))
    diffs.extend(sorted(str(Path(comparison.left) / name) for name in comparison.diff_files))
    for subdir in sorted(comparison.subdirs):
        diffs.extend(_recursive_mirror_diff(source / subdir, mirror / subdir))
    return diffs


def lint_managed_artifacts(mother_doc_root: str, mirror_root: str | None = None) -> dict[str, object]:
    root = Path(mother_doc_root)
    manifest_path = root / MANIFEST_REL_PATH
    errors: list[str] = []
    warnings: list[str] = []
    audited_files: list[str] = []
    if not manifest_path.exists():
        errors.append(f"missing:{MANIFEST_REL_PATH}")
        return {"status": "fail", "errors": errors, "warnings": warnings, "audited_files": audited_files, "mirror_diff": []}
    manifest = read_json(manifest_path)
    managed_files = manifest.get("managed_files", [])
    required_keys = manifest.get("required_frontmatter_keys", [])
    if not isinstance(managed_files, list) or not isinstance(required_keys, list):
        errors.append("invalid_manifest")
        return {"status": "fail", "errors": errors, "warnings": warnings, "audited_files": audited_files, "mirror_diff": []}

    for rel_path in managed_files:
        target = root / rel_path
        if not target.exists():
            errors.append(f"missing:{rel_path}")
            continue
        audited_files.append(rel_path)
        if target.suffix == ".json":
            json.loads(target.read_text(encoding="utf-8"))
            continue
        content = target.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(content)
        for key in required_keys:
            if key not in frontmatter or frontmatter[key] in ("", None, [], {}):
                errors.append(f"frontmatter:{rel_path}:{key}")
        if not isinstance(frontmatter.get("anchors"), list):
            errors.append(f"anchors_missing:{rel_path}")
        consumer_boundary = frontmatter.get("consumer_boundary")
        if not isinstance(consumer_boundary, dict) or not consumer_boundary.get("primary_consumers"):
            errors.append(f"consumer_boundary_missing:{rel_path}")
        if any(term in content for term in BANNED_TERMS):
            errors.append(f"banned_term:{rel_path}")

    mirror_diff: list[str] = []
    if mirror_root:
        mirror_diff = _recursive_mirror_diff(root, Path(mirror_root))
        if mirror_diff:
            warnings.extend(f"mirror_diff:{item}" for item in mirror_diff)
            errors.append("mirror_not_in_sync")
    return {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
        "audited_files": sorted(audited_files),
        "mirror_diff": mirror_diff,
    }
