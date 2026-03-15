---
name: SkillsManager-Tooling-CheckUp
description: 治理目标技能内部 CLI 与 tooling surface 的规则规范，重点覆盖依赖基线、输出落点、职责边界、链路编译 CLI 与整改闭环。
skill_mode: guide_with_tool
metadata:
  doc_structure:
    doc_id: skillsmanager_tooling_checkup.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Tooling-CheckUp skill
    reading_chain:
    - key: techstack_baseline
      target: ./path/techstack_baseline/00_TECHSTACK_BASELINE_ENTRY.md
      hop: entry
      reason: techstack baseline checking is a top-level function entry.
    - key: output_governance
      target: ./path/output_governance/00_OUTPUT_GOVERNANCE_ENTRY.md
      hop: entry
      reason: output governance checking is a top-level function entry.
    - key: cli_surface
      target: ./path/cli_surface/00_CLI_SURFACE_ENTRY.md
      hop: entry
      reason: CLI surface checking is a top-level function entry.
    - key: tooling_boundary
      target: ./path/tooling_boundary/00_TOOLING_BOUNDARY_ENTRY.md
      hop: entry
      reason: tooling boundary checking is a top-level function entry.
    - key: remediation
      target: ./path/remediation/00_REMEDIATION_ENTRY.md
      hop: entry
      reason: remediation is a top-level function entry.
---

# SkillsManager-Tooling-CheckUp

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能用于治理目标技能内部的 CLI 与 tooling surface。
- 治理面包括：依赖基线重叠、自造轮子判断、输出落点、CLI 契约、tooling 模块职责边界，以及整改闭环。
- 本技能不治理目标技能的根目录形态、门面形态或 `reading_chain` 设计本身；这些交给文档结构治理链。

### 2. 技能约束
- 本技能治理的是目标技能，不是本技能自身的运行日志或结果沉淀。
- 进入任一功能入口后，沿当前动作闭环继续阅读：
  - `contract`
  - `tools`
  - `execution`
  - `validation`
- 带 `scripts/ + path/` 且不是 `guide_only` 的目标技能，需要提供可工作的 `read-contract-context`；`read-path-context` 可作为等价别名保留。
- `read-contract-context` 输出的是文档真源的编译结果，不是另一套独立真源。
- Python 胖文件、typing 风格、异常风格等语言规范继续交给对应 constitution。

### 3. 顶层常驻合同
- 全局合同直接写在本门面中，不额外外跳到 CLI 合同。
- 后续阅读只沿当前选中的功能入口继续下沉。
- 本技能自身默认只通过 CLI stdout/stderr/JSON 返回审计结果，不在 skill 目录或受管根路径下持久化自有运行日志或结果文件。

## 2. 功能入口
- [依赖基线检查]：`path/techstack_baseline/00_TECHSTACK_BASELINE_ENTRY.md`
  - 作用：判断目标技能的自实现是否与 repo 既定依赖栈能力重叠。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry techstack_baseline --json`
- [输出落点检查]：`path/output_governance/00_OUTPUT_GOVERNANCE_ENTRY.md`
  - 作用：检查目标技能的 runtime 日志、默认产物、定向产物与迁移责任是否闭合。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry output_governance --json`
- [CLI Surface 检查]：`path/cli_surface/00_CLI_SURFACE_ENTRY.md`
  - 作用：检查目标技能的 CLI 入口、参数契约、JSON 输出、错误返回与链路编译能力。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry cli_surface --json`
- [Tooling 职责边界检查]：`path/tooling_boundary/00_TOOLING_BOUNDARY_ENTRY.md`
  - 作用：检查 parser / schema / helper / lint / test / glue 是否越权承载了域内规则。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry tooling_boundary --json`
- [整改入口]：`path/remediation/00_REMEDIATION_ENTRY.md`
  - 作用：在证据充分后，进入行为保持型 tooling 整改闭环。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry remediation --json`

## 3. 目录结构图
```text
SkillsManager-Tooling-CheckUp/
├── SKILL.md
├── agents/
├── path/
│   ├── techstack_baseline/
│   ├── output_governance/
│   ├── cli_surface/
│   ├── tooling_boundary/
│   └── remediation/
└── scripts/
```
- `path/`：本技能唯一的文档承载面，所有规则、步骤与校验都随功能入口下沉。
- `scripts/`：CLI 工具、运行时帮助模块与回归测试所在目录。
- `agents/`：agent runtime config。
