---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.entry
doc_type: action_entry_doc
topic: Mother doc entry
reading_chain:
- key: contract
  target: 10_CONTRACT.md
  hop: next
  reason: 先进入 mother_doc 局部合同。
---

# mother_doc 阶段入口

## 当前目标
- 用协议驱动原子文档树，把需求、边界、验收与设计切片固化为唯一需求源。
- mother_doc 不是“直接写几份文档”这么简单；它必须先锁定 runtime，再分析影响面，再检查 code graph，再决定文档树应如何纵向/横向生长，最后才进入状态同步与退出门。
- 模型应主动把语义拆得更细、更结构化、更贴合阅读链；靠近根入口的文档更偏人类叙事，越向外的文档越应主动原子化、参数化、机器友好。
- 当用户意图已经足够明显但尚未指定承载位置时，模型应主动替用户完成层级延伸、横向分支和文档落位裁决，而不是被动等待额外指令。
- 任何新层级或新横向分支一旦被采用，都必须立即固化成可复用规则，不能为单个节点临时发明一次性承载层。

## 下一跳列表
- [contract]：`10_CONTRACT.md`
