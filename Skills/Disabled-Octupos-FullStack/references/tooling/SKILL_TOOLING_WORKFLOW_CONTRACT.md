# Disabled-Octupos-FullStack Tooling & Workflow Contract


## Contract Header
- `required_fields`:
  - `contract_name`
  - `contract_version`
  - `validation_mode`
- `optional_fields`:
  - `notes`

## Contract Header

- `contract_name`: `octopus_fullstack_os_workflow_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`

## Top-Level Resident Docs

- `rules/FULLSTACK_SKILL_HARD_RULES.md`
- `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- `references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md`
- `/home/jasontan656/AI_Projects/AGENTS.md`

## Phase Read Policy

- 单阶段执行时，只读取当前阶段 checklist 与当前阶段直接需要的文档。
- 多阶段连续执行时，阶段切换后必须：
  - 保留 top-level resident docs
  - 重读当前阶段 checklist / doc / command / graph contracts
  - 丢弃上一阶段的阶段文档与局部 focus

## Implementation Policy

- `implementation` 必须像独立人类开发者一样推进：
  - 发现问题
  - 安装依赖
  - 修复环境
  - 运行测试
  - bring-up 服务
  - 验证交付
- doc-code drift 必须被显式识别并修复。

## Mother_Doc Navigation Policy

- `AGENTS.md` 当前只允许存在于 `Octopus_OS/AGENTS.md`。
- `mother_doc` 阶段下固定存在 root-only `AGENTS manager` 子分支，专门处理根 `AGENTS.md` 的 payload 管理。
- root-only `AGENTS manager` 固定采用 `scan / collect / push` 三阶段。
- `sync-mother-doc-navigation` 只刷新 `Mother_Doc` 树内的 README 与 scope 文档，并删除遗留 docs-tree `AGENTS.md`。
- `sync-mother-doc-status-from-git` 负责在 `mother_doc` 阶段基于本地 `git` 差异刷新文档生命周期状态。
- `sync-mother-doc-status` 负责在显式阶段回写时把目标文档状态覆盖成指定生命周期值，主要用于 `evidence -> developed`。
- `mother-doc-agents-scan` 只扫描根 `AGENTS.md` 与非法额外 `AGENTS.md`。
- `mother-doc-agents-collect` 只把根 `AGENTS.md` 回收到技能内 managed human/machine pair。
- `mother-doc-agents-push` 只把技能侧当前 payload 反推回根 `AGENTS.md`，并自动清理非法额外 `AGENTS.md` 与旧 legacy assets。

## Delivery Log Policy

- `mother_doc` 阶段禁止写任何开发/部署日志，也不承担 Git / GitHub 留痕。
- `implementation` 阶段只产生对齐结果与差异范围，不直接写日志，也不直接承担 Git / GitHub 留痕。
- `evidence` 阶段负责追加 implementation batch。
- `evidence` 形成真实部署 witness 后，必须追加 deployment checkpoint。
- 日志固定写入 `Octopus_OS/Mother_Doc/docs/Mother_Doc/common/development_logs/`。
- 日志只写摘要；摘要必须等于同轮 Git 提交 message，具体修改交由 Git / GitHub 追踪。

## Evidence Policy

- `evidence` 必须以 `OS_graph` 统一文档 graph 与代码 graph。
- `evidence` 固定先进入 `references/evidence/00_EVIDENCE_INDEX.md`，再进入 `references/evidence/graph/00_GRAPH_INDEX.md`。
- graph 命令域固定通过 `python3 scripts/os_graph_cli.py <command> [args...]` 进入。
- evidence 必须绑定回同一层级结构中的模块、helper、父级目录与 witness 节点。
- `sync-doc-bindings` 负责把 `Mother_Doc/docs` 编成文档节点、边和前端层视图。
- `sync-evidence` 负责把 development logs 与 lifecycle 状态编成 evidence 节点和证据时间线。
- `Mother_Doc/graph/runtime/frontend_views/` 只承载人类界面的聚合结果；源 authored docs 与碎片化 graph 资产仍然分开维护。
