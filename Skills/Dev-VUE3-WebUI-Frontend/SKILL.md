---
name: "Dev-VUE3-WebUI-Frontend"
description: "沉淀项目定制 Vue3 组件使用方式、自包含 UI 展厅、可肉眼验证的前端效果与开发规范的必用前端技能。"
metadata:
  doc_structure:
    doc_id: "skill.entry.facade"
    doc_type: "skill_facade"
    topic: "Entry facade for the staged Vue3 web UI frontend skill"
    anchors:
      - target: "references/runtime/SKILL_RUNTIME_CONTRACT.md"
        relation: "governed_by"
        direction: "downstream"
        reason: "The staged runtime contract defines resident docs, stage order, and CLI entrypoints."
      - target: "references/stages/00_STAGE_INDEX.md"
        relation: "routes_to"
        direction: "downstream"
        reason: "The stage index defines the concrete reading path for the frontend standards system."
---

# Dev-VUE3-WebUI-Frontend

## 1. 定位
- 本文件只做门面入口，不承载多 stage 规则正文。
- 本技能同时承担三种角色：
  - 项目定制 Vue3 组件与使用方式规范库
  - 自包含 UI 展厅开发文档与前端架构最佳实践
  - 未来可重建的 showroom runtime 目标定义
- 技能主轴是 `resident docs -> staged standards -> showroom redevelopment docs -> future runtime`。

## 2. 必读顺序
1. 先读取运行合同：
   - `npm run cli -- runtime-contract --json`
2. 再读取常驻文档：
   - `references/stages/01_RESIDENT_FRONTEND_NORTH_STAR.md`
   - `references/stages/00_STAGE_INDEX.md`
3. 进入任一阶段前，固定先读：
   - `npm run cli -- stage-checklist --stage <stage> --json`
   - `npm run cli -- stage-doc-contract --stage <stage> --json`
   - `npm run cli -- stage-command-contract --stage <stage> --json`
   - `npm run cli -- stage-graph-contract --stage <stage> --json`
4. 若任务落到 showroom 自身开发文档，再进入：
   - `ui-dev/UI_DEV_ENTRY.md`

## 3. 分类入口
- 运行合同层：
  - `references/runtime/SKILL_RUNTIME_CONTRACT.md`
  - `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md`
- 阶段层：
  - `references/stages/00_STAGE_INDEX.md`
  - `references/stages/10_STAGE_FOUNDATION.md`
  - `references/stages/20_STAGE_SURFACE_LAYOUTS.md`
  - `references/stages/30_STAGE_MOTION_COMPONENT_ARCHITECTURE.md`
  - `references/stages/40_STAGE_SHOWROOM_RUNTIME.md`
- UI 展厅层：
  - `ui-dev/UI_DEV_ENTRY.md`
  - `ui-dev/docs/`
  - `frontend_dev_contracts/`
- 工具层：
  - `scripts/Cli_Toolbox.ts`

## 4. 适用域
- 适用于：项目定制 Vue3 Web UI 组件使用方式、信息层级设计、桌面/移动端布局规范、动效规范、组件组织、代码组织、showroom 用途设计、SPA menu/canvas 目标定义。
- 不适用于：替代具体业务产品需求、替代纯视觉稿评审、替代 `skill-doc-structure` 的文档结构方法论本体。
- 本技能消费 doc graph 能力，但自身重点是前端标准、可运行展示面，以及前端开发阶段的必用规范入口。

## 5. 执行入口
- 运行合同：
  - `npm run cli -- runtime-contract --json`
- 阶段合同：
  - `npm run cli -- stage-checklist --stage <stage> --json`
  - `npm run cli -- stage-doc-contract --stage <stage> --json`
  - `npm run cli -- stage-command-contract --stage <stage> --json`
  - `npm run cli -- stage-graph-contract --stage <stage> --json`
- graph 校验：
  - `npm run cli -- build-anchor-graph --json`
  - `npm run cli -- rebuild-self-graph --json`
- UI 文档入口：
  - `ui-dev/UI_DEV_ENTRY.md`
  - `ui-dev/docs/00_UI_DEV_DOCS_INDEX.md`

## 6. 读取原则
- `SKILL.md` 只负责路由，不承担阶段正文。
- 顶层常驻文档只维持长期边界、目标与 stage 顺序。
- 阶段切换后必须丢弃上一阶段的局部 focus，只保留 resident docs。
- `ui-dev/` 当前先作为 showroom redevelopment docs root，不再假装已经有一套合格的可运行 UI。
- 组件、动效、布局、语言规则、menu/canvas 架构都应先写入文档，再进入下一轮代码重建。
- 只要任务进入前端开发，就应优先使用本技能收敛组件、界面与规范语义。

## 7. 结构索引
```text
Dev-VUE3-WebUI-Frontend/
├── SKILL.md
├── agents/
├── scripts/
├── src/
├── references/
│   ├── runtime/
│   ├── stages/
│   └── tooling/
├── frontend_dev_contracts/
├── assets/
│   ├── runtime/
│   └── templates/
├── tests/
└── ui-dev/
```
