---
doc_id: skill_creation_template.routing.profile_routing
doc_type: routing_doc
topic: Route readers by profile choice between basic and staged_cli_first
anchors:
- target: TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing delegates profile selection to this document.
- target: ../governance/SKILL_AUTHORING_RULES.md
  relation: routes_to
  direction: downstream
  reason: Both profile branches continue through the shared authoring contract.
- target: ../governance/STAGED_PROFILE_REFERENCE.md
  relation: routes_to
  direction: downstream
  reason: The staged branch needs the staged profile reference.
---

# Profile Routing

## 当前分叉轴线
- 本文只按 `basic / staged_cli_first` 分流，不处理任务意图或工具细节。

## basic 分支
- 目标形态：单主轴、轻运行面的 skill control plane。
- 必读文档：
  - `../governance/SKILL_AUTHORING_RULES.md`
  - `../governance/SKILL_ARCHITECTURE_PLAYBOOK.md`
- 关注输出：
  - facade
  - task routing
  - doc-structure policy
  - execution rules
  - tooling docs

## staged_cli_first 分支
- 目标形态：多阶段、CLI-first、强合同面的 skill control plane。
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
