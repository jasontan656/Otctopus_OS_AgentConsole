---
doc_id: skillsmanager_tooling_checkup.path.techstack_baseline.tools
doc_type: topic_atom
topic: Tools for techstack baseline checking
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: baseline tools are applied in the execution step.
---

# 依赖基线检查工具

## 当前动作会用到什么
- 本技能的 `scripts/Cli_Toolbox.py govern-target --target-skill-root <path> --json`
- 目标技能现有 `scripts/`、测试命令与 lint 命令
- repo 已声明的 `skills_required_techstacks`
- 目标技能相关代码与文档

## 当前动作必须满足什么
- `govern-target` 只给出 tooling surface 的首轮审计，不替代行为证据本身。
- 基线判断必须回到目标代码和调用语义，不得只凭文件名、函数名或模式相似度定性。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
