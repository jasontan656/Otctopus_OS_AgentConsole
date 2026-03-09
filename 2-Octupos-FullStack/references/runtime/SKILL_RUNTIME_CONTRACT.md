# 2-Octupos-FullStack Runtime Contract

> Audit copy for `references/runtime/SKILL_RUNTIME_CONTRACT.json`.

- `skill_name`: `2-Octupos-FullStack`
- `role_definition`: 未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护 `Mother_Doc`、开发代码并回填 evidence。
- `workspace_root`: `/home/jasontan656/AI_Projects/Octopus_OS`
- `document_root`: `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`
- `rule_layers`:
  - `skill_native_rules`: 本技能如何工作、如何写 `Mother_Doc`、如何落盘、如何回填 evidence
  - `authored_rules`: 本技能产出的开发运维文档中，对 UI、event、后端、数据库、部署、运维与运行时对象的规则
- `execution_model`: 文档直达实现；文档骨架直接匹配代码与部署边界，因此不保留独立的中间 `plan` / `construction_plan` 环节；容器集合允许在 `Mother_Doc` 入口按项目描述动态横向扩充。

## Governance Rules
- 文档、代码与 evidence 都是项目本体的一部分。
- 技能内部规则不得覆盖 workspace/runtime 的外层硬合同。
- 唯一工作目录固定为 `/home/jasontan656/AI_Projects/Octopus_OS`。
- 唯一文档承载目录固定为 `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`。
- 容器目录参考内容可以静态存在，但真实容器集合是项目驱动的动态集合。
- `SKILL.md` 门面只描述技能自有规则。
- UI 设计、event 设计、后端支持、数据库、部署、运维与运行时细节，必须落入被撰写规则中。
- 必须显式区分技能自有规则与被撰写规则。
- 技能写文档与按照文档开发出来的内容是两回事。
- `Mother_Doc/` 的目录架构既是被撰写文档架构，也是未来 Admin Panel 的可视化架构。
- `Mother_Doc/` 文件在仓库内作为源文档存在，但运行时消费者必须通过 `Mother_Doc_Service` API 获取内容。
- `Mother_Doc/` 当前入口形态应以同名容器目录为主，不保留 `01-07` 这类编号治理目录作为主要结构。
- 在 `Mother_Doc` 的撰写/维护入口，AI 必须依据用户描述判断是否横向新增容器目录。
- 若需求引入可独立部署、可独立演进或可独立承载职责的模块，AI 必须同步新增工作目录容器与 `Mother_Doc` 同名目录。
- 第一阶段命名规范采用“一个目录 = 一个可独立部署或独立演进的单元”。
