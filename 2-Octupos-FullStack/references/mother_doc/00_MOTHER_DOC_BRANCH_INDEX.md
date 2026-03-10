# Mother_Doc Branch Index

## 分支选择

- `direct_writeback`: 直接写当前明确的 Mother_Doc 内容。
- `question_backfill`: 先写已知内容，再回填仍未定的设计问题。
- `AGENTS manager`: 只处理 `Octopus_OS/AGENTS.md` 的统一治理映射，不再处理 container roots 或 `Mother_Doc/docs` 树的递归 AGENTS。

## AGENTS manager 入口

- `python3 scripts/Cli_Toolbox.py mother-doc-agents-contract --json`
- `python3 scripts/Cli_Toolbox.py mother-doc-agents-directive --stage <scan|collect|push> --json`
- `python3 scripts/Cli_Toolbox.py mother-doc-agents-registry --json`
