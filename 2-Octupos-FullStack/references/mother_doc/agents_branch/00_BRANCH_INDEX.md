# Mother_Doc AGENTS Branch

适用阶段：`mother_doc`

## Purpose

- 本分支只管理 `Octopus_OS/Mother_Doc/docs/**/AGENTS.md`。
- 目标是让 `AGENTS.md` 成为 Mother_Doc 树的单一递归索引入口，并为后续 `OS_graph` 提供稳定 index。
- 本分支只做 `scan / collect / push`，不写普通文档正文。

## Stage Entry

- `scan`
  - 规则/流程入口：[`scan/INSTRUCTION.md`](stages/scan/INSTRUCTION.md)
  - 用途：扫描当前文档树中的 `AGENTS.md` 实际状态。
- `collect`
  - 规则/流程入口：[`collect/INSTRUCTION.md`](stages/collect/INSTRUCTION.md)
  - 用途：把产品侧 `AGENTS.md` 反向采集回技能侧 registry。
- `push`
  - 规则/流程入口：[`push/INSTRUCTION.md`](stages/push/INSTRUCTION.md)
  - 用途：把技能侧当前模板反推回整棵文档树。

## Runtime Entry

- [运行合同 JSON](runtime/AGENTS_BRANCH_CONTRACT.json)
- [运行合同审计版](runtime/AGENTS_BRANCH_CONTRACT.md)
- CLI 合同：`python3 scripts/Cli_Toolbox.py mother-doc-agents-contract --json`
- CLI 阶段指引：`python3 scripts/Cli_Toolbox.py mother-doc-agents-directive --stage <scan|collect|push> --json`
