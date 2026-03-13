---
name: "Dev-VUE3-WebUI-Frontend"
description: "沉淀项目定制 Vue3 组件使用方式、前端交互合同、布局治理与产品运行时 handoff 的必用前端技能。"
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
- 本技能当前只承担两类职责：
  - 项目定制 Vue3 组件与使用方式规范库
  - 前端交互合同、布局治理、代码组织与产品运行时 handoff 规则
- 产品级界面需求、menu/canvas/panel 具体目标与实现前说明书，不再保存在本技能内。
- 技能主轴是 `resident docs -> staged standards -> product-runtime handoff`。

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
4. 若任务落到具体产品运行时需求，转入产品侧 `Workflow-OctopusOS-DevFlow` mother doc，而不是继续在本技能内沉淀产品需求。

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
- 前端合同层：
  - `frontend_dev_contracts/`
- 工具层：
  - `scripts/Cli_Toolbox.ts`

## 4. 适用域
- 适用于：项目定制 Vue3 Web UI 组件使用方式、信息层级设计、桌面/移动端布局规范、动效规范、组件组织、代码组织、多治理域 viewer 抽象、产品运行时 handoff 边界。
- 不适用于：替代具体业务产品需求、替代产品级母文档、替代纯视觉稿评审、替代 `SkillsManager-Doc-Structure` 的文档结构方法论本体。
- 本技能消费 doc graph 与 code graph 能力，但自身重点是前端标准与产品 handoff 规则，而不是保存具体产品界面说明。

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
- 产品 mother doc 门禁：
  - `npm run cli -- build-product-doc-graph --docs-root <development_docs_root> [--write-assets] --json`
  - `npm run cli -- lint-product-mother-doc --docs-root <development_docs_root> [--write-assets] --json`
- 产品运行时需求入口：
  - 由具体产品仓的 `Workflow-OctopusOS-DevFlow mother_doc` 承载

## 6. 读取原则
- `SKILL.md` 只负责路由，不承担阶段正文。
- 顶层常驻文档只维持长期边界、目标与 stage 顺序。
- 阶段切换后必须丢弃上一阶段的局部 focus，只保留 resident docs。
- 组件、动效、布局、语言规则、menu/canvas 架构都应先写入文档，再进入下一轮代码重建。
- 只要任务进入前端开发，就应优先使用本技能收敛组件、界面与规范语义。
- 当前技能不仅治理通用前端合同，也负责读取目标产品 `mother_doc` 并执行前端定制 lint；lint 应直接消费目标文档树与其 graph，而不是只检查 skill 自身规则文案。
- 统一前端壳应承载多治理域内容，但不得把各治理域的原始语义压平；应通过 domain-aware viewer projection 收口到统一 UI。
- 具体产品的运行时需求、panel catalog 与产品 UI 代码必须落在产品仓，而不回流进本技能。

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
└── tests/
```
