---
doc_id: "ui.dev.rules.product_spatial_field_relation_gate"
doc_type: "ui_dev_guide"
topic: "Field relation gate for product-owned frontend spatial contracts"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_RULES_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This field-relation gate belongs to the frontend rules branch."
  - target: "UI_PRODUCT_MOTHER_DOC_LINT_WORKFLOW.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Field relation checks are executed through the product mother doc lint workflow."
  - target: "UI_PRODUCT_BLUEPRINT_NUMERIC_GATE.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Numeric geometry checks must run after field relation checks succeed."
---

# UI Product Spatial Field Relation Gate

## 目标
- 把前端 mother doc 的 spatial 字段，从“是否存在”升级成“是否形成完整可推理合同”。
- 让 lint 先检查字段关系，再进入数值几何计算。

## 五层门禁
- `schema gate`
  - 键必须完整，值允许为空。
- `activation gate`
  - 某字段值一旦激活，必须带出伴随字段。
- `relational gate`
  - 单边声明不算成立，peer 侧也必须接受。
- `resolution gate`
  - 冲突发生后必须能推出处理策略。
- `geometry gate`
  - 只有前四层通过，才进入 bounds / overlap / overflow 计算。

## 当前首轮关系域
- `allow_overlap`
- `overlap_targets`
- `overlap_mode`
- `collision_policy`
- `elevation`
- `inbound_overlap_policy`
- `occlusion_policy`
- `interaction_states -> responsive_variants`

## 字段分类表
| 字段 | 类别 | 键必须存在 | 激活条件 | 说明 |
|---|---|---:|---|---|
| `allow_overlap` | `activation` | `yes` | `true` | actor 节点是否主动发起 overlap 关系 |
| `overlap_targets` | `structural` | `yes` | `allow_overlap=true` 时必须非空 | actor 指向的 peer 节点集合 |
| `overlap_mode` | `activation` | `yes` | `allow_overlap=true` 时必须非空 | overlap 的行为类型 |
| `collision_policy` | `activation` | `yes` | `allow_overlap=true` 时必须非空 | 几何冲突进入哪种收束策略 |
| `elevation` | `companion` | `yes` | `cover_peer` / `float_above` | actor 的叠放层级意图 |
| `inbound_overlap_policy` | `relational` | `yes` | peer 被引用时参与判定 | peer 是否接受被覆盖/浮层压住 |
| `occlusion_policy` | `relational` | `yes` | peer 被引用且涉及遮挡时参与判定 | peer 是否允许被部分或完全遮挡 |
| `interaction_states` | `activation` | `yes` | 包含 `focus` | 触发状态维度要求 |
| `responsive_variants.panel_focus` | `companion` | `yes` | `interaction_states` 包含 `focus` | 必须给出 focus 态可计算尺寸 |

## 激活依赖表
| 触发字段 | 触发值 | 必须补齐 |
|---|---|---|
| `allow_overlap` | `true` | `overlap_targets`, `overlap_mode`, `collision_policy` |
| `allow_overlap` | `false` | `overlap_targets=[]`, `overlap_mode=null`, `collision_policy=forbid` |
| `overlap_mode` | `cover_peer` | `elevation`, peer `inbound_overlap_policy=allow_declared_cover`, peer `occlusion_policy` 允许遮挡 |
| `overlap_mode` | `float_above` | `elevation`, peer `inbound_overlap_policy=allow_declared_float`, peer `occlusion_policy` 允许遮挡 |
| `overlap_mode` | `edge_bleed` | peer `inbound_overlap_policy=allow_declared_edge_bleed` |
| `interaction_states` | 包含 `focus` | `responsive_variants.panel_focus.frame_width`, `responsive_variants.panel_focus.frame_height` |

## 双边关系表
| actor 行为 | actor 侧要求 | peer 侧要求 | 失败后果 |
|---|---|---|---|
| `cover_peer` | `allow_overlap=true`、`overlap_targets` 包含 peer、`overlap_mode=cover_peer`、`elevation` 非空 | `inbound_overlap_policy=allow_declared_cover` 且 `occlusion_policy` 允许遮挡 | `field_relation.peer_contract_mismatch` |
| `float_above` | `allow_overlap=true`、`overlap_targets` 包含 peer、`overlap_mode=float_above`、`elevation` 非空 | `inbound_overlap_policy=allow_declared_float` 且 `occlusion_policy` 允许遮挡 | `field_relation.peer_contract_mismatch` |
| `edge_bleed` | `allow_overlap=true`、`overlap_targets` 包含 peer、`overlap_mode=edge_bleed` | `inbound_overlap_policy=allow_declared_edge_bleed` | `field_relation.peer_contract_mismatch` |

## 计算顺序表
1. `schema gate`
   键缺失直接失败。
2. `activation gate`
   激活字段触发后的伴随字段未补齐，直接失败。
3. `relational gate`
   actor 与 peer 合同不对齐，直接失败。
4. `resolution gate`
   冲突策略与几何结果预期矛盾，直接失败。
5. `geometry gate`
   最后才执行 bounds / overlap / overflow 计算。

## 当前首轮联动原则
- `allow_overlap=true`
  - 必须非空：`overlap_targets`、`overlap_mode`、`collision_policy`
- `overlap_mode in [cover_peer, float_above]`
  - 必须非空：`elevation`
- `overlap_mode=cover_peer`
  - peer 必须接受：`inbound_overlap_policy=allow_declared_cover`
  - peer 必须允许遮挡：`occlusion_policy in [allow_partial_occlusion, allow_full_occlusion]`
- `overlap_mode=float_above`
  - peer 必须接受：`inbound_overlap_policy=allow_declared_float`
- `allow_overlap=false`
  - `overlap_targets`、`overlap_mode` 必须为空态
  - `collision_policy` 必须为 `forbid`
- `interaction_states` 包含 `focus`
  - `responsive_variants.panel_focus` 必须存在并给出可计算尺寸

## 实现要求
- 这些关系不应散落成局部 if。
- lint 应读取 machine-readable registry，再按 registry 推理。
- registry 当前落在 `assets/runtime/product_spatial_field_relation_registry.json`。
- 产品 mother doc 必须本地化这套关系合同，而不是只引用 skill 文本。
