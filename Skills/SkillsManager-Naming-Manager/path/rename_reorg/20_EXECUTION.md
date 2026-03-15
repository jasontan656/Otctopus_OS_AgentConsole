---
doc_id: skillsmanager_naming_manager.path.rename_reorg.execution
doc_type: topic_atom
topic: Rename and reorg execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Validation closes the rename and reorg chain.
---

# 重命名与重组实施

## 变更类型
- 单技能重命名
- 整个 prefix 改名
- family 拆分或合并
- family code 建立、废弃或改名
- 展示名体系重写
- `canonical_id` 规则升级

## 固定顺序
1. 先定义新的命名规则。
2. 再定义新的 registry 结构。
3. 再明确自然语言调用语义如何迁移。
4. 最后才批量改技能目录与 frontmatter。

## 必查清单
- 哪些技能的 `canonical_id` 需要改。
- 哪些技能只是 `display_name` 需要改。
- 哪些 prefix / family 会受影响。
- 哪些自然语言短语会因此产生歧义。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
