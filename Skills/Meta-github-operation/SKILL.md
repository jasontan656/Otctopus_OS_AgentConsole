---
name: "meta-github-operation"
description: "受限 GitHub control plane：仅服务 Octopus_OS 与 octopus-os-agent-console 两个仓库的状态、提交、推送、远端信息与开发/发布分流约束。"
---

# Meta-github-operation

## Status

本技能已恢复为受限启用状态，但当前只服务以下两个仓库：
- `/home/jasontan656/AI_Projects/Octopus_OS`
- `/home/jasontan656/AI_Projects/octopus-os-agent-console`

对于 `octopus-os-agent-console`，当前已进入双远端模型：
- `origin`: 私有开发仓 `octopus-os-agent-console_AI_dev`
- `public-release`: 公开发布仓 `octopus-os-agent-console`

当前策略：
- 自动迭代、同回合 Git traceability、日常 `commit-and-push` 只允许走 `origin`
- `public-release` 只保留为未来发布用途
- 当前阶段禁止向 `public-release` 推送
- 禁用原因：
  - 开发尚未闭环到可发布状态
  - 发布流程尚未设计完成

## Scope

- 允许：
  - repo registry
  - status / remote-info
  - fetch / pull-rebase
  - push-contract
  - baseline-contract
  - commit / commit-and-push / push
  - baseline-create
  - rollback-contract
  - rollback-paths
  - rollback-sync
- 不允许：
  - 超出上述两个仓库的 Git / GitHub 自动化调用
  - 对 `octopus-os-agent-console/public-release` 的任何写入式 push 自动化
  - 仓库删除
  - 整个 workspace 根目录级 Git 操作

## Entry

- CLI 入口：`scripts/Cli_Toolbox.py`
- registry 固定只暴露：
  - `Octopus_OS`
  - `octopus-os-agent-console`
- `remote-info` 与 `push-contract` 应成为 remote policy 的主读取入口
- 与运行时落盘/结果落点相关的 machine-readable 合同，应以 `push-contract --json`、`baseline-contract --json` 与 `rollback-contract --json` 返回的 `runtime_governance` 字段为准

## Runtime And Output Governance

- 技能 runtime 根目录：
  - `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/meta-github-operation`
- thread-owned claims 目录：
  - `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/meta-github-operation/claims`
- 兼容回退读取：
  - `/home/jasontan656/AI_Projects/Codex_Skill_Runtime`
- 技能 result 根目录：
  - `/home/jasontan656/AI_Projects/Codex_Skills_Result/meta-github-operation`
- 当前默认行为：
  - CLI 以 stdout JSON 为主，不持久化滚动日志文件。
  - 若使用 `--use-latest-claims`，应优先读取 namespaced claims 目录；legacy root 仅保留兼容读取，不再作为首选落点。
  - 若未来新增文件型结果或审计导出，必须要求显式目标路径，或默认落入受管 result 根目录。
- 历史迁移责任：
  - 旧的 `Meta-github-operation_thread_owned_paths*.json*` 若仍散落在 `Codex_Skill_Runtime` 根目录，应整理迁移到 namespaced claims 目录。

## Remote Policy

- `Octopus_OS`
  - 当前按单远端常规开发仓处理
- `octopus-os-agent-console`
  - `origin`
    - 角色：private development traceability remote
    - 用途：自动迭代、开发日志、同回合 push
    - 写入策略：允许
  - `public-release`
    - 角色：future public release remote
    - 用途：未来人工选择稳定快照后发布
    - 写入策略：当前禁用
    - 禁用原因：开发未闭环至可发布；发布流程尚未设计

## Current Delivery Rule

- 若用户要求正常提交并推送 `octopus-os-agent-console`，默认只推 `origin`
- 若用户明确要求发布到公开仓，必须先声明当前禁用，再解释原因
- 在发布流程尚未设计完成前，不得把 `public-release` 当成可写远端偷偷使用

## Reactivation Boundary

- 这是 GitHub 重构后的第一阶段恢复。
- 若未来要支持更多仓库，必须先扩 registry 与 AGENTS 绑定，再扩工具面。
