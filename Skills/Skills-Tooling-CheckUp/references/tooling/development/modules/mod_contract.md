# contract 模块开发文档

## 模块标识
- `module_id`: `contract`
- `tool_alias`: `Cli_Toolbox.contract`
- `entrypoint`: `scripts/Cli_Toolbox.py`

## 职责
- 输出 `Skills-Tooling-CheckUp` 的 runtime contract JSON。
- 作为模型进入本技能时的第一跳。

## 输入输出契约
- 输入：
  - `--json`
- 输出：
  - `references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json` 的 payload
- 失败模式：
  - 合同文件缺失或非法 JSON 时直接失败

## 回归检查
```bash
cd /home/jasontan656/AI_Projects/octopus-os-agent-console/Skills/Skills-Tooling-CheckUp && python3 -m pytest tests/test_cli_toolbox.py
```
