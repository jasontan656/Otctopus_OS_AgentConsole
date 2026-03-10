---
name: "meta-skill-docstructure"
description: "治理 skills 内部文档组织、单 topic 原子文档与锚点图谱的技能。UI 视图工具作为内置子工具收敛在 ui-dev/。"
metadata:
  short-description: "治理 skills 内部文档结构与锚点图谱，内置 ui-dev 视图工具入口"
  doc_structure:
    doc_id: "skill.entry.facade"
    doc_type: "skill_facade"
    topic: "Meta-Skill-DocStructure entry facade and routing contract"
    anchors:
      - target: "references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
        relation: "governed_by"
        direction: "downstream"
        reason: "Detailed document-structure runtime rules live in the runtime contract."
      - target: "ui-dev/UI_DEV_ENTRY.md"
        relation: "routes_to"
        direction: "downstream"
        reason: "The embedded UI tool has its own entry and must be read separately."
---

# Meta-Skill-DocStructure

## 1. 定位
- 本文件只做技能门面入口，不承载 UI 工具正文。
- 本技能的唯一主轴是：`skill_facade -> runtime_contract -> doc_graph_assets -> optional_ui_tool`。
- 本技能负责治理 skill folder 内的单 topic 文档、frontmatter anchors、anchor graph 与 anchor-check workflow。
- UI 不是技能主体，而是技能内置的一个视图工具；其代码、依赖、回归用例、tooling 与开发文档必须全部收敛到 `ui-dev/`。

## 2. 必读顺序
1. 进入本技能后，先读取：
   - `npm run cli -- runtime-contract --json`
2. 若目标是文档结构治理，继续读取：
   - `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md`
   - `references/tooling/Cli_Toolbox_USAGE.md`
3. 若目标是 UI 视图工具开发或调界面，转入：
   - `ui-dev/UI_DEV_ENTRY.md`
4. 若修改了 tooling、contracts、asset 或图谱规则，必须同步更新相关文档与回归。

## 3. 分类入口
- 运行合同层：
  - `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.json`
  - `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md`
- 文档治理资产层：
  - `assets/templates/DOC_FRONTMATTER_TEMPLATE.yaml`
  - `assets/templates/ATOMIC_DOC_TEMPLATE.md`
  - `assets/runtime/anchor_query_matrix.json`
  - `assets/runtime/self_anchor_graph.json`
- 工具层：
  - `scripts/Cli_Toolbox.ts`
  - `src/lib/docstructure.ts`
  - `src/lib/types.ts`
- 校验层：
  - `tests/test_cli_toolbox.spec.ts`
- 内置 UI 工具层：
  - `ui-dev/UI_DEV_ENTRY.md`

## 4. 适用域
- 适用于：skills 内部文档拆分、frontmatter anchor 校验、graph 构建、自身 graph 回写、将文档结构治理收敛为稳定合同。
- 不适用于：普通 repo 文档治理、替代代码图谱技能、把 UI 本身当成技能主体。
- 若任务目标是 UI 视图、交互、布局或视觉层级调整，应转到 `ui-dev/` 处理，而不是把 UI 逻辑散回根技能。

## 5. 执行入口
- 运行合同：
  - `npm run cli -- runtime-contract --json`
- 锚点 lint：
  - `npm run cli -- lint-doc-anchors --target <skill_root> --json`
- 图谱构建：
  - `npm run cli -- build-anchor-graph --target <skill_root> --json`
- 自身 graph 回写：
  - `npm run cli -- rebuild-self-graph --json`
- UI 工具入口：
  - `ui-dev/UI_DEV_ENTRY.md`

## 6. 读取原则
- `SKILL.md` 只负责门面路由；运行时细节以下沉 contracts、tooling 文档与模板资产为准。
- 根技能只表达文档治理本体，不直接承载 UI payload 逻辑或 UI 回归用例。
- 所有 UI 相关代码、依赖、回归用例、tooling 与开发文档都必须留在 `ui-dev/`。
- 若技能存在执行态规则，模型不得直接读 markdown 当规则源；必须优先读取 machine-readable 合同。

## 7. 结构索引
```text
Meta-Skill-DocStructure/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── Cli_Toolbox.ts
├── src/
│   └── lib/
│       ├── docstructure.ts
│       └── types.ts
├── assets/
│   ├── runtime/
│   └── templates/
├── references/
│   ├── runtime/
│   └── tooling/
├── tests/
│   └── test_cli_toolbox.spec.ts
└── ui-dev/
    ├── UI_DEV_ENTRY.md
    ├── package.json
    ├── client/
    ├── server/
    ├── lib/
    ├── scripts/
    ├── assets/
    ├── docs/
    └── tests/
```
