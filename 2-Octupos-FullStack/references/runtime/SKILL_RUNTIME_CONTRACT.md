# 2-Octupos-FullStack Runtime Contract

> Audit copy for `references/runtime/SKILL_RUNTIME_CONTRACT.json`.

- `skill_name`: `2-Octupos-FullStack`
- `role_definition`: 未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护 `Mother_Doc`、开发代码并回填 evidence。
- `workspace_root`: `/home/jasontan656/AI_Projects/Octopus_OS`
- `document_root`: `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`
- `always_load_rules`:
  - `rules/FULLSTACK_SKILL_HARD_RULES.md`
  - `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- `stages`:
  - `mother_doc`
  - `implementation`
  - `evidence`
- `rule_layers`:
  - `skill_native_rules`: 本技能如何工作、如何维护 `Mother_Doc`、如何落盘、如何回填 evidence
  - `authored_rules`: 各容器文档中定义的架构、技术栈、命名、合同、运维与运行时规则
- `execution_model`: 文档直接驱动实现；容器集合允许在 `Mother_Doc` 入口按项目描述动态横向扩充；`mother_doc` 写回只维护当前状态。

## Governance Rules
- 文档、代码与 evidence 都是项目本体的一部分。
- 技能内部规则不得覆盖 workspace/runtime 的外层硬合同。
- 任意阶段开始前，必须先加载顶层规则，不得丢弃。
- 阶段顺序固定为 `mother_doc -> implementation -> evidence`。
- `implementation` 阶段必须显式引用 `mother_doc` 阶段产物。
- `evidence` 阶段必须显式引用 `mother_doc` 与 `implementation` 阶段产物。
- 整个技能必须采用“抽象层 + 三阶段显式拆分”的写法，禁止混写作用域。
- 抽象功能可共享，特定域命令禁止共享、禁止串用。
- 唯一工作目录固定为 `/home/jasontan656/AI_Projects/Octopus_OS`。
- 唯一文档承载目录固定为 `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`。
- `Mother_Doc/README.md` 是镜像根说明；`Mother_Doc/agents.md` 是镜像根递归索引入口。
- `Mother_Doc` 特例目录固定为 `Octopus_OS/Mother_Doc/Mother_Doc/`，其自身也必须具备 `README.md` 与 `agents.md`。
- `Mother_Doc` 每一层目录都必须具备 `README.md` 与 `agents.md`。
- `agents.md` 固定承载当前层索引；`README.md` 固定承载当前层用途说明。
- `mother_doc` 阶段每次撰写前，必须先结合上下文使用 `Meta-prompt-write` 强化用户意图。
- 强化完成后，必须先从根层 `README.md + agents.md` 进入，再逐层读取当前层 `README.md + agents.md`，递归覆盖完整影响面。
- 容器目录参考内容可以静态存在，但真实容器集合是项目驱动的动态集合。
- 若需求引入可独立部署、可独立演进或可独立承载职责的模块，AI 必须同步新增工作目录容器与 `Mother_Doc` 同名目录。
- 每个容器文档目录必须先固定为 `README.md + common/`。
- `common/` 当前固定 `architecture/`、`stack/`、`naming/`、`contracts/`、`operations/` 五个一级域。
- 每个最小知识点单独一个 `*.md`，新增容器后必须同步生成对应容器族模板骨架并刷新递归索引。
- `mother_doc` 回填采用覆盖写入，只维护当前状态；项目内部不做文档版本分流。
