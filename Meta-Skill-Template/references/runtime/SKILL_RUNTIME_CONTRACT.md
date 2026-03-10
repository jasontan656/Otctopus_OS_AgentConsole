# Meta-Skill-Template Runtime Contract

## Contract Header
- `contract_name`: `meta_skill_template_references_runtime_skill_runtime_contract`
- `contract_version`: `3.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `contract_name`
  - `contract_version`
  - `validation_mode`
- `optional_fields`:
  - `notes`

> Audit copy for `references/runtime/SKILL_RUNTIME_CONTRACT.json`.

## Authoring Model
- `SKILL.md` role: `entry_only`
- Proven source skill: `3-Octupos-OS-Backend`
- Default facade sections:
  - `定位`
  - `必读顺序`
  - `分类入口`
  - `适用域`
  - `执行入口`
  - `读取原则`
  - `结构索引`
- 抽取原则：只提炼稳定运行结构与治理形态，不复制后端业务术语、固定项目路径与验收语义。

## Routing Protocol
- 第一入口命令：`python3 scripts/Cli_Toolbox.py runtime-contract --json`
- 读取顺序：
  - `runtime-contract`
  - `contract-reference`
  - `architecture-playbook`
  - `staged-skill-reference`（仅 `staged_cli_first`）
  - `create-skill-from-template`
- profile 选择规则：
  - 默认优先 `basic`
  - 只有当目标技能需要阶段合同、resident docs 和 stage-switch discard 治理时才进入 `staged_cli_first`
- markdown 角色：人类审计与窄域导航
- 运行时规则源：`Cli_Toolbox` JSON 输出与生成后的 machine-readable contracts

## Profile Support
- `basic`
  - 目标形态：单主轴、entry-only 技能门面。
  - 必需输出：`SKILL.md`、`agents/openai.yaml`、tooling 文档。
  - 运行态合同可选；若存在运行态规则，则必须补齐 `references/runtime/`。
- `staged_cli_first`
  - 目标形态：来自 backend 成功骨架的 staged facade。
  - 必需输出：
    - runtime contract
    - `references/stages/00_STAGE_INDEX.md`
    - stage checklist
    - stage doc contract
    - stage command contract
    - stage graph contract
    - stage template kit

## Tool Contracts
- `Cli_Toolbox.create_skill_from_template`
  - 创建或改造受治理技能骨架。
- `Cli_Toolbox.skill_template`
  - 输出 `basic` 门面模板。
- `Cli_Toolbox.staged_skill_template`
  - 输出 backend-derived staged 门面模板。
- `Cli_Toolbox.openai_template`
  - 输出 `agents/openai.yaml` 模板。
- `Cli_Toolbox.contract_reference`
  - 输出模板作者合同。
- `Cli_Toolbox.staged_skill_reference`
  - 输出 `3-Octupos-OS-Backend` 的通用化提炼结果。
- `Cli_Toolbox.runtime_contract_template`
  - 输出 staged runtime contract 模板资产。
- `Cli_Toolbox.architecture_playbook`
  - 输出模板架构手册。
- `Cli_Toolbox.runtime_contract`
  - 输出本技能运行合同。

## Governance Rules
- `SKILL.md` 必须保持门面化，不得重新长回治理正文。
- 默认模板门面采用 backend 验证过的 7 段 façade，而不是旧的“抽象层/业务层标题重复堆叠”。
- 若技能存在运行态规则，必须以 CLI-first + machine-readable contract 作为真实规则源。
- `staged_cli_first` 技能必须显式建模：
  - stage order
  - top-level resident docs
  - stage checklist
  - stage doc contract
  - stage command contract
  - stage graph contract
  - stage-switch discard policy
- 模板簇必须分离人类叙事 markdown 与 machine-readable contracts。
- 模板升级时，同步更新脚本、文档、资产与回归检查，不得只改某一侧。

## Validation Closure
- 运行 toolbox 自检命令。
- 至少生成一份 `basic` sandbox。
- 至少生成一份 `staged_cli_first` sandbox。
- 验证 staged 输出包含 stage checklist 和合同四件套。
- 保持 tooling 文档与回归测试同步。
