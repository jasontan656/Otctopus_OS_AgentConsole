# Cli_Toolbox 使用文档

适用技能：`Meta-Skill-Template`

## 命名约束
- 本技能内工具统一使用 `Cli_Toolbox.<tool_name>` 命名。

## 工具清单
- `Cli_Toolbox.create_skill_from_template`
  - 入口：`scripts/Cli_Toolbox.py create-skill-from-template`
  - 用途：基于模板创建或更新技能骨架，并写入标准文档结构。
- `Cli_Toolbox.skill_template`
  - 入口：`scripts/Cli_Toolbox.py skill-template`
  - 用途：提供 1-7 章节描述模板。
- `Cli_Toolbox.openai_template`
  - 入口：`scripts/Cli_Toolbox.py openai-template`
  - 用途：提供 `agents/openai.yaml` 基线结构。
- `Cli_Toolbox.contract_reference`
  - 入口：`scripts/Cli_Toolbox.py contract-reference`
  - 用途：输出模板契约参考。
- `Cli_Toolbox.architecture_playbook`
  - 入口：`scripts/Cli_Toolbox.py architecture-playbook`
  - 用途：输出模板架构手册。
- `Cli_Toolbox.runtime_contract`
  - 入口：`scripts/Cli_Toolbox.py runtime-contract`
  - 用途：输出本技能运行合同。

## 叙事式使用说明（固定格式）

### Cli_Toolbox.runtime_contract
- 人类叙事版输入：
  - 我先想知道这个技能本身的运行边界和入口。
- 电脑动作发生了什么：
  - 系统执行 `python3 scripts/Cli_Toolbox.py runtime-contract --json`。
  - 命令读取 `references/runtime/SKILL_RUNTIME_CONTRACT.json` 并输出结构化合同。
- 人类叙事版输出：
  - 你会得到本技能的路由边界、工具映射和治理规则，不需要把这些细节继续堆回 `SKILL.md`。

### Cli_Toolbox.create_skill_from_template
- 人类叙事版输入：
  - 我想新建一个技能，名称是 `my-skill`，并且希望把目录自动搭好。
- 电脑动作发生了什么：
  - 系统执行 `python3 scripts/Cli_Toolbox.py create-skill-from-template --skill-name my-skill --target-root ~/.codex/skills --overwrite`。
  - 脚本按模板生成 `SKILL.md`、`agents/openai.yaml`、`references/tooling/*` 以及开发文档分层结构。
  - 生成内容会显式避免把“创建技能本身”写入被创建技能的 `1.目标` 章节。
  - 若技能后续存在运行态规则、约束、指引，模板正文会要求补齐 CLI 输出入口、machine-readable 合同与 markdown 审计版。
- 人类叙事版输出：
  - 你会得到一个可直接继续编辑的技能目录，并看到 JSON 结果（`skill_dir`、`resources_created`、`write_results`），可快速确认是否成功。

### Cli_Toolbox.skill_template
- 人类叙事版输入：
  - 我需要一份不会漏章节的技能描述正文框架。
- 电脑动作发生了什么：
  - 系统执行 `python3 scripts/Cli_Toolbox.py skill-template --json`，返回模板路径与正文内容。
- 人类叙事版输出：
  - 你会得到一份结构完整的 `SKILL.md` 草稿，可直接填内容，不会因为漏章导致契约不合规。

### Cli_Toolbox.openai_template
- 人类叙事版输入：
  - 我需要快速补齐 `agents/openai.yaml` 的标准接口字段。
- 电脑动作发生了什么：
  - 系统执行 `python3 scripts/Cli_Toolbox.py openai-template --json`，返回模板路径与内容。
- 人类叙事版输出：
  - 你会得到一个结构规范、可被系统识别的 `openai.yaml`，方便后续技能识别和调用。

### Cli_Toolbox.contract_reference
- 人类叙事版输入：
  - 我需要核对模板契约细节，不想让这些规则堆在 `SKILL.md`。
- 电脑动作发生了什么：
  - 系统执行 `python3 scripts/Cli_Toolbox.py contract-reference --json`。
- 人类叙事版输出：
  - 你会拿到契约文档内容和路径，便于比对治理要求。

## 参数与结果（供 AI/工程使用）
- 核心输入参数：`create-skill-from-template` 的 `--skill-name`、`--target-root`、`--resources`、`--description`、`--overwrite`
- 核心输出结构：
  - `create-skill-from-template`：JSON（`skill_dir`、`resources_created`、`write_results`）
  - 资源查询类命令：JSON（`asset/path/content`）
- 失败返回：参数缺失或模板/路径异常时返回非零退出码

## 同步维护要求
- 工具变更后必须同步更新本文件与 `Cli_Toolbox_DEVELOPMENT.md`。
- 多模块 Toolbox 变更时，还必须同步：
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - `references/tooling/development/20_CATEGORY_INDEX.md`
  - 对应模块文档（`references/tooling/development/modules/*.md`）
- 若模板契约变更影响运行态规则分发方式，还必须同步：
  - `references/skill_template_contract_v1.md`
  - `references/skill_architecture_playbook.md`
  - `assets/skill_template/SKILL_TEMPLATE.md`
