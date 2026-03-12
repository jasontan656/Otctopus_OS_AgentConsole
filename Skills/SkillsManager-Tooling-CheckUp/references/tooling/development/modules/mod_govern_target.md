# govern_target 模块开发文档

## 模块标识
- `module_id`: `govern_target`
- `tool_alias`: `Cli_Toolbox.govern_target`
- `entrypoint`: `scripts/Cli_Toolbox.py`

## 职责
- 针对目标 skill root 输出运行时形态治理审计结果。
- 检查 dual-file runtime assets、SKILL.md facade、`agents/openai.yaml` 是否已经切到 CLI-first。

## 输入输出契约
- 输入：
  - `--target-skill-root <path>`
  - `--json`
- 输出：
  - 目标 skill 的形态治理合同
  - 审计结果
  - 推荐修正动作
- 失败模式：
  - `target_skill_root_not_found`
  - `target_skill_root_missing_skill_md`

## 回归检查
```bash
cd <repo-root> && python3 -m unittest tests.test_cli_toolbox
```
