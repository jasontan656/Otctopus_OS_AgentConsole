---
name: "2-Octupos-FullStack"
description: "未来项目 admin panel 内置的运营AI“章鱼”，负责维护 Mother_Doc、代码落盘与 evidence 回填。"
---

# 2-Octupos-FullStack

## 1. 目标
- 本技能是未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护 `Mother_Doc`、开发代码并回填 evidence。
- 本技能采用文档直达实现模型；文档骨架直接匹配代码与部署边界，因此不保留独立的中间 `plan` / `construction_plan` 环节。
- 本技能唯一工作目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS`。
- 本技能唯一文档承载目录固定为：`/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`。

## 2. 门面边界
- `SKILL.md` 门面只描述本技能如何工作，也就是本技能的自有规则：如何使用本技能、如何撰写 `Mother_Doc`、如何落代码、如何回填 evidence。
- 实际对 UI 的设计、event 设计、后端支持、数据库、部署、运维与运行时细节，不属于本技能自有规则；它们属于本技能产出的被撰写规则，必须落入 `Mother_Doc/`。
- `Mother_Doc/` 的目录架构既是被撰写文档架构，也是未来 Admin Panel 的可视化架构。
- `Mother_Doc/` 在仓库内以文件存在，但运行时消费者必须通过 `Mother_Doc_Service` API 获取内容，不以直接文件访问作为消费模型。

## 3. 工作流约束
- 先用本技能产出和维护 `Mother_Doc`，再按文档直接落代码，并持续回填 evidence。
- 技能写文档是一回事；按照文档开发出来的 UI、event、后端、数据库、部署与运维内容是另一回事。
- 所有落盘动作都以 `Octopus_OS` 为唯一工作目录，并以 `Mother_Doc/` 为唯一文档根。
- 本技能自有规则只约束“如何写文档与如何落盘”；被撰写规则才约束“文档里定义出的系统实现与运行边界”。

## 4. 规则约束
- 不保留旧的 staged 施工叙事。
- 技能内部规则不得覆盖 workspace/runtime 的外层硬合同。
- `SKILL.md` 门面不得承载具体 UI 方案、event 设计、后端实现、数据库方案或运维实现细节。
- 必须显式区分：
  - `技能自有规则`
  - `被撰写规则`
- `Mother_Doc_Service` 属于被撰写规则，不属于技能门面设计。

## 5. 方法论约束
- 文档结构必须直接匹配代码结构与部署边界。
- 文档、代码与 evidence 都是项目本体的一部分。
- 技能负责产出文档与落盘规范；实现产物本身的设计与维护要回收进 `Mother_Doc` 中的开发运维文档。
- 先区分规则层级，再写内容：先明确哪些是技能自有规则，再明确哪些是被撰写规则。
- `Mother_Doc` 文件树应尽量与未来 Admin Panel 可视化节点树保持同构。

## 6. 内联导航索引
- [顶层规则] -> [rules/FULLSTACK_SKILL_HARD_RULES.md]
- [运行合同 JSON] -> [references/runtime/SKILL_RUNTIME_CONTRACT.json]
- [运行合同审计版] -> [references/runtime/SKILL_RUNTIME_CONTRACT.md]
- [唯一工作目录] -> [/home/jasontan656/AI_Projects/Octopus_OS]
- [唯一文档目录] -> [/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc]
- [Mother_Doc 索引] -> [/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/00_INDEX.md]

## 7. 架构契约
```text
2-Octupos-FullStack/
├── SKILL.md
├── agents/openai.yaml
├── rules/
├── references/
└── assets/
```

## 8. 规则落点
- 写进技能：
  - 本技能如何被使用
  - `Mother_Doc` 如何被撰写和维护
  - 代码落盘和 evidence 回填规范
  - 技能自有规则与被撰写规则的分层边界
- 写进 `Mother_Doc`：
  - Admin Panel UI
  - event
  - backend
  - database
  - deployment
  - operations
  - `Mother_Doc_Service`
  - runtime contracts
