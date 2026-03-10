---
name: "2-Octupos-FullStack"
description: "未来项目 admin panel 内置的运营AI“章鱼”，负责 mother_doc、implementation 与 evidence 三阶段。"
---

# 2-Octupos-FullStack

## 1. 目标
- 本技能用于 `Octopus_OS` 的全栈文档驱动开发与落盘维护。
- 本技能是 `Octopus_OS` 的开发操作手册门面，运行对象是内置运营AI“章鱼”。
- 阶段固定为：`mother_doc`、`implementation`、`evidence`。
- 长规则不在门面展开；门面只负责给出中文说明、人类导航与 CLI 入口。

## 2. 运行入口
- 统一入口：[Cli_Toolbox.py](scripts/Cli_Toolbox.py)
- 模型进入本技能后，先读取 skill 级 CLI 运行合同：
  - `python3 scripts/Cli_Toolbox.py skill-runtime-contract --json`
  - `python3 scripts/Cli_Toolbox.py skill-facade-contract --json`
- CLI JSON 是运行态唯一优先来源；技能内 markdown 不作为模型运行规则主来源。
- `AGENTS/README manager`、阶段合同、阶段命令、目标级合同都继续从 CLI JSON 下钻。

## 3. 中文门面说明
- 本技能保留中文说明，便于人类审计和理解阶段语义。
- 下沉到 CLI 的规则允许使用英文输出，只要运行态表达更稳定、更适合模型消费。
- `mother_doc` 负责当前态文档结构与容器语义。
- `implementation` 负责按当前文档结构实现并对齐代码。
- `evidence` 负责收集真实证据、日志与 graph 绑定。

## 4. 规则约束
- 顶层规则入口：[FULLSTACK_SKILL_HARD_RULES.md](rules/FULLSTACK_SKILL_HARD_RULES.md)
- skill 级运行合同入口：
  - CLI: `python3 scripts/Cli_Toolbox.py skill-runtime-contract --json`
  - CLI: `python3 scripts/Cli_Toolbox.py skill-facade-contract --json`
  - machine audit source: `references/runtime/SKILL_RUNTIME_CONTRACT.json`
  - human audit source: `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- `AGENTS/README manager` 分支运行合同入口：
  - CLI: `python3 scripts/Cli_Toolbox.py mother-doc-agents-contract --json`
  - CLI: `python3 scripts/Cli_Toolbox.py mother-doc-agents-directive --stage <scan|collect|push> --json`
  - CLI: `python3 scripts/Cli_Toolbox.py mother-doc-agents-registry --json`
  - CLI: `python3 scripts/Cli_Toolbox.py mother-doc-agents-target-contract --relative-path "<PATH>" --file-kind <agents|readme> --json`
  - machine cache: `assets/mother_doc_agents/runtime_rules/**/**/*.runtime.json`
  - human audit source: `assets/mother_doc_agents/runtime_rules/**/AGENT_AUDIT.md` / `README_AUDIT.md`
- 规则正文不在本门面重复抄写。

## 5. 人类审计导航
- [总入口图](references/skill_native/01_FACADE_LOAD_MAP.md)
- [skill native 索引](references/skill_native/00_SKILL_NATIVE_INDEX.md)
- [项目统一目标基线](references/skill_native/10_PROJECT_BASELINE_INDEX.md)
- [顶层规则](rules/FULLSTACK_SKILL_HARD_RULES.md)
- [运行合同](references/runtime/SKILL_RUNTIME_CONTRACT.md)
- [authored domains 索引](references/authored_domains/00_DOMAIN_INDEX.md)
- [工具入口](scripts/Cli_Toolbox.py)

## 6. 运行边界
- 模型默认先跑 CLI，再决定是否查看 markdown 审计版。
- `mother_doc_agents` 分支默认走 `branch contract JSON -> stage directive JSON -> registry/target contract JSON`，并把 branch index 的关键信息下沉到 CLI JSON payload。
- markdown 保留的内容限于：
  - 技能中文简介
  - 人类审计导航
  - 结构索引
- 任何会影响模型执行判断的规则，优先维护在脚本输出或其 JSON 源中，而不是维护在门面 markdown 中。
