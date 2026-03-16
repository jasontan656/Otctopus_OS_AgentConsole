---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.contract
doc_type: action_contract_doc
topic: Mother doc contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 mother_doc 合同，再看本阶段工具面。
---

# mother_doc 阶段合同

## Contract Header
- `contract_name`: `workflow_centralflow2_mother_doc_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `single_requirement_source_rule`
  - `atomic_doc_protocol`
  - `substep_order`
  - `stage_exit_gate`
- `optional_fields`:
  - `extension_policy`

- `mother_doc` 是唯一需求源；graph 只能补充现状，不得替代需求源。
- `00_index.md` 是固定根入口，必须由 `mother-doc-refresh-root-index` 自动生成。
- 原子文档协议至少包含：
  - `doc_work_state`
  - `doc_pack_refs`
  - `thumb_title`
  - `thumb_summary`
  - `display_layer`
  - `always_read`
  - `anchors_down`
  - `anchors_support`
- 原子文档协议允许附加产品级语义字段，例如：
  - `doc_kind`
  - `branch_family`
  这些字段不改变最小协议，但用于让模型判断当前节点属于主链节点、分支根、合同文档、场景文档还是交互文档。
- `mother_doc` 完整流程必须按隔离步骤执行：
  1. `scope_and_runtime`
  2. `impact_and_codegraph`
  3. `protocol_tree`
  4. `growth_architecture`
  5. `action_slicing`
  6. `state_and_sync`
  7. `lint_and_exit`
- 鼓励模型按需新增文档、向下扩层或横向长出 B-tree；但任何新增的“层”或“分支家族”一旦采用，必须先在技能内注册，并且必须可复用于同类语义，禁止只为单个节点发明一次性层级。
- 进入 `construction_plan` 之前，`mother-doc-lint` 必须通过。

## 下一跳列表
- [tools]：`15_TOOLS.md`
