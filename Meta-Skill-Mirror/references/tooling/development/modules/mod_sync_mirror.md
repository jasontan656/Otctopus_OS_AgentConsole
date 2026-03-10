# 模块：cli_toolbox_sync

## 模块标识
- `module_id`: `cli_toolbox_sync`
- `entrypoint`: `scripts/Cli_Toolbox.py`

## 职责
- 将同步动作收敛为单一 CLI 入口。
- 先检查目标是否已存在，再路由到 `Push` 或 `Install`。
- 在 `Push` 模式执行 mirror -> codex 覆盖同步。
- 在 `Install` 模式返回外部技能调用顺序。
- 在需要时将隐藏 mirror 根目录迁移为可见目录。

## 输入合同
- 可选：`--scope`（默认 `all`）
- 条件必填：`--skill-name`（当 `scope=skill`）
- `--skill-name` 支持 nested relative skill path；每段必须满足 `[A-Za-z0-9._-]+`，且禁止 `.` / `..` 越界段与反斜杠。
- 可选：`--mode`（默认 `auto`）

## 输出合同
- 成功：
  - Push:
    - `status=ok`
    - `action=mirror_to_codex`
    - `resolved_mode=push`
    - `scope/source/destination/command`
    - `source_skill_name/destination_skill_name`
  - Install:
    - `status=route_required`
    - `action=install_via_external_skills`
    - `resolved_mode=install`
    - `scope/source/destination/next_skills`
    - `source_skill_name/destination_skill_name`
- 失败：
  - `status=error`
  - `error`

## 失败模式
- 源目录不存在。
- `scope=skill` 且缺少 `--skill-name`。
- `skill-name` 非法字符。
- `skill-name` 包含空段、反斜杠、绝对路径或 `.` / `..` 越界段。
- `mode=install` 但 `scope!=skill`。
- `rsync` 执行失败。
