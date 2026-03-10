---
name: "Meta-Skill-Template"
description: "将 3-Octupos-OS-Backend 已验证的技能骨架提炼为通用模板治理面板，用统一 Cli_Toolbox 创建或改造 basic 与 staged_cli_first 技能。"
---

# Meta-Skill-Template

## 1. 定位
- 本文件只做模板技能门面入口，不承载模板治理正文。
- 本技能的唯一主轴是：`skill_facade -> runtime_contract -> template_assets -> generated_skill`。
- 本技能负责把 `3-Octupos-OS-Backend` 已验证成功的技能架构提炼成可复用模板，只抽取运行结构，不复制后端业务术语、固定路径与领域语义。
- 支持两类 profile：
  - `basic`
  - `staged_cli_first`
- 模板生成物的目标不是“看起来像模板”，而是让后续技能从创建开始就具备稳定路由、窄域读取、CLI-first 合同和可治理结构。

## 2. 必读顺序
1. 进入本技能后，先读取：
   - `python3 scripts/Cli_Toolbox.py runtime-contract --json`
2. 创建或改造技能前，必须先判定目标 profile：
   - `basic`
   - `staged_cli_first`
3. 若要理解通用模板硬约束，读取：
   - `python3 scripts/Cli_Toolbox.py contract-reference --json`
   - `python3 scripts/Cli_Toolbox.py architecture-playbook --json`
4. 若目标是复杂 staged skill，额外读取：
   - `python3 scripts/Cli_Toolbox.py staged-skill-reference --json`
5. 真正创建或改造技能时，优先走：
   - `python3 scripts/Cli_Toolbox.py create-skill-from-template ...`
6. 若修改了模板脚本、contracts 或模板资产，必须同步更新相关 tooling 文档与回归验证，不得只改单点。

## 3. 分类入口
- 运行合同层：
  - `references/runtime/SKILL_RUNTIME_CONTRACT.json`
  - `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- 模板治理层：
  - `references/skill_template_contract_v1.md`
  - `references/skill_architecture_playbook.md`
- profile 提炼层：
  - `references/staged_cli_first_profile_reference.md`
- 模板资产层：
  - `assets/skill_template/SKILL_TEMPLATE.md`
  - `assets/skill_template/SKILL_TEMPLATE_STAGED.md`
  - `assets/skill_template/runtime/*`
  - `assets/skill_template/stages/*`
- 工具层：
  - `scripts/Cli_Toolbox.py`
  - `scripts/create_skill_from_template.py`
- 校验层：
  - `tests/test_create_skill_from_template_regression.py`

## 4. 适用域
- 适用于：创建新技能、将已有技能重构到统一门面结构、补齐 runtime contract、补齐 staged 阶段合同与模板簇、把技能治理从口头规则收敛为模板规则。
- 不适用于：直接承担具体业务技能本身的 domain 实现、替代 `skill-creator` 的格式校验角色、替代 `Meta-Skill-Mirror` 的 mirror 同步角色。
- `basic` 用于单主轴、低阶段复杂度技能。
- `staged_cli_first` 用于多阶段、多合同、强读取边界和强门禁的复杂技能。

## 5. 执行入口
- 统一入口：
  - `python3 scripts/Cli_Toolbox.py create-skill-from-template --skill-name <name> --target-root <path> --profile <basic|staged_cli_first> --overwrite`
- 运行合同：
  - `python3 scripts/Cli_Toolbox.py runtime-contract --json`
- 模板契约：
  - `python3 scripts/Cli_Toolbox.py contract-reference --json`
- 架构手册：
  - `python3 scripts/Cli_Toolbox.py architecture-playbook --json`
- `basic` 门面模板：
  - `python3 scripts/Cli_Toolbox.py skill-template --json`
- `staged_cli_first` 门面模板：
  - `python3 scripts/Cli_Toolbox.py staged-skill-template --json`
- staged runtime 模板：
  - `python3 scripts/Cli_Toolbox.py runtime-contract-template --json`
- staged profile 提炼参考：
  - `python3 scripts/Cli_Toolbox.py staged-skill-reference --json`

## 6. 读取原则
- `SKILL.md` 只负责门面路由；运行时细节一律以下沉 contracts、references 与模板资产为准。
- 模板生成时优先抽象“成功技能的稳定结构”，不要把源技能的业务词、项目路径、验收语义原样搬运。
- `basic` 与 `staged_cli_first` 的差异应体现在生成骨架与合同深度上，不要靠事后补丁把 basic 叠成 staged。
- 若技能存在运行态规则，模型不得直接读 markdown 当规则源；必须通过 CLI 读取 machine-readable 合同。
- 若目标是 staged skill，必须显式建模：
  - top-level resident docs
  - stage checklist
  - stage doc contract
  - stage command contract
  - stage graph contract
  - stage switch discard protocol
- 模板、脚本、tooling 文档、测试必须一起治理；禁止只改模板正文而不更新生成器与验证。

## 7. 结构索引
```text
Meta-Skill-Template/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── Cli_Toolbox.py
│   └── create_skill_from_template.py
├── assets/
│   └── skill_template/
│       ├── SKILL_TEMPLATE.md
│       ├── SKILL_TEMPLATE_STAGED.md
│       ├── openai_template.yaml
│       ├── runtime/
│       └── stages/
├── references/
│   ├── runtime/
│   ├── tooling/
│   ├── skill_template_contract_v1.md
│   ├── skill_architecture_playbook.md
│   └── staged_cli_first_profile_reference.md
└── tests/
    └── test_create_skill_from_template_regression.py
```
