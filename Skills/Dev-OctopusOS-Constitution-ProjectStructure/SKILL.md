---
name: Dev-OctopusOS-Constitution-ProjectStructure
description: 治理整个章鱼OS项目的整体架构、项目结构与模块插拔定位，不负责具体域内实现细节。
metadata:
  doc_structure:
    doc_id: dev_octopusos_constitution_projectstructure.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Dev-OctopusOS-Constitution-ProjectStructure skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
---

# Dev-OctopusOS-Constitution-ProjectStructure

## Runtime Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/Dev-OctopusOS-Constitution-ProjectStructure/scripts/Cli_Toolbox.py contract --json`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.


## 1. 技能定位
- 本文件只做门面入口，不承载深规则正文。
- 本技能负责治理整个章鱼OS项目的整体架构、项目结构、模块定位与热插拔边界。
- 本技能只处理项目级结构，不治理某个域内部的具体实现架构；例如前端在章鱼OS中的系统定位、依赖关系、插拔方式归本技能，但前端域内组件分层、页面结构与具体前端规范不归本技能。
- 本技能当前通过静态 `Cli_Toolbox.py` 暴露 runtime contract；有效结构规则仍以下沉文档为准。

## 2. 必读顺序
1. 先读取 `references/routing/TASK_ROUTING.md`。
2. 再读取 `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`。
3. 再读取 `references/governance/SKILL_EXECUTION_RULES.md`。
4. 若任务在问章鱼OS整体定位、中枢边界或对象归属，再读取：
   - `references/project_structure/OCTOPUS_OS_HUB_POSITIONING_MODEL.md`
   - `references/project_structure/DOMAIN_OBJECT_POSITIONING_BOUNDARY.md`
5. 若任务在问模块插拔、能力依赖、底座 bundle 或常驻能力边界，再读取：
   - `references/project_structure/CAPABILITY_MODULE_HOTPLUG_RULES.md`
   - `references/project_structure/FOUNDATION_CAPABILITY_BUNDLE_BOUNDARY.md`
   - `references/project_structure/PROJECT_TECHSTACK_BASELINE.md`
6. 若任务在问项目目录、容器拆分、部署对象与文件夹规划，再读取：
   - `references/project_structure/FOLDER_CONTAINER_PLANNING_RULES.md`
   - `references/project_structure/OCTOPUS_OS_TARGET_FOLDER_LAYOUT.md`

## 3. 分类入口
- 路由层：
  - `references/routing/TASK_ROUTING.md`
- 治理层：
  - `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`
  - `references/governance/SKILL_EXECUTION_RULES.md`
- 项目结构层：
  - `references/project_structure/OCTOPUS_OS_HUB_POSITIONING_MODEL.md`
  - `references/project_structure/DOMAIN_OBJECT_POSITIONING_BOUNDARY.md`
  - `references/project_structure/CAPABILITY_MODULE_HOTPLUG_RULES.md`
  - `references/project_structure/FOUNDATION_CAPABILITY_BUNDLE_BOUNDARY.md`
  - `references/project_structure/PROJECT_TECHSTACK_BASELINE.md`
  - `references/project_structure/FOLDER_CONTAINER_PLANNING_RULES.md`
  - `references/project_structure/OCTOPUS_OS_TARGET_FOLDER_LAYOUT.md`
- 工具层：
  - `scripts/Cli_Toolbox.py`
  - `references/runtime_contracts/*`
  - `references/tooling/*`

## 4. 适用域
- 适用于：章鱼OS整体架构设计、项目级对象定位、模块热插拔边界、底座能力常驻边界、项目目录/容器规划、未来 lint 门禁的结构性依据。
- 适用于：固定章鱼OS当前阶段的项目级技术选型，并声明这些技术在系统中的定位与归属。
- 适用于：判断一个域在章鱼OS中应被视为“完整对象”“底座能力模块”还是“入口/适配层对象”。
- 不适用于：具体前端实现规范、具体后端域模型设计、具体数据库 schema、具体页面组件架构、具体业务工作流细则。
- `Meta-Architect-MindModel` 负责更高层的 architect-first 决策镜头；本技能负责把章鱼OS项目结构本身落成稳定的治理合同。

## 5. 执行入口
- 先执行 `./.venv_backend_skills/bin/python Skills/Dev-OctopusOS-Constitution-ProjectStructure/scripts/Cli_Toolbox.py contract --json`。
- 再按 `SKILL.md -> references/routing/TASK_ROUTING.md -> 对应 project_structure 原子文档` 深读。
- 若未来新增 lint、目录规划检查或模块注册检查工具，必须同步更新 `references/runtime_contracts/` 与 `references/tooling/` 全套文档。

## 6. 读取原则
- 门面只负责路由，不重新长回规则正文。
- `SkillsManager-Doc-Structure` 是创建与治理本技能时必须应用的显式规则。
- 若某条规则只属于单一 topic，应下沉到原子文档；不要继续堆在门面里。
- 项目级结构规则优先于局部域偏好；先确定对象在章鱼OS中的系统位置，再进入域内实现。
- 逻辑解耦优先于物理拆分；本技能允许“逻辑上可插拔、物理上先 bundle 部署”的过渡形态。
- 物理路径一次只表达一层语义：对象身份、能力边界、运行态、阶段态不得堆叠进同一层目录名。
- 不预置 `Common/`、`Core/` 这类高抽象内部角色骨架；只有真实代表未来可独立演化或拆部署的能力目录，才允许在项目结构层预留。

## 7. 结构索引
```text
Dev-OctopusOS-Constitution-ProjectStructure/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── governance/
│   ├── project_structure/
│   ├── routing/
│   └── tooling/
├── scripts/
├── assets/
└── tests/
```
