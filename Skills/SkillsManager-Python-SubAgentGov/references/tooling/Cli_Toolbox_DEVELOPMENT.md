---
doc_id: skillsmanager_python_subagentgov.references.tooling.cli_toolbox_development
doc_type: topic_atom
topic: CLI development for SkillsManager-Python-SubAgentGov
---

# Cli_Toolbox Development

## 模块划分
- `scripts/Cli_Toolbox.py`
  - 负责参数解析、命令分发和 JSON 输出。
- `scripts/controller_runtime.py`
  - 负责路径解析、目标发现、prompt 渲染、tmux/codex worker 启动、轮询、验证、Git 收口、mirror 收口与断点恢复。
- `assets/prompt_template.md`
  - 固定的单技能治理 prompt 模板，只做变量替换，不在 CLI 内拼接长文本。

## 设计约束
- controller 逻辑必须保持与 runtime 原型一致的关键行为：
  - `codex exec --json`
  - `tmux` background 守护
  - `gpt-5.4` + `high`
  - 单技能 runtime 隔离
  - 串行 closeout
- 兼容性保护必须保留：
  - `verification_commands` 同时兼容字符串和对象 schema
  - `result.json` 读取时必须容忍部分写入并短重试

## 测试建议
- CLI 回归测试至少覆盖：
  - contract 命令
  - target discovery
  - runtime status 汇总
  - prompt 渲染
- 运行时 helper 回归测试至少覆盖：
  - `expected_exit_code()` 的双 schema 兼容
  - `load_result()` 的 partial JSON retry
