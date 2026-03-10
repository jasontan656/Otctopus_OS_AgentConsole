---
doc_id: "ui.dev.entry"
doc_type: "ui_dev_entry"
topic: "UI development root for the Meta-Skill-DocStructure viewer"
anchors:
  - target: "../SKILL.md"
    relation: "implements"
    direction: "upstream"
    reason: "This UI dev root fulfills the facade promise of a dedicated embedded UI tool."
  - target: "docs/00_UI_DEVELOPMENT_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The UI docs index organizes architecture, workflow, and layout guidance."
---

# UI Dev Entry

`ui-dev/` 是本技能中唯一官方 UI 工作根目录，也是技能内部的独立 UI 工具边界。

## 目录角色
- `client/`
  - Vue3 + Vue Flow 门面代码。
- `server/`
  - watcher server、API、websocket 与 Vite middleware。
- `scripts/`
  - UI 相关启动与 service tooling。
- `assets/systemd/`
  - UI viewer 的 user-level service unit 文件。
- `docs/`
  - UI 设计、运行流与布局调整文档。
- `tests/`
  - UI payload 与运行链路回归用例。

## 启动原则
- 开发 UI 时从 `ui-dev/` 启动：
  - `npm install`
  - `npm run dev`
- 生产构建与常驻也从 `ui-dev/` 启动。
- UI 读取 skill root 中的真实文档来形成视图，但 UI 自己的代码、依赖、回归用例与文档不得回流到根技能。
