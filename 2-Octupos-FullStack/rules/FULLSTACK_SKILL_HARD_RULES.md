# FULLSTACK Skill Hard Rules

适用技能：
- `2-Octupos-FullStack`

## Rule Set

1. 本技能是未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护底层文档、开发代码并回填 evidence。
2. 本技能采用文档直达实现模型；新文档架构直接匹配代码结构，因此不保留独立的中间 `plan` / `construction_plan` 环节。
3. 技能内部规则不得覆盖 workspace/runtime 的外层硬合同。
4. `SKILL.md` 门面只描述如何使用本技能，以及文档撰写、代码落盘、evidence 回填规范。
5. 实际对 UI 的设计、event 设计、后端支持与其他实现细节，必须落入本技能产出的开发运维文档中，不得堆回 `SKILL.md` 门面。
6. 技能写文档是一回事；按照文档开发出来的内容是另一回事，二者边界必须清楚。
