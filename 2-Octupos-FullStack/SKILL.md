---
name: "2-Octupos-FullStack"
description: "OctopusOS 全栈文档驱动开发与长期治理技能：mother doc、fullstack graph、construction packs、implementation、acceptance。"
---

# 2-Octupos-FullStack

## 1. 目标
- 本技能用于 OctopusOS 的全栈开发、数据库设计、部署维护、多端协同与长期架构治理。
- 本技能覆盖：`frontend`、`backend`、`database`、`api_and_contracts`、`deployment_and_runtime`、`operations_and_maintenance`、`app_and_multi_client`、`integration_and_messaging`、`testing_and_acceptance`、`observability_and_security`、`documentation_and_mother_doc_governance`、`fullstack_graph_and_architecture_contracts`。
- 本技能的阶段主轴固定为：`mother_doc -> construction_plan -> implementation -> acceptance`。

## 2. 可用工具
- 统一工具入口预留为：`scripts/Cli_Toolbox.py`。
- 当前轮先固化顶层规则与 runtime contract；不宣称阶段级 CLI 合同已经实现。
- 后续阶段级命令统一收敛为：`Cli_Toolbox.stage-checklist`、`Cli_Toolbox.stage-doc-contract`、`Cli_Toolbox.stage-command-contract`、`Cli_Toolbox.stage-graph-contract`。
- 使用文档与开发文档保留在 `references/tooling/`，待命令面稳定后再回填。

## 3. 工作流约束
- 顶层阶段顺序固定为：`mother_doc -> construction_plan -> implementation -> acceptance`。
- `mother_doc` 是长期维护的顶层需求与设计容器；任何单域实施不得绕过它直接定义真实意图。
- 在阶段级 CLI 合同尚未完成前，以 `references/runtime/SKILL_RUNTIME_CONTRACT.json` 作为静态运行合同源；CLI 完成后切换为 CLI-first。
- 阶段切换时只保留 top-level resident docs，并显式丢弃上一阶段的局部 focus、临时文档上下文与实现噪音。

## 4. 规则约束
- top-level resident docs 固定为：
  - `rules/FULLSTACK_SKILL_HARD_RULES.md`
  - `references/runtime/SKILL_RUNTIME_CONTRACT.json`
  - `references/runtime/SKILL_RUNTIME_CONTRACT.md`
  - `references/stages/00_STAGE_INDEX.md`
  - `/home/jasontan656/AI_Projects/AGENTS.md`
- 顶层规则不得覆盖 workspace/runtime 的外层硬合同。
- 规则必须同时存在 markdown 审计版与 machine-readable 合同版，更新时必须同步。
- 若某些合同依赖真实项目状态，必须显式标注为 dynamic runtime contract。

## 5. 方法论约束
- 固定采用：先 `contract`，再 `directive`，再 `action`。
- 文档必须原子化、分域清晰、可被人类阅读，也可被机器作为合同消费。
- `fullstack graph` 管理的不只是 code，也包括文档、组件关系、合同依赖与架构回写意图；但它不能替代 `mother_doc` 作为需求源。
- 全栈公共内核只承载跨域稳定规则；前端、后端、数据库、部署、运维、APP 等差异约束以下沉 overlay 承载。

## 6. 内联导航索引
- [规则层] -> [rules/FULLSTACK_SKILL_HARD_RULES.md]
- [运行合同 JSON] -> [references/runtime/SKILL_RUNTIME_CONTRACT.json]
- [运行合同审计版] -> [references/runtime/SKILL_RUNTIME_CONTRACT.md]
- [阶段索引] -> [references/stages/00_STAGE_INDEX.md]
- [阶段模板簇] -> [assets/templates/stages/]
- [Cli_Toolbox 使用文档] -> [references/tooling/Cli_Toolbox_USAGE.md]
- [Cli_Toolbox 开发文档] -> [references/tooling/Cli_Toolbox_DEVELOPMENT.md]

## 7. 架构契约
```text
2-Octupos-FullStack/
├── SKILL.md
├── agents/openai.yaml
├── rules/
│   └── FULLSTACK_SKILL_HARD_RULES.md
├── scripts/
├── references/
│   ├── runtime/
│   ├── stages/
│   └── tooling/
└── assets/
    └── templates/
        └── stages/
```
