---
doc_id: functional_humenworkzone_manager.runtime_contracts.execution_boundary_contract
doc_type: topic_atom
topic: EXECUTION_BOUNDARY_CONTRACT
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This contract belongs to the governed skill tree under the main facade.
---

# EXECUTION_BOUNDARY_CONTRACT

<part_A>
- 本 contract 说明 `Functional-HumenWorkZone-Manager` 的写边界：只管理 `Human_Work_Zone` 及其 intake 流程。
- 模型运行时应先调用 `./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py directive --topic execution-boundary --json` 获取 payload。
- 人类可以看本 mirror；模型仍应以 Part B payload 为主。
</part_A>

<part_B>

```json
{
  "directive_name": "functional_humenworkzone_manager_execution_boundary_contract",
  "directive_version": "1.0.0",
  "doc_kind": "contract",
  "topic": "execution-boundary",
  "purpose": "Keep Functional-HumenWorkZone-Manager file operations scoped to Human_Work_Zone and its managed intake flows.",
  "instruction": [
    "Lock the managed target to Human_Work_Zone before any move, rename, delete, or README update.",
    "Allow external source paths only as intake origins; the managed destination must still resolve under Human_Work_Zone.",
    "Use paths --json whenever the canonical destination zone is not already obvious from the active branch."
  ],
  "workflow": [
    "Confirm whether the user request is read-only or write execution.",
    "If the task writes files, resolve the managed zone first and keep the destination under Human_Work_Zone.",
    "Temporary governance files must still land inside the registered Temporary_Files zone; do not create ad hoc sibling folders at the Human_Work_Zone root.",
    "When intake changes folder names, preserve content bodies and only normalize the container name and inventory entries.",
    "After file placement changes, update the relevant zone README before closing the turn."
  ],
  "rules": [
    "Do not use this skill to govern the whole workspace.",
    "Do not move files into unregistered ad hoc folders outside the managed zones.",
    "Do not leave stale inventory entries after renames, moves, or removals."
  ]
}
```
</part_B>
