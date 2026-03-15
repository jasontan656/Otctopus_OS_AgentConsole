---
name: SkillsManager-Mirror-To-Codex
description: 将产品仓内受管 skills 同步到 `~/.codex/skills`，并治理 push/install/rename 三类镜像动作的技能。
skill_mode: guide_with_tool
metadata:
  doc_structure:
    doc_id: skillsmanager_mirror_to_codex.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Mirror-To-Codex skill
---

# SkillsManager-Mirror-To-Codex

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能用于把产品仓中的受管技能镜像到 codex skills 安装目录，并为 `push`、`install`、`rename` 三类动作提供固定入口。
- 本技能只治理 mirror 到 codex 的同步动作，不接管目标技能模板治理、文档结构治理或 Git 推送本身。
- 当前形态为 `guide_with_tool`；门面直接暴露功能入口，深层正文沿各入口继续下沉。

### 2. 技能约束
- 进入任一功能入口后，沿当前动作闭环继续阅读：
  - `contract`
  - `tools`
  - `execution`
  - `validation`
- 文档是真源；`read-contract-context` 输出的是当前入口链路的编译结果，`read-path-context` 作为等价别名保留。
- `install` 只返回外部安装路由，不直接在 codex 目录中伪装首次安装为覆盖同步。
- `rename` 必须显式提供 `--rename-from`；`auto` 只在 `push/install` 之间收敛。

### 3. 顶层常驻合同
- `scope=skill` 时必须提供 `--skill-name`。
- `skill_name` 只能是 skills 边界内的相对路径，禁止空段、绝对路径、反斜杠与 `.` / `..` 越界段。
- `.system/*` 技能在 codex 安装目录中使用小写规范名；mirror 侧实际目录名需自动映射到安装目录规范名。

## 2. 功能入口
- [自动导航]：`path/auto_routing/00_AUTO_ROUTING_ENTRY.md`
  - 作用：定义 `auto` 如何在 `push` 与 `install` 之间收敛，并约束显式 `rename` 的进入条件。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry auto_routing --json`
- [Push 同步]：`path/push_sync/00_PUSH_SYNC_ENTRY.md`
  - 作用：治理已安装技能或全量镜像时的覆盖同步语义。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry push_sync --json`
- [Install 路由]：`path/install_route/00_INSTALL_ROUTE_ENTRY.md`
  - 作用：治理目标技能未安装时的外部安装路由，不直接执行伪安装。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry install_route --json`
- [Rename 同步]：`path/rename_sync/00_RENAME_SYNC_ENTRY.md`
  - 作用：治理技能重命名时的新旧目录切换，避免 codex 目录双目录并存。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry rename_sync --json`
- [镜像边界]：`path/mirror_boundary/00_MIRROR_BOUNDARY_ENTRY.md`
  - 作用：定义 mirror 根解析、可同步技能根发现与 codex 根禁留项的固定边界。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry mirror_boundary --json`

## 3. 目录结构图
```text
SkillsManager-Mirror-To-Codex/
├── SKILL.md
├── agents/
├── path/
│   ├── auto_routing/
│   ├── push_sync/
│   ├── install_route/
│   ├── rename_sync/
│   └── mirror_boundary/
└── scripts/
```
- `path/`：本技能唯一的文档承载面，自动导航、push/install/rename 与镜像边界都沿入口链路下沉。
- `scripts/`：实际同步 CLI、链路编译 CLI、运行时 helper 与回归测试。
- `agents/`：agent runtime config。
