---
doc_id: "ui.dev.entry"
doc_type: "ui_dev_entry"
topic: "Runnable showroom root for Meta-VUE3-WebUI-frontend"
anchors:
  - target: "../references/stages/40_STAGE_SHOWROOM_RUNTIME.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "The ui-dev root is the concrete surface of the showroom runtime stage."
  - target: "docs/00_UI_DEVELOPMENT_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The docs index defines the local UI development reading path."
---

# UI Dev Entry

`ui-dev/` 是本技能的 runnable showroom 根目录，也是前端实现、组件实验和 live graph 展示的唯一官方代码面。

## 包含内容
- Vue3 + Vue Flow 页面代码。
- viewer payload 装配层与 live server。
- systemd 安装脚本与运行文档。
- 组件、布局、运行链的 UI 开发文档。

## 使用方式
- 开发：
  - `npm run dev`
- 构建：
  - `npm run build`
- 常驻：
  - `npm run service:install`
