# Cli_Toolbox 使用文档

适用技能：`2-Octupos-FullStack`

## 命名约束
- 工具统一命名为 `Cli_Toolbox.<tool_name>`。

## 工具清单
- `Cli_Toolbox.mother_doc_stage` -> `scripts/Cli_Toolbox.py mother-doc-stage`
- `Cli_Toolbox.materialize_container_layout` -> `scripts/Cli_Toolbox.py materialize-container-layout`
- `Cli_Toolbox.sync_mother_doc_navigation` -> `scripts/Cli_Toolbox.py sync-mother-doc-navigation`
- `Cli_Toolbox.implementation_stage` -> `scripts/Cli_Toolbox.py implementation-stage`
- `Cli_Toolbox.evidence_stage` -> `scripts/Cli_Toolbox.py evidence-stage`

## 阶段化使用说明

### Cli_Toolbox.mother_doc_stage
- 做什么：
  - 打印 `mother_doc` 阶段合同，包括强化入口、递归导航入口与写回方式。
- 怎么用：
  - `cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack && python3 scripts/Cli_Toolbox.py mother-doc-stage --json | sed -n '1,220p'`

### Cli_Toolbox.materialize_container_layout
- 做什么：
  - 根据 AI 已判定的容器名，创建工作目录、`Mother_Doc` 同名目录、抽象层骨架，并刷新递归导航索引。
- 怎么用：
  - `cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack && python3 scripts/Cli_Toolbox.py materialize-container-layout --container User_UI --container Mongo_DB --dry-run --json | sed -n '1,260p'`

### Cli_Toolbox.sync_mother_doc_navigation
- 做什么：
  - 为 `Mother_Doc` 当前目录树刷新 `agents.md`，并为缺失层补齐最小 `README.md`。
- 怎么用：
  - `cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack && python3 scripts/Cli_Toolbox.py sync-mother-doc-navigation --json | sed -n '1,260p'`

### Cli_Toolbox.implementation_stage
- 做什么：
  - 打印 `implementation` 阶段合同，明确只能消费 `mother_doc` 当前状态产物。
- 怎么用：
  - `cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack && python3 scripts/Cli_Toolbox.py implementation-stage --json | sed -n '1,220p'`

### Cli_Toolbox.evidence_stage
- 做什么：
  - 打印 `evidence` 阶段合同，明确必须承接 `mother_doc + implementation` 当前状态产物。
- 怎么用：
  - `cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack && python3 scripts/Cli_Toolbox.py evidence-stage --json | sed -n '1,220p'`

## 结果字段
- `materialize-container-layout`：
  - `created_workspace_dirs`
  - `created_document_dirs`
  - `existing_workspace_dirs`
  - `existing_document_dirs`
  - `created_document_files`
  - `navigation_sync`
  - `warnings`
- `sync-mother-doc-navigation`：
  - `created_readmes`
  - `updated_agents`
  - `removed_legacy_indexes`

## 同步维护要求
- 修改工具行为后，必须同步更新本文件与 `Cli_Toolbox_DEVELOPMENT.md`。
- 若为多模块 Toolbox，还需同步更新：
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - `references/tooling/development/20_CATEGORY_INDEX.md`
  - 对应模块文档（`references/tooling/development/modules/*.md`）
