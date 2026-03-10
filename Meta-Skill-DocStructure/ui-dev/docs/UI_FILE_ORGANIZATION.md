---
doc_id: "ui.tool.file_organization"
doc_type: "ui_dev_guide"
topic: "File organization rules for the embedded UI tool"
anchors:
  - target: "UI_TOOL_POSITIONING.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Positioning and file organization should be read together."
  - target: "../UI_DEV_ENTRY.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This file organization guide belongs to the UI tool root."
---

# UI File Organization

## 必须留在 `ui-dev/` 的内容
- `client/` 下的页面与组件。
- `server/` 下的 UI 服务入口。
- `lib/` 下的 viewer payload、viewer contract types 与其他 UI 适配层。
- `tests/` 下的 UI 相关测试。
- `scripts/`、`assets/systemd/`、`package.json`、`tsconfig.json` 与 `vitest.config.ts`。
- `docs/` 下全部 UI 开发文档。

## 不应留在根技能的内容
- `PreviewPayload` 之类 UI 语义类型。
- UI entryPath、正文面板组装、incoming/outgoing viewer 组装逻辑。
- UI 测试与 UI 服务脚本。

## 根技能允许保留的内容
- 文档扫描、anchor lint、graph 构建、自身 graph 回写等通用治理核心。
- 对 `ui-dev/UI_DEV_ENTRY.md` 的门面级路由。
