---
name: SkillsManager-Creation-Template
description: 提供受治理技能模板与统一 Cli_Toolbox，用于创建或改造 `guide_only`、`guide_with_tool`、`executable_workflow_skill` 三类技能。
skill_mode: guide_with_tool
metadata:
  doc_structure:
    doc_id: skillsmanager_creation_template.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Creation-Template skill
    anchors:
    - target: ./path/template_creation/guide_only/00_GUIDE_ONLY_ENTRY.md
      relation: routes_to
      direction: downstream
      reason: guide_only creation is a top-level function entry.
    - target: ./path/template_creation/guide_with_tool/00_GUIDE_WITH_TOOL_ENTRY.md
      relation: routes_to
      direction: downstream
      reason: guide_with_tool creation is a top-level function entry.
    - target: ./path/template_creation/executable_workflow_skill/00_EXECUTABLE_WORKFLOW_ENTRY.md
      relation: routes_to
      direction: downstream
      reason: executable_workflow_skill creation is a top-level function entry.
    - target: ./path/maintenance/00_MAINTENANCE_ENTRY.md
      relation: routes_to
      direction: downstream
      reason: template maintenance is a top-level function entry.
---

# SkillsManager-Creation-Template

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能只负责两件事：一键落盘三种技能模板，以及维护这三种模板的位置注册。
- 当前模板分三类 `skill_mode`：`guide_only`、`guide_with_tool`、`executable_workflow_skill`。
- 其中 `guide_with_tool` 的语义应理解为单线入口内的 `tool/lint` 能力面，而不是强制每个技能都必须提供业务工具。
- 本技能自身已改为 `path-first / next-hop-only / action-closed-loop` 展示面。
- 技能创建完成后的文档组织、锚点写法、`SKILL.md` 约束与链路维护，后续统一交给 `SkillsManager-Doc-Structure`。
- 不适用于：直接代替目标 skill 编写业务语义，或承担技能创建后的文档结构治理职责。

### 2. 技能约束
- `SKILL.md` 只保留三段：`模型立刻需要知道的事情`、`功能入口` 与 `目录结构图`。
- `SKILL.md` 只暴露功能入口层；不并列暴露深层正文。
- 物理目录组织必须跟随阅读顺序逐级向下，不允许“一个入口文件夹平铺所有后续文件，再仅靠内联控制读序”。
- 根目录只保留：`SKILL.md`、`path/`、`agents/`、`scripts/`。
- 不允许继续保留：`references/`、`assets/`、`tests/` 作为主组织轴。
- 模型沿单条线路阅读时，应优先进入当前动作闭环：
  - `contract`
  - `tools`（可选）
  - `execution`
  - `validation`
- 命令脚本本体统一位于 `scripts/`；命令说明必须写在对应节点文档里。

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
