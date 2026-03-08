# staged_cli_first 复杂技能 profile 提炼参考

来源基准：`3-Octupos-OS-Backend`

## 目标
- 抽取“复杂但高服从度技能”的可复用制作规范。
- 这里提炼的是技能制作规则，不是源技能的业务领域内容。

## 核心原则
- 运行时指引优先由 CLI 输出，不直接让模型读 markdown 当规则源。
- markdown 必须结构化分层，作为人类审计与窄域导航。
- 目录深度本身就是模型约束工具；层级越深，适用域越窄。
- `SKILL.md` 只做门面入口，不承载规则正文。

## 推荐结构
- 门面层：`SKILL.md`
- 硬规则层：`rules/`
- 工作流合同层：`references/`
- 运行合同层：`references/runtime/`
- 阶段层：`references/stages/`
- 模板簇层：`assets/templates/`
- 工具层：`scripts/Cli_Toolbox.py`
- 接口层：`agents/openai.yaml`

## resident docs 规则
- 跨阶段只保留极少、固定的 resident docs。
- resident docs 负责维持全局边界，不负责承载某阶段细节。
- 阶段切换后，上一阶段 checklist、focus、模板填写上下文必须显式丢弃。

## 阶段合同规则
- 当前阶段至少应有以下合同中的适用子集：
  - `stage-checklist`
  - `stage-doc-contract`
  - `stage-command-contract`
  - `stage-graph-contract`
- 每类合同都应有明确消费方与适用域，避免“一个大文档全都写”。

## 模板簇规则
- 模板不能只有一份总模板。
- 人类阅读 markdown anchors 与 machine files 应分离维护。
- 复杂技能至少要有：
  - 门面模板
  - runtime contract 模板
  - stage system 模板
  - per-stage contract 模板

## static / dynamic contract 规则
- static contract：
  - 与具体项目状态无关。
  - 适合作为 authoring template 或固定规则输出。
- dynamic contract：
  - 依赖真实项目路径、当前产物、图谱或运行态。
  - 只能由 CLI 在真实上下文中计算输出。
  - 需要显式声明前置条件与失败口径。

## 模板治理建议
- `Meta-Skill-Template` 应支持至少两个 profile：
  - `basic`
  - `staged_cli_first`
- 复杂技能生成器应默认产出：
  - entry-only `SKILL.md`
  - runtime contract skeleton
  - stage system reference
  - stage template kit
