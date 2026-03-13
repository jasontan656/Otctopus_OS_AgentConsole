---
doc_id: dev_octopusos_constitution_projectstructure.tooling.changelog
doc_type: index_doc
topic: Tooling changelog for the OctopusOS project-structure constitution skill
anchors:
- target: ../Cli_Toolbox_DEVELOPMENT.md
  relation: implements
  direction: upstream
  reason: The development entry routes into this changelog.
---

# Changelog

- `v1`: 初始化技能骨架，建立门面、routing 与 project_structure 原子文档。
- `v2`: 启用静态 `Cli_Toolbox.py contract --json` 入口，并把目录命名宪法更新为“对象名不重复、对象级目录不再使用 `*_Runtime` 后缀”。
- `v3`: 撤销 `Common/`、`Core/` 作为默认预置骨架，恢复“只预置真实可拆能力边界”的项目结构语义。
