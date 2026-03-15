---
name: SkillsManager-Creation-Template
description: 提供受治理技能模板与统一 Cli_Toolbox，用于创建或改造 `guide_only`、`guide_with_tool`、`executable_workflow_skill`
  三类技能。
skill_mode: guide_with_tool
metadata:
  doc_structure:
    doc_id: skillsmanager_creation_template.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Creation-Template skill
    reading_chain:
    - key: guide_only
      target: ./path/template_creation/guide_only/00_GUIDE_ONLY_ENTRY.md
      hop: entry
      reason: guide_only creation is a top-level function entry.
    - key: guide_with_tool
      target: ./path/template_creation/guide_with_tool/00_GUIDE_WITH_TOOL_ENTRY.md
      hop: entry
      reason: guide_with_tool creation is a top-level function entry.
    - key: executable_workflow
      target: ./path/template_creation/executable_workflow_skill/00_EXECUTABLE_WORKFLOW_ENTRY.md
      hop: entry
      reason: executable_workflow_skill creation is a top-level function entry.
    - key: maintenance
      target: ./path/maintenance/00_MAINTENANCE_ENTRY.md
      hop: entry
      reason: template maintenance is a top-level function entry.
---

# SkillsManager-Creation-Template

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能用于创建三种技能模板，并查看这些模板的注册位置。
- 当前模板分三类 `skill_mode`：`guide_only`、`guide_with_tool`、`executable_workflow_skill`。
- 其中 `guide_with_tool` 的语义应理解为单线入口内的 `tool/lint` 能力面，而不是强制每个技能都必须提供业务工具。

### 2. 技能约束
- 模型沿单条线路阅读时，应优先进入当前动作闭环：
  - `contract`
  - `tools`（可选）
  - `execution`
  - `validation`
- `guide_only` 目标形态只生成 `SKILL.md / agents`。
- 其余两类模板会生成 `SKILL.md / path / agents / scripts`。
- 带 `scripts/` 的模板目标态包含 `read-path-context`。

### 3. 顶层常驻合同
- 全局合同直接写在本门面中，不额外外跳到 CLI 合同。
- 后续阅读只沿当前选中的功能入口继续下沉。

## 2. 功能入口
- [guide_only]：`path/template_creation/guide_only/00_GUIDE_ONLY_ENTRY.md`
  - 作用：创建最小技能形态，只落 `SKILL.md / agents`。
- [guide_with_tool]：`path/template_creation/guide_with_tool/00_GUIDE_WITH_TOOL_ENTRY.md`
  - 作用：创建单线闭环技能；允许多入口，但入口内不能再分叉。
- [executable_workflow_skill]：`path/template_creation/executable_workflow_skill/00_EXECUTABLE_WORKFLOW_ENTRY.md`
  - 作用：创建复合 workflow 技能；入口内允许继续下沉到复合步骤。
- [模板维护]：`path/maintenance/00_MAINTENANCE_ENTRY.md`
  - 作用：维护三种模板的注册位置，不进入创建链路。

## 3. 目录结构图
```text
SkillsManager-Creation-Template/
├── SKILL.md
├── agents/
├── path/
│   ├── template_creation/
│   └── maintenance/
└── scripts/
```
- `path/`：本技能唯一的文档承载面，所有合同、执行说明与校验说明都随节点下沉。
- `scripts/`：CLI 工具、生成器与测试脚本所在目录。
- `agents/`：agent runtime config。
