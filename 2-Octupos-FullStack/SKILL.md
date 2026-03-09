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
- 本技能的长期主轴是：
  - `mother_doc` 负责产出和维护当前状态文档结构
  - `implementation` 负责像独立人类开发者一样按产品上线级标准推进开发、测试、bring-up 与交付
  - `evidence` 负责以 `OS_graph` 统一文档图与代码图，并把真实 witness 回填回结构

## 2. 可用工具
- 统一工具入口：`scripts/Cli_Toolbox.py`
- `mother_doc`：
  - `stage-checklist --stage mother_doc`
    - 作用：打印 `mother_doc` 阶段 checklist。
    - 用法：`python3 scripts/Cli_Toolbox.py stage-checklist --stage mother_doc --json`
  - `stage-doc-contract --stage mother_doc`
    - 作用：打印 `mother_doc` 阶段的读物边界。
    - 用法：`python3 scripts/Cli_Toolbox.py stage-doc-contract --stage mother_doc --json`
  - `stage-command-contract --stage mother_doc`
    - 作用：打印 `mother_doc` 阶段可用命令与入口动作。
    - 用法：`python3 scripts/Cli_Toolbox.py stage-command-contract --stage mother_doc --json`
  - `stage-graph-contract --stage mother_doc`
    - 作用：打印 `mother_doc` 阶段的 `OS_graph` 结构角色。
    - 用法：`python3 scripts/Cli_Toolbox.py stage-graph-contract --stage mother_doc --json`
  - `materialize-container-layout`
    - 作用：按已判定容器名创建工作目录与 `Mother_Doc` 同名目录，并补齐抽象层骨架。
    - 用法：`python3 scripts/Cli_Toolbox.py materialize-container-layout --container <Name> --json`
  - `sync-mother-doc-navigation`
    - 作用：仅在 `Mother_Doc` 树内刷新 `README.md`、`agents.md` 与同名 `<folder_name>.md`。
    - 用法：`python3 scripts/Cli_Toolbox.py sync-mother-doc-navigation --json`
- `implementation`：
  - `stage-checklist --stage implementation`
    - 作用：打印 `implementation` 阶段 checklist。
    - 用法：`python3 scripts/Cli_Toolbox.py stage-checklist --stage implementation --json`
  - `stage-doc-contract --stage implementation`
    - 作用：打印 `implementation` 阶段的读物边界。
    - 用法：`python3 scripts/Cli_Toolbox.py stage-doc-contract --stage implementation --json`
  - `stage-command-contract --stage implementation`
    - 作用：打印 `implementation` 阶段可用命令与独立开发者动作。
    - 用法：`python3 scripts/Cli_Toolbox.py stage-command-contract --stage implementation --json`
  - `stage-graph-contract --stage implementation`
    - 作用：打印 `implementation` 阶段的 doc-code drift 与 `OS_graph` 对齐规则。
    - 用法：`python3 scripts/Cli_Toolbox.py stage-graph-contract --stage implementation --json`
  - `implementation-stage`
    - 作用：打印 `implementation` 阶段总合同。
    - 用法：`python3 scripts/Cli_Toolbox.py implementation-stage --json`
- `evidence`：
  - `stage-checklist --stage evidence`
    - 作用：打印 `evidence` 阶段 checklist。
    - 用法：`python3 scripts/Cli_Toolbox.py stage-checklist --stage evidence --json`
  - `stage-doc-contract --stage evidence`
    - 作用：打印 `evidence` 阶段的读物边界。
    - 用法：`python3 scripts/Cli_Toolbox.py stage-doc-contract --stage evidence --json`
  - `stage-command-contract --stage evidence`
    - 作用：打印 `evidence` 阶段可用命令与回填动作。
    - 用法：`python3 scripts/Cli_Toolbox.py stage-command-contract --stage evidence --json`
  - `stage-graph-contract --stage evidence`
    - 作用：打印 `evidence` 阶段的 `OS_graph` 合同。
    - 用法：`python3 scripts/Cli_Toolbox.py stage-graph-contract --stage evidence --json`
  - `evidence-stage`
    - 作用：打印 `evidence` 阶段总合同。
    - 用法：`python3 scripts/Cli_Toolbox.py evidence-stage --json`

