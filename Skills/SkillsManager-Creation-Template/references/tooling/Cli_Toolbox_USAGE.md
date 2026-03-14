---
doc_id: skill_creation_template.tooling.usage
doc_type: tooling_usage
topic: Usage guide for the SkillsManager-Creation-Template Cli_Toolbox
anchors:
- target: ../runtime/SKILL_RUNTIME_OVERVIEW.md
  relation: implements
  direction: upstream
  reason: Tool usage must follow the runtime contract.
- target: ../governance/SKILL_AUTHORING_RULES.md
  relation: details
  direction: upstream
  reason: The authoring contract defines what these tools must support.
- target: Cli_Toolbox_DEVELOPMENT.md
  relation: pairs_with
  direction: lateral
  reason: Development documentation complements the usage guide.
---

# Cli_Toolbox 使用文档

适用技能：`SkillsManager-Creation-Template`

## 工具清单
- `Cli_Toolbox.create_skill_from_template`
  - 入口：`scripts/Cli_Toolbox.py create-skill-from-template`
  - 用途：按 `skill_mode` 创建或改造技能骨架。
- `Cli_Toolbox.guide-only-template`
  - 用途：输出 `guide_only` 单文件模板。
- `Cli_Toolbox.guide-with-tool-template`
  - 用途：输出 `guide_with_tool` 门面模板。
- `Cli_Toolbox.executable-workflow-template`
  - 用途：输出 `executable_workflow_skill` 门面模板。
- `Cli_Toolbox.executable-workflow-reference`
  - 用途：输出可执行工作流技能的结构参考。
- 兼容别名：
  - `skill-template -> guide-with-tool-template`
  - `staged-skill-template -> executable-workflow-template`
  - `staged-skill-reference -> executable-workflow-reference`

## create-skill-from-template
- 主参数：
  - `--skill-name`
  - `--target-root`
  - `--resources`
  - `--description`
  - `--skill-mode <guide_only|guide_with_tool|executable_workflow_skill>`
  - `--overwrite`

## 输出差异
- `guide_only`
  - 只输出 `SKILL.md`
- `guide_with_tool`
  - 输出 facade、routing、governance、tooling docs
- `executable_workflow_skill`
  - 在 `guide_with_tool` 基线上再输出 runtime/stages/stage contracts

## 同步维护要求
- 工具行为变化后，必须同步更新：
  - `references/runtime/SKILL_RUNTIME_OVERVIEW.json`
  - `references/runtime/SKILL_RUNTIME_OVERVIEW.md`
  - `references/routing/TASK_ROUTING.md`
  - `references/routing/PROFILE_ROUTING.md`
  - `references/governance/SKILL_AUTHORING_RULES.md`
  - `references/governance/SKILL_ARCHITECTURE_PLAYBOOK.md`
  - `references/governance/STAGED_PROFILE_REFERENCE.md`
  - `assets/skill_template/*`
  - `tests/test_create_skill_from_template_regression.py`
