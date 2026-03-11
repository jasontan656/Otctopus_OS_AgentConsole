# Cli_Toolbox 使用文档

适用技能：`skill-creation-template`

## 命名约束
- 本技能内工具统一使用 `Cli_Toolbox.<tool_name>` 命名。

## 工具清单
- `Cli_Toolbox.create_skill_from_template`
  - 入口：`scripts/Cli_Toolbox.py create-skill-from-template`
  - 用途：基于受治理模板创建或改造技能骨架。
- `Cli_Toolbox.skill_template`
  - 入口：`scripts/Cli_Toolbox.py skill-template`
  - 用途：输出 `basic` profile 的 7 章门面模板。
- `Cli_Toolbox.staged_skill_template`
  - 入口：`scripts/Cli_Toolbox.py staged-skill-template`
  - 用途：输出 `staged_cli_first` profile 的 staged 门面模板。
- `Cli_Toolbox.openai_template`
  - 入口：`scripts/Cli_Toolbox.py openai-template`
  - 用途：输出 `agents/openai.yaml` 模板。
- `Cli_Toolbox.contract_reference`
  - 入口：`scripts/Cli_Toolbox.py contract-reference`
  - 用途：输出技能模板作者合同。
- `Cli_Toolbox.staged_skill_reference`
  - 入口：`scripts/Cli_Toolbox.py staged-skill-reference`
  - 用途：输出 `staged_cli_first` profile 的通用参考。
- `Cli_Toolbox.runtime_contract_template`
  - 入口：`scripts/Cli_Toolbox.py runtime-contract-template`
  - 用途：输出 staged runtime contract 模板资产。
- `Cli_Toolbox.architecture_playbook`
  - 入口：`scripts/Cli_Toolbox.py architecture-playbook`
  - 用途：输出技能架构手册。
- `Cli_Toolbox.runtime_contract`
  - 入口：`scripts/Cli_Toolbox.py runtime-contract`
  - 用途：输出本技能运行合同。

## 叙事式使用说明

### Cli_Toolbox.runtime_contract
- 人类叙事版输入：
  - 我先想知道这个模板技能现在到底要求我按什么结构创建技能。
- 电脑动作发生了什么：
  - 系统执行 `python3 scripts/Cli_Toolbox.py runtime-contract --json`。
  - 命令读取 `references/runtime/SKILL_RUNTIME_CONTRACT.json` 并输出结构化合同。
- 人类叙事版输出：
  - 你会得到当前模板技能的门面结构、profile 支持、工具映射、模板资产契约和验证闭环。

### Cli_Toolbox.create_skill_from_template
- 人类叙事版输入：
  - 我想创建一个新技能，并直接拿到受治理的骨架。
- 电脑动作发生了什么：
  - 系统执行 `python3 scripts/Cli_Toolbox.py create-skill-from-template --skill-name my-skill --target-root ~/.codex/skills --profile staged_cli_first --overwrite`。
  - 脚本会生成 `SKILL.md`、`agents/openai.yaml`、tooling 文档、开发索引，并默认创建 `tests/`。
  - 若使用 `--profile staged_cli_first`，还会补齐：
    - `references/runtime/*`
    - `references/stages/00_STAGE_INDEX.md`
    - `assets/templates/stages/README_STAGE_SYSTEM.md`
    - stage checklist 模板
    - stage doc/command/graph contract 模板
  - 生成门面默认采用标准化 7 章结构，而不是旧的抽象层/业务层堆叠标题。
- 人类叙事版输出：
  - 你会得到一个可直接继续编辑和治理的技能目录，以及 JSON 结果（`skill_dir`、`profile`、`resources_created`、`write_results`）。

### Cli_Toolbox.skill_template
- 人类叙事版输入：
  - 我需要一份 basic skill 的受治理门面模板。
- 电脑动作发生了什么：
  - 系统执行 `python3 scripts/Cli_Toolbox.py skill-template --json`。
- 人类叙事版输出：
  - 你会得到采用 `技能定位/适用域/可用工具简述&入口/文档指引&入口/工作流指引/顶层常驻通用规则/结构索引` 的 basic 门面草稿。

### Cli_Toolbox.staged_skill_template
- 人类叙事版输入：
  - 我需要一份复杂 staged skill 的门面模板。
- 电脑动作发生了什么：
  - 系统执行 `python3 scripts/Cli_Toolbox.py staged-skill-template --json`。
- 人类叙事版输出：
  - 你会得到一份强调 resident docs、stage checklist、合同四件套和 stage-switch discard policy 的 staged 门面草稿。

### Cli_Toolbox.runtime_contract_template
- 人类叙事版输入：
  - 我需要 staged skill 的 runtime contract 骨架。
- 电脑动作发生了什么：
  - 系统执行 `python3 scripts/Cli_Toolbox.py runtime-contract-template --json`。
- 人类叙事版输出：
  - 你会拿到要求 `skill_md_role`、`routing_protocol`、`resident_doc_policy`、`stage_contract_policy` 的 contract 模板。

### Cli_Toolbox.staged_skill_reference
- 人类叙事版输入：
  - 我想知道 staged 模板到底要求保留哪些稳定结构。
- 电脑动作发生了什么：
  - 系统执行 `python3 scripts/Cli_Toolbox.py staged-skill-reference --json`。
- 人类叙事版输出：
  - 你会得到“哪些结构必须保留，哪些项目专有语义必须剔除”的通用参考。

## 参数与结果
- 核心输入参数：`create-skill-from-template` 的 `--skill-name`、`--target-root`、`--resources`、`--description`、`--profile`、`--overwrite`
- 默认资源：`scripts,references,assets,tests`
- 核心输出结构：
  - `create-skill-from-template`：JSON（`skill_dir`、`profile`、`resources_created`、`write_results`）
  - 资源查询类命令：JSON（`asset/path/content`）
- 失败返回：参数缺失、模板文件缺失或路径不可写时返回非零退出码

## 同步维护要求
- 工具变更后必须同步更新本文件与 `Cli_Toolbox_DEVELOPMENT.md`。
- 若变更了门面结构、staged 合同面或默认生成资源，还必须同步：
  - `references/runtime/SKILL_RUNTIME_CONTRACT.json`
  - `references/skill_template_contract_v1.md`
  - `references/staged_cli_first_profile_reference.md`
  - `references/skill_architecture_playbook.md`
  - `assets/skill_template/*`
  - `tests/test_create_skill_from_template_regression.py`
