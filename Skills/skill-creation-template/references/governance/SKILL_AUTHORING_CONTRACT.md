---
doc_id: "skill_creation_template.governance.authoring_contract"
doc_type: "topic_atom"
topic: "Authoring contract for governed skills generated or refactored by this template"
anchors:
  - target: "../runtime/SKILL_RUNTIME_CONTRACT.md"
    relation: "expands"
    direction: "upstream"
    reason: "The runtime contract declares this contract as a required governance source."
  - target: "SKILL_DOCSTRUCTURE_ENFORCEMENT.md"
    relation: "governed_by"
    direction: "upstream"
    reason: "Doc-structure governance is a mandatory part of this authoring contract."
  - target: "../routing/PROFILE_ROUTING.md"
    relation: "details"
    direction: "upstream"
    reason: "Profile routing decides which profile branch this contract should be combined with."
---

# Skill Authoring Contract

## 合同目标
- 用受治理模板创建或重构 skill，不接受“先生成一个胖门面，再靠后补丁慢慢拆”的做法。
- 这里约束的是可执行的 skill 结构，而不是一次性写作格式。
- `skill-doc-structure` 在本合同中是强制组成部分：创建新 skill 与治理既有 skill 时都必须显式应用。
- `SKILL.md` 的入口门面 contract 由本技能负责；`skill-doc-structure` 从入口节点往下治理文档树。

## 门面契约
- `SKILL.md` 必须是 `entry-only facade`。
- 门面只能保留：
  - 技能定位
  - 必读顺序
  - 分类入口
  - 适用域
  - 执行入口
  - 读取原则
  - 结构索引
- 门面必须把读者路由到 routing doc，而不是直接承载 authoring 正文。
- 模板或治理类 skill 原有的 `技能本体 / 规则说明` 双段式约定保留，但应优先放在 routing doc 之后的 topic atom 中；只有在不破坏极简门面的前提下才允许出现在 facade。
- 门面契约属于模板治理面，由本技能持续维护。

## 文档结构契约
- skill 内 markdown 结构必须满足：
  - 顶层先有由模板定义的 facade。
  - facade 后至少有一层 routing doc。
  - 深规则落到单 topic 原子文档。
  - 索引文档只做导航，不承担主规则正文。
- 进入 facade 之后的文档树组织与 metadata/anchors 由 `skill-doc-structure` 继续治理。
- 所有 markdown 文档都必须具备 `doc_structure` frontmatter 与至少一个 anchor。
- 读写路径、阶段路径、语言路径等独立轴线不得混在同一个 routing doc 里。

## Profile 契约
- `basic`
  - 适用于单主轴、低阶段复杂度 skill。
  - 生成结果至少要具备：facade、task routing、doc-structure policy、execution rules、tooling docs。
  - 若存在运行态规则，必须补齐 runtime contract。
- `staged_cli_first`
  - 适用于多阶段、多门禁、强窄域读取 skill。
  - 除 basic 的 facade/routing/governance 结构外，还必须补齐 runtime contract、stage index 与 stage contract 四件套。
  - 阶段合同必须分离 machine-readable contracts 与 markdown 导航文档。

## 工具与资产契约
- 工具入口统一使用 `scripts/Cli_Toolbox.py`。
- 工具变更时，必须同步更新：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - 受影响模块文档
- 模板资产变更时，必须同步更新：
  - `assets/skill_template/`
  - `scripts/create_skill_from_template.py`
  - `tests/test_create_skill_from_template_regression.py`

## 验收门禁
- `SKILL.md` 是极简 facade，且已把读者路由到下一层文档。
- routing docs 与 atomic docs 已形成清晰 tree，anchors 已补齐 graph。
- `basic` 与 `staged_cli_first` 的生成结果与各自 profile 输出面一致。
- 若 skill 有运行态规则，则 CLI JSON、machine-readable contract、markdown audit copy 三者闭环完整。
