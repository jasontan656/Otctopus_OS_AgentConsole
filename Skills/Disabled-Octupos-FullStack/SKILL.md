---
name: "Disabled-Octupos-FullStack"
description: "暂时不启用，避免被误触发；仅保留为可修改的历史章鱼全栈技能。"
---

# Disabled-Octupos-FullStack

## 目标

- 当前状态：暂时不启用，避免被误触发；仅在明确点名进行遗留查看、迁移或改造时使用。
- 本技能用于 `Octopus_OS` 的全栈文档驱动开发与落盘维护。
- 阶段固定为：`mother_doc`、`implementation`、`evidence`。
- CLI JSON 是运行态唯一优先来源。

## 当前收敛状态

- 当前 AGENTS 治理只剩一个对象：`Octopus_OS/AGENTS.md`。
- mirror 内部只保留一组 managed assets：
- `assets/managed_targets/Octopus_OS/AGENTS_human.md`
- `assets/managed_targets/Octopus_OS/AGENTS_machine.json`
- 运行时导航固定走 `branch contract -> stage directive -> target contract`。

## AGENTS Manager 入口

- `python3 scripts/Cli_Toolbox.py mother-doc-agents-contract --json`
- `python3 scripts/Cli_Toolbox.py mother-doc-agents-directive --stage <scan|collect|push> --json`
- `python3 scripts/Cli_Toolbox.py mother-doc-agents-target-contract --relative-path "octopus_os_root" --file-kind agents --json`
- `python3 scripts/Cli_Toolbox.py mother-doc-agents-scan --json`
- `python3 scripts/Cli_Toolbox.py mother-doc-agents-collect --json`
- `python3 scripts/Cli_Toolbox.py mother-doc-agents-push --json`
