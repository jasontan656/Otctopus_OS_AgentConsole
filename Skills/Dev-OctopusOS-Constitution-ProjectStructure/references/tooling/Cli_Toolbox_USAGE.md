---
doc_id: dev_octopusos_constitution_projectstructure.tooling.toolbox_usage
doc_type: topic_atom
topic: Tooling usage status for the OctopusOS project-structure constitution skill
anchors:
- target: Cli_Toolbox_DEVELOPMENT.md
  relation: pairs_with
  direction: lateral
  reason: Usage and development notes should stay aligned.
---

# Cli_Toolbox Usage

## 当前状态
- 本技能当前提供静态 `scripts/Cli_Toolbox.py`。
- 当前唯一命令是 `contract`，用途是输出 runtime contract JSON，供模型在深读治理文档前先获得统一入口和命名宪法。
- 当前读取顺序固定为：
  - `./.venv_backend_skills/bin/python Skills/Dev-OctopusOS-Constitution-ProjectStructure/scripts/Cli_Toolbox.py contract --json`
  - `SKILL.md`
  - `references/routing/TASK_ROUTING.md`
  - 对应 `references/project_structure/*`
- 当前 contract 还负责声明一条硬边界：项目结构层不默认预置 `Common/`、`Core/`，只预置真实能力边界目录。

## 未来约束
- 若后续为项目结构 lint、目录规划校验或模块注册检查新增专属 CLI：
  - 工具入口统一落在 `scripts/Cli_Toolbox.py`
  - 使用文档必须在本文件维护
  - 工具语义必须以 `references/governance/` 与 `references/project_structure/` 为治理锚点
