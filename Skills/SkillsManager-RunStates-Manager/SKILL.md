---
name: SkillsManager-RunStates-Manager
description: 治理目标技能的 workflow/stage/skill-flow 三层运行态文件方法、checklist schema、runstate scaffold 与 runstate audit。
metadata:
  skill_profile:
    doc_topology: referenced
    tooling_surface: automation_cli
    workflow_control: guardrailed
  doc_structure:
    doc_id: skillsmanager_runstates_manager.entry.facade
    doc_type: skill_facade
    topic: Entry facade for SkillsManager-RunStates-Manager
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the runtime contract.
    - target: ./references/routing/TASK_ROUTING.md
      relation: routes_to
      direction: downstream
      reason: The routing note explains where runstates sits in the skill-governance chain.
---

# SkillsManager-RunStates-Manager

## Runtime Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-RunStates-Manager/scripts/Cli_Toolbox.py contract --json`
- Inspect entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-RunStates-Manager/scripts/Cli_Toolbox.py inspect --target-skill-root <path> --json`
- Scaffold entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-RunStates-Manager/scripts/Cli_Toolbox.py scaffold --target-skill-root <path> [--governed-type auto] --json`
- Audit entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-RunStates-Manager/scripts/Cli_Toolbox.py audit --target-skill-root <path> --json`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.

## 1. 技能定位
- 本技能不是新的顶层 workflow orchestrator，也不接管宿主技能的业务闭环。
- 本技能是技能创建/治理链中的新增一步 `runstates`，固定插入在 `SkillsManager-Tooling-CheckUp` 之前。
- 本技能既可作为治理步骤嵌入 `template -> doc_structure -> runstates -> tooling`，也可单独调用来治理一个目标技能。
- 本技能只治理目标技能是否正确具备并正确应用以下运行态方法：
  - `Skills_runtime_checklist`
  - `workflow_runtime_checklist`
  - `stage_runtime_checklist`
- 本技能要求这些中间态方法不只是文档命名存在，而是能够真实约束：
  - 上一步产物被下一步消费
  - 每个原子步骤结束后立即回填
  - 回填结果驱动下一步
  - 禁止跳步、并步与“一步到位结束”

## 2. 必读顺序
1. 先读取 `references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md`。
2. 再读取 `references/routing/TASK_ROUTING.md`。
3. 再读取 `references/policies/SKILL_EXECUTION_RULES.md`。
4. 真正执行时，根据任务进入：
   - `inspect`
   - `scaffold`
   - `audit`

## 3. 分类入口
- 路由层：
  - `references/routing/TASK_ROUTING.md`
- 规则层：
  - `references/policies/SKILL_EXECUTION_RULES.md`
- runtime 合同：
  - `references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md`
- tooling 层：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`

## 4. 适用域
- 适用于：为目标技能建立 runstate contract schema、三层 checklist 模板与中间态文件方法。
- 适用于：审计一个目标技能是否真的具备 workflow/stage/skill-flow 三层运行态承载方式。
- 适用于：在技能创建或技能治理流程中，作为 `runstates` 步骤插到 `SkillsManager-Tooling-CheckUp` 之前。
- 不适用于：替代 `SkillsManager-Creation-Template` 生成目标技能整体骨架。
- 不适用于：替代 `SkillsManager-Doc-Structure` 做拓扑 lint。
- 不适用于：替代 `SkillsManager-Tooling-CheckUp` 做 contract/tooling/artifact policy 审计。
