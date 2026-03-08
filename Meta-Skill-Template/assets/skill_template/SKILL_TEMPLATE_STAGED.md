---
name: "${skill_name}"
description: ${description}
---

# ${skill_name}

## 1. 目标
- [描述此技能在运行态要解决的业务问题，不要写“创建/生成本技能”这类建模流程目标。]
- [写明该技能的阶段主轴，示例：`scan -> collect -> push`。]

## 2. 可用工具
- 统一工具入口：`scripts/Cli_Toolbox.py`
- 命名规则：工具统一命名为 `Cli_Toolbox.<tool_name>`。
- [列出阶段级合同命令，例如：`stage-checklist`、`stage-doc-contract`、`stage-command-contract`、`stage-graph-contract`。]
- 若声明工具，维护以下文档：
  - 使用文档：`references/tooling/Cli_Toolbox_USAGE.md`
  - 开发文档：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
- 若技能存在运行态规则、约束、指引：
  - 必须提供 CLI 输出入口。
  - 必须提供 machine-readable `json/yaml` 合同。
  - markdown 只可作为审计版，不能作为模型运行时规则源。

## 3. 工作流约束
- [写明阶段顺序、阶段进入条件、阶段退出条件。]
- [写明进入任一阶段前必须读取的 CLI 合同。]
- [写明阶段切换后需要丢弃的上一阶段 focus。]

## 4. 规则约束
- [写明 top-level resident docs。]
- [显式声明：模型禁止直接阅读 markdown 获取运行指引；必须通过 CLI 读取 machine-readable 合同。]
- [显式声明：规则必须同时存在 markdown 与 json/yaml 两份，更新时必须同步。]
- [若某些合同依赖真实项目状态，显式标注为 dynamic runtime contract。]

## 5. 方法论约束
- [推荐声明：先 contract，再 directive，再动作。]
- [推荐声明：阶段文档按需读取，禁止跨阶段展开。]
- [推荐声明：目录层级用于收拢文档适用域。]

## 6. 内联导航索引
- [规则层] -> [rules/]
- [运行合同 JSON] -> [references/runtime/SKILL_RUNTIME_CONTRACT.json]
- [运行合同审计版] -> [references/runtime/SKILL_RUNTIME_CONTRACT.md]
- [阶段索引] -> [references/stages/00_STAGE_INDEX.md]
- [阶段模板簇] -> [assets/templates/stages/]
- [Cli_Toolbox 使用文档] -> [references/tooling/Cli_Toolbox_USAGE.md]
- [Cli_Toolbox 开发文档] -> [references/tooling/Cli_Toolbox_DEVELOPMENT.md]

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
