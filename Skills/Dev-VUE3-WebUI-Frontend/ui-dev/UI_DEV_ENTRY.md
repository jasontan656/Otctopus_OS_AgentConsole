---
doc_id: "ui.dev.entry"
doc_type: "ui_dev_entry"
topic: "Runnable showroom root for Dev-VUE3-WebUI-Frontend"
anchors:
  - target: "../references/stages/40_STAGE_SHOWROOM_RUNTIME.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "The ui-dev root is the concrete surface of the showroom runtime stage."
  - target: "../frontend_dev_contracts/00_UI_DEVELOPMENT_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The frontend contract index defines the official UI development reading path."
  - target: "../frontend_dev_contracts/containers/00_CONTAINERS_INDEX.md"
    relation: "implements"
    direction: "downstream"
    reason: "The runnable showroom must realize the container contracts through the SPA UI code."
---

# UI Dev Entry

`ui-dev/` 是本技能的 runnable showroom 根目录，也是前端实现、组件实验和 live graph 展示的唯一官方代码面。

## 包含内容
- Vue3 + Vue Flow 页面代码。
- app shell、scene、workspace、panel 容器实现。
- viewer payload 装配层与 live server。
- systemd 安装脚本与运行文档。
- 消费 `frontend_dev_contracts/` 中定义的前端开发合同。

## 使用方式
- 开发：
  - `npm run dev`
- 构建：
  - `npm run build`
- 常驻：
  - `npm run service:install`
