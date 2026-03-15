---
name: SkillsManager-Tooling-CheckUp
description: 治理技能内部 CLI 与 tooling surface 的规则规范，重点覆盖依赖基线、输出落点、职责边界与链路编译 CLI。
metadata:
  doc_structure:
    doc_id: skillsmanager_tooling_checkup.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Tooling-CheckUp skill
    reading_chain:
    - key: skill_runtime_contract
      target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json
      hop: entry
      reason: This skill remains CLI-first and routes runtime work through the local contract payload.
---

# SkillsManager-Tooling-CheckUp

## 1. 工具入口
- 本技能提供本地 CLI：
  - `contract`
  - `directive`
  - `govern-target`
- 运行时统一入口：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py contract --json`
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py directive --topic <topic> --json`
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py govern-target --target-skill-root <path> --json`
- 本技能仍采用 CLI-first 运行时；本门面只声明边界与入口，不承担运行时正文。

## 2. 适用域
- 适用于：已安装或已镜像 skill 内部的 Python / TypeScript / Vue tooling code、CLI glue code、parser / schema / helper / lint / test 代码的治理。
- 适用于：判断是否绕开 repo 当前 `skills_required_techstacks`，是否出现重复造轮子或机械自实现。
- 适用于：治理日志落盘、默认产物落点、定向输出、历史迁移责任。
- 适用于：治理本地 CLI 的命令命名、参数契约、JSON 输出、错误返回与 runtime-facing assets 一致性。
- 适用于：检查带 `scripts/` 且带 `path/` 的技能，是否提供可工作的 `read-path-context`，并能把文档真源编译成完整链路上下文。

## 3. 运行时边界
- 带 `scripts/ + path/` 且不是 `guide_only` 的技能，需要提供可工作的 `read-path-context`。
- `read-path-context` 读取一个功能入口，沿 `reading_chain` 向下，返回 `resolved_chain / segments / compiled_markdown`。
- CLI 输出的是文档链的编译结果，不是另一套独立真源。

## 4. 必读顺序
1. 先执行 `contract --json`。
2. 再按任务选择 `directive --topic <topic> --json`。
3. 若任务进入具体目标技能，使用 `govern-target --target-skill-root <path> --json`。
4. 只有当 JSON 仍留下真实语义缺口时，才回读 human mirror 或 legacy 参考文档。

## 5. 约束
- 文档形态问题不算 tooling 违规。
- `reading_chain` 的组织规则不在本技能内裁决；这里只检查 CLI 是否能正确编译它。
- Python 胖文件、typing 风格、异常风格等语言规范继续交给对应 constitution。
- 若 `read-path-context` 输出顺序错误、漏节点、跨链污染或 JSON 不稳定，应判为 tooling 违规。

## 6. 参考入口
- Runtime 合同：`references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json`
- Directive 索引：`references/runtime_contracts/DIRECTIVE_INDEX.json`
- Human mirrors：`references/runtime_contracts/*_human.md`
