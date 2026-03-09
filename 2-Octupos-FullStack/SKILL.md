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
- 保持 `SKILL.md` 轻量，仅承载入口、边界与导航。

## 2. 可用工具
- 统一工具入口：`scripts/Cli_Toolbox.py`
- `mother_doc` 阶段：
  - `mother-doc-stage`
    - 作用：打印 `mother_doc` 阶段的作用域、必须加载规则、输入输出。
    - 用法：`python3 scripts/Cli_Toolbox.py mother-doc-stage --json`
  - `materialize-container-layout`
    - 作用：按已判定容器名落工作目录与 `Mother_Doc` 同名目录，并补齐 `common/` 抽象层骨架。
    - 用法：`python3 scripts/Cli_Toolbox.py materialize-container-layout --container <Name> --json`
- `implementation` 阶段：
  - `implementation-stage`
    - 作用：打印 `implementation` 阶段的作用域、必须承接的前序产物、以及当前阶段产出。
    - 用法：`python3 scripts/Cli_Toolbox.py implementation-stage --json`
- `evidence` 阶段：
  - `evidence-stage`
    - 作用：打印 `evidence` 阶段的作用域、必须承接的前序产物、以及回填输出。
    - 用法：`python3 scripts/Cli_Toolbox.py evidence-stage --json`
- 各阶段共用同一 CLI 入口，但命令必须显式区分作用域。
- 详细工具说明下沉到 `references/tooling/`。

## 3. 工作流约束
- 进入技能后，任何阶段都必须先加载顶层规则，不得丢弃：
  - `rules/FULLSTACK_SKILL_HARD_RULES.md`
  - `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- 阶段顺序固定为：
  1. `mother_doc`
  2. `implementation`
  3. `evidence`
- 后续阶段必须显式引用前序阶段内容：
  - `implementation` 必须显式引用 `mother_doc` 产物
  - `evidence` 必须显式引用 `mother_doc` 与 `implementation` 产物
- 需要查看阶段作用域与输入输出时，读取：
  - `references/stages/00_STAGE_INDEX.md`
  - `references/stages/MOTHER_DOC_STAGE.md`
  - `references/stages/IMPLEMENTATION_STAGE.md`
  - `references/stages/EVIDENCE_STAGE.md`
- 涉及 `Mother_Doc` 结构、动态扩容、容器命名时，读取：
  - `references/mother_doc/MOTHER_DOC_ENTRY_RULES.md`
  - `references/mother_doc/PHASE1_CONTAINER_NAMING_REFERENCE.md`

## 4. 规则约束
- 本页禁止继续承载堆积式治理细节。
- 顶层规则属于 always-load 规则；进入任一阶段都必须先加载。
- 详细运行规则统一下沉到：
  - `rules/`
  - `references/runtime/`
  - `references/stages/`
  - `references/mother_doc/`
  - `references/tooling/`
- 若阶段边界、carry-forward 规则或 tooling 行为发生变化，必须同步更新本页入口、runtime contract、stages 文档、tooling 文档与安装目录。

## 5. 方法论约束
- 文档直接驱动实现。
- 顶层容器目录与 `Mother_Doc` 同名目录保持 1:1 映射。
- 容器集合允许按项目描述动态横向扩充。
- 每个容器文档目录先固定 `README.md + common/`，再继续展开具体内容。
- `implementation` 与 `evidence` 不得脱离前序阶段单独执行。

## 6. 内联导航索引
- [Cli_Toolbox 工具入口] -> [scripts/Cli_Toolbox.py]
- [容器骨架模块] -> [scripts/container_scaffold.py]
- [阶段运行模块] -> [scripts/stage_runtime.py]
- [顶层规则] -> [rules/FULLSTACK_SKILL_HARD_RULES.md]
- [运行合同 JSON] -> [references/runtime/SKILL_RUNTIME_CONTRACT.json]
- [运行合同审计版] -> [references/runtime/SKILL_RUNTIME_CONTRACT.md]
- [阶段索引] -> [references/stages/00_STAGE_INDEX.md]
- [mother_doc 阶段] -> [references/stages/MOTHER_DOC_STAGE.md]
- [implementation 阶段] -> [references/stages/IMPLEMENTATION_STAGE.md]
- [evidence 阶段] -> [references/stages/EVIDENCE_STAGE.md]
- [Mother_Doc 入口规则] -> [references/mother_doc/MOTHER_DOC_ENTRY_RULES.md]
- [第一阶段命名参考] -> [references/mother_doc/PHASE1_CONTAINER_NAMING_REFERENCE.md]
- [Cli_Toolbox 使用文档] -> [references/tooling/Cli_Toolbox_USAGE.md]
- [Cli_Toolbox 开发文档] -> [references/tooling/Cli_Toolbox_DEVELOPMENT.md]
- [工作目录] -> [/home/jasontan656/AI_Projects/Octopus_OS]
- [文档目录] -> [/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc]

## 7. 架构契约
```text
2-Octupos-FullStack/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── Cli_Toolbox.py
│   ├── container_scaffold.py
│   └── stage_runtime.py
├── rules/
│   └── FULLSTACK_SKILL_HARD_RULES.md
└── references/
    ├── mother_doc/
    │   ├── MOTHER_DOC_ENTRY_RULES.md
    │   └── PHASE1_CONTAINER_NAMING_REFERENCE.md
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
                ├── implementation_stage.md
                └── evidence_stage.md
```
