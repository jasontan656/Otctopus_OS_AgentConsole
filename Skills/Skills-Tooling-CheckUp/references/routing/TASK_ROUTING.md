---
doc_id: "skills_tooling_checkup.routing.task_routing"
doc_type: "routing_doc"
topic: "Task routing for skills tooling dependency-baseline review and remediation"
anchors:
  - target: "../../SKILL.md"
    relation: "implements"
    direction: "upstream"
    reason: "The facade routes readers into this task routing document."
  - target: "../governance/SKILL_DOCSTRUCTURE_POLICY.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Task routing must still pass through the doc-structure policy."
---

# Task Routing

## 当前分叉轴线
- 本文件只按一个语义轴线分流：当前任务是在做只读定位、实改修正，还是要求变更 repo 技术栈基线本身。

## 分支一：只读检查与问题定位
- 先读 `../governance/SKILL_DOCSTRUCTURE_POLICY.md`。
- 再读 `../governance/SKILL_EXECUTION_RULES.md`。
- 若任务涉及运行时日志、调试痕迹、默认产物或定向产物落点，再读 `../governance/OBSERVABILITY_AND_OUTPUT_GOVERNANCE.md`。
- 若需要判断现有依赖是否已覆盖目标能力，再读 `../governance/MANDATORY_TECHSTACK_BASELINE.md`。
- 若需要典型命中样式，再读 `../governance/COMMON_REDUNDANT_WHEEL_PATTERNS.md`。
- 输出应聚焦于：哪些实现是“可能重复造轮子”、日志与产物落盘治理是否闭合、证据是什么、哪些结论仍然未知。

## 分支二：进入目标 skill 做修正
- 先读 `../governance/SKILL_DOCSTRUCTURE_POLICY.md`。
- 再读 `../governance/SKILL_EXECUTION_RULES.md`。
- 再读 `../governance/OBSERVABILITY_AND_OUTPUT_GOVERNANCE.md`、`../governance/MANDATORY_TECHSTACK_BASELINE.md`、`../governance/COMMON_REDUNDANT_WHEEL_PATTERNS.md`、`../governance/REMEDIATION_GATES.md` 与 `../governance/TOOLING_REMEDIATION_PROTOCOL.md`。
- 然后进入目标 skill 自己的 `SKILL.md -> routing -> execution/tooling docs`，按其局部合同执行改写、测试和 lint。
- 若改动落在 Python，额外纳入 `Dev-PythonCode-Constitution-Backend` 的阅读与 lint；若落在 Vue3 / TS tooling，额外纳入目标前端 skill 的既有合同。

## 分支三：用户要改 repo 必用依赖栈
- 这不是本技能单独决策的范围。
- 此分支只负责识别并回退到 repo 合同治理链，不能在本技能内部私自新增、删除或重命名 tech stack 基线。
