[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在处理当前模块开发文档与施工闭环之前，必须先运行：
- `<root>/octopus-os-agent-console/.venv_backend_skills/bin/python <root>/octopus-os-agent-console/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "{{external_agents_path}}" --json`

2. 模块开发文档容器
- 当前目标项目根：`{{target_root}}`
- 当前开发文档总容器：`{{development_docs_root}}`
- 当前模块文档容器：`{{module_docs_root}}`
- 当前模块标识：`{{module_dir}}`
- mother doc root：`{{mother_doc_root}}`
- execution packs root：`{{construction_plan_root}}`
- graph root：`{{graph_runtime_root}}`

3. DevFlow 闭环入口
- 当前模块的开发文档、任务包、evidence 与 acceptance 闭环由 `$Workflow-OctopusOS-DevFlow` 治理。
- 进入任何阶段前，必须先运行：
- `<root>/octopus-os-agent-console/.venv_backend_skills/bin/python <root>/octopus-os-agent-console/Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py target-runtime-contract --target-root "{{target_root}}" --module-dir "{{module_dir}}" --json`
- 若当前模块已经存在 mother_doc、编号归档、execution packs 或 graph，必须先复用当前脉络；禁止另起脱节文档线。

4. 治理链约束
- 本文件属于 `Meta-RootFile-Manager` 的受管外部 `AGENTS.md`，外部文件只允许承载 `Part A`。
- 更新本文件时，必须使用 `$Meta-RootFile-Manager` 的 `collect` / `push` / `scaffold` 流程，避免治理链断裂。
- 本模块下的开发文档、任务包、graph、evidence 回写和 acceptance 收口，必须同时遵守 `$Workflow-OctopusOS-DevFlow` 的阶段合同。
</part_A>
