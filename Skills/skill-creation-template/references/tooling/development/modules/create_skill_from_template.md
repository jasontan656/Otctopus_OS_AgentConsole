# create_skill_from_template 模块开发文档

## 模块标识
- `module_id`: `create_skill_from_template`
- `tool_alias`: `Cli_Toolbox.create_skill_from_template`
- `entrypoint`: `scripts/create_skill_from_template.py`

## 职责
- 基于受治理模板创建技能骨架。
- 默认生成标准 7 章门面 `SKILL.md`。
- 根据 `--profile` 选择 basic 或 staged output surface。
- staged profile 额外补齐：
  - runtime contract skeleton
  - stage index
  - stage system README
  - stage checklist 模板
  - stage doc/command/graph contract 模板
- 默认创建 `tests/` 目录，为后续治理与回归预留位置。

## 输入输出契约
- 输入：`--skill-name`、`--target-root`、`--resources`、`--description`、`--profile`、`--overwrite`
- 默认资源：`scripts,references,assets,tests`
- 输出：JSON（`skill_dir`、`profile`、`resources_created`、`write_results`）
- 失败模式：参数缺失、模板文件缺失、路径不可写

## 依赖与边界
- 依赖：
  - `assets/skill_template/*.md|*.yaml`
  - `assets/skill_template/runtime/*`
  - `assets/skill_template/stages/*`
- 边界：
  - 不负责 Git 留痕
  - 不负责 mirror 同步
  - 不负责补齐业务语义，只负责生成治理骨架

## 回归检查
```bash
python3 scripts/create_skill_from_template.py --help
python3 scripts/create_skill_from_template.py --skill-name basic-sandbox --target-root /tmp/meta-skill-template --profile basic --overwrite
python3 scripts/create_skill_from_template.py --skill-name staged-sandbox --target-root /tmp/meta-skill-template --profile staged_cli_first --overwrite
python3 -m unittest discover -s tests
```

## 文档同步
- 使用文档已同步：是
- 模块目录已同步：是
- staged 模板 kit 已同步：是
