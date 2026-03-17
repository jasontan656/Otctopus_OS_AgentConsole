---
name: Workflow-SiteMap-Creation
description: 作为 Workflow-MotherDoc-OctopusOS 的上游协作技能，专门把每轮用户描述 factory 化为双重目的输入，并在 factory 后强制进入 Meta-Enhance-Prompt、background tmux subagent、Functional-Analysis-Runtask 九阶段 analysis_loop、artifact refresh 与 validation closeout 的正式闭环。
metadata:
  skill_profile:
    doc_topology: workflow_path
    tooling_surface: automation_cli
    workflow_control: compiled
  doc_structure:
    doc_id: workflow_sitemap_creation.entry.facade
    doc_type: skill_facade
    topic: Entry facade for Workflow-SiteMap-Creation
---

# Workflow-SiteMap-Creation

## Runtime Entry
- Primary runtime entry: `./scripts/Cli_Toolbox.py contract --json`
- Self governance entry: `./scripts/Cli_Toolbox.py read-contract-context --entry self_governance --json`
- Artifact lint audit entry: `./scripts/Cli_Toolbox.py read-contract-context --entry artifact_lint_audit --json`
- Runtime directives: `./scripts/Cli_Toolbox.py directive --topic <topic> --json`
- CLI JSON is the primary runtime source; `SKILL.md` only保留门面与路由叙事。

## 1. 技能定位
- 本技能不是泛化讨论技能，而是 `Workflow-MotherDoc-OctopusOS` 的固定上游协作技能。
- 它专门治理 `Octopus_OS/Development_Docs/mother_doc` 下的站点级开发文档、代码地图、使用说明书与衍生说明统一架构。
- 用户每轮输入必须被解释为双重目的输入：
  - 一条目的是驱动目标产物形态改写与结构化落盘。
  - 另一条目的是驱动技能自身的规则、架构说明、生成逻辑、lint 思路、lint 代码规则与治理工作流继续固化。
- 本技能的正式受管主链固定为：
  - `factory`
  - `Meta-Enhance-Prompt`
  - `background tmux subagent`
  - `Functional-Analysis-Runtask analysis_loop`
  - `artifact refresh`
  - `validation closeout`
- `Functional-Analysis-Runtask` 的九阶段不是说明性建议，而是本技能 runtime 内正式受管的执行路径。
- 本技能显式弃用“文档知识库”叫法；对外只使用“全站开发文档、代码地图、使用说明书及相关衍生说明统一架构”。

## 2. 必读顺序
1. 先读取 `references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md`。
2. 再读取 `references/routing/TASK_ROUTING.md`。
3. 若任务要执行正式闭环治理，进入 `path/self_governance/00_SELF_GOVERNANCE_ENTRY.md`。
4. 若任务要用技能自身规则审计已有产物架构，进入 `path/artifact_lint_audit/00_ARTIFACT_AUDIT_ENTRY.md`。
5. 若任务涉及运行态方法，继续读取 `references/runstates/RUNSTATE_METHOD_CONTRACT.md`。

## 3. 分类入口
- 路由：`references/routing/TASK_ROUTING.md`
- 自我治理 workflow：`path/self_governance/00_SELF_GOVERNANCE_ENTRY.md`
- 产物 lint 审计 workflow：`path/artifact_lint_audit/00_ARTIFACT_AUDIT_ENTRY.md`
- 治理规则：`references/governance/*.md`
- 运行合同：`references/runtime_contracts/*.json`
- tooling：`references/tooling/Cli_Toolbox_USAGE.md`

## 4. 常驻边界
- 目标真源根固定为 `Octopus_OS/Development_Docs/mother_doc`，client mirror 根固定为 `Octopus_OS/Client_Applications/mother_doc`。
- 任何实验性结构化目录与文档优先直接落在上述 `mother_doc` 真源根中，不先绕回技能目录。
- `self-governance-run` 必须写入两类对象：
  - `mother_doc` 真源中的受管实验文档架构。
  - 技能内部的演化信号注册表与轮次演化日志。
- `self-governance-run` 必须显式经过 `$Meta-Enhance-Prompt` 与 `$Functional-Analysis-Runtask`；不允许 factory 后直接落盘。
- background subagent 必须通过 `tmux` 启动，主 AGENT 必须轮询其输出，且只有连续 `10` 分钟无新输出时才允许判死。
- `design` 阶段必须显式执行 `$Meta-keyword-first-edit` 的删掉重写 / keyword-first 替换 / 最小必要新增裁决。
- `artifact-lint-audit` 必须能够仅依赖技能自身承载的规则，对目标自产文档架构执行 lint、审计与治理判断。
- workflow runtime 采用 `workflow_runtime_checklist` 与 `stage_runtime_checklist`，禁止跳过中间态写回。
