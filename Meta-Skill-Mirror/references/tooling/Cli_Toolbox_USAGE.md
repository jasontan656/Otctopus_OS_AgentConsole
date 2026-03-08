# Cli_Toolbox 使用文档

## 命名约束
- 统一入口：`scripts/Cli_Toolbox.py`
- 仅支持唯一动作：`mirror_to_codex`（单向 mirror -> codex）

## 工具清单
- `Cli_Toolbox.sync_mirror_to_codex`

## 同步排除项（固定）
- `Codex_Skill_Runtime/`：运行态临时产物，不参与 mirror -> codex 同步。
- `.git/`、`__pycache__/`、`*.pyc`：仓库与编译缓存噪声，按 rsync exclude 固定过滤。

## 叙事式使用说明（固定格式）
### Cli_Toolbox.sync_mirror_to_codex（全量）
- 人类叙事版输入：
  - “把 mirror 里当前所有技能完整同步回 codex 安装目录。”
  - 命令：
    - `python3 scripts/Cli_Toolbox.py --scope all`
- 电脑动作发生了什么：
  - 解析参数，确认方向是 `mirror -> codex`。
  - 检查 mirror 根目录是否为可见目录；如只存在旧隐藏目录，则自动迁移为可见目录。
  - 执行 `rsync -a --delete`，按目录镜像覆盖目标。
- 人类叙事版输出：
  - 返回结构化 JSON，明确同步方向、源目录、目标目录、实际命令。

### Cli_Toolbox.sync_mirror_to_codex（单技能）
- 人类叙事版输入：
  - “只同步 `3-Octupos-OS` 这个技能到 codex。”
  - 命令：
    - `python3 scripts/Cli_Toolbox.py --scope skill --skill-name 3-Octupos-OS`
- 电脑动作发生了什么：
  - 校验 `skill-name` 只包含允许字符。
  - 源目录锁定为 `<mirror>/<skill>`，目标目录锁定为 `<codex>/<skill>`。
  - 执行 `rsync -a --delete` 同步该技能子树。
- 人类叙事版输出：
  - 返回 `status=ok` 与技能级路径信息。

## 参数说明
- `action`：固定为 `mirror_to_codex`（输出字段）
- `--scope`：`all` 或 `skill`
- `--skill-name`：`scope=skill` 时必填
- `--codex-root`：可选；未提供时按 `CODEX_SKILLS_ROOT`，否则回退到 `$HOME/.codex/skills`
- `--mirror-root`：可选；未提供时按 `CODEX_SKILLS_MIRROR_ROOT` 或自动发现/迁移 mirror 目录
- `--dry-run`：可选，预演同步命令
