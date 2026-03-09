---
name: "${skill_name}"
description: ${description}
---

# ${skill_name}

## 1. 目标
- [描述此技能在运行态要解决的业务问题，不要写“创建/生成本技能”这类建模流程目标。]
- [写明该技能的阶段主轴，示例：`mother_doc -> implementation -> evidence`。]
- [复杂技能默认采用“抽象层 + 各阶段域”写法。]

## 2. 可用工具
- 抽象层：
  - 统一工具入口：`scripts/Cli_Toolbox.py`
  - 命名规则：工具统一命名为 `Cli_Toolbox.<tool_name>`。
  - [列出共享抽象命令，例如运行合同、顶层规则、统一入口命令。]
- 阶段域：
  - `[stage_1]`：
    - [列出该阶段专属命令、用途、入口。]
  - `[stage_2]`：
    - [列出该阶段专属命令、用途、入口。]
  - `[stage_3]`：
    - [列出该阶段专属命令、用途、入口。]
- 抽象功能可共享；阶段域命令必须独立，不得串用。
- 若声明工具，维护以下文档：
  - 使用文档：`references/tooling/Cli_Toolbox_USAGE.md`
  - 开发文档：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
- 若技能存在运行态规则、约束、指引：
  - 必须提供 CLI 输出入口。
  - 必须提供 machine-readable `json/yaml` 合同。
  - markdown 只可作为审计版，不能作为模型运行时规则源。

## 3. 工作流约束
- 抽象层：
  - [写明阶段顺序、top-level always-load 规则、统一入口。]
- 阶段域：
  - `[stage_1]`：
    - [写明进入条件、退出条件、产出。]
  - `[stage_2]`：
    - [写明进入条件、必须显式承接的前序阶段产物、退出条件、产出。]
  - `[stage_3]`：
    - [写明进入条件、必须显式承接的前序阶段产物、退出条件、产出。]

## 4. 规则约束
- 抽象层：
  - [写明 top-level resident docs。]
  - [显式声明：模型禁止直接阅读 markdown 获取运行指引；必须通过 CLI 读取 machine-readable 合同。]
  - [显式声明：规则必须同时存在 markdown 与 json/yaml 两份，更新时必须同步。]
  - [若某些合同依赖真实项目状态，显式标注为 dynamic runtime contract。]
- 阶段域：
  - `[stage_1]`：
    - [写明该阶段专属规则与专属禁止项。]
  - `[stage_2]`：
    - [写明该阶段专属规则与专属禁止项。]
  - `[stage_3]`：
    - [写明该阶段专属规则与专属禁止项。]

## 5. 方法论约束
- 抽象层：
  - [推荐声明：先 contract，再 directive，再动作。]
  - [推荐声明：抽象层与阶段域分开写，禁止混写。]
- 阶段域：
  - `[stage_1]`：
    - [写明该阶段专属方法论。]
  - `[stage_2]`：
    - [写明该阶段专属方法论。]
  - `[stage_3]`：
    - [写明该阶段专属方法论。]

## 6. 内联导航索引
- 抽象层：
  - [规则层] -> [rules/]
  - [运行合同 JSON] -> [references/runtime/SKILL_RUNTIME_CONTRACT.json]
  - [运行合同审计版] -> [references/runtime/SKILL_RUNTIME_CONTRACT.md]
  - [阶段索引] -> [references/stages/00_STAGE_INDEX.md]
  - [Cli_Toolbox 使用文档] -> [references/tooling/Cli_Toolbox_USAGE.md]
  - [Cli_Toolbox 开发文档] -> [references/tooling/Cli_Toolbox_DEVELOPMENT.md]
- 阶段域：
  - `[stage_1]` -> [相对路径]
  - `[stage_2]` -> [相对路径]
  - `[stage_3]` -> [相对路径]

## 7. 架构契约
```text
<skill-name>/
├── SKILL.md
├── agents/openai.yaml
├── rules/
├── scripts/
├── references/
│   ├── runtime/
│   └── stages/
└── assets/
    └── templates/
        └── stages/
```
