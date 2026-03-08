# 模块：cli_toolbox_sync

## 模块标识
- `module_id`: `cli_toolbox_sync`
- `entrypoint`: `scripts/Cli_Toolbox.py`

## 职责
- 将同步动作收敛为单一 CLI 入口。
- 执行 mirror -> codex 单向同步（全量/单技能）。
- 在需要时将隐藏 mirror 根目录迁移为可见目录。

## 输入合同
- 可选：`--scope`（默认 `all`）
- 条件必填：`--skill-name`（当 `scope=skill`）

## 输出合同
- 成功：
  - `status=ok`
  - `action/scope/source/destination/command`
- 失败：
  - `status=error`
  - `error`

## 失败模式
- 源目录不存在。
- `scope=skill` 且缺少 `--skill-name`。
- `skill-name` 非法字符。
- `rsync` 执行失败。
