---
doc_id: skill_creation_template.routing.skill_mode_routing
doc_type: routing_doc
topic: Route readers by skill_mode choice between guide_only, guide_with_tool, and executable_workflow_skill
anchors:
- target: TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing delegates skill-mode selection to this document.
- target: ../governance/SKILL_AUTHORING_RULES.md
  relation: routes_to
  direction: downstream
  reason: All skill modes continue through the shared authoring contract.
- target: ../governance/STAGED_PROFILE_REFERENCE.md
  relation: routes_to
  direction: downstream
  reason: The executable workflow branch needs the specialized staged reference.
---

# Skill Mode Routing

## 当前分叉轴线
- 本文只按 `skill_mode` 分流，不处理任务意图或具体工具细节。
- 文件名保留 `PROFILE_ROUTING.md` 仅为兼容；正文语义已改为 `skill_mode`。

## guide_only 分支
- 目标形态：极简单文件方法论。
- 必读文档：
  - `../governance/SKILL_AUTHORING_RULES.md`
  - `../governance/SKILL_ARCHITECTURE_PLAYBOOK.md`
- 关注输出：
  - `SKILL.md`
  - 顶层 `skill_mode: guide_only`
  - 无额外 doc tree / runtime contract / dedicated CLI

## guide_with_tool 分支
- 目标形态：带文档树与辅助工具面的复合方法论。
- 必读文档：
  - `../governance/SKILL_AUTHORING_RULES.md`
  - `../governance/SKILL_ARCHITECTURE_PLAYBOOK.md`
- 关注输出：
  - facade
  - task routing
  - doc-structure policy
  - execution rules
  - tooling docs

## executable_workflow_skill 分支
- 目标形态：多阶段、CLI-first、强合同面的复合可执行技能。
- 必读文档：
  - `../governance/SKILL_AUTHORING_RULES.md`
  - `../governance/SKILL_ARCHITECTURE_PLAYBOOK.md`
  - `../governance/STAGED_PROFILE_REFERENCE.md`
- 额外关注输出：
  - runtime contract
  - stage index
  - resident docs
  - stage contract 四件套
  - stage-switch discard policy
