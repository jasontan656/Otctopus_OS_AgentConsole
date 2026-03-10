---
doc_id: "ui.dev.entry"
doc_type: "ui_dev_entry"
topic: "UI development root for the Meta-Skill-DocStructure viewer"
anchors:
  - target: "../SKILL.md"
    relation: "implements"
    direction: "upstream"
    reason: "This UI dev root fulfills the facade promise of a dedicated viewer workspace."
  - target: "docs/00_UI_DEVELOPMENT_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The UI docs index organizes architecture, workflow, and layout guidance."
---

# UI Dev Entry

`ui-dev/` 是本技能中唯一官方 UI 工作根目录。

## 目录角色
- `client/`
  - Vue3 + Vue Flow 门面代码。
- `server/`
  - watcher server、API、websocket 与 Vite middleware。
- `scripts/`
  - UI 相关启动与 service 脚本。
- `assets/systemd/`
  - UI viewer 的 user-level service 模板。
- `docs/`
  - UI 架构、运行流与布局调整文档。

## 启动原则
- 开发 UI 时从 `ui-dev/` 启动：
  - `npm install`
  - `npm run dev`
- 生产构建与常驻也从 `ui-dev/` 启动。
