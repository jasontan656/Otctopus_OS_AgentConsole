---
doc_id: skillsmanager_naming_manager.path.rename_reorg.contract
doc_type: topic_atom
topic: Rename and reorg contract
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: Rename and reorg rules are expanded in the execution doc.
---

# 重命名与重组合同

## 当前动作要完成什么
- 当整体修改技能命名规范、prefix 体系或组织架构时，提供统一治理顺序。
- 避免出现“目录已改名，但 registry 与调用语义仍停留在旧规则”的脱节。

## 当前动作必须满足什么
- 固定顺序必须先治理规则，再治理注册，再治理调用语义，最后才批量改技能目录与 frontmatter。
- 任何重命名或重组都要先盘清受影响的 `canonical_id`、`display_name`、prefix、family 与自然语言短语。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
