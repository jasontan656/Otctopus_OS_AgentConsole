---
name: "meta-skill-docstructure"
description: "规范 skills 内部文档组织与前端可视化门面的治理技能。用于在 skill folder 内建立单 topic 原子文档、frontmatter 锚点规范、anchor graph JSON、TypeScript CLI、Vue3 + Vue Flow 实时 viewer、热更新服务与 systemd 常驻方案。仅在组织或校验 skill 内部文档时使用。"
metadata:
  short-description: "治理 skills 内部文档组织、TS 工具链、viewer 与热更新工作流"
  doc_structure:
    doc_id: "skill.entry.facade"
    doc_type: "skill_facade"
    topic: "Meta-Skill-DocStructure entry facade and routing contract"
    anchors:
      - target: "references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
        relation: "governed_by"
        direction: "downstream"
        reason: "Detailed runtime rules live in the runtime contract."
      - target: "ui-dev/UI_DEV_ENTRY.md"
        relation: "front_doored_by"
        direction: "downstream"
        reason: "The dedicated UI dev root explains how the viewer is organized and adjusted."
---

# Meta-Skill-DocStructure

## 1. 应用域
- 只服务 `skills` 内部文档组织与其可视化门面。
- 目标对象是 skill folder 内的 `SKILL.md`、runtime 文档、tooling 文档、viewer 文档、模板文档与相关资产。
- 不处理普通 repo 文档，不替代代码图谱技能，不把 viewer 做成与 skill 语义脱钩的独立产品。

## 2. 核心目标
- 让 skill 内部文档尽可能原子化，每份 markdown 只承载一个稳定 topic。
- 要求每份 markdown 文档至少声明一个 anchor，但不要求全连接。
- 用 `TypeScript CLI + JSON graph + Vue3 + Vue Flow + watcher server` 把文档结构实时投影到一个可交互页面。
- 默认第一页就是 `SKILL.md` 的正文；再通过点击 graph、anchor 与文档列表深入查看。
- UI 相关代码、脚本、systemd 与开发文档统一收敛到 `ui-dev/`，并把它作为 UI 启动根目录。

## 3. 内部思考链
1. 锁定目标 skill root。
2. 清点全部 markdown 文档，读取 frontmatter anchor 合同。
3. 判断 single-topic 是否成立；若 topic 漂移，优先拆分。
4. 用 `anchor_query_matrix.json` 检查是否命中拆分信号。
5. 运行 TS CLI，产出 lint、graph 与 preview payload。
6. 由 watcher server 热加载 payload，推动页面实时更新。

## 4. 工作流
1. 先读取 runtime contract：
   - `npm run cli -- runtime-contract --json`
2. 先 lint，再改文档：
   - `npm run cli -- lint-doc-anchors --target <skill_root> --json`
3. 看门面页面时启动 dev server：
   - `cd ui-dev && npm run dev`
4. 修改本技能自身文档后，必须回写：
   - `npm run cli -- rebuild-self-graph --json`
5. 需要常驻服务时：
   - `cd ui-dev && npm run build`
   - `cd ui-dev && npm run service:install`

## 5. 工具与资产
- TS CLI：`scripts/Cli_Toolbox.ts`
- 共享逻辑：`src/lib/docstructure.ts`
- UI dev 根目录：`ui-dev/`
- 实时服务：`ui-dev/server/viewer-server.ts`
- viewer 前端：`ui-dev/client/*`
- UI 开发文档：`ui-dev/docs/*`
- runtime contract：
  - `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.json`
  - `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md`
- UI dev 入口：
  - `ui-dev/UI_DEV_ENTRY.md`
- UI viewer 规范：
  - `ui-dev/docs/VIEWER_STACK_AND_REUSE.md`
  - `ui-dev/docs/VIEWER_SERVICE_WORKFLOW.md`
  - `ui-dev/docs/rules/UI_LAYOUT_ADJUSTMENT_RULES.md`
- systemd 模板：`ui-dev/assets/systemd/meta-skill-docstructure-viewer.service`

## 6. 读取顺序
1. `SKILL.md`
2. `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md`
3. `ui-dev/UI_DEV_ENTRY.md`
4. `references/tooling/Cli_Toolbox_USAGE.md`
5. 需要实现细节时，再读 `references/tooling/development/*`

## 7. Guardrails
- 任何 markdown 文档都不得做成零锚点孤岛。
- viewer 必须实时读取 skill 内文档变化；文档消失，页面对应节点也必须消失。
- viewer 不是手写静态 mock；它必须消费真实 graph 与真实正文。
- 原有 CLI 统一迁到 TS；不得继续保留 Python 版本。
- UI 视觉调整的文档、代码、运行脚本必须优先收敛在 `ui-dev/`，不要把 UI 设计知识散落回根目录。
