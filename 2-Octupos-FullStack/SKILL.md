---
name: "2-Octupos-FullStack"
description: "未来项目 admin panel 内置的运营AI“章鱼”，负责文档写作、代码落盘与 evidence 回填。"
---

# 2-Octupos-FullStack

## 1. 目标
- 本技能是未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护底层文档、开发代码并回填 evidence。
- 本技能采用文档直达实现模型；新文档架构直接匹配代码结构，因此不保留独立的中间 `plan` / `construction_plan` 环节。

## 2. 可用工具
- 当前技能从头设计，工具与可视化界面合同后续再定。

## 3. 工作流约束
- 先写文档，再按文档直接落代码，并持续回填 evidence。

## 4. 规则约束
- 不保留旧的 staged 施工叙事。
- 技能内部规则不得覆盖 workspace/runtime 的外层硬合同。

## 5. 方法论约束
- 文档结构必须直接匹配代码结构。
- 文档、代码与 evidence 都是项目本体的一部分。

## 6. 内联导航索引
- [顶层规则] -> [rules/FULLSTACK_SKILL_HARD_RULES.md]
- [运行合同 JSON] -> [references/runtime/SKILL_RUNTIME_CONTRACT.json]
- [运行合同审计版] -> [references/runtime/SKILL_RUNTIME_CONTRACT.md]

## 7. 架构契约
```text
2-Octupos-FullStack/
├── SKILL.md
├── agents/openai.yaml
├── rules/
├── references/
└── assets/
```
