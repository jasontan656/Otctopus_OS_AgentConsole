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
- `ui-dev/client/src/containers/`
  - 放置应用壳层、scene、workspace、panel 等容器。
- `ui-dev/client/src/components/`
  - 放置如 `GraphCanvas` 这类无全局状态所有权的展示组件。
- `ui-dev/client/src/composables/`
  - 放置 runtime bridge、derived view model 一类组合逻辑。
- `ui-dev/client/src/contracts/`
  - 放置前端容器 typed contract 与共享 UI 协议类型。

## 测试面
- payload 归一化继续由 `ui-dev/tests/test_viewer_payload.spec.ts` 保障。
- stage 合同与合同路由继续由 `tests/test_cli_toolbox.spec.ts` 保障。
- 容器拆分后的 UI 行为应优先通过 typecheck、build 和已有 runtime 测试守住。
