---
name: SkillsManager-Production-Form
description: 持续维护 console 目录的产品形态，并沉淀将 Skills 目录作为 console 产品化源面的本地设计连续性的技能。
skill_mode: guide_with_tool
metadata:
  doc_structure:
    doc_id: skillsmanager_production_form.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Production-Form skill
---

# SkillsManager-Production-Form

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能用于持续维护 `Otctopus_OS_AgentConsole/Skills` 的 console 产品形态，并保留本地设计连续性。
- 本技能只治理 console 产品形态、产品意图与本地连续性日志，不替代具体 domain skill 实现、mirror 同步或 Git 推送。
- 当前形态为 `guide_with_tool`；门面直接暴露功能入口，深层正文沿各入口继续下沉。

### 2. 技能约束
- 进入任一功能入口后，沿当前动作闭环继续阅读：
  - `contract`
  - `tools`
  - `execution`
  - `validation`
- 文档是真源；`read-contract-context` 输出当前入口链路的编译结果，`read-path-context` 作为等价别名保留。
- active 连续性日志只能写入受管 runtime root；repo 内 seed snapshot 只用于首轮迁移与审计。
- 当 console 产品化判断触及 root file 受管文件时，正文维护必须切到 `$Meta-RootFile-Manager`，不得在当前技能里直改外部受管文件。

### 3. 顶层常驻合同
- 当前工程仓仍是 `Otctopus_OS_AgentConsole`，`Skills/` 目录是 console 产品化源面。
- codex 安装目录是部署面，不是 console 产品化的直接编辑面。
- 当前产品叙事仍以“高级个人助理的定制化思路 + 技能原子化治理 + AI 原生维护”为主轴。

## 2. 功能入口
- [工作合同]：`path/working_contract/00_WORKING_CONTRACT_ENTRY.md`
  - 作用：读取当前 console 产品形态、运行根与硬边界的稳定合同。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry working_contract --json`
- [产品意图]：`path/current_intent/00_CURRENT_INTENT_ENTRY.md`
  - 作用：读取当前 console 产品身份、主叙事、方法论与阶段目标。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry current_intent --json`
- [最近迭代]：`path/latest_log/00_LATEST_LOG_ENTRY.md`
  - 作用：读取受管 runtime log 的最新记录与 seed snapshot 迁移规则。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry latest_log --json`
- [追加迭代日志]：`path/append_iteration_log/00_APPEND_ITERATION_LOG_ENTRY.md`
  - 作用：按固定模板把新的 console 产品化判断写入 active runtime log。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry append_iteration_log --json`
- [RootFile 边界]：`path/rootfile_boundary/00_ROOTFILE_BOUNDARY_ENTRY.md`
  - 作用：当产品形态判断触及外部 root file 时，明确切换到 `$Meta-RootFile-Manager`。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry rootfile_boundary --json`

## 3. 目录结构图
```text
SkillsManager-Production-Form/
├── SKILL.md
├── agents/
├── path/
│   ├── working_contract/
│   ├── current_intent/
│   ├── latest_log/
│   ├── append_iteration_log/
│   └── rootfile_boundary/
└── scripts/
```
- `path/`：本技能唯一的文档承载面，console 产品形态、产品意图、迭代历史、日志追加与 rootfile 边界都沿入口链路下沉。
- `scripts/`：工作合同 CLI、链路编译 CLI、本地日志工具与回归测试。
- `agents/`：agent runtime config。
