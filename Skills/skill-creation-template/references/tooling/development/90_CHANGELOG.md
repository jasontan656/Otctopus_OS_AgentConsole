# Cli_Toolbox 开发文档变更记录

- 2026-02-25
  - 将开发文档从单文件升级为“入口 + 分类 + 模块”结构。
- 2026-02-26
  - 澄清生成技能的 `1.目标` 只能写运行态目标，不能写“创建技能本身”。
- 2026-03-09
  - 引入 `staged_cli_first` profile，并为复杂技能补齐 runtime contract 与 stage template kit。
- 2026-03-10
  - 将模板门面统一升级为 7 段 façade：
    - `定位`
    - `必读顺序`
    - `分类入口`
    - `适用域`
    - `执行入口`
    - `读取原则`
    - `结构索引`
  - staged 模板 kit 新增 `CHECKLIST.json`，并把 resident docs、阶段合同四件套和 discard policy 升为模板硬约束。
  - `create_skill_from_template.py` 默认资源新增 `tests/`。
  - 引入生成回归测试，确保 profile 输出面不漂移。
