# create_skill_from_template 模块开发文档

## 模块标识
- `module_id`: `create_skill_from_template`
- `tool_alias`: `Cli_Toolbox.create_skill_from_template`
- `entrypoint`: `scripts/create_skill_from_template.py`

## 职责
- 生成技能骨架：`SKILL.md`、`agents/openai.yaml`、资源目录。
- 生成 `Cli_Toolbox` 使用文档和开发文档基础结构。
- 保障输出为稳定 JSON，便于上游自动化消费。
- 默认文案避免把“创建技能流程”写入被创建技能的运行态目标描述。

## 输入输出契约
- 输入：`--skill-name`、`--target-root`、`--resources`、`--description`、`--overwrite`
- 输出：JSON（`skill_dir`、`resources_created`、`write_results`）
- 失败模式：参数缺失、模板文件缺失、路径不可写。

## 依赖与边界
- 依赖：`assets/skill_template/*.md|*.yaml` 模板文件。
- 边界：不负责 Git 提交、不负责 mirror 同步（由上层流程处理）。
- 上层路由：优先由 `scripts/Cli_Toolbox.py create-skill-from-template` 进入。

## 回归检查
```bash
python3 scripts/create_skill_from_template.py --help
python3 scripts/create_skill_from_template.py --skill-name meta-skill-template-sandbox --target-root ~/AI_Projects/Codex_Skill_Runtime/Meta-Skill-Template --overwrite
```

## 文档同步
- 使用文档已同步：是
- 模块目录已同步：是
