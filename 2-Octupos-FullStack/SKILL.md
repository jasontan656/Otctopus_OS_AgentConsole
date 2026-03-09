---
name: "2-Octupos-FullStack"
description: "未来项目 admin panel 内置的运营AI“章鱼”，负责文档写作、代码落盘与 evidence 回填。"
---

# 2-Octupos-FullStack

## 1. 目标
- 本技能是未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护底层文档、开发代码并回填 evidence。
- 本技能采用文档直达实现模型；新文档架构直接匹配代码结构，因此不保留独立的中间 `plan` / `construction_plan` 环节。
- 本技能唯一工作目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS`。
- 本技能唯一文档承载目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`。

## 2. 可用工具
- `SKILL.md` 门面只描述如何使用本技能，以及文档撰写、代码落盘、evidence 回填的运行规范。
- 实际对 UI 的设计、event 设计、后端支持与其他实现细节，不属于 `SKILL.md` 门面；它们必须落入本技能产出的开发运维文档中。

## 3. 工作流约束
- 先用本技能产出文档，再按文档直接落代码，并持续回填 evidence。
- 技能写文档是一回事；按照文档开发出来的 UI、event、后端与运行时内容是另一回事。
- 所有落盘动作都以 `Octopus_OS` 为唯一工作目录，并以 `Mother_Doc/` 为唯一文档根。

## 4. 规则约束
- 不保留旧的 staged 施工叙事。
- 技能内部规则不得覆盖 workspace/runtime 的外层硬合同。
- `SKILL.md` 门面不得承载具体 UI 方案、event 设计、后端实现或运维实现细节。

## 5. 方法论约束
- 文档结构必须直接匹配代码结构。
- 文档、代码与 evidence 都是项目本体的一部分。
- 技能负责产出文档与落盘规范；实现产物本身的设计与维护要回收进技能产出的开发运维文档。

## 6. 内联导航索引
- [顶层规则] -> [rules/FULLSTACK_SKILL_HARD_RULES.md]
- [运行合同 JSON] -> [references/runtime/SKILL_RUNTIME_CONTRACT.json]
- [运行合同审计版] -> [references/runtime/SKILL_RUNTIME_CONTRACT.md]
- [唯一工作目录] -> [/home/jasontan656/AI_Projects/Octopus_OS]
- [唯一文档目录] -> [/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc]

## 7. 架构契约
```text
2-Octupos-FullStack/
├── SKILL.md
├── agents/openai.yaml
├── rules/
├── references/
└── assets/
```
