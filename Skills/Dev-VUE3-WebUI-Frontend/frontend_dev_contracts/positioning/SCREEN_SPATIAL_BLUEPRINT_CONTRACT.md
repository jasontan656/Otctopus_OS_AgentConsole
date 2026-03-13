---
doc_id: "ui.tool.spatial_blueprint_contract"
doc_type: "ui_dev_guide"
topic: "Screen spatial blueprint contract for AI-readable frontend layout planning"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_POSITIONING_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This blueprint contract belongs to the positioning branch."
  - target: "../containers/layout/10_APP_SHELL_AND_WORKSPACE_LAYOUT_AUTHORITY.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Spatial blueprints instantiate layout authority into concrete coordinates and constraints."
  - target: "../rules/UI_LAYOUT_ADJUSTMENT_RULES.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Responsive adjustment rules apply to spatial blueprints instead of bypassing them."
  - target: "../../references/stages/20_STAGE_SURFACE_LAYOUTS.md"
    relation: "supports"
    direction: "upstream"
    reason: "Stage surface planning must be expressible through this spatial blueprint grammar."
---

# Screen Spatial Blueprint Contract

## 目标
- 为 AI 提供可落在 markdown / yaml / json 中的屏幕空间描述系统。
- 让布局理解基于 `viewport + coordinates + constraints + relations`，而不是只靠自然语言猜测“左边、右边、上面、下面”。
- 避免把空间规划直接降成 DOM 实现细节；blueprint 只负责空间结构，不负责框架代码。

## 基本原则
- 任何复杂前端界面都应至少拥有一份 `viewport baseline blueprint`。
- 当 layout 不再只是简单流式排版时，必须使用 spatial blueprint，而不是只留段落叙事。
- blueprint 是合同，不是视觉稿；它描述的是空间位置、尺寸、层级、约束、关系。
- layout authority 决定谁有权摆放对象；spatial blueprint 决定对象摆在哪里、占多大、相对谁约束。

## 必填字段
- `viewport_id`
- `viewport_width`
- `viewport_height`
- `node_id`
- `parent_id`
- `x`
- `y`
- `w`
- `h`
- `z`
- `anchor`
- `layout_mode`
- `constraints`
- `purpose`

## 推荐扩展字段
- `surface_id`
- `component_seed_id`
- `state_variant`
- `relation_refs`
- `overflow_policy`
- `allow_overlap`
- `overlap_targets`
- `overlap_mode`
- `collision_policy`
- `inbound_overlap_policy`
- `occlusion_policy`
- `elevation`
- `scroll_axis`
- `grid_span`
- `min_w`
- `min_h`
- `max_w`
- `max_h`

## 空间关系词表
- `inside`
- `above`
- `below`
- `left_of`
- `right_of`
- `overlap`
- `fills_parent`
- `sticky_to`
- `centered_in`
- `pinned_top`
- `pinned_bottom`
- `stack_after`

## 维度语义
- `x`, `y`, `w`, `h`
  - 默认表示二维平面中的矩形边界。
- `z`
  - 表示空间层级和覆盖顺序，不等于视觉样式本身。
- 若产品需要空间立体感，可继续增加：
  - `elevation`
  - `surface_level`
  - `depth_relation`

## 坐标系要求
- 至少同时维护两种坐标：
  - 全局 `viewport` 坐标
  - 局部 `parent container` 坐标
- 子节点坐标默认相对其 `parent_id`。
- 当节点跨容器联动时，使用 `relation_refs` 描述，不允许靠口头解释。

## 最小蓝图示例
```yaml
viewport:
  viewport_id: desktop_default
  viewport_width: 1440
  viewport_height: 900

nodes:
  - node_id: shell.root
    parent_id: viewport
    x: 0
    y: 0
    w: 1440
    h: 900
    z: 0
    anchor: top_left
    layout_mode: fixed
    constraints: [fills_parent]
    purpose: product shell

  - node_id: nav.sidebar
    parent_id: shell.root
    x: 20
    y: 20
    w: 320
    h: 860
    z: 2
    anchor: top_left
    layout_mode: fixed
    constraints: [sticky_to]
    purpose: navigation rail
```

## 产品侧落盘要求
- 技能只定义 grammar，不保留具体产品蓝图。
- 具体产品必须把以下内容落在产品 mother doc：
  - `viewport baseline`
  - `workspace default blueprint`
  - `state blueprints`，例如 panel open/focus/split 等状态
