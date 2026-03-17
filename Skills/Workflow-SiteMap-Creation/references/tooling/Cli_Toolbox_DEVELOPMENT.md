# Cli_Toolbox Development

## Python Modules

- `scripts/Cli_Toolbox.py`：CLI entrypoint 与命令路由。
- `scripts/cli_support.py`：运行态解析、输出、frontmatter、mirror 通用支持。
- `scripts/factory_support.py`：factory-first 请求拆分与 skill evolution。
- `scripts/intent_support.py`：`$Meta-Enhance-Prompt` 集成与 `INTENT:` 产出。
- `scripts/subagent_support.py`：tmux background subagent 启动、轮询、idle 判死与手工终止。
- `scripts/artifact_support.py`：依据最新 skill 结果与 runtask 证据刷新 truth root / mirror 产物并做 lint。

## Test Surface

- `pytest Skills/Workflow-SiteMap-Creation/tests/test_cli_toolbox.py`
- 测试至少覆盖 contract、reading chain、factory intake、intent enhance、subagent status、self governance write、lint failure path。
