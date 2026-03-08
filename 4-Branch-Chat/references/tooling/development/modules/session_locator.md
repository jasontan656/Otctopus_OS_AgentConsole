# session_locator 模块开发文档

## 模块标识
- `module_id`: `session_locator`
- `tool_alias`: `Cli_Toolbox.locate_session`
- `entrypoint`: `scripts/branch_chat_toolbox.py locate-session`

## 职责
- 解析 Codex 根目录并定位目标 `session_id` 对应的 JSONL 文件。

## 输入输出契约
- 输入：`session_id`, optional `codex_home`
- 输出：`status`, `codex_home`, `session_files`, `file_count`
- 失败模式：
  - 根目录不存在
  - `session_id` 未命中任何日志文件

## 回归检查
```bash
python3 scripts/branch_chat_toolbox.py locate-session --session-id 019c9775-52cb-7b83-a15c-5fafb7998f2f
```
