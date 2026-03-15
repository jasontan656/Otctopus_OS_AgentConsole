---
doc_id: skillsmanager_doc_structure.path.primary_flow.validation
doc_type: topic_atom
topic: Final validation for the primary doc-structure governance flow
---

# 最终校验

## 校验
- `lint-root-shape` 结果为 `ok`。
- `lint-reading-chain` 结果为 `ok`。
- `compile-reading-chain` 能沿目标技能选中的入口成功输出完整上下文，或在复合节点返回 `branch_selection_required`。
- `lint-docstructure` 汇总结果为 `ok`。
- 模型完成一轮语义审查，确认各层正文没有越层、串层或重新集中成总则。

## 完成后意味着什么
- 目标技能已经按照其目标形态组织根目录。
- 目标技能的门面与路径链路职责已经分离清楚。
- reading-chain 只保留必要关系，没有继续用旧结构污染阅读路径。
