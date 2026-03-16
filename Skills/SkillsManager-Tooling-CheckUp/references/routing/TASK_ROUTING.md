---
doc_id: skillsmanager_tooling_checkup.references.routing.task_routing
doc_type: topic_atom
topic: Task routing for contract-first tooling audits
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This routing guide belongs to the governed skill tree under the facade.
---

# SkillsManager-Tooling-CheckUp Task Routing

## 任务入口
- 当任务是“这个技能有没有稳定 machine contract”，运行 `audit`。
- 当任务是“它的 CLI/tooling 表面是否成立”，运行 `audit`。
- 当任务是“artifact policy 是否干净”，运行 `audit`，重点看 `artifact_policy` 子结果。

## 审计顺序
1. 先探测 target skill 是否有 scripts 和 CLI 入口。
2. 再读取 runtime contract 文件；若缺失，再尝试 CLI `contract --json`。
3. 再根据 contract 内容检查 tooling surface 和 artifact policy。
4. 最后输出 remediation gate，而不是直接代改 target skill。
