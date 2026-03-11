---
name: "skill-creation-template"
description: "提供受治理技能模板与统一 Cli_Toolbox，用于创建或改造 basic 与 staged_cli_first 技能。"
---

# Skill-Creation-Template

## 1. 技能定位
- 本体描述：
  - 本技能是“创建技能 / 编辑技能”时使用的模板治理面板；当前 `SKILL.md` 的章节编排本身就是模板基线。
  - 本技能结构即为模板结构，模板内每章说明即为对应章节的写法规则，不额外依赖一套平行说明书。
  - `Cli_Toolbox.py` 既提供模板读取入口，也提供创建骨架时的 CLI tool 示例代码与生成器入口。
  - 本技能内置两类模板：
    - `basic`：纯方法论、单主轴、轻运行面的技能模板。
    - `staged_cli_first`：复合 stage 入口、CLI-first、强合同面的技能模板。
  - 模板目标不是“生成一堆占位文件”，而是让技能从第一版起就具备稳定门面、窄域读取与可治理结构。
- 注释描述：
  - 对模板类技能，`1. 技能定位` 采用两段写法：
    - `本体描述`：写技能本身是什么、承载什么内容、自己的工具是什么。
    - `注释描述`：像旁白一样写这一章怎么写，要求说清哪些信息必须交代、哪些表达应压缩。
  - `注释描述` 只解释本章使用规则，不重复本体内容；门面必须极简，不得在定位段落长篇铺陈。
  - 若确有必要，可在 `注释描述` 中给出进一步展开入口，但只能做轻量提示，不能把扩展说明正文塞回门面。

## 2. 适用域
- 本体描述：
  - 适用于：创建新技能、重排已有技能门面、把散乱技能收敛成统一模板结构、补齐 runtime contract 与 stage contract、把口头写法收敛成可复用模板。
  - 适用于：编辑技能时，需要判断应使用 `basic` 还是 `staged_cli_first`，并据此重写门面、文档和工具入口。
  - 不适用于：直接代替目标技能编写其业务语义、替代 `skill-creator` 的格式校验职责、替代 `skill-mirror-to-codex` 的 mirror 同步职责。
- 注释描述：
  - `适用域` 必须明确声明技能各部分的适用域，并按语义边界细分；不得把多个不自洽的域混写成一个总域。
  - 每个域都必须自洽，拥有自己的工具、入口、输入输出或阶段边界；不得与其他域混用。
  - 多阶段技能必须明确区分阶段域，不得把不同阶段职责写成一个模糊域。
  - 坏例子：`撰写文档和生成计划混在一起`、`校验和修复混在一起`。
  - 正确示例：`读取文档输出报告`、`扫描提问并回写`、`读取计划并落盘`。
  - 这里不是要求绝对单一动作，而是要求一个域内的动作语义连贯、服务同一目标，不得跳跃式混杂。

## 3. 可用工具简述&入口
- 本体描述：
  - `Cli_Toolbox.runtime_contract`
    - 入口：`python3 scripts/Cli_Toolbox.py runtime-contract --json`
    - 用途：输出本技能当前模板合同与 7 章基线。
  - `Cli_Toolbox.create_skill_from_template`
    - 入口：`python3 scripts/Cli_Toolbox.py create-skill-from-template --skill-name <name> --target-root <path> --profile <basic|staged_cli_first> --overwrite`
    - 用途：按选定 profile 创建或改造技能骨架。
  - `Cli_Toolbox.skill_template`
    - 入口：`python3 scripts/Cli_Toolbox.py skill-template --json`
    - 用途：输出 `basic` 模板正文。
  - `Cli_Toolbox.staged_skill_template`
    - 入口：`python3 scripts/Cli_Toolbox.py staged-skill-template --json`
    - 用途：输出 `staged_cli_first` 模板正文。
  - `Cli_Toolbox.contract_reference`
    - 入口：`python3 scripts/Cli_Toolbox.py contract-reference --json`
    - 用途：输出模板硬约束。
  - `Cli_Toolbox.architecture_playbook`
    - 入口：`python3 scripts/Cli_Toolbox.py architecture-playbook --json`
    - 用途：输出模板架构方法论。
  - `Cli_Toolbox.staged_skill_reference`
    - 入口：`python3 scripts/Cli_Toolbox.py staged-skill-reference --json`
    - 用途：输出复合 stage 模板的通用参考。
  - `Cli_Toolbox.runtime_contract_template`
    - 入口：`python3 scripts/Cli_Toolbox.py runtime-contract-template --json`
    - 用途：输出 staged runtime contract 模板资产。
