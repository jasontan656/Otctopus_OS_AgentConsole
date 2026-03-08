---
name: "Meta-Agents"
description: "集中回收、托管并同步 workspace 内的 AGENTS.md。用于扫描现有 AGENTS.md 完整复制进技能目录、维护源路径到托管模板的映射，并把技能内托管版本回写到指定或全部目标位置。"
---

# Meta-Agents

## 1. 目标
- 集中托管 workspace 内所有 `AGENTS.md`，避免规则分散在各仓库各目录。
- 提供两个固定动作：
  - `scan-collect`：扫描并完整复制现有 `AGENTS.md` 到技能目录。
  - `sync-out`：把技能内托管版本回写到指定目标或全部目标。
- 当新的 `AGENTS.md` 在扫描范围内出现时，再跑一次 `scan-collect` 即可把它纳入管理范围。

## 2. 可用工具
- 统一入口：`scripts/Cli_Toolbox.py`
- 工具清单：
  - `Cli_Toolbox.registry` - 查看当前托管的 `AGENTS.md` 映射。
  - `Cli_Toolbox.scan_collect` - 扫描 source root，完整复制所有 `AGENTS.md` 进技能并更新 registry。
  - `Cli_Toolbox.sync_out` - 把托管版本回写到指定目标或全部目标。
- 文档：
  - 使用文档：`references/tooling/Cli_Toolbox_USAGE.md`
  - 开发文档：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`

## 3. 工作流约束
- 输入：
  - `source_root`，默认 `/home/jasontan656/AI_Projects`
  - 可选 `target_source_path`
- 步骤：
  - 运行 `scan-collect`，把当前扫描到的全部 `AGENTS.md` 复制到 `assets/managed_agents/`
  - 直接修改技能内托管副本
  - 运行 `sync-out --target-source-path <abs_path>` 或 `sync-out --all`
- 输出：
  - `registry.json`
  - 托管副本目录 `assets/managed_agents/<root_slug>/.../AGENTS.md`
  - 结构化 JSON 执行结果
- 完成判定：
  - `scan-collect` 返回 `status=ok`
  - `sync-out` 返回 `status=ok`

## 4. 规则约束
- 仅管理文件名严格等于 `AGENTS.md` 的文件。
- `scan-collect` 必须完整复制文件内容，不做语义改写。
- `sync-out` 只能把技能内托管副本回写到 registry 中记录过的源路径。
- 扫描时必须排除技能自身的 `assets/managed_agents/` 托管副本，避免递归回收。
- 不允许把托管副本直接写到技能目录之外的任意新路径；回写目标必须来自 registry。

## 5. 方法论约束
- 默认把技能内托管副本视为唯一可批量编辑的管理面。
- 新出现的 `AGENTS.md` 先通过 `scan-collect` 纳入 registry，再允许统一回写。
- 当用户只想更新单个目标时，优先 `sync-out --target-source-path ...`，避免全量覆盖。

## 6. 内联导航索引
- [Cli_Toolbox 工具入口] -> [scripts/Cli_Toolbox.py]
- [Agent 元数据] -> [agents/openai.yaml]
- [托管 registry] -> [assets/managed_agents/registry.json]
- [Cli_Toolbox 使用文档] -> [references/tooling/Cli_Toolbox_USAGE.md]
- [Cli_Toolbox 开发文档] -> [references/tooling/Cli_Toolbox_DEVELOPMENT.md]
- [Cli_Toolbox 开发架构总览] -> [references/tooling/development/00_ARCHITECTURE_OVERVIEW.md]
- [Cli_Toolbox 开发分类索引] -> [references/tooling/development/20_CATEGORY_INDEX.md]
- [Cli_Toolbox 模块目录] -> [references/tooling/development/10_MODULE_CATALOG.yaml]

## 7. 架构契约
```text
Meta-Agents/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── managed_agents/
│       └── registry.json
├── scripts/
│   ├── Cli_Toolbox.py
│   ├── cli_parser_support.py
│   ├── managed_collect.py
│   ├── managed_paths.py
│   ├── managed_registry.py
│   └── managed_sync.py
├── references/
│   └── tooling/
│       ├── Cli_Toolbox_USAGE.md
│       ├── Cli_Toolbox_DEVELOPMENT.md
│       └── development/
│           ├── 00_ARCHITECTURE_OVERVIEW.md
│           ├── 10_MODULE_CATALOG.yaml
│           ├── 20_CATEGORY_INDEX.md
│           ├── 90_CHANGELOG.md
│           └── modules/
│               ├── MODULE_TEMPLATE.md
│               ├── mod_collect.md
│               └── mod_sync.md
└── tests/
    └── test_cli_toolbox.py
```
