---
doc_id: skills_tooling_checkup.governance.tooling_remediation_protocol
doc_type: topic_atom
topic: Protocol for reviewing and remediating self-built tooling wheels in installed
  skills
reading_chain:
- key: common_redundant_wheel_patterns
  target: COMMON_REDUNDANT_WHEEL_PATTERNS.md
  hop: branch
  reason: Concrete pattern examples live in a separate atomic document.
- key: remediation_gates
  target: REMEDIATION_GATES.md
  hop: branch
  reason: Replacement gates live in their own atomic document.
---

# Tooling Remediation Protocol

## 本地目的
- 定义本技能如何从“怀疑目标 skill 自造轮子”收敛到“给出证据并完成修正”。

## 执行流程
1. 锁定目标 skill 与具体 tooling code 范围，不做全 repo 漫游式脑补。
2. 读取目标 skill 的门面、routing、execution/tooling 文档，先确认它已有的局部合同。
3. 若任务涉及日志、调试痕迹、默认产物或定向产物，再对照 `OBSERVABILITY_AND_OUTPUT_GOVERNANCE.md` 检查代码语义、文档声明与历史落盘现状。
4. 对照 `MANDATORY_TECHSTACK_BASELINE.md`，找出当前代码是否重复实现了既有依赖已经覆盖的通用能力。
5. 若任务涉及 CLI 命令面、参数或 JSON 输出，则补读 runtime 的 `cli-surface` 合同；若任务涉及 parser/schema/helper/lint/test/glue 职责，则补读 runtime 的 `tooling-boundary` guide。
6. 若需要典型模式样本，再进入 `COMMON_REDUNDANT_WHEEL_PATTERNS.md`。
7. 再读取 `REMEDIATION_GATES.md`，确认替换门禁已满足。
8. 修正时优先删除冗余自实现，再接入既有依赖；若命中落盘治理，还要同步修正默认路径、显式落点参数、文档声明与旧内容迁移方案。
9. 若问题只是语言专属代码规范，不在本协议内修正；改交对应语言 constitution。
10. 使用目标 skill 现有测试和 lint 完成验证；若修改 Python，再补 `Dev-PythonCode-Constitution` lint。
