---
doc_id: dev_projectstructure_constitution.governance.execution_rules
doc_type: topic_atom
topic: Execution rules for OctopusOS project-structure governance
anchors:
- target: SKILL_DOCSTRUCTURE_POLICY.md
  relation: pairs_with
  direction: lateral
  reason: Execution rules and structure policy must evolve together.
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends project-structure decisions here first.
---

# Skill Execution Rules

## 本地目的
- 为章鱼OS项目级结构设计提供统一执行边界、判断顺序与排除规则，让 AI 在规划目录、容器和模块时先对齐系统位置，再谈局部实现。

## 当前边界
- 本技能治理的是整个章鱼OS的项目级结构，不替代各具体域自己的内部架构技能。
- 本技能不直接发明前端、后端、数据库或消息处理的域内实现细节；它只定义这些对象在章鱼OS中的系统位置、依赖边界和插拔方式。
- 本技能可以固定“项目级技术选型基线”，但不会替代对应技术栈技能对其域内编码规范的治理。

## 局部规则
- 先判断当前对象在章鱼OS里属于哪一类：后端平台能力对象、业务能力模块、客户端应用对象、集成适配对象、外部基础设施对象。
- `Development_Docs/` 与 `Deploy_Guide/` 是 repo 级治理容器，不是服务/模块对象；前者负责承载架构、技术基线与证据，后者负责承载部署脚本、门禁与 CI。
- 先定义逻辑边界，再决定物理部署形态；允许“逻辑上可插拔、物理上先 bundle 部署”的过渡设计。
- 章鱼OS默认采用 `开发文档容器 + 客户端应用容器 + 后端根容器 + 部署与交付容器` 的全栈项目级组织方式。
- 当前阶段一旦技术选型被写入 `references/project_structure/PROJECT_TECHSTACK_BASELINE.md`，后续目录规划、容器命名和 lint 判定都应引用该文档，而不是每轮重新拍脑袋决定。
- 跨对象路由、编排、注册与依赖判断应优先通过 `Development_Docs/` 的项目合同和对象级 manifest 表达；若当前阶段需要常驻运行控制面，应落在 `Foundation_Bundle` 或其他真实能力对象内，而不是恢复独立 `Octopus_Hub/` 抽象壳。
- `Foundation_Bundle` 作为后端根容器可以常驻存在，但其内部子能力、业务模块、集成适配和基础设施合同仍必须保留清晰的能力契约与未来可拆边界。
- 项目级叙事、阶段证据与全局索引不再通过顶层 `Mother_Doc/` 或 `System_Manifests/` 独立目录承载；应优先落在 `README.md`、`Development_Docs/` 或拥有该语义的对象自身 `Development_Docs/`。
- 目录命名必须遵守“单层单义”原则：
  - 对象根目录只表达对象身份。
  - 对象内部一级目录只表达真实能力边界或真实对象职责。
  - 运行态、部署态与流程阶段默认不得进入对象级物理目录名。
- 项目结构层禁止默认预置 `Common/`、`Core/` 这类高抽象角色目录；它们会把“未来可拆部署的能力边界”误导成“当前对象内部抽象分层”。
- 对象根内部禁止再出现 `<Object_Name>_Common`、`<Object_Name>_Core` 这类重复对象名的目录；若没有真实能力语义，就不应在项目结构层预置替代目录。
- `Foundation_Bundle` 下的公共能力目录应使用能力名本身，如 `Auth/`、`Payload/`、`Persistence/`，而不是带 `*_Runtime` 后缀的物理路径。
- 项目结构层默认只允许在服务/模块对象根下预置一个固定子目录：`Development_Docs/`。
- `Assets/`、`Channels/`、共享 `Development_Docs/` 根以及其他对象级固定子目录，不再属于章鱼OS当前阶段的权威预置结构。
- 任何域对象若要接入章鱼OS，应先被定义为“完整对象”，明确其 provides、requires、可拔除后的退化影响，再进入域内设计。
- 前端、后端、数据库等对象是否存在域内专属治理，不影响本技能对其项目级定位的裁决。
- 当任务涉及未来 lint、门禁或目录规划时，本技能的项目级结构规则应被视为上游治理来源。

## 例外与门禁
- 若任务已经进入某个域的内部实现，例如前端组件组织、后端服务内部模块划分、具体 schema 设计，应退出本技能主轴，转入对应域技能。
- 若用户显式要求恢复独立 `Octopus_Hub/`、`Mother_Doc/`、`System_Manifests/` 或其他旧顶层目录，应先明确这是“项目级架构改制”，而不是局部目录调整。
- 当前已有静态 contract CLI；任何未来工具化检查都必须先以本文和 `references/project_structure/` 的规则为治理锚点。
