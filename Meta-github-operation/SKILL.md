---
name: "meta-github-operation"
description: "AI-facing Git and GitHub automation control plane for local repositories. Use when work requires precise repository operations such as repo status, branch or divergence checks, scoped commit and push, fetch or pull with rebase, partial rollback, remote inspection, or GitHub traceability without unsafe whole-repo staging. Uses real repository names and safer multi-agent parallel workflows. Deleting repositories is out of scope."
---

# Meta-github-operation

## Overview

这是一个给 AI 使用的 Git/GitHub 自动化控制层。

它的目标不是“快速把整个仓推上去”，而是：

- 精确识别要操作哪个 repo
- 精确识别要提交哪些路径
- 在推送前检查分支、upstream、divergence 和 lease 风险
- 在多 AI 并行改同一仓库时，尽量避免互相污染

唯一明确不交给 AI 的操作是：删除仓库。

## Use This Skill For

当任务涉及以下 Git/GitHub 操作时使用本技能：

- 查询 repo registry、repo path
- 查询 branch、remote、ahead/behind、dirty state
- 精确 commit 指定文件或指定目录
- 精确 push 当前分支或带 `--force-with-lease` 的受控推送
- fetch、pull --rebase、同步本地与远端状态
- 按指定路径回滚到特定 ref，并清理该 ref 下不存在的空目录残留
- 保持 write turn 的 GitHub 留痕，但避免整仓 `git add -A`

## Command Surface

统一入口：

- `python3 scripts/Cli_Toolbox.py registry`
- `python3 scripts/Cli_Toolbox.py status --repo <repo_name>`
- `python3 scripts/Cli_Toolbox.py remote-info --repo <repo_name>`
- `python3 scripts/Cli_Toolbox.py fetch --repo <repo_name>`
- `python3 scripts/Cli_Toolbox.py pull-rebase --repo <repo_name>`
- `python3 scripts/Cli_Toolbox.py commit --repo <repo_name> --message "<msg>" --path <path> [...]`
- `python3 scripts/Cli_Toolbox.py push --repo <repo_name>`
- `python3 scripts/Cli_Toolbox.py commit-and-push --repo <repo_name> --message "<msg>" --path <path> [...]`
- `python3 scripts/Cli_Toolbox.py rollback-paths --repo <repo_name> --to-ref <ref> --path <path> [...]`

`--repo` 默认接受真实仓名，也兼容少量旧别名并自动映射到当前真实仓路径：

- `Codex_Skills_Mirror`
- `OctuposOS_RunTime_Frontend`
- `Octopus_CodeBase_Backend`
- `OctuposOS_Runtime_Backend`
- `Octopus_CodeBase_Frontend`

兼容旧别名：

- `Octopus_CodeBase` -> `Octopus_CodeBase_Backend`
- `OctuposOS_Runtime` -> `OctuposOS_Runtime_Backend`
- `OctuposOS_Runtime_Frontend` -> `OctuposOS_RunTime_Frontend`

## Safety Model

- 默认禁止隐式整仓 staging
- 默认按显式路径或已解析 scope 工作
- 默认 push 前检查当前 branch、upstream、ahead/behind
- 只有显式要求时才允许 `--force-with-lease`
- rollback 仅限指定路径，不提供删库
- rollback 后会向上清理空目录，使本地文件夹形态尽量与目标 ref 一致

## Repo Registry

本技能内建固定 repo registry，并允许直接传入 `--repo-path`：

- `Codex_Skills_Mirror`
- `OctuposOS_RunTime_Frontend`
- `Octopus_CodeBase_Backend`
- `OctuposOS_Runtime_Backend`
- `Octopus_CodeBase_Frontend`

结果产物仓库 `Codex_Skills_Result` 不属于固定 registry 管理范围；当该本地目录存在但远端已删除时，不应把它重新加入本技能的受管仓库列表。

## Parallel-Agent Friendly Default

当多个 AI 并行时，本技能的默认策略是：

- 不假设“当前仓里所有改动都属于我”
- 允许每个线程刷新自己的 claims 文件来声明本线程负责的路径范围
- 优先消费线程 claims 文件中的路径范围
- 如果没有 claims，就优先使用已 staged 的路径
- 如果既没有 claims 也没有 staged 路径，则只在“恰好 1 个变更路径”时自动收口
- 其余情况直接报 scope ambiguous，让调用方改用显式 `--path`

## Non-Goals

- 不提供删库能力
- 不提供 PR 审核流或 GitHub Web UI 自动化
- 不把 Git 教程塞进技能正文
