---
name: "Meta-VUE3-WebUI-frontend"
description: "治理 Vue3 Web UI 规范、前端展厅、可视化 graph 展示与可复用组件资产的多 stage 技能。"
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

# Meta-VUE3-WebUI-frontend

## 1. 定位
- 本文件只做门面入口，不承载多 stage 规则正文。
- 本技能同时承担三种角色：
  - Vue3 Web UI 规范库
  - 可复用组件与前端架构最佳实践
  - 以真实 doc graph 驱动的可运行展厅
- 技能主轴是 `resident docs -> staged standards -> runnable showroom`。

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
4. 若任务落到 runnable showroom，再进入：
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
- 工具层：
  - `scripts/Cli_Toolbox.ts`

## 4. 适用域
- 适用于：Vue3 Web UI 标准、信息层级设计、桌面/移动端布局规范、动效规范、组件组织、代码组织、图谱展示、前端展厅运行链。
- 不适用于：替代具体业务产品需求、替代纯视觉稿评审、替代 `Meta-Skill-DocStructure` 的文档结构方法论本体。
- 本技能消费 doc graph 能力，但自身重点是前端标准与可运行展示面。

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
- UI 运行：
  - `cd ui-dev && npm run dev`
  - `cd ui-dev && npm run build`

## 6. 读取原则
- `SKILL.md` 只负责路由，不承担阶段正文。
- 顶层常驻文档只维持长期边界、目标与 stage 顺序。
- 阶段切换后必须丢弃上一阶段的局部 focus，只保留 resident docs。
- UI 展厅不是静态 demo，而是当前技能真实 doc graph 的人类可视化门面。
- 组件、动效、布局、运行链都应先写入文档，再进入代码修改。

## 7. 结构索引
```text
Meta-VUE3-WebUI-frontend/
├── SKILL.md
├── agents/
├── scripts/
├── src/
├── references/
│   ├── runtime/
│   ├── stages/
│   └── tooling/
├── assets/
│   ├── runtime/
│   └── templates/
├── tests/
└── ui-dev/
```
