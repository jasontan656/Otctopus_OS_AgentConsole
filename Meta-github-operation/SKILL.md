---
name: "meta-github-operation"
description: "受限 GitHub control plane：仅服务 Octopus_OS 与 Codex_Skills_Mirror 两个仓库的状态、提交、推送与远端信息操作。"
---

# Meta-github-operation

## Status

本技能已恢复为受限启用状态，但当前只服务以下两个仓库：
- `/home/jasontan656/AI_Projects/Octopus_OS`
- `/home/jasontan656/AI_Projects/Codex_Skills_Mirror`

## Scope

- 允许：
  - repo registry
  - status / remote-info
  - fetch / pull-rebase
  - push-contract
  - commit / commit-and-push / push
  - rollback-contract
  - rollback-paths
  - rollback-sync
- 不允许：
  - 超出上述两个仓库的 Git / GitHub 自动化调用
  - 仓库删除
  - 整个 workspace 根目录级 Git 操作

## Entry

- CLI 入口：`scripts/Cli_Toolbox.py`
- registry 固定只暴露：
  - `Octopus_OS`
  - `Codex_Skills_Mirror`

## Reactivation Boundary

- 这是 GitHub 重构后的第一阶段恢复。
- 若未来要支持更多仓库，必须先扩 registry 与 AGENTS 绑定，再扩工具面。
