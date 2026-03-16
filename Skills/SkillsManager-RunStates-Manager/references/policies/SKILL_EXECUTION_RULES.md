---
doc_id: skillsmanager_runstates_manager.references.policies.skill_execution_rules
doc_type: topic_atom
topic: Execution rules for SkillsManager-RunStates-Manager
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This policy defines the stable runstate-governance rules.
---

# Skill Execution Rules

## 核心规则
- `Skills_runtime_checklist` 是 runstate contract schema 的正式字段，不得塞进 `metadata.skill_profile`。
- `workflow_runtime_checklist` 与 `stage_runtime_checklist` 不是可选装饰，而是 workflow-bearing target 的正式治理对象。
- 对 `not_applicable` 目标技能，必须明确返回 `not_applicable`，不得伪造 workflow/stage/skill-flow 中间态要求。
- runstate scaffold 只能在显式 `--target-skill-root` 下写入，不能隐式修改其他目标。
- runstate audit 只负责判断目标技能是否具备、落盘、消费、回填与驱动下一步的 runstate 方法，不直接改目标技能。

## 真实消费判定
- 不能只因为模板文件存在就判定通过。
- 至少要同时看到：
  - runstate contract/schema 已落盘
  - 对应 checklist 模板已落盘
  - 目标技能正文中出现这些 checklist 的消费/回填/推进约束
  - 目标技能正文明确要求“下一步必须消费上一步产物”

## scaffold 成功标准
- 生成目标 `governed_type` 对应的 runstate contract。
- 生成该类型所需的 checklist 模板文件。
- 生成面向目标技能作者的成功判定说明。
- 输出 machine-readable 结果，明确哪些运行层级被要求、哪些被判为 `not_applicable`。

## audit 成功标准
- applicable target 至少满足：
  - runstate contract schema 完整
  - 需要的 checklist 模板完整
  - 目标技能正文中可找到 checklist 消费证据
  - 目标技能正文中可找到“回填后驱动下一步”的约束
- `not_applicable` target 至少满足：
  - 审计结果明确说明 `not_applicable`
  - 没有伪造 checklist 或 runtime file 要求
