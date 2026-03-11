# Cli_Toolbox 开发文档架构总览

## 目标
- 让模板技能的脚本、contracts、assets、tooling 文档与测试围绕同一套 façade 治理。
- 保证 `create_skill_from_template.py` 生成的不是“占位文档集合”，而是可直接继续收敛的 skill control plane。
- 保证 `basic` 与 `staged_cli_first` 共享统一门面哲学，但输出不同深度的合同面。

## 分层结构
0. 技能门面层：`SKILL.md`
1. 运行合同层：`references/runtime/`
2. 模板治理层：
   - `references/skill_template_contract_v1.md`
   - `references/skill_architecture_playbook.md`
   - `references/staged_cli_first_profile_reference.md`
3. 工具入口层：
   - `scripts/Cli_Toolbox.py`
   - `scripts/create_skill_from_template.py`
4. 模板资产层：
   - `assets/skill_template/`
5. 校验层：
   - `tests/`

## 当前关键设计
- 默认门面采用标准 7 段 façade。
- `staged_cli_first` 默认生成 runtime contract 和 stage template kit。
- stage template kit 包含：
  - `CHECKLIST.json`
  - `DOC_CONTRACT.json`
  - `COMMAND_CONTRACT.json`
  - `GRAPH_CONTRACT.json`
- 默认资源目录包含 `tests/`，为模板回归预留位置。

## 维护原则
- 先改 contracts 与模板资产，再改生成器，再补工具文档与测试。
- 若改动的是 staged profile，必须把合同面和模板 kit 一起改完，不能只改 `SKILL_TEMPLATE_STAGED.md`。
- 若脚本与文档描述不一致，以脚本行为为准并立即回写文档；不要保留“双真相”。
