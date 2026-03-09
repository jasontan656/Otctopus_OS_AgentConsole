---
name: "Meta-Default-md-manager"
description: "集中管理 workspace 内的常驻默认文档。显式分离 scan、collect、push 三阶段；运行态规则与阶段指引必须通过 CLI 输出，markdown 仅供人类审计。"
---

# Meta-Default-md-manager

## 1. 目标
- 提供常驻默认文档的集中管理入口，默认管理 `AGENTS.md`、所有目录的 `.gitignore`、以及 `Octopus_CodeBase_Backend/README.md`、`Octopus_CodeBase_Backend/Deployment_Guide.md`。
- `Octopus_OS` 是显式排除域；其内部全部 `AGENTS.md` / `README.md` 由 `2-Octupos-FullStack` 自己的 AGENTS/README manager 独占管理。
- 统一 CLI 入口为 `scripts/Cli_Toolbox.py`。
- 阶段命令必须显式分离：
  - `scan`
  - `collect`
  - `push`
- 运行态规则、约束、指引必须通过 CLI 输出；模型禁止直接阅读 markdown 获取运行指引。

## 2. 可用工具
- 工具入口：`scripts/Cli_Toolbox.py`
- 命令清单：
  - `Cli_Toolbox.contract`
  - `Cli_Toolbox.directive`
  - `Cli_Toolbox.render_audit_docs`
  - `Cli_Toolbox.registry`
  - `Cli_Toolbox.scan`
  - `Cli_Toolbox.collect`
  - `Cli_Toolbox.push`
- 运行态读取约束：
  - 先执行 `contract` 获取技能级合同。
  - 再执行 `directive --stage <scan|collect|push>` 获取阶段指引。
  - `references/**/*.md` 只供人类审计，不是模型运行时规则源。

## 3. 工作流约束
- 技能级运行合同入口：
  - machine: `references/runtime/SKILL_RUNTIME_CONTRACT.json`
  - CLI: `python3 scripts/Cli_Toolbox.py contract --json`
  - audit: `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- `scan` 阶段入口：
  - machine: `references/stages/scan/DIRECTIVE.json`
  - CLI: `python3 scripts/Cli_Toolbox.py directive --stage scan --json`
  - audit: `references/stages/scan/INSTRUCTION.md` / `WORKFLOW.md` / `RULES.md`
- `collect` 阶段入口：
  - machine: `references/stages/collect/DIRECTIVE.json`
  - CLI: `python3 scripts/Cli_Toolbox.py directive --stage collect --json`
  - audit: `references/stages/collect/INSTRUCTION.md` / `WORKFLOW.md` / `RULES.md`
- `push` 阶段入口：
  - machine: `references/stages/push/DIRECTIVE.json`
  - CLI: `python3 scripts/Cli_Toolbox.py directive --stage push --json`
  - audit: `references/stages/push/INSTRUCTION.md` / `WORKFLOW.md` / `RULES.md`

## 4. 规则约束
- `SKILL.md` 只保留入口、边界和导航，不承载可直接执行的阶段细节。
- `scan / collect / push` 必须通过技能内互斥锁串行运行，禁止并行。
- `scan` 不允许写托管副本。
- `collect` 不允许重新扫描文件系统，只允许消费 `scan_report.json`。
- `push` 不允许绕过 `registry.json` 直接推断目标。
- `collect` 消费的 `scan_report.json` 不存在、为空或无条目时，必须显式报错。
- `push` 消费的 `registry.json` 不存在、为空或无条目时，必须显式报错。
- 除 `push` 对外回写源文件外，技能所有产物必须留在技能内部 `assets/managed_targets/`。
- 运行合同与阶段指引必须同时存在两份：
  - markdown 审计版
  - machine-readable JSON 版
- 约束更新时必须先更新 JSON，再运行 `render-audit-docs` 刷新 markdown 审计版。

## 5. 方法论约束
- 先 `contract`，再 `directive`，最后执行 `scan / collect / push`。
- 先 `scan`，再 `collect`，最后 `push`。
- 如果用户只要求某一阶段，只读取该阶段对应的 CLI 指引输出。
- 如果用户未显式要求审计 markdown，不读取 `references/**/*.md` 作为运行依据。

## 6. 内联导航索引
- [Cli_Toolbox 工具入口] -> [scripts/Cli_Toolbox.py]
- [运行合同 JSON] -> [references/runtime/SKILL_RUNTIME_CONTRACT.json]
- [运行合同审计版] -> [references/runtime/SKILL_RUNTIME_CONTRACT.md]
- [Scan Directive JSON] -> [references/stages/scan/DIRECTIVE.json]
- [Collect Directive JSON] -> [references/stages/collect/DIRECTIVE.json]
- [Push Directive JSON] -> [references/stages/push/DIRECTIVE.json]
- [托管 registry] -> [assets/managed_targets/registry.json]
- [托管索引] -> [assets/managed_targets/index.md]
- [扫描报告] -> [assets/managed_targets/scan_report.json]

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
│   ├── managed_guidance.py
│   ├── managed_index.py
│   ├── managed_lock.py
│   ├── managed_paths.py
│   ├── managed_push.py
│   ├── managed_registry.py
│   └── managed_scan.py
├── references/
│   ├── runtime/
│   │   ├── SKILL_RUNTIME_CONTRACT.json
│   │   └── SKILL_RUNTIME_CONTRACT.md
│   ├── stages/
│   │   ├── scan/
│   │   │   ├── DIRECTIVE.json
│   │   │   ├── INSTRUCTION.md
│   │   │   ├── RULES.md
│   │   │   └── WORKFLOW.md
│   │   ├── collect/
│   │   │   ├── DIRECTIVE.json
│   │   │   ├── INSTRUCTION.md
│   │   │   ├── RULES.md
│   │   │   └── WORKFLOW.md
│   │   └── push/
│   │       ├── DIRECTIVE.json
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
│               ├── mod_guidance.md
│               ├── mod_push.md
│               └── mod_scan.md
└── tests/
    └── test_cli_toolbox.py
```
