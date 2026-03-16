---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.growth_architecture.vertical_layer_registry
doc_type: topic_atom
topic: Mother doc vertical layer registry
reading_chain:
- key: branch_family_registry
  target: 12_HORIZONTAL_BRANCH_FAMILY_REGISTRY.md
  hop: next
  reason: 再确认横向分支家族注册表。
---

# 纵向层级注册表

当前固定纵向 `display_layer`：
1. `overview`
2. `entry`
3. `resolution`
4. `capability`
5. `support`

使用规则：
- 当前层级仍服务“离章鱼头远近”的显示分层，而不是文档语义类型。
- 模型应主动判断当前语义是否已经厚到需要新增一层；一旦决定扩层，就不应回头把这部分语义继续塞回旧层。
- 若未来要新增第六层或更多层，必须先回答：
  - 这层专门承载什么？
  - 为什么现有五层不足以承载？
  - 该层是否能适用于同层其他同类内容？
- 只有以上问题都能回答，才允许先更新本注册表，再把新层写进真实 mother_doc；一旦写入，就应把它当成长期框架的一部分继续复用。

## 下一跳列表
- [branch_family_registry]：`12_HORIZONTAL_BRANCH_FAMILY_REGISTRY.md`
