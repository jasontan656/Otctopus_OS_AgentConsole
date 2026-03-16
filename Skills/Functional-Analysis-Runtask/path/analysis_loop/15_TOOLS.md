---
doc_id: functional_analysis_runtask.path.analysis_loop.tools
doc_type: action_tool_doc
topic: Analysis loop tools
reading_chain:
- key: workflow_index
  target: 20_WORKFLOW_INDEX.md
  hop: next
  reason: 工具面之后进入主阶段索引。
---

# analysis_loop 工具面

## 运行时与编译命令
- `python3 ../Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py contract --json`
- `python3 ../Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py directive --topic task-routing --json`
- `python3 ../Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py directive --topic execution-boundary --json`
- `python3 ../Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py paths --json`
- `python3 ./scripts/Cli_Toolbox.py runtime-contract --json`
- `python3 ./scripts/Cli_Toolbox.py task-gate-check --json`
- `python3 ./scripts/Cli_Toolbox.py task-runtime-scaffold --task-name <slug> --workspace-root <path> --json`
- `python3 ./scripts/Cli_Toolbox.py read-contract-context --entry analysis_loop --selection architect --json`
- `python3 ./scripts/Cli_Toolbox.py read-contract-context --entry analysis_loop --selection impact --json`
- `python3 ./scripts/Cli_Toolbox.py read-path-context --entry analysis_loop --selection implementation --json`
- `python3 ./scripts/Cli_Toolbox.py stage-checklist --stage preview --json`
- `python3 ./scripts/Cli_Toolbox.py workspace-scaffold --workspace-root <path> --json`
- `python3 ./scripts/Cli_Toolbox.py stage-lint --workspace-root <path> --stage all --json`

## 小型对象参考
- `supporting/LIGHTWEIGHT_RUNTASK_OBJECT_MODEL.md`

## 任务产物落盘顺序
1. 先用 `Functional-HumenWorkZone-Manager` 确认当前任务属于哪个 `Human_Work_Zone` 受管分区。
2. 若属于临时治理文件或尚未确定长期归宿的任务产物，固定落到 `Temporary_Files/`。
3. 新任务必须先执行 `task-gate-check`，确认不存在未闭合历史任务。
4. 通过 gate 后，先生成 `Codex_Skill_Runtime/Functional-Analysis-Runtask/NNN_task_slug/task_runtime.yaml`。
5. `workspace-scaffold` 必须一次性生成九阶段对象与正式产物 skeleton。
6. 只有受管 root 已确定且 task runtime 已建立后，才允许执行 `workspace-scaffold`。

## 下一跳列表
- [workflow_index]：`20_WORKFLOW_INDEX.md`
