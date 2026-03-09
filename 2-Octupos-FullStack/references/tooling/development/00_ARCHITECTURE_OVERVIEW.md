# Cli_Toolbox Architecture Overview

适用技能：`2-Octupos-FullStack`

## 当前范围

- 当前提供一个统一 CLI 入口下的五个命令：
  - `Cli_Toolbox.mother_doc_stage`
  - `Cli_Toolbox.materialize_container_layout`
  - `Cli_Toolbox.sync_mother_doc_navigation`
  - `Cli_Toolbox.implementation_stage`
  - `Cli_Toolbox.evidence_stage`

## 目标

- 用同一 CLI 入口显式分隔 `mother_doc`、`implementation`、`evidence` 三阶段作用域。
- 在 `mother_doc` 阶段为 AI 提供可执行的目录物化与递归导航刷新入口。
- 保证 `Mother_Doc` 每一层目录都具备 `README.md + agents.md`。
- 保持幂等。