## 3. 工作流约束
- 抽象总则：
  - 顶层常驻文档只保留：
    - `rules/FULLSTACK_SKILL_HARD_RULES.md`
    - `references/runtime/SKILL_RUNTIME_CONTRACT.md`
    - `references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md`
    - `/home/jasontan656/AI_Projects/AGENTS.md`
  - 进入任一阶段前，固定先读：
    - `stage-checklist --stage <stage>`
    - `stage-doc-contract --stage <stage>`
    - `stage-command-contract --stage <stage>`
    - `stage-graph-contract --stage <stage>`
  - 阶段顺序固定为：`mother_doc -> implementation -> evidence`
  - 阶段切换时，必须显式丢弃上一阶段的阶段文档与临时 focus，只保留顶层常驻文档。
- `mother_doc`：
  - 先结合上下文使用 `Meta-prompt-write` 强化用户意图。
  - 再从 `Octopus_OS/Mother_Doc/README.md` 与 `Octopus_OS/Mother_Doc/agents.md` 进入作用域选择。
  - 每进入下一层目录，都必须先读该层 `README.md`、再读该层 `agents.md`、再读该层同名 `<folder_name>.md`，再选择下一层路径。
  - 写回时只保留当前状态，覆盖更新，不规划项目内文档版本。
- `implementation`：
  - 必须显式承接 `mother_doc` 当前状态产物。
  - 必须像独立人类开发者一样自行发现问题、安装依赖、修复环境、运行测试、启动服务、验证行为、直至达到产品上线级交付标准。
  - 必须主动发现 `Mother_Doc` 与实际代码库/运行时的不一致，并在代码与文档两侧做对齐更新。
- `evidence`：
  - 必须显式承接 `mother_doc + implementation` 当前状态产物。
  - `evidence` 的 graph 主体是 `OS_graph`，不再是单纯 `code graph`。
  - `OS_graph` 同时管理文档结构、代码结构、模块映射与 evidence 绑定关系。

## 4. 规则约束
- 抽象总则：
  - 整个技能禁止混写作用域；规则必须按抽象层与阶段层分开承载。
  - 规则正文统一下沉到：
    - `rules/`
    - `references/runtime/`
    - `references/tooling/`
    - `references/mother_doc/`
    - `references/implementation/`
    - `references/evidence/`
    - `references/stages/`
- `mother_doc`：
  - `agents.md` 只允许存在于 `Octopus_OS/Mother_Doc/**`。
  - 实际工作目录容器 `Octopus_OS/<Container_Name>/` 不得创建 `agents.md`。
  - `Mother_Doc` 每一层目录必须同时具备：
    - `README.md`
    - `agents.md`
    - `<folder_name>.md`
  - `README.md` 只说明当前层用途。
  - `agents.md` 只承担递归索引。
  - `<folder_name>.md` 只承担当前目录自身这个模块/父级域/黑盒容器/文档承载体的实体说明。
- `implementation`：
  - 不得脱离 `mother_doc` 当前状态产物单独实施。
  - 发现 doc-code drift 时，不得忽略；必须显式更新代码、文档或两者以恢复一致。
  - 不得因为本地可修问题而提前写成 `blocked`。
- `evidence`：
  - 不得伪造 witness。
  - 不得把 `OS_graph` 当成仅代码侧的解释层；它必须同时反映文档结构与代码结构。
  - 每个模块、每个 helper、每个父级目录都必须能在 `Mother_Doc` 层找到对应节点。

## 5. 方法论约束
- 抽象总则：
  - 文档即代码，代码组织最终应与 `Mother_Doc` 组织对齐。
  - 架构优先服务人类阅读与长期维护，但必须同时保留机械合同可读性。
  - 抽象功能可共享，特定域命令禁止共享。
