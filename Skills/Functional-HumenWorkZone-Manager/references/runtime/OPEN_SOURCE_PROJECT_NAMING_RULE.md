---
doc_id: functional_humenworkzone_manager.runtime.open_source_project_naming_rule
doc_type: topic_atom
topic: Naming rule for local open-source project folders
anchors:
- target: OPEN_SOURCE_PROJECTS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: Folder naming is a governed part of the managed zone.
- target: PULL_OPEN_SOURCE_PROJECT_FLOW.md
  relation: required_by
  direction: upstream
  reason: Intake needs a naming decision before the repo is placed locally.
- target: OPEN_SOURCE_PROJECT_README_MAINTENANCE_FLOW.md
  relation: referenced_by
  direction: upstream
  reason: Inventory entries should align with this naming rule.
---

# Open Source Project Naming Rule

## 固定格式
- 本地目录名格式固定为：`<项目原名>_<2-3word加强>`。

## 命名解释
- `<项目原名>` 保留项目原本最常用的仓库名或官方短名。
- `<2-3word加强>` 用 2 到 3 个英文词描述该本地副本的主要用途、观察视角或保留原因。
- 加强段使用 `kebab-case`，例如：`source-read`、`agent-os-core`、`fork-compare`。

## 例子
- `codex_cli-agent-study`
- `openfang_agent-os-core`
- `openclaw_fork-compare`
- `social-analyzer_osint-tool`

## 禁止项
- 不要只保留原名而没有加强段。
- 不要用纯中文、日期堆叠或无法解释的缩写作为加强段。
- 不要把加强段写成超过 3 个词的长短语。
