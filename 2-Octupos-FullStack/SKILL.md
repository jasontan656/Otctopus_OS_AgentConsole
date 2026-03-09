---
name: "2-Octupos-FullStack"
description: "未来项目 admin panel 内置的运营AI“章鱼”，负责 mother_doc、implementation 与 evidence 三阶段。"
---

# 2-Octupos-FullStack

## 1. 目标
- 本技能用于 `Octopus_OS` 的全栈文档驱动开发与落盘维护。
- 运行对象是未来项目 admin panel 内置的运营AI“章鱼”。
- 本技能显式承载三个阶段：
  - `mother_doc`
  - `implementation`
  - `evidence`
- 整个技能始终采用：`抽象总则 + 三阶段显式拆分`。

## 2. 可用工具
- 统一工具入口：`scripts/Cli_Toolbox.py`
- `mother_doc`：
  - `prompt-strengthening entry`
    - 作用：先用 `Meta-prompt-write` 结合完整上下文强化当前用户意图。
    - 用法：`python3 /home/jasontan656/.codex/skills/Meta-prompt-write/scripts/filter_active_invoke_output.py --mode active_invoke --input-text "<RAW_PROMPT_OUTPUT>"`
  - `mother-doc-stage`
    - 作用：打印 `mother_doc` 阶段的作用域、强制加载项、递归导航入口与回填规则。
    - 用法：`python3 scripts/Cli_Toolbox.py mother-doc-stage --json`
  - `materialize-container-layout`
    - 作用：按已判定容器名创建工作目录与 `Mother_Doc` 同名目录，并补齐容器抽象层骨架。
    - 用法：`python3 scripts/Cli_Toolbox.py materialize-container-layout --container <Name> --json`
  - `sync-mother-doc-navigation`
    - 作用：为 `Mother_Doc` 每一层目录刷新 `agents.md` 递归索引，并补齐缺失的 `README.md`。
    - 用法：`python3 scripts/Cli_Toolbox.py sync-mother-doc-navigation --json`
- `implementation`：
  - `implementation-stage`
    - 作用：打印 `implementation` 阶段的作用域、前序依赖与当前产出。
    - 用法：`python3 scripts/Cli_Toolbox.py implementation-stage --json`
- `evidence`：
  - `evidence-stage`
    - 作用：打印 `evidence` 阶段的作用域、前序依赖与回填输出。
    - 用法：`python3 scripts/Cli_Toolbox.py evidence-stage --json`
- 共用同一 CLI 入口，但各阶段命令必须显式分域，不得串用。

## 3. 工作流约束
- 抽象总则：
  - 任意阶段开始前，必须先加载顶层规则，不得丢弃：
    - `rules/FULLSTACK_SKILL_HARD_RULES.md`
    - `references/runtime/SKILL_RUNTIME_CONTRACT.md`
  - 阶段顺序固定为：`mother_doc -> implementation -> evidence`
  - 后续阶段缺失前序阶段显式输入时，必须停止并回到前序阶段补齐。
- `mother_doc`：
  - 先读取：
    - `references/stages/MOTHER_DOC_STAGE.md`
    - `references/mother_doc/MOTHER_DOC_ENTRY_RULES.md`
    - `references/mother_doc/AGENTS_MD_RULES.md`
    - `references/mother_doc/README_MD_RULES.md`
    - `references/mother_doc/MOTHER_DOC_WRITEBACK_RULES.md`
    - `references/mother_doc/PHASE1_CONTAINER_NAMING_REFERENCE.md`
  - 先结合上下文使用 `Meta-prompt-write` 强化用户意图。
  - 再从 `Octopus_OS/Mother_Doc/README.md` 与 `Octopus_OS/Mother_Doc/agents.md` 进入作用域选择。
  - 每进入下一层目录，都必须先读该层 `README.md`，再读该层 `agents.md`，再选择下一层路径，直至覆盖完整影响面。
  - 写回时只保留当前状态，覆盖更新，不规划项目内文档版本。
- `implementation`：
  - 先读取：
    - `references/stages/IMPLEMENTATION_STAGE.md`
    - `references/stages/MOTHER_DOC_STAGE.md`
  - 本阶段必须显式引用 `mother_doc` 产物后再执行代码与运行时落盘。
- `evidence`：
  - 先读取：
    - `references/stages/EVIDENCE_STAGE.md`
    - `references/stages/MOTHER_DOC_STAGE.md`
    - `references/stages/IMPLEMENTATION_STAGE.md`
  - 本阶段必须显式引用 `mother_doc` 与 `implementation` 产物后再回填 evidence。

## 4. 规则约束
- 抽象总则：
  - 顶层规则属于 always-load 规则；进入任一阶段都必须先加载。
  - 整个技能禁止混写作用域；规则必须按抽象层与阶段层分开承载。
  - 详细规则统一下沉到 `rules/`、`references/runtime/`、`references/stages/`、`references/mother_doc/`、`references/tooling/`。
