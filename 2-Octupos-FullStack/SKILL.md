---
name: "2-Octupos-FullStack"
description: "未来项目 admin panel 内置的运营AI“章鱼”，负责维护 Mother_Doc、代码落盘与 evidence 回填。"
---

# 2-Octupos-FullStack

## 1. 目标
- 本技能用于 `Octopus_OS` 的全栈文档驱动开发与落盘维护。
- 运行对象是未来项目 admin panel 内置的运营AI“章鱼”。
- 保持 `SKILL.md` 轻量，仅承载入口、边界与导航。

## 2. 可用工具
- 统一工具入口：`scripts/Cli_Toolbox.py`
- 当前主要命令：
  - `materialize-container-layout`
- 详细工具说明下沉到 `references/tooling/`。

## 3. 工作流约束
- 进入技能后，先读取 `references/runtime/SKILL_RUNTIME_CONTRACT.*` 明确运行边界。
- 涉及 `Mother_Doc` 结构、动态扩容、容器命名时，读取：
  - `references/mother_doc/MOTHER_DOC_ENTRY_RULES.md`
  - `references/mother_doc/PHASE1_CONTAINER_NAMING_REFERENCE.md`
- 需要落容器目录与 `common/` 抽象层骨架时，使用 `materialize-container-layout`。
- 具体容器规则、架构、技术栈、命名、合同与运维内容，下沉到 `Mother_Doc` 对应容器目录。

## 4. 规则约束
- 本页禁止继续承载堆积式治理细节。
- 详细运行规则统一下沉到：
  - `rules/`
  - `references/runtime/`
  - `references/mother_doc/`
  - `references/tooling/`
- 若 `Mother_Doc` 入口规则、容器模板、tooling 行为发生变化，必须同步更新本页入口、runtime contract、tooling 文档与安装目录。

## 5. 方法论约束
- 文档直接驱动实现。
- 顶层容器目录与 `Mother_Doc` 同名目录保持 1:1 映射。
- 容器集合允许按项目描述动态横向扩充。
- 每个容器文档目录先固定 `README.md + common/`，再继续展开具体内容。

## 6. 内联导航索引
- [Cli_Toolbox 工具入口] -> [scripts/Cli_Toolbox.py]
- [容器骨架模块] -> [scripts/container_scaffold.py]
- [顶层规则] -> [rules/FULLSTACK_SKILL_HARD_RULES.md]
- [运行合同 JSON] -> [references/runtime/SKILL_RUNTIME_CONTRACT.json]
- [运行合同审计版] -> [references/runtime/SKILL_RUNTIME_CONTRACT.md]
- [Mother_Doc 入口规则] -> [references/mother_doc/MOTHER_DOC_ENTRY_RULES.md]
- [第一阶段命名参考] -> [references/mother_doc/PHASE1_CONTAINER_NAMING_REFERENCE.md]
- [Cli_Toolbox 使用文档] -> [references/tooling/Cli_Toolbox_USAGE.md]
- [Cli_Toolbox 开发文档] -> [references/tooling/Cli_Toolbox_DEVELOPMENT.md]
- [工作目录] -> [/home/jasontan656/AI_Projects/Octopus_OS]
- [文档目录] -> [/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc]
- [Mother_Doc 容器索引] -> [/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/Mother_Doc/00_INDEX.md]

## 7. 架构契约
```text
2-Octupos-FullStack/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── Cli_Toolbox.py
│   └── container_scaffold.py
├── rules/
│   └── FULLSTACK_SKILL_HARD_RULES.md
└── references/
    ├── mother_doc/
    │   ├── MOTHER_DOC_ENTRY_RULES.md
    │   └── PHASE1_CONTAINER_NAMING_REFERENCE.md
    ├── runtime/
    │   ├── SKILL_RUNTIME_CONTRACT.json
    │   └── SKILL_RUNTIME_CONTRACT.md
    └── tooling/
        ├── Cli_Toolbox_USAGE.md
        ├── Cli_Toolbox_DEVELOPMENT.md
        └── development/
            ├── 00_ARCHITECTURE_OVERVIEW.md
            ├── 10_MODULE_CATALOG.yaml
            ├── 20_CATEGORY_INDEX.md
            ├── 90_CHANGELOG.md
            └── modules/
                └── materialize_container_layout.md
```
