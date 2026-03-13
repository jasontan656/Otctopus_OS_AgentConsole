---
doc_id: "ui.dev.container.permission_code_placement"
doc_type: "ui_dev_guide"
topic: "Permission, visibility, code placement, and testability rules for showroom containers"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_CONTAINER_GOVERNANCE_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This governance contract belongs to the governance branch."
  - target: "../../positioning/UI_FILE_ORGANIZATION.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Container governance refines the broader file-organization contract."
  - target: "../state/10_CONTAINER_STATE_OWNERSHIP.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Read/write permissions are meaningful only when state ownership is clear."
---

# Container Permission Code Placement

## 权限与可见性
- 当前 viewer 以文档浏览为主，容器的权限边界主要体现为读写权边界，而不是用户角色系统。
- `RuntimeStatusContainer` 与 `DocumentReaderContainer` 可见不等于可修改；它们默认只读。
- 写入 selection 和 search 的权限集中在 `ShowroomWorkspaceContainer`。

## 权限记录字段
- `action`
  - 记录容器试图执行的动作，例如 `selection.update`。
- `actor_id`
  - 记录触发动作的容器，例如 `DocumentNavigatorContainer`。
- `scope`
  - 记录动作生效域，例如 `workspace.selection`。
- `authz_result`
  - 记录是否允许该动作。
- `deny_code`
  - 若拒绝动作，记录拒绝原因。
- `policy_version`
  - 记录当前前端容器权限合同版本。

## 代码落点
- 下一轮代码重建时，预期代码根落在具体产品代码仓，而不是本技能目录。
- 未来实现应至少区分：
  - `containers/`
  - `components/`
  - `composables/`
  - `contracts/`
- 当前轮次不保留旧代码目录，避免把失效实现误读成正式落点。

## 测试面
- stage 合同与合同路由继续由 `tests/test_cli_toolbox.spec.ts` 保障。
- 当前轮次先以合同和文档 graph 约束为主；新的 UI 代码落地后再补回实现级测试面。