- `mother_doc`：
  - `Mother_Doc` 每一层目录必须同时具备 `README.md` 与 `agents.md`。
  - `agents.md` 是当前层固定索引入口；禁止继续使用 `index.md`、`00_INDEX.md` 或其他平行索引文件。
  - `README.md` 只说明当前层用途；`agents.md` 只维护对等层说明与下层索引。
  - 需要新增容器时，必须同步新增工作目录容器、`Mother_Doc` 同名目录、抽象层骨架、递归索引文件。
- `implementation`：
  - 不得脱离 `mother_doc` 产物单独实施。
  - 不得把实现阶段规则回写成顶层门面文本。
- `evidence`：
  - 不得跳过 `implementation` 产物直接伪造 evidence。
  - 不得把证据回填规则与前两阶段混写。

## 5. 方法论约束
- 抽象总则：
  - 文档直接驱动实现。
  - 顶层容器目录与 `Mother_Doc` 同名目录保持 1:1 映射。
  - 抽象功能可共享，特定域命令禁止共享。
- `mother_doc`：
  - 先定容器与作用域，再写抽象层与内容。
  - `common/` 只承载稳定抽象层；业务细节再进入更下层域。
  - 每个最小知识点单独落一个 `*.md`。
  - 回填采用覆盖写入，只维护当前状态；项目内部不做文档版本分流。
- `implementation`：
  - 只消费 `mother_doc` 已明确的当前状态产物。
  - 不把未定义的文档意图自行脑补成实现边界。
- `evidence`：
  - 只消费前两阶段的显式产物。
  - 证据必须能回指到对应文档节点与实现节点。

## 6. 内联导航索引
- 抽象总则：
  - [顶层规则](rules/FULLSTACK_SKILL_HARD_RULES.md)
  - [运行合同 JSON](references/runtime/SKILL_RUNTIME_CONTRACT.json)
  - [运行合同审计版](references/runtime/SKILL_RUNTIME_CONTRACT.md)
  - [阶段索引](references/stages/00_STAGE_INDEX.md)
  - [Cli_Toolbox 工具入口](scripts/Cli_Toolbox.py)
  - [容器骨架模块](scripts/container_scaffold.py)
  - [阶段运行模块](scripts/stage_runtime.py)
  - [Mother_Doc 导航模块](scripts/mother_doc_navigation.py)
- `mother_doc`：
  - [mother_doc 阶段](references/stages/MOTHER_DOC_STAGE.md)
  - [Mother_Doc 入口规则](references/mother_doc/MOTHER_DOC_ENTRY_RULES.md)
  - [agents.md 规则](references/mother_doc/AGENTS_MD_RULES.md)
  - [README.md 规则](references/mother_doc/README_MD_RULES.md)
  - [Mother_Doc 回填规则](references/mother_doc/MOTHER_DOC_WRITEBACK_RULES.md)
  - [第一阶段命名参考](references/mother_doc/PHASE1_CONTAINER_NAMING_REFERENCE.md)
- `implementation`：
  - [implementation 阶段](references/stages/IMPLEMENTATION_STAGE.md)
- `evidence`：
  - [evidence 阶段](references/stages/EVIDENCE_STAGE.md)
- 运行位置：
  - [工作目录](/home/jasontan656/AI_Projects/Octopus_OS)
  - [文档目录](/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc)
  - [Cli_Toolbox 使用文档](references/tooling/Cli_Toolbox_USAGE.md)
  - [Cli_Toolbox 开发文档](references/tooling/Cli_Toolbox_DEVELOPMENT.md)

## 7. 架构契约
```text
2-Octupos-FullStack/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── Cli_Toolbox.py
│   ├── container_scaffold.py
│   ├── mother_doc_navigation.py
│   └── stage_runtime.py
├── rules/
│   └── FULLSTACK_SKILL_HARD_RULES.md
└── references/
    ├── mother_doc/
    │   ├── AGENTS_MD_RULES.md
    │   ├── MOTHER_DOC_ENTRY_RULES.md
    │   ├── MOTHER_DOC_WRITEBACK_RULES.md
    │   ├── PHASE1_CONTAINER_NAMING_REFERENCE.md
    │   └── README_MD_RULES.md
    ├── runtime/
    │   ├── SKILL_RUNTIME_CONTRACT.json
    │   └── SKILL_RUNTIME_CONTRACT.md
    ├── stages/
    │   ├── 00_STAGE_INDEX.md
    │   ├── MOTHER_DOC_STAGE.md
    │   ├── IMPLEMENTATION_STAGE.md
    │   └── EVIDENCE_STAGE.md
    └── tooling/
        ├── Cli_Toolbox_USAGE.md
        ├── Cli_Toolbox_DEVELOPMENT.md
        └── development/
            ├── 00_ARCHITECTURE_OVERVIEW.md
            ├── 10_MODULE_CATALOG.yaml
            ├── 20_CATEGORY_INDEX.md
            ├── 90_CHANGELOG.md
            └── modules/
                ├── materialize_container_layout.md
                ├── mother_doc_stage.md
                ├── sync_mother_doc_navigation.md
                ├── implementation_stage.md
                └── evidence_stage.md
```
