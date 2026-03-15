---
doc_id: skillsmanager_tooling_checkup.path.remediation.tools
doc_type: topic_atom
topic: Tools for tooling remediation
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: remediation tools are applied in the execution step.
---

# 整改工具

## 当前动作会用到什么
- 目标技能现有测试与 lint 命令
- 目标技能自己的 CLI 与 `read-path-context`
- 本技能的 `scripts/Cli_Toolbox.py govern-target --target-skill-root <path> --json`
- 若改动涉及 Python：`Dev-PythonCode-Constitution` 对应 lint

## 当前动作必须满足什么
- 先读目标技能自己的合同与执行面，再动手修改。
- 整改验证优先使用目标技能现有命令，而不是新造并行验证面。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
