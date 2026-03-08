---
name: "Meta-Default-md-manager"
description: "集中管理 workspace 内的常驻默认文档。显式分离 scan、collect、push 三阶段：scan 只扫描清单，collect 只回收托管副本与索引，push 只把托管副本回写目标。"
---

# Meta-Default-md-manager

## 1. 目标
- 提供常驻默认文档的集中管理入口，默认管理 `AGENTS.md`、所有目录的 `.gitignore`、以及 `Octopus_CodeBase_Backend/README.md`、`Octopus_CodeBase_Backend/Deployment_Guide.md`。
- 统一 CLI 入口为 `scripts/Cli_Toolbox.py`。
- 阶段命令必须显式分离：
  - `scan`
  - `collect`
  - `push`
- `scan / collect / push` 必须通过技能内互斥锁串行运行，禁止并行。

## 2. 可用工具
- 工具入口：`scripts/Cli_Toolbox.py`
- 命令清单：
  - `Cli_Toolbox.registry`
  - `Cli_Toolbox.scan`
  - `Cli_Toolbox.collect`
  - `Cli_Toolbox.push`
- 本技能默认只允许按阶段读取对应文档：
  - `scan` 只读 `references/stages/scan/`
  - `collect` 只读 `references/stages/collect/`
  - `push` 只读 `references/stages/push/`
- 禁止跨阶段读取 instruction / workflow / rules，除非用户显式要求。

## 3. 工作流约束
- `scan` 阶段入口：
  - instruction: `references/stages/scan/INSTRUCTION.md`
  - workflow: `references/stages/scan/WORKFLOW.md`
  - rules: `references/stages/scan/RULES.md`
- `collect` 阶段入口：
  - instruction: `references/stages/collect/INSTRUCTION.md`
  - workflow: `references/stages/collect/WORKFLOW.md`
  - rules: `references/stages/collect/RULES.md`
- `push` 阶段入口：
  - instruction: `references/stages/push/INSTRUCTION.md`
  - workflow: `references/stages/push/WORKFLOW.md`
  - rules: `references/stages/push/RULES.md`

## 4. 规则约束
- 默认禁止把阶段说明写回 `SKILL.md` 主体。
- `SKILL.md` 只保留入口、边界和导航，不承载阶段细节。
- `scan` 不允许写托管副本。
- `collect` 不允许重新扫描文件系统，只允许消费 `scan_report.json`。
- `push` 不允许绕过 `registry.json` 直接推断目标。
- `collect` 消费的 `scan_report.json` 不存在、为空或无条目时，必须显式报错。
- `push` 消费的 `registry.json` 不存在、为空或无条目时，必须显式报错。
- 除 `push` 对外回写源文件外，技能所有产物必须留在技能内部 `assets/managed_targets/`。
- 默认扫描时忽略 `Human_Work_Zone/`、`Codex_Skills_Result/`、`Codex_Skill_Runtime/`、`.git/`、`__pycache__/`、`.pytest_cache/`、`node_modules/`、虚拟环境目录。

## 5. 方法论约束
- 先 `scan`，再 `collect`，最后 `push`。
- 如果用户只要求某一阶段，仅读该阶段目录。
- 如果用户未显式要求跨阶段信息，不读取其他阶段目录。

## 6. 内联导航索引
- [Cli_Toolbox 工具入口] -> [scripts/Cli_Toolbox.py]
- [托管 registry] -> [assets/managed_targets/registry.json]
- [托管索引] -> [assets/managed_targets/index.md]
- [扫描报告] -> [assets/managed_targets/scan_report.json]
- [Scan Stage] -> [references/stages/scan/INSTRUCTION.md]
- [Collect Stage] -> [references/stages/collect/INSTRUCTION.md]
- [Push Stage] -> [references/stages/push/INSTRUCTION.md]

## 7. 架构契约
```text
Meta-Default-md-manager/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── managed_targets/
│       ├── .cli.lock
│       ├── index.md
│       ├── registry.json
│       └── scan_report.json
├── scripts/
│   ├── Cli_Toolbox.py
│   ├── cli_parser_support.py
│   ├── managed_collect.py
│   ├── managed_index.py
│   ├── managed_paths.py
│   ├── managed_push.py
│   ├── managed_registry.py
│   └── managed_scan.py
├── references/
│   ├── stages/
│   │   ├── scan/
│   │   │   ├── INSTRUCTION.md
│   │   │   ├── RULES.md
│   │   │   └── WORKFLOW.md
│   │   ├── collect/
│   │   │   ├── INSTRUCTION.md
│   │   │   ├── RULES.md
│   │   │   └── WORKFLOW.md
│   │   └── push/
│   │       ├── INSTRUCTION.md
│   │       ├── RULES.md
│   │       └── WORKFLOW.md
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
│               ├── mod_push.md
│               └── mod_scan.md
└── tests/
    └── test_cli_toolbox.py
```
