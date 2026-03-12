---
doc_id: "skills_tooling_checkup.governance.tooling_remediation_protocol"
doc_type: "topic_atom"
topic: "Protocol for reviewing and remediating self-built tooling wheels in installed skills"
anchors:
  - target: "SKILL_EXECUTION_RULES.md"
    relation: "implements"
    direction: "upstream"
    reason: "Execution rules hand off concrete remediation flow to this protocol."
  - target: "MANDATORY_TECHSTACK_BASELINE.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Review steps depend on the mandatory baseline."
  - target: "COMMON_REDUNDANT_WHEEL_PATTERNS.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Concrete pattern examples live in a separate atomic document."
  - target: "REMEDIATION_GATES.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Replacement gates live in their own atomic document."
---

# Tooling Remediation Protocol

## 本地目的
- 定义本技能如何从“怀疑目标 skill 自造轮子”收敛到“给出证据并完成修正”。

## 执行流程
1. 锁定目标 skill 与具体 tooling code 范围，不做全 repo 漫游式脑补。
2. 读取目标 skill 的门面、routing、execution/tooling 文档，先确认它已有的局部合同。
3. 对照 `MANDATORY_TECHSTACK_BASELINE.md`，找出当前代码是否重复实现了既有依赖已经覆盖的通用能力。
4. 若需要典型模式样本，再进入 `COMMON_REDUNDANT_WHEEL_PATTERNS.md`。
5. 再读取 `REMEDIATION_GATES.md`，确认替换门禁已满足。
6. 修正时优先删除冗余自实现，再接入既有依赖；同步更新目标 skill 的测试、文档、类型或契约。
7. 使用目标 skill 现有测试和 lint 完成验证；若修改 Python，再补 `Dev-PythonCode-Constitution-Backend` lint。
