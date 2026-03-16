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

## Contract Header
- `contract_name`: `workflow_centralflow2_mother_doc_growth_architecture_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `tree_growth_rule`
  - `reusable_registry_rule`
  - `no_single_use_family_rule`
- `optional_fields`:
  - `notes`

- 模型应主动向外扩散，并优先把当前语义拆成更细、更清楚、更像框架树的承载结构；只要现有节点已经同时承载多个独立语义，就优先考虑新增长分支或新层，而不是继续堆叠正文。
- 模型应主动横向长出 B-tree；overview 节点、主链节点和 layer 节点都默认拥有继续长树的资格，同层兄弟不互连，但各自都可以长出自己的支撑树。
- 当用户意图已经足够明确但没有显式指定承载位置时，模型应主动代替用户做出分叉裁决、承载裁决和落位裁决，并对自己的裁决保持信心。
- 鼓励模型为同类文档定义固定内容结构，让越靠近根入口的文档越贴近人类叙事，让越向外生长的文档越主动原子化、参数化、机器可执行。
- 任何新增的“纵向层”一旦采用，必须先在 skill 内注册，并且必须能适用于同层其他同类语义。
- 任何新增的“横向分支家族”一旦采用，也必须先注册，并且必须可复用于其他同类节点。
- 任何新增的“内容结构家族”一旦采用，也必须先注册，并且必须能适用于同类文档，不得只为单个节点发明一次性写法。
- 禁止为单个节点临时发明一次性层或一次性分支；不存在 `john` 一套、`mike` 一套的私有语义承载层。
- 一旦某一层、某一横向分支家族、某一内容结构家族被采用，它就属于固定框架的一部分；后续同类语义必须继续复用，不得重新发明另一套平行承载方式。

## 下一跳列表
- [vertical_layer_registry]：`11_VERTICAL_LAYER_REGISTRY.md`
