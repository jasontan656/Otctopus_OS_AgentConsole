---
doc_id: skillsmanager_tooling_checkup.path.output_governance.tools
doc_type: topic_atom
topic: Tools for output governance checking
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: output governance tools are applied in the execution step.
---

# 输出落点检查工具

## 当前动作会用到什么
- 本技能的 `scripts/Cli_Toolbox.py govern-target --target-skill-root <path> --json`
- 目标技能现有 CLI、输出参数、配置与写入代码
- 目标技能文档中与日志、产物、落点相关的声明

## 当前动作必须满足什么
- 不能只靠字符串搜索判定输出治理是否成立。
- 必须同时检查：代码写入路径、默认回退、显式参数、文档声明、历史迁移责任。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
