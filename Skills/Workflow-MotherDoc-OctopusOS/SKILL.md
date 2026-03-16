---
name: Workflow-MotherDoc-OctopusOS
description: Octopus_OS 的 mother_doc 阶段技能；负责把需求按既有文档体系逐层写回，并同步整体架构。
skill_mode: guide_with_tool
metadata:
  doc_structure:
    doc_id: workflow_motherdoc_octopusos.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Workflow-MotherDoc-OctopusOS skill
---

# Workflow-MotherDoc-OctopusOS

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能仍以 `mother_doc` 阶段为唯一业务主职责，但现在同时内建一个面向“技能自身持续重构与维护”的治理入口。
- `stage_flow` 负责真实 `mother_doc` 阶段执行；`skill_maintenance` 负责在不推倒重来的前提下持续重组本技能自己的文档结构、分层职责、锚点规范与维护机制。
- 正确目标不是造一棵巨型混写知识树，而是让 `mother_doc` 文档体系与本技能自身的治理骨架都能按真实使用过程逐轮演进。
- 顶层文档先承担常驻规范、知识索引与产品级基线；越向下越从人类叙事过渡到机械叙事。
- 当主题需要进入更深锚点文档时，必须由用户显式指定下一个文档主题；本技能负责同步 overview/index/entry-map 等整体架构文档。

### 2. 技能约束
- 本技能的业务入口仍只处理 `mother_doc`，不在本技能里切 pack、不落 implementation、不做 acceptance 收口。
- `skill_maintenance` 只治理当前技能自身，不替代 `mother_doc` 的业务写回动作，也不篡改后续阶段技能的显式切换门禁。
- 当用户从流程、文档、前端呈现、锚点规范、阶段衔接或正文承载位置切入时，`skill_maintenance` 必须把这些输入同时视为“当前开发需求”与“技能自我演化信号”。
- 允许按回合增量调整本技能的文件夹架构、文档组织架构和正文承载位置，但必须同步迁移既有内容，禁止留下长期并行真源。
- 工作目录统一由本技能自己的 `target-runtime-contract` 解析；默认落在 `Octopus_OS/Development_Docs/mother_doc`。
- `mother-doc-audit` 只作为可选治理动作，不能替代 live requirement source。
- 真实写回后必须经过 `mother-doc-lint`、`mother-doc-refresh-root-index` 与 `mother-doc-sync-client-copy`。

### 3. 顶层常驻合同
- `stage_flow` 仍是本技能的唯一业务主入口，也是 `mother_doc` 阶段的默认读取路径。
- `skill_maintenance` 的目标是持续提高本技能自身结构质量，而不是预先假设一套一次性定死的完整终局结构。
- 先锁定当前主题与归属层级，再决定当前轮最小写回切片。
- 若用户尚未指定更深锚点主题，不得自动创建新的下层 anchor doc。
- 任何自维护改造都必须保持以下可观察合同不退化：
  - `mother_doc` 仍然负责把需求逐层写回既有文档体系。
  - 更深锚点主题仍然必须由用户显式指定。
  - 后续若要继续推进到下游阶段，必须由用户显式切换到对应的新技能，而不是经由兼容壳跳转。

## 2. 功能入口
- [mother_doc 主执行]：`path/stage_flow/00_STAGE_FLOW_ENTRY.md`
  - 作用：进入 `mother_doc` 阶段的最小执行链，处理真实需求写回与架构同步。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry stage_flow --json`
- [技能自维护]：`path/skill_maintenance/00_SKILL_MAINTENANCE_ENTRY.md`
  - 作用：当任务在重构、补强、迁移或持续维护 `Workflow-MotherDoc-OctopusOS` 自身时，读取最小治理链。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry skill_maintenance --json`

## 3. 目录结构图
```text
Workflow-MotherDoc-OctopusOS/
├── SKILL.md
├── agents/
├── path/
│   ├── stage_flow/
│   └── skill_maintenance/
├── references/
├── scripts/
└── tests/
```
- `path/stage_flow/`：承载 `mother_doc` 阶段执行链，是业务主入口真源。
- `path/skill_maintenance/`：承载本技能的自维护入口、分层原则、回合级迁移规则与边界校验。
- `references/`：保留运行时合同等稳定镜像；若结构演进后仍需要稳定发现面，优先在这里保留镜像而不是复制正文。
- `scripts/` 与 `tests/`：继续承接共享 CLI 包装层与最小回归验证，不为自维护入口额外引入独立 tooling surface。
