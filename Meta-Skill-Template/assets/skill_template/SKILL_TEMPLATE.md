---
name: "${skill_name}"
description: ${description}
---

# ${skill_name}

## 1. 目标
- [描述此技能在运行态要解决的业务问题，不要写“创建/生成本技能”这类建模流程目标。]

## 2. 可用工具
- [列出本技能可直接使用的工具与入口。若当前技能不涉及工具，请填写：N/A。]
- 命名规则：工具统一命名为 `Cli_Toolbox.<tool_name>`。
- [列出本技能可直接使用的脚本、模板、参考文件。]
- 若声明工具，维护以下文档：
  - 使用文档：`references/tooling/Cli_Toolbox_USAGE.md`
  - 开发文档：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
- 若工具为多模块结构，维护以下开发索引：
  - `references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - `references/tooling/development/20_CATEGORY_INDEX.md`
  - `references/tooling/development/modules/MODULE_TEMPLATE.md`

## 3. 工作流约束
- [若当前技能涉及流程执行，请写明步骤、输入输出和完成判定；若不涉及，填写 N/A。]

## 4. 规则约束
- [若当前技能涉及规则边界，请写明命名、边界、门禁与禁止项；若不涉及，填写 N/A。]

## 5. 方法论约束
- [若当前技能涉及固定思维或推理方式，请写明采用条件与例外条件；若不涉及，填写 N/A。]

## 6. 内联导航索引
- [索引项 1] -> [相对路径]
- [索引项 2] -> [相对路径]
- [Cli_Toolbox 使用文档] -> [references/tooling/Cli_Toolbox_USAGE.md]
- [Cli_Toolbox 开发文档] -> [references/tooling/Cli_Toolbox_DEVELOPMENT.md]
- [Cli_Toolbox 开发架构总览] -> [references/tooling/development/00_ARCHITECTURE_OVERVIEW.md]
- [Cli_Toolbox 开发分类索引] -> [references/tooling/development/20_CATEGORY_INDEX.md]
- [Cli_Toolbox 模块目录] -> [references/tooling/development/10_MODULE_CATALOG.yaml]

## 7. 架构契约
```text
<skill-name>/
├── SKILL.md
├── agents/openai.yaml
├── scripts/
├── references/
└── assets/
```