- 注释描述：
  - `可用工具简述&入口` 只写工具、命令、入口与用途，不把文档说明和工作流步骤混进来。
  - 工具应按能力域或 profile 分组；同一组内的工具必须服务同一语义域，不得跨域混排。
  - 一个工具条目可以包含多个连贯动作，但这些动作必须围绕同一工具职责，不得把“扫描 / 生成 / 校验 / 修复”随意并列成一个条目。

## 4. 文档指引&入口
- 本体描述：
  - 运行合同：
    - `references/runtime/SKILL_RUNTIME_CONTRACT.json`
    - `references/runtime/SKILL_RUNTIME_CONTRACT.md`
  - 模板契约与方法论：
    - `references/skill_template_contract_v1.md`
    - `references/skill_architecture_playbook.md`
    - `references/staged_cli_first_profile_reference.md`
  - 模板资产：
    - `assets/skill_template/SKILL_TEMPLATE.md`
    - `assets/skill_template/SKILL_TEMPLATE_STAGED.md`
    - `assets/skill_template/runtime/*`
    - `assets/skill_template/stages/*`
  - 工具与生成器：
    - `scripts/Cli_Toolbox.py`
    - `scripts/create_skill_from_template.py`
  - 回归验证：
    - `tests/test_create_skill_from_template_regression.py`
- 注释描述：
  - `文档指引&入口` 必须按文档层级和职责分域，至少区分合同、方法论、资产、工具、验证。
  - 文档入口必须和工具入口分离；不要把“读什么”与“执行什么”写成一个混合列表。
  - 每个文档域都应只承载一种主要职责，避免出现“规则 + 工作流 + 回归”三类信息塞在同一个域里的混合描述。

## 5. 工作流指引
- 本体描述：
  1. 先读取 `python3 scripts/Cli_Toolbox.py runtime-contract --json`，确认当前模板合同。
  2. 判断本次目标是创建技能还是编辑技能，并先判定应落到 `basic` 还是 `staged_cli_first`。
  3. 若是 `basic`，读取 `skill-template`、`contract-reference`、`architecture-playbook` 后再写。
  4. 若是 `staged_cli_first`，额外读取 `staged-skill-template`、`staged-skill-reference`、`runtime-contract-template`。
  5. 真正创建或改造技能时，优先使用 `create-skill-from-template` 生成骨架，再回填真实语义。
  6. 若修改了模板章节、合同、脚本或资产，必须同步更新 tooling 文档与回归测试，不得只改单点。
- 注释描述：
  - `工作流指引` 只写顺序化动作，不写背景大段解释。
  - 每一步必须是当前域内可直接执行的连贯动作；不要在同一步里混入另一个域的目标。
  - 若存在分支工作流，应先按 `basic` / `staged_cli_first` 之类语义边界分流，再分别列步骤。
  - 允许一步中包含多个紧邻动作，但必须服务同一阶段目标，不能出现跳跃式思维导致语义混淆。

## 6. 顶层常驻通用规则
- 本体描述：
  - 当前技能的 7 章结构就是模板基线；未来模板调整应先改基线，再同步改模板资产与合同。
  - 模板内每章文字就是章节使用规则，不再额外制造一份重复门面说明。
  - `SKILL.md` 只保留门面职责；运行细节必须下沉到 `references/`、contracts、assets 与脚本。
  - 若技能存在运行态规则，模型不得直接把 markdown 当规则源；必须通过 CLI 读取 machine-readable contract。
  - `basic` 与 `staged_cli_first` 的差异必须体现在模板骨架与合同深度上，不能靠事后补丁把前者叠成后者。
  - 模板、脚本、tooling 文档、测试必须一起治理；禁止只改模板正文而不更新生成器与验证。
- 注释描述：
  - `顶层常驻通用规则` 只容纳跨章节、跨域都成立的稳定规则，不写局部流程细节。
  - 若某条规则只对单一阶段、单一工具或单一文档域生效，应下沉到对应章节，不得冒充顶层常驻规则。
  - 对模板/治理类技能，双段写法可用于全文，但 `注释描述` 始终只解释写法和边界，不承担运行正文。

## 7. 结构索引
- 本体描述：
```text
skill-creation-template/
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
- 注释描述：
  - `结构索引` 只展示稳定结构，不展开逐文件说明，不把目录树写成正文讲解。
  - 若某层目录的职责需要说明，应在前文对应章节解释，不在结构索引里补第二套叙述。
