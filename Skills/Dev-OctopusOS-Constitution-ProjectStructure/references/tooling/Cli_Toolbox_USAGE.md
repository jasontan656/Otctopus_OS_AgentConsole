---
doc_id: "dev_octopusos_constitution_projectstructure.tooling.toolbox_usage"
doc_type: "topic_atom"
topic: "Tooling usage status for the OctopusOS project-structure constitution skill"
anchors:
  - target: "Cli_Toolbox_DEVELOPMENT.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Usage and development notes should stay aligned."
---

# Cli_Toolbox Usage

## 当前状态
- 本技能当前没有专属 `Cli_Toolbox.py`。
- 当前读取入口固定为门面与 `references/` 下的治理文档。

## 未来约束
- 若后续为项目结构 lint、目录规划校验或模块注册检查新增专属 CLI：
  - 工具入口统一落在 `scripts/Cli_Toolbox.py`
  - 使用文档必须在本文件维护
  - 工具语义必须以 `references/governance/` 与 `references/project_structure/` 为治理锚点
