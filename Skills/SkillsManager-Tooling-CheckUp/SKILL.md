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
- 不适用于：目标技能形态治理，包括 skill root 结构、`SKILL.md` 门面组织、path chain 组织、reading-chain 组织。
- 不适用于：Python / TypeScript 语言专属代码规范正文；这类规则交由对应 constitution 技能。

## 3. 运行时边界
- 本技能只治理 tooling surface，不反向要求目标技能继承本技能自己的 `references/runtime_contracts/` 或 CLI-first 门面形态。
- 对 path 技能的要求只有一条新增硬规则：
  - 若目标技能同时存在 `scripts/` 与 `path/`，且不是 `guide_only`，则必须提供可工作的 `read-path-context`。
- `read-path-context` 的职责是：
  - 接收一个功能入口
  - 沿目标技能 frontmatter 中的 `reading_chain` 逐级向下
  - 输出稳定 JSON
  - 返回完整 `resolved_chain / segments / compiled_markdown`
- CLI 是文档真源的编译器，不是另一套独立真源。

## 4. 必读顺序
1. 先执行 `contract --json`。
2. 再按任务选择 `directive --topic <topic> --json`。
3. 若任务进入具体目标技能，使用 `govern-target --target-skill-root <path> --json`。
4. 只有当 JSON 仍留下真实语义缺口时，才回读 human mirror 或 legacy 参考文档。

## 5. 约束
- 不得把目标技能缺少某种 root 形态误判成 tooling 违规。
- 不得把 `reading_chain` 的组织规则解释成由本技能治理；本技能只检查 path 技能是否能用 CLI 正确编译这条链。
- 不得把 Python 胖文件、typing 风格、异常风格等语言规范重新写回本技能。
- 若目标技能的 `read-path-context` 输出顺序错误、漏节点、跨链污染或 JSON 不稳定，应判为 tooling 违规。

## 6. 参考入口
- Runtime 合同：`references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json`
- Directive 索引：`references/runtime_contracts/DIRECTIVE_INDEX.json`
- Human mirrors：`references/runtime_contracts/*_human.md`
