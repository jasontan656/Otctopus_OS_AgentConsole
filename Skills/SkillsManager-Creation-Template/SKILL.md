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
    - target: ./path/00_SKILL_ENTRY.md
      relation: routes_to
      direction: downstream
      reason: The facade routes readers into the single path-first entry doc.
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
- `SKILL.md` 只保留三段：`模型立刻需要知道的事情`、`唯一入口` 与 `目录结构图`。
- `SKILL.md` 只指向一个下一级 md；不并列暴露多个深层文件。
- 物理目录组织必须跟随阅读顺序逐级向下，不允许“一个入口文件夹平铺所有后续文件，再仅靠内联控制读序”。
- 根目录只保留：`SKILL.md`、`path/`、`agents/`、`scripts/`。
- 不允许继续保留：`references/`、`assets/`、`tests/` 作为主组织轴。
- 模型沿单条线路阅读时，应优先进入当前动作闭环：
  - `contract`
  - `tools`（可选）
  - `execution`
  - `validation`
- 命令脚本本体统一位于 `scripts/`；命令说明必须写在对应节点文档里。
- 真实规则源以 `runtime-contract --json` 与 machine-readable contract 为准；markdown 负责窄域导航与行为收敛。

### 3. 顶层常驻合同
- `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py runtime-contract --json`
- `path/00_SKILL_ENTRY.md`

## 2. 唯一入口
- [技能主入口]：`path/00_SKILL_ENTRY.md`
  - 作用：把读者送入唯一的 path-first 起点，再按行为分支逐层收窄到当前动作闭环。

## 3. 目录结构图
```text
SkillsManager-Creation-Template/
├── SKILL.md
├── agents/
├── path/
│   ├── 00_SKILL_ENTRY.md
│   ├── template_creation/
│   └── maintenance/
└── scripts/
```
- `path/`：本技能唯一的文档承载面，所有合同、执行说明与校验说明都随节点下沉。
- `scripts/`：CLI 工具、生成器与测试脚本所在目录。
- `agents/`：agent runtime config。
