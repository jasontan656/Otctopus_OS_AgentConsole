---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.growth_architecture.contract
doc_type: action_contract_doc
topic: Mother doc growth architecture contract
reading_chain:
- key: vertical_layer_registry
  target: 11_VERTICAL_LAYER_REGISTRY.md
  hop: next
  reason: 先确认纵向层级注册表。
---

# growth_architecture 合同

- 鼓励模型向外扩散，但任何新增的“纵向层”一旦采用，必须先在 skill 内注册，并且必须能适用于同层其他同类语义。
- 鼓励模型横向长出 B-tree，但任何新增的“横向分支家族”一旦采用，也必须先注册，并且必须可复用于其他同类节点。
- 鼓励模型为同类文档定义固定内容结构；任何新增的“内容结构家族”一旦采用，也必须先注册，并且必须能适用于同类文档，不得只为单个节点发明一次性写法。
- 禁止为单个节点临时发明一次性层或一次性分支；不存在 `john` 一套、`mike` 一套的私有语义承载层。
- 主链节点、overview 节点和 layer 节点都允许继续长出 B-tree；同层兄弟默认不互连，但各自都可以长自己的支撑树。
- 越靠近根入口的文档，越应保持人类叙事；越向外生长的文档，越允许原子化、参数化、机器可执行。
- 一旦某一层、某一横向分支家族、某一内容结构家族被采用，它就属于固定框架的一部分；后续同类语义必须继续复用，不得重新发明另一套平行承载方式。

## 下一跳列表
- [vertical_layer_registry]：`11_VERTICAL_LAYER_REGISTRY.md`
