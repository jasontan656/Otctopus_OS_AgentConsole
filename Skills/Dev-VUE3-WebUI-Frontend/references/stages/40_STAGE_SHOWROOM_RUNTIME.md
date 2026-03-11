---
doc_id: "stages.showroom_runtime"
doc_type: "stage_doc"
topic: "Runnable showroom and runtime delivery stage for the Vue3 web UI frontend skill"
anchors:
  - target: "../../ui-dev/UI_DEV_ENTRY.md"
    relation: "implements"
    direction: "downstream"
    reason: "The runnable showroom root is the concrete execution surface of this stage."
  - target: "../../frontend_dev_contracts/containers/state/20_CONTAINER_PAYLOAD_NORMALIZATION.md"
    relation: "details"
    direction: "downstream"
    reason: "The payload normalization contract defines the runtime bridge input boundary for the showroom."
  - target: "../../references/tooling/development/modules/mod_showroom_runtime.md"
    relation: "explained_by"
    direction: "downstream"
    reason: "The showroom runtime module documents server, viewer, and service responsibilities."
---

# Stage Showroom Runtime

## 本阶段负责
- dev server、production build、user-level service、live payload 刷新。
- 展厅页面与真实技能文档变化保持同步。
- 让人类可以直接看到前端规范如何在真实页面中落地。
- 让 runtime bridge、workspace 容器、panel 容器按合同分层，不再堆叠在单页面入口。

## 交付要求
- `ui-dev` 能独立启动。
- 页面默认进入 `SKILL.md`。
- 文档变化、删除、新增都能在页面中实时体现。
