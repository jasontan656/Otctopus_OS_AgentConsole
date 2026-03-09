# Mother_Doc AGENTS/README Branch

适用阶段：`mother_doc`

## Purpose

- 本分支统一管理 3 类路径：
  - `octopus_os_root`: `Octopus_OS/AGENTS.md + README.md`
  - `container_roots`: `Octopus_OS/<Container_Name>/AGENTS.md + README.md`
  - `mother_doc_docs`: `Octopus_OS/Mother_Doc/docs/**/AGENTS.md + README.md`
- 目标是让所有 AGENTS/README 模板都由技能侧统一索引、统一推送、统一回收。
- 本分支只做 `scan / collect / push`，不写普通文档正文。

## Managed Path Branches

- `octopus_os_root`
  - 目标路径：`Octopus_OS/AGENTS.md`
  - 用途：总容器根索引，先引导模型理解章鱼OS技能锚点；如有需要，再读 `Octopus_OS/README.md`。
- `container_roots`
  - 目标路径：`Octopus_OS/<Container_Name>/AGENTS.md`
  - 用途：每个容器根自己的开发回写合同入口，并回指同层 `README.md`。
- `mother_doc_docs`
  - 目标路径：`Octopus_OS/Mother_Doc/docs/**/AGENTS.md`
  - 用途：Mother_Doc 文档树的递归索引入口，并回指同层 `README.md`。

## Stage Entry

- `scan`
  - 规则/流程入口：[`scan/INSTRUCTION.md`](stages/scan/INSTRUCTION.md)
  - 用途：扫描当前文档树中的 `AGENTS.md + README.md` 实际状态。
- `collect`
  - 规则/流程入口：[`collect/INSTRUCTION.md`](stages/collect/INSTRUCTION.md)
  - 用途：把产品侧 `AGENTS.md + README.md` 反向采集回技能侧 registry。
- `push`
  - 规则/流程入口：[`push/INSTRUCTION.md`](stages/push/INSTRUCTION.md)
  - 用途：把技能侧当前模板反推回整棵文档树。

## Runtime Entry

- [运行合同 JSON](runtime/AGENTS_BRANCH_CONTRACT.json)
- [运行合同审计版](runtime/AGENTS_BRANCH_CONTRACT.md)
- CLI 合同：`python3 scripts/Cli_Toolbox.py mother-doc-agents-contract --json`
- CLI 阶段指引：`python3 scripts/Cli_Toolbox.py mother-doc-agents-directive --stage <scan|collect|push> --json`
- 模板资产根：`assets/mother_doc_agents/templates/`
- 模板索引：`assets/mother_doc_agents/index.md`