- `mother_doc`：
  - 目录结构就是文档架构骨架。
  - `<folder_name>.md` 让每个目录自身也成为可读对象，不再只靠 `README.md` 或下层文件隐式表达。
- `implementation`：
  - 目录结构就是实现组织的主参照。
  - 每个模块 = 一个文档；每个模块 helper = 一个 helper 文档。
  - 模型默认要像独立开发者一样逐步推进：发现、实现、修复、测试、bring-up、验证、交付。
- `evidence`：
  - `OS_graph` 是文档图与代码图的统一视图。
  - evidence 必须能回指到同一层级结构中的模块文档、helper 文档、代码模块与运行 witness。

## 6. 内联导航索引
- 抽象总则：
  - [顶层规则](rules/FULLSTACK_SKILL_HARD_RULES.md)
  - [运行合同 JSON](references/runtime/SKILL_RUNTIME_CONTRACT.json)
  - [运行合同审计版](references/runtime/SKILL_RUNTIME_CONTRACT.md)
  - [workflow contract](references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md)
  - [Cli_Toolbox 工具入口](scripts/Cli_Toolbox.py)
  - [阶段合同支持模块](scripts/stage_contract_support.py)
  - [容器骨架模块](scripts/container_scaffold.py)
  - [Mother_Doc 导航模块](scripts/mother_doc_navigation.py)
- `mother_doc`：
  - [mother_doc 阶段](references/stages/MOTHER_DOC_STAGE.md)
  - [Mother_Doc 入口规则](references/mother_doc/MOTHER_DOC_ENTRY_RULES.md)
  - [agents.md 规则](references/mother_doc/AGENTS_MD_RULES.md)
  - [README.md 规则](references/mother_doc/README_MD_RULES.md)
  - [scope entity 规则](references/mother_doc/SCOPE_ENTITY_MD_RULES.md)
  - [Mother_Doc 回填规则](references/mother_doc/MOTHER_DOC_WRITEBACK_RULES.md)
  - [命名参考](references/mother_doc/PHASE1_CONTAINER_NAMING_REFERENCE.md)
- `implementation`：
  - [implementation 阶段](references/stages/IMPLEMENTATION_STAGE.md)
  - [独立开发者交付规则](references/implementation/IMPLEMENTATION_DELIVERY_RULES.md)
  - [doc-code 对齐规则](references/implementation/DOC_CODE_ALIGNMENT_RULES.md)
- `evidence`：
  - [evidence 阶段](references/stages/EVIDENCE_STAGE.md)
  - [OS_graph 规则](references/evidence/OS_GRAPH_RULES.md)

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
│   ├── stage_contract_registry.py
│   ├── stage_contract_support.py
│   └── stage_runtime.py
├── rules/
│   └── FULLSTACK_SKILL_HARD_RULES.md
└── references/
    ├── evidence/
    │   └── OS_GRAPH_RULES.md
    ├── implementation/
    │   ├── DOC_CODE_ALIGNMENT_RULES.md
    │   └── IMPLEMENTATION_DELIVERY_RULES.md
    ├── mother_doc/
    │   ├── AGENTS_MD_RULES.md
    │   ├── MOTHER_DOC_ENTRY_RULES.md
    │   ├── MOTHER_DOC_WRITEBACK_RULES.md
    │   ├── PHASE1_CONTAINER_NAMING_REFERENCE.md
    │   ├── README_MD_RULES.md
    │   └── SCOPE_ENTITY_MD_RULES.md
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
        ├── SKILL_TOOLING_WORKFLOW_CONTRACT.md
        └── development/
            ├── 00_ARCHITECTURE_OVERVIEW.md
            ├── 10_MODULE_CATALOG.yaml
            ├── 20_CATEGORY_INDEX.md
            ├── 90_CHANGELOG.md
            └── modules/
                ├── evidence_stage.md
                ├── implementation_stage.md
                ├── materialize_container_layout.md
                ├── mother_doc_stage.md
                ├── stage_checklist.md
                ├── stage_command_contract.md
                ├── stage_doc_contract.md
                ├── stage_graph_contract.md
                └── sync_mother_doc_navigation.md
```
