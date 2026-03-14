---
name: SkillsManager-Creation-Template
description: 提供受治理技能模板与统一 Cli_Toolbox，用于创建或改造 `guide_only`、`guide_with_tool`、`executable_workflow_skill` 三类技能。
metadata:
  doc_structure:
    doc_id: skillsmanager_creation_template.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Creation-Template skill
    anchors:
    - target: ./references/runtime/SKILL_RUNTIME_OVERVIEW.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the runtime overview contract.
---

# SkillsManager-Creation-Template

## 1. Immediate Contract
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py runtime-contract --json`
- `SKILL.md` 只保留 `Immediate Contract` 与 `Structured Entry` 两段，不承载模板治理正文。
- 本技能负责把“创建新技能”“治理既有 skill”“维护模板资产与生成器”收敛为同一套模板控制面。
- 当前模板分三类 `skill_mode`：`guide_only`、`guide_with_tool`、`executable_workflow_skill`。
- 真实规则源以 CLI JSON 与 machine-readable contracts 为准；markdown 只做人类审计与窄域导航。
- `guide_only` 是单文件例外；只有 `guide_with_tool` 与 `executable_workflow_skill` 必须保持极简 façade。
- 若某段内容既不是模型必须立刻知道的约束，也不是下一跳结构化入口，就必须下沉到 routing、topic、index 或 tooling docs。
- 不适用于：直接代替目标 skill 编写业务语义，或替代 mirror / git / installer 职责。

## 2. Structured Entry
1. 先读取 `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py runtime-contract --json`。
2. 再读取 `references/routing/TASK_ROUTING.md`，按任务意图分流。
3. 若任务涉及 `skill_mode` 选择，再读取 `references/routing/PROFILE_ROUTING.md`。
4. 若任务涉及新建或治理 skill 结构，必须读取 `references/governance/SKILL_DOCSTRUCTURE_ENFORCEMENT.md`。
5. 真正动手前，再按分支进入 `SKILL_AUTHORING_RULES.md`、`SKILL_ARCHITECTURE_PLAYBOOK.md`、`STAGED_PROFILE_REFERENCE.md`、`DOC_TREE.md` 或 tooling docs。
- 入口：
  - `references/runtime/SKILL_RUNTIME_OVERVIEW.json`
  - `references/runtime/SKILL_RUNTIME_OVERVIEW.md`
  - `references/routing/TASK_ROUTING.md`
  - `references/routing/PROFILE_ROUTING.md`
  - `references/governance/SKILL_DOCSTRUCTURE_ENFORCEMENT.md`
  - `references/governance/SKILL_AUTHORING_RULES.md`
  - `references/governance/SKILL_ARCHITECTURE_PLAYBOOK.md`
  - `references/governance/STAGED_PROFILE_REFERENCE.md`
  - `references/indexes/DOC_TREE.md`
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py create-skill-from-template --skill-name <name> --target-root <path> --skill-mode <guide_only|guide_with_tool|executable_workflow_skill> --overwrite`
