---
doc_id: workflow_sitemap_creation.references.tooling.cli_toolbox_usage
doc_type: topic_atom
topic: CLI usage for Workflow-SiteMap-Creation
---

# Cli_Toolbox Usage

## Read Contract

- `python3 scripts/Cli_Toolbox.py contract --json`
- `python3 scripts/Cli_Toolbox.py directive --topic self_governance_mainline --json`
- `python3 scripts/Cli_Toolbox.py directive --topic background_subagent_mainline --json`
- `python3 scripts/Cli_Toolbox.py read-contract-context --entry self_governance --json`
- `python3 scripts/Cli_Toolbox.py read-contract-context --entry artifact_lint_audit --json`

## Resolve Runtime

- `python3 scripts/Cli_Toolbox.py target-runtime-contract --target-root /abs/Octopus_OS --json`

## Managed Mainline

- `python3 scripts/Cli_Toolbox.py factory-intake --request-text "..." --json`
- `python3 scripts/Cli_Toolbox.py intent-enhance --request-text "..." --json`
- `python3 scripts/Cli_Toolbox.py runtask-subagent-run --request-text "..." --json`
- `python3 scripts/Cli_Toolbox.py subagent-status --json`
- `python3 scripts/Cli_Toolbox.py artifact-refresh --target-root /abs/Octopus_OS --json`
- `python3 scripts/Cli_Toolbox.py self-governance-run --target-root /abs/Octopus_OS --request-file /tmp/request.txt --json`

## Audit

- `python3 scripts/Cli_Toolbox.py artifact-lint-audit --target-root /abs/Octopus_OS --json`

## Mainline Expectation

- `self-governance-run` 必须按 `factory -> Meta-Enhance-Prompt -> tmux subagent -> Functional-Analysis-Runtask -> artifact refresh -> validation closeout` 顺序执行。
- `runtask-subagent-run` 必须持续轮询输出；只有连续 `10` 分钟无新输出时才允许判死。
