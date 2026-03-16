---
doc_id: workflow_motherdoc_octopusos.path.stage_flow.tools
doc_type: topic_atom
topic: Mother doc stage tools
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 工具之后进入校验条件。
---

# mother_doc 工具面

## 当前技能 CLI
- `python3 ./Skills/Workflow-MotherDoc-OctopusOS/scripts/Cli_Toolbox.py target-runtime-contract --json`
- `python3 ./Skills/Workflow-MotherDoc-OctopusOS/scripts/Cli_Toolbox.py stage-checklist --stage mother_doc --json`
- `python3 ./Skills/Workflow-MotherDoc-OctopusOS/scripts/Cli_Toolbox.py stage-doc-contract --stage mother_doc --json`
- `python3 ./Skills/Workflow-MotherDoc-OctopusOS/scripts/Cli_Toolbox.py stage-command-contract --stage mother_doc --json`
- `python3 ./Skills/Workflow-MotherDoc-OctopusOS/scripts/Cli_Toolbox.py mother-doc-lint --json`
- `python3 ./Skills/Workflow-MotherDoc-OctopusOS/scripts/Cli_Toolbox.py mother-doc-refresh-root-index --json`
- `python3 ./Skills/Workflow-MotherDoc-OctopusOS/scripts/Cli_Toolbox.py mother-doc-sync-client-copy --json`
- `python3 ./Skills/Workflow-MotherDoc-OctopusOS/scripts/Cli_Toolbox.py mother-doc-audit --json`

## 共享工作目录
- `target_root`: `Octopus_OS`
- `docs_root`: `Octopus_OS/Development_Docs`
- `mother_doc_root`: `Octopus_OS/Development_Docs/mother_doc`

## 下一跳列表
- [validation]：`30_VALIDATION.md`
