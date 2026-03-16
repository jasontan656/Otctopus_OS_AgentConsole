---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.protocol_tree.contract
doc_type: action_contract_doc
topic: Mother doc protocol tree contract
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: 进入当前步骤执行说明。
---

# protocol_tree 合同

## Contract Header
- `contract_name`: `workflow_centralflow2_mother_doc_protocol_tree_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `root_entry_rule`
  - `frontmatter_protocol`
  - `anchor_consistency_rule`
- `optional_fields`:
  - `display_layer_notes`

- 只允许 `00_index.md` 作为根入口。
- 原子文档必须满足 frontmatter 最小协议，并保持 `anchors_down / anchors_support` 一致。
- 原子文档必须显式声明 `doc_kind` 与 `content_family`，方便模型在读取链中立刻知道“这是什么语义、该怎么读、该怎么继续长”。
- `display_layer` 在本步骤里只表示显示分层，不负责决定是否扩层。
- `anchors_down` 与 `anchors_support` 都是遍历集合，不是单条边。
- `doc_kind`、`branch_family` 若出现，只是协议附加语义；本步骤不决定它们是否合法扩展，合法性由后续 `growth_architecture` 处理。
- 本步骤应把树协议写成“天然鼓励继续细化”的样子：只要节点还在同时承载多个独立语义，就不应把它伪装成最终形态。
- 靠近根入口的协议文档应优先服务人类阅读；中后段协议文档应优先服务模型快速定位、快速落盘和快速执行。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
